"""Fictional adjacent-window eligibility and provenance checks."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.eligibility_drift import audit_retail_eligibility_drift
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(index):
    return START + timedelta(days=index - 1)


def fixture(*, gaps=False, delayed75=84):
    rows, releases = [], []
    for index in range(1, 85):
        if gaps and index == 80:
            continue
        event = day(index)
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "PRIVATE-SKU",
            "InvoiceDate": datetime(event.year, event.month, event.day, 10),
            "Quantity": (index % 7) + 1,
            "CustomerID": "NEVER-COPY",
        })
        publication = (
            day(delayed75) if gaps and index == 75
            else day(85) if gaps and index == 82
            else event
        )
        releases.append(DeclaredProductRelease("PRIVATE-SKU", event, publication))
    return project_uci_retail_rows(rows), tuple(releases)


def evaluate(projection, releases, **kwargs):
    return audit_retail_eligibility_drift(
        projection, releases, stock_code="PRIVATE-SKU",
        evaluation_on=day(84), window_days=7, **kwargs,
    )


def test_complete_fictional_history_has_full_eligibility_in_both_windows():
    projection, releases = fixture()
    result = evaluate(projection, releases)
    assert (result.earlier_requested, result.later_requested) == (7, 7)
    assert (result.earlier_evaluated, result.later_evaluated) == (7, 7)
    assert result.receipt()["eligible_origin_change"] == 0
    assert result.receipt()["distribution_shift_status"] == "not_measured"
    assert result.receipt()["selection_bias_status"].startswith("not_identifiable")
    assert result.receipt()["statistical_significance"] is None
    receipt = str(result.receipt())
    for forbidden in ("PRIVATE-SKU", "NEVER-COPY", "500001"):
        assert forbidden not in receipt
    with pytest.raises(FrozenInstanceError):
        result.later_evaluated = 100


def test_gaps_late_publication_and_unknown_target_change_eligibility_not_demand():
    projection, releases = fixture(gaps=True)
    result = evaluate(projection, releases)
    assert result.earlier_evaluated < result.earlier_requested
    assert result.later_evaluated < result.later_requested
    assert result.earlier_unpublished >= 1
    assert result.later_missing == 1
    assert result.later_unpublished >= 1
    for prefix in ("earlier", "later"):
        assert getattr(result, prefix + "_requested") == sum(
            getattr(result, prefix + suffix) for suffix in (
                "_evaluated", "_missing", "_unpublished",
                "_history_abstained", "_calibration_abstained",
            )
        )
    assert result.receipt()["distribution_shift_status"] == "not_measured"


def test_future_release_change_cannot_rewrite_earlier_eligibility():
    projection, first = fixture(gaps=True, delayed75=84)
    _, second = fixture(gaps=True, delayed75=85)
    a = evaluate(projection, first)
    b = evaluate(projection, second)
    for name in a.__dataclass_fields__:
        if name.startswith("earlier_"):
            assert getattr(a, name) == getattr(b, name)


def test_missing_release_declaration_remains_a_hard_failure():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        evaluate(projection, releases[:-1])


@pytest.mark.parametrize("value", [True, 1, 31, 7.0, "7"])
def test_invalid_window_sizes_are_rejected(value):
    projection, releases = fixture()
    with pytest.raises(ValueError, match="window_days"):
        evaluate(projection, releases, window_days=value)


def test_ambiguous_dates_are_rejected():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="exact date"):
        audit_retail_eligibility_drift(
            projection, releases, stock_code="PRIVATE-SKU",
            evaluation_on=datetime(2011, 3, 25),
        )
