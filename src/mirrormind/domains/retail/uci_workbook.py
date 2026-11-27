"""Bounded optional reader for the approved UCI-shaped OOXML subset.

Parsing grants no source permission. Only approved projection columns are
materialized; descriptions, customer identifiers and other excluded values
remain outside the in-memory result.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
from io import BytesIO
from typing import BinaryIO
from zipfile import BadZipFile, ZipFile

from mirrormind.domains.retail.uci_transactions import (
    _UCI_UNVERIFIED_INVOICE_PREFIX,
    MAX_GROUPS,
    MAX_ROWS,
    MAX_SUPPORTED_ROWS,
    MAX_SUPPORTED_UCI_WORKBOOK_GROUPS,
    UciRetailProjection,
    _project_uci_retail_rows,
    is_valid_uci_stock_code,
)

MAX_WORKBOOK_BYTES = 32 * 1024 * 1024
MAX_ZIP_MEMBERS = 256
MAX_ZIP_ENTRY_BYTES = 64 * 1024 * 1024
MAX_ZIP_TOTAL_BYTES = 128 * 1024 * 1024
MAX_SUPPORTED_ZIP_ENTRY_BYTES = 192 * 1024 * 1024
MAX_SUPPORTED_ZIP_TOTAL_BYTES = 224 * 1024 * 1024
MAX_ZIP_COMPRESSION_RATIO = 200
UCI_HEADER = (
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
)
FORBIDDEN_PARTS = (
    "xl/externallinks/", "xl/vbaproject", "xl/activex/",
    "xl/embeddings/", "xl/oleobjects/", "xl/connections.xml",
    "xl/querytables/",
)


@dataclass(frozen=True, slots=True)
class UciWorkbookReadResult:
    """Local digest-coupled product-day projection without source approval."""

    sha256_hex: str
    projection: UciRetailProjection

    def receipt(self) -> dict[str, str | int]:
        """Summarize input identity and exclusions, not raw customer or invoice data."""
        return {
            **self.projection.receipt(),
            "status": "uci_xlsx_projection_not_authorized",
            "workbook_sha256": self.sha256_hex,
            "unverified_invoice_prefix_rows": (
                self.projection.unverified_invoice_prefix_rows
            ),
        }


def _bounded_read(stream: BinaryIO) -> bytes:
    """Consume at most one sentinel byte over the compressed workbook limit."""
    if not callable(getattr(stream, "read", None)):
        raise TypeError("expected a binary workbook stream")
    chunks: list[bytes] = []
    total = 0
    while total <= MAX_WORKBOOK_BYTES:
        requested = min(65_536, MAX_WORKBOOK_BYTES + 1 - total)
        try:
            chunk = stream.read(requested)
        except OSError:
            raise ValueError("failed to read workbook stream") from None
        if type(chunk) is not bytes:
            raise ValueError("workbook stream must yield bytes")
        if len(chunk) > requested:
            raise ValueError("workbook reader exceeded requested chunk")
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    if total > MAX_WORKBOOK_BYTES:
        raise ValueError("compressed workbook exceeds local size limit")
    return b"".join(chunks)


def _check_zip_members(
    raw: bytes, *, max_entry_bytes: int = MAX_ZIP_ENTRY_BYTES,
    max_total_bytes: int = MAX_ZIP_TOTAL_BYTES,
) -> None:
    """Reject excessive/active archive entries before workbook XML processing."""
    try:
        with ZipFile(BytesIO(raw)) as archive:
            members = archive.infolist()
            if not 1 <= len(members) <= MAX_ZIP_MEMBERS:
                raise ValueError("workbook has an unsupported entry count")
            total = 0
            seen_names: set[str] = set()
            for item in members:
                name = item.filename.replace("\\", "/").lower()
                if name in seen_names:
                    raise ValueError("workbook contains duplicate archive entries")
                seen_names.add(name)
                if (
                    name.startswith("/")
                    or any(part in ("", ".", "..") for part in name.split("/"))
                    or any(name.startswith(prefix) for prefix in FORBIDDEN_PARTS)
                    or item.flag_bits & 1
                ):
                    raise ValueError("workbook contains unsupported archive features")
                if item.file_size > max_entry_bytes:
                    raise ValueError("workbook archive entry exceeds byte budget")
                total += item.file_size
                if total > max_total_bytes:
                    raise ValueError("workbook archive uncompressed size exceeds budget")
                if item.file_size and (
                    item.compress_size == 0
                    or item.file_size > item.compress_size * MAX_ZIP_COMPRESSION_RATIO
                ):
                    raise ValueError("workbook archive compression ratio exceeds budget")
    except BadZipFile:
        raise ValueError("invalid ZIP workbook") from None


def _normalize_workbook_stock_code(value: object) -> str:
    """Normalize only the exact UCI workbook's reviewed cell encodings."""
    if type(value) is int and 10_000 <= value <= 99_999:
        return str(value)
    if is_valid_uci_stock_code(value, allow_internal_spaces=True):
        return value
    raise ValueError("invalid product stock code")


def _normalize_uci_workbook_invoice(value: object) -> object:
    """Classify publisher-shaped invoice IDs without retaining unknown prefixes."""
    if type(value) is int and 100_000 <= value <= 999_999:
        return value
    if type(value) is not str:
        raise ValueError("invalid UCI workbook invoice number")
    if re.fullmatch(r"[0-9]{6}", value):
        return value
    if re.fullmatch(r"[Cc][0-9]{6}", value):
        return f"C{value[1:]}"
    if re.fullmatch(r"[A-Za-z][0-9]{6}", value):
        return _UCI_UNVERIFIED_INVOICE_PREFIX
    raise ValueError("invalid UCI workbook invoice number")


def read_uci_workbook(
    stream: BinaryIO, *, expected_sha256: str,
    sheet_name: str = "Online Retail",
    max_rows: int = MAX_ROWS,
    max_groups: int = MAX_GROUPS,
    max_zip_entry_bytes: int = MAX_ZIP_ENTRY_BYTES,
    max_zip_total_bytes: int = MAX_ZIP_TOTAL_BYTES,
) -> UciWorkbookReadResult:
    """Project a small, already-authorized local workbook through strict UCI schema.

    The **caller** selects and approves source access. This code never opens a
    path, downloads data, verifies a license or invents publication timestamps.
    Archive expansion limits default to the conservative local profile. A
    caller may request a larger, still finite profile only after separate
    review of a trusted local source; the explicit supported ceilings remain
    192 MiB per member and 224 MiB total. Compressed bytes and compression
    ratio limits are unchanged.
    """
    if type(expected_sha256) is not str or not re.fullmatch(
        r"[0-9a-f]{64}", expected_sha256
    ):
        raise ValueError("expected workbook SHA-256 must be 64 lowercase hex digits")
    if sheet_name != "Online Retail":
        raise ValueError("unsupported workbook sheet selection")
    if type(max_rows) is not int or not 1 <= max_rows <= MAX_SUPPORTED_ROWS:
        raise ValueError("invalid bounded workbook row limit")
    if (
        type(max_groups) is not int
        or not 1 <= max_groups <= MAX_SUPPORTED_UCI_WORKBOOK_GROUPS
    ):
        raise ValueError("invalid bounded workbook group limit")
    if (
        type(max_zip_entry_bytes) is not int
        or not 1 <= max_zip_entry_bytes <= MAX_SUPPORTED_ZIP_ENTRY_BYTES
    ):
        raise ValueError("invalid bounded workbook ZIP entry limit")
    if (
        type(max_zip_total_bytes) is not int
        or not 1 <= max_zip_total_bytes <= MAX_SUPPORTED_ZIP_TOTAL_BYTES
    ):
        raise ValueError("invalid bounded workbook ZIP total limit")
    if max_zip_entry_bytes > max_zip_total_bytes:
        raise ValueError("invalid bounded workbook ZIP limits")
    raw = _bounded_read(stream)
    digest = sha256(raw).hexdigest()
    if not compare_digest(digest, expected_sha256):
        raise ValueError("workbook bytes do not match expected digest")
    _check_zip_members(
        raw,
        max_entry_bytes=max_zip_entry_bytes,
        max_total_bytes=max_zip_total_bytes,
    )
    try:
        import openpyxl.utils.datetime  # noqa: F401 - optional OOXML date conversion
    except ImportError:
        raise RuntimeError("optional XLSX support requires the uci extra") from None
    try:
        from mirrormind.domains.retail.uci_xlsx_xml import iter_uci_projection_rows

        with ZipFile(BytesIO(raw)) as archive:
            selected_rows = iter_uci_projection_rows(
                archive, sheet_name=sheet_name, max_rows=max_rows,
                expected_header=UCI_HEADER,
            )

            def normalized_rows():
                for row in selected_rows:
                    invoice = _normalize_uci_workbook_invoice(row["InvoiceNo"])
                    row["InvoiceNo"] = invoice
                    if invoice is _UCI_UNVERIFIED_INVOICE_PREFIX:
                        yield row
                        continue
                    row["StockCode"] = _normalize_workbook_stock_code(
                        row["StockCode"]
                    )
                    yield row

            projection = _project_uci_retail_rows(
                normalized_rows(), max_rows=max_rows, max_groups=max_groups,
                max_groups_ceiling=MAX_SUPPORTED_UCI_WORKBOOK_GROUPS,
                allow_internal_stock_code_spaces=True,
                allow_unverified_invoice_prefix=True,
            )
    except ImportError:
        raise RuntimeError("optional XLSX support requires the uci extra") from None
    except (ValueError, TypeError):
        raise
    except Exception:  # noqa: BLE001 - sanitize XML/ZIP parser errors
        raise ValueError("invalid workbook row structure") from None
    return UciWorkbookReadResult(digest, projection)
