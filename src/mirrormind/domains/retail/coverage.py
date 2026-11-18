"""Aggregate internal calendar coverage for experimental retail projections.

No missing product-day is inferred to be zero demand, a stockout or a
published observation. No product identifiers are returned by the summary.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from mirrormind.domains.retail.uci_transactions import (
    MAX_GROUPS,
    MAX_TOTAL_UNITS,
    UciRetailProjection,
)


@dataclass(frozen=True, slots=True)
class RetailCoverageSummary:
    """Bounded, identifier-free coverage metadata for observed positive lines."""

    observed_product_days: int
    distinct_products: int
    internal_missing_product_days: int
    products_with_internal_gaps: int
    earliest_event_day: date | None
    latest_event_day: date | None

    def receipt(self) -> dict[str, str | int | None]:
        """Return aggregate values only, with an explicit source-trust caveat."""
        return {
            "status": "synthetic_retail_coverage_not_authorized",
            "publication_time_status": "unknown_not_derived_from_invoice_date",
            "observed_product_days": self.observed_product_days,
            "distinct_products": self.distinct_products,
            "internal_missing_product_days": self.internal_missing_product_days,
            "products_with_internal_gaps": self.products_with_internal_gaps,
            "earliest_event_day": (
                self.earliest_event_day.isoformat() if self.earliest_event_day else None
            ),
            "latest_event_day": (
                self.latest_event_day.isoformat() if self.latest_event_day else None
            ),
        }


def summarize_retail_coverage(projection: UciRetailProjection) -> RetailCoverageSummary:
    """Count gaps *between* observed positive product-days, without imputation.

    A day absent after a product's last observed date or before its first
    observed date is not counted: observation-window boundaries are unknown.
    A cancellation/return-only day is also absent, not a recorded zero.
    """
    if type(projection) is not UciRetailProjection:
        raise TypeError("expected a UciRetailProjection")
    if type(projection.days) is not tuple or len(projection.days) > MAX_GROUPS:
        raise ValueError("invalid bounded product-day projection")
    previous: dict[str, date] = {}
    gap_products: set[str] = set()
    missing = 0
    total_units = 0
    earliest: date | None = None
    latest: date | None = None
    for item in projection.days:
        if (
            type(item.stock_code) is not str
            or not item.stock_code
            or type(item.observed_on) is not date
            or type(item.units) is not int
            or not 1 <= item.units <= MAX_TOTAL_UNITS
        ):
            raise ValueError("invalid product-day observation")
        total_units += item.units
        if total_units > MAX_TOTAL_UNITS:
            raise ValueError("product-day units exceed aggregate budget")
        last = previous.get(item.stock_code)
        if last is not None:
            if item.observed_on <= last:
                raise ValueError("duplicate or unordered product-day observation")
            gap = (item.observed_on - last).days - 1
            if gap:
                missing += gap
                gap_products.add(item.stock_code)
        previous[item.stock_code] = item.observed_on
        if earliest is None or item.observed_on < earliest:
            earliest = item.observed_on
        if latest is None or item.observed_on > latest:
            latest = item.observed_on
    return RetailCoverageSummary(
        observed_product_days=len(projection.days),
        distinct_products=len(previous),
        internal_missing_product_days=missing,
        products_with_internal_gaps=len(gap_products),
        earliest_event_day=earliest,
        latest_event_day=latest,
    )
