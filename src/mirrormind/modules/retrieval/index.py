"""Immutable, permission-filtered lexical index over bounded local documents."""

from __future__ import annotations

import math
import re
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
class _TokenSpan:
    term: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class _IndexedDocument:
    document: EvidenceDocument
    tokens: tuple[_TokenSpan, ...]
    term_counts: tuple[tuple[str, int], ...]


def _token_spans(text: str) -> tuple[_TokenSpan, ...]:
    """Tokenize Unicode words while retaining exact source offsets."""
    return tuple(
        _TokenSpan(match.group(0).casefold(), match.start(), match.end())
        for match in _TOKEN.finditer(text)
    )


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
            tokens = _token_spans(document.content)
            counts: dict[str, int] = {}
            for token in tokens:
                counts[token.term] = counts.get(token.term, 0) + 1
            indexed.append(
                _IndexedDocument(
                    document=document,
                    tokens=tokens,
                    term_counts=tuple(sorted(counts.items())),
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
        query_terms = tuple(dict.fromkeys(token.term for token in _token_spans(query.text)))
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

        count_by_term = dict(self._document_frequency)
        total_documents = len(self._documents)
        average_length = sum(len(item.tokens) for item in self._documents) / total_documents
        average_length = max(average_length, 1.0)
        ranked: list[tuple[float, _IndexedDocument]] = []
        for item in candidates:
            counts = dict(item.term_counts)
            document_length = len(item.tokens)
            score = 0.0
            for term in query_terms:
                term_frequency = counts.get(term, 0)
                if term_frequency == 0:
                    continue
                document_frequency = count_by_term[term]
                inverse_frequency = math.log(
                    1.0
                    + (total_documents - document_frequency + 0.5)
                    / (document_frequency + 0.5)
                )
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
    matching = next(token for token in item.tokens if token.term in query_terms)
    content = item.document.content
    start = max(0, matching.start - EXCERPT_MAX_CHARS // 4)
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
