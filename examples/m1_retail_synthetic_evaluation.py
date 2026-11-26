"""Run the fictional UCI-shaped evidence-to-evaluation example.

Usage: ``python -m examples.m1_retail_synthetic_evaluation --holdout-days 7``

The reusable fixture lives in the retail domain package so API and CLI callers
share one implementation. Its bytes and release declarations are fictional.
"""
from __future__ import annotations

import argparse
import json

from mirrormind.domains.retail.synthetic_fixtures import (
    EVALUATION_ON,
    SYNTHETIC_STOCK_CODE,
    build_synthetic_evidence_flow,
    run_synthetic_evaluation,
)

__all__ = (
    "EVALUATION_ON",
    "SYNTHETIC_STOCK_CODE",
    "build_synthetic_evidence_flow",
    "main",
    "run_synthetic_evaluation",
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a fictional release-aware retail baseline evaluation"
    )
    parser.add_argument("--holdout-days", type=int, default=7)
    args = parser.parse_args()
    try:
        result = run_synthetic_evaluation(holdout_days=args.holdout_days)
    except (OSError, TypeError, ValueError):
        parser.exit(2, "Invalid synthetic retail evaluation configuration.\n")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
