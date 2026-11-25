"""Exercise the no-argument synthetic retail policy CLI."""

import json

from examples.m1_retail_policy_test_double import main


def test_synthetic_policy_cli_replays_paired_comparison(capsys) -> None:
    assert main() == 0
    first = capsys.readouterr().out
    assert main() == 0
    second = capsys.readouterr().out

    assert first == second
    report = json.loads(first)
    assert report["fixture_label"] == "fictional_demo"
    assert report["simulation_status"] == "experimental_local_test_double_only"
    assert report["engine_execution"] == "worldkernel_not_invoked"
    assert report["decision_status"] == (
        "comparison_only_no_policy_selection_or_authorization"
    )
    assert "modeling_caveats" in report
    assert any(
        "not a standard or optimized" in caveat
        for caveat in report["modeling_caveats"]
    )
    assert len(report["lead_time_sensitivity"]) == 3
    assert all(
        len(scenario["policies"]) == 3
        for scenario in report["lead_time_sensitivity"]
    )
