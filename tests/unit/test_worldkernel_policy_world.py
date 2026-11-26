"""Synthetic contract regressions for the locally registered policy world."""
from __future__ import annotations

import random

import pytest

from mirrormind.domains.retail.policy_simulation import (
    RetailPolicyComparisonRequest,
    _build_demand_streams,
    _lead_time_scenarios,
    compare_synthetic_retail_policies,
    finalize_retail_policy_metrics,
)
from mirrormind.domains.retail.worldkernel_policy_world import (
    POLICY_WORLD_NAME,
    POLICY_WORLD_VERSION,
    mirrormind_retail_policy_step,
    register_mirrormind_policy_world,
)
from mirrormind.modules.simulation import worldkernel_runner
from mirrormind.modules.simulation.worldkernel_mapping import (
    WorldKernelMappingError,
    WorldKernelOperatorLimits,
)
from mirrormind.modules.simulation.worldkernel_policy_gateway import (
    LocalWorldKernelRetailPolicyGateway,
)
from mirrormind.modules.simulation.worldkernel_policy_mapping import (
    build_worldkernel_policy_exchange_request,
)


def _request(**changes: object) -> RetailPolicyComparisonRequest:
    values: dict[str, object] = {
        "demand_profile_units": tuple(8 + (day % 3) for day in range(28)),
        "assumptions": {
            "initial_stock_units": 18,
            "lead_time_days": 2,
            "fixed_order_quantity_units": 24,
            "reorder_point_units": 20,
            "review_period_days": 7,
            "safety_stock_units": 8,
            "procurement_cost_per_unit": 3,
            "holding_cost_per_unit_day": 1,
            "fixed_order_cost": 5,
            "unmet_demand_penalty_per_unit": 10,
        },
        "replications": 2,
        "seed": 317,
    }
    values.update(changes)
    return RetailPolicyComparisonRequest.model_validate(values)


def _limits(**changes: int) -> WorldKernelOperatorLimits:
    values = {
        "max_steps": 28,
        "max_runs": 12,
        "max_total_transitions": 10_000,
    }
    values.update(changes)
    return WorldKernelOperatorLimits(**values)


def test_policy_mapper_targets_fixed_world_and_bounds_all_policy_transitions() -> None:
    request = _request()

    mapped = build_worldkernel_policy_exchange_request(
        request, operator_limits=_limits()
    )

    assert mapped["schema_version"] == "worldkernel.simulation.v1"
    assert mapped["world"] == POLICY_WORLD_NAME
    assert mapped["world_version"] == POLICY_WORLD_VERSION
    assert mapped["steps"] == 28
    assert mapped["runs"] == request.replications
    assert mapped["seed"] == request.seed
    assert mapped["parameters"]["lead_time_days"] == list(
        _lead_time_scenarios(request.assumptions.lead_time_days)
    )
    assert mapped["limits"]["max_total_transitions"] == 10_000 // 9


@pytest.mark.parametrize(
    ("limit_changes", "message"),
    [
        ({"max_steps": 27}, "step limit"),
        ({"max_runs": 1}, "run limit"),
        ({"max_total_transitions": 500}, "transition budget"),
    ],
)
def test_policy_mapper_rejects_operator_limits_before_worker_launch(
    limit_changes: dict[str, int], message: str
) -> None:
    with pytest.raises(WorldKernelMappingError, match=message):
        build_worldkernel_policy_exchange_request(
            _request(), operator_limits=_limits(**limit_changes)
        )


def test_policy_gateway_rejects_budget_before_starting_worker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_spawned(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("invalid policy budgets must fail before worker launch")

    monkeypatch.setattr(worldkernel_runner.subprocess, "Popen", fail_if_spawned)
    gateway = LocalWorldKernelRetailPolicyGateway(
        operator_limits=_limits(max_total_transitions=500)
    )

    with pytest.raises(WorldKernelMappingError, match="transition budget"):
        gateway.compare(_request())


def test_registered_handler_matches_reference_policy_metrics_and_shared_stream() -> None:
    request = _request(replications=1)
    mapped = build_worldkernel_policy_exchange_request(
        request, operator_limits=_limits()
    )
    state = mapped["initial_state"]
    parameters = mapped["parameters"]
    generator = random.Random(request.seed)

    for _ in range(28):
        state = mirrormind_retail_policy_step(state, parameters, generator)

    reference = compare_synthetic_retail_policies(request)
    reference_stream = _build_demand_streams(request)[0]
    assert state["day_index"] == 28
    assert tuple(state["demand_units"]) == reference_stream["demand_units"]
    for scenario in reference["lead_time_sensitivity"]:
        for policy in scenario["policies"]:
            engine_policy_state = state["policy_states"][str(scenario["lead_time_days"])][
                policy["policy_id"]
            ]
            assert finalize_retail_policy_metrics(
                engine_policy_state, request.assumptions
            ) == policy["replication_results"][0]["metrics"]


def test_registration_uses_only_code_owned_exact_world_revision() -> None:
    calls: list[tuple[str, object, str]] = []

    def capture(name: str, handler: object, *, version: str) -> None:
        calls.append((name, handler, version))

    register_mirrormind_policy_world(capture)

    assert len(calls) == 1
    name, handler, version = calls[0]
    assert name == POLICY_WORLD_NAME
    assert handler is mirrormind_retail_policy_step
    assert version == POLICY_WORLD_VERSION


def test_policy_gateway_rejects_malformed_world_state_from_worker(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    fake_worker = tmp_path / "malformed_policy_worker.py"
    fake_worker.write_text(
        """
import json, sys
request = json.load(sys.stdin)
print(json.dumps({
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
    "final_states": [{} for _ in range(request["runs"])],
    "assumptions": ["synthetic malformed-state fixture"],
}))
""",
        encoding="utf-8",
    )
    monkeypatch.setattr(worldkernel_runner, "_WORKER_SCRIPT", fake_worker)
    gateway = LocalWorldKernelRetailPolicyGateway(operator_limits=_limits())

    with pytest.raises(worldkernel_runner.WorldKernelRunnerError, match="final-state fields"):
        gateway.compare(_request())
