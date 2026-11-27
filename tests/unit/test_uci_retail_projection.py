"""Bounded UCI-shaped transaction projections use only invented row mappings."""
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from mirrormind.domains.retail.uci_transactions import (
    MAX_ROWS,
    MAX_SUPPORTED_GROUPS,
    MAX_SUPPORTED_ROWS,
    ProductDayUnits,
    project_uci_retail_rows,
)


def row(
    invoice="536365",
    code="SKU-A",
    quantity=2,
    when=datetime(2011, 1, 5, 10, 30),
    **extras,
):
    return {
        "InvoiceNo": invoice,
        "StockCode": code,
        "Quantity": quantity,
        "InvoiceDate": when,
        **extras,
    }


def test_positive_rows_aggregate_by_product_calendar_day_without_raw_ids():
    inputs = [
        row("536366", "SKU-B", 4, datetime(2011, 1, 5, 9), CustomerID=9137),
        row("536365", "SKU-A", 2, datetime(2011, 1, 5, 10), CustomerID=7321),
        row(536367, "SKU-A", 3, datetime(2011, 1, 5, 17), Description="private"),
        row("536368", "SKU-A", 1, datetime(2011, 1, 6, 10), UnitPrice=29.99),
        row("C536369", "SKU-A", -2, datetime(2011, 1, 6, 11), CustomerID="secret"),
        row("536370", "SKU-B", -5, datetime(2011, 1, 6, 11)),
        row("536371", "SKU-B", 0, datetime(2011, 1, 6, 12)),
    ]
    result = project_uci_retail_rows(inputs)
    assert result.days == (
        ProductDayUnits("SKU-A", datetime(2011, 1, 5).date(), 5),
        ProductDayUnits("SKU-A", datetime(2011, 1, 6).date(), 1),
        ProductDayUnits("SKU-B", datetime(2011, 1, 5).date(), 4),
    )
    assert result.receipt() == {
        "status": "uci_shaped_projection_not_authorized",
        "publication_time_status": "unknown_not_derived_from_invoice_date",
        "processed_rows": 7,
        "accepted_rows": 4,
        "cancelled_rows": 1,
        "negative_quantity_rows": 1,
        "zero_quantity_rows": 1,
        "product_day_groups": 3,
    }
    assert all(not hasattr(day, "available_on") for day in result.days)
    with pytest.raises(FrozenInstanceError):
        result.days[0].units = 999
    with pytest.raises(FrozenInstanceError):
        result.processed_rows = 999


def test_shuffling_source_order_does_not_change_normalized_product_days():
    inputs = [
        row("536365", "SKU-A", 2),
        row("536366", "SKU-A", 3),
        row("536367", "SKU-B", 1),
        row("C536368", "SKU-A", -9),
    ]
    assert project_uci_retail_rows(inputs) == project_uci_retail_rows(inputs[::-1])


def test_empty_and_only_cancelled_inputs_are_distinct_outcomes():
    with pytest.raises(ValueError, match="at least one row"):
        project_uci_retail_rows([])
    result = project_uci_retail_rows([row(invoice="C536365", quantity=-4)])
    assert result.days == ()
    assert result.receipt()["cancelled_rows"] == 1
    assert result.receipt()["product_day_groups"] == 0


def test_retained_row_is_not_automatically_proof_of_merchandise_or_true_demand():
    result = project_uci_retail_rows([row(code="POST", quantity=4)])
    assert result.days[0].stock_code == "POST"
    # A real source adapter needs a reviewed merchandise-code classification.
    assert result.receipt()["status"].endswith("not_authorized")


def test_internal_ascii_space_policy_is_not_public_on_generic_projection():
    source_row = row(code="SPECIAL ITEM")
    with pytest.raises(ValueError, match="invalid product stock code"):
        project_uci_retail_rows([source_row])

    with pytest.raises(TypeError, match="unexpected keyword"):
        project_uci_retail_rows(
            [source_row], allow_internal_stock_code_spaces=True
        )


@pytest.mark.parametrize("bad", [True, 0, -2, MAX_SUPPORTED_ROWS + 1, 1.5, "10"])
def test_invalid_row_budgets_fail_before_consuming_rows(bad):
    with pytest.raises(ValueError, match="max_rows"):
        project_uci_retail_rows([row()], max_rows=bad)


@pytest.mark.parametrize("bad", [True, 0, -2, MAX_SUPPORTED_GROUPS + 1, 1.5, "10"])
def test_invalid_group_budgets_fail_before_consuming_rows(bad):
    with pytest.raises(ValueError, match="max_groups"):
        project_uci_retail_rows([row()], max_groups=bad)


def test_row_limit_is_enforced_on_iterator_without_materialization():
    seen = []

    def stream():
        for i in range(MAX_ROWS + 100):
            seen.append(i)
            yield row("536365", quantity=1)

    with pytest.raises(ValueError, match="row count"):
        project_uci_retail_rows(stream(), max_rows=2)
    assert seen == [0, 1, 2]


def test_explicit_source_bound_can_exceed_small_preflight_default():
    row_count = MAX_ROWS + 1

    def stream():
        for _ in range(row_count):
            yield row()

    result = project_uci_retail_rows(
        stream(), max_rows=row_count, max_groups=1
    )

    assert result.processed_rows == row_count
    assert result.accepted_rows == row_count
    assert len(result.days) == 1


def test_new_product_day_group_budget_rejects_excess_without_partial_result():
    with pytest.raises(ValueError, match="group count"):
        project_uci_retail_rows(
            [row("536365", code="SKU-A"), row("536366", code="SKU-B")],
            max_groups=1,
        )


def test_positive_quantity_total_is_bounded_not_wrapped():
    with pytest.raises(ValueError, match="aggregated positive quantity"):
        project_uci_retail_rows([
            row("536365", quantity=1_000_000_000),
            row("536366", quantity=1),
        ])


@pytest.mark.parametrize("quantity", [True, False, 1.5, "7", None, 1_000_000_001,
                                       -1_000_000_001])
def test_invalid_quantity_fails_closed_even_on_cancelled_invoice(quantity):
    with pytest.raises(ValueError, match="exact bounded integer"):
        project_uci_retail_rows([row(invoice="C536365", quantity=quantity)])


@pytest.mark.parametrize("invoice", ["", "X536365", "c536365", "=ABC", "C1", "123", True,
                                     536365.0, None, -1])
def test_invalid_invoice_format_does_not_get_treated_as_regular_sale(invoice):
    with pytest.raises(ValueError, match="invoice number") as caught:
        project_uci_retail_rows([row(invoice=invoice)])
    if str(invoice):
        assert str(invoice) not in str(caught.value)


@pytest.mark.parametrize("stock", ["", "=FORMULA", "SKU SPACE", None, True,
                                   12345, "X" * 33, "../unsafe"])
def test_invalid_stock_code_rejected_without_echoing_content(stock):
    with pytest.raises(ValueError, match="invalid product stock code") as caught:
        project_uci_retail_rows([row(code=stock)])
    assert "FORMULA" not in str(caught.value)


@pytest.mark.parametrize("when", ["2011-01-05", None,
                                 datetime(2011, 1, 5, tzinfo=UTC),
                                 True])
def test_event_datetime_is_not_an_authenticated_available_on_timestamp(when):
    with pytest.raises(ValueError, match="naive datetime"):
        project_uci_retail_rows([row(when=when)])


def test_missing_required_fields_refused_not_silently_filled():
    payload = row()
    del payload["Quantity"]
    with pytest.raises(ValueError, match="required transaction fields"):
        project_uci_retail_rows([payload])
    with pytest.raises(ValueError, match="required transaction fields"):
        project_uci_retail_rows([["536365", "SKU-A", 1, "2011-01-05"]])


def test_customer_columns_are_not_accessed_or_serialized():
    class DoNotInspect:
        def __str__(self):
            raise AssertionError("customer identifier was formatted")

        def __repr__(self):
            raise AssertionError("customer identifier was represented")

    result = project_uci_retail_rows([
        row(
            CustomerID=DoNotInspect(),
            Description=DoNotInspect(),
            Country=DoNotInspect(),
            UnitPrice=DoNotInspect(),
            InvoiceNo="536365",
        )
    ])
    assert "CustomerID" not in str(result)
    assert "InvoiceNo" not in str(result)
    assert "available_on" not in str(result)
    assert "536365" not in str(result)


def test_duplicate_identical_invoice_lines_are_not_silently_deduplicated():
    duplicated = row("536365", quantity=2)
    result = project_uci_retail_rows([duplicated, dict(duplicated)])
    assert result.days[0].units == 4
    assert result.receipt()["accepted_rows"] == 2
    # The source has no line identifier; duplicates may be errors OR valid repeated lines.


def test_input_must_be_iterable():
    with pytest.raises(TypeError, match="iterable"):
        project_uci_retail_rows(42)
