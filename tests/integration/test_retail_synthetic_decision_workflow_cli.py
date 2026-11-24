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
    assert result["schema_version"] == "mirrormind.synthetic_retail_decision_workflow.v1"
    assert result["status"] == "synthetic_comparison_ready_experimental"
    assert len(result["forecast"]["profile_units"]) == 28
    assert len(result["trace"]["forecasts"]) == 28
    assert len(result["trace"]["outcomes"]) == 9
    assert len(result["trace_sha256"]) == 64
    assert result["worldkernel_execution"] == "worldkernel_not_invoked"
    assert result["action_authorized"] is False
