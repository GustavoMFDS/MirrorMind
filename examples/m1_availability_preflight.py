"""Synthetic event-time versus availability-time preflight.

Educational local fixture only: declared publication dates are NOT
authenticated, and this is not licensed data ingestion or prediction.
Run: python -m examples.m1_availability_preflight examples/synthetic-asof-sales.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from examples.m1_observation_preflight import (
    MAX_DAILY_COUNT,
    MAX_INPUT_BYTES,
    MAX_RECORDS,
    _day,
    _no_duplicate_keys,
    _nonempty,
)

SCHEMA = "mirrormind.synthetic_availability.v1"


def asof_batch(payload: object) -> dict[str, object]:
    """Summarize only observations whose event and publication times precede cutoff.

    Reject malformed inputs; do not fill gaps, authenticate labels or
    leak raw withheld records into the returned aggregate.
    """
    if type(payload) is not dict or set(payload) != {
        "schema_version", "series_id", "source_id", "snapshot_id",
        "usage_note", "as_of_date", "records",
    }:
        raise ValueError("invalid synthetic availability envelope")
    if payload["schema_version"] != SCHEMA:
        raise ValueError("unsupported synthetic availability schema")
    series_id = _nonempty(payload["series_id"], "series_id")
    source_id = _nonempty(payload["source_id"], "source_id")
    _nonempty(payload["snapshot_id"], "snapshot_id")
    note = _nonempty(payload["usage_note"], "usage_note")
    if source_id != "synthetic-fixture-generator" or not note.startswith("Generated teaching data"):
        raise ValueError("only explicitly labeled synthetic teaching fixtures supported")
    cutoff = _day(payload["as_of_date"], "as_of_date")
    records = payload["records"]
    if type(records) is not list or not 1 <= len(records) <= MAX_RECORDS:
        raise ValueError("records must be bounded nonempty list")
    seen: set[object] = set()
    eligible: list[tuple[object, int]] = []
    delayed, future = 0, 0
    for i, row in enumerate(records):
        if type(row) is not dict or set(row) != {"observed_on", "available_on", "units"}:
            raise ValueError(f"record {i}: invalid fields")
        observed = _day(row["observed_on"], f"record {i} observed_on")
        available = _day(row["available_on"], f"record {i} available_on")
        count = row["units"]
        if type(count) is not int or not 0 <= count <= MAX_DAILY_COUNT:
            raise ValueError(f"record {i}: units must be an exact bounded nonnegative integer")
        if available < observed:
            raise ValueError(f"record {i}: publication precedes observation")
        if observed in seen:
            raise ValueError(f"record {i}: duplicate observed date")
        seen.add(observed)
        if observed > cutoff:
            future += 1
        elif available > cutoff:
            delayed += 1
        else:
            eligible.append((observed, count))
    if not eligible:
        raise ValueError("no eligible observations as of cutoff")
    eligible.sort(key=lambda value: value[0])
    first, last = eligible[0][0], eligible[-1][0]
    return {
        "schema_version": SCHEMA,
        "status": "synthetic_availability_filtered_not_verified_evidence",
        "source_status": "synthetic_unverified",
        "series_id": series_id,
        "as_of_date": cutoff.isoformat(),
        "eligible_count": len(eligible),
        "excluded_future_event_count": future,
        "excluded_late_available_count": delayed,
        "gaps_within_eligible_span": (last - first).days + 1 - len(eligible),
        "first_eligible_date": first.isoformat(),
        "last_eligible_date": last.isoformat(),
        "eligible_observed_units": sum(count for _, count in eligible),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic publication-time cutoff exercise")
    parser.add_argument("configuration", type=Path)
    args = parser.parse_args()
    try:
        with args.configuration.open("rb") as file:
            data = file.read(MAX_INPUT_BYTES + 1)
        if len(data) > MAX_INPUT_BYTES:
            raise ValueError("fixture exceeds byte cap")
        payload = json.loads(data, object_pairs_hook=_no_duplicate_keys)
        report = asof_batch(payload)
    except (OSError, UnicodeError, ValueError, TypeError):
        parser.exit(2, "Invalid synthetic availability fixture.\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
