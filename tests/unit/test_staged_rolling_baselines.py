"""Offline staged baseline arithmetic, still on an unverified fixture."""
from hashlib import sha256
from math import sqrt
from pathlib import Path

import pytest

from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.forecasting.baselines import (
    _predict,
    _score,
    backtest_staged_snapshot,
)

ROOT = Path(__file__).resolve().parents[2]


def staged():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    return stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())


def test_staged_rolling_baselines_score_four_of_seven_after_late_publication():
    result = backtest_staged_snapshot(staged(), series_id="item-A", evaluation_on="2025-02-04")
    assert result["status"] == "staged_asof_backtest_unverified"
    assert result["source_status"] == "not_authorized_or_authenticated"
    assert result["requested_origins"] == 7
    assert result["scored_origins"] == 4
    assert result["abstained_missing_history"] == 3
    assert result["abstained_target_unavailable"] == 0
    assert result["holdout_first_date"] == "2025-01-29"
    assert result["metrics"]["seasonal_naive_lag7"] == {
        "mae": 0.0, "rmse": 0.0, "bias": 0.0, "wape": 0.0
    }
    mean = result["metrics"]["trailing_mean_lag7"]
    assert mean["mae"] == pytest.approx(3)
    assert mean["rmse"] == pytest.approx(sqrt(14))
    assert mean["bias"] == pytest.approx(-3)
    assert mean["wape"] == pytest.approx(3 / 11)


def test_all_forecast_inputs_precede_origin_and_have_available_seven_day_window(monkeypatch):
    import mirrormind.modules.forecasting.baselines as mod

    observed_inputs = []
    original_predict = mod._predict

    def capture(data):
        observed_inputs.append(data)
        return original_predict(data)

    monkeypatch.setattr(mod, "_predict", capture)
    backtest_staged_snapshot(staged(), series_id="item-A", evaluation_on="2025-02-04")
    assert len(observed_inputs) == 4
    assert observed_inputs[0] == (8, 10, 12, 14, 2, 4, 6)
    assert observed_inputs[-1] == (14, 2, 4, 6, 8, 10, 12)


def test_declared_earlier_publication_recovers_seven_scored_origins():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    changed = raw.replace(b"2025-01-27,2025-01-31,12", b"2025-01-27,2025-01-27,12")
    snap = stage_csv_snapshot(changed, expected_sha256=sha256(changed).hexdigest())
    report = backtest_staged_snapshot(snap, series_id="item-A", evaluation_on="2025-02-04")
    assert report["scored_origins"] == 7
    assert report["abstained_missing_history"] == 0


def test_unpublished_evaluation_target_is_not_scored_and_reports_coverage():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    altered = raw.replace(b"2025-02-04,2025-02-04,14", b"2025-02-04,2025-02-05,14")
    snap = stage_csv_snapshot(altered, expected_sha256=sha256(altered).hexdigest())
    result = backtest_staged_snapshot(snap, series_id="item-A", evaluation_on="2025-02-04")
    assert result["scored_origins"] == 3
    assert result["abstained_missing_history"] == 3
    assert result["abstained_target_unavailable"] == 1


def test_all_origins_can_abstain_with_null_metrics_not_fake_winner():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    altered = raw.replace(b"2025-01-27,2025-01-31,12", b"2025-01-27,2025-03-01,12")
    altered = altered.replace(b"2025-01-28,2025-01-28,14", b"2025-01-28,2025-03-01,14")
    snap = stage_csv_snapshot(altered, expected_sha256=sha256(altered).hexdigest())
    result = backtest_staged_snapshot(snap, series_id="item-A", evaluation_on="2025-02-04")
    assert result["scored_origins"] == 0
    assert result["abstained_missing_history"] == 7
    assert result["metrics"] is None
    assert result["lower_mae_on_scored_origins_only"] is None


def test_zero_denominator_wape_is_null_for_scored_zero_targets():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    parts = raw.decode().splitlines()
    updated = [parts[0]] + [part.rsplit(",", 1)[0] + ",0" for part in parts[1:]]
    clean = ("\n".join(updated) + "\n").encode()
    snap = stage_csv_snapshot(clean, expected_sha256=sha256(clean).hexdigest())
    result = backtest_staged_snapshot(snap, series_id="item-A", evaluation_on="2025-02-04")
    assert result["scored_origins"] == 4
    assert result["lower_mae_on_scored_origins_only"] == "tie"
    assert all(m["wape"] is None for m in result["metrics"].values())


@pytest.mark.parametrize("invalid", [True, -1, 0, 101, 3.14, "7"])
def test_bad_holdout_size_rejected(invalid):
    with pytest.raises(ValueError, match="holdout_days"):
        backtest_staged_snapshot(
            staged(), series_id="item-A", evaluation_on="2025-02-04", holdout_days=invalid
        )


def test_bad_evaluation_calendar_and_unknown_series_fail_closed():
    with pytest.raises(ValueError, match="calendar date"):
        backtest_staged_snapshot(staged(), series_id="item-A", evaluation_on="2025-02-31")
    with pytest.raises(ValueError, match="unknown or empty"):
        backtest_staged_snapshot(staged(), series_id="missing", evaluation_on="2025-02-04")


def test_short_history_does_not_implicitly_train_on_holdout():
    with pytest.raises(ValueError, match="insufficient observed event-day history"):
        backtest_staged_snapshot(
            staged(), series_id="item-A", evaluation_on="2025-01-15", holdout_days=7
        )


def test_score_refuses_misalignment_and_prediction_refuses_missing_history():
    with pytest.raises(ValueError, match="aligned"):
        _score((1.0,), (1, 2))
    with pytest.raises(ValueError, match="seven exact"):
        _predict((2, 4, 6))


def test_every_requested_origin_has_one_reproducible_nonvalue_audit_record():
    result = backtest_staged_snapshot(
        staged(), series_id="item-A", evaluation_on="2025-02-04"
    )
    rows = result["origin_audit"]
    assert rows == [
        {
            "target_on": f"2025-01-{day:02d}",
            "origin_on": f"2025-01-{day - 1:02d}",
            "status": "required_history_unavailable",
        }
        for day in (29, 30, 31)
    ] + [
        {
            "target_on": f"2025-02-{day:02d}",
            "origin_on": (
                "2025-01-31" if day == 1 else f"2025-02-{day - 1:02d}"
            ),
            "status": "scored",
        }
        for day in (1, 2, 3, 4)
    ]
    assert len(rows) == result["requested_origins"]
    assert result["scored_origins"] == sum(x["status"] == "scored" for x in rows)
    assert result["abstained_target_missing"] == 0
    assert result["abstained_target_not_published"] == 0
    assert all(set(x) == {"target_on", "origin_on", "status"} for x in rows)
    assert result == backtest_staged_snapshot(
        staged(), series_id="item-A", evaluation_on="2025-02-04"
    )


def test_missing_target_is_not_conflated_with_unpublished_target():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    line = next(
        row for row in raw.splitlines(keepends=True)
        if row.startswith(b"item-A,2025-02-04,2025-02-04,14")
    )
    assert line in raw
    missing = raw.replace(line, b"")
    staged_missing = stage_csv_snapshot(
        missing, expected_sha256=sha256(missing).hexdigest()
    )
    report = backtest_staged_snapshot(
        staged_missing, series_id="item-A", evaluation_on="2025-02-04"
    )
    assert report["abstained_target_missing"] == 1
    assert report["abstained_target_not_published"] == 0
    assert report["origin_audit"][-1]["status"] == "target_missing"
    assert report["scored_origins"] == 3

    delayed = raw.replace(
        line, line.replace(b"2025-02-04,2025-02-04,14", b"2025-02-04,2025-02-05,14")
    )
    staged_late = stage_csv_snapshot(
        delayed, expected_sha256=sha256(delayed).hexdigest()
    )
    report = backtest_staged_snapshot(
        staged_late, series_id="item-A", evaluation_on="2025-02-04"
    )
    assert report["abstained_target_missing"] == 0
    assert report["abstained_target_not_published"] == 1
    assert report["origin_audit"][-1]["status"] == "target_not_published_by_cutoff"
    assert report["scored_origins"] == 3


def test_all_abstained_audit_has_no_fabricated_scores():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    altered = raw.replace(b"2025-01-27,2025-01-31,12", b"2025-01-27,2025-03-01,12")
    altered = altered.replace(b"2025-01-28,2025-01-28,14", b"2025-01-28,2025-03-01,14")
    snap = stage_csv_snapshot(altered, expected_sha256=sha256(altered).hexdigest())
    report = backtest_staged_snapshot(
        snap, series_id="item-A", evaluation_on="2025-02-04"
    )
    assert len(report["origin_audit"]) == 7
    assert {row["status"] for row in report["origin_audit"]} == {
        "required_history_unavailable"
    }
    assert report["scored_origins"] == 0
    assert report["metrics"] is None
    assert report["lower_mae_on_scored_origins_only"] is None


def test_min_history_counts_observations_not_one_ancient_row():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    lines = raw.splitlines(keepends=True)
    # 1 ancient row + the last 14 event days: only 8 preceding Jan 29,
    # despite the earliest date being almost a month before the holdout.
    reduced = b"".join(lines[:2] + lines[-14:])
    snapshot = stage_csv_snapshot(
        reduced, expected_sha256=sha256(reduced).hexdigest()
    )
    with pytest.raises(ValueError, match="insufficient observed event-day history"):
        backtest_staged_snapshot(
            snapshot, series_id="item-A", evaluation_on="2025-02-04"
        )
    allowed = backtest_staged_snapshot(
        snapshot, series_id="item-A", evaluation_on="2025-02-04",
        min_history_days=7,
    )
    assert allowed["requested_origins"] == 7
    assert allowed["scored_origins"] == 4
    assert allowed["abstained_missing_history"] == 3


def test_earliest_supported_calendar_cutoff_fails_cleanly_not_overflow():
    raw = (
        b"series_id,observed_on,available_on,units\n"
        b"item-A,0001-01-01,0001-01-01,1\n"
    )
    snapshot = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
    with pytest.raises(ValueError, match="evaluation window predates"):
        backtest_staged_snapshot(
            snapshot, series_id="item-A", evaluation_on="0001-01-03",
            holdout_days=7, min_history_days=7,
        )


def test_custom_history_minimum_is_an_observation_count():
    snap = staged()
    with pytest.raises(ValueError, match="insufficient observed event-day history"):
        backtest_staged_snapshot(
            snap, series_id="item-A", evaluation_on="2025-02-04",
            min_history_days=29,
        )
    report = backtest_staged_snapshot(
        snap, series_id="item-A", evaluation_on="2025-02-04",
        min_history_days=28,
    )
    assert report["scored_origins"] == 4
