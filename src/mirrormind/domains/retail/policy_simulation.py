"""Bounded, local-only synthetic retail replenishment policy comparison.

This test double consumes caller-declared daily demand assumptions. It does
not load evidence, forecast demand, call WorldKernel, or select a policy.
"""
from __future__ import annotations

import json
import random
from hashlib import sha256
from typing import Literal, TypedDict

from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator

HORIZON_DAYS = 28
MAX_DAILY_EXPECTED_DEMAND_UNITS = 1_000
MAX_REPLICATIONS = 250
MAX_TOTAL_POLICY_TRANSITIONS = 50_000
_MAX_SEED = (1 << 32) - 1 - MAX_REPLICATIONS
_DEMAND_MULTIPLIERS_PERCENT = (75, 100, 125)

POLICY_IDS = (
    "fixed_cycle_quantity",
    "reorder_point_fixed_quantity",
    "forecast_aware_order_up_to",
)
_MODELING_CAVEATS = (
    "forecast_aware_order_up_to sums expected profile indices [day + 1, arrival_day); it excludes demand on the arrival day.",
    "With lead_time_days=1, that interval is empty. With zero safety stock and zero inventory position, the rule orders zero even when arrival-day demand is positive.",
    "This is a toy day-boundary heuristic, not a standard or optimized order-up-to policy.",
)


class _DemandStream(TypedDict):
    replication: int
    seed: int
    demand_units: tuple[int, ...]
    demand_stream_sha256: str


class RetailPolicySimulationState(TypedDict):
    """JSON-safe inventory state shared by the reference and engine worlds."""

    on_hand_units: int
    pending_by_day: dict[str, int]
    pending_units: int
    fulfilled_units: int
    unmet_units: int
    total_demand_units: int
    stockout_days: int
    order_count: int
    ordered_units: int
    procurement_cost_units: int
    holding_cost_units: int


class RetailPolicyAssumptions(BaseModel):
    """Explicit units, inventory controls and abstract synthetic costs."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    quantity_unit: Literal["item"] = "item"
    time_unit: Literal["day"] = "day"
    cost_unit: Literal["synthetic_cost_unit"] = "synthetic_cost_unit"
    initial_stock_units: StrictInt = Field(ge=0, le=10_000)
    lead_time_days: StrictInt = Field(ge=1, le=HORIZON_DAYS)
    fixed_order_quantity_units: StrictInt = Field(ge=1, le=10_000)
    reorder_point_units: StrictInt = Field(ge=0, le=10_000)
    review_period_days: StrictInt = Field(ge=1, le=HORIZON_DAYS)
    safety_stock_units: StrictInt = Field(ge=0, le=10_000)
    procurement_cost_per_unit: StrictInt = Field(ge=0, le=10_000)
    holding_cost_per_unit_day: StrictInt = Field(ge=0, le=10_000)
    fixed_order_cost: StrictInt = Field(ge=0, le=10_000)
    unmet_demand_penalty_per_unit: StrictInt = Field(ge=0, le=10_000)


class RetailPolicyComparisonRequest(BaseModel):
    """Input contract for one paired, 28-day synthetic experiment."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    demand_profile_units: tuple[StrictInt, ...]
    assumptions: RetailPolicyAssumptions
    replications: StrictInt = Field(default=12, ge=1, le=MAX_REPLICATIONS)
    seed: StrictInt = Field(default=317, ge=0, le=_MAX_SEED)

    @model_validator(mode="after")
    def validate_experiment_bounds(self) -> RetailPolicyComparisonRequest:
        if len(self.demand_profile_units) != HORIZON_DAYS:
            raise ValueError("demand_profile_units must contain exactly 28 days")
        if any(
            type(value) is not int
            or value < 0
            or value > MAX_DAILY_EXPECTED_DEMAND_UNITS
            for value in self.demand_profile_units
        ):
            raise ValueError("daily expected demand must be an integer in 0..1000")
        if not any(self.demand_profile_units):
            raise ValueError("demand profile must contain at least one positive day")
        transition_count = self.replications * HORIZON_DAYS * len(POLICY_IDS) * 3
        if transition_count > MAX_TOTAL_POLICY_TRANSITIONS:
            raise ValueError("experiment exceeds the local transition budget")
        return self


def _build_demand_streams(
    request: RetailPolicyComparisonRequest,
) -> tuple[_DemandStream, ...]:
    """Generate one reproducible exogenous sequence per replication."""
    streams: list[_DemandStream] = []
    for replication in range(request.replications):
        stream_seed = request.seed + replication
        generator = random.Random(stream_seed)
        demand = tuple(
            sample_demand_units(expected, generator.randrange(3))
            for expected in request.demand_profile_units
        )
        payload = {
            "seed": stream_seed,
            "replication": replication,
            "demand_units": demand,
        }
        digest = sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("ascii")
        ).hexdigest()
        streams.append(
            {
                "replication": replication,
                "seed": stream_seed,
                "demand_units": demand,
                "demand_stream_sha256": digest,
            }
        )
    return tuple(streams)


def sample_demand_units(expected_units: int, multiplier_index: int) -> int:
    """Apply the fixed 75/100/125 percent synthetic multiplier with integer rounding."""
    if type(expected_units) is not int or expected_units < 0:
        raise ValueError("expected demand must be a non-negative integer")
    if type(multiplier_index) is not int or not 0 <= multiplier_index < len(
        _DEMAND_MULTIPLIERS_PERCENT
    ):
        raise ValueError("multiplier index must select one of the three fixed values")
    return (
        expected_units * _DEMAND_MULTIPLIERS_PERCENT[multiplier_index] + 50
    ) // 100


def _order_quantity(
    *,
    policy_id: str,
    day_index: int,
    inventory_position_units: int,
    demand_profile_units: tuple[int, ...],
    lead_time_days: int,
    assumptions: RetailPolicyAssumptions,
) -> int:
    if policy_id == "fixed_cycle_quantity":
        if day_index % assumptions.review_period_days == 0:
            return assumptions.fixed_order_quantity_units
        return 0

    if policy_id == "reorder_point_fixed_quantity":
        if inventory_position_units <= assumptions.reorder_point_units:
            return assumptions.fixed_order_quantity_units
        return 0

    if policy_id == "forecast_aware_order_up_to":
        first_future_day = day_index + 1
        arrival_day = min(day_index + lead_time_days, HORIZON_DAYS)
        expected_lead_time_demand = sum(
            demand_profile_units[first_future_day:arrival_day]
        )
        target_units = expected_lead_time_demand + assumptions.safety_stock_units
        return max(0, target_units - inventory_position_units)

    raise ValueError("unsupported synthetic retail policy")


def create_retail_policy_state(
    assumptions: RetailPolicyAssumptions,
) -> RetailPolicySimulationState:
    """Create a fresh, JSON-safe state with the declared starting inventory."""
    if not isinstance(assumptions, RetailPolicyAssumptions):
        raise TypeError("assumptions must be validated RetailPolicyAssumptions")
    return {
        "on_hand_units": assumptions.initial_stock_units,
        "pending_by_day": {},
        "pending_units": 0,
        "fulfilled_units": 0,
        "unmet_units": 0,
        "total_demand_units": 0,
        "stockout_days": 0,
        "order_count": 0,
        "ordered_units": 0,
        "procurement_cost_units": 0,
        "holding_cost_units": 0,
    }


def advance_retail_policy_day(
    state: RetailPolicySimulationState,
    *,
    policy_id: str,
    day_index: int,
    demand_units: int,
    demand_profile_units: tuple[int, ...],
    lead_time_days: int,
    assumptions: RetailPolicyAssumptions,
) -> RetailPolicySimulationState:
    """Apply one day boundary: receive, fulfill, cost, then place a new order."""
    if type(day_index) is not int or not 0 <= day_index < HORIZON_DAYS:
        raise ValueError("day_index must be within the fixed 28-day horizon")
    if type(demand_units) is not int or demand_units < 0:
        raise ValueError("demand_units must be a non-negative integer")
    if not isinstance(assumptions, RetailPolicyAssumptions):
        raise TypeError("assumptions must be validated RetailPolicyAssumptions")
    if type(state) is not dict or set(state) != set(create_retail_policy_state(assumptions)):
        raise ValueError("policy state fields do not match the reviewed contract")
    if any(type(value) is not int or value < 0 for key, value in state.items() if key != "pending_by_day"):
        raise ValueError("policy state counters must be non-negative integers")
    pending_by_day = state["pending_by_day"]
    if type(pending_by_day) is not dict or any(
        type(day) is not str
        or not day.isdecimal()
        or type(quantity) is not int
        or quantity < 0
        for day, quantity in pending_by_day.items()
    ):
        raise ValueError("pending orders must use non-negative string day keys")

    next_state: RetailPolicySimulationState = {
        **state,
        "pending_by_day": dict(pending_by_day),
    }
    received = next_state["pending_by_day"].pop(str(day_index), 0)
    next_state["on_hand_units"] += received
    next_state["pending_units"] -= received
    if next_state["pending_units"] < 0:
        raise ValueError("pending order balance cannot become negative")

    next_state["total_demand_units"] += demand_units
    fulfilled = min(next_state["on_hand_units"], demand_units)
    next_state["on_hand_units"] -= fulfilled
    unmet = demand_units - fulfilled
    next_state["fulfilled_units"] += fulfilled
    next_state["unmet_units"] += unmet
    next_state["stockout_days"] += int(unmet > 0)
    next_state["holding_cost_units"] += (
        next_state["on_hand_units"] * assumptions.holding_cost_per_unit_day
    )

    inventory_position = next_state["on_hand_units"] + next_state["pending_units"]
    quantity = _order_quantity(
        policy_id=policy_id,
        day_index=day_index,
        inventory_position_units=inventory_position,
        demand_profile_units=demand_profile_units,
        lead_time_days=lead_time_days,
        assumptions=assumptions,
    )
    if quantity:
        next_state["order_count"] += 1
        next_state["ordered_units"] += quantity
        next_state["procurement_cost_units"] += (
            quantity * assumptions.procurement_cost_per_unit
        )
        arrival_day = day_index + lead_time_days
        if arrival_day < HORIZON_DAYS:
            arrival_key = str(arrival_day)
            next_state["pending_by_day"][arrival_key] = (
                next_state["pending_by_day"].get(arrival_key, 0) + quantity
            )
        next_state["pending_units"] += quantity
    return next_state


def finalize_retail_policy_metrics(
    state: RetailPolicySimulationState,
    assumptions: RetailPolicyAssumptions,
) -> dict[str, int]:
    """Derive the public cost and service metrics from a completed state."""
    if type(state) is not dict or set(state) != set(create_retail_policy_state(assumptions)):
        raise ValueError("policy state fields do not match the reviewed contract")
    if any(type(value) is not int or value < 0 for key, value in state.items() if key != "pending_by_day"):
        raise ValueError("policy state counters must be non-negative integers")
    pending_by_day = state["pending_by_day"]
    if type(pending_by_day) is not dict or any(
        type(day) is not str
        or not day.isdecimal()
        or type(quantity) is not int
        or quantity < 0
        for day, quantity in pending_by_day.items()
    ):
        raise ValueError("pending orders must use non-negative string day keys")
    if sum(pending_by_day.values()) > state["pending_units"]:
        raise ValueError("scheduled pending orders exceed the pending order balance")
    if (
        assumptions.initial_stock_units + state["ordered_units"]
        != state["fulfilled_units"]
        + state["on_hand_units"]
        + state["pending_units"]
    ):
        raise ValueError("policy state violates item inventory balance")
    order_cost = state["order_count"] * assumptions.fixed_order_cost
    unmet_cost = state["unmet_units"] * assumptions.unmet_demand_penalty_per_unit
    total_cost = state["procurement_cost_units"] + state["holding_cost_units"] + order_cost + unmet_cost
    return {
        "total_demand_units": state["total_demand_units"],
        "fulfilled_units": state["fulfilled_units"],
        "unmet_units": state["unmet_units"],
        "stockout_days": state["stockout_days"],
        "ending_on_hand_units": state["on_hand_units"],
        "pending_order_units": state["pending_units"],
        "order_count": state["order_count"],
        "procurement_cost_units": state["procurement_cost_units"],
        "holding_cost_units": state["holding_cost_units"],
        "fixed_order_cost_units": order_cost,
        "unmet_demand_cost_units": unmet_cost,
        "total_cost_units": total_cost,
    }


def _simulate_replication(
    *,
    policy_id: str,
    demand_units: tuple[int, ...],
    demand_profile_units: tuple[int, ...],
    lead_time_days: int,
    assumptions: RetailPolicyAssumptions,
) -> dict[str, int]:
    """Run one policy against one fixed demand stream using day-boundary rules."""
    state = create_retail_policy_state(assumptions)
    for day_index, demand in enumerate(demand_units):
        state = advance_retail_policy_day(
            state,
            policy_id=policy_id,
            day_index=day_index,
            demand_units=demand,
            demand_profile_units=demand_profile_units,
            lead_time_days=lead_time_days,
            assumptions=assumptions,
        )
    return finalize_retail_policy_metrics(state, assumptions)


def _basis_points(numerator: int, denominator: int) -> int | None:
    if denominator == 0:
        return None
    return min(10_000, (numerator * 10_000 + denominator // 2) // denominator)


def summarize_retail_policy_runs(
    policy_id: str,
    replication_results: list[dict[str, object]],
) -> dict[str, object]:
    """Aggregate already computed replication rows without changing their source."""
    totals: dict[str, int] = {}
    for replication in replication_results:
        metrics = replication.get("metrics")
        if type(metrics) is not dict or any(
            type(value) is not int or value < 0 for value in metrics.values()
        ):
            raise ValueError("replication metrics must be non-negative integers")
        for key, value in metrics.items():
            totals[key] = totals.get(key, 0) + value

    count = len(replication_results)
    if count == 0:
        raise ValueError("at least one replication is required")
    aggregate_metrics: dict[str, int | None] = dict(totals)
    aggregate_metrics["fill_rate_basis_points"] = _basis_points(
        totals["fulfilled_units"], totals["total_demand_units"]
    )
    mean_metrics = {
        "total_cost_units": round(totals["total_cost_units"] / count, 2),
        "stockout_days_per_replication": round(totals["stockout_days"] / count, 2),
        "ending_on_hand_units": round(totals["ending_on_hand_units"] / count, 2),
        "pending_order_units": round(totals["pending_order_units"] / count, 2),
        "order_count": round(totals["order_count"] / count, 2),
        "fill_rate_basis_points": aggregate_metrics["fill_rate_basis_points"],
    }
    return {
        "policy_id": policy_id,
        "ranking": None,
        "ranking_status": "not_computed",
        "replication_results": replication_results,
        "aggregate_metrics_across_replications": aggregate_metrics,
        "mean_metrics_per_replication": mean_metrics,
    }


def _aggregate_policy(
    *,
    policy_id: str,
    demand_streams: tuple[_DemandStream, ...],
    demand_profile_units: tuple[int, ...],
    lead_time_days: int,
    assumptions: RetailPolicyAssumptions,
) -> dict[str, object]:
    replication_results = [
        {
            "replication": stream["replication"],
            "seed": stream["seed"],
            "demand_stream_sha256": stream["demand_stream_sha256"],
            "metrics": _simulate_replication(
                policy_id=policy_id,
                demand_units=stream["demand_units"],
                demand_profile_units=demand_profile_units,
                lead_time_days=lead_time_days,
                assumptions=assumptions,
            ),
        }
        for stream in demand_streams
    ]
    return summarize_retail_policy_runs(policy_id, replication_results)


def _lead_time_scenarios(base_lead_time_days: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                max(1, base_lead_time_days - 1),
                base_lead_time_days,
                min(HORIZON_DAYS, base_lead_time_days + 1),
            }
        )
    )


def compare_synthetic_retail_policies(
    request: RetailPolicyComparisonRequest,
) -> dict[str, object]:
    """Compare three replenishment rules using paired caller-declared inputs.

    The returned metrics are conditional synthetic outcomes. This function
    does not authenticate input origin, infer stock or cost, forecast demand,
    invoke WorldKernel, rank policies, or authorize an operational action.
    """
    if not isinstance(request, RetailPolicyComparisonRequest):
        raise TypeError("request must be a validated RetailPolicyComparisonRequest")

    streams = _build_demand_streams(request)
    assumptions = request.assumptions
    scenarios = []
    for lead_time_days in _lead_time_scenarios(assumptions.lead_time_days):
        scenarios.append(
            {
                "lead_time_days": lead_time_days,
                "is_base_assumption": lead_time_days == assumptions.lead_time_days,
                "policies": [
                    _aggregate_policy(
                        policy_id=policy_id,
                        demand_streams=streams,
                        demand_profile_units=request.demand_profile_units,
                        lead_time_days=lead_time_days,
                        assumptions=assumptions,
                    )
                    for policy_id in POLICY_IDS
                ],
            }
        )

    return {
        "schema_version": "mirrormind.retail.policy_comparison.v1",
        "simulation_status": "experimental_local_test_double_only",
        "engine_execution": "worldkernel_not_invoked",
        "input_status": "caller_supplied_assumptions_not_authenticated",
        "decision_status": "comparison_only_no_policy_selection_or_authorization",
        "modeling_caveats": list(_MODELING_CAVEATS),
        "horizon_days": HORIZON_DAYS,
        "replications": request.replications,
        "seed": request.seed,
        "quantity_unit": assumptions.quantity_unit,
        "time_unit": assumptions.time_unit,
        "cost_unit": assumptions.cost_unit,
        "demand_profile_units": list(request.demand_profile_units),
        "assumptions": assumptions.model_dump(mode="json"),
        "policy_ids": list(POLICY_IDS),
        "lead_time_sensitivity": scenarios,
    }
