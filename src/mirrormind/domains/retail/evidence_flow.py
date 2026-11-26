"""Composable local retail evidence preflight; never an authorization boundary.

These functions join bounded format readers, review-only metadata and
caller-declared temporal checks. All results stay in memory. A digest binds
the bytes that were supplied, not their publisher, legal rights or true
availability. Returned typed source objects can contain local series or
product identifiers; receipts deliberately contain aggregate metadata only.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from types import MappingProxyType
from typing import BinaryIO

from mirrormind.domains.retail.calendar_coverage import (
    DeclaredCalendarCoverage,
    summarize_declared_calendar_coverage,
)
from mirrormind.domains.retail.declared_releases import (
    DeclaredProductRelease,
    DeclaredRetailAsOfAudit,
    audit_declared_releases_as_of,
)
from mirrormind.domains.retail.uci_workbook import (
    UciWorkbookReadResult,
    read_uci_workbook,
)
from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    SourceReviewPacket,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.snapshots import (
    Observation,
    StagedSnapshot,
    available_as_of,
    read_staged_csv,
    snapshot_quality_summary,
)


@dataclass(frozen=True, slots=True)
class RetailCsvEvidenceFlow:
    """Staged CSV components and the rows matching one declared historical origin."""

    staged: StagedSnapshot
    review_packet: SourceReviewPacket
    quality_summary: Mapping[str, str | int]
    declared_as_of_observations: tuple[Observation, ...]
    origin_on: str

    def receipt(self) -> dict[str, object]:
        """Return status and aggregate counts without series identifiers or values."""
        as_of_status = (
            "declared_rows_selected_not_source_verified"
            if self.declared_as_of_observations
            else "abstained_no_declared_rows_available_as_of_origin"
        )
        return {
            "status": "local_retail_csv_evidence_flow_not_authorized",
            "source_review": self.review_packet.receipt(),
            "snapshot_quality": dict(self.quality_summary),
            "as_of": {
                "status": as_of_status,
                "origin_on": self.origin_on,
                "selected_observation_count": len(self.declared_as_of_observations),
                "series_identifier_status": "not_returned",
                "forecast_eligible": False,
            },
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


@dataclass(frozen=True, slots=True)
class RetailUciEvidenceFlow:
    """Workbook projection, declared calendar and release audit for later offline use."""

    workbook: UciWorkbookReadResult
    review_packet: SourceReviewPacket
    calendar_coverage: DeclaredCalendarCoverage
    declared_releases: tuple[DeclaredProductRelease, ...]
    release_audit: DeclaredRetailAsOfAudit

    def receipt(self) -> dict[str, object]:
        """Return component summaries only; never product IDs or transaction values."""
        return {
            "status": "local_retail_uci_evidence_flow_not_authorized",
            "source_review": self.review_packet.receipt(),
            "projection": self.workbook.receipt(),
            "calendar_coverage": self.calendar_coverage.receipt(),
            "release_audit": self.release_audit.receipt(),
            "release_declaration_count": len(self.declared_releases),
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def prepare_retail_csv_evidence_flow(
    stream: BinaryIO,
    *,
    expected_sha256: str,
    declaration: SourceReviewDeclaration,
    inspected_on: date,
    series_id: str,
    origin_on: str,
) -> RetailCsvEvidenceFlow:
    """Compose bounded CSV staging, review metadata, quality and declared as-of selection.

    The caller opens the stream and supplies an unverified declaration. The
    selected tuple is useful to later offline experiments but never certifies
    rights, publisher identity, actual historical publication or forecast use.
    An empty tuple is an abstention, not an implicit zero-filled history.
    """
    staged = read_staged_csv(stream, expected_sha256=expected_sha256)
    packet = prepare_source_review_packet(
        staged, declaration, inspected_on=inspected_on
    )
    quality = MappingProxyType(snapshot_quality_summary(staged))
    selected = available_as_of(
        staged, series_id=series_id, origin_on=origin_on
    )
    return RetailCsvEvidenceFlow(
        staged=staged,
        review_packet=packet,
        quality_summary=quality,
        declared_as_of_observations=selected,
        origin_on=origin_on,
    )


def prepare_retail_uci_evidence_flow(
    stream: BinaryIO,
    *,
    expected_sha256: str,
    declaration: SourceReviewDeclaration,
    inspected_on: date,
    declared_calendar: tuple[date, ...],
    declared_releases: tuple[DeclaredProductRelease, ...],
    origin_on: date,
) -> RetailUciEvidenceFlow:
    """Compose bounded XLSX projection and explicit, unverified calendar/release checks.

    `InvoiceDate` remains an event date only. Every publication date must be
    supplied in `declared_releases`; no publisher vintage is inferred. The
    returned audit exposes aggregate counts, while typed components remain
    available to a later offline consumer and are never permission grants.
    """
    workbook = read_uci_workbook(stream, expected_sha256=expected_sha256)
    packet = prepare_source_review_packet(
        workbook, declaration, inspected_on=inspected_on
    )
    coverage = summarize_declared_calendar_coverage(
        workbook.projection, declared_calendar
    )
    release_audit = audit_declared_releases_as_of(
        workbook.projection, declared_releases, origin_on=origin_on
    )
    return RetailUciEvidenceFlow(
        workbook=workbook,
        review_packet=packet,
        calendar_coverage=coverage,
        declared_releases=declared_releases,
        release_audit=release_audit,
    )
