"""Bounded synthetic daily-observation preflight; never accesses external data.

This is a teaching fixture for future evidence/forecast development, not
source authorization, customer ingestion, forecasting or simulation.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re

SCHEMA = "mirrormind.synthetic_observations.v1"
MAX_INPUT_BYTES = 1_048_576
MAX_RECORDS = 10_000
MAX_DAILY_COUNT = 1_000_000_000


def _day(value: object, field: str) -> date:
    if type(value) is not str or re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is None:
        raise ValueError(f"{field} must be a calendar date in YYYY-MM-DD format")
    try:
        result = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid calendar date") from exc
    if result.isoformat() != value:
        raise ValueError(f"{field} must be canonical YYYY-MM-DD")
    return result


def _nonempty(value: object, field: str) -> str:
    if type(value) is not str or not 1 <= len(value.strip()) <= 128:
        raise ValueError(f"{field} must be 1..128 nonblank characters")
    return value


def _no_duplicate_keys(items: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in items:
        if key in output:
            raise ValueError("duplicate JSON object key")
        output[key] = value
    return output


def validate_batch(payload: object, *, max_records: int = MAX_RECORDS) -> dict[str, object]:
    """Validate structure/cutoff without imputing or authenticating observations."""
    if type(max_records) is not int or not 1 <= max_records <= MAX_RECORDS:
        raise ValueError("max_records must be an exact integer in 1..10000")
    if type(payload) is not dict or set(payload) != {
        "schema_version", "series_id", "source_id", "snapshot_id",
        "usage_note", "cutoff_date", "records",
    }:
        raise ValueError("unexpected or missing synthetic observation fields")
    if payload["schema_version"] != SCHEMA:
        raise ValueError("unsupported synthetic observation schema")
    series_id = _nonempty(payload["series_id"], "series_id")
    _nonempty(payload["source_id"], "source_id")
    _nonempty(payload["snapshot_id"], "snapshot_id")
    _nonempty(payload["usage_note"], "usage_note")
    cutoff = _day(payload["cutoff_date"], "cutoff_date")
    rows = payload["records"]
    if type(rows) is not list or not 1 <= len(rows) <= max_records:
        raise ValueError("records must be a bounded nonempty array")
    values: list[tuple[date, int]] = []
    seen: set[date] = set()
    for index, row in enumerate(rows):
        if type(row) is not dict or set(row) != {"date", "units"}:
            raise ValueError(f"record {index}: expected date and units only")
        day = _day(row["date"], f"record {index} date")
        units = row["units"]
        if type(units) is not int or not 0 <= units <= MAX_DAILY_COUNT:
            raise ValueError(f"record {index}: units must be an exact bounded nonnegative integer")
        if day > cutoff:
            raise ValueError(f"record {index}: date exceeds declared cutoff")
        if day in seen:
            raise ValueError(f"record {index}: duplicate observation date")
        seen.add(day)
        values.append((day, units))
    values.sort(key=lambda item: item[0])
    first, last = values[0][0], values[-1][0]
    missing_days = (last - first).days + 1 - len(values)
    return {
        "status": "synthetic_structure_validated_not_forecast",
        "series_id": series_id,
        "source_status": "synthetic_unverified",
        "cutoff_date": cutoff.isoformat(),
        "first_date": first.isoformat(),
        "last_date": last.isoformat(),
        "record_count": len(values),
        "missing_day_count": missing_days,
        "total_observed_units": sum(units for _, units in values),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight synthetic daily observations")
    parser.add_argument("configuration", type=Path)
    args = parser.parse_args()
    try:
        with args.configuration.open("rb") as source:
            content = source.read(MAX_INPUT_BYTES + 1)
        if len(content) > MAX_INPUT_BYTES:
            raise ValueError("input bytes exceed synthetic fixture limit")
        payload = json.loads(content, object_pairs_hook=_no_duplicate_keys)
        summary = validate_batch(payload)
    except (OSError, UnicodeError, ValueError, TypeError):
        # Do not echo filenames, raw inputs, credentials or private records.
        parser.exit(2, "Invalid synthetic observation fixture.\n")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
