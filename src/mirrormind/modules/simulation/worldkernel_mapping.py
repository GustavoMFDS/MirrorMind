"""Fail-closed request mapping for one optional WorldKernel demo world.

This module creates JSON-compatible data only. It does not import the
WorldKernel package, execute a simulation, or validate a returned result.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal

from pydantic import ValidationError

from ...core.contracts import ScenarioSpec

_MAX_SCENARIO_STEPS = 366
_MAX_SCENARIO_RUNS = 10_000
_MAX_SCENARIO_TRANSITIONS = _MAX_SCENARIO_STEPS * _MAX_SCENARIO_RUNS
_ALLOWED_STATE_FIELDS = frozenset({"stock", "sold", "unmet", "orders"})
_REQUIRED_PARAMETER_FIELDS = frozenset(
    {"daily_demand", "reorder_point", "reorder_quantity"}
)


class WorldKernelMappingError(ValueError):
    """The MirrorMind scenario cannot be represented by the allowlisted world."""


@dataclass(frozen=True, slots=True)
class WorldKernelWorldMapping:
    """Exact source and target identifiers reviewed for request translation."""

    source_world_type: str
    source_world_version: str
    target_world: str
    target_world_version: str


SUPPORTED_WORLD_MAPPINGS: Mapping[tuple[str, str], WorldKernelWorldMapping] = (
    MappingProxyType(
        {
            ("retail.inventory", "0.1"): WorldKernelWorldMapping(
                source_world_type="retail.inventory",
                source_world_version="0.1",
                target_world="retail.inventory.demo",
                target_world_version="demo-1",
            )
        }
    )
)


@dataclass(frozen=True, slots=True)
class WorldKernelOperatorLimits:
    """Trusted composition-root ceilings, independent of scenario input."""

    max_steps: int
    max_runs: int
    max_total_transitions: int

    def __post_init__(self) -> None:
        limits = {
            "max_steps": (self.max_steps, _MAX_SCENARIO_STEPS),
            "max_runs": (self.max_runs, _MAX_SCENARIO_RUNS),
            "max_total_transitions": (
                self.max_total_transitions,
                _MAX_SCENARIO_TRANSITIONS,
            ),
        }
        for name, (value, upper_bound) in limits.items():
            if type(value) is not int or not 1 <= value <= upper_bound:
                raise ValueError(
                    f"{name} must be a positive integer no greater than {upper_bound}"
                )


@dataclass(frozen=True, slots=True)
class InventoryWorldUnitContext:
    """Explicit units required by the integer-only inventory demo contract."""

    quantity_unit: Literal["item"]
    step_unit: Literal["day"]
    order_unit: Literal["order"]


def _nonnegative_integer_object(
    values: object,
    *,
    name: str,
    allowed_fields: frozenset[str],
    required_fields: frozenset[str],
) -> dict[str, int]:
    if not isinstance(values, dict) or any(not isinstance(key, str) for key in values):
        raise WorldKernelMappingError(f"{name} must be a string-keyed object")

    keys = set(values)
    unknown = keys - allowed_fields
    if unknown:
        fields = ", ".join(sorted(unknown))
        raise WorldKernelMappingError(f"unsupported {name} fields: {fields}")
    missing = required_fields - keys
    if missing:
        fields = ", ".join(sorted(missing))
        raise WorldKernelMappingError(f"missing required {name} fields: {fields}")

    copied: dict[str, int] = {}
    for key, value in values.items():
        if type(value) is not int or value < 0:
            raise WorldKernelMappingError(
                f"{name}.{key} must be a non-negative integer"
            )
        copied[key] = value
    return copied


def _validate_units(unit_context: InventoryWorldUnitContext) -> None:
    if not isinstance(unit_context, InventoryWorldUnitContext):
        raise WorldKernelMappingError("inventory unit context is required")
    expected = {"quantity_unit": "item", "step_unit": "day", "order_unit": "order"}
    actual = {
        "quantity_unit": unit_context.quantity_unit,
        "step_unit": unit_context.step_unit,
        "order_unit": unit_context.order_unit,
    }
    if actual != expected:
        raise WorldKernelMappingError(
            "unit context must declare item quantities, daily steps and order counts"
        )


def build_worldkernel_exchange_request(
    scenario: ScenarioSpec,
    *,
    operator_limits: WorldKernelOperatorLimits,
    unit_context: InventoryWorldUnitContext,
) -> dict[str, object]:
    """Build a strict WorldKernel v1 request without executing it.

    Operator limits must come from trusted application configuration, never
    from fields inside the caller-controlled ``ScenarioSpec``. The unit
    context is an explicit caller assertion; this function cannot verify its
    provenance.
    """
    if not isinstance(scenario, ScenarioSpec):
        raise WorldKernelMappingError("scenario must be a validated ScenarioSpec")
    try:
        # ScenarioSpec is mutable; rebuild from its current fields so a mutation
        # after initial construction cannot bypass nested cross-field budgets.
        scenario = ScenarioSpec.model_validate(scenario.model_dump(mode="python"))
    except ValidationError as exc:
        raise WorldKernelMappingError(
            "scenario failed mapping-boundary revalidation"
        ) from exc
    if not isinstance(operator_limits, WorldKernelOperatorLimits):
        raise WorldKernelMappingError("operator-owned limits are required")
    if scenario.schema_version != "0.1":
        raise WorldKernelMappingError("unsupported MirrorMind scenario schema")
    if not isinstance(scenario.world_type, str) or not isinstance(
        scenario.world_version, str
    ):
        raise WorldKernelMappingError("world identifiers must be strings")

    mapping = SUPPORTED_WORLD_MAPPINGS.get(
        (scenario.world_type, scenario.world_version)
    )
    if mapping is None:
        raise WorldKernelMappingError("unsupported MirrorMind world mapping")
    _validate_units(unit_context)

    if type(scenario.horizon_days) is not int or scenario.horizon_days < 1:
        raise WorldKernelMappingError("horizon_days must be a positive integer")
    if type(scenario.runs) is not int or scenario.runs < 1:
        raise WorldKernelMappingError("runs must be a positive integer")
    if type(scenario.seed) is not int:
        raise WorldKernelMappingError("seed must be an integer")

    if scenario.interventions:
        raise WorldKernelMappingError("scenario interventions are unsupported")
    if scenario.evidence:
        raise WorldKernelMappingError("evidence references cannot be resolved by this mapping")
    if scenario.forecast is not None:
        raise WorldKernelMappingError("forecast references cannot be resolved by this mapping")

    state = _nonnegative_integer_object(
        scenario.initial_state,
        name="initial_state",
        allowed_fields=_ALLOWED_STATE_FIELDS,
        required_fields=frozenset({"stock"}),
    )
    parameters = _nonnegative_integer_object(
        scenario.parameters,
        name="parameters",
        allowed_fields=_REQUIRED_PARAMETER_FIELDS,
        required_fields=_REQUIRED_PARAMETER_FIELDS,
    )

    effective_max_runs = min(
        operator_limits.max_runs,
        scenario.budget.max_simulation_runs,
    )
    if scenario.runs > effective_max_runs:
        raise WorldKernelMappingError(
            "scenario run count exceeds a scenario budget or operator limit"
        )
    if (
        scenario.horizon_days > operator_limits.max_steps
        or scenario.horizon_days * scenario.runs
        > operator_limits.max_total_transitions
    ):
        raise WorldKernelMappingError("scenario exceeds an operator limit")

    return {
        "schema_version": "worldkernel.simulation.v1",
        "world": mapping.target_world,
        "world_version": mapping.target_world_version,
        "steps": scenario.horizon_days,
        "runs": scenario.runs,
        "seed": scenario.seed,
        "initial_state": state,
        "parameters": parameters,
        "limits": {
            "max_steps": operator_limits.max_steps,
            "max_runs": effective_max_runs,
            "max_total_transitions": operator_limits.max_total_transitions,
        },
    }
