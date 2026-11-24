"""Experimental nonce-challenged signed HTTPS current-fence *reader*.

An online signer can prove that it saw the client's fresh random challenge.
It CANNOT prove that the signer is operationally independent or tells the
truth about the globally latest head; no service is deployed here.
"""
from __future__ import annotations

import secrets
import ssl
import urllib.error
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from hmac import compare_digest

from mirrormind.modules.evidence.local_integrated_fence_registry import (
    LocalIntegratedFenceRegistry,
)
from mirrormind.modules.evidence.remote_fence_head_protocol import (
    _ID,
    _MAX_RESPONSE_BYTES,
    _SHA,
    _SIGNATURE,
    SignedRemoteFenceHead,
    _canonical_remote_message,
    _parse_signed_response,
    _signed_wire,
    _utc,
    _valid_endpoint,
)

__all__ = [
    "RemoteHeadComparison",
    "SignedRemoteFenceHead",
    "_canonical_remote_message",
    "_parse_signed_response",
    "_signed_wire",
    "_valid_endpoint",
    "fetch_and_compare_remote_head",
    "verify_challenged_remote_head",
]

_MAX_REMOTE_KEYS = 8
_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True, slots=True)
class RemoteHeadComparison:
    """Local equality to an authenticated fresh reply, not source authorization."""

    authority_sequence: int
    current_fence_sha256: str
    response_sha256: str
    verified_at_utc: str

    def receipt(self) -> dict[str, int | str | bool]:
        return {
            "status": "challenged_remote_head_matches_local_signed_heads_only",
            "authority_sequence": self.authority_sequence,
            "current_fence_sha256": self.current_fence_sha256,
            "response_sha256": self.response_sha256,
            "verified_at_utc": self.verified_at_utc,
            "authentication": "nonce_bound_configured_service_key",
            "independent_authority_status": "not_established_by_this_client",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _validate_remote_keys(
    registry: LocalIntegratedFenceRegistry,
    trusted_service_keys: Mapping[str, bytes],
) -> None:
    if (
        type(registry) is not LocalIntegratedFenceRegistry
        or not isinstance(trusted_service_keys, Mapping)
        or not 1 <= len(trusted_service_keys) <= _MAX_REMOTE_KEYS
        or any(
            type(key_id) is not str or _ID.fullmatch(key_id) is None
            or type(public_key) is not bytes or len(public_key) != 32
            for key_id, public_key in trusted_service_keys.items()
        )
        or len(set(trusted_service_keys.values())) != len(trusted_service_keys)
    ):
        raise ValueError("invalid remote head service public-key configuration")
    all_local_keys = {**registry._fence_keys, **registry._witness_keys}
    if (
        set(trusted_service_keys).intersection(all_local_keys)
        or set(trusted_service_keys.values()).intersection(all_local_keys.values())
    ):
        raise ValueError("remote service signing role must differ from authority/witness")


def verify_challenged_remote_head(
    registry: LocalIntegratedFenceRegistry,
    raw_response: bytes,
    *,
    requested_nonce_hex: str,
    service_id: str,
    endpoint: str,
    trusted_service_keys: Mapping[str, bytes],
    checked_at: datetime,
) -> RemoteHeadComparison:
    """Verify a supplied online reply and compare against signed local heads.

    The checked_at clock is caller-provided in this offline helper. Use
    fetch_and_compare_remote_head for the production path's device UTC clock.
    """
    _valid_endpoint(endpoint)
    _validate_remote_keys(registry, trusted_service_keys)
    if (
        type(service_id) is not str
        or _ID.fullmatch(service_id) is None
        or type(requested_nonce_hex) is not str
        or _SHA.fullmatch(requested_nonce_hex) is None
        or type(checked_at) is not datetime
        or checked_at.utcoffset() != timedelta(0)
    ):
        raise ValueError("invalid remote head verifier challenge or UTC clock")
    head = _parse_signed_response(raw_response)
    message = _canonical_remote_message(head)
    if (
        type(head.signature_hex) is not str
        or _SIGNATURE.fullmatch(head.signature_hex) is None
        or head.service_id != service_id
        or head.endpoint != endpoint
        or head.service_key_id not in trusted_service_keys
        or not compare_digest(head.nonce_hex, requested_nonce_hex)
        or not compare_digest(head.packet_sha256, registry._packet.declaration_sha256)
        or not compare_digest(head.snapshot_sha256, registry._packet.snapshot_sha256)
    ):
        raise ValueError("remote signed head wrong service, signer, challenge or packet")
    if not _utc(head.issued_at_utc) <= checked_at < _utc(head.expires_at_utc):
        raise ValueError("remote signed head not yet valid or expired at checked UTC")
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("remote head verification requires review extra") from None
    try:
        Ed25519PublicKey.from_public_bytes(
            trusted_service_keys[head.service_key_id]
        ).verify(bytes.fromhex(head.signature_hex), message)
    except (InvalidSignature, ValueError):
        raise ValueError("remote signed head Ed25519 signature invalid") from None
    local_head = registry.compare_local(checked_on=checked_at.date())
    if (
        head.authority_sequence != local_head.authority_sequence
        or not compare_digest(head.fence_sha256, local_head.fence_sha256)
    ):
        raise ValueError("remote signed current head differs from local signed registry")
    return RemoteHeadComparison(
        authority_sequence=head.authority_sequence,
        current_fence_sha256=head.fence_sha256,
        response_sha256=sha256(raw_response).hexdigest(),
        verified_at_utc=checked_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self, request: object, file: object, code: object,
        message: object, headers: object, new_url: object,
    ) -> None:
        return None


def _https_read(endpoint: str, nonce_hex: str, packet_sha256: str) -> bytes:
    """Strict HTTPS GET, system CA chain, no redirects/proxies, bounded body."""
    request = urllib.request.Request(
        f"{endpoint}?nonce={nonce_hex}&packet_sha256={packet_sha256}",
        headers={"Accept": "application/json"},
        method="GET",
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        _NoRedirect(),
    )
    try:
        with opener.open(request, timeout=_TIMEOUT_SECONDS) as response:
            if (
                response.status != 200
                or response.headers.get_content_type() != "application/json"
            ):
                raise ValueError("remote head response has invalid HTTP status or type")
            raw = response.read(_MAX_RESPONSE_BYTES + 1)
    except (urllib.error.URLError, OSError, TimeoutError):
        raise ValueError("remote head HTTPS request failed closed") from None
    if len(raw) > _MAX_RESPONSE_BYTES:
        raise ValueError("remote head HTTP response exceeds byte budget")
    return raw


def fetch_and_compare_remote_head(
    registry: LocalIntegratedFenceRegistry,
    *,
    endpoint: str,
    service_id: str,
    trusted_service_keys: Mapping[str, bytes],
) -> RemoteHeadComparison:
    """Opt-in network query. A response signature does not prove true latest state."""
    _valid_endpoint(endpoint)
    _validate_remote_keys(registry, trusted_service_keys)
    if type(service_id) is not str or _ID.fullmatch(service_id) is None:
        raise ValueError("invalid expected remote service identity")
    nonce = secrets.token_hex(32)
    raw = _https_read(endpoint, nonce, registry._packet.declaration_sha256)
    # Use the local system UTC clock; independent secure time is not asserted.
    checked_at = datetime.now(UTC)
    return verify_challenged_remote_head(
        registry, raw, requested_nonce_hex=nonce,
        service_id=service_id, endpoint=endpoint,
        trusted_service_keys=trusted_service_keys,
        checked_at=checked_at,
    )
