"""Run fixed monthly baselines against a fictional release-vintage series.

Example: python -m examples.m1_census_vintage_evaluation --split validation
All values, releases and publication dates are generated in memory.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from decimal import Decimal

from mirrormind.domains.retail.census_evaluation import (
    CensusForecastOrigin,
    evaluate_census_vintage_backtest,
)
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

SERIES_ID = "RSAFS"
_SPLITS = {
    "validation": (
        CensusForecastOrigin(date(2020, 12, 1), date(2021, 1, 16)),
        CensusForecastOrigin(date(2021, 1, 1), date(2021, 2, 16)),
    ),
    "holdout": (
        CensusForecastOrigin(date(2021, 2, 1), date(2021, 3, 16)),
        CensusForecastOrigin(date(2021, 3, 1), date(2021, 4, 16)),
    ),
}


def _next_month(month: date) -> date:
    return date(month.year + (month.month == 12), month.month % 12 + 1, 1)


def build_synthetic_records() -> tuple[CensusVintageRecord, ...]:
    """Create a deterministic monthly series and one later fictional revision."""
    records: list[CensusVintageRecord] = []
    month = date(2020, 1, 1)
    end = date(2021, 9, 1)
    index = 0
    while month <= end:
        target_value = 100 + 10 * month.month if month.year == 2021 else 100
        records.append(CensusVintageRecord(
            series_id=SERIES_ID,
            reference_month=month,
            value=Decimal(target_value),
            published_on=date(_next_month(month).year, _next_month(month).month, 15),
            release_kind="first_estimate",
            release_id=f"synthetic-first-{month:%Y-%m}",
            snapshot_sha256=f"{index:064x}",
        ))
        month = _next_month(month)
        index += 1

    november = next(item for item in records if item.reference_month == date(2020, 11, 1))
    records.append(CensusVintageRecord(
        series_id=SERIES_ID,
        reference_month=november.reference_month,
        value=Decimal(999),
        published_on=date(2021, 2, 1),
        release_kind="monthly_revision",
        release_id="synthetic-revision-2020-11",
        snapshot_sha256="f" * 64,
    ))
    return tuple(records)


def run_synthetic_evaluation(*, split: str = "validation") -> dict[str, object]:
    """Evaluate one fixed fictional origin split without reading source files."""
    if split not in _SPLITS:
        raise ValueError("split must be validation or holdout")
    return evaluate_census_vintage_backtest(
        build_synthetic_records(),
        series_id=SERIES_ID,
        origins=_SPLITS[split],
        split=split,  # type: ignore[arg-type] - the local allowlist bounds this value
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate fixed baselines on fictional Census vintages"
    )
    parser.add_argument("--split", choices=tuple(_SPLITS), default="validation")
    args = parser.parse_args()
    try:
        result = run_synthetic_evaluation(split=args.split)
        output = json.dumps(
            result, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
    except (TypeError, ValueError):
        parser.exit(2, "Invalid synthetic Census vintage evaluation input.\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
