"""Synthetic signed-head checkpoints against local SQLite signed decisions."""
import shutil
from dataclasses import FrozenInstanceError, replace
from datetime import date
from hashlib import sha256

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.head_checkpoints import (
    SignedReviewHeadCheckpoint,
    _canonical_checkpoint_message,
    compare_sqlite_to_signed_checkpoint,
)
from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SignedReviewDecision,
    _canonical_review_message,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry

CHECKED = date(2026, 11, 21)


def invented_packet(*, units=7, intended_use="research_evaluation"):
    rows = (
        b"series_id,observed_on,available_on,units\n"
        + f"PRIVATE-SERIES,2011-01-05,2011-01-08,{units}\n".encode()
    )
    staged = stage_csv_snapshot(rows, expected_sha256=sha256(rows).hexdigest())
    declaration = SourceReviewDeclaration(
        source_kind="daily_csv", source_record_ref="SOURCE_REVIEW_001",
        snapshot_sha256=staged.sha256_hex,
        license_evidence_ref="LICENSE_NOTE_001",
        permission_evidence_ref="RIGHTS_REVIEW_001",
        privacy_review_ref="PRIVACY_REVIEW_001",
        intended_use=intended_use, retention_days=45,
        captured_on=date(2026, 11, 18),
    )
    return prepare_source_review_packet(staged, declaration, inspected_on=date(2026, 11, 19))


def ephemeral_signer(key_id):
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return private, {key_id: public}


def signed_review(packet, signer, *, sequence=1, prior=GENESIS_HEAD, decision="approve"):
    event = SignedReviewDecision(
        review_ref=f"REVIEW_EVENT_{sequence:03}",
        reviewer_key_id="REVIEW_KEY_001", sequence=sequence,
        previous_head_sha256=prior, packet_sha256=packet.declaration_sha256,
        snapshot_sha256=packet.snapshot_sha256, source_kind=packet.source_kind,
        intended_use=packet.intended_use, decision=decision,
        decided_on=date(2026, 11, 20) if sequence == 1 else CHECKED,
        expires_on=date(2026, 12, 20) if decision == "approve" else None,
        signature_hex="0" * 128,
    )
    return replace(event, signature_hex=signer.sign(_canonical_review_message(event)).hex())


def checkpoint_for(packet, signer, *, revision, head, sequence=1, **changes):
    fields = {
        "anchor_key_id": "ANCHOR_KEY_001",
        "packet_sha256": packet.declaration_sha256,
        "snapshot_sha256": packet.snapshot_sha256,
        "source_kind": packet.source_kind,
        "intended_use": packet.intended_use,
        "review_revision": revision,
        "review_head_sha256": head,
        "anchor_sequence": sequence,
        "issued_on": date(2026, 11, 20),
        "expires_on": date(2026, 11, 25),
        "signature_hex": "0" * 128,
    }
    fields.update(changes)
    draft = SignedReviewHeadCheckpoint(**fields)
    return replace(
        draft, signature_hex=signer.sign(_canonical_checkpoint_message(draft)).hex()
    )


def store_with_approval(tmp_path):
    packet = invented_packet()
    reviewer, review_keys = ephemeral_signer("REVIEW_KEY_001")
    authority, anchor_keys = ephemeral_signer("ANCHOR_KEY_001")
    registry = SQLiteReviewRegistry(tmp_path / "reviews.db", review_keys, create=True)
    initial = registry.append(
        packet, signed_review(packet, reviewer),
        expected_revision=0, expected_head_sha256=GENESIS_HEAD,
        checked_on=CHECKED,
    )
    return packet, registry, reviewer, authority, anchor_keys, initial


def compare(registry, packet, checkpoint, anchor_keys, floor=1, when=CHECKED):
    return compare_sqlite_to_signed_checkpoint(
        registry, packet, checkpoint, trusted_anchor_keys=anchor_keys,
        minimum_anchor_sequence=floor, checked_on=when,
    )


def test_separately_signed_checkpoint_matches_exact_sqlite_head_without_authorizing(tmp_path):
    packet, registry, _, authority, keys, current = store_with_approval(tmp_path)
    signed = checkpoint_for(
        packet, authority, revision=current.revision,
        head=current.log_head_sha256, sequence=7,
    )
    receipt = compare(registry, packet, signed, keys, floor=7).receipt()
    assert receipt["review_revision"] == 1
    assert receipt["review_head_sha256"] == current.log_head_sha256
    assert receipt["review_status"] == "signed_approval_record_verified_not_legal_permission"
    assert receipt["anchor_sequence"] == 7
    assert receipt["ingestion_authorized"] is False
    assert receipt["forecast_eligible"] is False
    assert receipt["freshness_status"] == (
        "caller_supplied_high_water_not_independently_checked"
    )
    for identifier in ("PRIVATE-SERIES", "SOURCE_REVIEW_001", "ANCHOR_KEY_001"):
        assert identifier not in str(receipt)
    result = compare(registry, packet, signed, keys, floor=7)
    with pytest.raises(FrozenInstanceError):
        result.review_revision = 100


def test_restored_older_sqlite_is_rejected_against_newer_independent_signed_head(tmp_path):
    packet, registry, reviewer, authority, keys, approval = store_with_approval(tmp_path)
    backup_path = tmp_path / "older.db"
    shutil.copyfile(tmp_path / "reviews.db", backup_path)
    older_checkpoint = checkpoint_for(
        packet, authority, revision=1,
        head=approval.log_head_sha256, sequence=1,
    )
    revocation = signed_review(
        packet, reviewer, sequence=2,
        prior=approval.log_head_sha256, decision="revoke",
    )
    new_state = registry.append(
        packet, revocation, expected_revision=1,
        expected_head_sha256=approval.log_head_sha256, checked_on=CHECKED,
    )
    newer_checkpoint = checkpoint_for(
        packet, authority, revision=2,
        head=new_state.log_head_sha256, sequence=2,
    )
    restored = SQLiteReviewRegistry(backup_path, registry._keys)
    # Old signed history and its old checkpoint are internally consistent.
    assert compare(restored, packet, older_checkpoint, keys).review_revision == 1
    # An independently retained current sequence 2 rejects old checkpoint.
    with pytest.raises(ValueError, match="sequence floor"):
        compare(restored, packet, older_checkpoint, keys, floor=2)
    # The latest signed head also rejects the restored stale SQLite file.
    with pytest.raises(ValueError, match="externally trusted log head"):
        compare(restored, packet, newer_checkpoint, keys, floor=2)
    verified = compare(registry, packet, newer_checkpoint, keys, floor=2)
    assert verified.review_status == "revoked_blocks_reapproval_of_same_packet"
    assert verified.receipt()["ingestion_authorized"] is False


def test_older_valid_checkpoint_replay_is_not_prevented_if_high_water_is_stale(tmp_path):
    packet, registry, _, authority, keys, first = store_with_approval(tmp_path)
    checkpoint = checkpoint_for(
        packet, authority, revision=1, head=first.log_head_sha256,
        sequence=1,
    )
    # Re-running the same signed checkpoint with an unchanged caller-provided
    # floor remains valid. Only an external fresh minimum can detect replay.
    assert compare(registry, packet, checkpoint, keys, floor=1).anchor_sequence == 1
    assert compare(registry, packet, checkpoint, keys, floor=1).anchor_sequence == 1


def test_absent_review_history_has_only_genesis_checkpoint_without_permission(tmp_path):
    packet = invented_packet()
    _, reviewer_keys = ephemeral_signer("REVIEW_KEY_001")
    authority, anchor_keys = ephemeral_signer("ANCHOR_KEY_001")
    registry = SQLiteReviewRegistry(tmp_path / "empty.db", reviewer_keys, create=True)
    checkpoint = checkpoint_for(
        packet, authority, revision=0, head=GENESIS_HEAD, sequence=1,
    )
    receipt = compare(registry, packet, checkpoint, anchor_keys).receipt()
    assert receipt["review_status"] == "missing_review_record"
    assert receipt["ingestion_authorized"] is False


@pytest.mark.parametrize("mutation,match", [
    ({"packet_sha256": "f" * 64}, "source identity"),
    ({"snapshot_sha256": "f" * 64}, "source identity"),
    ({"source_kind": "uci_xlsx"}, "source identity"),
    ({"intended_use": "commercial_product"}, "source identity"),
    ({"anchor_key_id": "SOME_OTHER_KEY"}, "unknown external anchor"),
    ({"anchor_key_id": "url:/private"}, "metadata"),
    ({"anchor_sequence": True}, "sequence floor"),
    ({"anchor_sequence": 0}, "sequence floor"),
    ({"review_revision": True}, "revision"),
    ({"review_revision": 65}, "revision"),
    ({"review_revision": 0}, "revision"),
    ({"review_head_sha256": GENESIS_HEAD}, "revision"),
    ({"review_head_sha256": "x" * 64}, "metadata"),
    ({"issued_on": date(2026, 11, 22)}, "validity dates"),
    ({"expires_on": date(2026, 11, 20)}, "validity dates"),
    ({"expires_on": date(2027, 1, 1)}, "validity dates"),
])
def test_invalid_or_mismatched_checkpoint_claims_fail_closed(tmp_path, mutation, match):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    checkpoint = checkpoint_for(
        packet, authority, revision=1,
        head=state.log_head_sha256, **mutation,
    )
    with pytest.raises(ValueError, match=match):
        compare(registry, packet, checkpoint, keys)


def test_signed_revision_or_head_mismatch_with_sqlite_is_rejected(tmp_path):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    signed_revision = checkpoint_for(
        packet, authority, revision=2, head=state.log_head_sha256,
    )
    with pytest.raises(ValueError, match="revision"):
        compare(registry, packet, signed_revision, keys)
    other_head = checkpoint_for(
        packet, authority, revision=1, head="f" * 64,
    )
    with pytest.raises(ValueError, match="externally trusted log head"):
        compare(registry, packet, other_head, keys)


def test_tampered_signature_and_wrong_authority_key_fail(tmp_path):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    original = checkpoint_for(
        packet, authority, revision=1, head=state.log_head_sha256,
    )
    tampered = replace(original, signature_hex="b" * 128)
    with pytest.raises(ValueError, match="signature failed"):
        compare(registry, packet, tampered, keys)
    _, unrelated = ephemeral_signer("ANCHOR_KEY_001")
    with pytest.raises(ValueError, match="signature failed"):
        compare(registry, packet, original, unrelated)
    with pytest.raises(ValueError, match="trusted external anchor"):
        compare(registry, packet, original, {})


def test_scope_change_cannot_reuse_signed_checkpoint(tmp_path):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    original = checkpoint_for(
        packet, authority, revision=1, head=state.log_head_sha256,
    )
    for other in (invented_packet(units=8), invented_packet(intended_use="commercial_product")):
        with pytest.raises(ValueError, match="source identity"):
            compare(registry, other, original, keys)


@pytest.mark.parametrize("floor", [0, True, -1, 1_000_000_001, 10])
def test_invalid_or_newer_external_high_water_fails_closed(tmp_path, floor):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    checkpoint = checkpoint_for(
        packet, authority, revision=1, head=state.log_head_sha256, sequence=2,
    )
    with pytest.raises(ValueError, match="sequence floor"):
        compare(registry, packet, checkpoint, keys, floor=floor)


def test_expiry_is_checked_each_time_even_if_signature_still_valid(tmp_path):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    checkpoint = checkpoint_for(
        packet, authority, revision=1, head=state.log_head_sha256,
    )
    with pytest.raises(ValueError, match="expired"):
        compare(registry, packet, checkpoint, keys, when=date(2026, 11, 26))


def test_reviewer_signature_cannot_be_reused_as_checkpoint_signature(tmp_path):
    packet, registry, reviewer, authority, keys, state = store_with_approval(tmp_path)
    check = checkpoint_for(packet, authority, revision=1, head=state.log_head_sha256)
    event = signed_review(packet, reviewer)
    wrong = replace(check, signature_hex=event.signature_hex)
    with pytest.raises(ValueError, match="signature failed"):
        compare(registry, packet, wrong, keys)


def test_untrusted_anchor_map_rejects_invalid_public_key_shape(tmp_path):
    packet, registry, _, authority, _, state = store_with_approval(tmp_path)
    checkpoint = checkpoint_for(packet, authority, revision=1, head=state.log_head_sha256)
    with pytest.raises(ValueError, match="anchor key configuration"):
        compare(registry, packet, checkpoint, {"ANCHOR_KEY_001": b"short"})


def test_minimum_requires_non_requested_current_source_of_freshness(tmp_path):
    packet, registry, _, authority, keys, state = store_with_approval(tmp_path)
    checkpoint = checkpoint_for(
        packet, authority, revision=1, head=state.log_head_sha256, sequence=4,
    )
    assert compare(registry, packet, checkpoint, keys, floor=4).anchor_sequence == 4
    with pytest.raises(ValueError, match="sequence floor"):
        compare(registry, packet, checkpoint, keys, floor=5)
