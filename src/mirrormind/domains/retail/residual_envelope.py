"""Offline prequential residual-envelope diagnostics on fictional retail proxies.

A trailing maximum absolute residual is a descriptive *heuristic*, not a
calibrated predictive interval or a guarantee of any coverage level.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from functools import cache
from heapq import heappop, heappush

from mirrormind.domains.retail.declared_releases import (
    DeclaredProductRelease,
    audit_declared_releases_as_of,
)
from mirrormind.domains.retail.uci_transactions import UciRetailProjection
from mirrormind.modules.forecasting.baselines import _predict


def evaluate_retail_residual_envelopes(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    holdout_days: int = 7,
    calibration_days: int = 21,
    min_calibration_residuals: int = 5,
) -> dict[str, object]:
    """Audit one-day seasonal-naive envelopes using only past published errors.

    Each historical residual is admitted only if its own seven feature days
    were available before its forecast origin and its target was released
    no later than the *current* forecast origin. A target missing from the
    positive-line projection is never interpreted as a recorded zero.
    """
    if type(evaluation_on) is not date:
        raise ValueError("evaluation_on must be an exact date")
    if type(holdout_days) is not int or not 2 <= holdout_days <= 30:
        raise ValueError("holdout_days must be an exact integer in 2..30")
    if type(calibration_days) is not int or not 5 <= calibration_days <= 60:
        raise ValueError("calibration_days must be an exact integer in 5..60")
    if (
        type(min_calibration_residuals) is not int
        or not 3 <= min_calibration_residuals <= calibration_days
    ):
        raise ValueError("min_calibration_residuals must be in 3..calibration_days")
    if type(stock_code) is not str or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,31}", stock_code
    ):
        raise ValueError("invalid product selector")
    if evaluation_on.toordinal() <= holdout_days + calibration_days + 7:
        raise ValueError("evaluation calendar precedes supported calibration history")

    # Validates every release declaration (including other products) once.
    audit_declared_releases_as_of(projection, releases, origin_on=evaluation_on)
    observed = {day.observed_on: day.units for day in projection.days
                if day.stock_code == stock_code}
    if not observed:
        raise ValueError("unknown product selector")
    published = {(entry.stock_code, entry.observed_on): entry.available_on
                 for entry in releases}

    # Cache only within this evaluation: a forecast for target is determined
    # by the seven values published at its own preceding origin. Never reuse
    # predictions across distinct calls or evaluation cutoffs.
    @cache
    def _predict_on(target: date) -> float | None:
        origin = target - timedelta(days=1)
        history = tuple(origin - timedelta(days=offset) for offset in range(6, -1, -1))
        if any(
            day not in observed or published[(stock_code, day)] > origin
            for day in history
        ):
            return None
        return _predict(tuple(observed[day] for day in history))["seasonal_naive_lag7"]

    first = evaluation_on - timedelta(days=holdout_days - 1)
    # Only calendar candidates that can enter a holdout calibration window.
    # Scheduling uses declared dates, but a candidate's units are not read
    # until its release is available at the CURRENT holdout origin.
    earliest_candidate = first - timedelta(days=calibration_days)
    final_origin = evaluation_on - timedelta(days=1)
    release_events = sorted(
        (published[(stock_code, past)], past)
        for past in observed
        if earliest_candidate <= past <= final_origin
        and published[(stock_code, past)] <= final_origin
    )
    event_index = 0
    active_count = 0
    # A candidate expires based on its target date even if published late.
    expirations: list[tuple[date, float]] = []
    maximums: list[tuple[float, date]] = []

    statuses: list[dict[str, str]] = []
    covered = 0
    for index in range(holdout_days):
        target = first + timedelta(days=index)
        origin = target - timedelta(days=1)
        oldest = target - timedelta(days=calibration_days)

        # Advance publication time even when the present target abstains;
        # this retains eligible history for later origins. No future
        # outcome is read to compute a residual before publication.
        while event_index < len(release_events) and release_events[event_index][0] <= origin:
            _, past = release_events[event_index]
            event_index += 1
            if past < oldest:
                continue
            past_point = _predict_on(past)
            if past_point is None:
                continue
            residual = abs(observed[past] - past_point)
            heappush(expirations, (past, residual))
            heappush(maximums, (-residual, past))
            active_count += 1

        while expirations and expirations[0][0] < oldest:
            heappop(expirations)
            active_count -= 1
        while maximums and maximums[0][1] < oldest:
            heappop(maximums)

        prefix = {"target_on": target.isoformat(), "origin_on": origin.isoformat()}
        if target not in observed:
            statuses.append({**prefix, "status": "target_missing_not_zero"})
            continue
        if published[(stock_code, target)] > evaluation_on:
            statuses.append({**prefix, "status": "target_unpublished_by_evaluation"})
            continue
        point = _predict_on(target)
        if point is None:
            statuses.append({**prefix, "status": "forecast_history_unavailable"})
            continue
        if active_count < min_calibration_residuals:
            statuses.append({**prefix, "status": "insufficient_published_residuals"})
            continue
        # The maximum remains a descriptive heuristic, not a calibrated interval.
        radius = -maximums[0][0]
        low = max(0.0, point - radius)
        high = point + radius
        if low <= observed[target] <= high:
            covered += 1
        statuses.append({**prefix, "status": "retrospective_envelope_evaluated"})

    count = {status: sum(row["status"] == status for row in statuses) for status in (
        "target_missing_not_zero",
        "target_unpublished_by_evaluation",
        "forecast_history_unavailable",
        "insufficient_published_residuals",
        "retrospective_envelope_evaluated",
    )}
    eligible = count["retrospective_envelope_evaluated"]
    assert sum(count.values()) == holdout_days
    return {
        "status": "fictional_retail_residual_diagnostic_not_calibrated",
        "source_status": "caller_declared_release_not_authenticated_or_authorized",
        "method": "trailing_maximum_published_absolute_seasonal_naive_error",
        "uncertainty_status": "heuristic_envelope_not_prediction_interval",
        "evaluation_on": evaluation_on.isoformat(),
        "requested_origins": holdout_days,
        "calibration_days": calibration_days,
        "minimum_calibration_residuals": min_calibration_residuals,
        "evaluated_origins": eligible,
        "retrospective_covered_origins": covered,
        "retrospective_coverage_numerator": covered,
        "retrospective_coverage_denominator": eligible,
        "abstained_missing_target": count["target_missing_not_zero"],
        "abstained_unpublished_target": count["target_unpublished_by_evaluation"],
        "abstained_forecast_history": count["forecast_history_unavailable"],
        "abstained_calibration": count["insufficient_published_residuals"],
        "origin_audit": tuple(statuses),
        "nominal_coverage": None,
        "calibrated_prediction_interval": None,
    }
