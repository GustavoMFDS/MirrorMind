"""Offline verification of a supplied, signed integrated SQLite head fence.

The caller must obtain the trusted signing keys and exact current sequence
and digest independently. This module cannot fetch or attest their freshness.
It never grants source rights, publication, ingestion or forecasting.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta
from hashlib import sha256
from hmac import compare_digest

from mirrormind.modules.evidence.atomic_governed_publisher import AtomicGovernedPublisher
from mirrormind.modules.evidence.intake_review import SourceReviewPacket

_DOMAIN = "mirrormind.integrated-head-fence.v1"
_SHA = re.compile(r"[0-9a-f]{64}")
_SIG = re.compile(r"[0-9a-f]{128}")
_KEY_ID = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
_MAX_SEQUENCE = 1_000_000_000
_MAX_KEYS = 8
_MAX_VALIDITY_DAYS = 30


@dataclass(frozen=True, slots=True)
class SignedIntegratedHeadFence:
    """Signer-supplied exact local policy and per-packet publication state."""

    authority_key_id: str
    authority_sequence: int
    packet_sha256: str
    snapshot_sha256: str
    policy_revision: int
    policy_head_sha256: str
    publication_sequence: int
    publication_head_sha256: str
    issued_on: date
    expires_on: date
    signature_hex: str


@dataclass(frozen=True, slots=True)
class IntegratedHeadFenceAssessment:
    """Read-only local equality result; NEVER an authorization token."""

    authority_sequence: int
    supplied_fence_sha256: str
    policy_revision: int
    publication_sequence: int
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Return only identifier-minimized consistency and permission fields."""
        return {
            "status": "supplied_signed_integrated_heads_match_local_only",
            "authority_sequence": self.authority_sequence,
            "supplied_fence_sha256": self.supplied_fence_sha256,
            "policy_revision": self.policy_revision,
            "publication_sequence": self.publication_sequence,
            "checked_on": self.checked_on.isoformat(),
            "freshness_status": "caller_pinned_not_independently_fetched",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _canonical_fence_message(fence: SignedIntegratedHeadFence) -> bytes:
    """Canonical message in a domain distinct from review and publish roles."""
    if type(fence) is not SignedIntegratedHeadFence:
        raise ValueError("invalid integrated head fence type")
    if (
        type(fence.authority_key_id) is not str
        or _KEY_ID.fullmatch(fence.authority_key_id) is None
        or type(fence.authority_sequence) is not int
        or not 1 <= fence.authority_sequence <= _MAX_SEQUENCE
        or type(fence.policy_revision) is not int
        or not 0 <= fence.policy_revision <= _MAX_SEQUENCE
        or type(fence.publication_sequence) is not int
        or not 0 <= fence.publication_sequence <= _MAX_SEQUENCE
        or any(
            type(value) is not str or _SHA.fullmatch(value) is None
            for value in (
                fence.packet_sha256, fence.snapshot_sha256,
                fence.policy_head_sha256, fence.publication_head_sha256,
            )
        )
        or type(fence.issued_on) is not date
        or type(fence.expires_on) is not date
        or not fence.issued_on <= fence.expires_on
        or fence.expires_on - fence.issued_on > timedelta(days=_MAX_VALIDITY_DAYS)
    ):
        raise ValueError("integrated head fence has invalid fields or validity")
    record = {
        "domain": _DOMAIN,
        "authority_key_id": fence.authority_key_id,
        "authority_sequence": fence.authority_sequence,
        "packet_sha256": fence.packet_sha256,
        "snapshot_sha256": fence.snapshot_sha256,
        "policy_revision": fence.policy_revision,
        "policy_head_sha256": fence.policy_head_sha256,
        "publication_sequence": fence.publication_sequence,
        "publication_head_sha256": fence.publication_head_sha256,
        "issued_on": fence.issued_on.isoformat(),
        "expires_on": fence.expires_on.isoformat(),
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _fence_sha256(fence: SignedIntegratedHeadFence) -> str:
    """Hash the canonical payload AND actual Ed25519 signature bytes."""
    message = _canonical_fence_message(fence)
    if type(fence.signature_hex) is not str or _SIG.fullmatch(fence.signature_hex) is None:
        raise ValueError("malformed integrated head fence signature")
    return sha256(message + bytes.fromhex(fence.signature_hex)).hexdigest()


def verify_integrated_head_fence(
    gate: AtomicGovernedPublisher,
    packet: SourceReviewPacket,
    fence: SignedIntegratedHeadFence,
    *,
    trusted_fence_keys: Mapping[str, bytes],
    expected_current_authority_sequence: int,
    expected_current_fence_sha256: str,
    checked_on: date,
) -> IntegratedHeadFenceAssessment:
    """Check supplied signed heads against one consistent local SQLite snapshot.

    Trust roster, exact current sequence/digest and clock MUST come from
    independent trusted inputs. A matching old roster + fence + expected
    digest on a restored old SQLite database may still succeed.
    """
    if (
        type(gate) is not AtomicGovernedPublisher
        or type(packet) is not SourceReviewPacket
        or type(checked_on) is not date
    ):
        raise ValueError("invalid integrated gate, packet or check date")
    if (
        not isinstance(trusted_fence_keys, Mapping)
        or not 1 <= len(trusted_fence_keys) <= _MAX_KEYS
        or any(
            type(key_id) is not str or _KEY_ID.fullmatch(key_id) is None
            or type(public) is not bytes or len(public) != 32
            for key_id, public in trusted_fence_keys.items()
        )
        or len(set(trusted_fence_keys.values())) != len(trusted_fence_keys)
    ):
        raise ValueError("invalid trusted integrated-fence public-key roster")
    message = _canonical_fence_message(fence)
    if (
        type(expected_current_authority_sequence) is not int
        or expected_current_authority_sequence != fence.authority_sequence
        or type(expected_current_fence_sha256) is not str
        or _SHA.fullmatch(expected_current_fence_sha256) is None
        or not compare_digest(_fence_sha256(fence), expected_current_fence_sha256)
    ):
        raise ValueError("supplied fence differs from expected external current fence")
    if (
        fence.authority_key_id not in trusted_fence_keys
        or type(packet.declaration_sha256) is not str
        or type(packet.snapshot_sha256) is not str
        or not compare_digest(packet.declaration_sha256, fence.packet_sha256)
        or not compare_digest(packet.snapshot_sha256, fence.snapshot_sha256)
    ):
        raise ValueError("fence signer or source packet binding does not match")
    if (
        type(packet.inspected_on) is not date
        or fence.issued_on < packet.inspected_on
        or checked_on < fence.issued_on
        or checked_on > fence.expires_on
    ):
        raise ValueError("integrated fence not yet valid, expired or before packet review")
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("integrated fence verification requires review extra") from None
    try:
        Ed25519PublicKey.from_public_bytes(
            trusted_fence_keys[fence.authority_key_id]
        ).verify(bytes.fromhex(fence.signature_hex), message)
    except (InvalidSignature, ValueError):
        raise ValueError("integrated fence signature invalid") from None
    snapshot = gate.snapshot(packet, checked_on=checked_on)
    if (
        snapshot.policy_revision != fence.policy_revision
        or not compare_digest(snapshot.policy_head_sha256, fence.policy_head_sha256)
        or snapshot.publication_sequence != fence.publication_sequence
        or not compare_digest(
            snapshot.publication_head_sha256, fence.publication_head_sha256
        )
    ):
        raise ValueError("integrated SQLite heads differ from supplied signed fence")
    return IntegratedHeadFenceAssessment(
        authority_sequence=fence.authority_sequence,
        supplied_fence_sha256=expected_current_fence_sha256,
        policy_revision=snapshot.policy_revision,
        publication_sequence=snapshot.publication_sequence,
        checked_on=checked_on,
    )
