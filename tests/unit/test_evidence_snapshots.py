"""Staged local observations: structural and publication tests, not source rights."""
from dataclasses import FrozenInstanceError
from hashlib import sha256

import pytest

from mirrormind.modules.evidence.snapshots import (
    MAX_BYTES,
    available_as_of,
    stage_csv_snapshot,
)

HEADER = b"series_id,observed_on,available_on,units\n"
ROWS = (
    b"item-A,2025-01-01,2025-01-01,2\n"
    b"item-A,2025-01-02,2025-01-05,4\n"
    b"item-A,2025-01-03,2025-01-03,0\n"
    b"item-B,2025-01-02,2025-01-02,9\n"
)


def stage(raw=HEADER + ROWS, **kwargs):
    return stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest(), **kwargs)


def test_snapshot_content_hash_and_receipt_are_immutable_and_unverified():
    snap = stage()
    assert snap.receipt() == {
        "status": "local_structure_checked_not_authorized",
        "sha256": sha256(HEADER + ROWS).hexdigest(),
        "record_count": 4,
        "series_count": 2,
    }
    assert len(snap.observations) == 4
    with pytest.raises(FrozenInstanceError):
        snap.sha256_hex = "fake"


def test_asof_excludes_late_publication_but_keeps_real_zero():
    snap = stage()
    rows = available_as_of(snap, series_id="item-A", origin_on="2025-01-03")
    assert [(r.observed_on.isoformat(), r.units) for r in rows] == [
        ("2025-01-01", 2), ("2025-01-03", 0)
    ]
    later = available_as_of(snap, series_id="item-A", origin_on="2025-01-05")
    assert [r.units for r in later] == [2, 4, 0]
    assert available_as_of(snap, series_id="item-A", origin_on="2024-12-30") == ()
    assert [r.units for r in available_as_of(snap, series_id="item-B", origin_on="2025-01-03")] == [9]


def test_digest_mismatch_fails_before_interpreting_unverified_bytes():
    with pytest.raises(ValueError, match="do not match"):
        stage_csv_snapshot(HEADER + ROWS, expected_sha256="0" * 64)
    with pytest.raises(ValueError, match="expected SHA-256"):
        stage_csv_snapshot(HEADER + ROWS, expected_sha256="FAKE")


@pytest.mark.parametrize("bad", [b"", b"x" * (MAX_BYTES + 1), "not bytes", bytearray(HEADER)])
def test_unbounded_or_nonbytes_snapshot_rejected(bad):
    with pytest.raises(ValueError, match="bounded and nonempty"):
        stage_csv_snapshot(bad, expected_sha256="0" * 64)


@pytest.mark.parametrize("bad", [0, True, -1, 10001, 2.5])
def test_row_limit_must_be_exact_and_bounded(bad):
    with pytest.raises(ValueError, match="max_rows"):
        stage(HEADER + ROWS, max_rows=bad)


def test_row_limit_checks_before_appending_more_records():
    with pytest.raises(ValueError, match="row count"):
        stage(HEADER + ROWS, max_rows=3)


@pytest.mark.parametrize("bad", [
    HEADER + b"item-A,2025-01-02,2025-01-02,2\nitem-A,2025-01-02,2025-01-03,3\n",
    HEADER + b"item-A,2025-02-30,2025-03-01,1\n",
    HEADER + b"item-A,2025-01-02,2025-01-01,1\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,-1\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,True\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,1.5\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,01\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,1000000001\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,1,secret\n",
    HEADER + b"item-A,2025-01-02,2025-01-02,1\n\n",
    HEADER + b"=IMPORT,2025-01-02,2025-01-02,1\n",
    b"series_id,observed_on,observed_on,units\nitem-A,2025-01-01,2025-01-01,1\n",
    b"series_id,observed_on,available_on,units,pii\nitem-A,2025-01-01,2025-01-01,1,abc\n",
    b"series_id,observed_on,available_on,units\n",
    HEADER + b"\xff\n",
    HEADER + b"item-A,2025-01-01,2025-01-01,1\x00\n",
])
def test_malformed_or_ambiguous_csv_data_fails_closed(bad):
    with pytest.raises(ValueError):
        stage(bad)


def test_canonical_digest_covers_byte_order_but_staging_sorts_rows():
    reordered = HEADER + b"item-B,2025-01-02,2025-01-02,9\n" + ROWS[:len(ROWS)-len(b"item-B,2025-01-02,2025-01-02,9\n")]
    first = stage()
    second = stage(reordered)
    assert first.observations == second.observations
    assert first.sha256_hex != second.sha256_hex


def test_unknown_series_and_invalid_date_abstain_without_fabrication():
    snap = stage()
    with pytest.raises(ValueError, match="unknown series"):
        available_as_of(snap, series_id="missing", origin_on="2025-01-03")
    with pytest.raises(ValueError, match="calendar date"):
        available_as_of(snap, series_id="item-A", origin_on="2025-02-31")
    with pytest.raises(ValueError, match="expected a staged"):
        available_as_of(None, series_id="item-A", origin_on="2025-01-03")
