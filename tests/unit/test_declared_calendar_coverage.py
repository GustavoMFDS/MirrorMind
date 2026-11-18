"""Purely fictional operational-calendar coverage and negative contracts."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime

import pytest

from mirrormind.domains.retail.calendar_coverage import (
    MAX_DECLARED_DAYS,
    summarize_declared_calendar_coverage,
)
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows


def _row(invoice: str, stock: str, day: int, quantity: int = 1):
    return {
        "InvoiceNo": invoice,
        "StockCode": stock,
        "Quantity": quantity,
        "InvoiceDate": datetime(2011, 1, day, 9),
        "CustomerID": "FICTIONAL-SECRET",
    }


def test_closed_day_not_counted_as_missing_declared_observation():
    projection = project_uci_retail_rows([
        _row("536365", "PRIVATE-SKU", 7),
        _row("536366", "PRIVATE-SKU", 10),
        _row("536367", "OTHER-SKU", 7),
        _row("C536368", "PRIVATE-SKU", 8, -2),
    ])
    # Jan 8 and 9 are explicitly omitted; Jan 10 is a declared day.
    result = summarize_declared_calendar_coverage(
        projection, (date(2011, 1, 7), date(2011, 1, 10))
    )
    assert result.internal_missing_declared_days == 0
    assert result.internal_unscheduled_civil_days == 2
    assert result.distinct_products == 2
    assert result.observed_product_days == 3
    receipt = str(result.receipt())
    assert "PRIVATE-SKU" not in receipt
    assert "OTHER-SKU" not in receipt
    assert "FICTIONAL-SECRET" not in receipt
    assert "caller_declared_unverified" in receipt
    with pytest.raises(FrozenInstanceError):
        result.calendar_days = 12


def test_declared_open_day_between_sales_is_missing_not_zero():
    projection = project_uci_retail_rows([
        _row("536365", "SKU-A", 7),
        _row("536366", "SKU-A", 10),
    ])
    result = summarize_declared_calendar_coverage(
        projection,
        (date(2011, 1, 7), date(2011, 1, 8), date(2011, 1, 10)),
    )
    assert result.internal_missing_declared_days == 1
    assert result.internal_unscheduled_civil_days == 1
    assert result.products_with_declared_gaps == 1
    assert "not_source_verified" in result.receipt()["status"]


@pytest.mark.parametrize("calendar", [
    (), [], (date(2011, 1, 7), date(2011, 1, 7)),
    (date(2011, 1, 10), date(2011, 1, 7)),
    (datetime(2011, 1, 7), date(2011, 1, 10)),
    (True,), (date(2011, 1, 7),) * (MAX_DECLARED_DAYS + 1),
])
def test_invalid_or_unbounded_declared_calendar_fails_closed(calendar):
    projection = project_uci_retail_rows([_row("536365", "SKU-A", 7)])
    with pytest.raises(ValueError, match="declared calendar"):
        summarize_declared_calendar_coverage(projection, calendar)


def test_observed_sale_outside_declared_calendar_is_rejected():
    projection = project_uci_retail_rows([_row("536365", "SKU-A", 7)])
    with pytest.raises(ValueError, match="absent from declared calendar"):
        summarize_declared_calendar_coverage(projection, (date(2011, 1, 8),))


def test_no_positive_sales_cannot_prove_any_product_existed_or_was_open():
    projection = project_uci_retail_rows([_row("C536365", "SKU-A", 7, -2)])
    result = summarize_declared_calendar_coverage(
        projection, (date(2011, 1, 7), date(2011, 1, 8))
    )
    assert result.observed_product_days == 0
    assert result.distinct_products == 0
    assert result.internal_missing_declared_days == 0
    assert result.internal_unscheduled_civil_days == 0


def test_calendar_before_first_or_after_last_sale_is_not_missing():
    projection = project_uci_retail_rows([_row("536365", "SKU-A", 8)])
    result = summarize_declared_calendar_coverage(
        projection, (date(2011, 1, 7), date(2011, 1, 8), date(2011, 1, 9))
    )
    assert result.internal_missing_declared_days == 0
