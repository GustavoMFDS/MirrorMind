"""Review packets bind existing in-memory data to unverified references."""
from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime
from hashlib import sha256
from io import BytesIO

import pytest
from openpyxl import Workbook

from mirrormind.domains.retail.uci_workbook import read_uci_workbook
from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot

CAPTURED = date(2026, 11, 18)
INSPECTED = date(2026, 11, 21)


def csv_stage():
    raw = (
        b"series_id,observed_on,available_on,units\n"
        b"SECRET-SERIES,2011-01-05,2011-01-08,7\n"
    )
    return stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())


def workbook_stage():
    book = Workbook()
    sheet = book.active
    sheet.title = "Online Retail"
    sheet.append((
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country",
    ))
    sheet.append((
        "536365", "PRIVATE-SKU", "DO-NOT-LEAK", 3,
        datetime(2011, 1, 5, 8), 2.25, 987654, "UK",
    ))
    buffer = BytesIO()
    book.save(buffer)
    book.close()
    raw = buffer.getvalue()
    return read_uci_workbook(
        BytesIO(raw), expected_sha256=sha256(raw).hexdigest(),
    )


def declaration(stage, kind="daily_csv", **overrides):
    fields = {
        "source_kind": kind,
        "source_record_ref": "SOURCE_REVIEW_001",
        "snapshot_sha256": stage.sha256_hex,
        "license_evidence_ref": "LICENSE_NOTE_001",
        "permission_evidence_ref": "RIGHTS_REVIEW_001",
        "privacy_review_ref": "PRIVACY_REVIEW_001",
        "intended_use": "research_evaluation",
        "retention_days": 45,
        "captured_on": CAPTURED,
    }
    fields.update(overrides)
    return SourceReviewDeclaration(**fields)


def test_staged_csv_packet_is_digest_bound_but_never_permission_approval():
    stage = csv_stage()
    declared = declaration(stage)
    result = prepare_source_review_packet(stage, declared, inspected_on=INSPECTED)
    receipt = result.receipt()
    assert receipt["status"] == "source_intake_requires_independent_human_review"
    assert receipt["snapshot_sha256"] == stage.sha256_hex
    assert receipt["record_count"] == 1
    assert receipt["permission_status"] == "not_verified_no_ingestion"
    assert receipt["historical_availability_status"] == "not_verified_no_asof_claim"
    assert receipt["evidence_reference_status"] == "caller_declared_not_authenticated"
    assert receipt["ingestion_authorized"] is False
    assert receipt["forecast_eligible"] is False
    assert receipt["human_review_required"] is True
    assert len(receipt["declaration_sha256"]) == 64
    for private in ("SECRET-SERIES", "SOURCE_REVIEW_001", "LICENSE_NOTE_001",
                    "RIGHTS_REVIEW_001", "PRIVACY_REVIEW_001"):
        assert private not in str(receipt)
    with pytest.raises(FrozenInstanceError):
        result.retention_days = 999


def test_uci_xlsx_packet_preserves_unknown_vintages_and_customer_minimization():
    stage = workbook_stage()
    declared = declaration(
        stage, kind="uci_xlsx", intended_use="commercial_product",
        availability_evidence_ref="VINTAGE_REVIEW_001",
    )
    result = prepare_source_review_packet(stage, declared, inspected_on=INSPECTED)
    receipt = result.receipt()
    assert receipt["source_kind"] == "uci_xlsx"
    assert receipt["intended_use"] == "commercial_product"
    assert receipt["record_count"] == 1
    assert receipt["availability_evidence_declared"] is True
    assert receipt["historical_availability_status"] == "not_verified_no_asof_claim"
    assert receipt["ingestion_authorized"] is False
    for private in ("536365", "PRIVATE-SKU", "DO-NOT-LEAK", "987654",
                    "VINTAGE_REVIEW_001", "RIGHTS_REVIEW_001"):
        assert private not in str(receipt)


def test_manifest_is_stable_but_sensitive_to_review_reference_and_requested_use():
    stage = csv_stage()
    standard = declaration(stage)
    again = prepare_source_review_packet(stage, standard, inspected_on=INSPECTED)
    assert again == prepare_source_review_packet(stage, standard, inspected_on=INSPECTED)
    alternate = replace(standard, permission_evidence_ref="RIGHTS_REVIEW_002")
    commercial = replace(standard, intended_use="commercial_product")
    other_retention = replace(standard, retention_days=30)
    assert len({
        prepare_source_review_packet(stage, item, inspected_on=INSPECTED).declaration_sha256
        for item in (standard, alternate, commercial, other_retention)
    }) == 4


@pytest.mark.parametrize("modifications,error", [
    ({"source_kind": "uci_xlsx"}, "source kind"),
    ({"source_kind": "untrusted_http"}, "source kind"),
    ({"snapshot_sha256": "0" * 64}, "does not match"),
    ({"snapshot_sha256": "bad-digest"}, "snapshot SHA-256"),
    ({"snapshot_sha256": "A" * 64}, "snapshot SHA-256"),
    ({"source_record_ref": "https://example.com/token?key=SECRET"}, "reference"),
    ({"license_evidence_ref": ""}, "reference"),
    ({"permission_evidence_ref": "password=SECRET"}, "reference"),
    ({"privacy_review_ref": None}, "reference"),
    ({"availability_evidence_ref": "REF/../../../secret"}, "availability"),
    ({"intended_use": "unknown_use"}, "intended use"),
    ({"retention_days": True}, "retention"),
    ({"retention_days": 0}, "retention"),
    ({"retention_days": 3651}, "retention"),
    ({"captured_on": datetime(2026, 11, 18)}, "exact calendar"),
    ({"captured_on": date(2027, 1, 1)}, "after inspection"),
])
def test_review_packet_fails_closed_for_invalid_claims(modifications, error):
    stage = csv_stage()
    with pytest.raises(ValueError, match=error) as raised:
        prepare_source_review_packet(
            stage, declaration(stage, **modifications), inspected_on=INSPECTED
        )
    assert "SECRET" not in str(raised.value)


def test_review_packet_rejects_wrong_stage_and_bad_inspection_calendar():
    stage = csv_stage()
    declared = declaration(stage)
    with pytest.raises(ValueError, match="supported staged"):
        prepare_source_review_packet(object(), declared, inspected_on=INSPECTED)
    with pytest.raises(ValueError, match="exact calendar"):
        prepare_source_review_packet(
            stage, declared, inspected_on=datetime(2026, 11, 21)
        )
    with pytest.raises(ValueError, match="source review declaration"):
        prepare_source_review_packet(stage, object(), inspected_on=INSPECTED)


def test_source_digest_cannot_be_swapped_for_different_csv_contents():
    original = csv_stage()
    changed_bytes = (
        b"series_id,observed_on,available_on,units\n"
        b"SECRET-SERIES,2011-01-05,2011-01-08,8\n"
    )
    changed = stage_csv_snapshot(
        changed_bytes, expected_sha256=sha256(changed_bytes).hexdigest()
    )
    declared = declaration(original)
    with pytest.raises(ValueError, match="does not match"):
        prepare_source_review_packet(changed, declared, inspected_on=INSPECTED)
