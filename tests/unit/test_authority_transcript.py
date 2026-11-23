"""Purely fictional witness transcript, handoff, replay and outage regressions."""
from dataclasses import FrozenInstanceError, replace
from datetime import date
from hashlib import sha256

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.authority_transcript import (
    SignedAuthorityReceipt,
    WitnessKeyHandoff,
    _canonical_authority_receipt_message,
    _canonical_handoff_message,
    verify_authority_transcript,
)
from mirrormind.modules.evidence.head_checkpoints import (
    SignedReviewHeadCheckpoint,
    _canonical_checkpoint_message,
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

TODAY = date(2026, 11, 21)
ZERO = "0" * 64


def signer(key_id):
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return private, {key_id: public}


def make_packet(units=7):
    raw = (
        b"series_id,observed_on,available_on,units\n"
        + f"PRIVATE-SERIES,2011-01-05,2011-01-08,{units}\n".encode()
    )
    staged = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
    declared = SourceReviewDeclaration(
        source_kind="daily_csv", source_record_ref="SOURCE_REVIEW_001",
        snapshot_sha256=staged.sha256_hex, license_evidence_ref="LICENSE_NOTE_001",
        permission_evidence_ref="RIGHTS_REVIEW_001",
        privacy_review_ref="PRIVACY_REVIEW_001",
        intended_use="research_evaluation", retention_days=45,
        captured_on=date(2026, 11, 18),
    )
    return prepare_source_review_packet(
        staged, declared, inspected_on=date(2026, 11, 19)
    )


def review_event(packet, private, *, sequence=1, previous=GENESIS_HEAD,
                 decision="approve"):
    value = SignedReviewDecision(
        review_ref=f"REVIEW_EVENT_{sequence:03}", reviewer_key_id="REVIEW_KEY_001",
        sequence=sequence, previous_head_sha256=previous,
        packet_sha256=packet.declaration_sha256,
        snapshot_sha256=packet.snapshot_sha256,
        source_kind=packet.source_kind, intended_use=packet.intended_use,
        decision=decision,
        decided_on=date(2026, 11, 20) if sequence == 1 else TODAY,
        expires_on=date(2026, 12, 20) if decision == "approve" else None,
        signature_hex="0" * 128,
    )
    return replace(value, signature_hex=private.sign(
        _canonical_review_message(value)
    ).hex())


def checkpoint(packet, private, revision, head, sequence, issued_on):
    value = SignedReviewHeadCheckpoint(
        anchor_key_id="ANCHOR_KEY_001",
        packet_sha256=packet.declaration_sha256,
        snapshot_sha256=packet.snapshot_sha256,
        source_kind=packet.source_kind,
        intended_use=packet.intended_use,
        review_revision=revision, review_head_sha256=head,
        anchor_sequence=sequence, issued_on=issued_on,
        expires_on=date(2026, 11, 25),
        signature_hex="0" * 128,
    )
    return replace(value, signature_hex=private.sign(
        _canonical_checkpoint_message(value)
    ).hex())


def witnessed(check, private, key_id, epoch, previous):
    value = SignedAuthorityReceipt(
        checkpoint=check, witness_key_id=key_id, key_epoch=epoch,
        previous_receipt_sha256=previous, witness_signature_hex="0" * 128,
    )
    signed = replace(value, witness_signature_hex=private.sign(
        _canonical_authority_receipt_message(value)
    ).hex())
    digest = sha256(
        _canonical_authority_receipt_message(signed)
        + bytes.fromhex(signed.witness_signature_hex)
    ).hexdigest()
    return signed, digest


def handoff(old, new, prior_hash, *, sequence=2):
    value = WitnessKeyHandoff(
        previous_key_id="WITNESS_OLD", new_key_id="WITNESS_NEW",
        previous_epoch=1, new_epoch=2,
        effective_sequence=sequence, previous_receipt_sha256=prior_hash,
        old_signature_hex="0" * 128, new_signature_hex="0" * 128,
    )
    message = _canonical_handoff_message(value)
    return replace(value, old_signature_hex=old.sign(message).hex(),
                   new_signature_hex=new.sign(message).hex())


def scenario(tmp_path, *, rotate=False):
    packet = make_packet()
    reviewer, reviewer_keys = signer("REVIEW_KEY_001")
    anchor, anchor_keys = signer("ANCHOR_KEY_001")
    old, old_keys = signer("WITNESS_OLD")
    new, new_keys = signer("WITNESS_NEW")
    witnesses = {**old_keys, **new_keys}
    registry = SQLiteReviewRegistry(tmp_path / "review.db", reviewer_keys, create=True)
    approval = registry.append(
        packet, review_event(packet, reviewer),
        expected_revision=0, expected_head_sha256=GENESIS_HEAD, checked_on=TODAY,
    )
    before = checkpoint(
        packet, anchor, 1, approval.log_head_sha256, 1, date(2026, 11, 20)
    )
    first, first_hash = witnessed(before, old, "WITNESS_OLD", 1, ZERO)
    revoked = registry.append(
        packet, review_event(
            packet, reviewer, sequence=2, previous=approval.log_head_sha256,
            decision="revoke",
        ), expected_revision=1, expected_head_sha256=approval.log_head_sha256,
        checked_on=TODAY,
    )
    after = checkpoint(packet, anchor, 2, revoked.log_head_sha256, 2, TODAY)
    second, last_hash = witnessed(
        after, new if rotate else old,
        "WITNESS_NEW" if rotate else "WITNESS_OLD",
        2 if rotate else 1, first_hash,
    )
    handoffs = (handoff(old, new, first_hash),) if rotate else ()
    return packet, registry, (first, second), handoffs, anchor_keys, witnesses, last_hash


def check(case, *, receipts=None, handoffs=None, floor=0, start_hash=ZERO,
          start_key="WITNESS_OLD", start_epoch=1, current_sequence=2,
          current_hash=None, keys=None, anchor_keys=None, when=TODAY):
    packet, registry, original, transfers, checkpoint_keys, witness_keys, final = case
    return verify_authority_transcript(
        registry, packet, original if receipts is None else receipts,
        transfers if handoffs is None else handoffs,
        trusted_checkpoint_keys=checkpoint_keys if anchor_keys is None else anchor_keys,
        trusted_witness_keys=witness_keys if keys is None else keys,
        previous_sequence=floor,
        previous_receipt_sha256=start_hash,
        previous_witness_key_id=start_key,
        previous_key_epoch=start_epoch,
        expected_current_sequence=current_sequence,
        expected_current_receipt_sha256=final if current_hash is None else current_hash,
        checked_on=when,
    )


@pytest.mark.parametrize("rotate", [False, True])
def test_contiguous_signed_authority_transcript_and_rotation_are_nonauthorizing(tmp_path, rotate):
    case = scenario(tmp_path, rotate=rotate)
    result = check(case)
    receipt = result.receipt()
    assert receipt["validated_receipts"] == 2
    assert receipt["current_sequence"] == 2
    assert receipt["review_status"] == "revoked_blocks_reapproval_of_same_packet"
    assert receipt["ingestion_authorized"] is False
    assert receipt["forecast_eligible"] is False
    assert receipt["freshness_status"] == "caller_fences_not_independently_fetched"
    assert receipt["equivocation_status"] == "only_conflicts_in_supplied_chain_detectable"
    for secret in ("PRIVATE-SERIES", "SOURCE_REVIEW_001", "WITNESS_OLD",
                   "WITNESS_NEW", "ANCHOR_KEY_001"):
        assert secret not in str(receipt)
    with pytest.raises(FrozenInstanceError):
        result.current_sequence = 42


def test_outage_empty_or_incomplete_recovery_transcript_fails_closed(tmp_path):
    case = scenario(tmp_path)
    with pytest.raises(ValueError, match="transcript missing"):
        check(case, receipts=())
    with pytest.raises(ValueError, match="gap|replay|predecessor"):
        check(case, receipts=(case[2][-1],))
    with pytest.raises(ValueError, match="expected current"):
        check(case, receipts=(case[2][0],), current_sequence=2)


def test_stale_expected_end_fence_and_altered_start_fence_rejected(tmp_path):
    case = scenario(tmp_path)
    with pytest.raises(ValueError, match="expected current"):
        check(case, current_sequence=3)
    with pytest.raises(ValueError, match="expected current"):
        check(case, current_hash="f" * 64)
    with pytest.raises(ValueError, match="gap|replay|predecessor"):
        check(case, start_hash="f" * 64)


def test_repeated_sequence_and_conflicting_signed_head_are_detectable_if_both_seen(tmp_path):
    case = scenario(tmp_path)
    first, second = case[2]
    duplicate = replace(second, checkpoint=first.checkpoint)
    with pytest.raises(ValueError, match="gap|replay|predecessor"):
        check(case, receipts=(first, duplicate))
    # One isolated signed fork may be valid with self-consistent untrusted
    # fences. Such unseen equivocation CANNOT be ruled out by this verifier.
    assert check(case).current_sequence == 2


def test_tampered_witness_signature_cannot_alter_fenced_chain(tmp_path):
    case = scenario(tmp_path)
    first, second = case[2]
    tampered = replace(second, witness_signature_hex="a" * 128)
    with pytest.raises(ValueError, match="signature invalid"):
        check(case, receipts=(first, tampered))


def test_tampered_checkpoint_signature_fails_even_with_witness_signature(tmp_path):
    case = scenario(tmp_path)
    first, second = case[2]
    tampered = replace(
        second, checkpoint=replace(second.checkpoint, signature_hex="b" * 128)
    )
    with pytest.raises(ValueError, match="checkpoint signature failed"):
        check(case, receipts=(first, tampered))


def test_switching_witness_key_without_dual_signed_handoff_fails(tmp_path):
    case = scenario(tmp_path, rotate=True)
    with pytest.raises(ValueError, match="handoff"):
        check(case, handoffs=())


def test_wrong_old_or_new_handoff_signature_fails(tmp_path):
    case = scenario(tmp_path, rotate=True)
    transfer = case[3][0]
    for mutation in (
        {"old_signature_hex": "a" * 128},
        {"new_signature_hex": "b" * 128},
    ):
        with pytest.raises(ValueError, match="signature invalid"):
            check(case, handoffs=(replace(transfer, **mutation),))


def test_handoff_wrong_predecessor_and_extra_handoffs_fail(tmp_path):
    case = scenario(tmp_path, rotate=True)
    transfer = case[3][0]
    with pytest.raises(ValueError, match="handoff"):
        check(case, handoffs=(replace(transfer, previous_receipt_sha256="f" * 64),))
    with pytest.raises(ValueError, match="handoff|unused|conflicting"):
        check(case, handoffs=(transfer, transfer))


def test_same_key_cannot_silently_increment_epoch(tmp_path):
    case = scenario(tmp_path)
    first, second = case[2]
    with pytest.raises(ValueError, match="rotation"):
        check(case, receipts=(first, replace(second, key_epoch=2)))


def test_packet_scope_and_review_head_mismatch_are_denied(tmp_path):
    case = scenario(tmp_path)
    wrong_packet = make_packet(units=8)
    with pytest.raises(ValueError, match="source identity"):
        verify_authority_transcript(
            case[1], wrong_packet, case[2], (),
            trusted_checkpoint_keys=case[4], trusted_witness_keys=case[5],
            previous_sequence=0, previous_receipt_sha256=ZERO,
            previous_witness_key_id="WITNESS_OLD", previous_key_epoch=1,
            expected_current_sequence=2, expected_current_receipt_sha256=case[6],
            checked_on=TODAY,
        )


def test_expired_latest_receipt_blocks_recovery(tmp_path):
    case = scenario(tmp_path)
    with pytest.raises(ValueError, match="expired"):
        check(case, when=date(2026, 11, 26))


def test_missing_trust_roots_and_invalid_current_metadata_fail(tmp_path):
    case = scenario(tmp_path)
    with pytest.raises(ValueError, match="trusted checkpoint and witness"):
        check(case, keys={})
    with pytest.raises(ValueError, match="trusted checkpoint and witness"):
        check(case, anchor_keys={})
    with pytest.raises(ValueError, match="invalid externally supplied"):
        check(case, current_hash="not-a-hash")
    with pytest.raises(ValueError, match="invalid externally supplied"):
        check(case, floor=True)


def test_valid_stale_transcript_with_caller_stale_fences_cannot_prove_freshness(tmp_path):
    case = scenario(tmp_path)
    # A local check with static fences can be replayed indefinitely within
    # the validity window. No live externally published current head exists.
    assert check(case).current_receipt_sha256 == check(case).current_receipt_sha256
    assert check(case).receipt()["ingestion_authorized"] is False
