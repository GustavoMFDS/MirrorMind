"""End-to-end local package composition without authenticating any source."""
from hashlib import sha256
from pathlib import Path

from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.forecasting.baselines import backtest_staged_snapshot

ROOT = Path(__file__).resolve().parents[2]


def test_staged_csv_to_matched_rolling_backtest_without_runtime_io():
    raw = (ROOT / "examples/staged-weekly-availability.csv").read_bytes()
    snapshot = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
    result = backtest_staged_snapshot(
        snapshot, series_id="item-A", evaluation_on="2025-02-04"
    )
    assert result["snapshot_sha256"] == snapshot.receipt()["sha256"]
    assert result["status"] == "staged_asof_backtest_unverified"
    assert result["scored_origins"] == 4
    assert result["abstained_missing_history"] == 3
    assert result["metrics"]["seasonal_naive_lag7"]["mae"] == 0
    assert "observations" not in result
