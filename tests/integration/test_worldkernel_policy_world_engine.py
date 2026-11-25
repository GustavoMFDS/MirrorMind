"""Exact-pin WorldKernel regressions for the synthetic M1 policy path."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from importlib import metadata
from pathlib import Path
from urllib.parse import urlsplit

import pytest

from mirrormind.domains.retail.policy_simulation import (
    RetailPolicyComparisonRequest,
    compare_synthetic_retail_policies,
)
from mirrormind.modules.simulation.worldkernel_mapping import WorldKernelOperatorLimits
from mirrormind.modules.simulation.worldkernel_policy_gateway import (
    LocalWorldKernelRetailPolicyGateway,
)
from mirrormind.modules.simulation.worldkernel_runner import WORLDKERNEL_SOURCE_COMMIT


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
    url = direct_url.get("url", "")
    parsed = urlsplit(url.removeprefix("git+")) if isinstance(url, str) else None
    repository = (
        f"{parsed.netloc}/{parsed.path.strip('/').removesuffix('.git')}".lower()
        if parsed is not None
        else ""
    )
    vcs_info = direct_url.get("vcs_info", {})
    return (
        distribution.version == "0.0.1"
        and repository == "github.com/gustavomfds/worldkernel"
        and vcs_info.get("vcs") == "git"
        and vcs_info.get("commit_id") == WORLDKERNEL_SOURCE_COMMIT
    )


pytestmark = pytest.mark.skipif(
    not _installed_pin_matches(),
    reason="optional WorldKernel package is not installed at the reviewed commit",
)


def _request() -> RetailPolicyComparisonRequest:
    return RetailPolicyComparisonRequest.model_validate(
        {
            "demand_profile_units": tuple(8 + day % 3 for day in range(28)),
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
    )


def test_pinned_engine_policy_gateway_matches_synthetic_reference() -> None:
    request = _request()
    gateway = LocalWorldKernelRetailPolicyGateway(
        operator_limits=WorldKernelOperatorLimits(
            max_steps=28,
            max_runs=4,
            max_total_transitions=2_000,
        )
    )

    actual = gateway.compare(request)
    expected = compare_synthetic_retail_policies(request)

    assert actual["engine_execution"] == "worldkernel_invoked"
    assert actual["simulation_status"] == "experimental_local_worldkernel_policy_world"
    assert actual["lead_time_sensitivity"] == expected["lead_time_sensitivity"]
    assert actual["worldkernel_execution"]["source_commit"] == WORLDKERNEL_SOURCE_COMMIT
    assert len(actual["worldkernel_execution"]["result_sha256"]) == 64


def test_m1_cli_worldkernel_option_runs_end_to_end_with_synthetic_data() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    environment = dict(os.environ)
    source_path = str(repository_root / "src")
    existing_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        source_path + os.pathsep + existing_path if existing_path else source_path
    )
    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "examples.m1_retail_decision_workflow",
            "--as-of",
            "2011-01-26",
            "--replications",
            "2",
            "--seed",
            "317",
            "--engine",
            "worldkernel",
        ],
        cwd=repository_root,
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )

    assert process.returncode == 0, process.stderr
    result = json.loads(process.stdout)
    assert result["status"] == "synthetic_comparison_ready_experimental"
    assert result["worldkernel_execution"] == "worldkernel_invoked"
    assert result["simulation"]["policy_test_double_invoked"] is False
    policy_result = result["simulation"]["result"]
    assert policy_result["engine_execution"] == "worldkernel_invoked"
    assert policy_result["lead_time_sensitivity"]
    assert len(result["trace_sha256"]) == 64
    assert all(
        gap["gap_id"] != "gap-worldkernel-execution"
        for gap in result["trace"]["missing_evidence"]
    )
