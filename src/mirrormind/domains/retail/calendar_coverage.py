"""Experimental declared-calendar coverage: an unverified schedule is not evidence.

A caller must explicitly supply a bounded, strictly ordered calendar. The
function never assumes weekends, holidays, open hours or publisher vintages.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from datetime import date

from mirrormind.domains.retail.coverage import summarize_retail_coverage
from mirrormind.domains.retail.uci_transactions import UciRetailProjection

MAX_DECLARED_DAYS = 3_660


@dataclass(frozen=True, slots=True)
class DeclaredCalendarCoverage:
    """Aggregate scheduled internal gaps without product identifiers."""

    calendar_days: int
    observed_product_days: int
    distinct_products: int
    internal_unscheduled_civil_days: int
    internal_missing_declared_days: int
    products_with_declared_gaps: int

    def receipt(self) -> dict[str, str | int]:
        """Keep the unverified calendar and unknown publisher availability explicit."""
        return {
            "status": "declared_calendar_not_source_verified",
            "calendar_authority": "caller_declared_unverified",
            "publication_time_status": "unknown_not_derived_from_invoice_date",
            "calendar_days": self.calendar_days,
            "observed_product_days": self.observed_product_days,
            "distinct_products": self.distinct_products,
            "internal_unscheduled_civil_days": self.internal_unscheduled_civil_days,
            "internal_missing_declared_days": self.internal_missing_declared_days,
            "products_with_declared_gaps": self.products_with_declared_gaps,
        }


def summarize_declared_calendar_coverage(
    projection: UciRetailProjection,
    declared_days: tuple[date, ...],
) -> DeclaredCalendarCoverage:
    """Count only absent *declared* dates between observed positive product-days.

    Every observed product-date must be present in the declared calendar.
    This catches contradictions, but does NOT verify that this was a real
    opening, collection or publisher schedule.
    """
    base = summarize_retail_coverage(projection)
    if type(declared_days) is not tuple or not 1 <= len(declared_days) <= MAX_DECLARED_DAYS:
        raise ValueError("declared calendar must be a bounded nonempty date tuple")
    previous_day: date | None = None
    for day in declared_days:
        if type(day) is not date or (previous_day is not None and day <= previous_day):
            raise ValueError("declared calendar requires sorted unique exact dates")
        previous_day = day

    last_by_product: dict[str, date] = {}
    missing = 0
    affected: set[str] = set()
    for item in projection.days:
        position = bisect_left(declared_days, item.observed_on)
        if position == len(declared_days) or declared_days[position] != item.observed_on:
            raise ValueError("observed product-day absent from declared calendar")
        last = last_by_product.get(item.stock_code)
        if last is not None:
            gap = bisect_left(declared_days, item.observed_on) - bisect_right(
                declared_days, last
            )
            if gap:
                missing += gap
                affected.add(item.stock_code)
        last_by_product[item.stock_code] = item.observed_on

    return DeclaredCalendarCoverage(
        calendar_days=len(declared_days),
        observed_product_days=base.observed_product_days,
        distinct_products=base.distinct_products,
        internal_unscheduled_civil_days=base.internal_missing_product_days - missing,
        internal_missing_declared_days=missing,
        products_with_declared_gaps=len(affected),
    )
