"""Experimental in-process responder for the challenged current-head wire contract.

This module is a pure HTTP-shaped handler boundary. It does not bind a socket,
authenticate callers, persist state or establish an independently operated
authority. A future transport may adapt these request and response records.
"""
from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta
from types import MappingProxyType
from typing import Protocol

from mirrormind.modules.evidence.remote_fence_head_protocol import (
    _ENDPOINT_PATH,
    _ID,
    _MAX_RESPONSE_BYTES,
    _MAX_TTL_SECONDS,
    _SHA,
    SignedRemoteFenceHead,
    _canonical_remote_message,
    _signed_wire,
    _valid_endpoint,
)

_REQUEST_QUERY = re.compile(r"nonce=([0-9a-f]{64})&packet_sha256=([0-9a-f]{64})")
_MAX_QUERY_LENGTH = len("nonce=") + 64 + len("&packet_sha256=") + 64
_MAX_NON_SERVICE_KEYS = 16


@dataclass(frozen=True, slots=True)
class CurrentRemoteFenceHead:
    """One store-supplied claim; it contains digests, never source payloads."""

    packet_sha256: str
    snapshot_sha256: str
    authority_sequence: int
    fence_sha256: str


class RemoteFenceHeadStoreError(Exception):
    """A store adapter cannot safely provide the requested current record."""


class RemoteFenceHeadClockError(Exception):
    """A clock adapter cannot safely provide the requested UTC instant."""


class RemoteFenceHeadStore(Protocol):
    """Read contract for a future separately implemented current-head store.

    Implementations must return the current record for the exact packet digest
    or ``None`` when no record exists. This Protocol has no persistence,
    transaction, authentication or independent-administration guarantee.
    Expected operational read failures must be translated to
    ``RemoteFenceHeadStoreError``; programming errors should remain visible.
    """

    def read_current(self, packet_sha256: str) -> CurrentRemoteFenceHead | None:
        """Return the claimed head or raise ``RemoteFenceHeadStoreError``."""


@dataclass(frozen=True, slots=True)
class RemoteFenceHeadRequest:
    """Minimal decoded request fields consumed by the responder."""

    method: str
    path: str
    query_string: str
    accept: str


@dataclass(frozen=True, slots=True)
class RemoteFenceHeadResponse:
    """Transport-neutral status, headers and bounded response bytes."""

    status_code: int
    headers: Mapping[str, str]
    body: bytes

    def __post_init__(self) -> None:
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))


class RemoteFenceHeadResponder:
    """Sign one fixed-path nonce challenge from a typed current-head store.

    The injected clock translates expected operational failures to
    ``RemoteFenceHeadClockError``. Other adapter exceptions propagate to the
    in-process caller rather than being hidden by a broad exception handler.
    """

    __slots__ = (
        "_clock",
        "_endpoint",
        "_non_service_public_keys",
        "_service_id",
        "_service_key_id",
        "_signing_key",
        "_store",
        "_ttl_seconds",
    )

    def __init__(
        self,
        *,
        service_id: str,
        service_key_id: str,
        endpoint: str,
        signing_key: object,
        non_service_public_keys: Mapping[str, bytes],
        store: RemoteFenceHeadStore,
        clock: Callable[[], datetime],
        ttl_seconds: int = 60,
    ) -> None:
        if type(service_id) is not str or _ID.fullmatch(service_id) is None:
            raise ValueError("invalid remote head service identity")
        if type(service_key_id) is not str or _ID.fullmatch(service_key_id) is None:
            raise ValueError("invalid remote head service key identity")
        _valid_endpoint(endpoint)
        if type(ttl_seconds) is not int or not 1 <= ttl_seconds <= _MAX_TTL_SECONDS:
            raise ValueError("remote head response validity interval must be 1-120 seconds")
        if not callable(clock) or not callable(getattr(store, "read_current", None)):
            raise TypeError("remote head clock and store reader must be callable")
        if (
            not isinstance(non_service_public_keys, Mapping)
            or not 1 <= len(non_service_public_keys) <= _MAX_NON_SERVICE_KEYS
            or any(
                type(key_id) is not str or _ID.fullmatch(key_id) is None
                or type(public_key) is not bytes or len(public_key) != 32
                for key_id, public_key in non_service_public_keys.items()
            )
            or len(set(non_service_public_keys.values())) != len(non_service_public_keys)
        ):
            raise ValueError("invalid non-service public-key configuration")
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PrivateKey,
            )
            from cryptography.hazmat.primitives.serialization import (
                Encoding,
                PublicFormat,
            )
        except ImportError:
            raise RuntimeError("remote head signing requires the review extra") from None
        if not isinstance(signing_key, Ed25519PrivateKey):
            raise TypeError("remote head signing key must be Ed25519 private key")
        service_public_key = signing_key.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        if (
            service_key_id in non_service_public_keys
            or service_public_key in non_service_public_keys.values()
        ):
            raise ValueError("remote service signer role must be distinct")

        self._service_id = service_id
        self._service_key_id = service_key_id
        self._endpoint = endpoint
        self._signing_key = signing_key
        self._store = store
        self._clock = clock
        self._ttl_seconds = ttl_seconds
        # Freeze a defensive copy so caller mutation cannot change the checked roster.
        self._non_service_public_keys = MappingProxyType(dict(non_service_public_keys))

    def respond(self, request: RemoteFenceHeadRequest) -> RemoteFenceHeadResponse:
        """Return one canonical signed response, or a bodyless generic failure."""
        if type(request) is not RemoteFenceHeadRequest:
            return _empty_response(400)
        if type(request.method) is not str:
            return _empty_response(400)
        if request.method != "GET":
            return _empty_response(405, allow_get=True)
        if type(request.path) is not str or request.path != _ENDPOINT_PATH:
            return _empty_response(404)
        if type(request.accept) is not str or request.accept != "application/json":
            return _empty_response(406)
        if type(request.query_string) is not str:
            return _empty_response(400)
        if len(request.query_string) != _MAX_QUERY_LENGTH:
            return _empty_response(400)
        match = _REQUEST_QUERY.fullmatch(request.query_string)
        if match is None:
            return _empty_response(400)
        nonce_hex, packet_sha256 = match.groups()
        if _SHA.fullmatch(packet_sha256) is None:
            return _empty_response(400)

        try:
            current = self._store.read_current(packet_sha256)
        except RemoteFenceHeadStoreError:
            # Do not let an adapter exception or its contents cross the wire boundary.
            return _empty_response(503)
        if current is None:
            return _empty_response(404)
        if type(current) is not CurrentRemoteFenceHead:
            return _empty_response(503)
        if current.packet_sha256 != packet_sha256:
            # A store that returns a different scope violates its read contract.
            return _empty_response(404)

        try:
            now = self._clock()
        except RemoteFenceHeadClockError:
            # Keep expected adapter details behind the generic wire failure.
            return _empty_response(503)
        if type(now) is not datetime:
            return _empty_response(503)
        try:
            if now.utcoffset() != timedelta(0):
                return _empty_response(503)
            issued = now.astimezone(UTC).replace(microsecond=0)
            expires = issued + timedelta(seconds=self._ttl_seconds)
            unsigned = SignedRemoteFenceHead(
                service_id=self._service_id,
                service_key_id=self._service_key_id,
                endpoint=self._endpoint,
                nonce_hex=nonce_hex,
                packet_sha256=current.packet_sha256,
                snapshot_sha256=current.snapshot_sha256,
                authority_sequence=current.authority_sequence,
                fence_sha256=current.fence_sha256,
                issued_at_utc=issued.strftime("%Y-%m-%dT%H:%M:%SZ"),
                expires_at_utc=expires.strftime("%Y-%m-%dT%H:%M:%SZ"),
                signature_hex="0" * 128,
            )
            signature = self._signing_key.sign(
                _canonical_remote_message(unsigned)
            ).hex()
            body = _signed_wire(replace(unsigned, signature_hex=signature))
            if not 0 < len(body) <= _MAX_RESPONSE_BYTES:
                return _empty_response(503)
        except (OverflowError, TypeError, ValueError):
            # Invalid persisted records and unrepresentable times fail closed.
            return _empty_response(503)
        return RemoteFenceHeadResponse(
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "no-store",
                "Content-Length": str(len(body)),
            },
            body=body,
        )


def _empty_response(status_code: int, *, allow_get: bool = False) -> RemoteFenceHeadResponse:
    headers = {"Cache-Control": "no-store", "Content-Length": "0"}
    if allow_get:
        headers["Allow"] = "GET"
    return RemoteFenceHeadResponse(status_code, headers, b"")
