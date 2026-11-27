"""Fixed-split event-time research evaluation for a reviewed local UCI snapshot.

The evaluator compares positive invoice-line units, not latent demand. It
requires explicit date-coverage assertions before interpreting absent rows as
zero and never treats ``InvoiceDate`` as historical publication time.
"""
from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import date, timedelta
from typing import Literal

from mirrormind.domains.retail.uci_transactions import (
    MAX_SUPPORTED_UCI_WORKBOOK_GROUPS,
    ProductDayUnits,
    is_valid_uci_stock_code,
)
from mirrormind.domains.retail.uci_workbook import UciWorkbookReadResult
from mirrormind.modules.forecasting.baselines import _predict, _score

SOURCE_START = date(2010, 12, 1)
FIT_START = SOURCE_START
FIT_END = date(2011, 8, 30)
VALIDATION_ORIGIN_START = date(2011, 8, 31)
VALIDATION_ORIGIN_END = date(2011, 9, 30)
HOLDOUT_ORIGIN_START = date(2011, 10, 1)
HOLDOUT_ORIGIN_END = date(2011, 12, 8)
SOURCE_END = HOLDOUT_ORIGIN_END + timedelta(days=1)
MAX_SOURCE_DAYS = 400
MAX_EVENT_PRODUCTS = 10_000
_SHA256 = re.compile(r"[0-9a-f]{64}")
_BASELINES = (
    ("same_weekday_last_week", "seasonal_naive_lag7"),
    ("trailing_7_calendar_day_mean", "trailing_mean_lag7"),
)


class UciEventTimeEvaluationError(ValueError):
    """A snapshot, coverage contract or fixed split is not representable."""


def _date_range(start: date, end: date) -> tuple[date, ...]:
    return tuple(start + timedelta(days=index) for index in range((end - start).days + 1))


def _snapshot_counts(snapshot: UciWorkbookReadResult) -> dict[tuple[str, date], int]:
    if not isinstance(snapshot, UciWorkbookReadResult):
        raise UciEventTimeEvaluationError("a parsed local workbook snapshot is required")
    if type(snapshot.sha256_hex) is not str or not _SHA256.fullmatch(snapshot.sha256_hex):
        raise UciEventTimeEvaluationError("snapshot digest is malformed")
    projection = snapshot.projection
    if (
        type(projection.days) is not tuple
        or len(projection.days) > MAX_SUPPORTED_UCI_WORKBOOK_GROUPS
    ):
        raise UciEventTimeEvaluationError("snapshot product-day groups exceed the local bound")

    counts: dict[tuple[str, date], int] = {}
    for item in projection.days:
        if not isinstance(item, ProductDayUnits):
            raise UciEventTimeEvaluationError("snapshot contains an invalid product-day record")
        if not is_valid_uci_stock_code(item.stock_code, allow_internal_spaces=True):
            raise UciEventTimeEvaluationError("snapshot contains an invalid product code")
        if type(item.observed_on) is not date or not SOURCE_START <= item.observed_on <= SOURCE_END:
            raise UciEventTimeEvaluationError("snapshot event date is outside the reviewed window")
        if type(item.units) is not int or item.units <= 0:
            raise UciEventTimeEvaluationError("snapshot units must be positive exact integers")
        key = (item.stock_code, item.observed_on)
        if key in counts:
            raise UciEventTimeEvaluationError("snapshot has duplicate product-day groups")
        counts[key] = item.units
    if len({code for code, _ in counts}) > MAX_EVENT_PRODUCTS:
        raise UciEventTimeEvaluationError("snapshot product count exceeds the local bound")
    return counts


def _coverage_dates(values: Iterable[date]) -> frozenset[date]:
    try:
        iterator = iter(values)
    except TypeError as exc:
        raise UciEventTimeEvaluationError("complete_event_dates must be iterable") from exc
    dates: set[date] = set()
    for value in iterator:
        if type(value) is not date or not SOURCE_START <= value <= SOURCE_END:
            raise UciEventTimeEvaluationError("coverage date is outside the reviewed window")
        if value in dates:
            raise UciEventTimeEvaluationError("coverage dates must not contain duplicates")
        if len(dates) >= MAX_SOURCE_DAYS:
            raise UciEventTimeEvaluationError("coverage calendar exceeds the local bound")
        dates.add(value)
    fit_dates = set(_date_range(FIT_START, FIT_END))
    if not fit_dates.issubset(dates):
        raise UciEventTimeEvaluationError("fit period coverage must be complete to freeze cohort")
    return frozenset(dates)


def _metrics(
    forecasts: tuple[float, ...], actuals: tuple[int, ...]
) -> dict[str, float | None] | None:
    if len(actuals) < 2:
        return None
    full = _score(forecasts, actuals)
    return {name: full[name] for name in ("mae", "rmse", "wape")}


def evaluate_uci_event_time(
    snapshot: UciWorkbookReadResult,
    *,
    complete_event_dates: Iterable[date],
    split: Literal["validation", "holdout"],
) -> dict[str, object]:
    """Compare fixed one-day baselines on one frozen UCI event-time split.

    The caller supplies date-level completeness from a separately reviewed
    snapshot manifest. An absent product-day is zero only on a covered date;
    otherwise that product-origin abstains. Returned product summaries use
    stable ordinals, never the source stock code. All claims remain
    retrospective because UCI provides no row-level publication vintages.
    """
    if split == "validation":
        origin_start, origin_end = VALIDATION_ORIGIN_START, VALIDATION_ORIGIN_END
    elif split == "holdout":
        origin_start, origin_end = HOLDOUT_ORIGIN_START, HOLDOUT_ORIGIN_END
    else:
        raise UciEventTimeEvaluationError("split must be validation or holdout")

    counts = _snapshot_counts(snapshot)
    coverage = _coverage_dates(complete_event_dates)
    fit_codes = sorted({
        code for code, observed in counts if FIT_START <= observed <= FIT_END
    })
    all_codes = {code for code, _ in counts}
    excluded_future = len(all_codes - set(fit_codes))
    target_dates = _date_range(origin_start + timedelta(days=1), origin_end + timedelta(days=1))
    eligible_pairs = len(fit_codes) * len(target_dates)
    scored_actuals: list[int] = []
    scored_forecasts: dict[str, list[float]] = {name: [] for name, _ in _BASELINES}
    product_scores: list[dict[str, object]] = []
    abstentions = {
        "target_coverage_unverified": 0,
        "history_coverage_unverified": 0,
    }
    scored_pairs = 0

    for ordinal, stock_code in enumerate(fit_codes, start=1):
        product_actuals: list[int] = []
        product_forecasts: dict[str, list[float]] = {
            name: [] for name, _ in _BASELINES
        }
        for target_on in target_dates:
            if target_on not in coverage:
                abstentions["target_coverage_unverified"] += 1
                continue
            history = _date_range(target_on - timedelta(days=7), target_on - timedelta(days=1))
            if not set(history).issubset(coverage):
                abstentions["history_coverage_unverified"] += 1
                continue
            values = tuple(counts.get((stock_code, day), 0) for day in history)
            actual = counts.get((stock_code, target_on), 0)
            predictions = _predict(values)
            scored_actuals.append(actual)
            product_actuals.append(actual)
            for name, baseline_key in _BASELINES:
                prediction = predictions[baseline_key]
                scored_forecasts[name].append(prediction)
                product_forecasts[name].append(prediction)
            scored_pairs += 1
        product_scores.append({
            "product_ordinal": ordinal,
            "scored_pairs": len(product_actuals),
            "coverage": (
                len(product_actuals) / len(target_dates) if target_dates else 0.0
            ),
            "metrics": {
                name: _metrics(tuple(product_forecasts[name]), tuple(product_actuals))
                for name, _ in _BASELINES
            },
        })

    pooled_metrics = None
    if scored_pairs >= 2:
        pooled_metrics = {
            name: _metrics(tuple(scored_forecasts[name]), tuple(scored_actuals))
            for name, _ in _BASELINES
        }
    return {
        "schema_version": "mirrormind.uci.event_time_evaluation.v1",
        "status": "event_time_retrospective_unverified_availability",
        "evaluation_status": "metrics_available" if pooled_metrics else "abstained",
        "source_status": "caller_supplied_snapshot_not_authorized_by_parser",
        "publication_time_status": "unknown_not_derived_from_invoice_date",
        "target_semantics": (
            "positive_invoice_line_units_from_recognized_invoice_ids_not_latent_demand"
        ),
        "snapshot_sha256": snapshot.sha256_hex,
        "split": split,
        "fit_start": FIT_START.isoformat(),
        "fit_end": FIT_END.isoformat(),
        "origin_start": origin_start.isoformat(),
        "origin_end": origin_end.isoformat(),
        "target_start": target_dates[0].isoformat(),
        "target_end": target_dates[-1].isoformat(),
        "cohort_rule": "positive_product_day_in_fit_period",
        "cohort_size": len(fit_codes),
        "excluded_post_fit_products": excluded_future,
        "eligible_product_origin_pairs": eligible_pairs,
        "scored_product_origin_pairs": scored_pairs,
        "coverage": scored_pairs / eligible_pairs if eligible_pairs else 0.0,
        "abstentions": abstentions,
        "metrics": pooled_metrics,
        "per_product": tuple(product_scores),
        "projection_receipt": {
            **snapshot.projection.receipt(),
            "unverified_invoice_prefix_rows": (
                snapshot.projection.unverified_invoice_prefix_rows
            ),
        },
        "ingestion_authorized": False,
        "point_in_time_eligible": False,
    }
