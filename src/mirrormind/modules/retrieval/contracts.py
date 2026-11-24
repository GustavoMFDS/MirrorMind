"""Strict versioned contracts for local evidence retrieval."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    StrictInt,
    StrictStr,
    StringConstraints,
    field_validator,
    model_validator,
)

Identifier = Annotated[
    StrictStr,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=128,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$",
    ),
]
Digest = Annotated[StrictStr, StringConstraints(pattern=r"^[0-9a-f]{64}$")]


class _RetrievalModel(BaseModel):
    """Share immutable, non-coercing validation across retrieval contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class EvidenceDocument(_RetrievalModel):
    """One bounded fictional document with caller-declared visibility scope."""

    document_id: Identifier
    collection_id: Identifier
    source_ref: Identifier
    snapshot_ref: Identifier
    content: Annotated[StrictStr, StringConstraints(min_length=1, max_length=12_000)]
    allowed_principals: tuple[Identifier, ...] = Field(min_length=1, max_length=32)
    source_status: Literal["fictional_fixture"] = "fictional_fixture"

    @field_validator("content")
    @classmethod
    def reject_unsafe_controls(cls, value: str) -> str:
        if any(ord(character) < 32 and character not in "\t\n\r" for character in value):
            raise ValueError("document content contains a forbidden control character")
        return value

    @field_validator("allowed_principals")
    @classmethod
    def require_unique_principals(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("allowed principals must be unique")
        return value


class EvidenceAccessContext(_RetrievalModel):
    """Trusted-caller scope; not an authenticated identity or permission grant."""

    principal_id: Identifier
    allowed_collection_ids: tuple[Identifier, ...] = Field(max_length=16)

    @field_validator("allowed_collection_ids")
    @classmethod
    def require_unique_collections(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("allowed collections must be unique")
        return value


class EvidenceQuery(_RetrievalModel):
    """Bounded lexical query and optional subset of caller-visible collections."""

    text: Annotated[StrictStr, StringConstraints(min_length=1, max_length=512)]
    top_k: StrictInt = Field(default=5, ge=1, le=10)
    collection_ids: tuple[Identifier, ...] | None = Field(default=None, max_length=16)

    @field_validator("text")
    @classmethod
    def normalize_and_bound_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("query text must contain non-whitespace characters")
        if any(ord(character) < 32 for character in normalized):
            raise ValueError("query text must not contain control characters")
        return normalized

    @field_validator("collection_ids")
    @classmethod
    def require_unique_query_collections(
        cls, value: tuple[str, ...] | None
    ) -> tuple[str, ...] | None:
        if value is not None and len(value) != len(set(value)):
            raise ValueError("query collections must be unique")
        return value


class EvidenceCitation(_RetrievalModel):
    """Exact source pointer for one excerpt, using Python Unicode code-point offsets."""

    document_id: Identifier
    collection_id: Identifier
    source_ref: Identifier
    snapshot_ref: Identifier
    start_offset: StrictInt = Field(ge=0)
    end_offset: StrictInt = Field(ge=1)
    excerpt_sha256: Digest

    @model_validator(mode="after")
    def require_nonempty_span(self) -> EvidenceCitation:
        if self.end_offset <= self.start_offset:
            raise ValueError("citation span must be nonempty and forward")
        return self


class RetrievedEvidence(_RetrievalModel):
    """Retrieved text stays explicitly untrusted and carries a verifiable citation."""

    excerpt: Annotated[StrictStr, StringConstraints(min_length=1, max_length=480)]
    score: FiniteFloat = Field(gt=0)
    citation: EvidenceCitation
    trust_label: Literal["untrusted_evidence"]

    @model_validator(mode="after")
    def require_exact_cited_excerpt_length(self) -> RetrievedEvidence:
        if len(self.excerpt) != self.citation.end_offset - self.citation.start_offset:
            raise ValueError("citation offsets must exactly cover the excerpt")
        return self


class EvidenceRetrievalResult(_RetrievalModel):
    """Versioned result envelope; query text and denied-record metadata are omitted."""

    status: Literal["results", "no_matches"]
    algorithm: Literal["bm25_lexical_v1"]
    hits: tuple[RetrievedEvidence, ...] = Field(max_length=10)

    @model_validator(mode="after")
    def match_status_to_hits(self) -> EvidenceRetrievalResult:
        if (self.status == "results") != bool(self.hits):
            raise ValueError("result status must match whether hits are present")
        return self
