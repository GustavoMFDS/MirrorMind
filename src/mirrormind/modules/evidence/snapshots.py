"""Strict, bounded local CSV preflight for dated observations.

A byte digest proves only equality with the declared bytes, never the
publisher's identity, access rights, provenance, or data quality.
This module performs no I/O, persistence, network access or AI inference.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from hmac import compare_digest
from io import StringIO
from typing import BinaryIO

MAX_BYTES = 1_048_576
MAX_ROWS = 10_000
MAX_UNITS = 1_000_000_000
COLUMNS = ("series_id", "observed_on", "available_on", "units")


@dataclass(frozen=True, slots=True)
class Observation:
    """One structurally checked row; its publisher and meaning remain unverified."""

    series_id: str
    observed_on: date
    available_on: date
    units: int


@dataclass(frozen=True, slots=True)
class StagedSnapshot:
    """In-memory immutable receipt with observations, NOT an authorized dataset."""

    sha256_hex: str
    observations: tuple[Observation, ...]

    def receipt(self) -> dict[str, str | int]:
        """Report structure and digest only, without returning raw observations."""
        return {
            "status": "local_structure_checked_not_authorized",
            "sha256": self.sha256_hex,
            "record_count": len(self.observations),
            "series_count": len({row.series_id for row in self.observations}),
        }


def _day(text: str) -> date:
    """Accept only canonical ISO calendar dates, never ambiguous local timestamps."""
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
        raise ValueError("invalid calendar date format")
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError("invalid calendar date value") from exc
    if parsed.isoformat() != text:
        raise ValueError("noncanonical calendar date")
    return parsed


def stage_csv_snapshot(
    data: bytes, *, expected_sha256: str, max_rows: int = MAX_ROWS
) -> StagedSnapshot:
    """Verify declared bytes, then reject malformed/ambiguous daily CSV rows.

    Caller must independently verify legal rights and original provenance
    before using any real data. No successful result from this function
    constitutes that authorization; there is no persistence or API route.
    """
    if type(data) is not bytes or not 0 < len(data) <= MAX_BYTES:
        raise ValueError("snapshot bytes must be bounded and nonempty")
    if type(max_rows) is not int or not 1 <= max_rows <= MAX_ROWS:
        raise ValueError("max_rows must be an exact bounded integer")
    if type(expected_sha256) is not str or not re.fullmatch(
        r"[0-9a-f]{64}", expected_sha256
    ):
        raise ValueError("invalid expected SHA-256 encoding")
    digest = sha256(data).hexdigest()
    if not compare_digest(expected_sha256, digest):
        raise ValueError("snapshot bytes do not match declared SHA-256")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("snapshot must be UTF-8") from exc
    if "\x00" in text:
        raise ValueError("snapshot contains forbidden NUL byte")
    if any(not line.strip() for line in text.splitlines()):
        raise ValueError("blank CSV rows are not allowed")
    stream = csv.reader(StringIO(text, newline=""), strict=True)
    try:
        header = next(stream)
        if tuple(header) != COLUMNS:
            raise ValueError("unexpected CSV schema or ambiguous headers")
        staged: list[Observation] = []
        seen: set[tuple[str, date]] = set()
        for fields in stream:
            if len(staged) >= max_rows:
                raise ValueError("snapshot exceeds bounded row count")
            if len(fields) != len(COLUMNS):
                raise ValueError("CSV row has an unexpected field count")
            series_id, observed, available, units = fields
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", series_id):
                raise ValueError("invalid or ambiguous series identifier")
            observed_on = _day(observed)
            available_on = _day(available)
            if available_on < observed_on:
                raise ValueError("publication precedes recorded observation")
            if not re.fullmatch(r"(?:0|[1-9][0-9]{0,9})", units):
                raise ValueError("units must be canonical nonnegative integers")
            count = int(units)
            if count > MAX_UNITS:
                raise ValueError("units exceed declared bound")
            key = (series_id, observed_on)
            if key in seen:
                raise ValueError("duplicate series/observation date")
            seen.add(key)
            staged.append(Observation(series_id, observed_on, available_on, count))
    except (csv.Error, StopIteration) as exc:
        raise ValueError("malformed or empty CSV snapshot") from exc
    if not staged:
        raise ValueError("CSV snapshot must have at least one observation")
    return StagedSnapshot(digest, tuple(sorted(staged, key=lambda r: (r.series_id, r.observed_on))))


def available_as_of(
    snapshot: StagedSnapshot, *, series_id: str, origin_on: str
) -> tuple[Observation, ...]:
    """Select only dates and values published by this *historical* origin.

    A missing or not-yet-published row stays absent, not zero-valued.
    This is data selection, not a forecast, rights check or permission gate.
    """
    if type(snapshot) is not StagedSnapshot:
        raise ValueError("expected a staged snapshot")
    if type(series_id) is not str or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", series_id
    ):
        raise ValueError("invalid series identifier")
    origin = _day(origin_on)
    if not any(row.series_id == series_id for row in snapshot.observations):
        raise ValueError("unknown series identifier")
    return tuple(
        row for row in snapshot.observations
        if row.series_id == series_id
        and row.observed_on <= origin
        and row.available_on <= origin
    )


def read_staged_csv(
    stream: BinaryIO, *, expected_sha256: str, max_rows: int = MAX_ROWS
) -> StagedSnapshot:
    """Read a cooperative local binary stream with a strict byte ceiling.

    A trusted caller is responsible for opening and authorizing the
    source. This function never opens paths, fetches remote content,
    stores records or verifies legal permission or producer identity.
    Short reads are not EOF; continue until the stream returns b"".
    """
    if not callable(getattr(stream, "read", None)):
        raise TypeError("expected readable binary snapshot stream")
    chunks: list[bytes] = []
    total = 0
    while total <= MAX_BYTES:
        requested = min(65_536, MAX_BYTES + 1 - total)
        try:
            chunk = stream.read(requested)
        except OSError:
            raise ValueError("failed to read binary snapshot stream") from None
        if type(chunk) is not bytes:
            raise ValueError("snapshot stream must yield exact bytes")
        if len(chunk) > requested:
            raise ValueError("binary stream returned more than requested")
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    if total > MAX_BYTES:
        raise ValueError("snapshot exceeds byte limit")
    return stage_csv_snapshot(
        b"".join(chunks), expected_sha256=expected_sha256, max_rows=max_rows
    )


def snapshot_quality_summary(snapshot: StagedSnapshot) -> dict[str, str | int]:
    """Summarize observed calendar gaps and delays without imputing or authorizing.

    Counts refer to structurally staged rows, not true demand, stockouts,
    source release authenticity or an actual permission/quality certificate.
    """
    if type(snapshot) is not StagedSnapshot:
        raise ValueError("expected structurally staged snapshot")
    if not 1 <= len(snapshot.observations) <= MAX_ROWS:
        raise ValueError("snapshot must have a bounded nonempty row count")
    days_by_series: dict[str, set[date]] = {}
    delayed = 0
    zeros = 0
    all_days: list[date] = []
    for row in snapshot.observations:
        if type(row) is not Observation:
            raise ValueError("invalid staged observation")
        days = days_by_series.setdefault(row.series_id, set())
        if row.observed_on in days:
            raise ValueError("duplicate series/observation date")
        days.add(row.observed_on)
        all_days.append(row.observed_on)
        if row.available_on > row.observed_on:
            delayed += 1
        if row.units == 0:
            zeros += 1
    calendar_gap_days = sum(
        (max(days) - min(days)).days + 1 - len(days)
        for days in days_by_series.values()
    )
    return {
        "status": "local_quality_summary_not_authorized",
        "snapshot_sha256": snapshot.sha256_hex,
        "record_count": len(snapshot.observations),
        "series_count": len(days_by_series),
        "calendar_gap_days": calendar_gap_days,
        "late_published_rows": delayed,
        "explicit_zero_unit_rows": zeros,
        "first_observed_on": min(all_days).isoformat(),
        "last_observed_on": max(all_days).isoformat(),
    }
