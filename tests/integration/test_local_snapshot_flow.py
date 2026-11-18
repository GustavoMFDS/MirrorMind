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
