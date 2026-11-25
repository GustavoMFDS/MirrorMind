"""Code-owned WorldKernel handler for the synthetic M1 retail policy comparison."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from random import Random
from typing import Any

from .policy_simulation import (
    HORIZON_DAYS,
    POLICY_IDS,
    RetailPolicyAssumptions,
    RetailPolicyComparisonRequest,
    RetailPolicySimulationState,
    advance_retail_policy_day,
    create_retail_policy_state,
    sample_demand_units,
)

POLICY_WORLD_NAME = "mirrormind.retail.policy_comparison"
POLICY_WORLD_VERSION = "mm-retail-policy-v1"
POLICY_WORLD_STATE_SCHEMA = "mirrormind.retail.policy_world_state.v1"
POLICY_WORLD_PARAMETERS_SCHEMA = "mirrormind.retail.policy_world_parameters.v1"

_PARAMETER_FIELDS = frozenset(
    {
        "schema_version",
        "demand_profile_units",
        "lead_time_days",
        "assumptions",
    }
)
_STATE_FIELDS = frozenset(
    {"schema_version", "day_index", "demand_units", "policy_states"}
)
_MAX_SAMPLED_DEMAND_UNITS = 1_250


def create_policy_world_initial_state(
    assumptions: RetailPolicyAssumptions,
    lead_time_days: tuple[int, ...],
) -> dict[str, object]:
    """Create the exact state envelope accepted by the registered handler."""
    if not isinstance(assumptions, RetailPolicyAssumptions):
        raise TypeError("assumptions must be validated RetailPolicyAssumptions")
    if type(lead_time_days) is not tuple or not lead_time_days:
        raise ValueError("lead_time_days must be a nonempty tuple")
    if any(type(day) is not int or not 1 <= day <= HORIZON_DAYS for day in lead_time_days):
        raise ValueError("lead_time_days must remain inside the 28-day horizon")
    if tuple(sorted(set(lead_time_days))) != lead_time_days:
        raise ValueError("lead_time_days must be unique and sorted")
    policy_states = {
        str(lead_time): {
            policy_id: create_retail_policy_state(assumptions)
            for policy_id in POLICY_IDS
        }
        for lead_time in lead_time_days
    }
    return {
        "schema_version": POLICY_WORLD_STATE_SCHEMA,
        "day_index": 0,
        "demand_units": [],
        "policy_states": policy_states,
    }


def _validated_parameters(
    parameters: Mapping[str, Any],
) -> tuple[tuple[int, ...], tuple[int, ...], RetailPolicyAssumptions]:
    if type(parameters) is not dict or set(parameters) != _PARAMETER_FIELDS:
        raise ValueError("policy-world parameters do not match the registered contract")
    if parameters["schema_version"] != POLICY_WORLD_PARAMETERS_SCHEMA:
        raise ValueError("policy-world parameter revision is unsupported")
    profile = parameters["demand_profile_units"]
    lead_times = parameters["lead_time_days"]
    if type(profile) is not list or any(type(value) is not int for value in profile):
        raise ValueError("demand_profile_units must be an integer list")
    if type(lead_times) is not list or any(type(value) is not int for value in lead_times):
        raise ValueError("lead_time_days must be an integer list")
    assumptions = RetailPolicyAssumptions.model_validate(parameters["assumptions"])
    RetailPolicyComparisonRequest.model_validate(
        {
            "demand_profile_units": tuple(profile),
            "assumptions": assumptions.model_dump(mode="python"),
            "replications": 1,
            "seed": 0,
        }
    )
    expected_lead_times = tuple(
        sorted(
            {
                max(1, assumptions.lead_time_days - 1),
                assumptions.lead_time_days,
                min(HORIZON_DAYS, assumptions.lead_time_days + 1),
            }
        )
    )
    if tuple(lead_times) != expected_lead_times:
        raise ValueError("lead_time_days do not match the declared sensitivity rule")
    return tuple(profile), tuple(lead_times), assumptions


def mirrormind_retail_policy_step(
    state: dict[str, Any],
    parameters: Mapping[str, Any],
    rng: Random,
) -> dict[str, Any]:
    """Apply one shared synthetic demand draw to all policy/sensitivity pairs."""
    profile, lead_times, assumptions = _validated_parameters(parameters)
    if type(state) is not dict or set(state) != _STATE_FIELDS:
        raise ValueError("policy-world state does not match the registered contract")
    day_index = state["day_index"]
    demand_stream = state["demand_units"]
    expected_policy_keys = {str(value) for value in lead_times}
    if (
        state["schema_version"] != POLICY_WORLD_STATE_SCHEMA
        or type(day_index) is not int
        or not 0 <= day_index < HORIZON_DAYS
        or type(demand_stream) is not list
        or len(demand_stream) != day_index
        or any(
            type(value) is not int or not 0 <= value <= _MAX_SAMPLED_DEMAND_UNITS
            for value in demand_stream
        )
    ):
        raise ValueError("policy-world day state is invalid")
    policy_states = state["policy_states"]
    if type(policy_states) is not dict or set(policy_states) != expected_policy_keys:
        raise ValueError("policy-world sensitivity state is invalid")
    if not callable(getattr(rng, "randrange", None)):
        raise TypeError("WorldKernel random source must provide randrange")

    demand = sample_demand_units(profile[day_index], rng.randrange(3))
    next_policy_states: dict[str, dict[str, RetailPolicySimulationState]] = {}
    for lead_time in lead_times:
        lead_key = str(lead_time)
        policies = policy_states[lead_key]
        if type(policies) is not dict or set(policies) != set(POLICY_IDS):
            raise ValueError("policy-world policy state is invalid")
        next_policy_states[lead_key] = {}
        for policy_id in POLICY_IDS:
            policy_state = policies[policy_id]
            if type(policy_state) is not dict:
                raise ValueError("policy-world inventory state is invalid")
            next_policy_states[lead_key][policy_id] = advance_retail_policy_day(
                policy_state,
                policy_id=policy_id,
                day_index=day_index,
                demand_units=demand,
                demand_profile_units=profile,
                lead_time_days=lead_time,
                assumptions=assumptions,
            )
    return {
        "schema_version": POLICY_WORLD_STATE_SCHEMA,
        "day_index": day_index + 1,
        "demand_units": [*demand_stream, demand],
        "policy_states": next_policy_states,
    }


def register_mirrormind_policy_world(
    registrar: Callable[..., None],
) -> None:
    """Register exactly this versioned handler through trusted worker code."""
    if not callable(registrar):
        raise TypeError("trusted WorldKernel registrar is required")
    registrar(
        POLICY_WORLD_NAME,
        mirrormind_retail_policy_step,
        version=POLICY_WORLD_VERSION,
    )
