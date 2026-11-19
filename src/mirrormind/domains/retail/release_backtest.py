"""Synthetic-only rolling comparison on caller-declared release dates.

Positive invoice-line counts are NOT complete daily demand observations.
The evaluator abstains on missing targets/history instead of imputing zeros.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

from mirrormind.domains.retail.declared_releases import (
    DeclaredProductRelease,
    audit_declared_releases_as_of,
)
from mirrormind.domains.retail.uci_transactions import UciRetailProjection
from mirrormind.modules.forecasting.baselines import BASELINES, _predict, _score


def backtest_declared_retail_releases(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    holdout_days: int = 7,
) -> dict[str, object]:
    """Compare two fixed one-day baselines on matched, eligible fictional days.

    Release assertions are checked for *all* projected product-days, not only
    the selected product. Every origin requires seven consecutive prior
    calendar days with a positive row and release <= origin. Target scoring
    additionally requires the target release <= evaluation cutoff.
    """
    if type(evaluation_on) is not date:
        raise ValueError("evaluation_on must be an exact date")
    if type(holdout_days) is not int or not 2 <= holdout_days <= 30:
        raise ValueError("holdout_days must be an exact integer in 2..30")
    if type(stock_code) is not str or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._-]{0,31}", stock_code
    ):
        raise ValueError("invalid product selector")
    if evaluation_on.toordinal() < holdout_days + 7:
        raise ValueError("evaluation dates precede supported calendar history")
    # This validates all keys, duplicates, release ordering and budgets.
    audit_declared_releases_as_of(projection, releases, origin_on=evaluation_on)
    selected = {item.observed_on: item.units for item in projection.days
                if item.stock_code == stock_code}
    if not selected:
        raise ValueError("unknown product selector")
    release_on = {(r.stock_code, r.observed_on): r.available_on for r in releases}
    first = evaluation_on - timedelta(days=holdout_days - 1)
    forecasts: dict[str, list[float]] = {name: [] for name in BASELINES}
    actuals: list[int] = []
    audit: list[dict[str, str]] = []
    for n in range(holdout_days):
        target_on = first + timedelta(days=n)
        origin = target_on - timedelta(days=1)
        prefix = {"target_on": target_on.isoformat(), "origin_on": origin.isoformat()}
        target = selected.get(target_on)
        if target is None:
            audit.append({**prefix, "status": "target_missing_not_zero"})
            continue
        if release_on[(stock_code, target_on)] > evaluation_on:
            audit.append({**prefix, "status": "target_unpublished_at_evaluation"})
            continue
        required = tuple(origin - timedelta(days=delta) for delta in range(6, -1, -1))
        if any(
            day not in selected or release_on[(stock_code, day)] > origin
            for day in required
        ):
            audit.append({**prefix, "status": "required_history_unavailable"})
            continue
        predictions = _predict(tuple(selected[day] for day in required))
        for name in BASELINES:
            forecasts[name].append(predictions[name])
        actuals.append(target)
        audit.append({**prefix, "status": "scored"})
    metrics = None
    winner = None
    if len(actuals) >= 2:
        metrics = {
            name: _score(tuple(forecasts[name]), tuple(actuals)) for name in BASELINES
        }
        naive = metrics[BASELINES[0]]["mae"]
        mean = metrics[BASELINES[1]]["mae"]
        assert isinstance(naive, float) and isinstance(mean, float)
        winner = "tie" if naive == mean else BASELINES[0] if naive < mean else BASELINES[1]
    counts = {status: sum(item["status"] == status for item in audit) for status in (
        "target_missing_not_zero", "target_unpublished_at_evaluation",
        "required_history_unavailable", "scored",
    )}
    return {
        "status": "fictional_retail_backtest_unverified" if metrics else "fictional_retail_backtest_abstained",
        "source_status": "caller_declared_release_not_authenticated_or_authorized",
        "proxy": "positive_invoice_line_units_not_true_demand",
        "evaluation_on": evaluation_on.isoformat(),
        "holdout_days": holdout_days,
        "scored_origins": counts["scored"],
        "abstained_missing_target": counts["target_missing_not_zero"],
        "abstained_unpublished_target": counts["target_unpublished_at_evaluation"],
        "abstained_history": counts["required_history_unavailable"],
        "origin_audit": tuple(audit),
        "metrics": metrics,
        "lower_mae_on_matched_origins_only": winner,
    }
