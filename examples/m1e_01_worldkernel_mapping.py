"""Print a synthetic request mapping; does not import or execute WorldKernel."""
import json

from mirrormind.core.contracts import ScenarioSpec
from mirrormind.modules.simulation.worldkernel_mapping import (
    InventoryWorldUnitContext,
    WorldKernelOperatorLimits,
    build_worldkernel_exchange_request,
)


def main() -> None:
    scenario = ScenarioSpec(
        world_type="retail.inventory",
        world_version="0.1",
        horizon_days=28,
        runs=3,
        seed=42,
        initial_state={"stock": 150, "sold": 0, "unmet": 0, "orders": 0},
        parameters={
            "daily_demand": 10,
            "reorder_point": 30,
            "reorder_quantity": 75,
        },
        budget={"max_simulation_runs": 100},
    )
    request = build_worldkernel_exchange_request(
        scenario,
        operator_limits=WorldKernelOperatorLimits(
            max_steps=28,
            max_runs=100,
            max_total_transitions=2800,
        ),
        unit_context=InventoryWorldUnitContext(
            quantity_unit="item",
            step_unit="day",
            order_unit="order",
        ),
    )
    print(json.dumps(request, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
