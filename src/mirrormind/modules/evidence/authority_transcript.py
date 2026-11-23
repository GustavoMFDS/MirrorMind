"""Bounded offline witness transcript for signed SQLite review-head checkpoints.

This verifies only a supplied transcript, trusted-key *configuration* and
caller-furnished starting/current fences. It does NOT fetch trustworthy
freshness, operate a signing authority, authorize reviewers or ingest data.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from hmac import compare_digest

from mirrormind.modules.evidence.head_checkpoints import (
    SignedReviewHeadCheckpoint,
    _canonical_checkpoint_message,
    compare_sqlite_to_signed_checkpoint,
    verify_signed_head_checkpoint,
)
from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry

_SHA256 = re.compile(r"[0-9a-f]{64}")
_SIGNATURE = re.compile(r"[0-9a-f]{128}")
_KEY_ID = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
_TRANSCRIPT_DOMAIN = "mirrormind.review-head-witness.v1"
_HANDOFF_DOMAIN = "mirrormind.review-head-witness-handoff.v1"
_MAX_RECEIPTS = 32
_MAX_SEQUENCE = 1_000_000_000


@dataclass(frozen=True, slots=True)
class SignedAuthorityReceipt:
    """Witness attestation of one independently signed review checkpoint."""

    checkpoint: SignedReviewHeadCheckpoint
    witness_key_id: str
    key_epoch: int
    previous_receipt_sha256: str
    witness_signature_hex: str


@dataclass(frozen=True, slots=True)
class WitnessKeyHandoff:
    """Both old and new witness sign a specific forward key transition."""

    previous_key_id: str
    new_key_id: str
    previous_epoch: int
    new_epoch: int
    effective_sequence: int
    previous_receipt_sha256: str
    old_signature_hex: str
    new_signature_hex: str


@dataclass(frozen=True, slots=True)
class AuthorityTranscriptAssessment:
    """Non-authorizing result of a locally supplied and matched transcript."""

    validated_receipts: int
    current_sequence: int
    current_receipt_sha256: str
    review_status: str
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Output only non-sensitive receipt metadata and blocked permissions."""
        return {
            "status": "supplied_authority_transcript_verified_not_live_authority",
            "validated_receipts": self.validated_receipts,
            "current_sequence": self.current_sequence,
            "current_receipt_sha256": self.current_receipt_sha256,
            "review_status": self.review_status,
            "checked_on": self.checked_on.isoformat(),
            "freshness_status": "caller_fences_not_independently_fetched",
            "equivocation_status": "only_conflicts_in_supplied_chain_detectable",
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _canonical_authority_receipt_message(receipt: SignedAuthorityReceipt) -> bytes:
    """Separate signature domain from both review decisions and checkpoints."""
    record = {
        "domain": _TRANSCRIPT_DOMAIN,
        "checkpoint_sha256": sha256(
            _canonical_checkpoint_message(receipt.checkpoint)
            + bytes.fromhex(receipt.checkpoint.signature_hex)
        ).hexdigest(),
        "witness_key_id": receipt.witness_key_id,
        "key_epoch": receipt.key_epoch,
        "previous_receipt_sha256": receipt.previous_receipt_sha256,
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _canonical_handoff_message(handoff: WitnessKeyHandoff) -> bytes:
    """Bind old/new witness keys to the exact predecessor and next sequence."""
    record = {
        "domain": _HANDOFF_DOMAIN,
        "previous_key_id": handoff.previous_key_id,
        "new_key_id": handoff.new_key_id,
        "previous_epoch": handoff.previous_epoch,
        "new_epoch": handoff.new_epoch,
        "effective_sequence": handoff.effective_sequence,
        "previous_receipt_sha256": handoff.previous_receipt_sha256,
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _verify_signature(public_key: bytes, signature: str, message: bytes) -> None:
    """Check one signature without leaking keys or caller-supplied text."""
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("witness verification requires review extra") from None
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(
            bytes.fromhex(signature), message
        )
    except (InvalidSignature, ValueError):
        raise ValueError("authority witness signature invalid") from None


def _keys_valid(keys: Mapping[str, bytes]) -> bool:
    return (
        isinstance(keys, Mapping)
        and bool(keys)
        and all(
            type(key_id) is str and _KEY_ID.fullmatch(key_id) is not None
            and type(public_key) is bytes and len(public_key) == 32
            for key_id, public_key in keys.items()
        )
    )


def verify_authority_transcript(
    registry: SQLiteReviewRegistry,
    packet: SourceReviewPacket,
    receipts: tuple[SignedAuthorityReceipt, ...],
    handoffs: tuple[WitnessKeyHandoff, ...],
    *,
    trusted_checkpoint_keys: Mapping[str, bytes],
    trusted_witness_keys: Mapping[str, bytes],
    previous_sequence: int,
    previous_receipt_sha256: str,
    previous_witness_key_id: str,
    previous_key_epoch: int,
    expected_current_sequence: int,
    expected_current_receipt_sha256: str,
    checked_on: date,
) -> AuthorityTranscriptAssessment:
    """Reject non-contiguous or conflicting witnessed history and unsafe rotation.

    Both the *starting* and *ending* fences and both key maps MUST be
    obtained independently of the requester from a current trust service.
    This code cannot establish that they actually were. Outages/missing
    receipts always fail, never grant permission.
    """
    if type(registry) is not SQLiteReviewRegistry or type(packet) is not SourceReviewPacket:
        raise ValueError("expected local SQLite registry and exact source packet")
    if (type(receipts) is not tuple or not 1 <= len(receipts) <= _MAX_RECEIPTS
            or type(handoffs) is not tuple or len(handoffs) > len(receipts)):
        raise ValueError("authority transcript missing or exceeds bounded size")
    if type(checked_on) is not date:
        raise ValueError("invalid witness verification date")
    if not _keys_valid(trusted_checkpoint_keys) or not _keys_valid(trusted_witness_keys):
        raise ValueError("trusted checkpoint and witness public keys required")
    if set(trusted_checkpoint_keys).intersection(trusted_witness_keys):
        raise ValueError("review checkpoint and witness key roles must be distinct")
    if (
        type(previous_sequence) is not int
        or not 0 <= previous_sequence < _MAX_SEQUENCE
        or type(expected_current_sequence) is not int
        or not previous_sequence < expected_current_sequence <= _MAX_SEQUENCE
        or type(previous_key_epoch) is not int
        or not 1 <= previous_key_epoch < _MAX_SEQUENCE
        or type(previous_witness_key_id) is not str
        or previous_witness_key_id not in trusted_witness_keys
        or type(previous_receipt_sha256) is not str
        or _SHA256.fullmatch(previous_receipt_sha256) is None
        or type(expected_current_receipt_sha256) is not str
        or _SHA256.fullmatch(expected_current_receipt_sha256) is None
    ):
        raise ValueError("invalid externally supplied transcript fences")

    previous_digest = previous_receipt_sha256
    previous_key = previous_witness_key_id
    epoch = previous_key_epoch
    previous_issue = packet.inspected_on
    sequence = previous_sequence
    last_revision = -1
    last_head: str | None = None
    used_handoffs: set[int] = set()

    for receipt in receipts:
        if type(receipt) is not SignedAuthorityReceipt:
            raise ValueError("invalid authority receipt")
        checkpoint = receipt.checkpoint
        if type(checkpoint) is not SignedReviewHeadCheckpoint:
            raise ValueError("invalid witnessed checkpoint")
        if (
            type(receipt.witness_key_id) is not str
            or receipt.witness_key_id not in trusted_witness_keys
            or type(receipt.key_epoch) is not int
            or not 1 <= receipt.key_epoch <= _MAX_SEQUENCE
            or type(receipt.previous_receipt_sha256) is not str
            or _SHA256.fullmatch(receipt.previous_receipt_sha256) is None
            or not compare_digest(receipt.previous_receipt_sha256, previous_digest)
            or type(receipt.witness_signature_hex) is not str
            or _SIGNATURE.fullmatch(receipt.witness_signature_hex) is None
            or type(checkpoint.anchor_sequence) is not int
            or checkpoint.anchor_sequence != sequence + 1
        ):
            raise ValueError("authority receipt has a gap, replay or incorrect predecessor")
        if type(checkpoint.issued_on) is not date or checkpoint.issued_on < previous_issue:
            raise ValueError("authority checkpoint dates must be nondecreasing")

        verify_signed_head_checkpoint(
            packet, checkpoint,
            trusted_anchor_keys=trusted_checkpoint_keys,
            minimum_anchor_sequence=checkpoint.anchor_sequence,
            checked_on=checkpoint.issued_on,
        )

        if receipt.witness_key_id != previous_key or receipt.key_epoch != epoch:
            if receipt.witness_key_id == previous_key or receipt.key_epoch != epoch + 1:
                raise ValueError("witness key change requires next-epoch rotation")
            matched = [
                (index, handoff)
                for index, handoff in enumerate(handoffs)
                if type(handoff) is WitnessKeyHandoff
                and handoff.previous_key_id == previous_key
                and handoff.new_key_id == receipt.witness_key_id
                and handoff.previous_epoch == epoch
                and handoff.new_epoch == receipt.key_epoch
                and handoff.effective_sequence == checkpoint.anchor_sequence
                and handoff.previous_receipt_sha256 == previous_digest
            ]
            if len(matched) != 1 or matched[0][0] in used_handoffs:
                raise ValueError("missing unique dual-signed witness key handoff")
            index, handoff = matched[0]
            if (
                type(handoff.old_signature_hex) is not str
                or _SIGNATURE.fullmatch(handoff.old_signature_hex) is None
                or type(handoff.new_signature_hex) is not str
                or _SIGNATURE.fullmatch(handoff.new_signature_hex) is None
            ):
                raise ValueError("invalid witness rotation signatures")
            message = _canonical_handoff_message(handoff)
            _verify_signature(trusted_witness_keys[previous_key],
                              handoff.old_signature_hex, message)
            _verify_signature(trusted_witness_keys[receipt.witness_key_id],
                              handoff.new_signature_hex, message)
            used_handoffs.add(index)
        if checkpoint.review_revision < last_revision:
            raise ValueError("witnessed review revision regressed")
        if (last_head is not None and
                (checkpoint.review_revision == last_revision)
                != (checkpoint.review_head_sha256 == last_head)):
            raise ValueError("witnessed review head conflicts with revision")
        message = _canonical_authority_receipt_message(receipt)
        _verify_signature(
            trusted_witness_keys[receipt.witness_key_id],
            receipt.witness_signature_hex, message,
        )
        previous_digest = sha256(
            message + bytes.fromhex(receipt.witness_signature_hex)
        ).hexdigest()
        previous_key = receipt.witness_key_id
        epoch = receipt.key_epoch
        previous_issue = checkpoint.issued_on
        last_revision = checkpoint.review_revision
        last_head = checkpoint.review_head_sha256
        sequence = checkpoint.anchor_sequence

    if len(used_handoffs) != len(handoffs):
        raise ValueError("unused or conflicting witness handoff")
    if (sequence != expected_current_sequence
            or not compare_digest(previous_digest, expected_current_receipt_sha256)):
        raise ValueError("transcript does not match externally expected current receipt")
    latest = receipts[-1].checkpoint
    comparison = compare_sqlite_to_signed_checkpoint(
        registry, packet, latest,
        trusted_anchor_keys=trusted_checkpoint_keys,
        minimum_anchor_sequence=expected_current_sequence,
        checked_on=checked_on,
    )
    return AuthorityTranscriptAssessment(
        validated_receipts=len(receipts),
        current_sequence=sequence,
        current_receipt_sha256=previous_digest,
        review_status=comparison.review_status,
        checked_on=checked_on,
    )
