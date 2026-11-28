"""Compose reviewed retail evidence with fixed, release-aware baseline evaluation.

The evaluator reuses the existing bounded retail backtest. Its declared
release dates remain caller assertions, and its output is not an authorized
forecast, a demand estimate or a recommendation.
"""
from __future__ import annotations

from datetime import date, timedelta

from mirrormind.domains.retail.evidence_flow import RetailUciEvidenceFlow
from mirrormind.domains.retail.release_backtest import (
    backtest_declared_retail_releases,
)


def evaluate_retail_evidence_flow(
    flow: RetailUciEvidenceFlow,
    *,
    stock_code: str,
    evaluation_on: date,
    holdout_days: int = 7,
) -> dict[str, object]:
    """Return an aggregate fixed-split evaluation and one status per target.

    The prepared flow's declared-release audit must use the same evaluation
    cutoff. The existing release backtest then validates every projected
    product-day declaration, requires seven consecutive released history
    days, and scores both fixed baselines on exactly the same eligible targets.
    Dates, counts and statuses are retained; identifiers and raw observations
    are not copied into the result.
    """
    if type(flow) is not RetailUciEvidenceFlow:
        raise ValueError("expected a composed local UCI retail evidence flow")
    if type(evaluation_on) is not date:
        raise ValueError("evaluation_on must be an exact date")
    if (
        type(flow.release_audit.origin_on) is not date
        or flow.release_audit.origin_on != evaluation_on
    ):
        raise ValueError("evaluation_on must match the evidence flow audit cutoff")

    backtest = backtest_declared_retail_releases(
        flow.workbook.projection,
        flow.declared_releases,
        stock_code=stock_code,
        evaluation_on=evaluation_on,
        holdout_days=holdout_days,
    )
    scored = backtest["metrics"] is not None
    # The lower-level helper is fixture-oriented. This wrapper accepts any
    # prepared flow, so keep the output truthful when caller provenance is
    # unknown instead of repeating its fictional-fixture label.
    baseline_evaluation = {
        **backtest,
        "status": (
            "declared_retail_evaluation_unverified"
            if scored else "declared_retail_evaluation_abstained"
        ),
    }
    requested_origins = backtest["holdout_days"]
    assert type(requested_origins) is int
    first_target_on = evaluation_on - timedelta(days=requested_origins - 1)
    return {
        "schema_version": "mirrormind.retail.evidence_evaluation.v1",
        "status": (
            "local_retail_evidence_evaluation_unverified"
            if scored else "local_retail_evidence_evaluation_abstained"
        ),
        "source_status": "caller_declared_release_not_authenticated_or_authorized",
        "evaluation_cutoff": evaluation_on.isoformat(),
        "split": {
            "method": "fixed_last_n_calendar_days",
            "first_target_on": first_target_on.isoformat(),
            "last_target_on": evaluation_on.isoformat(),
            "requested_origins": requested_origins,
        },
        "evidence_receipt": flow.receipt(),
        "baseline_evaluation": baseline_evaluation,
        "origin_receipts": backtest["origin_audit"],
        "ingestion_authorized": False,
        "forecast_eligible": False,
    }
