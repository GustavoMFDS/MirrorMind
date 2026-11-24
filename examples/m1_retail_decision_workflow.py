"""Run the complete fictional retail decision comparison locally.

Usage: ``python -m examples.m1_retail_decision_workflow --as-of 2011-01-26``

Only generated in-memory evidence is used. Successful output remains
experimental, conditional, non-authorizing and separate from WorldKernel.
"""
from __future__ import annotations

import argparse
import json
from datetime import date

from mirrormind.domains.retail.synthetic_decision_workflow import (
    DEFAULT_AS_OF,
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a fictional end-to-end retail decision comparison"
    )
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat())
    parser.add_argument("--replications", type=int, default=12)
    parser.add_argument("--seed", type=int, default=317)
    args = parser.parse_args(argv)
    try:
        as_of = date.fromisoformat(args.as_of)
        if as_of.isoformat() != args.as_of:
            raise ValueError("as-of date must be canonical YYYY-MM-DD")
        request = SyntheticDecisionWorkflowRequest(
            as_of=as_of,
            replications=args.replications,
            seed=args.seed,
        )
        result = run_synthetic_decision_workflow(request)
    except (OSError, TypeError, ValueError):
        parser.exit(2, "Invalid synthetic retail decision workflow configuration.\n")
    print(json.dumps(result, ensure_ascii=False, allow_nan=False,
                     sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
