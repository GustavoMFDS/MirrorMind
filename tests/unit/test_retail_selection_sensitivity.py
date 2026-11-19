"""Counterfactual bounds on invented retail rows, not demand inference."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.selection_sensitivity import (
    assess_excluded_target_sensitivity,
)
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(index):
    return START + timedelta(days=index - 1)


def fixture(*, missing80=False, late75=False, value75=75, late83=False):
    rows, releases = [], []
    for index in range(1, 85):
        if missing80 and index == 80:
            continue
        event = day(index)
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "PRIVATE-SKU",
            "InvoiceDate": datetime(event.year, event.month, event.day, 10),
            "Quantity": value75 if index == 75 else index,
            "CustomerID": "NEVER-COPY",
        })
        released = (
            day(84) if late75 and index == 75
            else day(85) if late83 and index == 83
            else event
        )
        releases.append(DeclaredProductRelease("PRIVATE-SKU", event, released))
    return project_uci_retail_rows(rows), tuple(releases)


def evaluate(projection, releases, *, ceiling=200, **kwargs):
    return assess_excluded_target_sensitivity(
        projection, releases, stock_code="PRIVATE-SKU",
        evaluation_on=day(84), excluded_value_ceiling=ceiling, **kwargs,
    )


def test_complete_fictional_windows_have_exact_observed_mean_difference():
    projection, releases = fixture()
    report = evaluate(projection, releases)
    assert (report.earlier_eligible, report.later_eligible) == (7, 7)
    assert (report.earlier_mean_floor, report.earlier_mean_ceiling) == (74, 74)
    assert (report.later_mean_floor, report.later_mean_ceiling) == (81, 81)
    assert (report.difference_floor, report.difference_ceiling) == (7, 7)
    assert report.direction_status == "positive_under_declared_counterfactual_bounds_only"
    receipt = str(report.receipt())
    for private in ("PRIVATE-SKU", "NEVER-COPY", "500001"):
        assert private not in receipt
    assert "population_shift_status" in receipt
    with pytest.raises(FrozenInstanceError):
        report.later_eligible = 99


def test_incomplete_windows_show_unknown_days_can_reverse_apparent_difference():
    projection, releases = fixture(missing80=True, late75=True, late83=True)
    report = evaluate(projection, releases, ceiling=1000)
    assert report.earlier_eligible < 7 and report.later_eligible < 7
    assert report.difference_floor < 0 < report.difference_ceiling
    assert report.direction_status == "direction_not_robust_to_declared_counterfactual_bounds"
    assert report.receipt()["selection_bias_status"] == "not_identified"


def test_unpublished_value_change_does_not_rewrite_earlier_counterfactual_bounds():
    projection, releases = fixture(late75=True, value75=75)
    changed, same_releases = fixture(late75=True, value75=999999)
    earlier = evaluate(projection, releases)
    later = evaluate(changed, same_releases)
    assert releases == same_releases
    assert earlier.earlier_eligible == later.earlier_eligible
    assert earlier.earlier_mean_floor == later.earlier_mean_floor
    assert earlier.earlier_mean_ceiling == later.earlier_mean_ceiling


def test_counterfactual_ceiling_changes_assumption_not_observed_eligibility():
    projection, releases = fixture(missing80=True, late75=True, late83=True)
    lower = evaluate(projection, releases, ceiling=100)
    higher = evaluate(projection, releases, ceiling=200)
    assert lower.earlier_eligible == higher.earlier_eligible
    assert lower.later_eligible == higher.later_eligible
    assert higher.difference_floor <= lower.difference_floor
    assert higher.difference_ceiling >= lower.difference_ceiling


@pytest.mark.parametrize("bad", [True, -1, 1_000_001, 1.0, "100", None])
def test_assumptions_are_exact_and_bounded(bad):
    projection, releases = fixture()
    with pytest.raises(ValueError, match="excluded_value_ceiling"):
        evaluate(projection, releases, ceiling=bad)


def test_missing_release_declaration_fails_before_scenario_analysis():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        evaluate(projection, releases[:-1])


def test_invalid_calendar_cutoff_rejected():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="exact date"):
        assess_excluded_target_sensitivity(
            projection, releases, stock_code="PRIVATE-SKU",
            evaluation_on=datetime(2011, 3, 25), excluded_value_ceiling=100,
        )
