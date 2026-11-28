"""Selectively stream the narrow OOXML subset used by the UCI workbook.

The worksheet's Description column is deliberately not delivered to Python
character handlers or materialized as a cell value. Expat still parses the
worksheet stream to validate structure and advance between cells.
"""
from __future__ import annotations

import re
from collections import deque
from collections.abc import Iterator
from datetime import datetime
from decimal import Decimal, DecimalException
from math import isfinite
from xml.parsers import expat
from zipfile import ZipFile

_MAX_METADATA_BYTES = 4 * 1024 * 1024
_MAX_SELECTED_STRING_CHARS = 256
_MAX_SELECTED_SHARED_STRING_BYTES = 32 * 1024 * 1024
_MAX_SELECTED_STRING_REFERENCES = 2_400_008
_MAX_XLSX_ROW = 1_048_576
_MAX_XLSX_COLUMN = 16_384
_MAX_SCHEMA_COLUMN = 8
_HEADER_COLUMNS = frozenset(range(1, _MAX_SCHEMA_COLUMN + 1))
_PROJECTION_COLUMNS = frozenset({1, 2, 4, 5})
_CELL_REFERENCE = re.compile(r"([A-Z]{1,3})([1-9][0-9]{0,6})")
_NUMERIC_CELL_VALUE = re.compile(
    r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[Ee][+-]?[0-9]+)?"
)
_HEADER_CELL_TYPES = frozenset({"inlineStr", "s", "str"})
# OOXML types accepted for projection columns A, B, D and E, respectively.
_DATA_CELL_TYPES = {
    1: frozenset({"", "inlineStr", "n", "s", "str"}),
    2: frozenset({"", "inlineStr", "n", "s", "str"}),
    4: frozenset({"", "n"}),
    5: frozenset({"", "d", "n"}),
}


def _local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def _reject_xml_feature(*_args: object) -> None:
    raise ValueError("unsupported XML features")


def _new_xml_parser() -> expat.XMLParserType:
    parser = expat.ParserCreate(namespace_separator="}")
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    parser.StartDoctypeDeclHandler = _reject_xml_feature
    parser.EntityDeclHandler = _reject_xml_feature
    parser.ExternalEntityRefHandler = lambda *_args: 0
    return parser


def _parse_small_xml_member(archive: ZipFile, name: str, start_handler) -> None:
    try:
        info = archive.getinfo(name)
    except KeyError:
        raise ValueError("workbook is missing a required OOXML part") from None
    if info.file_size > _MAX_METADATA_BYTES:
        raise ValueError("workbook OOXML metadata exceeds local budget")
    parser = _new_xml_parser()
    parser.StartElementHandler = start_handler
    try:
        with archive.open(info) as stream:
            parser.ParseFile(stream)
    except (expat.ExpatError, OSError, RuntimeError):
        raise ValueError("invalid or unsupported OOXML metadata") from None


def _resolve_worksheet(archive: ZipFile, sheet_name: str) -> tuple[str, bool]:
    """Resolve the one allowed sheet and the workbook's date-system flag."""
    sheets: list[tuple[str, str]] = []
    date_1904 = False

    def workbook_start(name: str, attributes: dict[str, str]) -> None:
        nonlocal date_1904
        element = _local_name(name)
        attrs = {_local_name(key): value for key, value in attributes.items()}
        if element == "sheet":
            sheets.append((attrs.get("name", ""), attrs.get("id", "")))
        elif element == "workbookPr":
            date_1904 = attrs.get("date1904", "0").lower() in {"1", "true"}

    _parse_small_xml_member(archive, "xl/workbook.xml", workbook_start)
    if len(sheets) != 1 or sheets[0][0] != sheet_name:
        raise ValueError("unsupported workbook sheet layout")
    relation_id = sheets[0][1]
    if not relation_id:
        raise ValueError("unsupported workbook sheet relationship")

    relationships: dict[str, tuple[str, str]] = {}

    def relationships_start(name: str, attributes: dict[str, str]) -> None:
        if _local_name(name) != "Relationship":
            return
        attrs = {_local_name(key): value for key, value in attributes.items()}
        rel_id = attrs.get("Id", "")
        if rel_id in relationships:
            raise ValueError("duplicate workbook relationship")
        relationships[rel_id] = (
            attrs.get("Target", ""), attrs.get("TargetMode", "")
        )

    _parse_small_xml_member(
        archive, "xl/_rels/workbook.xml.rels", relationships_start
    )
    target, target_mode = relationships.get(relation_id, ("", "External"))
    if target_mode or "\\" in target:
        raise ValueError("unsupported workbook sheet relationship")
    if target.startswith("/xl/"):
        target = target[1:]
    elif target.startswith("/"):
        raise ValueError("unsupported workbook sheet relationship")
    parts = target.split("/")
    if target.startswith("xl/"):
        parts = target.split("/")
        if len(parts) != 3 or parts[:2] != ["xl", "worksheets"]:
            raise ValueError("unsupported workbook sheet relationship")
        worksheet_path = target
    elif len(parts) == 2 and parts[0] == "worksheets":
        worksheet_path = f"xl/{target}"
    else:
        raise ValueError("unsupported workbook sheet relationship")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("unsupported workbook sheet relationship")
    if worksheet_path not in archive.namelist():
        raise ValueError("workbook is missing its worksheet part")
    return worksheet_path, date_1904


def _date_style_ids(archive: ZipFile) -> frozenset[int]:
    """Return style indexes whose number formats represent Excel dates."""
    try:
        from openpyxl.styles.numbers import BUILTIN_FORMATS, is_date_format
    except ImportError:
        raise RuntimeError("optional XLSX support requires the uci extra") from None

    custom_formats: dict[int, str] = {}
    style_formats: list[int] = []
    in_cell_xfs = False

    def styles_start(name: str, attributes: dict[str, str]) -> None:
        nonlocal in_cell_xfs
        element = _local_name(name)
        attrs = {_local_name(key): value for key, value in attributes.items()}
        if element == "numFmt":
            try:
                custom_formats[int(attrs["numFmtId"])] = attrs["formatCode"]
            except (KeyError, ValueError):
                raise ValueError("invalid workbook number format") from None
        elif element == "cellXfs":
            in_cell_xfs = True
        elif element == "xf" and in_cell_xfs:
            try:
                style_formats.append(int(attrs.get("numFmtId", "0")))
            except ValueError:
                raise ValueError("invalid workbook cell style") from None

    def styles_end(name: str) -> None:
        nonlocal in_cell_xfs
        if _local_name(name) == "cellXfs":
            in_cell_xfs = False

    try:
        info = archive.getinfo("xl/styles.xml")
    except KeyError:
        return frozenset()
    if info.file_size > _MAX_METADATA_BYTES:
        raise ValueError("workbook OOXML metadata exceeds local budget")
    parser = _new_xml_parser()
    parser.StartElementHandler = styles_start
    parser.EndElementHandler = styles_end
    try:
        with archive.open(info) as stream:
            parser.ParseFile(stream)
    except (expat.ExpatError, OSError, RuntimeError):
        raise ValueError("invalid or unsupported workbook styles") from None

    result: set[int] = set()
    for style_id, num_format_id in enumerate(style_formats):
        code = custom_formats.get(num_format_id, BUILTIN_FORMATS.get(num_format_id))
        if code is not None and is_date_format(code):
            result.add(style_id)
    return frozenset(result)


def _column_and_row(reference: str) -> tuple[int, int]:
    match = _CELL_REFERENCE.fullmatch(reference)
    if match is None:
        raise ValueError("unsupported workbook cell reference")
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - ord("A") + 1
    row = int(match.group(2))
    if column > _MAX_XLSX_COLUMN or row > _MAX_XLSX_ROW:
        raise ValueError("unsupported workbook cell reference")
    return column, row


def _iter_worksheet_rows(
    archive: ZipFile,
    worksheet_path: str,
    *,
    max_rows: int,
    collect_shared_references: bool,
) -> Iterator[tuple[int, dict[int, dict[str, object]]]]:
    """Stream selected cells and reject duplicate coordinates or payloads."""
    queue: deque[tuple[int, dict[int, dict[str, object]]]] = deque()
    parser = _new_xml_parser()
    current_row_number: int | None = None
    last_row_number = 0
    row_cells: dict[int, dict[str, object]] = {}
    seen_cell_coordinates: set[tuple[int, int]] = set()
    current_cell: dict[str, object] | None = None
    current_column: int | None = None
    capture_kind: str | None = None
    capture_parts: list[str] = []
    phonetic_depth = 0

    def start(name: str, attributes: dict[str, str]) -> None:
        nonlocal current_row_number, row_cells, current_cell
        nonlocal current_column, capture_kind, capture_parts, phonetic_depth
        element = _local_name(name)
        attrs = {_local_name(key): value for key, value in attributes.items()}
        if element == "row":
            if current_row_number is not None:
                raise ValueError("nested workbook rows are unsupported")
            try:
                row_number = int(attrs["r"])
            except (KeyError, ValueError):
                raise ValueError("workbook rows require numeric indexes") from None
            if row_number != last_row_number + 1 or row_number > max_rows + 1:
                if row_number > max_rows + 1:
                    raise ValueError("row count exceeds local projection budget")
                raise ValueError("workbook rows must be consecutive")
            current_row_number = row_number
            row_cells = {}
            seen_cell_coordinates.clear()
        elif element == "c" and current_row_number is not None:
            if current_cell is not None:
                raise ValueError("nested workbook cells are unsupported")
            reference = attrs.get("r", "")
            column, cell_row = _column_and_row(reference)
            if cell_row != current_row_number or column > _MAX_SCHEMA_COLUMN:
                raise ValueError("workbook cell is outside the reviewed schema")
            coordinate = (cell_row, column)
            if coordinate in seen_cell_coordinates:
                raise ValueError("duplicate workbook cell coordinate")
            seen_cell_coordinates.add(coordinate)
            selected = (
                column in _HEADER_COLUMNS
                if current_row_number == 1
                else column in _PROJECTION_COLUMNS
            )
            current_column = column
            if selected:
                try:
                    style_id = int(attrs.get("s", "0"))
                except ValueError:
                    raise ValueError("invalid workbook cell style") from None
                current_cell = {
                    "type": attrs.get("t", "n"),
                    "style_id": style_id,
                    "formula": False,
                    "selected": True,
                    "scalar_value_count": 0,
                    "inline_payload_count": 0,
                    "in_inline_string": False,
                    "raw_parts": [],
                }
                parser.CharacterDataHandler = characters
            else:
                current_cell = {"selected": False}
                parser.CharacterDataHandler = None
            capture_kind = None
            capture_parts = []
        elif element == "f" and current_cell and current_cell.get("selected"):
            current_cell["formula"] = True
        elif element == "v" and current_cell and current_cell.get("selected"):
            if current_cell.get("inline_payload_count"):
                raise ValueError("ambiguous selected workbook cell payload")
            previous_count = current_cell.get("scalar_value_count", 0)
            assert type(previous_count) is int
            scalar_value_count = previous_count + 1
            if scalar_value_count > 1:
                raise ValueError("duplicate selected workbook scalar value")
            current_cell["scalar_value_count"] = scalar_value_count
            should_capture = (
                collect_shared_references
                and current_cell.get("type") == "s"
            ) or not collect_shared_references
            if should_capture:
                capture_kind = "v"
                capture_parts = []
        elif element == "is" and current_cell and current_cell.get("selected"):
            if current_cell.get("scalar_value_count"):
                raise ValueError("ambiguous selected workbook cell payload")
            if current_cell.get("inline_payload_count"):
                raise ValueError("duplicate selected inline string payload")
            current_cell["inline_payload_count"] = 1
            current_cell["in_inline_string"] = True
        elif (
            element == "t"
            and current_cell
            and current_cell.get("selected")
            and current_cell.get("type") == "inlineStr"
            and current_cell.get("in_inline_string")
            and phonetic_depth == 0
            and not collect_shared_references
        ):
            capture_kind = "t"
            capture_parts = []
        elif element == "rPh":
            phonetic_depth += 1

    def end(name: str) -> None:
        nonlocal current_row_number, last_row_number, row_cells, current_cell
        nonlocal current_column, capture_kind, capture_parts, phonetic_depth
        element = _local_name(name)
        if element == "v" and capture_kind == "v" and current_cell:
            current_cell["raw"] = "".join(capture_parts)
            capture_kind = None
            capture_parts = []
        elif element == "t" and capture_kind == "t" and current_cell:
            raw_parts = current_cell.setdefault("raw_parts", [])
            assert isinstance(raw_parts, list)
            raw_parts.extend(capture_parts)
            capture_kind = None
            capture_parts = []
        elif element == "is" and current_cell and current_cell.get("selected"):
            current_cell["in_inline_string"] = False
        elif element == "c" and current_cell is not None:
            if current_cell.get("selected") and current_column is not None:
                cell = dict(current_cell)
                raw_parts = cell.pop("raw_parts", [])
                if raw_parts:
                    assert isinstance(raw_parts, list)
                    cell["raw"] = "".join(raw_parts)
                if collect_shared_references:
                    if cell.get("type") == "s" and "raw" in cell:
                        row_cells[current_column] = cell
                else:
                    row_cells[current_column] = cell
            current_cell = None
            current_column = None
            capture_kind = None
            capture_parts = []
            parser.CharacterDataHandler = characters
        elif element == "rPh" and phonetic_depth:
            phonetic_depth -= 1
        elif element == "row" and current_row_number is not None:
            queue.append((current_row_number, row_cells))
            last_row_number = current_row_number
            current_row_number = None
            row_cells = {}

    def characters(value: str) -> None:
        if capture_kind is None:
            return
        capture_parts.append(value)
        if sum(map(len, capture_parts)) > _MAX_SELECTED_STRING_CHARS:
            raise ValueError("selected workbook cell exceeds text budget")

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = characters
    try:
        with archive.open(worksheet_path) as stream:
            while True:
                chunk = stream.read(65_536)
                parser.Parse(chunk, not chunk)
                while queue:
                    yield queue.popleft()
                if not chunk:
                    break
    except (expat.ExpatError, OSError, RuntimeError):
        raise ValueError("invalid or unsupported worksheet XML") from None
    while queue:
        yield queue.popleft()


def _selected_shared_string_indices(
    archive: ZipFile, worksheet_path: str, *, max_rows: int
) -> frozenset[int]:
    references: set[int] = set()
    for row_number, cells in _iter_worksheet_rows(
        archive, worksheet_path, max_rows=max_rows,
        collect_shared_references=True,
    ):
        for cell in cells.values():
            raw = cell.get("raw")
            if not isinstance(raw, str) or not raw.isdecimal() or len(raw) > 10:
                raise ValueError("invalid workbook shared-string reference")
            references.add(int(raw))
            if len(references) > _MAX_SELECTED_STRING_REFERENCES:
                raise ValueError("selected workbook string budget exceeded")
    return frozenset(references)


def _read_required_shared_strings(
    archive: ZipFile, required: frozenset[int]
) -> dict[int, str]:
    if not required:
        return {}
    try:
        info = archive.getinfo("xl/sharedStrings.xml")
    except KeyError:
        raise ValueError("workbook is missing referenced shared strings") from None

    parser = _new_xml_parser()
    current_index = -1
    capture = False
    in_phonetic = 0
    in_text = False
    parts: list[str] = []
    selected_chars = 0
    result: dict[int, str] = {}
    selected_bytes = 0

    def start(name: str, _attributes: dict[str, str]) -> None:
        nonlocal current_index, capture, in_phonetic, in_text, parts, selected_chars
        element = _local_name(name)
        if element == "si":
            current_index += 1
            capture = current_index in required
            parts = []
            selected_chars = 0
            parser.CharacterDataHandler = characters if capture else None
        elif element == "rPh":
            in_phonetic += 1
        elif element == "t" and capture and in_phonetic == 0:
            in_text = True

    def end(name: str) -> None:
        nonlocal capture, in_phonetic, in_text, selected_bytes, parts
        element = _local_name(name)
        if element == "t":
            in_text = False
        elif element == "rPh" and in_phonetic:
            in_phonetic -= 1
        elif element == "si":
            if capture:
                value = "".join(parts)
                if len(value) > _MAX_SELECTED_STRING_CHARS:
                    raise ValueError("selected workbook string exceeds text budget")
                selected_bytes += len(value.encode("utf-8"))
                if selected_bytes > _MAX_SELECTED_SHARED_STRING_BYTES:
                    raise ValueError("selected workbook strings exceed local budget")
                result[current_index] = value
            capture = False
            parts = []
            parser.CharacterDataHandler = characters

    def characters(value: str) -> None:
        nonlocal selected_chars
        if in_text:
            parts.append(value)
            selected_chars += len(value)
            if selected_chars > _MAX_SELECTED_STRING_CHARS:
                raise ValueError("selected workbook string exceeds text budget")

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = characters
    try:
        with archive.open(info) as stream:
            parser.ParseFile(stream)
    except (expat.ExpatError, OSError, RuntimeError):
        raise ValueError("invalid or unsupported shared strings") from None
    if result.keys() != required:
        raise ValueError("workbook references a missing shared string")
    return result


def _decode_cell(
    cell: dict[str, object] | None,
    *,
    column: int,
    shared_strings: dict[int, str],
    date_style_ids: frozenset[int],
    epoch: datetime,
    is_header: bool = False,
) -> object:
    """Decode one selected cell under the header or field-specific type contract."""
    if cell is None:
        return None
    if cell.get("formula"):
        raise ValueError("unsupported formula cell")
    cell_type = cell.get("type", "n")
    allowed_types = _HEADER_CELL_TYPES if is_header else _DATA_CELL_TYPES[column]
    if cell_type not in allowed_types:
        raise ValueError("unsupported selected workbook cell type")
    raw = cell.get("raw")
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise TypeError("invalid workbook cell value")
    if cell_type == "s":
        if not raw.isdecimal() or len(raw) > 10:
            raise ValueError("invalid workbook shared-string reference")
        try:
            return shared_strings[int(raw)]
        except KeyError:
            raise ValueError("workbook references an unselected shared string") from None
    if cell_type == "inlineStr" or cell_type == "str":
        return raw
    if cell_type == "d":
        try:
            from openpyxl.utils.datetime import from_ISO8601
            return from_ISO8601(raw)
        except (ImportError, ValueError):
            raise ValueError("invalid date workbook cell") from None
    if cell_type not in {"n", ""}:
        raise ValueError("unsupported selected workbook cell type")
    if not _NUMERIC_CELL_VALUE.fullmatch(raw):
        raise ValueError("invalid numeric workbook cell")
    try:
        exact_number = Decimal(raw)
        if not exact_number.is_finite():
            raise ValueError("invalid numeric workbook cell")
        if "." in raw or "E" in raw.upper():
            number = float(exact_number)
            if (
                not isfinite(number)
                or (exact_number != 0 and number == 0.0)
            ):
                raise ValueError("invalid numeric workbook cell")
        else:
            number = int(raw)
    except (DecimalException, OverflowError, ValueError):
        raise ValueError("invalid numeric workbook cell") from None
    style_id = cell.get("style_id", 0)
    if column == 5 and type(style_id) is not int:
        raise ValueError("invalid workbook cell style")
    if column == 5 and isinstance(style_id, int) and style_id in date_style_ids:
        try:
            from openpyxl.utils.datetime import from_excel
            return from_excel(number, epoch)
        except (ImportError, OverflowError, ValueError):
            return raw
    return number


def iter_uci_projection_rows(
    archive: ZipFile, *, sheet_name: str, max_rows: int,
    expected_header: tuple[str, ...],
) -> Iterator[dict[str, object]]:
    """Yield only approved projection fields; never materialize Description values."""
    try:
        from openpyxl.utils.datetime import MAC_EPOCH, WINDOWS_EPOCH
    except ImportError:
        raise RuntimeError("optional XLSX support requires the uci extra") from None

    worksheet_path, date_1904 = _resolve_worksheet(archive, sheet_name)
    epoch = MAC_EPOCH if date_1904 else WINDOWS_EPOCH
    date_styles = _date_style_ids(archive)
    needed_strings = _selected_shared_string_indices(
        archive, worksheet_path, max_rows=max_rows
    )
    shared_strings = _read_required_shared_strings(archive, needed_strings)
    rows = _iter_worksheet_rows(
        archive, worksheet_path, max_rows=max_rows,
        collect_shared_references=False,
    )
    header_row = next(rows, None)
    if header_row is None or header_row[0] != 1:
        raise ValueError("unsupported workbook header layout")
    header_cells = header_row[1]
    header = tuple(
        _decode_cell(
            header_cells.get(column), column=column,
            shared_strings=shared_strings, date_style_ids=date_styles,
            epoch=epoch, is_header=True,
        )
        for column in range(1, _MAX_SCHEMA_COLUMN + 1)
    )
    if header != expected_header:
        raise ValueError("unsupported workbook header layout")

    for row_number, cells in rows:
        if row_number <= 1:
            raise ValueError("workbook rows must follow the header")
        yield {
            "InvoiceNo": _decode_cell(
                cells.get(1), column=1, shared_strings=shared_strings,
                date_style_ids=date_styles, epoch=epoch,
            ),
            "StockCode": _decode_cell(
                cells.get(2), column=2, shared_strings=shared_strings,
                date_style_ids=date_styles, epoch=epoch,
            ),
            "Quantity": _decode_cell(
                cells.get(4), column=4, shared_strings=shared_strings,
                date_style_ids=date_styles, epoch=epoch,
            ),
            "InvoiceDate": _decode_cell(
                cells.get(5), column=5, shared_strings=shared_strings,
                date_style_ids=date_styles, epoch=epoch,
            ),
        }
