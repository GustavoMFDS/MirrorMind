"""Adversarial tests for the process-local source-review revision store."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
from datetime import date
from hashlib import sha256

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.local_review_registry import (
    GENESIS_HEAD,
    LocalReviewRegistry,
)
from mirrormind.modules.evidence.review_decisions import (
    SignedReviewDecision,
    _canonical_review_message,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot

INSPECTED = date(2026, 11, 19)
CHECKED = date(2026, 11, 21)


def source_packet(units=7, use="research_evaluation"):
    rows = (
        b"series_id,observed_on,available_on,units\n"
        + f"PRIVATE-SERIES,2011-01-05,2011-01-08,{units}\n".encode()
    )
    staged = stage_csv_snapshot(rows, expected_sha256=sha256(rows).hexdigest())
    fields = SourceReviewDeclaration(
        source_kind="daily_csv", source_record_ref="SOURCE_REVIEW_001",
        snapshot_sha256=staged.sha256_hex,
        license_evidence_ref="LICENSE_NOTE_001",
        permission_evidence_ref="RIGHTS_REVIEW_001",
        privacy_review_ref="PRIVACY_REVIEW_001",
        intended_use=use, retention_days=45,
        captured_on=date(2026, 11, 18),
    )
    return prepare_source_review_packet(staged, fields, inspected_on=INSPECTED)


def temporary_signer():
    signer = Ed25519PrivateKey.generate()
    public_key = signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return signer, {"REVIEW_KEY_001": public_key}


def signed(packet, signer, *, sequence=1, previous_head=GENESIS_HEAD,
           decision="approve", review_ref=None):
    entry = SignedReviewDecision(
        review_ref=review_ref or f"REVIEW_EVENT_{sequence:03}",
        reviewer_key_id="REVIEW_KEY_001",
        sequence=sequence, previous_head_sha256=previous_head,
        packet_sha256=packet.declaration_sha256,
        snapshot_sha256=packet.snapshot_sha256,
        source_kind=packet.source_kind,
        intended_use=packet.intended_use,
        decision=decision,
        decided_on=date(2026, 11, 20) if sequence == 1 else CHECKED,
        expires_on=date(2026, 12, 20) if decision == "approve" else None,
        signature_hex="0" * 128,
    )
    return replace(entry, signature_hex=signer.sign(_canonical_review_message(entry)).hex())


def test_atomic_append_and_read_preserve_revision_digest_and_never_authorize():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    start = registry.snapshot(packet, checked_on=CHECKED)
    assert start.revision == 0
    assert start.log_head_sha256 == GENESIS_HEAD
    assert start.review_status == "missing_review_record"

    approval = signed(packet, signer)
    current = registry.append(
        packet, approval, expected_revision=0,
        expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED,
    )
    assert current.revision == 1
    assert current.log_head_sha256 != GENESIS_HEAD
    assert current.review_status == "signed_approval_record_verified_not_legal_permission"
    assert registry.snapshot(packet, checked_on=CHECKED) == current
    receipt = current.receipt()
    assert receipt["ingestion_authorized"] is False
    assert receipt["forecast_eligible"] is False
    assert receipt["head_trust_status"] == "local_not_independently_attested"
    assert receipt["persistence_status"] == "process_memory_only_lost_on_restart"
    for private in ("PRIVATE-SERIES", "SOURCE_REVIEW_001",
                    "REVIEW_EVENT_001", "REVIEW_KEY_001"):
        assert private not in str(receipt)
    with pytest.raises(FrozenInstanceError):
        current.revision = 99


def test_revocation_is_terminal_and_old_head_cannot_rewrite_current_state():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    approval = signed(packet, signer)
    one = registry.append(packet, approval, expected_revision=0,
                          expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    revocation = signed(packet, signer, sequence=2,
                        previous_head=one.log_head_sha256, decision="revoke")
    two = registry.append(packet, revocation, expected_revision=1,
                          expected_head_sha256=one.log_head_sha256, checked_on=CHECKED)
    assert two.revision == 2
    assert two.review_status == "revoked_blocks_reapproval_of_same_packet"

    with pytest.raises(ValueError, match="stale"):
        registry.append(packet, approval, expected_revision=0,
                        expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    renewed = signed(packet, signer, sequence=3, previous_head=two.log_head_sha256)
    with pytest.raises(ValueError, match="revoked"):
        registry.append(packet, renewed, expected_revision=2,
                        expected_head_sha256=two.log_head_sha256, checked_on=CHECKED)
    assert registry.snapshot(packet, checked_on=CHECKED) == two


@pytest.mark.parametrize("revision,head", [
    (True, GENESIS_HEAD),
    (-1, GENESIS_HEAD),
    (0, "f" * 64),
    (1, GENESIS_HEAD),
    (0, "invalid"),
])
def test_stale_or_invalid_expected_version_and_head_fail_closed(revision, head):
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    event = signed(packet, signer)
    with pytest.raises(ValueError, match="stale"):
        registry.append(packet, event, expected_revision=revision,
                        expected_head_sha256=head, checked_on=CHECKED)
    assert registry.snapshot(packet, checked_on=CHECKED).revision == 0


def test_invalid_signature_fails_without_mutating_the_registry():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    forged = replace(signed(packet, signer), signature_hex="a" * 128)
    with pytest.raises(ValueError, match="signature verification failed"):
        registry.append(packet, forged, expected_revision=0,
                        expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    assert registry.snapshot(packet, checked_on=CHECKED).revision == 0


def test_duplicate_and_wrong_scope_events_rejected_with_unchanged_head():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    one = registry.append(packet, signed(packet, signer), expected_revision=0,
                          expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    for entry in (
        signed(packet, signer),
        signed(source_packet(use="commercial_product"), signer,
               sequence=2, previous_head=one.log_head_sha256),
        signed(source_packet(units=9), signer,
               sequence=2, previous_head=one.log_head_sha256),
    ):
        with pytest.raises(ValueError):
            registry.append(packet, entry, expected_revision=1,
                            expected_head_sha256=one.log_head_sha256,
                            checked_on=CHECKED)
    assert registry.snapshot(packet, checked_on=CHECKED) == one


def test_public_key_configuration_is_frozen_from_caller_mutations():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    public["REVIEW_KEY_001"] = b"x" * 32
    one = registry.append(packet, signed(packet, signer), expected_revision=0,
                          expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    assert one.revision == 1


def test_second_same_revision_writer_loses_atomic_compare_and_swap():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    left = signed(packet, signer, review_ref="REVIEW_EVENT_LEFT")
    right = signed(packet, signer, review_ref="REVIEW_EVENT_RIGHT")

    def append_one(event):
        try:
            registry.append(packet, event, expected_revision=0,
                            expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
            return "won"
        except ValueError:
            return "stale"

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(append_one, (left, right)))
    assert sorted(results) == ["stale", "won"]
    assert registry.snapshot(packet, checked_on=CHECKED).revision == 1


def test_separate_packets_have_isolated_revision_histories():
    first = source_packet()
    second = source_packet(units=9)
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    registry.append(first, signed(first, signer), expected_revision=0,
                    expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    assert registry.snapshot(first, checked_on=CHECKED).revision == 1
    assert registry.snapshot(second, checked_on=CHECKED).revision == 0


def test_same_fingerprint_but_changed_metadata_cannot_alias_review_history():
    first = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    registry.append(first, signed(first, signer), expected_revision=0,
                    expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    # This forged dataclass has an identical digest but different metadata.
    tampered = replace(first, record_count=99)
    with pytest.raises(ValueError, match="different packet metadata"):
        registry.snapshot(tampered, checked_on=CHECKED)


def test_registry_enforces_event_and_packet_budgets(monkeypatch):
    import mirrormind.modules.evidence.local_review_registry as module

    monkeypatch.setattr(module, "MAX_LOCAL_PACKETS", 1)
    monkeypatch.setattr(module, "MAX_EVENTS_PER_PACKET", 1)
    first = source_packet()
    other = source_packet(units=9)
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    one = registry.append(first, signed(first, signer), expected_revision=0,
                          expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    with pytest.raises(ValueError, match="packet budget"):
        registry.append(other, signed(other, signer), expected_revision=0,
                        expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    with pytest.raises(ValueError, match="event budget"):
        registry.append(first, signed(first, signer, sequence=2,
                        previous_head=one.log_head_sha256), expected_revision=1,
                        expected_head_sha256=one.log_head_sha256, checked_on=CHECKED)


def test_new_instance_has_no_rollback_freshness_memory_after_restart():
    packet = source_packet()
    signer, public = temporary_signer()
    active = LocalReviewRegistry(public)
    one = active.append(packet, signed(packet, signer), expected_revision=0,
                        expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    assert one.revision == 1
    restarted = LocalReviewRegistry(public)
    assert restarted.snapshot(packet, checked_on=CHECKED).revision == 0
    assert restarted.snapshot(packet, checked_on=CHECKED).receipt()[
        "ingestion_authorized"
    ] is False


def test_expired_approval_is_recomputed_at_each_read_date():
    packet = source_packet()
    signer, public = temporary_signer()
    registry = LocalReviewRegistry(public)
    entry = signed(packet, signer)
    registry.append(packet, entry, expected_revision=0,
                    expected_head_sha256=GENESIS_HEAD, checked_on=CHECKED)
    later = registry.snapshot(packet, checked_on=date(2027, 1, 2))
    assert later.revision == 1
    assert later.review_status == "signed_approval_expired"
    assert later.receipt()["ingestion_authorized"] is False


@pytest.mark.parametrize("invalid_keys", [
    {},
    {"bad-id": b"x" * 32},
    {"REVIEW_KEY_001": b"short"},
])
def test_registry_rejects_untrusted_key_configuration(invalid_keys):
    with pytest.raises(ValueError, match="trusted reviewer|invalid trusted"):
        LocalReviewRegistry(invalid_keys)
