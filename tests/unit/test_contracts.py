"""Pure contract validation tests (no HTTP server)."""
import pytest
from pydantic import ValidationError

from mirrormind.core.contracts import ScenarioSpec


def test_valid_scenario():
    scenario = ScenarioSpec(
        world_type="retail.inventory",
        world_version="0.1",
        horizon_days=28,
        runs=4,
        budget={"max_simulation_runs": 4},
    )
    assert scenario.world_type == "retail.inventory"


def test_exceeding_budget_rejected():
    with pytest.raises(ValidationError):
        ScenarioSpec(
            world_type="retail.inventory",
            world_version="0.1",
            horizon_days=28,
            runs=5,
            budget={"max_simulation_runs": 4},
        )


def test_forecast_coverage_rejected():
    with pytest.raises(ValidationError):
        ScenarioSpec(
            world_type="retail.inventory",
            world_version="0.1",
            horizon_days=28,
            forecast={"forecast_id": "x", "model_version": "0", "horizon_days": 7},
        )
