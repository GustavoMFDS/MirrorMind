"""End-to-end synthetic evidence-to-retail-evaluation regressions."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date

import pytest

from examples.m1_retail_synthetic_evaluation import (
    build_synthetic_evidence_flow,
    run_synthetic_evaluation,
)
from mirrormind.domains.retail.evaluation_flow import evaluate_retail_evidence_flow


def test_synthetic_cli_is_reproducible_and_returns_sanitized_origin_receipts():
    command = [
        sys.executable,
        "-m",
        "examples.m1_retail_synthetic_evaluation",
        "--holdout-days",
        "7",
    ]
    first = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    second = subprocess.run(command, check=True, capture_output=True, text=True, timeout=30)
    result = json.loads(first.stdout)

    assert first.stdout == second.stdout
    assert result["schema_version"] == "mirrormind.retail.evidence_evaluation.v1"
    assert result["status"] == "local_retail_evidence_evaluation_unverified"
    assert result["source_status"] == (
        "caller_declared_release_not_authenticated_or_authorized"
    )
    assert result["forecast_eligible"] is False
    assert result["ingestion_authorized"] is False
    assert result["evidence_receipt"]["status"] == (
        "local_retail_uci_evidence_flow_not_authorized"
    )
    assert result["evidence_receipt"]["forecast_eligible"] is False
    assert result["evidence_receipt"]["ingestion_authorized"] is False
    assert result["baseline_evaluation"]["status"] == (
        "declared_retail_evaluation_unverified"
    )
    assert result["split"] == {
        "method": "fixed_last_n_calendar_days",
        "first_target_on": "2011-01-29",
        "last_target_on": "2011-02-04",
        "requested_origins": 7,
    }
    evaluation = result["baseline_evaluation"]
    assert evaluation["scored_origins"] == 2
    assert evaluation["abstained_history"] == 3
    assert evaluation["abstained_missing_target"] == 1
    assert evaluation["abstained_unpublished_target"] == 1
    assert len(result["origin_receipts"]) == 7
    assert result["origin_receipts"] == evaluation["origin_audit"]
    assert [item["status"] for item in result["origin_receipts"]] == [
        "required_history_unavailable",
        "required_history_unavailable",
        "scored",
        "scored",
        "target_missing_not_zero",
        "required_history_unavailable",
        "target_unpublished_at_evaluation",
    ]
    assert set(evaluation["metrics"]) == {
        "seasonal_naive_lag7",
        "trailing_mean_lag7",
    }
    for private_value in (
        "SYNTHETIC-SKU",
        "500001",
        "1234501",
        "SYNTHETIC-SOURCE-01",
        "SYNTHETIC-LICENSE-01",
    ):
        assert private_value not in first.stdout


def test_evaluation_rejects_mismatched_release_audit_cutoff():
    flow = build_synthetic_evidence_flow()

    with pytest.raises(ValueError, match="must match the evidence flow audit cutoff"):
        evaluate_retail_evidence_flow(
            flow,
            stock_code="SYNTHETIC-SKU",
            evaluation_on=date(2011, 2, 3),
        )


def test_unpublished_target_mutation_does_not_change_scores_or_origin_receipts():
    baseline = run_synthetic_evaluation(future_units=9)
    mutated = run_synthetic_evaluation(future_units=999)

    assert baseline["baseline_evaluation"] == mutated["baseline_evaluation"]
    assert baseline["origin_receipts"] == mutated["origin_receipts"]
    assert baseline["evidence_receipt"]["projection"]["workbook_sha256"] != (
        mutated["evidence_receipt"]["projection"]["workbook_sha256"]
    )


def test_unpublished_holdout_abstains_without_metrics_or_winner():
    result = run_synthetic_evaluation(all_unpublished=True)
    evaluation = result["baseline_evaluation"]

    assert result["status"] == "local_retail_evidence_evaluation_abstained"
    assert evaluation["scored_origins"] == 0
    assert evaluation["metrics"] is None
    assert evaluation["lower_mae_on_matched_origins_only"] is None
    assert evaluation["abstained_unpublished_target"] == 6
    assert evaluation["abstained_missing_target"] == 1
