"""Offline release assertions: synthetic only, no source authorization claims."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime

import pytest

from mirrormind.domains.retail.declared_releases import (
    DeclaredProductRelease,
    audit_declared_releases_as_of,
)
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows


def row(invoice, code, day, quantity):
    return {
        "InvoiceNo": invoice,
        "StockCode": code,
        "InvoiceDate": datetime(2011, 1, day, 12),
        "Quantity": quantity,
        "CustomerID": "NEVER-COPY",
    }


def fixture_projection():
    return project_uci_retail_rows([
        row("536365", "SECRET-A", 1, 2),
        row("536366", "SECRET-A", 2, 5),
        row("536367", "SECRET-B", 4, 7),
        row("C536368", "SECRET-A", 3, -4),
    ])


def releases():
    return (
        DeclaredProductRelease("SECRET-A", date(2011, 1, 1), date(2011, 1, 1)),
        DeclaredProductRelease("SECRET-A", date(2011, 1, 2), date(2011, 1, 5)),
        DeclaredProductRelease("SECRET-B", date(2011, 1, 4), date(2011, 1, 4)),
    )


def test_declared_asof_excludes_late_and_future_product_days_without_identifiers():
    result = audit_declared_releases_as_of(
        fixture_projection(), releases(), origin_on=date(2011, 1, 3)
    )
    assert (result.total_product_days, result.available_product_days) == (3, 1)
    assert (result.withheld_unpublished_days, result.future_event_days) == (1, 1)
    assert result.available_positive_units == 2
    receipt = str(result.receipt())
    assert "SECRET-A" not in receipt
    assert "SECRET-B" not in receipt
    assert "NEVER-COPY" not in receipt
    assert "caller_declared_unverified" in receipt
    assert "not_source_verified" in receipt
    with pytest.raises(FrozenInstanceError):
        result.available_positive_units = 999


def test_later_origin_changes_availability_but_not_source_trust():
    result = audit_declared_releases_as_of(
        fixture_projection(), releases(), origin_on=date(2011, 1, 6)
    )
    assert result.available_product_days == 3
    assert result.withheld_unpublished_days == 0
    assert result.future_event_days == 0
    assert result.available_positive_units == 14
    assert result.receipt()["publication_authority"] == "caller_declared_unverified"


def test_missing_release_declaration_must_not_be_derived_from_invoice_date():
    with pytest.raises(ValueError, match="each positive product-day"):
        audit_declared_releases_as_of(
            fixture_projection(), releases()[:-1], origin_on=date(2011, 1, 6)
        )


def test_duplicate_and_unmatched_release_declarations_are_rejected():
    projection = fixture_projection()
    with pytest.raises(ValueError, match="duplicate declared"):
        audit_declared_releases_as_of(
            projection, releases() + releases()[:1], origin_on=date(2011, 1, 6)
        )
    with pytest.raises(ValueError, match="no matching"):
        audit_declared_releases_as_of(
            projection,
            releases() + (
                DeclaredProductRelease("UNRELATED", date(2011, 1, 1), date(2011, 1, 1)),
            ),
            origin_on=date(2011, 1, 6),
        )


def test_release_cannot_precede_event_date_even_if_origin_is_later():
    bad = (
        releases()[0], releases()[1],
        DeclaredProductRelease("SECRET-B", date(2011, 1, 4), date(2011, 1, 3)),
    )
    with pytest.raises(ValueError, match="precede"):
        audit_declared_releases_as_of(
            fixture_projection(), bad, origin_on=date(2011, 1, 6)
        )


@pytest.mark.parametrize("bad_origin", [True, datetime(2011, 1, 3), "2011-01-03", None])
def test_origin_rejects_ambiguous_or_inexact_dates(bad_origin):
    with pytest.raises(ValueError, match="exact date"):
        audit_declared_releases_as_of(
            fixture_projection(), releases(), origin_on=bad_origin
        )


def test_empty_positive_projection_stays_empty_without_inventing_a_sale():
    projection = project_uci_retail_rows([row("C536365", "SECRET-A", 1, -2)])
    result = audit_declared_releases_as_of(
        projection, (), origin_on=date(2011, 1, 5)
    )
    assert result.total_product_days == 0
    assert result.available_positive_units == 0


def test_input_must_be_bounded_tuple_and_release_fields_exact_types():
    with pytest.raises(ValueError, match="bounded tuple"):
        audit_declared_releases_as_of(
            fixture_projection(), list(releases()), origin_on=date(2011, 1, 6)
        )
    bad = (
        DeclaredProductRelease("SECRET-A", date(2011, 1, 1), datetime(2011, 1, 1)),
    ) + releases()[1:]
    with pytest.raises(ValueError, match="invalid declared release"):
        audit_declared_releases_as_of(
            fixture_projection(), bad, origin_on=date(2011, 1, 6)
        )
