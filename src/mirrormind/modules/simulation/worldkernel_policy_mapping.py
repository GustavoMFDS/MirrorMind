"""Strict translation for the MirrorMind-owned WorldKernel policy world."""
from __future__ import annotations

from pydantic import ValidationError

from ...domains.retail.policy_simulation import (
    HORIZON_DAYS,
    MAX_REPLICATIONS,
    MAX_TOTAL_POLICY_TRANSITIONS,
    POLICY_IDS,
    RetailPolicyComparisonRequest,
    _lead_time_scenarios,
)
from ...domains.retail.worldkernel_policy_world import (
    POLICY_WORLD_NAME,
    POLICY_WORLD_PARAMETERS_SCHEMA,
    POLICY_WORLD_VERSION,
    create_policy_world_initial_state,
)
from .worldkernel_mapping import WorldKernelMappingError, WorldKernelOperatorLimits

_SENSITIVITY_SCENARIOS = 3


def build_worldkernel_policy_exchange_request(
    request: RetailPolicyComparisonRequest,
    *,
    operator_limits: WorldKernelOperatorLimits,
) -> dict[str, object]:
    """Build one fixed 28-step exchange request; reject work over operator limits."""
    if type(request) is not RetailPolicyComparisonRequest:
        raise WorldKernelMappingError(
            "request must be a validated RetailPolicyComparisonRequest"
        )
    try:
        snapshot = RetailPolicyComparisonRequest.model_validate(
            request.model_dump(mode="python")
        )
    except ValidationError as exc:
        raise WorldKernelMappingError(
            "policy comparison failed mapping-boundary revalidation"
        ) from exc
    if not isinstance(operator_limits, WorldKernelOperatorLimits):
        raise WorldKernelMappingError("operator-owned WorldKernel limits are required")

    if operator_limits.max_steps < HORIZON_DAYS:
        raise WorldKernelMappingError("operator step limit is below the fixed 28-day horizon")
    if operator_limits.max_runs < snapshot.replications:
        raise WorldKernelMappingError("request exceeds the operator run limit")
    lead_times = _lead_time_scenarios(snapshot.assumptions.lead_time_days)
    policy_transition_count = (
        HORIZON_DAYS
        * snapshot.replications
        * len(POLICY_IDS)
        * len(lead_times)
    )
    effective_policy_budget = min(
        MAX_TOTAL_POLICY_TRANSITIONS,
        operator_limits.max_total_transitions,
    )
    if policy_transition_count > effective_policy_budget:
        raise WorldKernelMappingError(
            "policy comparison exceeds the operator transition budget"
        )

    # Each WorldKernel event updates all policy/sensitivity pairs. Divide the
    # app-owned work budget by that fixed fan-out before declaring engine limits.
    max_engine_transitions = effective_policy_budget // (
        len(POLICY_IDS) * len(lead_times)
    )
    if snapshot.replications * HORIZON_DAYS > max_engine_transitions:
        raise WorldKernelMappingError(
            "policy comparison exceeds the mapped WorldKernel transition budget"
        )

    return {
        "schema_version": "worldkernel.simulation.v1",
        "world": POLICY_WORLD_NAME,
        "world_version": POLICY_WORLD_VERSION,
        "steps": HORIZON_DAYS,
        "runs": snapshot.replications,
        "seed": snapshot.seed,
        "initial_state": create_policy_world_initial_state(
            snapshot.assumptions, lead_times
        ),
        "parameters": {
            "schema_version": POLICY_WORLD_PARAMETERS_SCHEMA,
            "demand_profile_units": list(snapshot.demand_profile_units),
            "lead_time_days": list(lead_times),
            "assumptions": snapshot.assumptions.model_dump(mode="json"),
        },
        "limits": {
            "max_steps": HORIZON_DAYS,
            "max_runs": min(operator_limits.max_runs, MAX_REPLICATIONS),
            "max_total_transitions": max_engine_transitions,
        },
    }
