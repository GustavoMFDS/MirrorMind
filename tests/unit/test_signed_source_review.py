"""Synthetic Ed25519 review-chain tests; never production permission evidence."""
from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime, timedelta
from hashlib import sha256

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SignedReviewDecision,
    _canonical_review_message,
    verify_review_history,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot

TODAY = date(2026, 11, 21)


def packet(*, intended_use="research_evaluation", units=7):
    contents = (
        b"series_id,observed_on,available_on,units\n"
        + f"PRIVATE-SERIES,2011-01-05,2011-01-08,{units}\n".encode()
    )
    staged = stage_csv_snapshot(contents, expected_sha256=sha256(contents).hexdigest())
    declaration = SourceReviewDeclaration(
        source_kind="daily_csv",
        source_record_ref="SOURCE_REVIEW_001",
        snapshot_sha256=staged.sha256_hex,
        license_evidence_ref="LICENSE_NOTE_001",
        permission_evidence_ref="RIGHTS_REVIEW_001",
        privacy_review_ref="PRIVACY_REVIEW_001",
        intended_use=intended_use,
        retention_days=45,
        captured_on=date(2026, 11, 18),
    )
    return prepare_source_review_packet(staged, declaration, inspected_on=date(2026, 11, 19))


def keys():
    signing = Ed25519PrivateKey.generate()
    verifier = signing.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return signing, {"REVIEW_KEY_001": verifier}


def signed_event(
    source_packet, signing, *, decision="approve", sequence=1,
    previous_head=GENESIS_HEAD, decided_on=date(2026, 11, 20),
    expires_on=date(2026, 12, 20), **overrides,
):
    if decision != "approve":
        expires_on = None
    fields = {
        "review_ref": f"REVIEW_EVENT_{sequence:03d}",
        "reviewer_key_id": "REVIEW_KEY_001",
        "sequence": sequence,
        "previous_head_sha256": previous_head,
        "packet_sha256": source_packet.declaration_sha256,
        "snapshot_sha256": source_packet.snapshot_sha256,
        "source_kind": source_packet.source_kind,
        "intended_use": source_packet.intended_use,
        "decision": decision,
        "decided_on": decided_on,
        "expires_on": expires_on,
        "signature_hex": "0" * 128,
    }
    fields.update(overrides)
    draft = SignedReviewDecision(**fields)
    signature = signing.sign(_canonical_review_message(draft))
    signed = replace(draft, signature_hex=signature.hex())
    head = sha256(_canonical_review_message(signed) + signature).hexdigest()
    return signed, head


def verify(source_packet, events, public_keys, expected_head, checked_on=TODAY):
    return verify_review_history(
        source_packet, events, trusted_reviewer_keys=public_keys,
        expected_head_sha256=expected_head, checked_on=checked_on,
    )


def test_valid_signature_is_review_metadata_not_permission_to_ingest():
    source_packet = packet()
    private, public = keys()
    approval, head = signed_event(source_packet, private)
    result = verify(source_packet, (approval,), public, head)
    receipt = result.receipt()
    assert receipt["review_status"] == "signed_approval_record_verified_not_legal_permission"
    assert receipt["log_head_sha256"] == head
    assert receipt["reviewed_events"] == 1
    assert receipt["ingestion_authorized"] is False
    assert receipt["forecast_eligible"] is False
    assert receipt["permission_status"] == "independent_legal_permission_not_verified"
    assert receipt["log_freshness_status"] == "supplied_head_not_independently_attested"
    for identifier in ("PRIVATE-SERIES", "REVIEW_KEY_001", "SOURCE_REVIEW_001",
                       "RIGHTS_REVIEW_001", "REVIEW_EVENT_001"):
        assert identifier not in str(receipt)
    with pytest.raises(FrozenInstanceError):
        result.reviewed_events = 99


def test_signed_revocation_is_terminal_for_same_manifest_even_after_reapproval():
    source_packet = packet()
    signing, public = keys()
    approve, head1 = signed_event(source_packet, signing)
    revoke, head2 = signed_event(
        source_packet, signing, decision="revoke", sequence=2,
        previous_head=head1, decided_on=TODAY,
    )
    result = verify(source_packet, (approve, revoke), public, head2)
    assert result.review_status == "revoked_blocks_reapproval_of_same_packet"
    again, head3 = signed_event(
        source_packet, signing, decision="approve", sequence=3,
        previous_head=head2, decided_on=TODAY,
        expires_on=date(2026, 12, 31),
    )
    assert verify(
        source_packet, (approve, revoke, again), public, head3
    ).review_status == "revoked_blocks_reapproval_of_same_packet"
    assert verify(source_packet, (approve, revoke, again), public, head3).receipt()[
        "ingestion_authorized"
    ] is False


def test_signature_valid_denial_and_expired_approval_block():
    source_packet = packet()
    signing, public = keys()
    deny, head = signed_event(source_packet, signing, decision="deny")
    assert verify(source_packet, (deny,), public, head).review_status == "review_denied"
    approval, head = signed_event(
        source_packet, signing, expires_on=date(2026, 11, 20),
    )
    assert verify(source_packet, (approval,), public, head).review_status == "signed_approval_expired"


def test_absent_review_record_is_not_an_implicit_grant():
    source_packet = packet()
    _, public = keys()
    result = verify(source_packet, (), public, GENESIS_HEAD)
    assert result.review_status == "missing_review_record"
    assert result.receipt()["ingestion_authorized"] is False


@pytest.mark.parametrize("mutation,match", [
    ({"packet_sha256": "f" * 64}, "packet"),
    ({"snapshot_sha256": "f" * 64}, "packet"),
    ({"source_kind": "uci_xlsx"}, "packet"),
    ({"intended_use": "commercial_product"}, "packet"),
    ({"previous_head_sha256": "f" * 64}, "previous head"),
    ({"sequence": 2}, "sequence"),
    ({"reviewer_key_id": "UNKNOWN_KEY_001"}, "signer"),
    ({"review_ref": "url:https://private"}, "reference"),
    ({"signature_hex": "00" * 64}, "signature"),
    ({"decided_on": date(2026, 11, 18)}, "decision date"),
    ({"decided_on": date(2026, 12, 1)}, "decision date"),
    ({"expires_on": date(2026, 11, 20)}, "expiration"),
    ({"expires_on": date(2037, 1, 1)}, "expiration"),
])
def test_mutated_or_invalid_decisions_never_pass(mutation, match):
    source_packet = packet()
    private, public = keys()
    event, head = signed_event(source_packet, private)
    altered = replace(event, **mutation)
    with pytest.raises(ValueError, match=match):
        verify(source_packet, (altered,), public, head)


def test_tampered_signed_metadata_fails_even_with_trusted_key():
    source_packet = packet()
    private, public = keys()
    event, head = signed_event(source_packet, private)
    altered = replace(event, expires_on=date(2026, 12, 21))
    with pytest.raises(ValueError, match="signature verification failed"):
        verify(source_packet, (altered,), public, head)


def test_mismatched_packet_and_intended_use_cannot_reuse_approval():
    source_packet = packet()
    private, public = keys()
    signed, head = signed_event(source_packet, private)
    for changed in (packet(intended_use="commercial_product"), packet(units=8)):
        with pytest.raises(ValueError, match="packet"):
            verify(changed, (signed,), public, head)


def test_unknown_key_or_wrong_public_key_denies_without_payload():
    source_packet = packet()
    private, _ = keys()
    signed, head = signed_event(source_packet, private)
    _, other = keys()
    with pytest.raises(ValueError, match="signature verification failed"):
        verify(source_packet, (signed,), other, head)
    with pytest.raises(ValueError, match="trusted reviewer"):
        verify(source_packet, (signed,), {}, head)


def test_missing_or_old_trusted_log_head_rejects_truncation():
    source_packet = packet()
    private, public = keys()
    approve, head1 = signed_event(source_packet, private)
    revoke, head2 = signed_event(
        source_packet, private, decision="revoke", sequence=2,
        previous_head=head1, decided_on=TODAY,
    )
    with pytest.raises(ValueError, match="externally expected"):
        verify(source_packet, (approve,), public, "bad")
    with pytest.raises(ValueError, match="differs from externally expected"):
        verify(source_packet, (approve,), public, head2)
    with pytest.raises(ValueError, match="differs from externally expected"):
        verify(source_packet, (approve, revoke), public, head1)


def test_reordered_or_gap_or_duplicate_review_events_are_denied():
    source_packet = packet()
    private, public = keys()
    first, first_head = signed_event(source_packet, private)
    second, second_head = signed_event(
        source_packet, private, decision="deny", sequence=2,
        previous_head=first_head, decided_on=TODAY,
    )
    with pytest.raises(ValueError, match="sequence"):
        verify(source_packet, (second, first), public, second_head)
    with pytest.raises(ValueError, match="sequence"):
        verify(source_packet, (first, first), public, second_head)
    with pytest.raises(ValueError, match="previous head"):
        verify(source_packet, (first, replace(second, previous_head_sha256=GENESIS_HEAD)),
               public, second_head)


@pytest.mark.parametrize("bad_keys", [
    {"REVIEW_KEY_001": b"short"},
    {"bad-id": b"x" * 32},
    {"REVIEW_KEY_001": "key" * 11},
])
def test_malformed_trust_roots_refused(bad_keys):
    source_packet = packet()
    private, _ = keys()
    approval, head = signed_event(source_packet, private)
    with pytest.raises(ValueError, match="invalid trusted reviewer key configuration"):
        verify(source_packet, (approval,), bad_keys, head)


def test_no_future_verification_or_unsigned_date_type():
    source_packet = packet()
    private, public = keys()
    approval, head = signed_event(source_packet, private)
    with pytest.raises(ValueError, match="verification date"):
        verify(source_packet, (approval,), public, head, checked_on=datetime(2026, 11, 21))
    with pytest.raises(ValueError, match="verification date"):
        verify(source_packet, (approval,), public, head, checked_on=date(2026, 11, 18))


def test_explicit_revocation_without_earlier_approval_is_still_blocking():
    source_packet = packet()
    private, public = keys()
    revoked, head = signed_event(source_packet, private, decision="revoke")
    result = verify(source_packet, (revoked,), public, head)
    assert result.review_status == "revoked_blocks_reapproval_of_same_packet"
    assert result.receipt()["forecast_eligible"] is False
