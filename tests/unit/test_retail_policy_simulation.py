"""Regression tests for the local synthetic retail policy test double."""

import subprocess
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from mirrormind.domains.retail.policy_simulation import (
    RetailPolicyAssumptions,
    RetailPolicyComparisonRequest,
    _order_quantity,
    compare_synthetic_retail_policies,
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
        "replications": 5,
        "seed": 317,
    }
    values.update(changes)
    return RetailPolicyComparisonRequest.model_validate(values)


def test_three_policies_share_each_reproducible_demand_stream() -> None:
    request = _request()

    first = compare_synthetic_retail_policies(request)
    second = compare_synthetic_retail_policies(request)

    assert first == second
    assert first["horizon_days"] == 28
    assert first["simulation_status"] == "experimental_local_test_double_only"
    scenarios = first["lead_time_sensitivity"]
    assert [item["lead_time_days"] for item in scenarios] == [1, 2, 3]
    for scenario in scenarios:
        policies = scenario["policies"]
        assert [item["policy_id"] for item in policies] == [
            "fixed_cycle_quantity",
            "reorder_point_fixed_quantity",
            "forecast_aware_order_up_to",
        ]
        digest_lists = [
            [run["demand_stream_sha256"] for run in item["replication_results"]]
            for item in policies
        ]
        assert digest_lists[0] == digest_lists[1] == digest_lists[2]
        assert all(len(item["replication_results"]) == 5 for item in policies)


def test_seed_changes_paired_exogenous_stream_digests() -> None:
    baseline = compare_synthetic_retail_policies(_request())
    changed = compare_synthetic_retail_policies(_request(seed=318))

    baseline_digests = baseline["lead_time_sensitivity"][1]["policies"][0][
        "replication_results"
    ]
    changed_digests = changed["lead_time_sensitivity"][1]["policies"][0][
        "replication_results"
    ]
    assert [row["demand_stream_sha256"] for row in baseline_digests] != [
        row["demand_stream_sha256"] for row in changed_digests
    ]


def test_policy_rules_can_produce_distinct_conditional_outcomes() -> None:
    result = compare_synthetic_retail_policies(_request())
    policies = result["lead_time_sensitivity"][1]["policies"]
    mean_costs = {
        policy["mean_metrics_per_replication"]["total_cost_units"]
        for policy in policies
    }

    assert len(mean_costs) > 1


def test_profile_aware_target_stops_before_arrival_day() -> None:
    request = _request()
    inputs = {
        "policy_id": "forecast_aware_order_up_to",
        "day_index": 0,
        "inventory_position_units": 0,
        "demand_profile_units": request.demand_profile_units,
        "assumptions": request.assumptions,
    }

    assert _order_quantity(**inputs, lead_time_days=1) == 8
    assert _order_quantity(**inputs, lead_time_days=2) == 17


def test_summary_reports_inventory_service_and_synthetic_cost_components() -> None:
    result = compare_synthetic_retail_policies(_request())
    policy = result["lead_time_sensitivity"][1]["policies"][0]
    metrics = policy["aggregate_metrics_across_replications"]

    assert result["quantity_unit"] == "item"
    assert result["time_unit"] == "day"
    assert result["cost_unit"] == "synthetic_cost_unit"
    assert metrics["fulfilled_units"] >= 0
    assert metrics["unmet_units"] >= 0
    assert 0 <= metrics["fill_rate_basis_points"] <= 10_000
    assert metrics["stockout_days"] >= 0
    assert metrics["ending_on_hand_units"] >= 0
    assert metrics["pending_order_units"] >= 0
    assert metrics["order_count"] >= 0
    assert metrics["total_cost_units"] == sum(
        metrics[key]
        for key in (
            "procurement_cost_units",
            "holding_cost_units",
            "fixed_order_cost_units",
            "unmet_demand_cost_units",
        )
    )


def test_invalid_profile_and_unsupported_units_fail_closed() -> None:
    with pytest.raises(ValidationError):
        _request(demand_profile_units=(1, 2, 3))

    with pytest.raises(ValidationError):
        RetailPolicyAssumptions.model_validate(
            {
                "initial_stock_units": 10,
                "lead_time_days": 1,
                "fixed_order_quantity_units": 5,
                "reorder_point_units": 5,
                "review_period_days": 7,
                "safety_stock_units": 2,
                "procurement_cost_per_unit": 1,
                "holding_cost_per_unit_day": 1,
                "fixed_order_cost": 1,
                "unmet_demand_penalty_per_unit": 1,
                "quantity_unit": "case",
            }
        )

    with pytest.raises(ValidationError):
        _request(replications=250)


def test_out_of_range_profile_stock_cost_and_seed_fail_validation() -> None:
    request = _request()
    assumptions = request.assumptions.model_dump()
    invalid_inputs: tuple[dict[str, object], ...] = (
        {
            "demand_profile_units": (1_001, *request.demand_profile_units[1:]),
        },
        {
            "assumptions": {**assumptions, "initial_stock_units": 10_001},
        },
        {
            "assumptions": {**assumptions, "procurement_cost_per_unit": 10_001},
        },
        {"seed": 1 << 32},
    )

    for invalid_input in invalid_inputs:
        with pytest.raises(ValidationError):
            _request(**invalid_input)


def test_sensitivity_reuses_the_same_paired_streams() -> None:
    result = compare_synthetic_retail_policies(_request())
    scenarios = result["lead_time_sensitivity"]
    expected = [
        row["demand_stream_sha256"]
        for row in scenarios[0]["policies"][0]["replication_results"]
    ]

    assert all(
        [row["demand_stream_sha256"] for row in scenario["policies"][2]["replication_results"]]
        == expected
        for scenario in scenarios
    )


def test_policy_test_double_does_not_import_worldkernel() -> None:
    root = Path(__file__).resolve().parents[2]
    script = """
import builtins
original_import = builtins.__import__
def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name.split('.', 1)[0].lower().startswith('worldkernel'):
        raise AssertionError('optional WorldKernel dependency imported')
    return original_import(name, globals, locals, fromlist, level)
builtins.__import__ = guarded_import
import mirrormind.domains.retail.policy_simulation
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=root,
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
