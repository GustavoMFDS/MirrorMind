"""Offline dual-witness continuity and supplied-fork checks for integrated head fences.

Caller-provided anchors, trust rosters and latest pins are NOT independently
fetched or guaranteed fresh. A successful check never authorizes publication
or source ingestion.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from hmac import compare_digest

from mirrormind.modules.evidence.atomic_governed_publisher import AtomicGovernedPublisher
from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.integrated_head_fence import (
    SignedIntegratedHeadFence,
    _canonical_fence_message,
    _fence_sha256,
    verify_integrated_head_fence,
)

_DOMAIN = "mirrormind.integrated-fence-dual-witness.v1"
_SHA = re.compile(r"[0-9a-f]{64}")
_SIG = re.compile(r"[0-9a-f]{128}")
_KEY_ID = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
_MAX_SEQUENCE = 1_000_000_000
_MAX_TRANSITIONS = 32
_MAX_KEYS_PER_ROLE = 8


@dataclass(frozen=True, slots=True)
class SignedIntegratedFenceTransition:
    """Two witnesses endorse the exact successor of an authority-signed fence."""

    fence: SignedIntegratedHeadFence
    previous_authority_sequence: int
    previous_fence_sha256: str
    witnessed_on: date
    witness_key_ids: tuple[str, str]
    witness_signatures_hex: tuple[str, str]


@dataclass(frozen=True, slots=True)
class IntegratedFenceTranscriptAssessment:
    """Caller-pinned chain agrees with local heads; NOT an authorization token."""

    validated_transitions: int
    anchor_authority_sequence: int
    current_authority_sequence: int
    current_fence_sha256: str
    checked_on: date

    def receipt(self) -> dict[str, int | str | bool]:
        return {
            "status": "supplied_dual_witness_fence_chain_matches_local_only",
            "validated_transitions": self.validated_transitions,
            "anchor_authority_sequence": self.anchor_authority_sequence,
            "current_authority_sequence": self.current_authority_sequence,
            "current_fence_sha256": self.current_fence_sha256,
            "checked_on": self.checked_on.isoformat(),
            "freshness_status": "caller_pinned_not_independently_fetched",
            "equivocation_status": "only_supplied_competing_successors_detectable",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


@dataclass(frozen=True, slots=True)
class SuppliedFenceForkEvidence:
    """Two verified signed successors conflict; neither is selected as current."""

    previous_authority_sequence: int
    previous_fence_sha256: str
    successor_authority_sequence: int
    first_fence_sha256: str
    second_fence_sha256: str
    checked_on: date

    def receipt(self) -> dict[str, int | str | bool]:
        return {
            "status": "observed_supplied_signed_fence_conflict_no_resolution",
            "previous_authority_sequence": self.previous_authority_sequence,
            "previous_fence_sha256": self.previous_fence_sha256,
            "successor_authority_sequence": self.successor_authority_sequence,
            "first_fence_sha256": self.first_fence_sha256,
            "second_fence_sha256": self.second_fence_sha256,
            "checked_on": self.checked_on.isoformat(),
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _canonical_fence_transition_message(link: SignedIntegratedFenceTransition) -> bytes:
    """Both witness signatures cover the same immutable canonical message."""
    if type(link) is not SignedIntegratedFenceTransition:
        raise ValueError("invalid integrated fence transition type")
    fence_sha256 = _fence_sha256(link.fence)  # checks fence and signature framing
    if (
        type(link.previous_authority_sequence) is not int
        or not 0 <= link.previous_authority_sequence < _MAX_SEQUENCE
        or type(link.previous_fence_sha256) is not str
        or _SHA.fullmatch(link.previous_fence_sha256) is None
        or type(link.witnessed_on) is not date
        or type(link.witness_key_ids) is not tuple
        or len(link.witness_key_ids) != 2
        or any(
            type(key_id) is not str or _KEY_ID.fullmatch(key_id) is None
            for key_id in link.witness_key_ids
        )
        or link.witness_key_ids[0] >= link.witness_key_ids[1]
        or type(link.witness_signatures_hex) is not tuple
        or len(link.witness_signatures_hex) != 2
        or any(
            type(signature) is not str or _SIG.fullmatch(signature) is None
            for signature in link.witness_signatures_hex
        )
        or link.fence.authority_sequence != link.previous_authority_sequence + 1
        or not link.fence.issued_on <= link.witnessed_on <= link.fence.expires_on
    ):
        raise ValueError("malformed integrated fence transition")
    record = {
        "domain": _DOMAIN,
        "previous_authority_sequence": link.previous_authority_sequence,
        "previous_fence_sha256": link.previous_fence_sha256,
        "authority_sequence": link.fence.authority_sequence,
        "fence_sha256": fence_sha256,
        "witnessed_on": link.witnessed_on.isoformat(),
        "witness_key_ids": list(link.witness_key_ids),
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _validate_rosters(
    trusted_fence_keys: Mapping[str, bytes],
    trusted_witness_keys: Mapping[str, bytes],
) -> None:
    for roster, minimum in ((trusted_fence_keys, 1), (trusted_witness_keys, 2)):
        if (
            not isinstance(roster, Mapping)
            or not minimum <= len(roster) <= _MAX_KEYS_PER_ROLE
            or any(
                type(key_id) is not str
                or _KEY_ID.fullmatch(key_id) is None
                or type(public) is not bytes
                or len(public) != 32
                for key_id, public in roster.items()
            )
            or len(set(roster.values())) != len(roster)
        ):
            raise ValueError("invalid integrated fence authority/witness key roster")
    if (
        set(trusted_fence_keys).intersection(trusted_witness_keys)
        or set(trusted_fence_keys.values()).intersection(trusted_witness_keys.values())
    ):
        raise ValueError("authority and witness signing roles must be distinct")


def _verify_one_transition(
    link: SignedIntegratedFenceTransition,
    packet: SourceReviewPacket,
    *,
    trusted_fence_keys: Mapping[str, bytes],
    trusted_witness_keys: Mapping[str, bytes],
    checked_on: date,
) -> str:
    message = _canonical_fence_transition_message(link)
    fence = link.fence
    if (
        fence.authority_key_id not in trusted_fence_keys
        or any(key_id not in trusted_witness_keys for key_id in link.witness_key_ids)
        or fence.packet_sha256 != packet.declaration_sha256
        or fence.snapshot_sha256 != packet.snapshot_sha256
        or type(packet.inspected_on) is not date
        or fence.issued_on < packet.inspected_on
        or link.witnessed_on > checked_on
    ):
        raise ValueError("untrusted transition signer, source packet or witness date")
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("integrated fence transcript requires review extra") from None
    try:
        Ed25519PublicKey.from_public_bytes(
            trusted_fence_keys[fence.authority_key_id]
        ).verify(bytes.fromhex(fence.signature_hex), _canonical_fence_message(fence))
        for key_id, signature in zip(
            link.witness_key_ids, link.witness_signatures_hex, strict=True
        ):
            Ed25519PublicKey.from_public_bytes(
                trusted_witness_keys[key_id]
            ).verify(bytes.fromhex(signature), message)
    except (InvalidSignature, ValueError):
        raise ValueError("invalid integrated fence authority or dual-witness signature") from None
    return _fence_sha256(fence)


def verify_integrated_fence_transcript(
    gate: AtomicGovernedPublisher,
    packet: SourceReviewPacket,
    transitions: tuple[SignedIntegratedFenceTransition, ...],
    *,
    trusted_fence_keys: Mapping[str, bytes],
    trusted_witness_keys: Mapping[str, bytes],
    anchor_authority_sequence: int,
    anchor_fence_sha256: str,
    expected_current_authority_sequence: int,
    expected_current_fence_sha256: str,
    checked_on: date,
) -> IntegratedFenceTranscriptAssessment:
    """Verify caller-pinned consecutive two-witness links and terminal SQLite heads."""
    if (
        type(gate) is not AtomicGovernedPublisher
        or type(packet) is not SourceReviewPacket
        or type(checked_on) is not date
        or type(transitions) is not tuple
        or not 1 <= len(transitions) <= _MAX_TRANSITIONS
        or type(anchor_authority_sequence) is not int
        or not 0 <= anchor_authority_sequence < _MAX_SEQUENCE
        or type(anchor_fence_sha256) is not str
        or _SHA.fullmatch(anchor_fence_sha256) is None
        or type(expected_current_authority_sequence) is not int
        or type(expected_current_fence_sha256) is not str
        or _SHA.fullmatch(expected_current_fence_sha256) is None
    ):
        raise ValueError("invalid supplied fence transcript bounds or anchor")
    _validate_rosters(trusted_fence_keys, trusted_witness_keys)
    previous_sequence, previous_digest = anchor_authority_sequence, anchor_fence_sha256
    previous_policy_revision = -1
    previous_publication_sequence = -1
    previous_policy_head = ""
    previous_publication_head = ""
    previous_witnessed_on: date | None = None
    for link in transitions:
        if type(link) is not SignedIntegratedFenceTransition:
            raise ValueError("invalid supplied fence transition type")
        if (
            link.previous_authority_sequence != previous_sequence
            or not compare_digest(link.previous_fence_sha256, previous_digest)
            or (previous_witnessed_on is not None and link.witnessed_on < previous_witnessed_on)
        ):
            raise ValueError("supplied fence transcript has missing, forked or reversed link")
        current_digest = _verify_one_transition(
            link, packet, trusted_fence_keys=trusted_fence_keys,
            trusted_witness_keys=trusted_witness_keys, checked_on=checked_on,
        )
        fence = link.fence
        if (
            fence.policy_revision < previous_policy_revision
            or fence.publication_sequence < previous_publication_sequence
            or (
                fence.policy_revision == previous_policy_revision
                and fence.policy_head_sha256 != previous_policy_head
            )
            or (
                fence.publication_sequence == previous_publication_sequence
                and fence.publication_head_sha256 != previous_publication_head
            )
        ):
            raise ValueError("supplied fence transcript state counters regressed or forked")
        previous_sequence, previous_digest = fence.authority_sequence, current_digest
        previous_policy_revision = fence.policy_revision
        previous_publication_sequence = fence.publication_sequence
        previous_policy_head = fence.policy_head_sha256
        previous_publication_head = fence.publication_head_sha256
        previous_witnessed_on = link.witnessed_on
    if (
        previous_sequence != expected_current_authority_sequence
        or not compare_digest(previous_digest, expected_current_fence_sha256)
    ):
        raise ValueError("supplied chain terminal differs from external current pin")
    verify_integrated_head_fence(
        gate, packet, transitions[-1].fence,
        trusted_fence_keys=trusted_fence_keys,
        expected_current_authority_sequence=expected_current_authority_sequence,
        expected_current_fence_sha256=expected_current_fence_sha256,
        checked_on=checked_on,
    )
    return IntegratedFenceTranscriptAssessment(
        validated_transitions=len(transitions),
        anchor_authority_sequence=anchor_authority_sequence,
        current_authority_sequence=previous_sequence,
        current_fence_sha256=previous_digest,
        checked_on=checked_on,
    )


def classify_supplied_fence_fork(
    packet: SourceReviewPacket,
    first: SignedIntegratedFenceTransition,
    second: SignedIntegratedFenceTransition,
    *,
    trusted_fence_keys: Mapping[str, bytes],
    trusted_witness_keys: Mapping[str, bytes],
    checked_on: date,
) -> SuppliedFenceForkEvidence:
    """Classify only two supplied valid incompatible successors; do not select a head."""
    if type(packet) is not SourceReviewPacket or type(checked_on) is not date:
        raise ValueError("invalid packet or check date")
    _validate_rosters(trusted_fence_keys, trusted_witness_keys)
    first_digest = _verify_one_transition(
        first, packet, trusted_fence_keys=trusted_fence_keys,
        trusted_witness_keys=trusted_witness_keys, checked_on=checked_on,
    )
    second_digest = _verify_one_transition(
        second, packet, trusted_fence_keys=trusted_fence_keys,
        trusted_witness_keys=trusted_witness_keys, checked_on=checked_on,
    )
    if (
        first.previous_authority_sequence != second.previous_authority_sequence
        or not compare_digest(first.previous_fence_sha256, second.previous_fence_sha256)
        or first.fence.authority_sequence != second.fence.authority_sequence
        or compare_digest(first_digest, second_digest)
    ):
        raise ValueError("no competing authenticated same-predecessor fence successors")
    return SuppliedFenceForkEvidence(
        previous_authority_sequence=first.previous_authority_sequence,
        previous_fence_sha256=first.previous_fence_sha256,
        successor_authority_sequence=first.fence.authority_sequence,
        first_fence_sha256=first_digest,
        second_fence_sha256=second_digest,
        checked_on=checked_on,
    )
