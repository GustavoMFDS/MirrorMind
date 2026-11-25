"""Pure, bounded selection over normalized aggregate release-vintage records.

This module performs no I/O and does not verify source bytes or permission.
Tests and examples must use generated records until B-01/B-02 are resolved.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal

VINTAGE_VIEW_SCHEMA = "mirrormind.census.aggregate_vintage_view.v1"
MAX_VINTAGE_RECORDS = 50_000
_RELEASE_KINDS = frozenset({"first_estimate", "monthly_revision", "annual_revision"})
_SERIES_ID = re.compile(r"[A-Z0-9][A-Z0-9._-]{0,63}")
_RELEASE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,95}")
_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class CensusVintageRecord:
    """One normalized aggregate value from one immutable release artifact."""

    series_id: str
    reference_month: date
    value: Decimal
    published_on: date
    release_kind: Literal["first_estimate", "monthly_revision", "annual_revision"]
    release_id: str
    snapshot_sha256: str


@dataclass(frozen=True, slots=True)
class CensusVintageView:
    """Selected values available before a target release date, not source proof."""

    series_id: str
    target_release_on: date
    records: tuple[CensusVintageRecord, ...]

    def receipt(self) -> dict[str, object]:
        """Return sanitized selection provenance without value-level observations."""
        return {
            "schema_version": VINTAGE_VIEW_SCHEMA,
            "status": (
                "aggregate_vintage_selection_unverified"
                if self.records else "aggregate_vintage_selection_abstained"
            ),
            "source_status": "caller_supplied_not_source_verified",
            "series_id": self.series_id,
            "publication_cutoff": self.target_release_on.isoformat(),
            "cutoff_rule": "published_on_strictly_before_target_release_date",
            "timestamp_precision": "date_only_no_intraday_ordering",
            "selected_observation_count": len(self.records),
            "selected_release_ids": tuple(sorted({item.release_id for item in self.records})),
            "selected_snapshot_sha256s": tuple(sorted({
                item.snapshot_sha256 for item in self.records
            })),
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _validate_record(record: CensusVintageRecord, *, series_id: str) -> None:
    """Reject malformed normalized metadata before applying time selection."""
    if type(record) is not CensusVintageRecord:
        raise ValueError("records must contain exact CensusVintageRecord values")
    if type(record.series_id) is not str or not _SERIES_ID.fullmatch(record.series_id):
        raise ValueError("series_id is malformed")
    if record.series_id != series_id:
        raise ValueError("records must belong to the selected series")
    if type(record.reference_month) is not date or record.reference_month.day != 1:
        raise ValueError("reference_month must be the first day of a calendar month")
    if type(record.published_on) is not date:
        raise ValueError("published_on must be an exact calendar date")
    if type(record.value) is not Decimal or not record.value.is_finite() or record.value < 0:
        raise ValueError("value must be a finite non-negative Decimal")
    if type(record.release_kind) is not str or record.release_kind not in _RELEASE_KINDS:
        raise ValueError("unsupported release_kind")
    if type(record.release_id) is not str or not _RELEASE_ID.fullmatch(record.release_id):
        raise ValueError("release_id is malformed")
    if type(record.snapshot_sha256) is not str or not _SHA256.fullmatch(
        record.snapshot_sha256
    ):
        raise ValueError("snapshot_sha256 must be lowercase SHA-256")


def select_census_vintage_as_of(
    records: tuple[CensusVintageRecord, ...],
    *,
    series_id: str,
    target_release_on: date,
) -> CensusVintageView:
    """Select latest per-month records published strictly before target release.

    Publication dates are day-granular. A record published on the target
    release date is not considered available, because this contract has no
    trusted intraday ordering. An empty result is a valid abstention and never
    fills missing reference months with zeros.
    """
    if type(series_id) is not str or not _SERIES_ID.fullmatch(series_id):
        raise ValueError("series_id is malformed")
    if type(target_release_on) is not date:
        raise ValueError("target_release_on must be an exact calendar date")
    if type(records) is not tuple or len(records) > MAX_VINTAGE_RECORDS:
        raise ValueError("record limit exceeded or records must be a bounded tuple")

    record_keys: set[tuple[date, date]] = set()
    release_metadata: dict[str, tuple[date, str]] = {}
    latest_by_month: dict[date, CensusVintageRecord] = {}
    for record in records:
        _validate_record(record, series_id=series_id)
        key = (record.reference_month, record.published_on)
        if key in record_keys:
            raise ValueError("ambiguous publication date for reference month")
        record_keys.add(key)

        metadata = (record.published_on, record.snapshot_sha256)
        previous_metadata = release_metadata.setdefault(record.release_id, metadata)
        if previous_metadata != metadata:
            raise ValueError("conflicting release metadata for release_id")

        if record.published_on >= target_release_on:
            continue
        previous = latest_by_month.get(record.reference_month)
        if previous is None or record.published_on > previous.published_on:
            latest_by_month[record.reference_month] = record

    selected = tuple(latest_by_month[month] for month in sorted(latest_by_month))
    return CensusVintageView(
        series_id=series_id,
        target_release_on=target_release_on,
        records=selected,
    )
