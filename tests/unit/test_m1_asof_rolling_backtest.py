"""Synthetic integration: every rolling forecast needs published lag-7 history."""
import json
from math import sqrt
from pathlib import Path

import pytest

from examples import m1_asof_rolling_backtest as model

ROOT = Path(__file__).resolve().parents[2]


def fixture():
    return json.loads(
        (ROOT / "examples/synthetic-asof-weekly-sales.json").read_text(encoding="utf-8")
    )


def test_late_weekly_observation_causes_three_safe_abstentions():
    report = model.backtest_asof(fixture())
    assert report["status"] == "synthetic_asof_rolling_evaluation_not_real_forecast"
    assert report["requested_origins"] == 7
    assert report["abstained_origins"] == 3
    assert report["scored_origins"] == 4
    assert report["lower_mae_on_scored_synthetic_origins"] == "seasonal_naive_lag7"
    assert report["metrics"]["seasonal_naive_lag7"]["mae"] == 0
    mean = report["metrics"]["trailing_mean_lag7"]
    assert mean["mae"] == pytest.approx(3.0)
    assert mean["rmse"] == pytest.approx(sqrt(14))
    assert mean["bias"] == pytest.approx(-3.0)
    assert mean["wape"] == pytest.approx(3 / 11)


def test_origin_inputs_use_only_full_last_seven_available_dates(monkeypatch):
    data = fixture()
    rows = data["records"]
    inputs = []
    actual = model._predict

    def observe(past):
        inputs.append(past)
        return actual(past)

    monkeypatch.setattr(model, "_predict", observe)
    model.backtest_asof(data)
    assert inputs == [
        tuple(row["units"] for row in rows[index - 7:index])
        for index in range(31, 35)
    ]
    assert all(len(history) == 7 for history in inputs)


def test_same_pattern_with_immediate_publication_scores_all_origins():
    data = fixture()
    data["records"][26]["available_on"] = "2025-01-27"
    report = model.backtest_asof(data)
    assert report["scored_origins"] == 7
    assert report["abstained_origins"] == 0
    assert report["metrics"]["seasonal_naive_lag7"]["mae"] == 0.0


def test_unreleased_evaluation_target_fails_closed():
    data = fixture()
    data["records"][-1]["available_on"] = "2025-02-05"
    with pytest.raises(ValueError, match="held-out target was not published"):
        model.backtest_asof(data)


def test_missing_event_day_not_imputed_even_with_publication_metadata():
    data = fixture()
    del data["records"][3]
    with pytest.raises(ValueError, match="missing event-date record"):
        model.backtest_asof(data)


def test_all_origins_can_abstain_without_fake_scores():
    data = fixture()
    for row in data["records"][21:28]:
        row["available_on"] = "2025-03-01"
    report = model.backtest_asof(data)
    assert report["status"] == "synthetic_asof_rolling_abstained"
    assert report["scored_origins"] == 0
    assert report["abstained_origins"] == 7
    assert report["metrics"] is None
    assert report["lower_mae_on_scored_synthetic_origins"] is None


def test_one_eligible_origin_also_abstains_from_reporting_scores():
    data = fixture()
    data["records"][28]["available_on"] = "2025-02-03"
    report = model.backtest_asof(data, holdout_days=2)
    assert report["scored_origins"] == 1
    assert report["abstained_origins"] == 1
    assert report["metrics"] is None


@pytest.mark.parametrize("bad", [True, 1, 101, 2.1, "7"])
def test_invalid_origin_budget_rejected(bad):
    with pytest.raises(ValueError, match="holdout_days"):
        model.backtest_asof(fixture(), holdout_days=bad)
