"""Fictional conditional value comparisons and anti-hindsight regressions."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.eligible_values import compare_eligible_retail_values
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(index):
    return START + timedelta(days=index - 1)


def fixture(*, delay75=False, value75=75, omit80=False, delay83=False):
    rows, releases = [], []
    for index in range(1, 85):
        if omit80 and index == 80:
            continue
        event = day(index)
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "SECRET-SKU",
            "InvoiceDate": datetime(event.year, event.month, event.day, 10),
            "Quantity": value75 if index == 75 else index,
            "CustomerID": "NEVER-COPY",
        })
        available = (day(84) if delay75 and index == 75
                     else day(85) if delay83 and index == 83 else event)
        releases.append(DeclaredProductRelease("SECRET-SKU", event, available))
    return project_uci_retail_rows(rows), tuple(releases)


def evaluate(projection, releases, **options):
    return compare_eligible_retail_values(
        projection, releases, stock_code="SECRET-SKU",
        evaluation_on=day(84), **options,
    )


def test_complete_fictional_history_exposes_only_conditional_means_and_medians():
    projection, releases = fixture()
    result = evaluate(projection, releases)
    receipt = result.receipt()
    assert (result.earlier_eligible, result.later_eligible) == (7, 7)
    assert (result.earlier_requested, result.later_requested) == (7, 7)
    assert (result.earlier_mean, result.later_mean) == (74, 81)
    assert result.later_minus_earlier_mean == 7
    assert (result.earlier_median, result.later_median) == (74, 81)
    assert receipt["status"] == "eligible_subset_descriptive_comparison_only"
    assert receipt["selection_bias_status"] == "unknown_for_excluded_targets"
    assert receipt["distribution_shift_status"] == "not_identified"
    assert receipt["significance"] is None
    for secret in ("SECRET-SKU", "NEVER-COPY", "500001"):
        assert secret not in str(receipt)
    with pytest.raises(FrozenInstanceError):
        result.earlier_mean = 1


def test_sparse_observed_and_late_targets_refuse_conditional_difference():
    projection, releases = fixture(delay75=True, omit80=True, delay83=True)
    result = evaluate(projection, releases)
    assert result.earlier_eligible < 7
    assert result.later_eligible < 7
    assert result.earlier_unpublished >= 1
    assert result.later_unpublished >= 1
    assert result.later_missing == 1
    assert result.status == "insufficient_comparable_coverage_abstained"
    assert result.earlier_mean is None
    assert result.later_mean is None
    assert result.later_minus_earlier_mean is None
    for prefix in ("earlier", "later"):
        assert getattr(result, prefix + "_requested") == sum(
            getattr(result, prefix + suffix) for suffix in (
                "_eligible", "_missing", "_unpublished",
                "_history_unavailable", "_calibration_unavailable",
            )
        )


def test_changing_unpublished_earlier_target_does_not_rewrite_earlier_statistics():
    first, releases = fixture(delay75=True, value75=75)
    changed, same_releases = fixture(delay75=True, value75=999999)
    assert releases == same_releases
    a = evaluate(first, releases, minimum_coverage_percent=1)
    b = evaluate(changed, same_releases, minimum_coverage_percent=1)
    assert a.earlier_eligible == b.earlier_eligible
    assert a.earlier_mean == b.earlier_mean
    assert a.earlier_median == b.earlier_median
    assert a.earlier_unpublished == b.earlier_unpublished


def test_minimum_coverage_threshold_blocks_conditional_statistics():
    projection, releases = fixture(delay75=True)
    blocked = evaluate(projection, releases, minimum_coverage_percent=80)
    assert blocked.earlier_mean is None
    assert blocked.status.endswith("abstained")
    allowed = evaluate(projection, releases, minimum_coverage_percent=50)
    assert allowed.earlier_eligible >= 2
    assert allowed.status == "eligible_subset_descriptive_comparison_only"
    assert allowed.earlier_mean is not None


def test_release_declaration_missing_fails_closed():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        evaluate(projection, releases[:-1])


@pytest.mark.parametrize("key,value,match", [
    ("window_days", True, "window_days"),
    ("window_days", 31, "window_days"),
    ("minimum_eligible_per_window", 1, "minimum_eligible_per_window"),
    ("minimum_eligible_per_window", 8, "minimum_eligible_per_window"),
    ("minimum_coverage_percent", 0, "minimum_coverage_percent"),
    ("minimum_coverage_percent", 101, "minimum_coverage_percent"),
    ("minimum_coverage_percent", 80.0, "minimum_coverage_percent"),
])
def test_invalid_thresholds_fail_closed(key, value, match):
    projection, releases = fixture()
    with pytest.raises(ValueError, match=match):
        evaluate(projection, releases, **{key: value})


def test_datetime_not_accepted_as_exact_cutoff():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="exact date"):
        compare_eligible_retail_values(
            projection, releases, stock_code="SECRET-SKU",
            evaluation_on=datetime(2011, 3, 25),
        )
