"""Local staged snapshot flow: no external source or authorized ingestion."""
from hashlib import sha256
from pathlib import Path

from mirrormind.modules.evidence.snapshots import available_as_of, stage_csv_snapshot

ROOT = Path(__file__).resolve().parents[2]


def test_local_example_receipt_and_historical_view_remain_unverified():
    data = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    expected_digest = sha256(data).hexdigest()
    staged = stage_csv_snapshot(data, expected_sha256=expected_digest)
    assert staged.receipt() == {
        "status": "local_structure_checked_not_authorized",
        "sha256": expected_digest,
        "record_count": 4,
        "series_count": 2,
    }
    earlier = available_as_of(staged, series_id="item-A", origin_on="2025-01-03")
    assert [row.units for row in earlier] == [2, 0]
    assert [row.units for row in available_as_of(
        staged, series_id="item-A", origin_on="2025-01-05"
    )] == [2, 4, 0]
    # The raw local fixture is never presented in an API response by this module.


def test_bounded_file_stream_stages_exactly_same_invented_fixture():
    from mirrormind.modules.evidence.snapshots import read_staged_csv

    path = ROOT / "examples/staged-daily-observations.csv"
    expected = sha256(path.read_bytes()).hexdigest()
    with path.open("rb") as stream:
        snap = read_staged_csv(stream, expected_sha256=expected)
    assert snap.sha256_hex == expected
    assert snap.receipt()["status"] == "local_structure_checked_not_authorized"
    assert snap.receipt()["record_count"] == 4
    assert [row.units for row in available_as_of(
        snap, series_id="item-A", origin_on="2025-01-03"
    )] == [2, 0]


def test_quality_summary_from_bounded_file_reader_remains_non_authorizing():
    from mirrormind.modules.evidence.snapshots import (
        read_staged_csv,
        snapshot_quality_summary,
    )

    path = ROOT / "examples/staged-daily-observations.csv"
    expected = sha256(path.read_bytes()).hexdigest()
    with path.open("rb") as file:
        snapshot = read_staged_csv(file, expected_sha256=expected)
    summary = snapshot_quality_summary(snapshot)
    assert summary["status"] == "local_quality_summary_not_authorized"
    assert summary["record_count"] == 4
    assert summary["calendar_gap_days"] == 0
    assert summary["late_published_rows"] == 1
    assert summary["explicit_zero_unit_rows"] == 1
    assert "observations" not in summary
