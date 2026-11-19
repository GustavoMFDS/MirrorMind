"""Synthetic-only conservative coverage gate regressions."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.coverage_gate import assess_retail_backtest_coverage
from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows


def fixture(*, incomplete=False):
    start = date(2011, 1, 1)
    rows = []
    releases = []
    for index in range(1, 36):
        if incomplete and index == 33:
            continue
        day = start + timedelta(days=index - 1)
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "SECRET-SKU",
            "Quantity": (index % 7) + 1,
            "InvoiceDate": datetime(day.year, day.month, day.day, 10),
            "CustomerID": "DO-NOT-LEAK",
        })
        released = (
            start + timedelta(days=29) if incomplete and index == 27
            else start + timedelta(days=35) if incomplete and index == 35
            else day
        )
        releases.append(DeclaredProductRelease("SECRET-SKU", day, released))
    return (
        project_uci_retail_rows(rows), tuple(releases),
        start + timedelta(days=34),
    )


def evaluate(*, incomplete=False, threshold=80):
    projection, releases, evaluation_on = fixture(incomplete=incomplete)
    return assess_retail_backtest_coverage(
        projection, releases, stock_code="SECRET-SKU",
        evaluation_on=evaluation_on, holdout_days=7,
        minimum_coverage_percent=threshold,
    )


def test_incomplete_declared_releases_suppress_model_ranking_and_report_exact_coverage():
    report = evaluate(incomplete=True)
    receipt = report.receipt()
    assert (report.scored_origins, report.requested_origins) == (2, 7)
    assert (report.unavailable_history, report.missing_target,
            report.unpublished_target) == (3, 1, 1)
    assert receipt["coverage_numerator"] == 2
    assert receipt["coverage_denominator"] == 7
    assert report.comparison_status == "insufficient_coverage_for_comparison"
    assert receipt["conditional_lower_mae"] is None
    assert receipt["prediction_interval"] is None
    assert receipt["uncertainty_status"] == "not_estimated_or_calibrated"
    assert "SECRET-SKU" not in str(receipt)
    assert "DO-NOT-LEAK" not in str(receipt)
    with pytest.raises(FrozenInstanceError):
        report.scored_origins = 100


def test_complete_fictional_history_passes_gate_without_proving_forecast_skill():
    report = evaluate()
    assert report.scored_origins == 7
    assert report.comparison_status == "eligible_for_conditional_comparison_only"
    assert report.conditional_lower_mae in (
        "seasonal_naive_lag7", "trailing_mean_lag7", "tie",
    )
    assert report.receipt()["status"] == "fictional_retail_coverage_gate_not_authorized"
    assert report.receipt()["prediction_interval"] is None


def test_exact_integer_threshold_boundary_prevents_rounding_up_coverage():
    assert evaluate(incomplete=True, threshold=28).comparison_status == (
        "eligible_for_conditional_comparison_only"
    )
    assert evaluate(incomplete=True, threshold=29).comparison_status == (
        "insufficient_coverage_for_comparison"
    )


@pytest.mark.parametrize("bad", [0, 101, True, 80.0, "80", None])
def test_invalid_thresholds_fail_before_backtest(bad):
    projection, releases, evaluation_on = fixture()
    with pytest.raises(ValueError, match="minimum_coverage_percent"):
        assess_retail_backtest_coverage(
            projection, releases, stock_code="SECRET-SKU",
            evaluation_on=evaluation_on, minimum_coverage_percent=bad,
        )


def test_impossible_release_declarations_still_fail_closed():
    projection, releases, evaluation_on = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        assess_retail_backtest_coverage(
            projection, releases[:-1], stock_code="SECRET-SKU",
            evaluation_on=evaluation_on,
        )
