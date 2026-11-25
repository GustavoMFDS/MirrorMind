"""Composed retail evidence preflight on generated local fixtures only."""
from datetime import date, datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pytest
from openpyxl import Workbook

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.evidence_flow import (
    prepare_retail_csv_evidence_flow,
    prepare_retail_uci_evidence_flow,
)
from mirrormind.domains.retail.uci_workbook import UCI_HEADER
from mirrormind.modules.evidence.intake_review import SourceReviewDeclaration

ROOT = Path(__file__).resolve().parents[2]
INSPECTED_ON = date(2026, 11, 23)
CAPTURED_ON = date(2026, 11, 22)


def _declaration(source_kind: str, digest: str) -> SourceReviewDeclaration:
    return SourceReviewDeclaration(
        source_kind=source_kind,
        source_record_ref="SRC-001",
        snapshot_sha256=digest,
        license_evidence_ref="LIC-001",
        permission_evidence_ref="PERM-001",
        privacy_review_ref="PRIV-001",
        intended_use="research_evaluation",
        retention_days=30,
        captured_on=CAPTURED_ON,
        availability_evidence_ref="AVAIL-001",
    )


def _uci_workbook_bytes() -> bytes:
    book = Workbook()
    sheet = book.active
    sheet.title = "Online Retail"
    sheet.append(list(UCI_HEADER))
    for invoice, day, units in (
        ("536365", 1, 2),
        ("536366", 2, 5),
        ("536367", 3, 7),
    ):
        sheet.append([
            invoice, "SECRET-SKU", "PRIVATE DESCRIPTION", units,
            datetime(2011, 1, day, 12), 1.5, 12345, "fictional",
        ])
    stream = BytesIO()
    book.save(stream)
    book.close()
    return stream.getvalue()


def _uci_flow(
    data: bytes,
    *,
    calendar: tuple[date, ...] | None = None,
    releases: tuple[DeclaredProductRelease, ...] | None = None,
):
    digest = sha256(data).hexdigest()
    return prepare_retail_uci_evidence_flow(
        BytesIO(data),
        expected_sha256=digest,
        declaration=_declaration("uci_xlsx", digest),
        inspected_on=INSPECTED_ON,
        declared_calendar=(
            calendar if calendar is not None
            else tuple(date(2011, 1, day) for day in (1, 2, 3))
        ),
        declared_releases=(
            releases if releases is not None else (
                DeclaredProductRelease("SECRET-SKU", date(2011, 1, 1), date(2011, 1, 1)),
                DeclaredProductRelease("SECRET-SKU", date(2011, 1, 2), date(2011, 1, 3)),
                DeclaredProductRelease("SECRET-SKU", date(2011, 1, 3), date(2011, 1, 3)),
            )
        ),
        origin_on=date(2011, 1, 2),
    )


def test_csv_flow_binds_review_quality_and_declared_asof_slice_without_authorizing():
    data = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    digest = sha256(data).hexdigest()
    flow = prepare_retail_csv_evidence_flow(
        BytesIO(data),
        expected_sha256=digest,
        declaration=_declaration("daily_csv", digest),
        inspected_on=INSPECTED_ON,
        series_id="item-A",
        origin_on="2025-01-03",
    )

    assert [row.units for row in flow.declared_as_of_observations] == [2, 0]
    assert flow.quality_summary["late_published_rows"] == 1
    aggregate = flow.receipt()
    assert aggregate["source_review"] == flow.review_packet.receipt()
    assert aggregate["snapshot_quality"] == dict(flow.quality_summary)
    receipt = str(aggregate)
    assert aggregate["ingestion_authorized"] is False
    assert aggregate["forecast_eligible"] is False
    assert "item-A" not in receipt
    for reference in ("SRC-001", "LIC-001", "PERM-001", "PRIV-001", "AVAIL-001"):
        assert reference not in receipt
    assert "declared_rows_selected_not_source_verified" in receipt


def test_csv_flow_abstains_when_no_declared_observation_is_available_at_origin():
    data = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    digest = sha256(data).hexdigest()
    flow = prepare_retail_csv_evidence_flow(
        BytesIO(data),
        expected_sha256=digest,
        declaration=_declaration("daily_csv", digest),
        inspected_on=INSPECTED_ON,
        series_id="item-A",
        origin_on="2024-12-31",
    )

    assert flow.declared_as_of_observations == ()
    assert flow.receipt()["as_of"]["status"] == (
        "abstained_no_declared_rows_available_as_of_origin"
    )
    assert flow.receipt()["as_of"]["selected_observation_count"] == 0
    assert flow.receipt()["as_of"]["forecast_eligible"] is False


def test_uci_flow_composes_calendar_and_release_cutoff_without_returning_identifiers():
    flow = _uci_flow(_uci_workbook_bytes())

    assert flow.calendar_coverage.observed_product_days == 3
    assert flow.release_audit.available_product_days == 1
    assert flow.release_audit.withheld_unpublished_days == 1
    assert flow.release_audit.future_event_days == 1
    aggregate = flow.receipt()
    assert aggregate["source_review"] == flow.review_packet.receipt()
    assert aggregate["projection"] == flow.workbook.receipt()
    assert aggregate["calendar_coverage"] == flow.calendar_coverage.receipt()
    assert aggregate["release_audit"] == flow.release_audit.receipt()
    receipt = str(aggregate)
    assert "SECRET-SKU" not in receipt
    assert "PRIVATE DESCRIPTION" not in receipt
    assert "12345" not in receipt
    assert "536365" not in receipt
    for reference in ("SRC-001", "LIC-001", "PERM-001", "PRIV-001", "AVAIL-001"):
        assert reference not in receipt
    assert "unknown_not_derived_from_invoice_date" in receipt
    assert flow.receipt()["forecast_eligible"] is False


def test_uci_flow_rejects_missing_calendar_dates_and_release_declarations():
    data = _uci_workbook_bytes()
    with pytest.raises(ValueError, match="absent from declared calendar"):
        _uci_flow(data, calendar=(date(2011, 1, 1), date(2011, 1, 3)))
    with pytest.raises(ValueError, match="each positive product-day"):
        _uci_flow(data, releases=(
            DeclaredProductRelease("SECRET-SKU", date(2011, 1, 1), date(2011, 1, 1)),
        ))


def test_csv_flow_rejects_digest_and_review_declaration_mismatch():
    data = (ROOT / "examples/staged-daily-observations.csv").read_bytes()
    digest = sha256(data).hexdigest()
    declaration = _declaration("daily_csv", digest)
    with pytest.raises(ValueError, match="do not match declared SHA-256"):
        prepare_retail_csv_evidence_flow(
            BytesIO(data),
            expected_sha256="0" * 64,
            declaration=declaration,
            inspected_on=INSPECTED_ON,
            series_id="item-A",
            origin_on="2025-01-03",
        )

    mismatched = _declaration("daily_csv", "0" * 64)
    with pytest.raises(ValueError, match="does not match declared snapshot SHA-256"):
        prepare_retail_csv_evidence_flow(
            BytesIO(data),
            expected_sha256=digest,
            declaration=mismatched,
            inspected_on=INSPECTED_ON,
            series_id="item-A",
            origin_on="2025-01-03",
        )

    wrong_format = _declaration("uci_xlsx", digest)
    with pytest.raises(ValueError, match="source kind does not match staged format"):
        prepare_retail_csv_evidence_flow(
            BytesIO(data),
            expected_sha256=digest,
            declaration=wrong_format,
            inspected_on=INSPECTED_ON,
            series_id="item-A",
            origin_on="2025-01-03",
        )
