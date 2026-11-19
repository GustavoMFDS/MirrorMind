"""Aggregated staged quality metadata is neither a data release nor permission."""
from hashlib import sha256
from pathlib import Path

import pytest

from mirrormind.modules.evidence.snapshots import (
    StagedSnapshot,
    snapshot_quality_summary,
    stage_csv_snapshot,
)

ROOT = Path(__file__).resolve().parents[2]


def _staged(raw: bytes | None = None):
    if raw is None:
        raw = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    return stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())


def test_quality_report_distinguishes_explicit_zero_from_absent_day():
    raw = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    report = snapshot_quality_summary(_staged(raw))
    assert report == {
        "status": "local_quality_summary_not_authorized",
        "snapshot_sha256": sha256(raw).hexdigest(),
        "record_count": 4,
        "series_count": 2,
        "calendar_gap_days": 0,
        "late_published_rows": 1,
        "explicit_zero_unit_rows": 1,
        "first_observed_on": "2025-01-01",
        "last_observed_on": "2025-01-03",
    }
    missing = b"".join(
        line for line in raw.splitlines(keepends=True)
        if not line.startswith(b"item-A,2025-01-02,2025-01-05,4")
    )
    assert missing != raw
    changed = snapshot_quality_summary(_staged(missing))
    assert changed["calendar_gap_days"] == 1
    assert changed["explicit_zero_unit_rows"] == 1
    assert changed["record_count"] == 3
    assert changed["late_published_rows"] == 0
    assert "total_observed_units" not in changed


def test_quality_publication_lag_is_declared_not_source_authenticated():
    raw = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    corrected = raw.replace(
        b"2025-01-02,2025-01-05,4", b"2025-01-02,2025-01-02,4"
    )
    baseline = snapshot_quality_summary(_staged(raw))
    report = snapshot_quality_summary(_staged(corrected))
    assert baseline["late_published_rows"] == 1
    assert report["late_published_rows"] == 0
    assert report["calendar_gap_days"] == baseline["calendar_gap_days"]
    assert report["snapshot_sha256"] != baseline["snapshot_sha256"]


@pytest.mark.parametrize("invalid", [None, object(), StagedSnapshot("x", ())])
def test_quality_requires_nonempty_staged_snapshot(invalid):
    with pytest.raises(ValueError, match="staged snapshot|bounded nonempty"):
        snapshot_quality_summary(invalid)


def test_quality_does_not_echo_series_names_or_raw_count_values():
    report = snapshot_quality_summary(_staged())
    result = str(report)
    assert "item-A" not in result
    assert "item-B" not in result
    assert "customer" not in result.lower()
    assert "total_observed_units" not in report
    assert "source_status" not in report  # Status is explicit in the report instead.
    assert report["status"].endswith("not_authorized")


def test_quality_rejects_directly_constructed_duplicate_staged_rows():
    snapshot = _staged()
    forged = StagedSnapshot(
        snapshot.sha256_hex,
        snapshot.observations + (snapshot.observations[0],),
    )
    with pytest.raises(ValueError, match="duplicate series/observation"):
        snapshot_quality_summary(forged)
