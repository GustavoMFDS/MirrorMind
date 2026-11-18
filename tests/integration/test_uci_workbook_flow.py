"""Invented local workbook -> private projection, without real dataset access."""
from datetime import datetime
from hashlib import sha256

import pytest
from openpyxl import Workbook

from mirrormind.domains.retail.uci_workbook import UCI_HEADER, read_uci_workbook
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot


def test_synthetic_local_xlsx_file_to_product_day_projection(tmp_path):
    path = tmp_path / "invented-uci-shaped.xlsx"
    book = Workbook()
    worksheet = book.active
    worksheet.title = "Online Retail"
    worksheet.append(list(UCI_HEADER))
    worksheet.append([
        "536365", "SKU-A", "PRIVATE DESCRIPTOR", 3,
        datetime(2011, 1, 5, 9), 2.9, 12345, "fictional",
    ])
    worksheet.append([
        "C536366", "SKU-A", "PRIVATE DESCRIPTOR", -1,
        datetime(2011, 1, 6, 10), 2.9, 12345, "fictional",
    ])
    worksheet.append([
        "536367", "SKU-A", "PRIVATE DESCRIPTOR", 7,
        datetime(2011, 1, 7, 17), 2.9, 67890, "fictional",
    ])
    book.save(path)
    book.close()

    expected = sha256(path.read_bytes()).hexdigest()
    with path.open("rb") as file:
        processed = read_uci_workbook(file, expected_sha256=expected)
    assert processed.sha256_hex == expected
    assert processed.receipt()["status"] == "uci_xlsx_projection_not_authorized"
    assert processed.receipt()["publication_time_status"] == (
        "unknown_not_derived_from_invoice_date"
    )
    assert processed.receipt()["processed_rows"] == 3
    assert processed.receipt()["accepted_rows"] == 2
    assert processed.receipt()["cancelled_rows"] == 1
    assert [
        (x.stock_code, x.observed_on.isoformat(), x.units)
        for x in processed.projection.days
    ] == [("SKU-A", "2011-01-05", 3), ("SKU-A", "2011-01-07", 7)]
    assert not hasattr(processed.projection.days[0], "available_on")

    # A workbook event date cannot be passed as an authenticated publication
    # timestamp to the old as-of staging/forecasting pipeline.
    with pytest.raises(ValueError, match="bytes must be bounded"):
        stage_csv_snapshot(processed.projection.days, expected_sha256="0" * 64)

    for forbidden in ("PRIVATE DESCRIPTOR", "12345", "67890", "536365"):
        assert forbidden not in str(processed.receipt())
        assert forbidden not in str(processed)
