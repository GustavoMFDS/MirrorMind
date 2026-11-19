"""Retrospective availability audit for explicitly declared, unverified release dates.

This module does not infer first availability from transaction timestamps,
authenticate a publisher or authorize processing a real retail dataset.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from mirrormind.domains.retail.coverage import summarize_retail_coverage
from mirrormind.domains.retail.uci_transactions import (
    MAX_GROUPS,
    UciRetailProjection,
)


@dataclass(frozen=True, slots=True)
class DeclaredProductRelease:
    """An explicitly asserted release day for one positive product/event day."""

    stock_code: str
    observed_on: date
    available_on: date


@dataclass(frozen=True, slots=True)
class DeclaredRetailAsOfAudit:
    """Identifier-free counts, not an authenticated historical evidence view."""

    origin_on: date
    total_product_days: int
    available_product_days: int
    withheld_unpublished_days: int
    future_event_days: int
    available_positive_units: int

    def receipt(self) -> dict[str, str | int]:
        """No identifiers or source data; prominently mark asserted release dates."""
        return {
            "status": "declared_release_audit_not_source_verified",
            "publication_authority": "caller_declared_unverified",
            "origin_on": self.origin_on.isoformat(),
            "total_product_days": self.total_product_days,
            "available_product_days": self.available_product_days,
            "withheld_unpublished_days": self.withheld_unpublished_days,
            "future_event_days": self.future_event_days,
            "available_positive_units": self.available_positive_units,
        }


def audit_declared_releases_as_of(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    origin_on: date,
) -> DeclaredRetailAsOfAudit:
    """Account for every positive product-day without inferring availability.

    Release declarations must match every projected (product, event-day) key
    exactly once. Future events and observations not released by the origin
    are *counted as excluded*, never exposed as accessible evidence.
    """
    validated = summarize_retail_coverage(projection)
    if type(origin_on) is not date:
        raise ValueError("origin_on must be an exact date")
    if type(releases) is not tuple or len(releases) > MAX_GROUPS:
        raise ValueError("release declarations exceed bounded tuple budget")
    actual = {(item.stock_code, item.observed_on): item for item in projection.days}
    declared: dict[tuple[str, date], date] = {}
    for release in releases:
        if (
            type(release) is not DeclaredProductRelease
            or type(release.stock_code) is not str
            or type(release.observed_on) is not date
            or type(release.available_on) is not date
        ):
            raise ValueError("invalid declared release")
        key = (release.stock_code, release.observed_on)
        if key not in actual:
            raise ValueError("release has no matching positive product-day")
        if key in declared:
            raise ValueError("duplicate declared product-day release")
        if release.available_on < release.observed_on:
            raise ValueError("release cannot precede its event day")
        declared[key] = release.available_on
    if len(declared) != validated.observed_product_days:
        raise ValueError("each positive product-day needs a declared release")

    available = withheld = future = units = 0
    for item in projection.days:
        if item.observed_on > origin_on:
            future += 1
        elif declared[(item.stock_code, item.observed_on)] > origin_on:
            withheld += 1
        else:
            available += 1
            units += item.units
    return DeclaredRetailAsOfAudit(
        origin_on=origin_on,
        total_product_days=validated.observed_product_days,
        available_product_days=available,
        withheld_unpublished_days=withheld,
        future_event_days=future,
        available_positive_units=units,
    )
