"""End-to-end offline retail projection on fictional transactions only."""
from datetime import datetime

import pytest

from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot


def test_retail_projection_preserves_unknown_release_time_and_cannot_be_staged_directly():
    fake = [
        {
            "InvoiceNo": "536365",
            "StockCode": "SKU-001",
            "Quantity": 2,
            "InvoiceDate": datetime(2011, 1, 5, 9, 10),
            "CustomerID": 17850,
            "Description": "FAKE ITEM",
            "UnitPrice": 2.55,
            "Country": "Fictional",
        },
        {
            "InvoiceNo": "536366",
            "StockCode": "SKU-001",
            "Quantity": 3,
            "InvoiceDate": datetime(2011, 1, 5, 17, 45),
            "CustomerID": 99999,
        },
        {
            "InvoiceNo": "C536367",
            "StockCode": "SKU-001",
            "Quantity": -1,
            "InvoiceDate": datetime(2011, 1, 6, 10),
            "CustomerID": 45678,
        },
        {
            "InvoiceNo": "536368",
            "StockCode": "SKU-001",
            "Quantity": 4,
            "InvoiceDate": datetime(2011, 1, 7, 10),
            "CustomerID": 12345,
        },
    ]
    projected = project_uci_retail_rows(iter(fake))
    assert projected.receipt()["accepted_rows"] == 3
    assert projected.receipt()["cancelled_rows"] == 1
    assert projected.receipt()["product_day_groups"] == 2
    assert [(x.observed_on.isoformat(), x.units) for x in projected.days] == [
        ("2011-01-05", 5), ("2011-01-07", 4)
    ]
    assert projected.receipt()["publication_time_status"] == (
        "unknown_not_derived_from_invoice_date"
    )
    assert not hasattr(projected.days[0], "available_on")
    # Stage requires a real, reviewed availability timestamp; the
    # projection refuses to invent one merely to fit the downstream schema.
    with pytest.raises(ValueError, match="bytes must be bounded"):
        stage_csv_snapshot(projected.days, expected_sha256="0" * 64)
    report_text = str(projected)
    assert "17850" not in report_text
    assert "99999" not in report_text
    assert "536365" not in report_text
    assert "FAKE ITEM" not in report_text


def test_permitted_processing_cannot_be_inferred_from_successful_offline_projection():
    projected = project_uci_retail_rows([{
        "InvoiceNo": "536365",
        "StockCode": "SKU-001",
        "Quantity": 1,
        "InvoiceDate": datetime(2011, 1, 5),
    }])
    assert projected.receipt()["status"] == "uci_shaped_projection_not_authorized"
    assert "license" not in projected.receipt()
    assert "customer" not in str(projected.receipt()).lower()
