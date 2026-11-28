"""Bounded local retrieval and synthetic evaluation contracts."""

from mirrormind.modules.retrieval.contracts import (
    EvidenceAccessContext,
    EvidenceCitation,
    EvidenceDocument,
    EvidenceQuery,
    EvidenceRetrievalResult,
    RetrievedEvidence,
)
from mirrormind.modules.retrieval.evaluation import (
    MAX_EVALUATION_CASES,
    RetrievalCaseOutcome,
    RetrievalEvaluationCase,
    RetrievalEvaluationReport,
    run_retrieval_evaluation,
)
from mirrormind.modules.retrieval.index import InMemoryEvidenceIndex

__all__ = (
    "MAX_EVALUATION_CASES",
    "EvidenceAccessContext",
    "EvidenceCitation",
    "EvidenceDocument",
    "EvidenceQuery",
    "EvidenceRetrievalResult",
    "InMemoryEvidenceIndex",
    "RetrievalCaseOutcome",
    "RetrievalEvaluationCase",
    "RetrievalEvaluationReport",
    "RetrievedEvidence",
    "run_retrieval_evaluation",
)
