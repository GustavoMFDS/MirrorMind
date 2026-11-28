"""Pure local schedule binding; no trusted registration or source authority."""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from datetime import date
from itertools import pairwise
from typing import Literal

from mirrormind.domains.retail.census_evaluation import (
    CENSUS_HORIZONS_MONTHS,
    MAX_CENSUS_EVALUATION_ORIGINS,
    CensusForecastOrigin,
    evaluate_census_vintage_descriptive,
)
from mirrormind.domains.retail.census_vintages import (
    CensusVintageRecord,
    select_census_vintage_as_of,
)

_SCHEMA = "mirrormind.census.origin_schedule.v1"
_SERIES = re.compile(r"[A-Z0-9][A-Z0-9._-]{0,63}")
_SHA = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class CensusOriginSchedule:
    """Caller-declared schedule, not a signed registration."""

    series_id: str
    origins: tuple[CensusForecastOrigin, ...]


def _ordinal(value: date) -> int:
    return value.year * 12 + value.month - 1


def _partition(
    plan: CensusOriginSchedule,
) -> tuple[tuple[CensusForecastOrigin, ...], ...]:
    if type(plan) is not CensusOriginSchedule:
        raise ValueError("exact origin schedule required")
    if type(plan.series_id) is not str or not _SERIES.fullmatch(plan.series_id):
        raise ValueError("invalid series")
    if type(plan.origins) is not tuple or not 10 <= len(plan.origins) <= MAX_CENSUS_EVALUATION_ORIGINS:
        raise ValueError("schedule requires 10 to 250 declared origins")
    prev = None
    for origin in plan.origins:
        if (
            type(origin) is not CensusForecastOrigin
            or type(origin.reference_month) is not date
            or origin.reference_month.day != 1
            or type(origin.issued_on) is not date
            or _ordinal(origin.issued_on) <= _ordinal(origin.reference_month)
        ):
            raise ValueError("invalid monthly origin or issue boundary")
        if prev is not None and (
            origin.reference_month <= prev.reference_month
            or origin.issued_on <= prev.issued_on
        ):
            raise ValueError("origins and issue dates must be strictly increasing")
        prev = origin
    n = len(plan.origins)
    a, b = 3 * n // 5, 4 * n // 5
    parts = (plan.origins[:a], plan.origins[a:b], plan.origins[b:])
    for earlier, later in pairwise(parts):
        if _ordinal(earlier[-1].reference_month) + max(CENSUS_HORIZONS_MONTHS) >= _ordinal(later[0].reference_month):
            raise ValueError("cross-split target reach overlaps next origin")
    return parts


def census_schedule_sha256(plan: CensusOriginSchedule) -> str:
    """Fingerprint validated schedule and fixed partition policy."""
    parts = _partition(plan)
    payload = {
        "schema": _SCHEMA,
        "series_id": plan.series_id,
        "partition": "floor_cumulative_60_80_percent",
        "horizons": CENSUS_HORIZONS_MONTHS,
        "splits": [
            [[o.reference_month.isoformat(), o.issued_on.isoformat()] for o in part]
            for part in parts
        ],
    }
    return hashlib.sha256(json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")).hexdigest()


def evaluate_frozen_census_split(
    records: tuple[CensusVintageRecord, ...],
    *,
    plan: CensusOriginSchedule,
    expected_schedule_sha256: str,
    split: Literal["validation", "holdout"],
) -> dict[str, object]:
    """Compare a caller-retained schedule digest before fictional scoring."""
    actual = census_schedule_sha256(plan)
    if (
        type(expected_schedule_sha256) is not str
        or not _SHA.fullmatch(expected_schedule_sha256)
        or not hmac.compare_digest(actual, expected_schedule_sha256)
    ):
        raise ValueError("schedule fingerprint mismatch")
    if type(split) is not str or split not in ("validation", "holdout"):
        raise ValueError("invalid evaluation split")
    parts = _partition(plan)
    # Validate normalized records using existing selector, not a new parser.
    select_census_vintage_as_of(
        records, series_id=plan.series_id, target_release_on=plan.origins[0].issued_on
    )
    labels: dict[int, CensusVintageRecord] = {}
    for record in records:
        if record.release_kind == "first_estimate":
            key = _ordinal(record.reference_month)
            if key in labels:
                raise ValueError("each month must have one unique first-estimate label")
            labels[key] = record
    for earlier, later in pairwise(parts):
        for origin in earlier:
            for horizon in CENSUS_HORIZONS_MONTHS:
                label = labels.get(_ordinal(origin.reference_month) + horizon)
                if label is None or label.published_on >= later[0].issued_on:
                    raise ValueError("cross-split target publication is not strictly prior")
    evaluation = evaluate_census_vintage_descriptive(
        records, series_id=plan.series_id, origins=parts[1 if split == "validation" else 2],
        split=split,
    )
    result: dict[str, object] = {
        "schema_version": "mirrormind.census.frozen_split.v1",
        "schedule_sha256": actual,
        "schedule_digest_matched": True,
        "cross_split_target_boundary_checked": True,
        "split_sizes": tuple(map(len, parts)),
        "registration_verified": False,
        "holdout_lock_verified": False,
        "inference_status": "abstained",
        "action_authorized": False,
        "evaluation": evaluation,
    }
    result["receipt_sha256"] = hashlib.sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")).hexdigest()
    return result
