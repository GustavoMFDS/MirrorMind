"""Bounded, privacy-minimizing projection of UCI-shaped retail row mappings.

This module neither reads the official workbook nor establishes permissions.
InvoiceDate is an *event* timestamp, NOT verified historical publication
time; its outputs MUST NOT be passed to as-of forecasting as known evidence.
"""
from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import TypeGuard

MAX_ROWS = 10_000
MAX_GROUPS = 2_000
MAX_SUPPORTED_ROWS = 600_000
MAX_SUPPORTED_GROUPS = 100_000
MAX_SUPPORTED_UCI_WORKBOOK_GROUPS = 250_000
MAX_LINE_UNITS = 1_000_000_000
MAX_TOTAL_UNITS = 1_000_000_000
REQUIRED_FIELDS = frozenset({"InvoiceNo", "StockCode", "Quantity", "InvoiceDate"})
_STOCK_CODE_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,31}")
_SPACED_STOCK_CODE_PATTERN = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9._ -]{0,30}[A-Za-z0-9]"
)
_UCI_UNVERIFIED_INVOICE_PREFIX = object()


@dataclass(frozen=True, slots=True)
class ProductDayUnits:
    """Positive invoice-line units for a product/event day, not latent demand."""

    stock_code: str
    observed_on: date
    units: int


@dataclass(frozen=True, slots=True)
class UciRetailProjection:
    """Immutable local research projection with no authenticated data rights."""

    days: tuple[ProductDayUnits, ...]
    processed_rows: int
    accepted_rows: int
    cancelled_rows: int
    negative_quantity_rows: int
    zero_quantity_rows: int
    unverified_invoice_prefix_rows: int = 0

    def receipt(self) -> dict[str, str | int]:
        """Return only aggregate counters and explicit permission/time uncertainty."""
        return {
            "status": "uci_shaped_projection_not_authorized",
            "publication_time_status": "unknown_not_derived_from_invoice_date",
            "processed_rows": self.processed_rows,
            "accepted_rows": self.accepted_rows,
            "cancelled_rows": self.cancelled_rows,
            "negative_quantity_rows": self.negative_quantity_rows,
            "zero_quantity_rows": self.zero_quantity_rows,
            "product_day_groups": len(self.days),
        }


def _invoice_number(value: object) -> str:
    """Normalize an invoice code, preserving explicit C-prefixed cancellations."""
    if type(value) is int and 0 < value <= 999_999_999_999:
        return str(value)
    if type(value) is not str or not re.fullmatch(r"C?[0-9]{5,12}", value):
        raise ValueError("invalid invoice number format")
    return value


def _transaction_day(value: object) -> date:
    """Accept only timezone-naive Excel-style datetimes as event observations."""
    if type(value) is not datetime or value.tzinfo is not None:
        raise ValueError("InvoiceDate must be a naive datetime")
    return value.date()


def is_valid_uci_stock_code(
    value: object, *, allow_internal_spaces: bool = False
) -> TypeGuard[str]:
    """Validate a normalized source code without trimming or coercion.

    The normal synthetic row contract remains a compact ASCII token. The
    reviewed XLSX adapter may additionally preserve internal ASCII spaces as
    opaque categories; leading/trailing whitespace and non-ASCII characters
    remain invalid.
    """
    if type(value) is not str:
        return False
    if _STOCK_CODE_PATTERN.fullmatch(value):
        return True
    return (
        type(allow_internal_spaces) is bool
        and allow_internal_spaces
        and _SPACED_STOCK_CODE_PATTERN.fullmatch(value) is not None
    )


def project_uci_retail_rows(
    rows: Iterable[Mapping[str, object]], *,
    max_rows: int = MAX_ROWS,
    max_groups: int = MAX_GROUPS,
) -> UciRetailProjection:
    """Summarize strictly positive invoice quantities, never source availability.

    The trusted caller must project/authorize rows before calling this bounded
    local function. Extra fields (notably CustomerID, Description, Country,
    UnitPrice) are neither accessed nor returned. Nothing is persisted or
    logged. Cancellation/negative/zero rows are reported, not imputed.
    """
    return _project_uci_retail_rows(
        rows,
        max_rows=max_rows,
        max_groups=max_groups,
        max_groups_ceiling=MAX_SUPPORTED_GROUPS,
        allow_internal_stock_code_spaces=False,
    )


def _project_uci_retail_rows(
    rows: Iterable[Mapping[str, object]], *,
    max_rows: int,
    max_groups: int,
    max_groups_ceiling: int,
    allow_internal_stock_code_spaces: bool,
    allow_unverified_invoice_prefix: bool = False,
) -> UciRetailProjection:
    """Internal bounded implementation shared with the UCI workbook adapter."""
    if type(max_rows) is not int or not 1 <= max_rows <= MAX_SUPPORTED_ROWS:
        raise ValueError(
            f"max_rows must be an exact integer in 1..{MAX_SUPPORTED_ROWS}"
        )
    if type(max_groups_ceiling) is not int or max_groups_ceiling not in {
        MAX_SUPPORTED_GROUPS, MAX_SUPPORTED_UCI_WORKBOOK_GROUPS
    }:
        raise ValueError("unsupported local group-budget profile")
    if type(max_groups) is not int or not 1 <= max_groups <= max_groups_ceiling:
        raise ValueError(
            f"max_groups must be an exact integer in 1..{max_groups_ceiling}"
        )
    if type(allow_internal_stock_code_spaces) is not bool:
        raise ValueError("allow_internal_stock_code_spaces must be a boolean")
    if type(allow_unverified_invoice_prefix) is not bool:
        raise ValueError("allow_unverified_invoice_prefix must be a boolean")
    try:
        iterator = iter(rows)
    except TypeError as exc:
        raise TypeError("rows must be an iterable of mappings") from exc
    grouped: dict[tuple[str, date], int] = {}
    processed = accepted = cancelled = negative = zeros = 0
    unverified_invoice_prefixes = total = 0
    for row in iterator:
        if processed >= max_rows:
            raise ValueError("row count exceeds local projection budget")
        processed += 1
        if not isinstance(row, Mapping) or not REQUIRED_FIELDS.issubset(row):
            raise ValueError("invalid required transaction fields")
        invoice_value = row["InvoiceNo"]
        if invoice_value is _UCI_UNVERIFIED_INVOICE_PREFIX:
            if not allow_unverified_invoice_prefix:
                raise ValueError("invalid invoice number format")
            unverified_invoice_prefixes += 1
            continue
        invoice = _invoice_number(invoice_value)
        stock_code = row["StockCode"]
        if not is_valid_uci_stock_code(
            stock_code, allow_internal_spaces=allow_internal_stock_code_spaces
        ):
            raise ValueError("invalid product stock code")
        quantity = row["Quantity"]
        if type(quantity) is not int or not -MAX_LINE_UNITS <= quantity <= MAX_LINE_UNITS:
            raise ValueError("Quantity must be an exact bounded integer")
        observed = _transaction_day(row["InvoiceDate"])
        if invoice.startswith("C"):
            cancelled += 1
            continue
        if quantity < 0:
            negative += 1
            continue
        if quantity == 0:
            zeros += 1
            continue
        key = (stock_code, observed)
        if key not in grouped and len(grouped) >= max_groups:
            raise ValueError("product-day group count exceeds local budget")
        if total + quantity > MAX_TOTAL_UNITS:
            raise ValueError("aggregated positive quantity exceeds local budget")
        grouped[key] = grouped.get(key, 0) + quantity
        total += quantity
        accepted += 1
    if not processed:
        raise ValueError("transaction projection requires at least one row")
    return UciRetailProjection(
        days=tuple(ProductDayUnits(code, day, units)
                   for (code, day), units in sorted(grouped.items())),
        processed_rows=processed,
        accepted_rows=accepted,
        cancelled_rows=cancelled,
        negative_quantity_rows=negative,
        zero_quantity_rows=zeros,
        unverified_invoice_prefix_rows=unverified_invoice_prefixes,
    )
