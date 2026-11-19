"""Fictional release-aware retail baseline regressions; no actual UCI rows."""
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.release_backtest import backtest_declared_retail_releases
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(index):
    return START + timedelta(days=index - 1)


def fixture(*, future_units=9):
    rows = []
    releases = []
    for index in range(1, 36):
        if index == 33:
            continue
        observed = day(index)
        units = future_units if index == 35 else (index % 7) + 1
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "PRIVATE-SKU",
            "InvoiceDate": datetime(observed.year, observed.month, observed.day, 10),
            "Quantity": units,
            "CustomerID": "PRIVATE-CUSTOMER",
        })
        available = day(30) if index == 27 else day(36) if index == 35 else observed
        releases.append(DeclaredProductRelease("PRIVATE-SKU", observed, available))
    return project_uci_retail_rows(rows), tuple(releases)


def evaluate(projection=None, releases=None, *, holdout_days=7):
    if projection is None:
        projection, default_releases = fixture()
        releases = default_releases if releases is None else releases
    return backtest_declared_retail_releases(
        projection, releases, stock_code="PRIVATE-SKU",
        evaluation_on=day(35), holdout_days=holdout_days,
    )


def test_missing_late_and_unpublished_days_abstain_and_models_share_origins():
    result = evaluate()
    assert result["scored_origins"] == 2
    assert result["abstained_history"] == 3
    assert result["abstained_missing_target"] == 1
    assert result["abstained_unpublished_target"] == 1
    assert sum(result[key] for key in (
        "scored_origins", "abstained_history", "abstained_missing_target",
        "abstained_unpublished_target",
    )) == result["holdout_days"]
    assert [a["status"] for a in result["origin_audit"]] == [
        "required_history_unavailable", "required_history_unavailable",
        "scored", "scored", "target_missing_not_zero",
        "required_history_unavailable", "target_unpublished_at_evaluation",
    ]
    assert result["metrics"] is not None
    assert set(result["metrics"]) == {"seasonal_naive_lag7", "trailing_mean_lag7"}
    assert "not_authenticated_or_authorized" in result["source_status"]
    serialized = str(result)
    for secret in ("PRIVATE-SKU", "PRIVATE-CUSTOMER", "500001"):
        assert secret not in serialized


def test_unpublished_future_target_value_does_not_change_scores_or_audit():
    projection, releases = fixture(future_units=9)
    mutated, other_releases = fixture(future_units=999_999)
    assert releases == other_releases
    assert evaluate(projection, releases) == evaluate(mutated, other_releases)


def test_unpublished_required_history_abstains_without_imputing_zero():
    projection, releases = fixture()
    revised = tuple(
        DeclaredProductRelease(r.stock_code, r.observed_on, day(36))
        if r.observed_on == day(27) else r for r in releases
    )
    result = evaluate(projection, revised)
    assert result["scored_origins"] == 0
    assert result["metrics"] is None
    assert result["lower_mae_on_matched_origins_only"] is None
    assert result["status"].endswith("abstained")


def test_missing_release_cannot_fall_back_to_invoice_date():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        evaluate(projection, releases[:-1])


def test_reject_unknown_product_ambiguous_cutoff_and_wrong_horizon():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="unknown product selector"):
        backtest_declared_retail_releases(
            projection, releases, stock_code="MISSING",
            evaluation_on=day(35),
        )
    with pytest.raises(ValueError, match="exact date"):
        backtest_declared_retail_releases(
            projection, releases, stock_code="PRIVATE-SKU",
            evaluation_on=datetime(2011, 2, 4),
        )
    for horizon in (True, 1, 31, "7"):
        with pytest.raises(ValueError, match="holdout_days"):
            evaluate(projection, releases, holdout_days=horizon)


def test_no_source_rights_or_available_on_field_are_fabricated():
    projection, releases = fixture()
    result = evaluate(projection, releases)
    assert all(not hasattr(item, "available_on") for item in projection.days)
    assert result["proxy"] == "positive_invoice_line_units_not_true_demand"
    assert result["evaluation_on"] == day(35).isoformat()
