"""Source-unverified rolling-origin baseline evaluation on staged daily rows.

This is an offline, bounded algorithm; no licensed data ingestion,
model training, uncertainty calibration or real-world inference API.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from math import sqrt

from mirrormind.modules.evidence.snapshots import StagedSnapshot, available_as_of

BASELINES = ("seasonal_naive_lag7", "trailing_mean_lag7")


def _day(value: str) -> date:
    """Require exact, unambiguous ISO calendar days for evaluation cutoffs."""
    if type(value) is not str or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        raise ValueError("evaluation date must be canonical YYYY-MM-DD")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("invalid evaluation calendar date") from exc
    if parsed.isoformat() != value:
        raise ValueError("noncanonical evaluation date")
    return parsed


def _predict(seven: tuple[int, ...]) -> dict[str, float]:
    """Return fixed one-day estimates from exactly seven prior daily values."""
    if len(seven) != 7 or any(type(value) is not int or value < 0 for value in seven):
        raise ValueError("seven exact nonnegative historical integers required")
    return {
        "seasonal_naive_lag7": float(seven[0]),
        "trailing_mean_lag7": sum(seven) / 7,
    }


def _score(forecasts: tuple[float, ...], actuals: tuple[int, ...]) -> dict[str, float | None]:
    """Return matched MAE/RMSE/signed bias and undefined-zero WAPE as None."""
    if not actuals or len(forecasts) != len(actuals):
        raise ValueError("aligned nonempty scoring observations required")
    errors = tuple(forecast - value for forecast, value in zip(forecasts, actuals))
    sum_abs = sum(abs(error) for error in errors)
    observed_sum = sum(actuals)
    return {
        "mae": sum_abs / len(errors),
        "rmse": sqrt(sum(error * error for error in errors) / len(errors)),
        "bias": sum(errors) / len(errors),
        "wape": None if observed_sum == 0 else sum_abs / observed_sum,
    }


def backtest_staged_snapshot(
    snapshot: StagedSnapshot, *, series_id: str, evaluation_on: str,
    holdout_days: int = 7, min_history_days: int = 14,
) -> dict[str, object]:
    """Evaluate fixed daily origins only with data published before each origin.

    The snapshot carries **unverified source assertions**. Scores on its
    contents cannot be described as authentic empirical model performance.
    Each score uses the same tested origins for both fixed heuristics.
    """
    if type(snapshot) is not StagedSnapshot:
        raise ValueError("expected structurally staged snapshot")
    if type(holdout_days) is not int or not 2 <= holdout_days <= 100:
        raise ValueError("holdout_days must be an exact integer in 2..100")
    if type(min_history_days) is not int or not 7 <= min_history_days <= 10_000:
        raise ValueError("min_history_days must be an exact integer in 7..10000")
    cutoff = _day(evaluation_on)
    series = tuple(row for row in snapshot.observations if row.series_id == series_id)
    if not series:
        raise ValueError("unknown or empty staged series")
    first_holdout = cutoff - timedelta(days=holdout_days - 1)
    if series[0].observed_on > first_holdout - timedelta(days=min_history_days):
        raise ValueError("insufficient event-day history before holdout")
    by_day = {row.observed_on: row for row in series}
    forecast_values: dict[str, list[float]] = {name: [] for name in BASELINES}
    actual_values: list[int] = []
    history_abstained = 0
    target_abstained = 0
    missing_targets = 0
    unpublished_targets = 0
    origin_audit: list[dict[str, str]] = []
    for offset in range(holdout_days):
        target_day = first_holdout + timedelta(days=offset)
        target = by_day.get(target_day)
        origin = target_day - timedelta(days=1)
        audit = {"target_on": target_day.isoformat(), "origin_on": origin.isoformat()}
        # Missing and late-published targets must not be combined in the audit.
        # Neither reason exposes the underlying target value.
        if target is None:
            target_abstained += 1
            missing_targets += 1
            origin_audit.append({**audit, "status": "target_missing"})
            continue
        if target.available_on > cutoff:
            target_abstained += 1
            unpublished_targets += 1
            origin_audit.append({**audit, "status": "target_not_published_by_cutoff"})
            continue
        past = available_as_of(snapshot, series_id=series_id, origin_on=origin.isoformat())
        eligible_by_day = {row.observed_on: row.units for row in past}
        required = tuple(origin - timedelta(days=delta) for delta in range(6, -1, -1))
        if any(day not in eligible_by_day for day in required):
            history_abstained += 1
            origin_audit.append({**audit, "status": "required_history_unavailable"})
            continue
        values = tuple(eligible_by_day[day] for day in required)
        predictions = _predict(values)
        for name in BASELINES:
            forecast_values[name].append(predictions[name])
        actual_values.append(target.units)
        origin_audit.append({**audit, "status": "scored"})
    count = len(actual_values)
    metrics = None
    winner = None
    if count >= 2:
        metrics = {name: _score(tuple(forecast_values[name]), tuple(actual_values))
                   for name in BASELINES}
        seasonal = metrics[BASELINES[0]]["mae"]
        moving = metrics[BASELINES[1]]["mae"]
        assert isinstance(seasonal, float) and isinstance(moving, float)
        winner = "tie" if seasonal == moving else BASELINES[0] if seasonal < moving else BASELINES[1]
    return {
        "status": "staged_asof_backtest_unverified" if count >= 2 else "staged_asof_backtest_abstained",
        "source_status": "not_authorized_or_authenticated",
        "snapshot_sha256": snapshot.sha256_hex,
        "series_id": series_id,
        "evaluation_on": cutoff.isoformat(),
        "holdout_first_date": first_holdout.isoformat(),
        "holdout_last_date": cutoff.isoformat(),
        "requested_origins": holdout_days,
        "scored_origins": count,
        "abstained_missing_history": history_abstained,
        "abstained_target_unavailable": target_abstained,
        "abstained_target_missing": missing_targets,
        "abstained_target_not_published": unpublished_targets,
        "origin_audit": origin_audit,
        "metrics": metrics,
        "lower_mae_on_scored_origins_only": winner,
    }
