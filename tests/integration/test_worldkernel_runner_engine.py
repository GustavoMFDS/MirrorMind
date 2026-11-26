"""Execute the pinned WorldKernel demo using fictional input only."""
from __future__ import annotations

import json
from importlib import metadata

import pytest

from mirrormind.core.contracts import ScenarioSpec
from mirrormind.modules.simulation.worldkernel_mapping import (
    InventoryWorldUnitContext,
    WorldKernelOperatorLimits,
)
from mirrormind.modules.simulation.worldkernel_runner import (
    WORLDKERNEL_SOURCE_COMMIT,
    LocalWorldKernelGateway,
)


def _installed_pin_matches() -> bool:
    try:
        distribution = metadata.distribution("worldkernel")
        direct_url_text = distribution.read_text("direct_url.json")
    except metadata.PackageNotFoundError:
        return False
    if not direct_url_text:
        return False
    try:
        direct_url = json.loads(direct_url_text)
    except json.JSONDecodeError:
        return False
    vcs_info = direct_url.get("vcs_info", {})
    return (
        distribution.version == "0.0.1"
        and vcs_info.get("vcs") == "git"
        and vcs_info.get("commit_id") == WORLDKERNEL_SOURCE_COMMIT
    )


pytestmark = pytest.mark.skipif(
    not _installed_pin_matches(),
    reason="optional WorldKernel package is not installed at the reviewed commit",
)


def test_pinned_local_runner_executes_synthetic_inventory_world_deterministically() -> None:
    scenario = ScenarioSpec.model_validate(
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
    limits = WorldKernelOperatorLimits(
        max_steps=5,
        max_runs=3,
        max_total_transitions=15,
    )
    units = InventoryWorldUnitContext(
        quantity_unit="item",
        step_unit="day",
        order_unit="order",
    )

    gateway = LocalWorldKernelGateway(operator_limits=limits, unit_context=units)
    first = gateway.execute(scenario)
    second = gateway.execute(scenario)

    assert first == second
    assert first.engine_version == (
        f"worldkernel/0.0.1@{WORLDKERNEL_SOURCE_COMMIT}"
    )
    assert first.run_count == 3
    assert first.results["engine_result_schema"] == "worldkernel.result.v1"
    assert first.results["world"] == "retail.inventory.demo"
    assert len(first.results["final_states"]) == 3
    for state in first.results["final_states"]:
        assert 20 + state["orders"] * 12 == state["stock"] + state["sold"]
    assert any("does not model lead time" in item for item in first.assumptions)
