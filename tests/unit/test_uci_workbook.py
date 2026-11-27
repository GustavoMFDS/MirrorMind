"""Synthetic XLSX workbook security and strict retail-schema regressions."""
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from io import BytesIO, StringIO
from string import ascii_letters
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from openpyxl import Workbook

from mirrormind.domains.retail.uci_transactions import MAX_SUPPORTED_ROWS
from mirrormind.domains.retail.uci_workbook import (
    MAX_SUPPORTED_ZIP_ENTRY_BYTES,
    MAX_SUPPORTED_ZIP_TOTAL_BYTES,
    MAX_ZIP_ENTRY_BYTES,
    MAX_ZIP_TOTAL_BYTES,
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


def with_shared_strings(raw):
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    type_ns = "http://schemas.openxmlformats.org/package/2006/content-types"
    ET.register_namespace("", main_ns)
    strings = []
    indexes = {}
    worksheet = ET.fromstring(
        ZipFile(BytesIO(raw)).read("xl/worksheets/sheet1.xml")
    )
    for cell in worksheet.findall(f".//{{{main_ns}}}c"):
        if cell.get("t") != "inlineStr":
            continue
        inline = cell.find(f"{{{main_ns}}}is")
        text = "".join(
            node.text or "" for node in inline.iter(f"{{{main_ns}}}t")
        )
        index = indexes.get(text)
        if index is None:
            index = len(strings)
            indexes[text] = index
            strings.append(text)
        cell.remove(inline)
        cell.set("t", "s")
        value = ET.SubElement(cell, f"{{{main_ns}}}v")
        value.text = str(index)

    shared = ET.Element(
        f"{{{main_ns}}}sst",
        {"count": str(len(strings)), "uniqueCount": str(len(strings))},
    )
    for text in strings:
        item = ET.SubElement(shared, f"{{{main_ns}}}si")
        node = ET.SubElement(item, f"{{{main_ns}}}t")
        node.text = text

    replacements = {
        "xl/worksheets/sheet1.xml": ET.tostring(worksheet, encoding="utf-8"),
        "xl/sharedStrings.xml": ET.tostring(shared, encoding="utf-8"),
    }
    source = ZipFile(BytesIO(raw))
    workbook_rels = ET.fromstring(source.read("xl/_rels/workbook.xml.rels"))
    shared_rel = ET.SubElement(workbook_rels, f"{{{rel_ns}}}Relationship")
    shared_rel.attrib.update({
        "Id": "rIdSharedStrings",
        "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings",
        "Target": "sharedStrings.xml",
    })
    replacements["xl/_rels/workbook.xml.rels"] = ET.tostring(
        workbook_rels, encoding="utf-8"
    )
    content_types = ET.fromstring(source.read("[Content_Types].xml"))
    override = ET.SubElement(content_types, f"{{{type_ns}}}Override")
    override.attrib.update({
        "PartName": "/xl/sharedStrings.xml",
        "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml",
    })
    replacements["[Content_Types].xml"] = ET.tostring(
        content_types, encoding="utf-8"
    )
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as destination:
        for item in source.infolist():
            if item.filename not in replacements:
                destination.writestr(item, source.read(item.filename))
        for name, content in replacements.items():
            destination.writestr(name, content)
    source.close()
    return output.getvalue()


def invoice(number="536365", stock="SKU-A", units=2, when=None, customer=17850):
    if when is None:
        when = datetime(2011, 1, 5, 12, 45)
    return [number, stock, "PRIVATE-DESCRIPTION", units, when, 9.99, customer, "UK"]


def stage(raw, **kwargs):
    return read_uci_workbook(
        BytesIO(raw), expected_sha256=sha256(raw).hexdigest(), **kwargs
    )


def edit_worksheet(raw, edit):
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    ET.register_namespace("", main_ns)
    source = ZipFile(BytesIO(raw))
    worksheet = ET.fromstring(source.read("xl/worksheets/sheet1.xml"))
    edit(worksheet, main_ns)
    output = BytesIO()
    with ZipFile(output, "w", ZIP_DEFLATED) as destination:
        for item in source.infolist():
            content = source.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                content = ET.tostring(worksheet, encoding="utf-8")
            destination.writestr(item, content)
    source.close()
    return output.getvalue()


def duplicate_cell(raw, coordinate, *, replacement_value=None):
    def edit(worksheet, namespace):
        cell = worksheet.find(f".//{{{namespace}}}c[@r='{coordinate}']")
        assert cell is not None
        row_number = "".join(character for character in coordinate if character.isdigit())
        row = worksheet.find(f".//{{{namespace}}}row[@r='{row_number}']")
        assert row is not None
        duplicate = deepcopy(cell)
        if replacement_value is not None:
            value = duplicate.find(f"{{{namespace}}}v")
            assert value is not None
            value.text = replacement_value
        row.append(duplicate)

    return edit_worksheet(raw, edit)


def replace_cell_value(raw, coordinate, *, cell_type, value):
    def edit(worksheet, namespace):
        cell = worksheet.find(f".//{{{namespace}}}c[@r='{coordinate}']")
        assert cell is not None
        cell.clear()
        cell.attrib.update({"r": coordinate, "t": cell_type})
        value_element = ET.SubElement(cell, f"{{{namespace}}}v")
        value_element.text = value

    return edit_worksheet(raw, edit)


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


def test_description_shared_string_is_not_extracted_for_projection(monkeypatch):
    from xml.parsers import expat

    import mirrormind.domains.retail.uci_xlsx_xml as xlsx_xml
    from mirrormind.domains.retail.uci_xlsx_xml import (
        _iter_worksheet_rows,
        _read_required_shared_strings,
        _resolve_worksheet,
        _selected_shared_string_indices,
    )

    marker = "PRIVATE-DESCRIPTION-MUST-NOT-BE-LOADED"
    row = invoice(stock="SKU-A")
    row[2] = marker
    raw = with_shared_strings(fictional_workbook(row))

    parsers = []

    class TrackingParser:
        def __init__(self):
            object.__setattr__(self, "_parser", expat.ParserCreate(namespace_separator="}"))
            object.__setattr__(self, "_character_handler", None)
            object.__setattr__(self, "character_chunks", [])

        def __getattr__(self, name):
            return getattr(self._parser, name)

        def __setattr__(self, name, value):
            if name == "CharacterDataHandler":
                object.__setattr__(self, "_character_handler", value)
                self._parser.CharacterDataHandler = (
                    self._capture if value is not None else None
                )
            else:
                setattr(self._parser, name, value)

        def _capture(self, value):
            self.character_chunks.append(value)
            self._character_handler(value)

    def tracking_parser():
        parser = TrackingParser()
        parsers.append(parser)
        return parser

    monkeypatch.setattr(xlsx_xml, "_new_xml_parser", tracking_parser)

    with ZipFile(BytesIO(raw)) as archive:
        worksheet_path, _ = _resolve_worksheet(archive, "Online Retail")
        shared_xml = archive.read("xl/sharedStrings.xml")
        required = _selected_shared_string_indices(
            archive, worksheet_path, max_rows=100
        )
        selected = _read_required_shared_strings(archive, required)
        parsed_rows = list(_iter_worksheet_rows(
            archive, worksheet_path, max_rows=100,
            collect_shared_references=False,
        ))

    assert set(parsed_rows[1][1]) == {1, 2, 4, 5}
    assert marker.encode() in shared_xml
    assert marker not in str(parsed_rows[1][1])
    assert marker not in selected.values()
    assert marker not in "".join(
        chunk for parser in parsers for chunk in parser.character_chunks
    )
    assert marker not in str(stage(raw))


def test_duplicate_quantity_cell_is_rejected_instead_of_overwriting_original():
    raw = duplicate_cell(
        fictional_workbook(invoice("536365", "SKU-A", 2)),
        "D2",
        replacement_value="99",
    )

    with pytest.raises(ValueError, match="duplicate workbook cell coordinate"):
        stage(raw)


@pytest.mark.parametrize("coordinate", ["A1", "B2", "C2"])
@pytest.mark.parametrize("collect_shared_references", [True, False])
def test_duplicate_header_selected_and_excluded_cells_fail_in_both_passes(
    coordinate, collect_shared_references
):
    from mirrormind.domains.retail.uci_xlsx_xml import (
        _iter_worksheet_rows,
        _resolve_worksheet,
    )

    raw = duplicate_cell(fictional_workbook(invoice()), coordinate)

    with ZipFile(BytesIO(raw)) as archive:
        worksheet_path, _ = _resolve_worksheet(archive, "Online Retail")
        with pytest.raises(ValueError, match="duplicate workbook cell coordinate"):
            list(_iter_worksheet_rows(
                archive,
                worksheet_path,
                max_rows=100,
                collect_shared_references=collect_shared_references,
            ))


@pytest.mark.parametrize(
    ("coordinate", "cell_type", "value"),
    [
        ("A2", "e", "536365"),
        ("B2", "e", "SKU-ERROR"),
        ("B2", "future-type", "SKU-UNKNOWN"),
    ],
)
def test_error_and_unknown_selected_cell_types_fail_without_echo(
    coordinate, cell_type, value
):
    raw = replace_cell_value(
        fictional_workbook(invoice()),
        coordinate,
        cell_type=cell_type,
        value=value,
    )

    with pytest.raises(
        ValueError, match="unsupported selected workbook cell type"
    ) as caught:
        stage(raw)

    assert value not in str(caught.value)


@pytest.mark.parametrize("value", ["SKU-X", "12_345", "1e999", "1e-999"])
def test_malformed_numeric_cell_encodings_fail_without_becoming_stock_codes(value):
    raw = replace_cell_value(
        fictional_workbook(invoice()),
        "B2",
        cell_type="n",
        value=value,
    )

    with pytest.raises(ValueError, match="invalid numeric workbook cell") as caught:
        stage(raw)

    assert value not in str(caught.value)


def test_uci_non_c_alpha_invoice_prefixes_are_counted_and_excluded():
    raw = fictional_workbook(
        invoice(536365, "SKU-A", 2),
        invoice("C536366", "SKU-A", 3),
        invoice("c536367", "SKU-A", 5),
        invoice("A123456", "SKU-A", 7),
    )

    result = stage(raw)

    assert result.projection.processed_rows == 4
    assert result.projection.accepted_rows == 1
    assert result.projection.cancelled_rows == 1
    assert result.receipt()["unverified_invoice_prefix_rows"] == 2
    assert len(result.projection.days) == 1
    assert result.projection.days[0].units == 2
    assert "A123456" not in str(result)
    assert "C536366" not in str(result)
    assert "c536367" not in str(result)


def test_all_single_ascii_letter_prefixes_have_one_aggregate_exclusion_class():
    invoice_numbers = [f"{prefix}123456" for prefix in ascii_letters]
    raw = fictional_workbook(*(
        invoice(invoice_number, "SKU-A", 1)
        for invoice_number in invoice_numbers
    ))

    result = stage(raw)
    receipt = result.receipt()

    assert result.projection.processed_rows == len(ascii_letters)
    assert result.projection.accepted_rows == 0
    assert result.projection.cancelled_rows == 1
    assert receipt["unverified_invoice_prefix_rows"] == len(ascii_letters) - 1
    assert not result.projection.days
    assert sum(key.startswith("unverified_invoice_prefix") for key in receipt) == 1
    assert all(invoice_number not in str(result) for invoice_number in invoice_numbers)


@pytest.mark.parametrize(
    "invoice_number",
    ["AB123456", "X12345", "12345", "1234567", "é123456", "_123456"],
)
def test_uci_invoice_formats_outside_scoped_classes_fail_without_echo(
    invoice_number,
):
    raw = fictional_workbook(invoice(invoice_number, "SKU-A", 1))

    with pytest.raises(ValueError, match="invoice number") as caught:
        stage(raw)

    assert invoice_number not in str(caught.value)


def test_numeric_and_textual_five_digit_stock_codes_share_one_exact_group():
    raw = fictional_workbook(
        invoice("536365", 12345, 2),
        invoice("536366", "12345", 3),
    )

    result = stage(raw)

    assert len(result.projection.days) == 1
    assert result.projection.days[0].stock_code == "12345"
    assert result.projection.days[0].units == 5
    assert "12345" not in str(result.receipt())


def test_internal_ascii_spaces_are_preserved_as_distinct_stock_code_keys():
    raw = fictional_workbook(
        invoice("536365", "SKU A", 2),
        invoice("536366", "SKUA", 3),
        invoice("536367", "SKU  A", 4),
    )

    result = stage(raw)

    assert {item.stock_code: item.units for item in result.projection.days} == {
        "SKU A": 2,
        "SKUA": 3,
        "SKU  A": 4,
    }
    assert "SKU A" not in str(result.receipt())


def test_reordered_or_added_header_fails_closed():
    rows = [invoice()]
    with pytest.raises(ValueError, match="header layout"):
        stage(fictional_workbook(*rows, header=(*UCI_HEADER[:-1], "Unreviewed")))
    with pytest.raises(ValueError, match="sheet layout"):
        stage(fictional_workbook(*rows, extra_sheet=True))


def test_malformed_required_excel_cell_rejected_without_echoing_value():
    bad = invoice()
    bad[3] = "PRIVATE_BAD_QUANTITY"
    with pytest.raises(
        ValueError, match="unsupported selected workbook cell type"
    ) as caught:
        stage(fictional_workbook(bad))
    assert "PRIVATE_BAD_QUANTITY" not in str(caught.value)


@pytest.mark.parametrize(
    ("stock_code", "message"),
    [
        (1234, "invalid product stock code"),
        (123456, "invalid product stock code"),
        (True, "unsupported selected workbook cell type"),
        (" SKU-A", "invalid product stock code"),
        ("SKU-A ", "invalid product stock code"),
        ("SKU\tA", "invalid product stock code"),
        ("SKU\nA", "invalid product stock code"),
    ],
)
def test_unsupported_stock_code_encoding_fails_without_echoing_value(
    stock_code, message
):
    with pytest.raises(ValueError, match=message) as caught:
        stage(fictional_workbook(invoice(stock=stock_code)))
    assert str(stock_code) not in str(caught.value)


def test_workbook_stock_code_normalizer_rejects_float_cells():
    from mirrormind.domains.retail.uci_workbook import _normalize_workbook_stock_code

    with pytest.raises(ValueError, match="invalid product stock code"):
        _normalize_workbook_stock_code(12345.0)


def test_required_formula_cell_is_not_evaluated_or_treated_as_observation():
    bad = invoice()
    bad[3] = "=2+3"
    with pytest.raises(ValueError, match="unsupported formula cell"):
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
    with pytest.raises(ValueError, match="compression ratio exceeds budget"):
        stage(
            buffer.getvalue(),
            max_zip_entry_bytes=MAX_SUPPORTED_ZIP_ENTRY_BYTES,
            max_zip_total_bytes=MAX_SUPPORTED_ZIP_TOTAL_BYTES,
        )


def test_explicit_zip_entry_budget_rejects_before_workbook_processing():
    raw = fictional_workbook(invoice())
    with pytest.raises(ValueError, match="entry exceeds byte budget"):
        stage(raw, max_zip_entry_bytes=1)


def test_zip_expansion_profile_is_explicit_bounded_and_defaults_stay_unchanged():
    from zipfile import ZipFile

    raw = fictional_workbook(invoice())
    with ZipFile(BytesIO(raw)) as archive:
        members = archive.infolist()
    largest_member = max(item.file_size for item in members)
    total_uncompressed = sum(item.file_size for item in members)

    assert MAX_ZIP_ENTRY_BYTES == 64 * 1024 * 1024
    assert MAX_ZIP_TOTAL_BYTES == 128 * 1024 * 1024
    assert MAX_SUPPORTED_ZIP_ENTRY_BYTES == 192 * 1024 * 1024
    assert MAX_SUPPORTED_ZIP_TOTAL_BYTES == 224 * 1024 * 1024
    assert stage(raw).projection.accepted_rows == 1
    assert stage(
        raw,
        max_zip_entry_bytes=MAX_SUPPORTED_ZIP_ENTRY_BYTES,
        max_zip_total_bytes=MAX_SUPPORTED_ZIP_TOTAL_BYTES,
    ).projection.accepted_rows == 1
    with pytest.raises(ValueError, match="uncompressed size exceeds budget"):
        stage(
            raw, max_zip_entry_bytes=largest_member,
            max_zip_total_bytes=total_uncompressed - 1,
        )


@pytest.mark.parametrize(
    ("entry_limit", "total_limit"),
    [
        (True, 224 * 1024 * 1024),
        (192 * 1024 * 1024, True),
        (0, 1),
        (192 * 1024 * 1024 + 1, 224 * 1024 * 1024),
        (192 * 1024 * 1024, 224 * 1024 * 1024 + 1),
        (224 * 1024 * 1024, 192 * 1024 * 1024),
    ],
)
def test_zip_expansion_budgets_must_be_exact_bounded_and_consistent(
    entry_limit, total_limit
):
    stream = BytesIO(b"DO-NOT-READ")
    with pytest.raises(ValueError, match="bounded workbook ZIP"):
        read_uci_workbook(
            stream, expected_sha256="0" * 64,
            max_zip_entry_bytes=entry_limit,
            max_zip_total_bytes=total_limit,
        )
    assert stream.tell() == 0


def test_uci_workbook_group_override_is_bounded_and_keeps_generic_projection_cap():
    from mirrormind.domains.retail.uci_transactions import (
        MAX_SUPPORTED_GROUPS,
        MAX_SUPPORTED_UCI_WORKBOOK_GROUPS,
        project_uci_retail_rows,
    )

    assert MAX_SUPPORTED_GROUPS == 100_000
    assert MAX_SUPPORTED_UCI_WORKBOOK_GROUPS == 250_000
    with pytest.raises(ValueError, match="max_groups"):
        project_uci_retail_rows([{
            "InvoiceNo": "536365", "StockCode": "SKU-A", "Quantity": 1,
            "InvoiceDate": datetime(2011, 1, 5),
        }], max_groups=MAX_SUPPORTED_UCI_WORKBOOK_GROUPS)

    raw = fictional_workbook(invoice())
    result = stage(raw, max_groups=MAX_SUPPORTED_UCI_WORKBOOK_GROUPS)
    assert result.projection.accepted_rows == 1

    stream = BytesIO(raw)
    with pytest.raises(ValueError, match="bounded workbook group limit"):
        read_uci_workbook(
            stream, expected_sha256=sha256(raw).hexdigest(),
            max_groups=MAX_SUPPORTED_UCI_WORKBOOK_GROUPS + 1,
        )
    assert stream.tell() == 0


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
