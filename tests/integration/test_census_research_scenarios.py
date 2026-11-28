"""Fictional scenario selection and commitment isolation."""
import json

import pytest

from examples import m1_census_research_observatory as observatory
from examples import m1_census_research_runner as runner

REV = "27ca278e6c41ef79790c6492f94c25b179439958"


def test_scenario_catalog_preserves_default_and_separates_commitments():
    assert runner.build_fixture() == runner.build_fixture(runner.FIXTURE)
    reports = [runner.prepare_report(REV, scenario) for scenario in runner.SCENARIOS]
    assert len(reports) == 4
    assert len({r["experiment_sha256"] for r in reports}) == 4
    assert len({r["input_manifest_sha256"] for r in reports}) == 4
    assert len({r["schedule_sha256"] for r in reports}) == 1
    assert reports[0] == runner.prepare_report(REV)
    assert reports[0]["experiment_sha256"] == (
        "8b037d7514a2232b05b4d233ee55a36802d6d497de79b2af273c7a6156bdf620"
    )


@pytest.mark.parametrize("scenario", runner.SCENARIOS)
def test_scenario_full_replay_and_expected_metrics(tmp_path, scenario):
    expected = runner.prepare_report(REV, scenario)["experiment_sha256"]
    kwargs = {
        "journal_path": tmp_path / "journal.sqlite", "expected": expected,
        "splits": ("validation", "holdout"), "commitment_mode": "self_generated_demo",
        "scenario": scenario,
    }
    result = runner.run_research(REV, **kwargs)
    assert result == runner.run_research(REV, **kwargs)
    assert result["fixture"] == scenario
    assert result["inference_status"] == "abstained"
    assert result["holdout_lock_verified"] is False
    assert all(s["stored_replay_matched"] and s["winner"] is None for s in result["splits"])
    actual = [
        [h["metrics"]["seasonal_naive_lag12"]["mae"],
         h["metrics"]["trailing_12_month_mean"]["mae"]]
        for h in result["splits"][1]["horizons"]
    ]
    expected_metrics = {
        runner.FIXTURE: [[24, 15], [24, 17], [24, 21.2]],
        "fictional-flat-v1": [[0, 0], [0, 0], [0, 0]],
        "fictional-volatile-v1": [[36, 313/12], [30.9, 1283/60], [44.1, 1681/60]],
        "fictional-regime-shift-v1": [[56, 43.5], [72, 58], [80, 64.2]],
    }
    for a, b in zip(actual, expected_metrics[scenario], strict=True):
        assert a == pytest.approx(b)
    if scenario == runner.FIXTURE:
        assert result["report_sha256"] == (
            "1939ed6baf227ef91d7d88c1c17f1b641bfd4912ea7901a68b80e564af47ccac"
        )
    assert scenario in observatory.build_observatory(REV, ("holdout",), scenario)


def test_scenario_cross_commitment_rejected_before_journal(tmp_path):
    path = tmp_path / "never.sqlite"
    expected = runner.prepare_report(REV)["experiment_sha256"]
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        runner.run_research(
            REV, journal_path=path, expected=expected, splits=("validation",),
            commitment_mode="caller_retained", scenario="fictional-flat-v1",
        )
    assert not path.exists()


def test_unknown_scenario_rejected():
    for bad in ("arbitrary", None, True):
        with pytest.raises(ValueError, match="unknown fictional scenario"):
            runner.build_fixture(bad)


def test_scenario_cli_selection(monkeypatch, capsys):
    import sys

    monkeypatch.setattr(sys, "argv", [
        "runner", "prepare", "--revision", REV, "--scenario", "fictional-flat-v1"
    ])
    assert runner.main() == 0
    assert json.loads(capsys.readouterr().out)["fixture"] == "fictional-flat-v1"
