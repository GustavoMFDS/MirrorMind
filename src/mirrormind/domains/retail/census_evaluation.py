"""Synthetic-only fixed-baseline evaluation over aggregate release vintages.

The evaluator consumes normalized, caller-supplied records and performs no I/O.
Its fingerprints bind those records for replay; they do not authenticate source
bytes, grant data rights, or establish empirical forecast quality.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from fractions import Fraction
from math import isfinite, ldexp, sqrt
from typing import Literal

from mirrormind.domains.retail.census_vintages import (
    VINTAGE_VIEW_SCHEMA,
    CensusVintageRecord,
    CensusVintageView,
    select_census_vintage_as_of,
)

CENSUS_BACKTEST_SCHEMA = "mirrormind.census.vintage_backtest.v2"
MAX_CENSUS_EVALUATION_ORIGINS = 250
CENSUS_HORIZONS_MONTHS = (1, 3, 6)
_TRAILING_MONTHS = 12
_MAX_DECIMAL_DIGITS = 34
_MIN_DECIMAL_EXPONENT = -433
_MAX_DECIMAL_EXPONENT = 150
_MIN_ADJUSTED_EXPONENT = -400
_MAX_ADJUSTED_EXPONENT = 150
_MAX_METRIC_VALUE = Decimal("1e150")
_BASELINES = ("seasonal_naive_lag12", "trailing_12_month_mean")


@dataclass(frozen=True, slots=True)
class CensusForecastOrigin:
    """One predeclared monthly reference period and date-only issue boundary."""

    reference_month: date
    issued_on: date


def _month_offset(month: date, offset: int) -> date:
    ordinal = month.year * 12 + month.month - 1 + offset
    year, zero_month = divmod(ordinal, 12)
    if not 1 <= year <= 9999:
        raise ValueError("month arithmetic falls outside supported calendar dates")
    return date(year, zero_month + 1, 1)


def _record_payload(record: CensusVintageRecord) -> dict[str, str]:
    return {
        "series_id": record.series_id,
        "reference_month": record.reference_month.isoformat(),
        "value": str(record.value),
        "published_on": record.published_on.isoformat(),
        "release_kind": record.release_kind,
        "release_id": record.release_id,
        "snapshot_sha256": record.snapshot_sha256,
    }


def _manifest_sha256(records: tuple[CensusVintageRecord, ...]) -> str:
    payload = [
        _record_payload(record)
        for record in sorted(
            records,
            key=lambda item: (
                item.reference_month,
                item.published_on,
                item.release_id,
                item.release_kind,
            ),
        )
    ]
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _selection_receipt(
    view: CensusVintageView, manifest_sha256: str
) -> dict[str, object]:
    """Summarize a selected vintage without repeating every release identifier."""
    return {
        "schema_version": VINTAGE_VIEW_SCHEMA,
        "status": (
            "aggregate_vintage_selection_unverified"
            if view.records else "aggregate_vintage_selection_abstained"
        ),
        "source_status": "caller_supplied_not_source_verified",
        "series_id": view.series_id,
        "publication_cutoff": view.target_release_on.isoformat(),
        "cutoff_rule": "published_on_strictly_before_target_release_date",
        "timestamp_precision": "date_only_no_intraday_ordering",
        "selected_observation_count": len(view.records),
        "as_of_vintage_manifest_sha256": manifest_sha256,
        "ingestion_authorized": False,
        "forecast_eligible": False,
    }


def _validate_metric_input(value: Decimal) -> None:
    parts = value.as_tuple()
    if (
        len(parts.digits) > _MAX_DECIMAL_DIGITS
        or not _MIN_DECIMAL_EXPONENT <= parts.exponent <= _MAX_DECIMAL_EXPONENT
        or (
            not value.is_zero()
            and not _MIN_ADJUSTED_EXPONENT <= value.adjusted() <= _MAX_ADJUSTED_EXPONENT
        )
        or value.copy_abs() > _MAX_METRIC_VALUE
    ):
        raise ValueError("aggregate values exceed the supported metric range")


def _metric_float(value: Fraction) -> float:
    if value == 0:
        return 0.0
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError("metric result overflows finite float range") from exc
    if not isfinite(result):
        raise ValueError("metric result overflows finite float range")
    if result == 0.0:
        raise ValueError("metric result underflows finite float range")
    return result


def _sqrt_metric_float(value: Fraction) -> float:
    """Round a non-negative exact mean square without underflowing its root."""
    if value == 0:
        return 0.0
    if value < 0:
        raise ValueError("mean squared error cannot be negative")

    numerator = value.numerator
    denominator = value.denominator
    exponent = numerator.bit_length() - denominator.bit_length()
    if exponent >= 0:
        if numerator < denominator << exponent:
            exponent -= 1
    else:
        if numerator << -exponent < denominator:
            exponent -= 1

    if exponent >= 0:
        scaled = Fraction(numerator, denominator << exponent)
    else:
        scaled = Fraction(numerator << -exponent, denominator)

    if exponent % 2:
        scaled *= 2
        exponent -= 1
    try:
        result = ldexp(sqrt(float(scaled)), exponent // 2)
    except OverflowError as exc:
        raise ValueError("metric result overflows finite float range") from exc
    if not isfinite(result):
        raise ValueError("metric result overflows finite float range")
    if result == 0.0:
        raise ValueError("metric result underflows finite float range")
    return result


def _metrics(
    forecasts: tuple[Fraction, ...], actuals: tuple[Fraction, ...]
) -> dict[str, float | None]:
    if len(actuals) < 2 or len(forecasts) != len(actuals):
        raise ValueError("metrics require at least two paired observations")
    errors = tuple(abs(forecast - actual) for forecast, actual in zip(forecasts, actuals))
    absolute_error = sum(errors, Fraction())
    squared_error_mean = sum(
        (error * error for error in errors), Fraction()
    ) / len(errors)
    observed_total = sum(actuals, Fraction())
    rmse = _sqrt_metric_float(squared_error_mean)
    return {
        "mae": _metric_float(absolute_error / len(errors)),
        "rmse": rmse,
        "wape": (
            None if observed_total == 0 else _metric_float(absolute_error / observed_total)
        ),
    }


def evaluate_census_vintage_backtest(
    records: tuple[CensusVintageRecord, ...],
    *,
    series_id: str,
    origins: tuple[CensusForecastOrigin, ...],
    split: Literal["validation", "holdout"],
) -> dict[str, object]:
    """Evaluate fixed monthly baselines using only each origin's visible vintage.

    Forecast targets are the unique first-estimate records for months 1, 3 and
    6 after each origin month. Seasonal naive reads the target's lag-12 month;
    trailing mean averages the 12 consecutive months ending at the origin.
    Both baselines abstain together whenever required history is incomplete.
    """
    if type(split) is not str or split not in {"validation", "holdout"}:
        raise ValueError("split must be validation or holdout")
    if type(origins) is not tuple or not 1 <= len(origins) <= MAX_CENSUS_EVALUATION_ORIGINS:
        raise ValueError("origins must be a bounded nonempty tuple")

    previous_month: date | None = None
    previous_issue: date | None = None
    for origin in origins:
        if type(origin) is not CensusForecastOrigin:
            raise ValueError("origins must contain exact CensusForecastOrigin values")
        if type(origin.reference_month) is not date or origin.reference_month.day != 1:
            raise ValueError("origin reference_month must be the first day of a month")
        if type(origin.issued_on) is not date:
            raise ValueError("origin issued_on must be an exact calendar date")
        if previous_month is not None and origin.reference_month <= previous_month:
            raise ValueError("origins must use unique reference months in chronological order")
        if previous_issue is not None and origin.issued_on <= previous_issue:
            raise ValueError("origin issue dates must be strictly increasing")
        previous_month = origin.reference_month
        previous_issue = origin.issued_on

    # One selector call validates the entire normalized input before the
    # evaluator indexes labels or computes any fingerprint.
    select_census_vintage_as_of(
        records, series_id=series_id, target_release_on=origins[0].issued_on
    )
    for record in records:
        _validate_metric_input(record.value)

    first_estimate_by_month: dict[date, CensusVintageRecord] = {}
    for record in records:
        if record.release_kind != "first_estimate":
            continue
        if record.reference_month in first_estimate_by_month:
            raise ValueError("each month must have one unique first-estimate label")
        first_estimate_by_month[record.reference_month] = record

    unanchored_revision_count = sum(
        record.release_kind != "first_estimate"
        and record.reference_month not in first_estimate_by_month
        for record in records
    )
    feature_records = tuple(
        record
        for record in records
        if record.release_kind == "first_estimate"
        or record.reference_month in first_estimate_by_month
    )

    input_manifest_sha256 = _manifest_sha256(records)
    per_horizon: dict[int, dict[str, object]] = {
        horizon: {
            "horizon_months": horizon,
            "requested_origins": len(origins),
            "scored_origins": 0,
            "coverage": 0.0,
            "abstentions": {
                "origin_first_estimate_missing": 0,
                "origin_not_published_at_issue": 0,
                "target_first_estimate_missing": 0,
                "target_not_future_at_origin": 0,
                "required_monthly_history_unavailable": 0,
            },
            "metrics": None,
        }
        for horizon in CENSUS_HORIZONS_MONTHS
    }
    forecasts: dict[int, dict[str, list[Fraction]]] = {
        horizon: {baseline: [] for baseline in _BASELINES}
        for horizon in CENSUS_HORIZONS_MONTHS
    }
    actuals: dict[int, list[Fraction]] = {
        horizon: [] for horizon in CENSUS_HORIZONS_MONTHS
    }
    origin_audit: list[dict[str, object]] = []

    for origin in origins:
        view = select_census_vintage_as_of(
            feature_records, series_id=series_id, target_release_on=origin.issued_on
        )
        visible_by_month = {item.reference_month: item for item in view.records}
        target_months = {
            _month_offset(origin.reference_month, horizon)
            for horizon in CENSUS_HORIZONS_MONTHS
        }
        unexpected_future = {
            month for month in visible_by_month
            if month > origin.reference_month and month not in target_months
        }
        if unexpected_future:
            raise ValueError("as-of vintage contains a future reference month")

        origin_record = first_estimate_by_month.get(origin.reference_month)
        if origin_record is None:
            origin_status = "origin_first_estimate_missing"
        elif origin_record.published_on >= origin.issued_on:
            origin_status = "origin_not_published_at_issue"
        else:
            origin_status = "origin_ready"

        horizon_audit: list[dict[str, object]] = []
        for horizon in CENSUS_HORIZONS_MONTHS:
            target_month = _month_offset(origin.reference_month, horizon)
            target = first_estimate_by_month.get(target_month)
            if origin_status != "origin_ready":
                status = origin_status
            elif target is None:
                if target_month in visible_by_month:
                    raise ValueError("target vintage is visible without a first-estimate label")
                status = "target_first_estimate_missing"
            elif target.published_on <= origin.issued_on:
                status = "target_not_future_at_origin"
            elif target_month in visible_by_month:
                raise ValueError("target vintage is visible before its first-estimate label")
            else:
                history_months = tuple(
                    _month_offset(origin.reference_month, -offset)
                    for offset in range(_TRAILING_MONTHS - 1, -1, -1)
                )
                if any(month not in visible_by_month for month in history_months):
                    status = "required_monthly_history_unavailable"
                else:
                    history = tuple(visible_by_month[month] for month in history_months)
                    seasonal_month = _month_offset(target_month, -12)
                    seasonal = visible_by_month.get(seasonal_month)
                    if seasonal is None:
                        status = "required_monthly_history_unavailable"
                    else:
                        history_values = tuple(
                            Fraction(item.value) for item in history
                        )
                        predictions = {
                            "seasonal_naive_lag12": Fraction(seasonal.value),
                            "trailing_12_month_mean": sum(
                                history_values, Fraction()
                            ) / _TRAILING_MONTHS,
                        }
                        for baseline in _BASELINES:
                            forecasts[horizon][baseline].append(predictions[baseline])
                        actuals[horizon].append(Fraction(target.value))
                        per_horizon[horizon]["scored_origins"] += 1
                        status = "scored"

            if status != "scored":
                abstentions = per_horizon[horizon]["abstentions"]
                abstentions[status] += 1
            horizon_audit.append({
                "horizon_months": horizon,
                "target_month": target_month.isoformat(),
                "status": status,
                "target_published_on": target.published_on.isoformat() if target else None,
                "target_release_id": target.release_id if target else None,
                "target_snapshot_sha256": target.snapshot_sha256 if target else None,
            })

        as_of_manifest_sha256 = _manifest_sha256(view.records)
        origin_audit.append({
            "reference_month": origin.reference_month.isoformat(),
            "issued_on": origin.issued_on.isoformat(),
            "origin_status": origin_status,
            "as_of_vintage_receipt": _selection_receipt(
                view, as_of_manifest_sha256
            ),
            "as_of_vintage_manifest_sha256": as_of_manifest_sha256,
            "horizon_results": tuple(horizon_audit),
        })

    for horizon in CENSUS_HORIZONS_MONTHS:
        summary = per_horizon[horizon]
        count = summary["scored_origins"]
        summary["coverage"] = count / len(origins)
        if count >= 2:
            summary["metrics"] = {
                baseline: _metrics(tuple(forecasts[horizon][baseline]), tuple(actuals[horizon]))
                for baseline in _BASELINES
            }
        summary["evaluation_status"] = "metrics_available" if count >= 2 else "abstained"

    any_metrics = any(item["metrics"] is not None for item in per_horizon.values())
    return {
        "schema_version": CENSUS_BACKTEST_SCHEMA,
        "status": (
            "aggregate_vintage_backtest_unverified"
            if any_metrics else "aggregate_vintage_backtest_abstained"
        ),
        "evaluation_split": split,
        "source_status": "caller_supplied_not_source_verified",
        "series_id": series_id,
        "input_record_count": len(records),
        "unanchored_revision_count": unanchored_revision_count,
        "input_manifest_sha256": input_manifest_sha256,
        "requested_origins": len(origins),
        "horizons": tuple(per_horizon[horizon] for horizon in CENSUS_HORIZONS_MONTHS),
        "origin_audit": tuple(origin_audit),
        "ingestion_authorized": False,
        "forecast_eligible": False,
    }
