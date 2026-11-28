"""Immutable, permission-filtered lexical index over bounded local documents."""

from __future__ import annotations

import math
import re
from bisect import bisect_left
from collections.abc import Iterator
from dataclasses import dataclass
from hashlib import sha256

from mirrormind.modules.retrieval.contracts import (
    EvidenceAccessContext,
    EvidenceCitation,
    EvidenceDocument,
    EvidenceQuery,
    EvidenceRetrievalResult,
    RetrievedEvidence,
)

MAX_INDEX_DOCUMENTS = 100
EXCERPT_MAX_CHARS = 480
_TOKEN = re.compile(r"[^\W_]+", flags=re.UNICODE)
_BM25_K1 = 1.2
_BM25_B = 0.75


@dataclass(frozen=True, slots=True)
class _IndexedDocument:
    document: EvidenceDocument
    token_count: int
    term_counts: tuple[tuple[str, int, int], ...]


def _token_spans(text: str) -> Iterator[tuple[str, int]]:
    """Stream casefolded words with exact starting code-point offsets."""
    for match in _TOKEN.finditer(text):
        yield match.group(0).casefold(), match.start()


@dataclass(frozen=True, slots=True)
class InMemoryEvidenceIndex:
    """A read-only index containing only records visible to its build context."""

    _documents: tuple[_IndexedDocument, ...]
    _document_frequency: tuple[tuple[str, int], ...]

    @classmethod
    def build(
        cls,
        documents: tuple[EvidenceDocument, ...] | list[EvidenceDocument],
        access: EvidenceAccessContext,
    ) -> InMemoryEvidenceIndex:
        """Filter scope first, then tokenize only documents caller may see."""
        if type(access) is not EvidenceAccessContext:
            raise TypeError("access must be an exact EvidenceAccessContext")
        if type(documents) not in (tuple, list):
            raise TypeError("documents must be a bounded list or tuple")
        if len(documents) > MAX_INDEX_DOCUMENTS:
            raise ValueError("document limit exceeded")
        if any(type(document) is not EvidenceDocument for document in documents):
            raise TypeError("documents must contain exact EvidenceDocument values")
        document_ids = tuple(document.document_id for document in documents)
        if len(document_ids) != len(set(document_ids)):
            raise ValueError("document identifiers must be unique")

        allowed_collections = frozenset(access.allowed_collection_ids)
        visible = tuple(
            document
            for document in documents
            if document.collection_id in allowed_collections
            and access.principal_id in document.allowed_principals
        )

        indexed: list[_IndexedDocument] = []
        document_frequency: dict[str, int] = {}
        for document in visible:
            token_count = 0
            counts: dict[str, list[int]] = {}
            for term, start in _token_spans(document.content):
                token_count += 1
                entry = counts.get(term)
                if entry is None:
                    counts[term] = [1, start]
                else:
                    entry[0] += 1
            indexed.append(
                _IndexedDocument(
                    document=document,
                    token_count=token_count,
                    term_counts=tuple(sorted(
                        (term, count, first) for term, (count, first) in counts.items()
                    )),
                )
            )
            for term in counts:
                document_frequency[term] = document_frequency.get(term, 0) + 1

        return cls(
            _documents=tuple(indexed),
            _document_frequency=tuple(sorted(document_frequency.items())),
        )

    def search(self, query: EvidenceQuery) -> EvidenceRetrievalResult:
        """Run deterministic BM25 over pre-filtered documents and return exact citations."""
        if type(query) is not EvidenceQuery:
            raise TypeError("query must be an exact EvidenceQuery")
        query_terms = tuple(dict.fromkeys(term for term, _ in _token_spans(query.text)))
        if not query_terms or not self._documents:
            return _empty_result()

        requested_collections = (
            frozenset(query.collection_ids) if query.collection_ids is not None else None
        )
        candidates = tuple(
            item
            for item in self._documents
            if requested_collections is None
            or item.document.collection_id in requested_collections
        )
        if not candidates:
            return _empty_result()

        total_documents = len(self._documents)
        weighted_terms = []
        for term in query_terms:
            document_frequency = _frequency(self._document_frequency, term)
            if document_frequency:
                inverse_frequency = math.log(
                    1.0
                    + (total_documents - document_frequency + 0.5)
                    / (document_frequency + 0.5)
                )
                weighted_terms.append((term, inverse_frequency))
        if not weighted_terms:
            return _empty_result()
        average_length = sum(item.token_count for item in self._documents) / total_documents
        average_length = max(average_length, 1.0)
        ranked: list[tuple[float, _IndexedDocument]] = []
        for item in candidates:
            document_length = item.token_count
            score = 0.0
            for term, inverse_frequency in weighted_terms:
                entry = _term_entry(item.term_counts, term)
                if entry is None:
                    continue
                term_frequency = entry[1]
                denominator = term_frequency + _BM25_K1 * (
                    1.0 - _BM25_B + _BM25_B * document_length / average_length
                )
                score += inverse_frequency * (
                    term_frequency * (_BM25_K1 + 1.0) / denominator
                )
            if score > 0.0:
                ranked.append((score, item))

        ranked.sort(key=lambda pair: (-pair[0], pair[1].document.document_id))
        hits = tuple(
            _make_hit(score, item, frozenset(query_terms))
            for score, item in ranked[: query.top_k]
        )
        return EvidenceRetrievalResult(
            status="results" if hits else "no_matches",
            algorithm="bm25_lexical_v1",
            hits=hits,
        )


def _frequency(counts: tuple[tuple[str, int], ...], term: str) -> int:
    """Find one term in the immutable, sorted frequency table."""
    position = bisect_left(counts, (term, 0))
    if position < len(counts) and counts[position][0] == term:
        return counts[position][1]
    return 0


def _term_entry(
    counts: tuple[tuple[str, int, int], ...], term: str
) -> tuple[str, int, int] | None:
    """Return frequency and earliest code-point offset for a term."""
    position = bisect_left(counts, (term, 0, 0))
    if position < len(counts) and counts[position][0] == term:
        return counts[position]
    return None


def _empty_result() -> EvidenceRetrievalResult:
    return EvidenceRetrievalResult(
        status="no_matches",
        algorithm="bm25_lexical_v1",
        hits=(),
    )


def _make_hit(
    score: float,
    item: _IndexedDocument,
    query_terms: frozenset[str],
) -> RetrievedEvidence:
    first = min(
        entry[2] for term in query_terms
        if (entry := _term_entry(item.term_counts, term)) is not None
    )
    content = item.document.content
    start = max(0, first - EXCERPT_MAX_CHARS // 4)
    end = min(len(content), start + EXCERPT_MAX_CHARS)
    if end - start < EXCERPT_MAX_CHARS:
        start = max(0, end - EXCERPT_MAX_CHARS)
    excerpt = content[start:end]
    citation = EvidenceCitation(
        document_id=item.document.document_id,
        collection_id=item.document.collection_id,
        source_ref=item.document.source_ref,
        snapshot_ref=item.document.snapshot_ref,
        start_offset=start,
        end_offset=end,
        excerpt_sha256=sha256(excerpt.encode("utf-8")).hexdigest(),
    )
    return RetrievedEvidence(
        excerpt=excerpt,
        score=round(score, 6),
        citation=citation,
        trust_label="untrusted_evidence",
    )
