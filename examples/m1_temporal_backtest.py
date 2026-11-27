"""Experimental rolling-origin forecasts on a synthetic daily series only.

No real-data connector, historical availability proof, trained ML model,
uncertainty interval or production forecasting API is provided.
Run: python -m examples.m1_temporal_backtest examples/synthetic-weekly-sales.json
"""
from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path

from examples.m1_observation_preflight import (
    MAX_INPUT_BYTES,
    _no_duplicate_keys,
    validate_batch,
)

SCHEMA = "mirrormind.synthetic_backtest.v1"
MODEL_NAMES = ("seasonal_naive_lag7", "trailing_mean_lag7")


def _predict(past: tuple[int, ...]) -> dict[str, float]:
    """Produce only one-step-ahead estimates from available past values."""
    if len(past) < 7:
        raise ValueError("at least seven past calendar observations required")
    last_seven = past[-7:]
    return {
        "seasonal_naive_lag7": float(last_seven[0]),
        "trailing_mean_lag7": sum(last_seven) / 7,
    }


def _score(predictions: list[float], actual: list[int]) -> dict[str, float | None]:
    """Evaluate aligned held-out observations, with zero-denominator abstention."""
    if not actual or len(predictions) != len(actual):
        raise ValueError("predictions and actual values must align and be nonempty")
    count = len(actual)
    errors = [forecast - value for forecast, value in zip(predictions, actual, strict=True)]
    absolute = sum(abs(error) for error in errors)
    total = sum(actual)
    return {
        "mae": absolute / count,
        "rmse": sqrt(sum(error * error for error in errors) / count),
        "bias": sum(errors) / count,
        "wape": None if total == 0 else absolute / total,
    }


def backtest_batch(
    payload: object, *, holdout_days: int = 7, min_train_days: int = 14,
) -> dict[str, object]:
    """Run fixed, one-step rolling origins without imputing or using future targets.

    This evaluation is only for a synthetic fixture with one contiguous
    daily series and an explicit last-observation cutoff.
    """
    if type(holdout_days) is not int or not 2 <= holdout_days <= 100:
        raise ValueError("holdout_days must be an exact integer between 2 and 100")
    if type(min_train_days) is not int or not 7 <= min_train_days <= 10_000:
        raise ValueError("min_train_days must be an exact integer between 7 and 10000")
    summary = validate_batch(payload)
    assert isinstance(payload, dict)
    if payload["source_id"] != "synthetic-fixture-generator" or not str(
        payload["usage_note"]
    ).lower().startswith("generated teaching data"):
        raise ValueError("only explicitly labeled synthetic teaching fixtures supported")
    records = sorted(payload["records"], key=lambda row: row["date"])
    if summary["missing_day_count"] != 0:
        raise ValueError("daily series has gaps; missing observations must not become zeros")
    if records[-1]["date"] != summary["cutoff_date"]:
        raise ValueError("cutoff must be the date of the last observed row")
    if len(records) < min_train_days + holdout_days:
        raise ValueError("not enough history for the declared train and holdout spans")
    if len(records) > 10_000:
        raise ValueError("observation count exceeds experiment limit")
    values = tuple(row["units"] for row in records)
    start = len(values) - holdout_days
    predictions: dict[str, list[float]] = {name: [] for name in MODEL_NAMES}
    observed = list(values[start:])
    for index in range(start, len(values)):
        # Past is a new *prefix*, excluding the target and every future row.
        forecasts = _predict(values[:index])
        for name in MODEL_NAMES:
            predictions[name].append(forecasts[name])
    model_scores = {
        name: _score(predictions[name], observed) for name in MODEL_NAMES
    }
    baseline_mae = model_scores["seasonal_naive_lag7"]["mae"]
    mean_mae = model_scores["trailing_mean_lag7"]["mae"]
    assert isinstance(baseline_mae, float) and isinstance(mean_mae, float)
    winner = (
        "tie" if baseline_mae == mean_mae
        else "seasonal_naive_lag7" if baseline_mae < mean_mae
        else "trailing_mean_lag7"
    )
    return {
        "schema_version": SCHEMA,
        "status": "synthetic_rolling_backtest_not_production_forecast",
        "series_id": summary["series_id"],
        "source_status": "synthetic_unverified",
        "cutoff_date": summary["cutoff_date"],
        "holdout_first_date": records[start]["date"],
        "holdout_last_date": records[-1]["date"],
        "train_days_before_first_origin": start,
        "evaluated_origins": holdout_days,
        "protocol": "one_step_rolling_origin_history_only",
        "metrics": model_scores,
        "lower_mae_on_this_fixture": winner,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic-only rolling-origin baseline comparison")
    parser.add_argument("configuration", type=Path)
    parser.add_argument("--holdout-days", type=int, default=7)
    args = parser.parse_args()
    try:
        with args.configuration.open("rb") as stream:
            raw = stream.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("synthetic input exceeds byte cap")
        payload = json.loads(raw, object_pairs_hook=_no_duplicate_keys)
        result = backtest_batch(payload, holdout_days=args.holdout_days)
    except (OSError, UnicodeError, ValueError, TypeError):
        parser.exit(2, "Invalid synthetic backtest fixture.\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
