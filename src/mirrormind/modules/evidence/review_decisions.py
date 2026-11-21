"""Offline verification of independently signed review decisions and revocations.

A validated signature is not proof of data rights, publisher identity, reviewer
authority, trusted-key provisioning, log freshness, or permission to ingest.
This module never grants ingestion or forecasting.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256
from hmac import compare_digest

from mirrormind.modules.evidence.intake_review import SourceReviewPacket

GENESIS_HEAD = "0" * 64
SHA256_RE = re.compile(r"[0-9a-f]{64}")
SIGNATURE_RE = re.compile(r"[0-9a-f]{128}")
REFERENCE_RE = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
DECISIONS = frozenset(("approve", "deny", "revoke"))


@dataclass(frozen=True, slots=True)
class SignedReviewDecision:
    """Externally signed metadata; must not originate from the intake requester."""

    review_ref: str
    reviewer_key_id: str
    sequence: int
    previous_head_sha256: str
    packet_sha256: str
    snapshot_sha256: str
    source_kind: str
    intended_use: str
    decision: str
    decided_on: date
    expires_on: date | None
    signature_hex: str


@dataclass(frozen=True, slots=True)
class ReviewHistoryAssessment:
    """Non-authorizing, identifier-minimized result of signature/log verification."""

    review_status: str
    log_head_sha256: str
    reviewed_events: int
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Expose a signed-review status, never source or reviewer references."""
        return {
            "status": "signed_review_history_checked_not_ingestion_authorization",
            "review_status": self.review_status,
            "log_head_sha256": self.log_head_sha256,
            "reviewed_events": self.reviewed_events,
            "checked_on": self.checked_on.isoformat(),
            "signature_status": (
                "validated_against_supplied_public_keys_not_identity_proof"
                if self.reviewed_events else "no_signatures_present"
            ),
            "log_freshness_status": "supplied_head_not_independently_attested",
            "permission_status": "independent_legal_permission_not_verified",
            "historical_availability_status": "not_verified",
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _canonical_review_message(event: SignedReviewDecision) -> bytes:
    """Encode the exact v1 review record for external Ed25519 signature verification."""
    record = {
        "version": 1,
        "review_ref": event.review_ref,
        "reviewer_key_id": event.reviewer_key_id,
        "sequence": event.sequence,
        "previous_head_sha256": event.previous_head_sha256,
        "packet_sha256": event.packet_sha256,
        "snapshot_sha256": event.snapshot_sha256,
        "source_kind": event.source_kind,
        "intended_use": event.intended_use,
        "decision": event.decision,
        "decided_on": event.decided_on.isoformat(),
        "expires_on": event.expires_on.isoformat() if event.expires_on else None,
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_review_history(
    packet: SourceReviewPacket,
    events: tuple[SignedReviewDecision, ...],
    *,
    trusted_reviewer_keys: Mapping[str, bytes],
    expected_head_sha256: str,
    checked_on: date,
) -> ReviewHistoryAssessment:
    """Verify offline Ed25519 review events and fail closed on revoked/expired records.

    Trusted public keys AND the expected latest log head must be supplied by
    an independent control plane. Values submitted by the intake requester
    are not a trust root. No persistence or downstream authorization occurs.
    """
    if type(packet) is not SourceReviewPacket:
        raise ValueError("expected an exact source review packet")
    if type(events) is not tuple or len(events) > 64:
        raise ValueError("review history must be a tuple with at most 64 events")
    if (type(checked_on) is not date
            or type(packet.inspected_on) is not date
            or type(packet.captured_on) is not date
            or checked_on < packet.inspected_on):
        raise ValueError("invalid review verification date")
    if type(expected_head_sha256) is not str or not SHA256_RE.fullmatch(expected_head_sha256):
        raise ValueError("invalid externally expected log head")
    if not isinstance(trusted_reviewer_keys, Mapping) or not trusted_reviewer_keys:
        raise ValueError("trusted reviewer public-key mapping required")
    if any(
        type(key_id) is not str or REFERENCE_RE.fullmatch(key_id) is None
        or type(pub) is not bytes or len(pub) != 32
        for key_id, pub in trusted_reviewer_keys.items()
    ):
        raise ValueError("invalid trusted reviewer key configuration")
    if (type(packet.declaration_sha256) is not str
            or not SHA256_RE.fullmatch(packet.declaration_sha256)
            or type(packet.snapshot_sha256) is not str
            or not SHA256_RE.fullmatch(packet.snapshot_sha256)):
        raise ValueError("invalid packet fingerprint")

    # The optional dependency is loaded only for signature verification.
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("signed review verification requires the review extra") from None

    current_head = GENESIS_HEAD
    previous_date = packet.inspected_on
    revoked = False
    last_event: SignedReviewDecision | None = None
    seen_refs: set[str] = set()
    for sequence, event in enumerate(events, start=1):
        if type(event) is not SignedReviewDecision:
            raise ValueError("invalid signed review event")
        if (type(event.sequence) is not int or event.sequence != sequence
                or type(event.review_ref) is not str
                or REFERENCE_RE.fullmatch(event.review_ref) is None
                or event.review_ref in seen_refs
                or type(event.reviewer_key_id) is not str
                or event.reviewer_key_id not in trusted_reviewer_keys):
            raise ValueError("invalid review sequence, reference or signer")
        if (
            type(event.previous_head_sha256) is not str
            or not compare_digest(event.previous_head_sha256, current_head)
            or event.packet_sha256 != packet.declaration_sha256
            or event.snapshot_sha256 != packet.snapshot_sha256
            or event.source_kind != packet.source_kind
            or event.intended_use != packet.intended_use
        ):
            raise ValueError("review event does not match packet or previous head")
        if (type(event.decision) is not str or event.decision not in DECISIONS
                or type(event.decided_on) is not date
                or not previous_date <= event.decided_on <= checked_on):
            raise ValueError("invalid review decision date or action")
        if event.decision == "approve":
            if (type(event.expires_on) is not date
                    or not event.decided_on < event.expires_on
                    or event.expires_on > event.decided_on + timedelta(days=3650)):
                raise ValueError("approval requires a bounded expiration date")
        elif event.expires_on is not None:
            raise ValueError("denial or revocation cannot carry an expiration")
        if type(event.signature_hex) is not str or not SIGNATURE_RE.fullmatch(event.signature_hex):
            raise ValueError("invalid review signature encoding")
        message = _canonical_review_message(event)
        signature = bytes.fromhex(event.signature_hex)
        try:
            Ed25519PublicKey.from_public_bytes(
                trusted_reviewer_keys[event.reviewer_key_id]
            ).verify(signature, message)
        except (InvalidSignature, ValueError):
            raise ValueError("review signature verification failed") from None
        current_head = sha256(message + signature).hexdigest()
        previous_date = event.decided_on
        seen_refs.add(event.review_ref)
        if event.decision == "revoke":
            revoked = True
        last_event = event

    if not compare_digest(current_head, expected_head_sha256):
        raise ValueError("review history differs from externally expected log head")
    if revoked:
        status = "revoked_blocks_reapproval_of_same_packet"
    elif last_event is None:
        status = "missing_review_record"
    elif last_event.decision == "deny":
        status = "review_denied"
    elif last_event.expires_on is not None and last_event.expires_on < checked_on:
        status = "signed_approval_expired"
    else:
        status = "signed_approval_record_verified_not_legal_permission"
    return ReviewHistoryAssessment(
        review_status=status,
        log_head_sha256=current_head,
        reviewed_events=len(events),
        checked_on=checked_on,
    )
