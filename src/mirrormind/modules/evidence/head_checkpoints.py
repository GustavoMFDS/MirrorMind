"""Verify independently signed review-head checkpoints against local SQLite.

A checkpoint signature attests to a particular record, not its freshness:
the caller MUST obtain trusted signer keys and a monotonic minimum sequence
from an independently controlled source. No such authority is implemented.
No review status here enables source ingestion or forecasting.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta
from hmac import compare_digest

from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.review_decisions import GENESIS_HEAD
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry

_HASH = re.compile(r"[0-9a-f]{64}")
_SIGNATURE = re.compile(r"[0-9a-f]{128}")
_KEY_REF = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
_DOMAIN = "mirrormind.review-head-checkpoint.v1"
_MAX_REVIEW_EVENTS = 64
_MAX_SEQUENCE = 1_000_000_000


@dataclass(frozen=True, slots=True)
class SignedReviewHeadCheckpoint:
    """External signer's attestation of one exact packet's review log head."""

    anchor_key_id: str
    packet_sha256: str
    snapshot_sha256: str
    source_kind: str
    intended_use: str
    review_revision: int
    review_head_sha256: str
    anchor_sequence: int
    issued_on: date
    expires_on: date
    signature_hex: str


@dataclass(frozen=True, slots=True)
class CheckpointComparison:
    """Identifier-minimized verification result; never an access-control token."""

    review_revision: int
    review_head_sha256: str
    review_status: str
    anchor_sequence: int
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Avoid leaking private record/key identifiers or implying authorization."""
        return {
            "status": "signed_checkpoint_matches_local_review_not_authorization",
            "review_revision": self.review_revision,
            "review_head_sha256": self.review_head_sha256,
            "review_status": self.review_status,
            "anchor_sequence": self.anchor_sequence,
            "checked_on": self.checked_on.isoformat(),
            "signature_status": "valid_against_supplied_anchor_key_not_identity_proof",
            "freshness_status": "caller_supplied_high_water_not_independently_checked",
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _canonical_checkpoint_message(checkpoint: SignedReviewHeadCheckpoint) -> bytes:
    """Domain-separated, versioned bytes to be signed by the EXTERNAL authority."""
    record = {
        "domain": _DOMAIN,
        "anchor_key_id": checkpoint.anchor_key_id,
        "packet_sha256": checkpoint.packet_sha256,
        "snapshot_sha256": checkpoint.snapshot_sha256,
        "source_kind": checkpoint.source_kind,
        "intended_use": checkpoint.intended_use,
        "review_revision": checkpoint.review_revision,
        "review_head_sha256": checkpoint.review_head_sha256,
        "anchor_sequence": checkpoint.anchor_sequence,
        "issued_on": checkpoint.issued_on.isoformat(),
        "expires_on": checkpoint.expires_on.isoformat(),
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_signed_head_checkpoint(
    packet: SourceReviewPacket,
    checkpoint: SignedReviewHeadCheckpoint,
    *,
    trusted_anchor_keys: Mapping[str, bytes],
    minimum_anchor_sequence: int,
    checked_on: date,
) -> None:
    """Verify metadata and signature against caller-supplied trust + high-water.

    Does NOT query a current registry or persist any monotonic counter. A
    supplied high-water that is stale or requester-controlled defeats replay
    rejection, even when Ed25519 signature verification itself succeeds.
    """
    if type(packet) is not SourceReviewPacket or type(checkpoint) is not SignedReviewHeadCheckpoint:
        raise ValueError("invalid source packet or signed checkpoint")
    if (
        type(checked_on) is not date
        or type(packet.inspected_on) is not date
        or type(checkpoint.issued_on) is not date
        or type(checkpoint.expires_on) is not date
        or not packet.inspected_on <= checkpoint.issued_on <= checked_on <= checkpoint.expires_on
        or not checkpoint.issued_on < checkpoint.expires_on
        or checkpoint.expires_on > checkpoint.issued_on + timedelta(days=30)
    ):
        raise ValueError("checkpoint validity dates are invalid or expired")
    if (
        type(checkpoint.anchor_key_id) is not str
        or _KEY_REF.fullmatch(checkpoint.anchor_key_id) is None
        or type(checkpoint.packet_sha256) is not str
        or _HASH.fullmatch(checkpoint.packet_sha256) is None
        or type(checkpoint.snapshot_sha256) is not str
        or _HASH.fullmatch(checkpoint.snapshot_sha256) is None
        or type(checkpoint.review_head_sha256) is not str
        or _HASH.fullmatch(checkpoint.review_head_sha256) is None
        or type(checkpoint.signature_hex) is not str
        or _SIGNATURE.fullmatch(checkpoint.signature_hex) is None
    ):
        raise ValueError("invalid signed checkpoint metadata")
    if (
        checkpoint.packet_sha256 != packet.declaration_sha256
        or checkpoint.snapshot_sha256 != packet.snapshot_sha256
        or checkpoint.source_kind != packet.source_kind
        or checkpoint.intended_use != packet.intended_use
    ):
        raise ValueError("checkpoint source identity or use does not match packet")
    if (
        type(minimum_anchor_sequence) is not int
        or not 1 <= minimum_anchor_sequence <= _MAX_SEQUENCE
        or type(checkpoint.anchor_sequence) is not int
        or not minimum_anchor_sequence <= checkpoint.anchor_sequence <= _MAX_SEQUENCE
    ):
        raise ValueError("checkpoint is below supplied independent sequence floor")
    if (
        type(checkpoint.review_revision) is not int
        or not 0 <= checkpoint.review_revision <= _MAX_REVIEW_EVENTS
        or (checkpoint.review_revision == 0) != (checkpoint.review_head_sha256 == GENESIS_HEAD)
    ):
        raise ValueError("checkpoint review revision or head is invalid")
    if not isinstance(trusted_anchor_keys, Mapping) or not trusted_anchor_keys:
        raise ValueError("trusted external anchor keys required")
    if any(
        type(key_id) is not str or _KEY_REF.fullmatch(key_id) is None
        or type(public_key) is not bytes or len(public_key) != 32
        for key_id, public_key in trusted_anchor_keys.items()
    ):
        raise ValueError("invalid external anchor key configuration")
    if checkpoint.anchor_key_id not in trusted_anchor_keys:
        raise ValueError("unknown external anchor key")
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("signed checkpoint verification requires review extra") from None
    try:
        Ed25519PublicKey.from_public_bytes(
            trusted_anchor_keys[checkpoint.anchor_key_id]
        ).verify(
            bytes.fromhex(checkpoint.signature_hex),
            _canonical_checkpoint_message(checkpoint),
        )
    except (InvalidSignature, ValueError):
        raise ValueError("external checkpoint signature failed") from None


def compare_sqlite_to_signed_checkpoint(
    registry: SQLiteReviewRegistry,
    packet: SourceReviewPacket,
    checkpoint: SignedReviewHeadCheckpoint,
    *,
    trusted_anchor_keys: Mapping[str, bytes],
    minimum_anchor_sequence: int,
    checked_on: date,
) -> CheckpointComparison:
    """Check a verified signed head against the SAME atomic SQLite snapshot."""
    if type(registry) is not SQLiteReviewRegistry:
        raise ValueError("expected exact local SQLite review registry")
    verify_signed_head_checkpoint(
        packet, checkpoint,
        trusted_anchor_keys=trusted_anchor_keys,
        minimum_anchor_sequence=minimum_anchor_sequence,
        checked_on=checked_on,
    )
    current = registry.snapshot(
        packet, checked_on=checked_on,
        externally_expected_head_sha256=checkpoint.review_head_sha256,
    )
    if (
        type(current.revision) is not int
        or current.revision != checkpoint.review_revision
        or not compare_digest(current.log_head_sha256, checkpoint.review_head_sha256)
    ):
        raise ValueError("checkpoint review revision or log head differs from SQLite")
    return CheckpointComparison(
        review_revision=current.revision,
        review_head_sha256=current.log_head_sha256,
        review_status=current.review_status,
        anchor_sequence=checkpoint.anchor_sequence,
        checked_on=checked_on,
    )
