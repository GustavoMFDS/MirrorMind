"""Bounded synthetic evaluation for the experimental local retrieval index."""

from __future__ import annotations

from hashlib import sha256
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StrictBool,
    StrictInt,
    field_validator,
    model_validator,
)

from mirrormind.modules.retrieval.contracts import (
    EvidenceAccessContext,
    EvidenceCitation,
    EvidenceDocument,
    EvidenceQuery,
    EvidenceRetrievalResult,
    Identifier,
)
from mirrormind.modules.retrieval.index import MAX_INDEX_DOCUMENTS, InMemoryEvidenceIndex

MAX_EVALUATION_CASES = 100


class _EvaluationModel(BaseModel):
    """Immutable, non-coercing base for local evaluation contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class RetrievalEvaluationCase(_EvaluationModel):
    """One declared fictional query, caller scope and relevant-document set."""

    case_id: Identifier
    access: EvidenceAccessContext
    query: EvidenceQuery
    relevant_document_ids: tuple[Identifier, ...] = Field(max_length=MAX_INDEX_DOCUMENTS)

    @field_validator("relevant_document_ids")
    @classmethod
    def require_unique_relevance_labels(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("relevance document identifiers must be unique")
        return value


class RetrievalCaseOutcome(_EvaluationModel):
    """Query-free case counts and citation refs verified against visible data."""

    case_index: StrictInt = Field(ge=0, lt=MAX_EVALUATION_CASES)
    top_k: StrictInt = Field(ge=1, le=10)
    expected_relevant_document_count: StrictInt = Field(ge=0)
    retrieved_count: StrictInt = Field(ge=0, le=10)
    relevant_retrieved_document_count: StrictInt = Field(ge=0, le=MAX_INDEX_DOCUMENTS)
    expected_abstention: StrictBool
    abstained: StrictBool
    lineage_match_count: StrictInt = Field(ge=0, le=10)
    supported_citation_count: StrictInt = Field(ge=0, le=10)
    out_of_scope_hit_count: StrictInt = Field(ge=0, le=10)
    verified_citations: tuple[EvidenceCitation, ...] = Field(max_length=10)

    @model_validator(mode="after")
    def require_consistent_counts(self) -> RetrievalCaseOutcome:
        if self.relevant_retrieved_document_count > self.expected_relevant_document_count:
            raise ValueError("relevant result count cannot exceed relevance labels")
        if self.lineage_match_count > self.retrieved_count:
            raise ValueError("lineage count cannot exceed retrieved count")
        if self.supported_citation_count != len(self.verified_citations):
            raise ValueError("verified citation count must match citation list")
        if self.supported_citation_count > self.lineage_match_count:
            raise ValueError("supported citations must have matching lineage")
        if self.out_of_scope_hit_count > self.retrieved_count:
            raise ValueError("scope violations cannot exceed retrieved count")
        if self.abstained != (self.retrieved_count == 0):
            raise ValueError("abstention must match an empty retrieval result")
        if self.expected_abstention != (self.expected_relevant_document_count == 0):
            raise ValueError("expected abstention must match empty relevance labels")
        return self


class RetrievalEvaluationReport(_EvaluationModel):
    """Aggregate retrieval metrics with explicit counts and no query text."""

    schema_version: Literal["m2_retrieval_eval_v1"] = "m2_retrieval_eval_v1"
    retrieval_algorithm: Literal["bm25_lexical_v1"] = "bm25_lexical_v1"
    case_count: StrictInt = Field(ge=1, le=MAX_EVALUATION_CASES)
    relevant_query_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    relevant_query_hit_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    expected_relevant_document_count: StrictInt = Field(ge=0)
    relevant_retrieved_document_count: StrictInt = Field(ge=0)
    recall_at_k: FiniteFloat | None = Field(default=None, ge=0.0, le=1.0)
    relevant_query_hit_rate: FiniteFloat | None = Field(default=None, ge=0.0, le=1.0)
    expected_abstention_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    correct_abstention_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    correct_abstention_rate: FiniteFloat | None = Field(default=None, ge=0.0, le=1.0)
    missed_relevant_query_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    unexpected_hit_query_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    abstained_query_count: StrictInt = Field(ge=0, le=MAX_EVALUATION_CASES)
    abstention_rate: FiniteFloat = Field(ge=0.0, le=1.0)
    citation_count: StrictInt = Field(ge=0)
    lineage_match_count: StrictInt = Field(ge=0)
    lineage_match_rate: FiniteFloat | None = Field(default=None, ge=0.0, le=1.0)
    supported_citation_count: StrictInt = Field(ge=0)
    citation_support_rate: FiniteFloat | None = Field(default=None, ge=0.0, le=1.0)
    out_of_scope_hit_count: StrictInt = Field(ge=0)
    scope_compliance_rate: FiniteFloat | None = Field(default=None, ge=0.0, le=1.0)
    cases: tuple[RetrievalCaseOutcome, ...] = Field(
        min_length=1, max_length=MAX_EVALUATION_CASES
    )

    @model_validator(mode="after")
    def require_consistent_aggregate_counts(self) -> RetrievalEvaluationReport:
        if len(self.cases) != self.case_count:
            raise ValueError("case count must match case outcomes")
        if self.relevant_query_hit_count > self.relevant_query_count:
            raise ValueError("relevant query hits cannot exceed relevant queries")
        if self.relevant_retrieved_document_count > self.expected_relevant_document_count:
            raise ValueError("retrieved relevant documents cannot exceed labels")
        if self.correct_abstention_count > self.expected_abstention_count:
            raise ValueError("correct abstentions cannot exceed expected abstentions")
        if self.lineage_match_count > self.citation_count:
            raise ValueError("lineage matches cannot exceed citations")
        if self.supported_citation_count > self.lineage_match_count:
            raise ValueError("supported citations must have matching lineage")
        if self.out_of_scope_hit_count > self.citation_count:
            raise ValueError("scope violations cannot exceed citations")
        if sum(case.retrieved_count for case in self.cases) != self.citation_count:
            raise ValueError("citation count must match case outcomes")
        return self


def run_retrieval_evaluation(
    documents: tuple[EvidenceDocument, ...] | list[EvidenceDocument],
    cases: tuple[RetrievalEvaluationCase, ...] | list[RetrievalEvaluationCase],
) -> RetrievalEvaluationReport:
    """Evaluate a bounded declared test set against the fictional lexical index.

    The function rebuilds the index under each case's access context. It
    records only aggregate counts and citation references that resolve to a
    visible document, match its source lineage and reproduce the exact excerpt
    span and digest. Query text, excerpt text and scope-violating identifiers
    never enter the report.
    """
    if type(cases) not in (tuple, list):
        raise TypeError("cases must be a bounded list or tuple")
    if not cases:
        raise ValueError("evaluation cases must be non-empty")
    if len(cases) > MAX_EVALUATION_CASES:
        raise ValueError("evaluation case limit exceeded")
    if any(type(case) is not RetrievalEvaluationCase for case in cases):
        raise TypeError("cases must contain exact RetrievalEvaluationCase values")
    case_ids = tuple(case.case_id for case in cases)
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("evaluation case identifiers must be unique")

    if type(documents) not in (tuple, list):
        raise TypeError("documents must be a bounded list or tuple")
    if not documents:
        raise ValueError("evaluation documents must be non-empty")

    # Reuse the index's document and duplicate-ID validation without tokenizing
    # any content during evaluation preflight.
    preflight_scope = EvidenceAccessContext(
        principal_id="evaluation-preflight",
        allowed_collection_ids=(),
    )
    InMemoryEvidenceIndex.build(documents, preflight_scope)
    document_by_id = {document.document_id: document for document in documents}

    outcomes: list[RetrievalCaseOutcome] = []
    for case_index, case in enumerate(cases):
        relevant_ids = frozenset(case.relevant_document_ids)
        if any(
            document_id not in document_by_id
            or not _is_visible(document_by_id[document_id], case)
            for document_id in relevant_ids
        ):
            raise ValueError(
                "relevance labels must resolve within the declared visible corpus"
            )

        index = InMemoryEvidenceIndex.build(documents, case.access)
        result = index.search(case.query)
        if type(result) is not EvidenceRetrievalResult:
            raise TypeError("retrieval must return an exact EvidenceRetrievalResult")
        if len(result.hits) > case.query.top_k:
            raise ValueError("retrieval result exceeds the declared top_k")
        supported_ids: set[str] = set()
        verified_citations: list[EvidenceCitation] = []
        lineage_match_count = 0
        out_of_scope_hit_count = 0

        for hit in result.hits:
            document = document_by_id.get(hit.citation.document_id)
            if document is None or not _is_visible(document, case):
                # Do not serialize identifiers or refs from an unauthorized hit.
                out_of_scope_hit_count += 1
                continue

            if _matches_document_lineage(hit.citation, document):
                lineage_match_count += 1
            if _citation_is_supported(hit.excerpt, hit.citation, document):
                verified_citations.append(hit.citation)
                if hit.citation.document_id in relevant_ids:
                    supported_ids.add(hit.citation.document_id)

        outcomes.append(
            RetrievalCaseOutcome(
                case_index=case_index,
                top_k=case.query.top_k,
                expected_relevant_document_count=len(relevant_ids),
                retrieved_count=len(result.hits),
                relevant_retrieved_document_count=len(supported_ids),
                expected_abstention=not relevant_ids,
                abstained=not result.hits,
                lineage_match_count=lineage_match_count,
                supported_citation_count=len(verified_citations),
                out_of_scope_hit_count=out_of_scope_hit_count,
                verified_citations=tuple(verified_citations),
            )
        )

    case_count = len(outcomes)
    relevant_cases = tuple(
        outcome for outcome in outcomes if outcome.expected_relevant_document_count > 0
    )
    expected_abstentions = tuple(
        outcome for outcome in outcomes if outcome.expected_abstention
    )
    expected_relevance_count = sum(
        outcome.expected_relevant_document_count for outcome in outcomes
    )
    relevant_retrieved_count = sum(
        outcome.relevant_retrieved_document_count for outcome in outcomes
    )
    relevant_hit_count = sum(
        outcome.relevant_retrieved_document_count > 0 for outcome in relevant_cases
    )
    correct_abstention_count = sum(
        outcome.abstained for outcome in expected_abstentions
    )
    missed_relevant_count = sum(
        outcome.relevant_retrieved_document_count == 0 for outcome in relevant_cases
    )
    unexpected_hit_count = sum(
        outcome.expected_abstention and outcome.retrieved_count > 0 for outcome in outcomes
    )
    abstained_count = sum(outcome.abstained for outcome in outcomes)
    citation_count = sum(outcome.retrieved_count for outcome in outcomes)
    lineage_count = sum(outcome.lineage_match_count for outcome in outcomes)
    supported_count = sum(outcome.supported_citation_count for outcome in outcomes)
    out_of_scope_count = sum(outcome.out_of_scope_hit_count for outcome in outcomes)

    return RetrievalEvaluationReport(
        case_count=case_count,
        relevant_query_count=len(relevant_cases),
        relevant_query_hit_count=relevant_hit_count,
        expected_relevant_document_count=expected_relevance_count,
        relevant_retrieved_document_count=relevant_retrieved_count,
        recall_at_k=_rate(relevant_retrieved_count, expected_relevance_count),
        relevant_query_hit_rate=_rate(relevant_hit_count, len(relevant_cases)),
        expected_abstention_count=len(expected_abstentions),
        correct_abstention_count=correct_abstention_count,
        correct_abstention_rate=_rate(
            correct_abstention_count, len(expected_abstentions)
        ),
        missed_relevant_query_count=missed_relevant_count,
        unexpected_hit_query_count=unexpected_hit_count,
        abstained_query_count=abstained_count,
        abstention_rate=_rate(abstained_count, case_count) or 0.0,
        citation_count=citation_count,
        lineage_match_count=lineage_count,
        lineage_match_rate=_rate(lineage_count, citation_count),
        supported_citation_count=supported_count,
        citation_support_rate=_rate(supported_count, citation_count),
        out_of_scope_hit_count=out_of_scope_count,
        scope_compliance_rate=_rate(citation_count - out_of_scope_count, citation_count),
        cases=tuple(outcomes),
    )


def _is_visible(document: EvidenceDocument, case: RetrievalEvaluationCase) -> bool:
    """Apply both caller-declared access and requested collection scope."""
    if document.collection_id not in case.access.allowed_collection_ids:
        return False
    if case.access.principal_id not in document.allowed_principals:
        return False
    return (
        case.query.collection_ids is None
        or document.collection_id in case.query.collection_ids
    )


def _matches_document_lineage(
    citation: EvidenceCitation, document: EvidenceDocument
) -> bool:
    """Check that a citation names the exact visible fixture and snapshot."""
    return (
        citation.document_id == document.document_id
        and citation.collection_id == document.collection_id
        and citation.source_ref == document.source_ref
        and citation.snapshot_ref == document.snapshot_ref
    )


def _citation_is_supported(
    excerpt: str, citation: EvidenceCitation, document: EvidenceDocument
) -> bool:
    """Verify lineage, code-point span, exact excerpt and UTF-8 digest."""
    if not _matches_document_lineage(citation, document):
        return False
    if citation.end_offset > len(document.content):
        return False
    source_excerpt = document.content[citation.start_offset : citation.end_offset]
    if source_excerpt != excerpt:
        return False
    return citation.excerpt_sha256 == sha256(excerpt.encode("utf-8")).hexdigest()


def _rate(numerator: int, denominator: int) -> float | None:
    """Return a stable six-decimal descriptive rate or null if undefined."""
    if denominator == 0:
        return None
    return round(numerator / denominator, 6)
