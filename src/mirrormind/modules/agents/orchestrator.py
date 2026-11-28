"""Sequential, bounded orchestration with fail-closed tool and citation checks."""
from __future__ import annotations

from typing import Literal

from .contracts import (
    MAX_PROVIDER_CONTEXT_BYTES,
    AgentProvider,
    AgentRunReport,
    AgentRunRequest,
    AgentTurn,
    ProviderRequest,
    RefusalCode,
    ToolObservation,
    ToolReceipt,
)
from .registry import ToolInvocationError, ToolRegistry, provider_context_size
from .synthetic_tools import EvidenceSearchOutput, build_synthetic_tool_registry


def run_bounded_tool_orchestration(
    request: AgentRunRequest,
    provider: AgentProvider,
    *,
    registry: ToolRegistry | None = None,
) -> AgentRunReport:
    """Run only a test double over fixed tools and return a minimized receipt.

    ``registry`` is a trusted local test/composition seam. The default path
    creates the reviewed fixed registry; no HTTP route accepts a registry.
    """
    if type(request) is not AgentRunRequest:
        raise TypeError("request must be an exact validated AgentRunRequest")
    if registry is not None and type(registry) is not ToolRegistry:
        raise TypeError("registry must be an exact ToolRegistry")
    selected_registry = registry or build_synthetic_tool_registry()
    try:
        provider_mode = getattr(provider, "provider_mode", None)
    except Exception:  # noqa: BLE001 - provider configuration details are untrusted
        return _refused("provider_not_authorized", provider_mode="rejected")
    if type(provider_mode) is not str or provider_mode != "test_double":
        return _refused("provider_not_authorized", provider_mode="rejected")

    if any(not selected_registry.contains(name) for name in request.allowed_tool_names):
        return _refused("tool_not_registered", provider_mode="test_double")

    descriptors = selected_registry.describe(request.allowed_tool_names)
    observations: list[ToolObservation] = []
    receipts: list[ToolReceipt] = []
    seen_call_ids: set[str] = set()
    provider_turn_count = 0
    tool_call_count = 0
    total_output_bytes = 0

    for turn_index in range(request.max_provider_turns):
        provider_request = ProviderRequest(
            question=request.question,
            turn_index=turn_index,
            available_tools=descriptors,
            observations=tuple(observations),
        )
        if provider_context_size(provider_request) > MAX_PROVIDER_CONTEXT_BYTES:
            return _refused(
                "provider_context_too_large",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        try:
            turn = provider.next_turn(provider_request)
        except Exception:  # noqa: BLE001 - provider diagnostics must not enter the receipt
            return _refused(
                "provider_failure",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count + 1,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        provider_turn_count += 1
        validated_turn = _revalidate_provider_turn(turn)
        if validated_turn is None:
            return _refused(
                "invalid_provider_turn",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        turn = validated_turn

        if turn.kind == "final":
            assert turn.final is not None
            known_citations = _observed_citation_refs(observations)
            if any(reference not in known_citations for reference in turn.final.citation_refs):
                return _refused(
                    "unsupported_evidence_reference",
                    provider_mode="test_double",
                    provider_turn_count=provider_turn_count,
                    tool_call_count=tool_call_count,
                    tool_receipts=tuple(receipts),
                )
            status: Literal["completed", "abstained"] = (
                "completed"
                if turn.final.status == "draft_for_human_review"
                else "abstained"
            )
            return AgentRunReport(
                status=status,
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
                draft=turn.final,
                draft_trust_label="untrusted_provider_draft",
            )

        assert turn.tool_call is not None
        tool_call_count += 1
        call = turn.tool_call
        if tool_call_count > request.max_tool_calls:
            return _refused(
                "tool_call_budget_exhausted",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        if call.call_id in seen_call_ids:
            return _refused(
                "duplicate_tool_call_id",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        seen_call_ids.add(call.call_id)
        if not selected_registry.contains(call.tool_name):
            return _refused(
                "tool_not_registered",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        if call.tool_name not in request.allowed_tool_names:
            return _refused(
                "tool_not_allowed",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        try:
            execution = selected_registry.invoke(call)
        except ToolInvocationError as exc:
            return _refused(
                exc.code,
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )

        output_bytes = execution.receipt.output_bytes
        if total_output_bytes + output_bytes > MAX_PROVIDER_CONTEXT_BYTES:
            return _refused(
                "provider_context_too_large",
                provider_mode="test_double",
                provider_turn_count=provider_turn_count,
                tool_call_count=tool_call_count,
                tool_receipts=tuple(receipts),
            )
        total_output_bytes += output_bytes
        observations.append(execution.observation)
        receipts.append(execution.receipt)

    return _refused(
        "provider_turn_budget_exhausted",
        provider_mode="test_double",
        provider_turn_count=provider_turn_count,
        tool_call_count=tool_call_count,
        tool_receipts=tuple(receipts),
    )


def _revalidate_provider_turn(value: object) -> AgentTurn | None:
    """Rebuild the provider value from plain data before trusting its fields.

    Pydantic ``model_copy(update=...)`` skips validation. Dumping to Python
    primitives first ensures ``model_validate`` rechecks nested models and
    model-level invariants instead of accepting existing model instances.
    """
    if type(value) is not AgentTurn:
        return None
    try:
        raw_turn = value.model_dump(mode="python")
        return AgentTurn.model_validate(raw_turn, strict=True)
    except Exception:  # noqa: BLE001 - malformed provider values must fail closed
        return None


def _observed_citation_refs(observations: list[ToolObservation]) -> frozenset[str]:
    references: set[str] = set()
    for observation in observations:
        if observation.tool_name != "search_synthetic_evidence":
            continue
        try:
            result = EvidenceSearchOutput.model_validate_json(
                observation.output_json, strict=True
            )
        except ValueError:
            continue
        references.update(hit.citation_ref for hit in result.hits)
    return frozenset(references)


def _refused(
    code: RefusalCode,
    *,
    provider_mode: Literal["test_double", "rejected"],
    provider_turn_count: int = 0,
    tool_call_count: int = 0,
    tool_receipts: tuple[ToolReceipt, ...] = (),
) -> AgentRunReport:
    return AgentRunReport(
        status="refused",
        provider_mode=provider_mode,
        provider_turn_count=provider_turn_count,
        tool_call_count=tool_call_count,
        tool_receipts=tool_receipts,
        refusal_code=code,
    )
