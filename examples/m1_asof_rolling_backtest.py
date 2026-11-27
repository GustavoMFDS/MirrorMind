"""Synthetic one-step rolling evaluation with as-of publication-time abstention.

Unlike a mere event-date cutoff, each forecast origin uses a complete
lag-7 window available by that origin. Neither publication timestamps nor
source permission are authenticated in this teaching experiment.
Run: python -m examples.m1_asof_rolling_backtest examples/synthetic-asof-weekly-sales.json
"""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from itertools import pairwise
from pathlib import Path

from examples.m1_availability_preflight import asof_batch
from examples.m1_observation_preflight import MAX_INPUT_BYTES, _day, _no_duplicate_keys
from examples.m1_temporal_backtest import _predict, _score

SCHEMA = "mirrormind.synthetic_asof_backtest.v1"
MODEL_NAMES = ("seasonal_naive_lag7", "trailing_mean_lag7")


def _require_contiguous_days(days: list[date]) -> None:
    """Reject calendar gaps without filling missing dates with zero demand."""
    for previous, next_day in pairwise(days):
        if next_day != previous + timedelta(days=1):
            raise ValueError("missing event-date record; do not impute demand")


def backtest_asof(
    payload: object, *, holdout_days: int = 7, min_train_days: int = 14,
) -> dict[str, object]:
    """Score one-step synthetic baselines only when lag history was published."""
    if type(holdout_days) is not int or not 2 <= holdout_days <= 100:
        raise ValueError("holdout_days must be an exact integer in 2..100")
    if type(min_train_days) is not int or not 7 <= min_train_days <= 10000:
        raise ValueError("min_train_days must be an exact integer in 7..10000")

    # Validates synthetic envelope, dates, publication order, uniqueness and units.
    verified_shape = asof_batch(payload)
    assert isinstance(payload, dict)
    rows = sorted(payload["records"], key=lambda value: value["observed_on"])
    if len(rows) < min_train_days + holdout_days:
        raise ValueError("insufficient history for declared evaluation spans")
    cutoff = _day(payload["as_of_date"], "as_of_date")
    days = [_day(row["observed_on"], "observed_on") for row in rows]
    if cutoff != days[-1]:
        raise ValueError("evaluation cutoff must be last observed day")
    _require_contiguous_days(days)

    first_test = len(rows) - holdout_days
    forecast_lists: dict[str, list[float]] = {name: [] for name in MODEL_NAMES}
    targets: list[int] = []
    abstained = 0
    for i in range(first_test, len(rows)):
        origin = days[i - 1]
        target = rows[i]
        if _day(target["available_on"], "target available_on") > cutoff:
            raise ValueError("held-out target was not published by evaluation cutoff")
        last_seven = rows[i - 7:i]
        if any(
            _day(row["available_on"], "history available_on") > origin
            for row in last_seven
        ):
            abstained += 1
            continue
        # Last seven events are consecutive and published by *this* origin.
        # We never pass current/future target values into the two estimators.
        forecasts = _predict(tuple(row["units"] for row in last_seven))
        for name in MODEL_NAMES:
            forecast_lists[name].append(forecasts[name])
        targets.append(target["units"])

    scored = len(targets)
    scores: dict[str, dict[str, float | None]] | None = None
    winner: str | None = None
    if scored >= 2:
        scores = {name: _score(forecast_lists[name], targets) for name in MODEL_NAMES}
        a, b = (scores[name]["mae"] for name in MODEL_NAMES)
        assert isinstance(a, float) and isinstance(b, float)
        winner = "tie" if a == b else MODEL_NAMES[0] if a < b else MODEL_NAMES[1]
    return {
        "schema_version": SCHEMA,
        "status": (
            "synthetic_asof_rolling_evaluation_not_real_forecast"
            if scored >= 2 else "synthetic_asof_rolling_abstained"
        ),
        "source_status": "synthetic_unverified",
        "series_id": verified_shape["series_id"],
        "evaluation_cutoff": cutoff.isoformat(),
        "holdout_first_date": days[first_test].isoformat(),
        "holdout_last_date": days[-1].isoformat(),
        "requested_origins": holdout_days,
        "scored_origins": scored,
        "abstained_origins": abstained,
        "protocol": "rolling_one_step_full_lag7_available_at_each_origin",
        "metrics": scores,
        "lower_mae_on_scored_synthetic_origins": winner,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic as-of one-step rolling evaluation")
    parser.add_argument("configuration", type=Path)
    parser.add_argument("--holdout-days", type=int, default=7)
    args = parser.parse_args()
    try:
        with args.configuration.open("rb") as file:
            raw = file.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("fixture exceeds byte cap")
        payload = json.loads(raw, object_pairs_hook=_no_duplicate_keys)
        result = backtest_asof(payload, holdout_days=args.holdout_days)
    except (OSError, UnicodeError, ValueError, TypeError):
        parser.exit(2, "Invalid synthetic as-of backtest fixture.\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
