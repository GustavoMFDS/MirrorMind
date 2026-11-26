"""Run the pinned WorldKernel inventory demo on synthetic scenario input.

Install the optional reviewed local engine with ``pip install -e ".[worldkernel]"``
then run ``python -m examples.m1e_02_worldkernel_local_runner``. This example
does not read files, call the network, or produce a business recommendation.
"""
from __future__ import annotations

import json

from mirrormind.core.contracts import ScenarioSpec
from mirrormind.modules.simulation.worldkernel_mapping import (
    InventoryWorldUnitContext,
    WorldKernelOperatorLimits,
)
from mirrormind.modules.simulation.worldkernel_runner import (
    LocalWorldKernelGateway,
    WorldKernelRunnerError,
)


def build_synthetic_scenario() -> ScenarioSpec:
    """Create one fictional inventory case with declared item/day/order units."""
    return ScenarioSpec.model_validate(
        {
            "world_type": "retail.inventory",
            "world_version": "0.1",
            "horizon_days": 5,
            "runs": 3,
            "seed": 2026,
            "initial_state": {"stock": 20, "sold": 0, "unmet": 0, "orders": 0},
            "parameters": {
                "daily_demand": 4,
                "reorder_point": 8,
                "reorder_quantity": 12,
            },
            "budget": {"max_simulation_runs": 3, "timeout_seconds": 20},
        }
    )


def run_synthetic_local_simulation() -> dict[str, object]:
    """Execute a real pinned engine on the fixed fictional scenario."""
    gateway = LocalWorldKernelGateway(
        operator_limits=WorldKernelOperatorLimits(
            max_steps=5,
            max_runs=3,
            max_total_transitions=15,
        ),
        unit_context=InventoryWorldUnitContext(
            quantity_unit="item",
            step_unit="day",
            order_unit="order",
        ),
    )
    summary = gateway.execute(build_synthetic_scenario())
    return summary.model_dump(mode="json")


def main() -> int:
    try:
        result = run_synthetic_local_simulation()
    except WorldKernelRunnerError as exc:
        raise SystemExit(f"Local WorldKernel simulation unavailable: {exc}") from None
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
