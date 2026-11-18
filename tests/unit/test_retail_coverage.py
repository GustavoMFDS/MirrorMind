"""No-imputation coverage regressions use only invented transactions."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime

import pytest

from mirrormind.domains.retail.coverage import summarize_retail_coverage
from mirrormind.domains.retail.uci_transactions import (
    ProductDayUnits,
    UciRetailProjection,
    project_uci_retail_rows,
)


def _row(invoice: str, product: str, day: int, quantity: int = 1):
    return {
        "InvoiceNo": invoice,
        "StockCode": product,
        "InvoiceDate": datetime(2011, 1, day, 10),
        "Quantity": quantity,
        "CustomerID": "TOP-SECRET",
    }


def test_internal_gaps_are_not_zero_or_imputed_and_receipt_has_no_identifiers():
    projection = project_uci_retail_rows([
        _row("536365", "PRIVATE-A", 1, 2),
        _row("536366", "PRIVATE-A", 4, 3),
        _row("536367", "PRIVATE-B", 2, 1),
        _row("C536368", "PRIVATE-A", 2, -2),
        _row("536369", "PRIVATE-A", 3, -1),
    ])
    summary = summarize_retail_coverage(projection)
    assert summary.observed_product_days == 3
    assert summary.distinct_products == 2
    assert summary.internal_missing_product_days == 2
    assert summary.products_with_internal_gaps == 1
    assert summary.earliest_event_day == date(2011, 1, 1)
    assert summary.latest_event_day == date(2011, 1, 4)
    receipt = str(summary.receipt())
    assert "PRIVATE-A" not in receipt
    assert "PRIVATE-B" not in receipt
    assert "TOP-SECRET" not in receipt
    assert "not_authorized" in receipt
    assert "unknown_not_derived_from_invoice_date" in receipt
    with pytest.raises(FrozenInstanceError):
        summary.distinct_products = 99


def test_all_excluded_transactions_have_no_imputed_observation_window():
    projection = project_uci_retail_rows([_row("C536365", "SKU-A", 1, -1)])
    summary = summarize_retail_coverage(projection)
    assert summary.observed_product_days == 0
    assert summary.internal_missing_product_days == 0
    assert summary.earliest_event_day is None
    assert summary.latest_event_day is None


def test_observation_window_excludes_before_first_and_after_last():
    projection = project_uci_retail_rows([
        _row("536365", "SKU-A", 11),
        _row("536366", "SKU-A", 12),
    ])
    assert summarize_retail_coverage(projection).internal_missing_product_days == 0


def test_repeated_or_reversed_product_days_cannot_masquerade_as_valid():
    for days in (
        (ProductDayUnits("A", date(2011, 1, 1), 1),) * 2,
        (
            ProductDayUnits("A", date(2011, 1, 2), 1),
            ProductDayUnits("A", date(2011, 1, 1), 1),
        ),
    ):
        projection = UciRetailProjection(days, 2, 2, 0, 0, 0)
        with pytest.raises(ValueError, match="duplicate or unordered"):
            summarize_retail_coverage(projection)


@pytest.mark.parametrize("bad_units", [True, 0, -1, 1_000_000_001, "3"])
def test_forged_invalid_product_day_units_fail_closed(bad_units):
    projection = UciRetailProjection(
        (ProductDayUnits("SKU-A", date(2011, 1, 1), bad_units),), 1, 1, 0, 0, 0
    )
    with pytest.raises(ValueError, match="invalid product-day"):
        summarize_retail_coverage(projection)


def test_wrong_projection_type_is_rejected():
    with pytest.raises(TypeError, match="UciRetailProjection"):
        summarize_retail_coverage([])
