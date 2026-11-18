"""Leakage and metric regressions for a *synthetic* rolling-origin exercise."""
import json
from pathlib import Path

import pytest

from examples import m1_temporal_backtest as backtest

ROOT = Path(__file__).resolve().parents[2]


def fixture():
    return json.loads(
        (ROOT / "examples/synthetic-weekly-sales.json").read_text(encoding="utf-8")
    )


def test_seasonal_naive_is_exact_on_weekly_fixture_and_mean_is_not():
    report = backtest.backtest_batch(fixture())
    assert report["status"] == "synthetic_rolling_backtest_not_production_forecast"
    assert report["holdout_first_date"] == "2025-01-29"
    assert report["holdout_last_date"] == "2025-02-04"
    assert report["evaluated_origins"] == 7
    assert report["train_days_before_first_origin"] == 28
    assert report["lower_mae_on_this_fixture"] == "seasonal_naive_lag7"
    assert report["metrics"]["seasonal_naive_lag7"] == {
        "mae": 0.0, "rmse": 0.0, "bias": 0.0, "wape": 0.0
    }
    mean = report["metrics"]["trailing_mean_lag7"]
    assert mean["mae"] == pytest.approx(24 / 7)
    assert mean["rmse"] == pytest.approx(4.0)
    assert mean["bias"] == pytest.approx(0.0)
    assert mean["wape"] == pytest.approx(3 / 7)


def test_each_one_step_prediction_receives_only_prior_observations(monkeypatch):
    records = fixture()["records"]
    units = tuple(row["units"] for row in records)
    captured = []
    original = backtest._predict

    def checked(past):
        captured.append(tuple(past))
        return original(past)

    monkeypatch.setattr(backtest, "_predict", checked)
    report = backtest.backtest_batch(fixture())
    assert report["evaluated_origins"] == 7
    assert captured == [units[:i] for i in range(28, 35)]
    assert all(len(past) < len(units) for past in captured)


def test_missing_day_abstains_instead_of_zero_imputation():
    payload = fixture()
    del payload["records"][7]
    with pytest.raises(ValueError, match="daily series has gaps"):
        backtest.backtest_batch(payload)


def test_old_cutoff_rejects_future_target():
    payload = fixture()
    payload["cutoff_date"] = "2025-02-03"
    with pytest.raises(ValueError, match="exceeds declared cutoff"):
        backtest.backtest_batch(payload)


def test_cutoff_later_than_last_row_is_not_accepted_as_a_test_endpoint():
    payload = fixture()
    payload["cutoff_date"] = "2025-02-05"
    with pytest.raises(ValueError, match="cutoff must be the date"):
        backtest.backtest_batch(payload)


def test_explicitly_synthetic_labels_required_but_are_not_proof_of_provenance():
    payload = fixture()
    payload["source_id"] = "unverified-private-system"
    with pytest.raises(ValueError, match="explicitly labeled synthetic"):
        backtest.backtest_batch(payload)
    payload = fixture()
    payload["usage_note"] = "A real retailer's sales"
    with pytest.raises(ValueError, match="explicitly labeled synthetic"):
        backtest.backtest_batch(payload)


@pytest.mark.parametrize("limit", [True, 0, 1, 101, 2.4, "7"])
def test_invalid_holdout_limits_fail_before_evaluation(limit):
    with pytest.raises(ValueError, match="holdout_days"):
        backtest.backtest_batch(fixture(), holdout_days=limit)


def test_not_enough_training_days_abstains():
    payload = fixture()
    payload["records"] = payload["records"][:20]
    payload["cutoff_date"] = payload["records"][-1]["date"]
    with pytest.raises(ValueError, match="not enough history"):
        backtest.backtest_batch(payload)


def test_zero_denominator_wape_is_null_not_zero_percent():
    payload = fixture()
    for record in payload["records"]:
        record["units"] = 0
    report = backtest.backtest_batch(payload)
    assert report["lower_mae_on_this_fixture"] == "tie"
    for metric in report["metrics"].values():
        assert metric["mae"] == 0
        assert metric["rmse"] == 0
        assert metric["wape"] is None


def test_score_requires_aligned_predictions():
    with pytest.raises(ValueError, match="align"):
        backtest._score([1.0, 2.0], [1])
