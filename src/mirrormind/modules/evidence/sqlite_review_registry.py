"""Transactional SQLite storage for synthetic signed review histories.

Durability of a local database is NOT independent authorization or a fresh,
externally anchored audit log. The caller controls keys, clock and DB path.
No source ingestion or forecasting can be enabled by this module.
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import date
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path

from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SIGNATURE_RE,
    SignedReviewDecision,
    _canonical_review_message,
    verify_review_history,
)

MAX_STORED_PACKETS = 32
MAX_STORED_EVENTS = 64
SCHEMA_VERSION = 1
_DIGEST = re.compile(r"[0-9a-f]{64}")
_KEY_ID = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")


def _json(data: dict[str, object]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _packet_json(packet: SourceReviewPacket) -> str:
    if type(packet) is not SourceReviewPacket:
        raise ValueError("expected an exact source review packet")
    if (
        type(packet.declaration_sha256) is not str
        or _DIGEST.fullmatch(packet.declaration_sha256) is None
        or type(packet.snapshot_sha256) is not str
        or _DIGEST.fullmatch(packet.snapshot_sha256) is None
        or type(packet.captured_on) is not date
        or type(packet.inspected_on) is not date
    ):
        raise ValueError("invalid source packet metadata")
    record = asdict(packet)
    record["captured_on"] = packet.captured_on.isoformat()
    record["inspected_on"] = packet.inspected_on.isoformat()
    return _json(record)


def _event_json(event: SignedReviewDecision) -> str:
    if (
        type(event) is not SignedReviewDecision
        or type(event.decided_on) is not date
        or (event.expires_on is not None and type(event.expires_on) is not date)
        or type(event.signature_hex) is not str
        or SIGNATURE_RE.fullmatch(event.signature_hex) is None
    ):
        raise ValueError("invalid signed review event")
    record = asdict(event)
    record["decided_on"] = event.decided_on.isoformat()
    record["expires_on"] = event.expires_on.isoformat() if event.expires_on else None
    return _json(record)


def _parse_event(serialized: str) -> SignedReviewDecision:
    """Fail closed on unexpected or rewritten persisted event encodings."""
    try:
        fields = json.loads(serialized)
        if type(fields) is not dict:
            raise ValueError
        fields["decided_on"] = date.fromisoformat(fields["decided_on"])
        if fields["expires_on"] is not None:
            fields["expires_on"] = date.fromisoformat(fields["expires_on"])
        event = SignedReviewDecision(**fields)
        if _event_json(event) != serialized:
            raise ValueError
        return event
    except (TypeError, KeyError, ValueError, OverflowError):
        raise ValueError("stored review event is invalid") from None


@dataclass(frozen=True, slots=True)
class SQLiteReviewRevision:
    """Non-authorizing local snapshot of the stored signed history."""

    revision: int
    log_head_sha256: str
    review_status: str
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Report integrity status without exposing any source or reviewer IDs."""
        return {
            "status": "local_sqlite_signed_review_not_ingestion_authorization",
            "revision": self.revision,
            "log_head_sha256": self.log_head_sha256,
            "review_status": self.review_status,
            "checked_on": self.checked_on.isoformat(),
            "persistence_status": "local_sqlite_transactional_not_tamper_proof",
            "head_trust_status": "database_head_not_externally_attested",
            "permission_status": "human_legal_permission_not_verified",
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


class SQLiteReviewRegistry:
    """Per-packet signed event log using SQLite BEGIN IMMEDIATE transactions.

    A protected source of reviewer public keys, trusted wall clock, and
    independently current head must exist OUTSIDE this library before a
    real application can depend on its history. No access control is added.
    """

    def __init__(
        self, db_path: Path, trusted_reviewer_keys: Mapping[str, bytes],
        *, create: bool = False,
    ) -> None:
        if not isinstance(db_path, Path) or not db_path.is_absolute():
            raise ValueError("database must have an explicit absolute local path")
        if db_path.is_symlink() or not db_path.parent.is_dir():
            raise ValueError("database path must have an existing local parent")
        if not isinstance(trusted_reviewer_keys, Mapping) or not trusted_reviewer_keys:
            raise ValueError("trusted reviewer public keys required")
        keys = dict(trusted_reviewer_keys)
        if any(
            type(key_id) is not str or _KEY_ID.fullmatch(key_id) is None
            or type(key) is not bytes or len(key) != 32
            for key_id, key in keys.items()
        ):
            raise ValueError("invalid trusted reviewer key configuration")
        if type(create) is not bool:
            raise ValueError("create must be an exact boolean")
        self._path = db_path
        self._keys = keys
        if create:
            if db_path.exists():
                raise ValueError("refusing to replace existing review registry")
            connection = sqlite3.connect(str(db_path), timeout=5, isolation_level=None)
            try:
                connection.execute("PRAGMA foreign_keys = ON")
                connection.execute("PRAGMA synchronous = FULL")
                connection.execute("BEGIN IMMEDIATE")
                connection.execute(
                    "CREATE TABLE registry_schema (version INTEGER NOT NULL)"
                )
                connection.execute(
                    "INSERT INTO registry_schema(version) VALUES (?)", (SCHEMA_VERSION,)
                )
                connection.execute(
                    "CREATE TABLE packet_heads ("
                    " packet_sha256 TEXT PRIMARY KEY,"
                    " packet_json TEXT NOT NULL,"
                    " revision INTEGER NOT NULL,"
                    " log_head_sha256 TEXT NOT NULL)"
                )
                connection.execute(
                    "CREATE TABLE review_events ("
                    " packet_sha256 TEXT NOT NULL,"
                    " sequence INTEGER NOT NULL,"
                    " event_json TEXT NOT NULL,"
                    " PRIMARY KEY (packet_sha256, sequence),"
                    " FOREIGN KEY (packet_sha256)"
                    " REFERENCES packet_heads(packet_sha256))"
                )
                connection.execute("COMMIT")
            except sqlite3.DatabaseError:
                connection.rollback()
                raise ValueError("cannot initialize review registry schema") from None
            finally:
                connection.close()
        if not db_path.is_file():
            raise ValueError("review registry database does not exist")
        with self._connection() as connection:
            self._validate_schema(connection)

    def _connection(self) -> sqlite3.Connection:
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("review registry database is missing or unsafe")
        try:
            connection = sqlite3.connect(str(self._path), timeout=5, isolation_level=None)
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA busy_timeout = 5000")
            connection.execute("PRAGMA synchronous = FULL")
            return connection
        except sqlite3.DatabaseError:
            raise ValueError("cannot open review registry database") from None

    @staticmethod
    def _validate_schema(connection: sqlite3.Connection) -> None:
        try:
            rows = connection.execute("SELECT version FROM registry_schema").fetchall()
            if rows != [(SCHEMA_VERSION,)]:
                raise ValueError("unsupported review registry schema")
            # Do not initialize or silently repair a damaged existing database.
            for table in ("packet_heads", "review_events"):
                connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        except sqlite3.DatabaseError:
            raise ValueError("invalid existing review registry schema") from None

    @staticmethod
    def _load(
        connection: sqlite3.Connection, packet: SourceReviewPacket,
    ) -> tuple[tuple[SignedReviewDecision, ...], str]:
        serialized = _packet_json(packet)
        row = connection.execute(
            "SELECT packet_json, revision, log_head_sha256"
            " FROM packet_heads WHERE packet_sha256 = ?",
            (packet.declaration_sha256,),
        ).fetchone()
        if row is None:
            return (), GENESIS_HEAD
        stored_packet, revision, head = row
        if stored_packet != serialized:
            raise ValueError("stored packet identity differs from signed manifest")
        if (
            type(revision) is not int or not 1 <= revision <= MAX_STORED_EVENTS
            or type(head) is not str or _DIGEST.fullmatch(head) is None
        ):
            raise ValueError("stored review revision or head is invalid")
        rows = connection.execute(
            "SELECT sequence, event_json FROM review_events"
            " WHERE packet_sha256 = ? ORDER BY sequence",
            (packet.declaration_sha256,),
        ).fetchall()
        if len(rows) != revision or [seq for seq, _ in rows] != list(range(1, revision + 1)):
            raise ValueError("stored signed review history has gaps or missing events")
        events = tuple(_parse_event(event_json) for _, event_json in rows)
        if any(item.decision == "revoke" for item in events[:-1]):
            raise ValueError("stored review history contains events after revocation")
        return events, head

    def snapshot(
        self, packet: SourceReviewPacket, *, checked_on: date,
        externally_expected_head_sha256: str | None = None,
    ) -> SQLiteReviewRevision:
        """Verify stored signatures, with optional *independent* rollback anchor."""
        connection = self._connection()
        try:
            connection.execute("BEGIN")
            self._validate_schema(connection)
            events, head = self._load(connection, packet)
            if externally_expected_head_sha256 is not None and (
                type(externally_expected_head_sha256) is not str
                or _DIGEST.fullmatch(externally_expected_head_sha256) is None
                or not compare_digest(head, externally_expected_head_sha256)
            ):
                raise ValueError("review database differs from externally trusted log head")
            assessed = verify_review_history(
                packet, events, trusted_reviewer_keys=self._keys,
                expected_head_sha256=head, checked_on=checked_on,
            )
            connection.execute("COMMIT")
            return SQLiteReviewRevision(
                revision=len(events), log_head_sha256=head,
                review_status=assessed.review_status, checked_on=checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("review database read failed") from None
        finally:
            if connection.in_transaction:
                connection.rollback()
            connection.close()

    def append(
        self, packet: SourceReviewPacket, event: SignedReviewDecision,
        *, expected_revision: int, expected_head_sha256: str, checked_on: date,
    ) -> SQLiteReviewRevision:
        """Atomically compare the current stored head and append a signed event."""
        connection = self._connection()
        try:
            connection.execute("BEGIN IMMEDIATE")
            self._validate_schema(connection)
            events, head = self._load(connection, packet)
            if (
                type(expected_revision) is not int
                or expected_revision != len(events)
                or type(expected_head_sha256) is not str
                or _DIGEST.fullmatch(expected_head_sha256) is None
                or not compare_digest(head, expected_head_sha256)
            ):
                raise ValueError("stale review revision or head")
            if len(events) >= MAX_STORED_EVENTS:
                raise ValueError("review history exceeds event budget")
            if any(old.decision == "revoke" for old in events):
                raise ValueError("revoked review packet cannot be appended")
            serialized_event = _event_json(event)
            candidate_head = sha256(
                _canonical_review_message(event) + bytes.fromhex(event.signature_hex)
            ).hexdigest()
            proposed = (*events, event)
            assessed = verify_review_history(
                packet, proposed, trusted_reviewer_keys=self._keys,
                expected_head_sha256=candidate_head, checked_on=checked_on,
            )
            if not events:
                if connection.execute("SELECT COUNT(*) FROM packet_heads").fetchone()[0] >= (
                    MAX_STORED_PACKETS
                ):
                    raise ValueError("review registry exceeds packet budget")
                connection.execute(
                    "INSERT INTO packet_heads "
                    "(packet_sha256,packet_json,revision,log_head_sha256)"
                    " VALUES (?,?,?,?)",
                    (packet.declaration_sha256, _packet_json(packet), 0, GENESIS_HEAD),
                )
            connection.execute(
                "INSERT INTO review_events (packet_sha256,sequence,event_json)"
                " VALUES (?,?,?)",
                (packet.declaration_sha256, len(proposed), serialized_event),
            )
            connection.execute(
                "UPDATE packet_heads SET revision = ?, log_head_sha256 = ?"
                " WHERE packet_sha256 = ?",
                (len(proposed), candidate_head, packet.declaration_sha256),
            )
            connection.execute("COMMIT")
            return SQLiteReviewRevision(
                revision=len(proposed), log_head_sha256=candidate_head,
                review_status=assessed.review_status, checked_on=checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("review database write failed without commit") from None
        finally:
            if connection.in_transaction:
                connection.rollback()
            connection.close()
