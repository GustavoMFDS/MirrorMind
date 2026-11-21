"""Review-only manifest binding for previously staged local evidence.

This does not acquire, authorize, persist or publish a dataset. Evidence
references are caller assertions; even an exact checksum is not provenance.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from hmac import compare_digest

from mirrormind.domains.retail.uci_workbook import UciWorkbookReadResult
from mirrormind.modules.evidence.snapshots import StagedSnapshot

SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
REFERENCE_PATTERN = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
SOURCE_KINDS = frozenset(("daily_csv", "uci_xlsx"))
INTENDED_USES = frozenset(("research_evaluation", "commercial_product"))


@dataclass(frozen=True, slots=True)
class SourceReviewDeclaration:
    """Human-supplied review references; not authenticated permissions."""

    source_kind: str
    source_record_ref: str
    snapshot_sha256: str
    license_evidence_ref: str
    permission_evidence_ref: str
    privacy_review_ref: str
    intended_use: str
    retention_days: int
    captured_on: date
    availability_evidence_ref: str | None = None


@dataclass(frozen=True, slots=True)
class SourceReviewPacket:
    """Identifier-minimized metadata for an external human reviewer."""

    source_kind: str
    intended_use: str
    snapshot_sha256: str
    declaration_sha256: str
    captured_on: date
    inspected_on: date
    retention_days: int
    record_count: int
    availability_evidence_declared: bool

    def receipt(self) -> dict[str, str | int | bool]:
        """Expose a non-authorizing summary, never input rows or references."""
        return {
            "status": "source_intake_requires_independent_human_review",
            "source_kind": self.source_kind,
            "intended_use": self.intended_use,
            "snapshot_sha256": self.snapshot_sha256,
            "declaration_sha256": self.declaration_sha256,
            "captured_on": self.captured_on.isoformat(),
            "inspected_on": self.inspected_on.isoformat(),
            "declared_retention_days": self.retention_days,
            "record_count": self.record_count,
            "evidence_reference_status": "caller_declared_not_authenticated",
            "permission_status": "not_verified_no_ingestion",
            "privacy_status": "not_verified",
            "historical_availability_status": "not_verified_no_asof_claim",
            "availability_evidence_declared": self.availability_evidence_declared,
            "human_review_required": True,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def prepare_source_review_packet(
    staged: StagedSnapshot | UciWorkbookReadResult,
    declaration: SourceReviewDeclaration,
    *,
    inspected_on: date,
) -> SourceReviewPacket:
    """Bind a staged digest to unverified review declarations without approval.

    Only the existing in-memory CSV/XLSX staging types are accepted, and no
    raw content, URL, identifier or sensitive reference is returned.
    """
    if type(declaration) is not SourceReviewDeclaration:
        raise ValueError("expected an exact source review declaration")
    if type(inspected_on) is not date or type(declaration.captured_on) is not date:
        raise ValueError("inspection and capture require exact calendar dates")
    if declaration.captured_on > inspected_on:
        raise ValueError("capture cannot occur after inspection")
    if type(declaration.source_kind) is not str or declaration.source_kind not in SOURCE_KINDS:
        raise ValueError("unsupported source kind")
    if (type(declaration.intended_use) is not str
            or declaration.intended_use not in INTENDED_USES):
        raise ValueError("unsupported declared intended use")
    if type(declaration.retention_days) is not int or not 1 <= declaration.retention_days <= 3650:
        raise ValueError("invalid declared retention period")

    references = (
        declaration.source_record_ref,
        declaration.license_evidence_ref,
        declaration.permission_evidence_ref,
        declaration.privacy_review_ref,
    )
    if any(type(value) is not str or REFERENCE_PATTERN.fullmatch(value) is None
           for value in references):
        raise ValueError("invalid source or review evidence reference")
    vintage_ref = declaration.availability_evidence_ref
    if vintage_ref is not None and (
        type(vintage_ref) is not str or REFERENCE_PATTERN.fullmatch(vintage_ref) is None
    ):
        raise ValueError("invalid availability evidence reference")

    digest = declaration.snapshot_sha256
    if type(digest) is not str or SHA256_PATTERN.fullmatch(digest) is None:
        raise ValueError("invalid declared snapshot SHA-256")
    if type(staged) is StagedSnapshot:
        if declaration.source_kind != "daily_csv":
            raise ValueError("source kind does not match staged format")
        staged_digest = staged.sha256_hex
        record_count = len(staged.observations)
    elif type(staged) is UciWorkbookReadResult:
        if declaration.source_kind != "uci_xlsx":
            raise ValueError("source kind does not match staged format")
        staged_digest = staged.sha256_hex
        record_count = staged.projection.processed_rows
    else:
        raise ValueError("expected a supported staged source result")
    if not compare_digest(digest, staged_digest):
        raise ValueError("staged content does not match declared snapshot SHA-256")
    if record_count < 1:
        raise ValueError("staged result must be nonempty")

    canonical = {
        "version": 1,
        "source_kind": declaration.source_kind,
        "source_record_ref": declaration.source_record_ref,
        "snapshot_sha256": digest,
        "license_evidence_ref": declaration.license_evidence_ref,
        "permission_evidence_ref": declaration.permission_evidence_ref,
        "privacy_review_ref": declaration.privacy_review_ref,
        "intended_use": declaration.intended_use,
        "retention_days": declaration.retention_days,
        "captured_on": declaration.captured_on.isoformat(),
        "inspected_on": inspected_on.isoformat(),
        "availability_evidence_ref": vintage_ref,
    }
    manifest_digest = sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return SourceReviewPacket(
        source_kind=declaration.source_kind,
        intended_use=declaration.intended_use,
        snapshot_sha256=digest,
        declaration_sha256=manifest_digest,
        captured_on=declaration.captured_on,
        inspected_on=inspected_on,
        retention_days=declaration.retention_days,
        record_count=record_count,
        availability_evidence_declared=vintage_ref is not None,
    )
