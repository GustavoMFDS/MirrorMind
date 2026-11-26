"""Synthetic regressions for the optional, bounded WorldKernel worker."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from mirrormind.core.contracts import ScenarioSpec
from mirrormind.modules.simulation import worldkernel_runner, worldkernel_worker
from mirrormind.modules.simulation.worldkernel_mapping import (
    InventoryWorldUnitContext,
    WorldKernelMappingError,
    WorldKernelOperatorLimits,
)
from mirrormind.modules.simulation.worldkernel_runner import (
    WorldKernelExecutionTimeout,
    WorldKernelOutputLimitExceeded,
    WorldKernelRunnerError,
    WorldKernelRuntimeConfig,
    WorldKernelRuntimeUnavailable,
    run_worldkernel_scenario,
)


def _scenario(**changes: object) -> ScenarioSpec:
    payload: dict[str, object] = {
        "world_type": "retail.inventory",
        "world_version": "0.1",
        "horizon_days": 3,
        "runs": 2,
        "seed": 27,
        "initial_state": {"stock": 20, "sold": 0, "unmet": 0, "orders": 0},
        "parameters": {
            "daily_demand": 4,
            "reorder_point": 8,
            "reorder_quantity": 12,
        },
        "budget": {"max_simulation_runs": 5, "timeout_seconds": 5},
    }
    payload.update(changes)
    return ScenarioSpec.model_validate(payload)


def _limits() -> WorldKernelOperatorLimits:
    return WorldKernelOperatorLimits(
        max_steps=4,
        max_runs=4,
        max_total_transitions=16,
    )


def _units() -> InventoryWorldUnitContext:
    return InventoryWorldUnitContext(
        quantity_unit="item",
        step_unit="day",
        order_unit="order",
    )


def _install_fake_worker(monkeypatch: pytest.MonkeyPatch, tmp_path, source: str) -> None:
    worker = tmp_path / "fake_worldkernel_worker.py"
    worker.write_text(source, encoding="utf-8")
    monkeypatch.setattr(worldkernel_runner, "_WORKER_SCRIPT", worker)


def _fake_distribution(*, commit: str, version: str = "0.0.1") -> SimpleNamespace:
    source = {
        "url": "https://github.com/GustavoMFDS/WorldKernel.git",
        "vcs_info": {"vcs": "git", "commit_id": commit},
    }
    return SimpleNamespace(version=version, read_text=lambda _name: json.dumps(source))


def test_worker_accepts_exact_pep610_repository_and_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    distribution = _fake_distribution(
        commit=worldkernel_runner.WORLDKERNEL_SOURCE_COMMIT
    )
    monkeypatch.setattr(
        worldkernel_worker.metadata,
        "distribution",
        lambda name: distribution if name == "worldkernel" else None,
    )

    worldkernel_worker._verify_installed_runtime(
        worldkernel_runner.WORLDKERNEL_SOURCE_COMMIT
    )


def test_worker_rejects_different_pep610_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    distribution = _fake_distribution(commit="0" * 40)
    monkeypatch.setattr(
        worldkernel_worker.metadata,
        "distribution",
        lambda _name: distribution,
    )

    with pytest.raises(worldkernel_worker._RuntimePinMismatch):
        worldkernel_worker._verify_installed_runtime(
            worldkernel_runner.WORLDKERNEL_SOURCE_COMMIT
        )


def test_worker_rejects_missing_optional_distribution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_distribution(_name: str):
        raise worldkernel_worker.metadata.PackageNotFoundError("worldkernel")

    monkeypatch.setattr(
        worldkernel_worker.metadata, "distribution", missing_distribution
    )

    with pytest.raises(worldkernel_worker._RuntimeMissing):
        worldkernel_worker._verify_installed_runtime(
            worldkernel_runner.WORLDKERNEL_SOURCE_COMMIT
        )


_VALID_RESULT_WORKER = r'''
import json
import sys
request = json.load(sys.stdin)
result = {
    "schema_version": "worldkernel.result.v1",
    "engine": "worldkernel",
    "engine_adapter_version": "1",
    "world": request["world"],
    "declared_world_version": request["world_version"],
    "registered_world_version": request["world_version"],
    "world_version_matches_registry": True,
    "runs": request["runs"],
    "steps": request["steps"],
    "seed": request["seed"],
    "final_states": [
        {"stock": 16, "sold": 4, "unmet": 0, "orders": 0}
        for _ in range(request["runs"])
    ],
    "assumptions": ["synthetic fake result for parent-protocol test"],
}
print(json.dumps(result, sort_keys=True, separators=(",", ":")))
'''


def test_local_runner_validates_result_and_creates_stable_summary(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _install_fake_worker(monkeypatch, tmp_path, _VALID_RESULT_WORKER)

    first = run_worldkernel_scenario(
        _scenario(), operator_limits=_limits(), unit_context=_units()
    )
    second = run_worldkernel_scenario(
        _scenario(), operator_limits=_limits(), unit_context=_units()
    )

    assert first == second
    assert first.run_count == 2
    assert first.engine_version.endswith("@" + worldkernel_runner.WORLDKERNEL_SOURCE_COMMIT)
    assert first.results["engine_result_schema"] == "worldkernel.result.v1"
    assert first.results["world"] == "retail.inventory.demo"
    assert len(first.results["final_states"]) == 2
    assert any("does not model lead time" in item for item in first.assumptions)


def test_local_runner_rejects_result_revision_mismatch(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    source = _VALID_RESULT_WORKER.replace(
        '"world_version_matches_registry": True',
        '"world_version_matches_registry": False',
    )
    _install_fake_worker(monkeypatch, tmp_path, source)

    with pytest.raises(WorldKernelRunnerError, match="revision mismatch"):
        run_worldkernel_scenario(
            _scenario(), operator_limits=_limits(), unit_context=_units()
        )


def test_local_runner_rejects_inventory_result_that_breaks_balance(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    source = _VALID_RESULT_WORKER.replace('"stock": 16', '"stock": 15')
    _install_fake_worker(monkeypatch, tmp_path, source)

    with pytest.raises(WorldKernelRunnerError, match="inventory balance"):
        run_worldkernel_scenario(
            _scenario(), operator_limits=_limits(), unit_context=_units()
        )


def test_local_runner_rejects_unknown_result_fields(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    source = _VALID_RESULT_WORKER.replace(
        '"engine": "worldkernel",',
        '"engine": "worldkernel",\n    "unexpected": "not in result v1",',
    )
    _install_fake_worker(monkeypatch, tmp_path, source)

    with pytest.raises(WorldKernelRunnerError, match="result fields"):
        run_worldkernel_scenario(
            _scenario(), operator_limits=_limits(), unit_context=_units()
        )


def test_local_runner_rejects_nonzero_model_budgets_before_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_spawned(*_args, **_kwargs):
        raise AssertionError("unsupported model budget must fail before spawning")

    monkeypatch.setattr(worldkernel_runner.subprocess, "Popen", fail_if_spawned)

    with pytest.raises(WorldKernelMappingError, match="model-call and token budgets"):
        run_worldkernel_scenario(
            _scenario(budget={"max_simulation_runs": 5, "max_model_calls": 1}),
            operator_limits=_limits(),
            unit_context=_units(),
        )


def test_local_runner_enforces_operator_wall_clock_timeout(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _install_fake_worker(
        monkeypatch,
        tmp_path,
        "import time\ntime.sleep(5)\n",
    )

    with pytest.raises(WorldKernelExecutionTimeout, match="local timeout"):
        run_worldkernel_scenario(
            _scenario(),
            operator_limits=_limits(),
            unit_context=_units(),
            runtime=WorldKernelRuntimeConfig(max_timeout_seconds=0.1),
        )


def test_scenario_timeout_cannot_exceed_effective_operator_deadline(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _install_fake_worker(
        monkeypatch,
        tmp_path,
        "import time\ntime.sleep(5)\n",
    )

    with pytest.raises(WorldKernelExecutionTimeout, match="local timeout"):
        run_worldkernel_scenario(
            _scenario(budget={"max_simulation_runs": 5, "timeout_seconds": 1}),
            operator_limits=_limits(),
            unit_context=_units(),
            runtime=WorldKernelRuntimeConfig(max_timeout_seconds=5),
        )


def test_local_runner_bounds_worker_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _install_fake_worker(monkeypatch, tmp_path, "print('x' * 128)\n")

    with pytest.raises(WorldKernelOutputLimitExceeded, match="output exceeded"):
        run_worldkernel_scenario(
            _scenario(),
            operator_limits=_limits(),
            unit_context=_units(),
            runtime=WorldKernelRuntimeConfig(max_output_bytes=32),
        )


def test_local_runner_bounds_worker_error_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _install_fake_worker(
        monkeypatch,
        tmp_path,
        "import sys\nsys.stderr.write('x' * 10000)\n",
    )

    with pytest.raises(WorldKernelOutputLimitExceeded, match="output exceeded"):
        run_worldkernel_scenario(
            _scenario(), operator_limits=_limits(), unit_context=_units()
        )


def test_local_runner_sanitizes_worker_failure_marker(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _install_fake_worker(
        monkeypatch,
        tmp_path,
        "import sys\nsys.stderr.write('WORLDKERNEL_PIN_MISMATCH\\n')\nsys.exit(2)\n",
    )

    with pytest.raises(WorldKernelRuntimeUnavailable, match="does not match") as error:
        run_worldkernel_scenario(
            _scenario(), operator_limits=_limits(), unit_context=_units()
        )
    assert "synthetic" not in str(error.value)


def test_local_runner_handles_missing_python_without_exposing_request(tmp_path) -> None:
    missing_python = tmp_path / "missing-python.exe"

    with pytest.raises(WorldKernelRuntimeUnavailable, match="runtime is unavailable") as error:
        run_worldkernel_scenario(
            _scenario(),
            operator_limits=_limits(),
            unit_context=_units(),
            runtime=WorldKernelRuntimeConfig(python_executable=str(missing_python)),
        )
    assert "daily_demand" not in str(error.value)


def test_api_import_does_not_require_worldkernel_package() -> None:
    script = r'''
import builtins
original_import = builtins.__import__
def reject_worldkernel(name, *args, **kwargs):
    if name == "worldkernel" or name.startswith("worldkernel."):
        raise AssertionError("API import attempted to load optional WorldKernel")
    return original_import(name, *args, **kwargs)
builtins.__import__ = reject_worldkernel
from mirrormind.api.app import app
assert app is not None
'''
    repository_root = Path(__file__).resolve().parents[2]
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
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
