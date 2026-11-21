"""Volatile compare-and-swap registry for fictional signed source-review histories.

This object has no protected storage, independent clock, key custody or durable
freshness anchor. Restarting or replacing the instance loses rollback protection.
It NEVER authorizes source ingestion, regardless of review status.
"""
from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from hmac import compare_digest
from threading import RLock

from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SIGNATURE_RE,
    SignedReviewDecision,
    _canonical_review_message,
    verify_review_history,
)

MAX_LOCAL_PACKETS = 32
MAX_EVENTS_PER_PACKET = 64


@dataclass(frozen=True, slots=True)
class LocalReviewRevision:
    """Identifier-minimized snapshot; not a source authorization token."""

    revision: int
    log_head_sha256: str
    review_status: str
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Return only local revision metadata and explicitly blocked permissions."""
        return {
            "status": "volatile_signed_review_registry_not_authorization",
            "revision": self.revision,
            "log_head_sha256": self.log_head_sha256,
            "review_status": self.review_status,
            "checked_on": self.checked_on.isoformat(),
            "persistence_status": "process_memory_only_lost_on_restart",
            "head_trust_status": "local_not_independently_attested",
            "legal_rights_status": "not_verified",
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


class LocalReviewRegistry:
    """Atomic in-process append on a signed chain with expected revision and head.

    Caller is responsible for independently provisioning the reviewer public
    keys and for ensuring that only the review authority can append decisions.
    This class does not authenticate callers or survive process crashes.
    """

    def __init__(self, trusted_reviewer_keys: Mapping[str, bytes]) -> None:
        if not isinstance(trusted_reviewer_keys, Mapping) or not trusted_reviewer_keys:
            raise ValueError("trusted reviewer keys are required")
        # Copy the provided trust configuration so later caller mutations cannot
        # silently change the keys under which stored events were verified.
        keys = dict(trusted_reviewer_keys)
        if any(
            type(key_id) is not str or re.fullmatch(r"[A-Z][A-Z0-9_-]{3,39}", key_id) is None
            or type(public_key) is not bytes or len(public_key) != 32
            for key_id, public_key in keys.items()
        ):
            raise ValueError("invalid trusted reviewer key configuration")
        self._keys = keys
        self._entries: dict[
            str, tuple[SourceReviewPacket, tuple[SignedReviewDecision, ...], str]
        ] = {}
        self._lock = RLock()

    def _current(
        self, packet: SourceReviewPacket
    ) -> tuple[tuple[SignedReviewDecision, ...], str]:
        if type(packet) is not SourceReviewPacket:
            raise ValueError("expected an exact source review packet")
        if not isinstance(packet.declaration_sha256, str) or not re.fullmatch(
            r"[0-9a-f]{64}", packet.declaration_sha256
        ):
            raise ValueError("invalid packet digest")
        record = self._entries.get(packet.declaration_sha256)
        if record is None:
            return (), GENESIS_HEAD
        original, events, head = record
        if original != packet:
            raise ValueError("same manifest digest bound to different packet metadata")
        return events, head

    def snapshot(
        self, packet: SourceReviewPacket, *, checked_on: date
    ) -> LocalReviewRevision:
        """Inspect current in-process history; a snapshot is not a trusted fresh head."""
        with self._lock:
            events, head = self._current(packet)
            report = verify_review_history(
                packet, events,
                trusted_reviewer_keys=self._keys,
                expected_head_sha256=head, checked_on=checked_on,
            )
            return LocalReviewRevision(
                revision=len(events), log_head_sha256=head,
                review_status=report.review_status, checked_on=checked_on,
            )

    def append(
        self,
        packet: SourceReviewPacket,
        event: SignedReviewDecision,
        *,
        expected_revision: int,
        expected_head_sha256: str,
        checked_on: date,
    ) -> LocalReviewRevision:
        """Atomically append one signed event, rejecting stale or revoked writers.

        Expected values are read from this instance's current snapshot. They
        cannot protect against a replaced/restarted registry or a dishonest
        caller controlling the trust root.
        """
        with self._lock:
            prior, head = self._current(packet)
            if (
                type(expected_revision) is not int
                or expected_revision != len(prior)
                or type(expected_head_sha256) is not str
                or len(expected_head_sha256) != 64
                or not compare_digest(expected_head_sha256, head)
            ):
                raise ValueError("stale local review revision or log head")
            if len(prior) >= MAX_EVENTS_PER_PACKET:
                raise ValueError("local review history exceeds bounded event budget")
            if any(item.decision == "revoke" for item in prior):
                raise ValueError("revoked packet cannot receive more review events")
            if type(event) is not SignedReviewDecision:
                raise ValueError("expected an exact signed review decision")
            if (
                type(event.decided_on) is not date
                or (event.expires_on is not None and type(event.expires_on) is not date)
                or type(event.signature_hex) is not str
                or SIGNATURE_RE.fullmatch(event.signature_hex) is None
            ):
                raise ValueError("invalid signed review event metadata")
            # This is the *candidate* next head; the verifier must validate
            # the entire proposed chain before any state is modified.
            signature = bytes.fromhex(event.signature_hex)
            candidate_head = sha256(_canonical_review_message(event) + signature).hexdigest()
            proposed = (*prior, event)
            assessed = verify_review_history(
                packet, proposed,
                trusted_reviewer_keys=self._keys,
                expected_head_sha256=candidate_head, checked_on=checked_on,
            )
            if not prior and len(self._entries) >= MAX_LOCAL_PACKETS:
                raise ValueError("local registry exceeds packet budget")
            self._entries[packet.declaration_sha256] = (packet, proposed, candidate_head)
            return LocalReviewRevision(
                revision=len(proposed), log_head_sha256=candidate_head,
                review_status=assessed.review_status, checked_on=checked_on,
            )
