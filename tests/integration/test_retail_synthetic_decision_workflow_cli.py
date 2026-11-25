"""Reproduce the full local synthetic decision comparison via its CLI."""
from __future__ import annotations

import json

from examples.m1_retail_decision_workflow import main


def test_synthetic_decision_cli_replays_trace_and_paired_policy_comparison(capsys):
    assert main([]) == 0
    first = capsys.readouterr().out
    assert main([]) == 0
    second = capsys.readouterr().out

    assert first == second
    result = json.loads(first)
    assert result["schema_version"] == "mirrormind.synthetic_retail_decision_workflow.v2"
    assert result["status"] == "synthetic_comparison_ready_experimental"
    assert len(result["forecast"]["profile_units"]) == 28
    assert len(result["trace"]["forecasts"]) == 28
    assert len(result["trace"]["outcomes"]) == 9
    assert result["trace"]["schema_version"] == "mirrormind.decision_trace.v2"
    assert result["simulation"]["selected_result_source"] == "policy_test_double"
    assert result["simulation"]["policy_test_double_invoked"] is True
    assert result["simulation"]["policy_test_double_result_selected"] is True
    selected = result["trace"]["execution_evidence"][0]
    assert selected["role"] == "selected_output"
    assert selected["engine_contract_ref"] == (
        "mirrormind.local.retail_policy_test_double.v1"
    )
    assert all(
        outcome["engine_contract_ref"] == selected["engine_contract_ref"]
        and outcome["execution_evidence_refs"] == [selected["execution_id"]]
        for outcome in result["trace"]["outcomes"]
    )
    assert len(result["trace_sha256"]) == 64
    assert result["worldkernel_execution"] == "worldkernel_not_invoked"
    assert result["action_authorized"] is False
