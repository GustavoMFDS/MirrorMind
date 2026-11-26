"""Synthetic XLSX workbook security and strict retail-schema regressions."""
from datetime import datetime
from hashlib import sha256
from io import BytesIO, StringIO
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from openpyxl import Workbook

from mirrormind.domains.retail.uci_transactions import MAX_SUPPORTED_ROWS
from mirrormind.domains.retail.uci_workbook import (
    UCI_HEADER,
    read_uci_workbook,
)


def fictional_workbook(*rows, header=UCI_HEADER, extra_sheet=False):
    book = Workbook()
    sheet = book.active
    sheet.title = "Online Retail"
    sheet.append(list(header))
    for row in rows:
        sheet.append(row)
    if extra_sheet:
        book.create_sheet("Unreviewed Sheet")
    buffer = BytesIO()
    book.save(buffer)
    book.close()
    return buffer.getvalue()


def invoice(number="536365", stock="SKU-A", units=2, when=None, customer=17850):
    if when is None:
        when = datetime(2011, 1, 5, 12, 45)
    return [number, stock, "PRIVATE-DESCRIPTION", units, when, 9.99, customer, "UK"]


def stage(raw, **kwargs):
    return read_uci_workbook(
        BytesIO(raw), expected_sha256=sha256(raw).hexdigest(), **kwargs
    )


def test_xlsx_stage_projects_positive_units_and_never_copies_sensitive_values():
    raw = fictional_workbook(
        invoice("536365", "SKU-A", 2, customer=12345),
        invoice(536366, "SKU-A", 3, when=datetime(2011, 1, 5, 17), customer=98765),
        invoice("C536367", "SKU-A", -1, customer=11111),
        invoice("536368", "SKU-B", 0, customer=22222),
        invoice("536369", "SKU-A", -3, customer=33333),
    )
    result = stage(raw)
    assert result.projection.receipt()["accepted_rows"] == 2
    assert result.projection.receipt()["cancelled_rows"] == 1
    assert result.projection.receipt()["negative_quantity_rows"] == 1
    assert result.projection.receipt()["zero_quantity_rows"] == 1
    assert len(result.projection.days) == 1
    assert result.projection.days[0].units == 5
    assert result.projection.days[0].observed_on.isoformat() == "2011-01-05"
    receipt = result.receipt()
    assert receipt["status"] == "uci_xlsx_projection_not_authorized"
    assert receipt["publication_time_status"] == "unknown_not_derived_from_invoice_date"
    assert receipt["workbook_sha256"] == sha256(raw).hexdigest()
    assert not hasattr(result.projection.days[0], "available_on")
    for secret in ("PRIVATE-DESCRIPTION", "12345", "98765", "536365"):
        assert secret not in str(receipt)
        assert secret not in str(result)


def test_reordered_or_added_header_fails_closed():
    rows = [invoice()]
    with pytest.raises(ValueError, match="header layout"):
        stage(fictional_workbook(*rows, header=(*UCI_HEADER[:-1], "Unreviewed")))
    with pytest.raises(ValueError, match="sheet layout"):
        stage(fictional_workbook(*rows, extra_sheet=True))


def test_malformed_required_excel_cell_rejected_without_echoing_value():
    bad = invoice()
    bad[3] = "PRIVATE_BAD_QUANTITY"
    with pytest.raises(ValueError, match="exact bounded integer") as caught:
        stage(fictional_workbook(bad))
    assert "PRIVATE_BAD_QUANTITY" not in str(caught.value)


def test_required_formula_cell_is_not_evaluated_or_treated_as_observation():
    bad = invoice()
    bad[3] = "=2+3"
    with pytest.raises(ValueError, match="exact bounded integer"):
        stage(fictional_workbook(bad))


def test_wrong_digest_detected_before_xlsx_parser():
    raw = fictional_workbook(invoice())
    with pytest.raises(ValueError, match="do not match"):
        read_uci_workbook(BytesIO(raw), expected_sha256="0" * 64)
    with pytest.raises(ValueError, match="SHA-256"):
        read_uci_workbook(BytesIO(raw), expected_sha256="not-a-digest")


def test_invalid_zip_rejected_with_generic_error():
    raw = b"not-an-xlsx-but-with-hash"
    with pytest.raises(ValueError, match="invalid ZIP workbook"):
        stage(raw)


def test_unsupported_zip_external_link_rejected_before_processing():
    original = fictional_workbook(invoice())
    buffer = BytesIO(original)
    with ZipFile(buffer, "a") as archive:
        archive.writestr("xl/externalLinks/externalLink1.xml", "SHOULD-NOT-BE-PARSED")
    with pytest.raises(ValueError, match="unsupported archive features"):
        stage(buffer.getvalue())


def test_zip_compression_ratio_bomb_header_rejected():
    original = fictional_workbook(invoice())
    buffer = BytesIO(original)
    with ZipFile(buffer, "a") as archive:
        archive.writestr(
            "xl/surprise.xml", b"x" * 250_000, compress_type=ZIP_DEFLATED
        )
    with pytest.raises(ValueError, match="compression ratio exceeds budget"):
        stage(buffer.getvalue())


def test_oversized_uncompressed_member_budget_rejected(monkeypatch):
    import mirrormind.domains.retail.uci_workbook as mod

    raw = fictional_workbook(invoice())
    monkeypatch.setattr(mod, "MAX_ZIP_ENTRY_BYTES", 100)
    with pytest.raises(ValueError, match="entry exceeds byte budget"):
        stage(raw)


def test_bounded_row_and_group_limits_do_not_truncate():
    raw = fictional_workbook(invoice("536365", "SKU-A"), invoice("536366", "SKU-B"))
    with pytest.raises(ValueError, match="row count"):
        stage(raw, max_rows=1)
    with pytest.raises(ValueError, match="group count"):
        stage(raw, max_groups=1)


def test_zero_transaction_workbook_abstains():
    raw = fictional_workbook()
    with pytest.raises(ValueError, match="at least one row"):
        stage(raw)


def test_reader_rejects_oversized_compressed_bytes_without_consuming_tail(monkeypatch):
    import mirrormind.domains.retail.uci_workbook as mod

    monkeypatch.setattr(mod, "MAX_WORKBOOK_BYTES", 100)
    stream = BytesIO(b"X" * 500)
    with pytest.raises(ValueError, match="exceeds local size limit"):
        read_uci_workbook(stream, expected_sha256="0" * 64)
    assert stream.tell() == 101


def test_partial_reads_finish_through_true_eof_and_retain_full_digest():
    raw = fictional_workbook(invoice())

    class ShortRead:
        def __init__(self):
            self.stream = BytesIO(raw)
            self.reads = 0

        def read(self, size):
            self.reads += 1
            return self.stream.read(min(size, 13))

    stream = ShortRead()
    result = read_uci_workbook(stream, expected_sha256=sha256(raw).hexdigest())
    assert stream.reads > 20
    assert result.receipt()["accepted_rows"] == 1


def test_text_stream_and_missing_read_method_fail():
    with pytest.raises(TypeError, match="binary workbook stream"):
        read_uci_workbook(None, expected_sha256="0" * 64)
    with pytest.raises(ValueError, match="yield bytes"):
        read_uci_workbook(StringIO("fake"), expected_sha256="0" * 64)


def test_stream_os_error_message_does_not_expose_source_location():
    class ErrorReader:
        def read(self, size):
            raise OSError("secret-home-or-user-file-path")

    with pytest.raises(ValueError, match="failed to read workbook stream") as caught:
        read_uci_workbook(ErrorReader(), expected_sha256="0" * 64)
    assert "secret-home" not in str(caught.value)


@pytest.mark.parametrize("rows", [0, True, -1, MAX_SUPPORTED_ROWS + 1, "100", 1.5])
def test_invalid_row_budget_rejected_before_stream_read(rows):
    with pytest.raises(ValueError, match="bounded workbook row limit"):
        read_uci_workbook(BytesIO(b"DO-NOT-READ"), expected_sha256="0" * 64, max_rows=rows)


def test_reader_accepts_explicit_large_source_cap_without_changing_defaults():
    raw = fictional_workbook(invoice())
    result = stage(raw, max_rows=MAX_SUPPORTED_ROWS, max_groups=100_000)

    assert result.projection.processed_rows == 1


def test_unsupported_sheet_selection_rejected_before_stream_read():
    with pytest.raises(ValueError, match="sheet selection"):
        read_uci_workbook(
            BytesIO(b"DO-NOT-READ"), expected_sha256="0" * 64,
            sheet_name="Any Other Sheet"
        )
