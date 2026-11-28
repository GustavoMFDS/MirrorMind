"""Strict wire-shaped contracts for bounded in-process tool orchestration."""
from __future__ import annotations

import math
from hashlib import sha256
from typing import Annotated, Literal, Protocol, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    StrictStr,
    StringConstraints,
    field_validator,
    model_validator,
)

MAX_TOOL_CALLS = 2
MAX_PROVIDER_TURNS = 3
MAX_TOOL_OUTPUT_BYTES = 16_384
MAX_PROVIDER_CONTEXT_BYTES = 65_536

ToolName = Annotated[
    StrictStr,
    StringConstraints(min_length=1, max_length=64, pattern=r"^[a-z][a-z0-9_.-]*$"),
]
CallId = Annotated[
    StrictStr,
    StringConstraints(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9._-]+$"),
]
Sha256 = Annotated[StrictStr, StringConstraints(pattern=r"^[0-9a-f]{64}$")]


class _AgentModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class AgentRunRequest(_AgentModel):
    """One caller-declared local run; scope is not authenticated identity."""

    question: Annotated[
        StrictStr,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    ]
    allowed_tool_names: tuple[ToolName, ...] = Field(
        default=("search_synthetic_evidence", "run_synthetic_retail_decision"),
        max_length=MAX_TOOL_CALLS,
    )
    max_tool_calls: StrictInt = Field(default=MAX_TOOL_CALLS, ge=0, le=MAX_TOOL_CALLS)
    max_provider_turns: StrictInt = Field(
        default=MAX_PROVIDER_TURNS, ge=1, le=MAX_PROVIDER_TURNS
    )

    @field_validator("question")
    @classmethod
    def reject_question_controls(cls, value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("question must not contain control characters")
        return value

    @field_validator("allowed_tool_names")
    @classmethod
    def require_unique_tools(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("allowed tool names must be unique")
        return value


class ToolCall(_AgentModel):
    """Untrusted provider request to invoke one named tool with JSON inputs."""

    call_id: CallId
    tool_name: ToolName
    arguments: dict[StrictStr, object] = Field(max_length=16)

    @field_validator("arguments")
    @classmethod
    def require_bounded_json_values(cls, value: dict[str, object]) -> dict[str, object]:
        visited = 0

        def inspect(item: object, depth: int, ancestors: frozenset[int]) -> None:
            nonlocal visited
            visited += 1
            if visited > 256 or depth > 8:
                raise ValueError("tool arguments exceed the JSON nesting budget")
            if item is None or type(item) is bool:
                return
            if type(item) is int:
                if abs(item) > (1 << 63) - 1:
                    raise ValueError("tool integer arguments exceed the safe bound")
                return
            if type(item) is float:
                if not math.isfinite(item):
                    raise ValueError("tool numeric arguments must be finite")
                return
            if type(item) is str:
                if len(item) > 8_192:
                    raise ValueError("tool string argument exceeds the size bound")
                return
            if type(item) is list:
                list_values = cast(list[object], item)
                identity = id(item)
                if identity in ancestors or len(list_values) > 64:
                    raise ValueError("tool JSON arguments contain a cycle or oversized container")
                next_ancestors = ancestors | {identity}
                for child in list_values:
                    inspect(child, depth + 1, next_ancestors)
                return
            if type(item) is dict:
                dict_values = cast(dict[object, object], item)
                identity = id(item)
                if identity in ancestors or len(dict_values) > 64:
                    raise ValueError("tool JSON arguments contain a cycle or oversized container")
                next_ancestors = ancestors | {identity}
                for key, child in dict_values.items():
                    if type(key) is not str or len(key) > 128:
                        raise ValueError("tool JSON object keys must be bounded strings")
                    inspect(child, depth + 1, next_ancestors)
                return
            raise ValueError("tool arguments must contain only JSON values")

        for key, item in value.items():
            if len(key) > 128:
                raise ValueError("tool JSON object keys must be bounded strings")
            inspect(item, 1, frozenset({id(value)}))
        return value


class AgentDraft(_AgentModel):
    """Provider text remains a draft; citations are checked for membership only."""

    status: Literal["draft_for_human_review", "insufficient_evidence"]
    summary: Annotated[
        StrictStr,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=1_000),
    ]
    citation_refs: tuple[Sha256, ...] = Field(max_length=10)

    @field_validator("citation_refs")
    @classmethod
    def require_unique_citations(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(value) != len(set(value)):
            raise ValueError("citation references must be unique")
        return value

    @model_validator(mode="after")
    def match_status_to_citations(self) -> AgentDraft:
        if self.status == "draft_for_human_review" and not self.citation_refs:
            raise ValueError("review drafts require at least one observed citation")
        if self.status == "insufficient_evidence" and self.citation_refs:
            raise ValueError("insufficient-evidence responses cannot cite unsupported data")
        return self


class AgentTurn(_AgentModel):
    """Exactly one provider action: request one tool or return a bounded draft."""

    kind: Literal["tool_call", "final"]
    tool_call: ToolCall | None = None
    final: AgentDraft | None = None

    @model_validator(mode="after")
    def require_matching_payload(self) -> AgentTurn:
        if self.kind == "tool_call" and (self.tool_call is None or self.final is not None):
            raise ValueError("tool-call turns require only a tool_call payload")
        if self.kind == "final" and (self.final is None or self.tool_call is not None):
            raise ValueError("final turns require only a final payload")
        return self


class ToolDescriptor(_AgentModel):
    """Safe static tool help sent to the provider; never contains a handler."""

    name: ToolName
    description: Annotated[StrictStr, StringConstraints(min_length=1, max_length=240)]
    input_fields: tuple[StrictStr, ...] = Field(min_length=1, max_length=16)


class ToolObservation(_AgentModel):
    """Immutable JSON tool bytes, digest and trust boundary for one provider turn."""

    call_id: CallId
    tool_name: ToolName
    output_json: Annotated[
        StrictStr,
        StringConstraints(min_length=2, max_length=MAX_TOOL_OUTPUT_BYTES),
    ]
    output_sha256: Sha256
    trust_label: Literal["untrusted_tool_output"] = "untrusted_tool_output"

    @model_validator(mode="after")
    def verify_output_digest(self) -> ToolObservation:
        if sha256(self.output_json.encode("utf-8")).hexdigest() != self.output_sha256:
            raise ValueError("tool observation digest must match exact UTF-8 JSON")
        return self


class ProviderRequest(_AgentModel):
    """Bounded provider context; observations remain explicitly untrusted."""

    question: Annotated[
        StrictStr,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=512),
    ]
    turn_index: StrictInt = Field(ge=0, lt=MAX_PROVIDER_TURNS)
    available_tools: tuple[ToolDescriptor, ...] = Field(max_length=MAX_TOOL_CALLS)
    observations: tuple[ToolObservation, ...] = Field(max_length=MAX_TOOL_CALLS)


class ToolReceipt(_AgentModel):
    """Minimized successful-call record; raw arguments and outputs are omitted."""

    call_id: CallId
    tool_name: ToolName
    input_sha256: Sha256
    output_sha256: Sha256
    output_bytes: StrictInt = Field(ge=0, le=MAX_TOOL_OUTPUT_BYTES)


RefusalCode = Literal[
    "provider_not_authorized",
    "provider_failure",
    "invalid_provider_turn",
    "provider_context_too_large",
    "provider_turn_budget_exhausted",
    "tool_call_budget_exhausted",
    "tool_not_registered",
    "tool_not_allowed",
    "duplicate_tool_call_id",
    "invalid_tool_input",
    "invalid_tool_output",
    "tool_input_too_large",
    "tool_output_too_large",
    "tool_failed",
    "unsupported_evidence_reference",
]


class AgentRunReport(_AgentModel):
    """Query-free, non-persisted receipt; a completed draft is never approval."""

    schema_version: Literal["mirrormind.local_tool_orchestration.v1"] = (
        "mirrormind.local_tool_orchestration.v1"
    )
    status: Literal["completed", "abstained", "refused"]
    provider_mode: Literal["test_double", "rejected"]
    provider_turn_count: StrictInt = Field(ge=0, le=MAX_PROVIDER_TURNS)
    tool_call_count: StrictInt = Field(ge=0, le=MAX_PROVIDER_TURNS)
    tool_receipts: tuple[ToolReceipt, ...] = Field(max_length=MAX_TOOL_CALLS)
    draft: AgentDraft | None = None
    draft_trust_label: Literal["untrusted_provider_draft"] | None = None
    refusal_code: RefusalCode | None = None
    human_review_required: Literal[True] = True
    action_authorized: Literal[False] = False
    writes_performed: Literal[False] = False

    @model_validator(mode="after")
    def require_consistent_run_state(self) -> AgentRunReport:
        if len(self.tool_receipts) > self.tool_call_count:
            raise ValueError("successful tool receipts cannot exceed call attempts")
        draft = self.draft
        if self.status == "refused":
            if draft is not None or self.refusal_code is None:
                raise ValueError("refused runs require a refusal code and no draft")
        else:
            if self.refusal_code is not None or draft is None:
                raise ValueError("completed and abstained runs require one final draft")
            if self.draft_trust_label != "untrusted_provider_draft":
                raise ValueError("provider drafts must remain explicitly untrusted")
            if self.status == "completed" and draft.status != "draft_for_human_review":
                raise ValueError("completed status requires a review draft")
            if self.status == "abstained" and draft.status != "insufficient_evidence":
                raise ValueError("abstained status requires an insufficient-evidence response")
        return self


class AgentProvider(Protocol):
    """Only deterministic test doubles are admitted by this M2-03 slice."""

    provider_mode: Literal["test_double"]

    def next_turn(self, request: ProviderRequest, /) -> object: ...
