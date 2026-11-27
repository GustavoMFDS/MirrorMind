"""Shared canonical wire contract for challenged remote fence-head messages.

The client verifies and the in-process service signs the same immutable record
through these helpers. Keeping canonicalization here prevents either side from
silently defining a second JSON or signature format.
"""
from __future__ import annotations

import ipaddress
import json
import re
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timedelta
from urllib.parse import urlsplit

_DOMAIN = "mirrormind.remote-fence-head-challenge.v1"
_ENDPOINT_PATH = "/v1/integrated-fence/head"
_SHA = re.compile(r"[0-9a-f]{64}")
_SIGNATURE = re.compile(r"[0-9a-f]{128}")
_ID = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
_DNS = re.compile(
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+"
)
_UTC_SECONDS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_MAX_RESPONSE_BYTES = 4096
_MAX_TTL_SECONDS = 120
_MAX_SEQUENCE = 1_000_000_000


@dataclass(frozen=True, slots=True)
class SignedRemoteFenceHead:
    """Remote service signature over one challenge-bound claimed current head."""

    service_id: str
    service_key_id: str
    endpoint: str
    nonce_hex: str
    packet_sha256: str
    snapshot_sha256: str
    authority_sequence: int
    fence_sha256: str
    issued_at_utc: str
    expires_at_utc: str
    signature_hex: str


def _utc(raw: str) -> datetime:
    if type(raw) is not str or _UTC_SECONDS.fullmatch(raw) is None:
        raise ValueError("remote signed head must use exact UTC-second timestamps")
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        raise ValueError("invalid remote signed head calendar instant") from None


def _valid_endpoint(endpoint: str) -> None:
    """Avoid arbitrary URLs: an explicit fixed path, canonical public DNS, TLS."""
    if type(endpoint) is not str or len(endpoint) > 256:
        raise ValueError("invalid configured remote head HTTPS endpoint")
    parts = urlsplit(endpoint)
    host = parts.hostname
    try:
        ipaddress.ip_address(host or "")
    except ValueError:
        pass
    else:
        raise ValueError("remote head endpoint cannot be an IP literal")
    if (
        parts.scheme != "https"
        or type(host) is not str
        or _DNS.fullmatch(host) is None
        or endpoint != f"https://{host}{_ENDPOINT_PATH}"
        or parts.username is not None
        or parts.password is not None
        or parts.port is not None
        or parts.query
        or parts.fragment
    ):
        raise ValueError("remote head endpoint must be canonical fixed-path HTTPS DNS")


def _canonical_remote_message(head: SignedRemoteFenceHead) -> bytes:
    """All signed fields in a protocol-specific domain excluding signature."""
    if type(head) is not SignedRemoteFenceHead:
        raise ValueError("invalid signed remote head type")
    if (
        type(head.service_id) is not str
        or _ID.fullmatch(head.service_id) is None
        or type(head.service_key_id) is not str
        or _ID.fullmatch(head.service_key_id) is None
        or type(head.nonce_hex) is not str
        or _SHA.fullmatch(head.nonce_hex) is None
        or type(head.packet_sha256) is not str
        or _SHA.fullmatch(head.packet_sha256) is None
        or type(head.snapshot_sha256) is not str
        or _SHA.fullmatch(head.snapshot_sha256) is None
        or type(head.fence_sha256) is not str
        or _SHA.fullmatch(head.fence_sha256) is None
        or type(head.authority_sequence) is not int
        or not 1 <= head.authority_sequence <= _MAX_SEQUENCE
    ):
        raise ValueError("invalid signed remote head identity/digest/sequence")
    _valid_endpoint(head.endpoint)
    issued, expires = _utc(head.issued_at_utc), _utc(head.expires_at_utc)
    if not issued < expires or expires - issued > timedelta(seconds=_MAX_TTL_SECONDS):
        raise ValueError("remote signed response validity interval invalid")
    record = {
        "domain": _DOMAIN,
        "service_id": head.service_id,
        "service_key_id": head.service_key_id,
        "endpoint": head.endpoint,
        "nonce_hex": head.nonce_hex,
        "packet_sha256": head.packet_sha256,
        "snapshot_sha256": head.snapshot_sha256,
        "authority_sequence": head.authority_sequence,
        "fence_sha256": head.fence_sha256,
        "issued_at_utc": head.issued_at_utc,
        "expires_at_utc": head.expires_at_utc,
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _signed_wire(head: SignedRemoteFenceHead) -> bytes:
    """Canonical complete signed JSON response; no raw source data."""
    return json.dumps(asdict(head), sort_keys=True, separators=(",", ":")).encode("utf-8")


def _parse_signed_response(raw: bytes) -> SignedRemoteFenceHead:
    if type(raw) is not bytes or not 0 < len(raw) <= _MAX_RESPONSE_BYTES:
        raise ValueError("remote signed response exceeds bounded size or is missing")

    def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("remote signed response contains duplicate JSON keys")
            result[key] = value
        return result

    def _no_nonfinite(_: str) -> object:
        raise ValueError("remote signed response has invalid JSON numeric constant")

    try:
        data = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_unique_pairs,
            parse_constant=_no_nonfinite,
        )
        if type(data) is not dict or set(data) != {
            field.name for field in fields(SignedRemoteFenceHead)
        }:
            raise ValueError("remote signed response missing or extra fields")
        head = SignedRemoteFenceHead(**data)
        if _signed_wire(head) != raw:
            raise ValueError("remote signed response is not canonical JSON")
        return head
    except (UnicodeError, TypeError, json.JSONDecodeError, RecursionError):
        raise ValueError("invalid remote signed response JSON") from None
