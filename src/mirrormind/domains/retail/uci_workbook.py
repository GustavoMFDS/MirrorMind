"""Bounded optional XLSX reader for *trusted, approved* UCI-shaped sources.

No source permission is granted by parsing. Original UCI data, customer
identifiers, release vintages, full workbook support and model fitness remain
outside this experimental in-memory fixture-based reader.
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
    MAX_GROUPS,
    MAX_ROWS,
    MAX_SUPPORTED_GROUPS,
    MAX_SUPPORTED_ROWS,
    UciRetailProjection,
    project_uci_retail_rows,
)

MAX_WORKBOOK_BYTES = 32 * 1024 * 1024
MAX_ZIP_MEMBERS = 256
MAX_ZIP_ENTRY_BYTES = 64 * 1024 * 1024
MAX_ZIP_TOTAL_BYTES = 128 * 1024 * 1024
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


def _check_zip_members(raw: bytes) -> None:
    """Reject excessive/active archive entries before workbook XML processing."""
    try:
        with ZipFile(BytesIO(raw)) as archive:
            members = archive.infolist()
            if not 1 <= len(members) <= MAX_ZIP_MEMBERS:
                raise ValueError("workbook has an unsupported entry count")
            total = 0
            for item in members:
                name = item.filename.replace("\\", "/").lower()
                if (
                    name.startswith("/")
                    or any(part in ("", ".", "..") for part in name.split("/"))
                    or any(name.startswith(prefix) for prefix in FORBIDDEN_PARTS)
                    or item.flag_bits & 1
                ):
                    raise ValueError("workbook contains unsupported archive features")
                if item.file_size > MAX_ZIP_ENTRY_BYTES:
                    raise ValueError("workbook archive entry exceeds byte budget")
                total += item.file_size
                if total > MAX_ZIP_TOTAL_BYTES:
                    raise ValueError("workbook archive uncompressed size exceeds budget")
                if item.file_size and (
                    item.compress_size == 0
                    or item.file_size > item.compress_size * MAX_ZIP_COMPRESSION_RATIO
                ):
                    raise ValueError("workbook archive compression ratio exceeds budget")
    except BadZipFile:
        raise ValueError("invalid ZIP workbook") from None


def read_uci_workbook(
    stream: BinaryIO, *, expected_sha256: str,
    sheet_name: str = "Online Retail",
    max_rows: int = MAX_ROWS,
    max_groups: int = MAX_GROUPS,
) -> UciWorkbookReadResult:
    """Project a small, already-authorized local workbook through strict UCI schema.

    The **caller** selects and approves source access. This code never opens a
    path, downloads data, verifies a license or invents publication timestamps.
    """
    if type(expected_sha256) is not str or not re.fullmatch(
        r"[0-9a-f]{64}", expected_sha256
    ):
        raise ValueError("expected workbook SHA-256 must be 64 lowercase hex digits")
    if sheet_name != "Online Retail":
        raise ValueError("unsupported workbook sheet selection")
    if type(max_rows) is not int or not 1 <= max_rows <= MAX_SUPPORTED_ROWS:
        raise ValueError("invalid bounded workbook row limit")
    if type(max_groups) is not int or not 1 <= max_groups <= MAX_SUPPORTED_GROUPS:
        raise ValueError("invalid bounded workbook group limit")
    raw = _bounded_read(stream)
    digest = sha256(raw).hexdigest()
    if not compare_digest(digest, expected_sha256):
        raise ValueError("workbook bytes do not match expected digest")
    _check_zip_members(raw)
    try:
        from openpyxl import load_workbook
    except ImportError:
        raise RuntimeError("optional XLSX support requires the uci extra") from None
    try:
        book = load_workbook(
            BytesIO(raw), read_only=True, data_only=False, keep_links=False
        )
    except Exception:  # noqa: BLE001 - sanitize third-party parser errors that may include input
        raise ValueError("invalid or unsupported XLSX structure") from None
    try:
        if book.sheetnames != ["Online Retail"]:
            raise ValueError("unsupported workbook sheet layout")
        rows = iter(book["Online Retail"].iter_rows(values_only=True))
        header = next(rows, None)
        if tuple(header or ()) != UCI_HEADER:
            raise ValueError("unsupported workbook header layout")

        def selected_rows():
            for values in rows:
                if len(values) != len(UCI_HEADER):
                    raise ValueError("unsupported workbook transaction row")
                yield {
                    "InvoiceNo": values[0],
                    "StockCode": values[1],
                    "Quantity": values[3],
                    "InvoiceDate": values[4],
                }

        projection = project_uci_retail_rows(
            selected_rows(), max_rows=max_rows, max_groups=max_groups
        )
    except (ValueError, TypeError):
        raise
    except Exception:  # noqa: BLE001 - do not expose workbook cell contents in errors
        raise ValueError("invalid workbook row structure") from None
    finally:
        book.close()
    return UciWorkbookReadResult(digest, projection)
