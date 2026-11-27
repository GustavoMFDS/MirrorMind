"""Bounded local evidence retrieval contracts and implementations."""

from mirrormind.modules.retrieval.contracts import (
    EvidenceAccessContext,
    EvidenceCitation,
    EvidenceDocument,
    EvidenceQuery,
    EvidenceRetrievalResult,
    RetrievedEvidence,
)
from mirrormind.modules.retrieval.index import InMemoryEvidenceIndex

__all__ = (
    "EvidenceAccessContext",
    "EvidenceCitation",
    "EvidenceDocument",
    "EvidenceQuery",
    "EvidenceRetrievalResult",
    "InMemoryEvidenceIndex",
    "RetrievedEvidence",
)
