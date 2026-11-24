"""Pure tests for the strict, optional WorldKernel request boundary."""
import builtins
import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

import mirrormind.modules.simulation.worldkernel_mapping as mapping_module
from mirrormind.core.contracts import ScenarioSpec
from mirrormind.modules.simulation.worldkernel_mapping import (
    InventoryWorldUnitContext,
    WorldKernelMappingError,
    WorldKernelOperatorLimits,
    build_worldkernel_exchange_request,
)


def _scenario(**changes: object) -> ScenarioSpec:
    payload: dict[str, object] = {
        "world_type": "retail.inventory",
        "world_version": "0.1",
        "horizon_days": 28,
        "runs": 3,
        "seed": 42,
        "initial_state": {"stock": 150, "sold": 0, "unmet": 0, "orders": 0},
        "parameters": {
            "daily_demand": 10,
            "reorder_point": 30,
            "reorder_quantity": 75,
        },
        "budget": {"max_simulation_runs": 100},
    }
    payload.update(changes)
    return ScenarioSpec.model_validate(payload)


def _limits(**changes: int) -> WorldKernelOperatorLimits:
    values = {
        "max_steps": 28,
        "max_runs": 10,
        "max_total_transitions": 280,
    }
    values.update(changes)
    return WorldKernelOperatorLimits(**values)


def _units(**changes: str) -> InventoryWorldUnitContext:
    values = {
        "quantity_unit": "item",
        "step_unit": "day",
        "order_unit": "order",
    }
    values.update(changes)
    return InventoryWorldUnitContext(**values)


def _map(
    scenario: ScenarioSpec | None = None,
    *,
    operator_limits: WorldKernelOperatorLimits | None = None,
    unit_context: InventoryWorldUnitContext | None = None,
) -> dict[str, object]:
    return build_worldkernel_exchange_request(
        scenario or _scenario(),
        operator_limits=operator_limits or _limits(),
        unit_context=unit_context or _units(),
    )


def test_supported_inventory_scenario_maps_to_exact_v1_request() -> None:
    assert _map() == {
        "schema_version": "worldkernel.simulation.v1",
        "world": "retail.inventory.demo",
        "world_version": "demo-1",
        "steps": 28,
        "runs": 3,
        "seed": 42,
        "initial_state": {"stock": 150, "sold": 0, "unmet": 0, "orders": 0},
        "parameters": {
            "daily_demand": 10,
            "reorder_point": 30,
            "reorder_quantity": 75,
        },
        "limits": {
            "max_steps": 28,
            "max_runs": 10,
            "max_total_transitions": 280,
        },
    }


def test_mapping_is_deterministic_and_uses_operator_limits() -> None:
    scenario = _scenario(budget={"max_simulation_runs": 100})
    operator_limits = _limits(max_steps=30, max_runs=12, max_total_transitions=360)

    first = build_worldkernel_exchange_request(
        scenario, operator_limits=operator_limits, unit_context=_units()
    )
    second = build_worldkernel_exchange_request(
        scenario, operator_limits=operator_limits, unit_context=_units()
    )

    assert first == second
    assert first["limits"] == {
        "max_steps": 30,
        "max_runs": 12,
        "max_total_transitions": 360,
    }


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"world_type": "retail.other"}, "world mapping"),
        ({"world_version": "0.2"}, "world mapping"),
        ({"interventions": [{"kind": "reorder_policy"}]}, "interventions"),
        ({"evidence": [{"source_id": "s", "snapshot_id": "v1", "observed_until": "2026-01-01", "provenance": "fixture"}]}, "evidence"),
        ({"forecast": {"forecast_id": "f1", "model_version": "m1", "horizon_days": 28}}, "forecast"),
    ],
)
def test_unrepresentable_scenario_fields_are_rejected(
    changes: dict[str, object], message: str
) -> None:
    with pytest.raises(WorldKernelMappingError, match=message):
        _map(_scenario(**changes))


def test_state_requires_stock_and_rejects_unknown_fields() -> None:
    with pytest.raises(WorldKernelMappingError, match="stock"):
        _map(_scenario(initial_state={"sold": 0, "unmet": 0, "orders": 0}))
    with pytest.raises(WorldKernelMappingError, match="state fields"):
        _map(_scenario(initial_state={"stock": 20, "backlog": 2}))


@pytest.mark.parametrize("state", [{"stock": -1}, {"stock": True}, {"stock": 2.5}])
def test_state_values_must_be_nonnegative_integers(state: dict[str, object]) -> None:
    with pytest.raises(WorldKernelMappingError, match="non-negative integer"):
        _map(_scenario(initial_state=state))


def test_parameters_are_explicit_and_allowlisted() -> None:
    with pytest.raises(WorldKernelMappingError, match="daily_demand"):
        _map(_scenario(parameters={"reorder_point": 30, "reorder_quantity": 75}))
    with pytest.raises(WorldKernelMappingError, match="parameters fields"):
        _map(
            _scenario(
                parameters={
                    "daily_demand": 10,
                    "reorder_point": 30,
                    "reorder_quantity": 75,
                    "lead_time_days": 2,
                }
            )
        )


@pytest.mark.parametrize("value", [-1, True, 1.5])
def test_parameter_values_must_be_nonnegative_integers(value: object) -> None:
    with pytest.raises(WorldKernelMappingError, match="non-negative integer"):
        _map(_scenario(parameters={"daily_demand": value, "reorder_point": 30, "reorder_quantity": 75}))


def test_unknown_units_are_rejected() -> None:
    with pytest.raises(WorldKernelMappingError, match="unit context"):
        _map(unit_context=_units(quantity_unit="case"))


@pytest.mark.parametrize(
    ("scenario_changes", "limit_changes"),
    [
        ({"horizon_days": 29}, {"max_steps": 28}),
        ({"runs": 11, "budget": {"max_simulation_runs": 11}}, {"max_runs": 10}),
        ({"runs": 4, "budget": {"max_simulation_runs": 4}}, {"max_total_transitions": 100}),
    ],
)
def test_operator_limits_reject_steps_runs_and_total_work(
    scenario_changes: dict[str, object], limit_changes: dict[str, int]
) -> None:
    with pytest.raises(WorldKernelMappingError, match="operator limit"):
        _map(_scenario(**scenario_changes), operator_limits=_limits(**limit_changes))


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("max_steps", 0),
        ("max_steps", True),
        ("max_runs", 10_001),
        ("max_total_transitions", 3_660_001),
    ],
)
def test_operator_limit_configuration_has_hard_contract_bounds(
    name: str, value: int
) -> None:
    with pytest.raises(ValueError):
        WorldKernelOperatorLimits(
            max_steps=28 if name != "max_steps" else value,
            max_runs=10 if name != "max_runs" else value,
            max_total_transitions=280 if name != "max_total_transitions" else value,
        )


def test_mapping_module_imports_without_worldkernel_package(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def reject_worldkernel(name: str, *args: object, **kwargs: object) -> object:
        if name == "worldkernel" or name.startswith("worldkernel."):
            raise AssertionError("mapping must not import WorldKernel")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_worldkernel)
    importlib.reload(mapping_module)


def test_api_app_imports_without_worldkernel_package() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    script = """
import builtins
original_import = builtins.__import__
def reject_worldkernel(name, *args, **kwargs):
    if name == "worldkernel" or name.startswith("worldkernel."):
        raise AssertionError("API attempted to import WorldKernel")
    return original_import(name, *args, **kwargs)
builtins.__import__ = reject_worldkernel
from mirrormind.api.app import app
assert app is not None
"""
    environment = dict(os.environ)
    source_path = str(repository_root / "src")
    existing_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        source_path + os.pathsep + existing_path if existing_path else source_path
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=repository_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
