"""Separate *local* SQLite registry of fully signed, witnessed integrated fences.

This is a second failure domain only if independently protected operationally.
This module never provisions witness keys, guarantees currentness, or grants
publication/source permissions. Two SQLite files have NO common transaction.
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Mapping
from dataclasses import asdict, dataclass, fields
from datetime import date
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path

from mirrormind.modules.evidence.atomic_governed_publisher import AtomicGovernedPublisher
from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.integrated_fence_transcript import (
    SignedIntegratedFenceTransition,
    _validate_rosters,
    _verify_one_transition,
    verify_integrated_fence_transcript,
)
from mirrormind.modules.evidence.integrated_head_fence import (
    SignedIntegratedHeadFence,
)

_GENESIS = "0" * 64
_SHA = re.compile(r"[0-9a-f]{64}")
_MAX_LINKS = 32
_MAX_LINK_BYTES = 8192
_VERSION = 1


@dataclass(frozen=True, slots=True)
class LocalFenceRegistryHead:
    """Replayed registry head, NOT a permission or independent timestamp."""

    authority_sequence: int
    fence_sha256: str
    policy_revision: int | None
    publication_sequence: int | None
    checked_on: date

    def receipt(self) -> dict[str, int | str | bool | None]:
        return {
            "status": "separate_local_registry_verified_not_independent_authority",
            "authority_sequence": self.authority_sequence,
            "fence_sha256": self.fence_sha256,
            "policy_revision": self.policy_revision,
            "publication_sequence": self.publication_sequence,
            "checked_on": self.checked_on.isoformat(),
            "currentness": "locally_durable_if_registry_file_intact",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _dump_link(link: SignedIntegratedFenceTransition) -> str:
    """Deterministic bounded JSON of complete signed payload, not just heads."""
    def encode(obj: object) -> str:
        if type(obj) is date:
            return obj.isoformat()
        raise TypeError("unsupported signed registry payload")

    value = json.dumps(
        asdict(link), default=encode, sort_keys=True, separators=(",", ":")
    )
    if len(value.encode("utf-8")) > _MAX_LINK_BYTES:
        raise ValueError("signed registry payload exceeds bounded size")
    return value


def _load_link(serialized: str) -> SignedIntegratedFenceTransition:
    """Strictly parse one stored canonical transition; refuse extra/missing fields."""
    if (
        type(serialized) is not str
        or len(serialized.encode("utf-8")) > _MAX_LINK_BYTES
    ):
        raise ValueError("invalid stored signed registry payload size")
    def unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate signed registry JSON key")
            result[key] = value
        return result

    try:
        raw = json.loads(serialized, object_pairs_hook=unique_pairs)
        link_fields = {f.name for f in fields(SignedIntegratedFenceTransition)}
        fence_fields = {f.name for f in fields(SignedIntegratedHeadFence)}
        if (
            type(raw) is not dict or set(raw) != link_fields
            or type(raw["fence"]) is not dict
            or set(raw["fence"]) != fence_fields
            or type(raw["witness_key_ids"]) is not list
            or type(raw["witness_signatures_hex"]) is not list
            or len(raw["witness_key_ids"]) != 2
            or len(raw["witness_signatures_hex"]) != 2
        ):
            raise ValueError("malformed stored signed registry structure")
        nested = dict(raw["fence"])
        nested["issued_on"] = date.fromisoformat(nested["issued_on"])
        nested["expires_on"] = date.fromisoformat(nested["expires_on"])
        record = dict(raw)
        record["fence"] = SignedIntegratedHeadFence(**nested)
        record["witnessed_on"] = date.fromisoformat(record["witnessed_on"])
        record["witness_key_ids"] = tuple(record["witness_key_ids"])
        record["witness_signatures_hex"] = tuple(record["witness_signatures_hex"])
        result = SignedIntegratedFenceTransition(**record)
        if _dump_link(result) != serialized:
            raise ValueError("noncanonical stored signed registry encoding")
        return result
    except (TypeError, KeyError, UnicodeError, json.JSONDecodeError, OverflowError):
        raise ValueError("invalid stored signed registry payload") from None


class LocalIntegratedFenceRegistry:
    """CAS-persist one packet's witnessed fence chain in a distinct SQLite file.

    This is **not** independent externally operated storage. The operator
    must protect the file and signer keys separately; restoring both files
    together defeats the local rollback diagnostic.
    """

    def __init__(
        self,
        path: Path,
        gate: AtomicGovernedPublisher,
        packet: SourceReviewPacket,
        *,
        trusted_fence_keys: Mapping[str, bytes],
        trusted_witness_keys: Mapping[str, bytes],
        create: bool = False,
    ) -> None:
        if (
            type(gate) is not AtomicGovernedPublisher
            or type(packet) is not SourceReviewPacket
            or not isinstance(path, Path)
            or not path.is_absolute()
            or not path.parent.is_dir()
            or path.is_symlink()
            or path.resolve() == gate._path.resolve()
            or type(create) is not bool
        ):
            raise ValueError("registry requires separate safe absolute SQLite path")
        _validate_rosters(trusted_fence_keys, trusted_witness_keys)
        if (
            type(packet.declaration_sha256) is not str
            or _SHA.fullmatch(packet.declaration_sha256) is None
            or type(packet.snapshot_sha256) is not str
            or _SHA.fullmatch(packet.snapshot_sha256) is None
        ):
            raise ValueError("registry source packet digest invalid")
        self._path = path
        self._gate = gate
        self._packet = packet
        self._fence_keys = dict(trusted_fence_keys)
        self._witness_keys = dict(trusted_witness_keys)
        roles = json.dumps(
            {
                "fence": {k: v.hex() for k, v in sorted(self._fence_keys.items())},
                "witness": {k: v.hex() for k, v in sorted(self._witness_keys.items())},
            },
            sort_keys=True, separators=(",", ":"),
        )
        self._roster_digest = sha256(roles.encode("utf-8")).hexdigest()
        if create:
            if path.exists():
                raise ValueError("refuse to recreate existing signed registry")
            db = self._connect()
            try:
                db.execute("BEGIN IMMEDIATE")
                db.execute(
                    "CREATE TABLE registry_identity("
                    "version INTEGER NOT NULL, packet_sha TEXT NOT NULL,"
                    "snapshot_sha TEXT NOT NULL, roster_sha TEXT NOT NULL)"
                )
                db.execute(
                    "CREATE TABLE signed_transitions("
                    "seq INTEGER PRIMARY KEY, signed_json TEXT NOT NULL)"
                )
                db.execute(
                    "INSERT INTO registry_identity VALUES(?,?,?,?)",
                    (_VERSION, packet.declaration_sha256,
                     packet.snapshot_sha256, self._roster_digest),
                )
                db.execute("COMMIT")
            except sqlite3.DatabaseError:
                raise ValueError("cannot initialize separate signed registry") from None
            finally:
                if db.in_transaction:
                    db.rollback()
                db.close()
        elif not path.is_file():
            raise ValueError("separate signed registry file absent: fail closed")
        db = self._connect()
        try:
            db.execute("BEGIN")
            self._verify_schema(db)
            db.execute("COMMIT")
        except sqlite3.DatabaseError:
            raise ValueError("separate registry schema unreadable") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path, timeout=5, isolation_level=None)

    def _verify_schema(self, db: sqlite3.Connection) -> None:
        rows = db.execute(
            "SELECT version,packet_sha,snapshot_sha,roster_sha FROM registry_identity"
        ).fetchall()
        if rows != [(
            _VERSION, self._packet.declaration_sha256,
            self._packet.snapshot_sha256, self._roster_digest,
        )]:
            raise ValueError("registry packet, schema or trusted roster changed")

    def _replay(
        self, db: sqlite3.Connection, checked_on: date,
    ) -> tuple[LocalFenceRegistryHead, tuple[SignedIntegratedFenceTransition, ...]]:
        self._verify_schema(db)
        rows = db.execute(
            "SELECT seq,signed_json FROM signed_transitions ORDER BY seq LIMIT 33"
        ).fetchall()
        if len(rows) > _MAX_LINKS:
            raise ValueError("signed registry history budget exceeded")
        previous_sequence = 0
        previous_digest = _GENESIS
        prior_fence: SignedIntegratedHeadFence | None = None
        prior_witnessed_on: date | None = None
        links: list[SignedIntegratedFenceTransition] = []
        for seq, payload in rows:
            link = _load_link(payload)
            if (
                type(seq) is not int
                or seq != previous_sequence + 1
                or link.previous_authority_sequence != previous_sequence
                or not compare_digest(link.previous_fence_sha256, previous_digest)
                or link.fence.authority_sequence != seq
                or (
                    prior_witnessed_on is not None
                    and link.witnessed_on < prior_witnessed_on
                )
            ):
                raise ValueError("separate registry missing or diverging signed link")
            current_digest = _verify_one_transition(
                link, self._packet,
                trusted_fence_keys=self._fence_keys,
                trusted_witness_keys=self._witness_keys,
                checked_on=checked_on,
            )
            if prior_fence is not None and (
                link.fence.policy_revision < prior_fence.policy_revision
                or link.fence.publication_sequence < prior_fence.publication_sequence
                or (
                    link.fence.policy_revision == prior_fence.policy_revision
                    and link.fence.policy_head_sha256 != prior_fence.policy_head_sha256
                )
                or (
                    link.fence.publication_sequence == prior_fence.publication_sequence
                    and link.fence.publication_head_sha256
                    != prior_fence.publication_head_sha256
                )
            ):
                raise ValueError("separate registry signed policy/publication rollback")
            previous_sequence, previous_digest = seq, current_digest
            prior_fence, prior_witnessed_on = link.fence, link.witnessed_on
            links.append(link)
        head = LocalFenceRegistryHead(
            authority_sequence=previous_sequence,
            fence_sha256=previous_digest,
            policy_revision=prior_fence.policy_revision if prior_fence else None,
            publication_sequence=(
                prior_fence.publication_sequence if prior_fence else None
            ),
            checked_on=checked_on,
        )
        return head, tuple(links)

    def head(self, *, checked_on: date) -> LocalFenceRegistryHead:
        """Read and verify all signed stored links, without trusting publisher DB."""
        if type(checked_on) is not date or checked_on < self._packet.inspected_on:
            raise ValueError("invalid signed-registry observation date")
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("signed-registry file unavailable")
        db = self._connect()
        try:
            db.execute("BEGIN")
            head, _ = self._replay(db, checked_on)
            db.execute("COMMIT")
            return head
        except sqlite3.DatabaseError:
            raise ValueError("signed registry read failed") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def compare_local(self, *, checked_on: date) -> LocalFenceRegistryHead:
        """Fail when governed publisher differs from verified separately stored pin.

        Cross-file read transactions are NOT globally atomic with publisher writes.
        """
        if type(checked_on) is not date or checked_on < self._packet.inspected_on:
            raise ValueError("invalid signed-registry comparison date")
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("signed-registry file unavailable")
        db = self._connect()
        try:
            db.execute("BEGIN")
            head, links = self._replay(db, checked_on)
            if not links:
                raise ValueError("no signed registry head: fail closed")
            verify_integrated_fence_transcript(
                self._gate, self._packet, links,
                trusted_fence_keys=self._fence_keys,
                trusted_witness_keys=self._witness_keys,
                anchor_authority_sequence=0, anchor_fence_sha256=_GENESIS,
                expected_current_authority_sequence=head.authority_sequence,
                expected_current_fence_sha256=head.fence_sha256,
                checked_on=checked_on,
            )
            db.execute("COMMIT")
            return head
        except sqlite3.DatabaseError:
            raise ValueError("signed registry/local comparison failed") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def append(
        self, link: SignedIntegratedFenceTransition, *,
        expected_authority_sequence: int,
        expected_fence_sha256: str,
        checked_on: date,
    ) -> LocalFenceRegistryHead:
        """Commit a next doubly witnessed fence with registry-local BEGIN IMMEDIATE.

        A separate publisher write may still race the snapshot read after it
        commits: the next comparison will fail closed until a fresh fence.
        """
        if (
            type(link) is not SignedIntegratedFenceTransition
            or type(checked_on) is not date
            or checked_on < self._packet.inspected_on
            or type(expected_authority_sequence) is not int
            or not 0 <= expected_authority_sequence < _MAX_LINKS
            or type(expected_fence_sha256) is not str
            or _SHA.fullmatch(expected_fence_sha256) is None
        ):
            raise ValueError("invalid registry append or compare-and-swap fence")
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("signed-registry file unavailable")
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            head, old_links = self._replay(db, checked_on)
            if (
                head.authority_sequence != expected_authority_sequence
                or not compare_digest(head.fence_sha256, expected_fence_sha256)
            ):
                raise ValueError("stale signed registry compare-and-swap head")
            if len(old_links) >= _MAX_LINKS:
                raise ValueError("signed registry history budget exceeded")
            next_links = (*old_links, link)
            next_digest = _fence_digest(link)
            verify_integrated_fence_transcript(
                self._gate, self._packet, next_links,
                trusted_fence_keys=self._fence_keys,
                trusted_witness_keys=self._witness_keys,
                anchor_authority_sequence=0, anchor_fence_sha256=_GENESIS,
                expected_current_authority_sequence=expected_authority_sequence + 1,
                expected_current_fence_sha256=next_digest,
                checked_on=checked_on,
            )
            db.execute(
                "INSERT INTO signed_transitions(seq,signed_json) VALUES(?,?)",
                (expected_authority_sequence + 1, _dump_link(link)),
            )
            db.execute("COMMIT")
            return LocalFenceRegistryHead(
                expected_authority_sequence + 1, next_digest,
                link.fence.policy_revision, link.fence.publication_sequence,
                checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("signed registry append aborted without commit") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()


def _fence_digest(link: SignedIntegratedFenceTransition) -> str:
    from mirrormind.modules.evidence.integrated_head_fence import _fence_sha256

    return _fence_sha256(link.fence)
