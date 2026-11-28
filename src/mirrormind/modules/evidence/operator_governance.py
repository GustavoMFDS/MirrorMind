"""Experimental *local* dual-admin operator-key policy, not authorization.

No actual administrator identity, secure signer, external head custody,
publisher integration, source license, or real-data access is provided.
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path

GENESIS_POLICY_HEAD = "0" * 64
_MAX_ADMINS = 8
_MAX_OPERATORS = 32
_MAX_EVENTS = 64
_VERSION = 1
_NAME = re.compile(r"[A-Z][A-Z0-9_-]{3,39}")
_SHA = re.compile(r"[0-9a-f]{64}")
_SIGNATURE = re.compile(r"[0-9a-f]{128}")
_KEY_BYTES = re.compile(r"[0-9a-f]{64}")
_DOMAIN = "mirrormind.operator-policy.v1"


@dataclass(frozen=True, slots=True)
class SignedOperatorPolicyEvent:
    """Enrollment/revocation attested by two separate configured admins."""

    action: str
    operator_key_id: str
    operator_public_key_hex: str
    sequence: int
    previous_head_sha256: str
    issued_on: date
    expires_on: date | None
    admin_key_ids: tuple[str, str]
    first_signature_hex: str
    second_signature_hex: str


@dataclass(frozen=True, slots=True)
class OperatorPolicyRevision:
    """Local policy head; cannot be used to authorize publication."""

    revision: int
    head_sha256: str
    registered_count: int
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        return {
            "status": "local_operator_governance_not_publication_authority",
            "revision": self.revision,
            "head_sha256": self.head_sha256,
            "registered_count": self.registered_count,
            "checked_on": self.checked_on.isoformat(),
            "independent_head_status": "not_attested",
            "admin_identity_status": "supplied_public_keys_only",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


@dataclass(frozen=True, slots=True)
class OperatorPolicyAssessment:
    """A record status, NOT a valid permission to publish or ingest."""

    record_status: str
    revision: int
    head_sha256: str
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        return {
            "status": "local_operator_policy_record_not_access_grant",
            "record_status": self.record_status,
            "revision": self.revision,
            "head_sha256": self.head_sha256,
            "checked_on": self.checked_on.isoformat(),
            "external_freshness_status": "not_verified",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _canonical_event_message(event: SignedOperatorPolicyEvent) -> bytes:
    """Domain-separated signable fields; signatures not included."""
    data = {
        "domain": _DOMAIN,
        "action": event.action,
        "operator_key_id": event.operator_key_id,
        "operator_public_key_hex": event.operator_public_key_hex,
        "sequence": event.sequence,
        "previous_head_sha256": event.previous_head_sha256,
        "issued_on": event.issued_on.isoformat(),
        "expires_on": event.expires_on.isoformat() if event.expires_on else None,
        "admin_key_ids": list(event.admin_key_ids),
    }
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _validate_event(event: SignedOperatorPolicyEvent) -> None:
    if type(event) is not SignedOperatorPolicyEvent:
        raise ValueError("invalid signed operator policy event")
    if (
        type(event.action) is not str or event.action not in ("enroll", "revoke")
        or type(event.operator_key_id) is not str
        or _NAME.fullmatch(event.operator_key_id) is None
        or type(event.operator_public_key_hex) is not str
        or _KEY_BYTES.fullmatch(event.operator_public_key_hex) is None
        or type(event.sequence) is not int or not 1 <= event.sequence <= _MAX_EVENTS
        or type(event.previous_head_sha256) is not str
        or _SHA.fullmatch(event.previous_head_sha256) is None
        or type(event.issued_on) is not date
        or type(event.admin_key_ids) is not tuple
        or len(event.admin_key_ids) != 2
        or event.admin_key_ids[0] == event.admin_key_ids[1]
        or any(type(key) is not str or _NAME.fullmatch(key) is None
               for key in event.admin_key_ids)
        or type(event.first_signature_hex) is not str
        or _SIGNATURE.fullmatch(event.first_signature_hex) is None
        or type(event.second_signature_hex) is not str
        or _SIGNATURE.fullmatch(event.second_signature_hex) is None
    ):
        raise ValueError("invalid operator policy identity, event or signatures")
    if event.action == "enroll":
        if (
            type(event.expires_on) is not date
            or not event.issued_on < event.expires_on
            or event.expires_on > event.issued_on + timedelta(days=365)
        ):
            raise ValueError("enrollment requires bounded future expiration")
    elif event.expires_on is not None:
        raise ValueError("revocation cannot have an expiration")


def _serialize(event: SignedOperatorPolicyEvent) -> str:
    _validate_event(event)
    data = asdict(event)
    data["issued_on"] = event.issued_on.isoformat()
    data["expires_on"] = event.expires_on.isoformat() if event.expires_on else None
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _decode(raw: str) -> SignedOperatorPolicyEvent:
    """No dynamic deserialization; reject noncanonical and huge records."""
    if type(raw) is not str or len(raw) > 4096:
        raise ValueError("stored operator event is malformed")
    try:
        fields = json.loads(raw)
        fields["issued_on"] = date.fromisoformat(fields["issued_on"])
        if fields["expires_on"] is not None:
            fields["expires_on"] = date.fromisoformat(fields["expires_on"])
        fields["admin_key_ids"] = tuple(fields["admin_key_ids"])
        event = SignedOperatorPolicyEvent(**fields)
        if _serialize(event) != raw:
            raise ValueError
        return event
    except (TypeError, ValueError, KeyError, OverflowError):
        raise ValueError("stored operator event is malformed") from None


def _verify_admin_signature(public: bytes, signature: str, message: bytes) -> None:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ImportError:
        raise RuntimeError("operator policy verification requires review extra") from None
    try:
        Ed25519PublicKey.from_public_bytes(public).verify(
            bytes.fromhex(signature), message
        )
    except (InvalidSignature, ValueError):
        raise ValueError("operator administrator signature invalid") from None


class LocalOperatorGovernance:
    """Single-local-database CAS of dual-admin signed key policy events.

    This is metadata-only. It is NOT integrated into publisher admission
    because a separate read followed by a write in another SQLite
    database cannot be made atomic with these two independent files.
    """

    def __init__(
        self,
        path: Path,
        *,
        administrator_public_keys: Mapping[str, bytes],
        create: bool = False,
    ) -> None:
        if (
            not isinstance(path, Path) or not path.is_absolute()
            or not path.parent.is_dir() or path.is_symlink()
        ):
            raise ValueError("governance requires explicit safe absolute database path")
        if (
            not isinstance(administrator_public_keys, Mapping)
            or not 2 <= len(administrator_public_keys) <= _MAX_ADMINS
        ):
            raise ValueError("two or more configured administrator keys required")
        keys = dict(administrator_public_keys)
        if any(
            type(key) is not str or _NAME.fullmatch(key) is None
            or type(pub) is not bytes or len(pub) != 32
            for key, pub in keys.items()
        ) or len(set(keys.values())) != len(keys):
            raise ValueError("administrator key roster must be distinct and valid")
        if type(create) is not bool:
            raise ValueError("create flag must be boolean")
        self._path = path
        self._admins = keys
        self._roster_sha256 = sha256(json.dumps(
            {name: pub.hex() for name, pub in sorted(keys.items())},
            sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        if create:
            if path.exists():
                raise ValueError("refusing to replace existing governance registry")
            connection = sqlite3.connect(str(path), timeout=5, isolation_level=None)
            try:
                connection.execute("PRAGMA synchronous = FULL")
                connection.execute("BEGIN IMMEDIATE")
                connection.execute(
                    "CREATE TABLE governance_schema (version INTEGER NOT NULL,"
                    "admin_roster_sha256 TEXT NOT NULL)"
                )
                connection.execute(
                    "INSERT INTO governance_schema VALUES (?,?)",
                    (_VERSION, self._roster_sha256),
                )
                connection.execute(
                    "CREATE TABLE governance_head ("
                    "id INTEGER PRIMARY KEY CHECK(id=1),"
                    "revision INTEGER NOT NULL,head_sha256 TEXT NOT NULL)"
                )
                connection.execute(
                    "INSERT INTO governance_head VALUES (1,0,?)",
                    (GENESIS_POLICY_HEAD,),
                )
                connection.execute(
                    "CREATE TABLE governance_events ("
                    "sequence INTEGER PRIMARY KEY,event_json TEXT NOT NULL)"
                )
                connection.execute("COMMIT")
            except sqlite3.DatabaseError:
                connection.rollback()
                raise ValueError("governance schema initialization failed") from None
            finally:
                connection.close()
        if not path.is_file():
            raise ValueError("governance database does not exist")
        connection = self._connect()
        try:
            self._check_schema(connection)
        finally:
            connection.close()

    def _connect(self) -> sqlite3.Connection:
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("governance database missing or unsafe")
        try:
            connection = sqlite3.connect(
                str(self._path), timeout=5, isolation_level=None
            )
            connection.execute("PRAGMA synchronous = FULL")
            connection.execute("PRAGMA busy_timeout = 5000")
            return connection
        except sqlite3.DatabaseError:
            raise ValueError("cannot open operator governance database") from None

    def _check_schema(self, connection: sqlite3.Connection) -> None:
        try:
            rows = connection.execute(
                "SELECT version,admin_roster_sha256 FROM governance_schema"
            ).fetchall()
            if rows != [(_VERSION, self._roster_sha256)]:
                raise ValueError("governance schema or administrator roster mismatch")
            head = connection.execute(
                "SELECT revision,head_sha256 FROM governance_head WHERE id=1"
            ).fetchall()
            if len(head) != 1:
                raise ValueError("missing governance policy head")
            connection.execute("SELECT COUNT(*) FROM governance_events").fetchone()
        except sqlite3.DatabaseError:
            raise ValueError("invalid governance database schema") from None

    def _read(
        self, connection: sqlite3.Connection
    ) -> tuple[int, str, dict[str, tuple[str, date, bool]], date | None]:
        revision, stored_head = connection.execute(
            "SELECT revision,head_sha256 FROM governance_head WHERE id=1"
        ).fetchone()
        if (
            type(revision) is not int or not 0 <= revision <= _MAX_EVENTS
            or type(stored_head) is not str or _SHA.fullmatch(stored_head) is None
        ):
            raise ValueError("governance stored head is invalid")
        rows = connection.execute(
            "SELECT sequence,event_json FROM governance_events ORDER BY sequence"
        ).fetchall()
        if len(rows) != revision or [num for num, _ in rows] != list(
            range(1, revision + 1)
        ):
            raise ValueError("governance history contains gaps")
        history: dict[str, tuple[str, date, bool]] = {}
        all_material: set[str] = set()
        head = GENESIS_POLICY_HEAD
        last_date: date | None = None
        for seq, encoded in rows:
            event = _decode(encoded)
            head, last_date = self._evaluate(
                event, expected_sequence=seq,
                previous_head=head, previous_date=last_date,
                history=history, used_material=all_material,
            )
        if not compare_digest(head, stored_head):
            raise ValueError("governance signed head mismatch")
        return revision, head, history, last_date

    def _evaluate(
        self,
        event: SignedOperatorPolicyEvent,
        *,
        expected_sequence: int,
        previous_head: str,
        previous_date: date | None,
        history: dict[str, tuple[str, date, bool]],
        used_material: set[str],
    ) -> tuple[str, date]:
        _validate_event(event)
        if (
            event.sequence != expected_sequence
            or not compare_digest(event.previous_head_sha256, previous_head)
            or previous_date is not None and event.issued_on < previous_date
        ):
            raise ValueError("operator policy has stale sequence, head or date")
        if (
            any(admin_id not in self._admins for admin_id in event.admin_key_ids)
            or event.operator_key_id in self._admins
            or event.operator_public_key_hex in {
                pub.hex() for pub in self._admins.values()
            }
        ):
            raise ValueError("operator governance roles or signing keys overlap")
        message = _canonical_event_message(event)
        _verify_admin_signature(
            self._admins[event.admin_key_ids[0]], event.first_signature_hex, message
        )
        _verify_admin_signature(
            self._admins[event.admin_key_ids[1]], event.second_signature_hex, message
        )
        if event.action == "enroll":
            if (
                event.operator_key_id in history
                or event.operator_public_key_hex in used_material
                or len(history) >= _MAX_OPERATORS
            ):
                raise ValueError("operator key ID/material already used or budget exhausted")
            expires_on = event.expires_on
            assert type(expires_on) is date  # validated by _validate_event
            history[event.operator_key_id] = (
                event.operator_public_key_hex, expires_on, False
            )
            used_material.add(event.operator_public_key_hex)
        else:
            original = history.get(event.operator_key_id)
            if (
                original is None
                or original[2] is True
                or not compare_digest(original[0], event.operator_public_key_hex)
            ):
                raise ValueError("revocation must match a previously active key")
            history[event.operator_key_id] = (original[0], original[1], True)
        digest = sha256(
            message + bytes.fromhex(event.first_signature_hex)
            + bytes.fromhex(event.second_signature_hex)
        ).hexdigest()
        return digest, event.issued_on

    @staticmethod
    def _check_external_head(head: str, expected: str | None) -> None:
        if expected is not None and (
            type(expected) is not str
            or _SHA.fullmatch(expected) is None
            or not compare_digest(head, expected)
        ):
            raise ValueError("governance head differs from independently expected head")

    def snapshot(
        self, *, checked_on: date,
        externally_expected_head_sha256: str | None = None,
    ) -> OperatorPolicyRevision:
        if type(checked_on) is not date:
            raise ValueError("governance check date must be a calendar date")
        db = self._connect()
        try:
            db.execute("BEGIN")
            self._check_schema(db)
            revision, head, history, latest = self._read(db)
            if latest is not None and checked_on < latest:
                raise ValueError("cannot assess history before latest governance event")
            self._check_external_head(head, externally_expected_head_sha256)
            db.execute("COMMIT")
            return OperatorPolicyRevision(
                revision=revision, head_sha256=head,
                registered_count=len(history), checked_on=checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("governance snapshot database error") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def assess_operator(
        self, operator_key_id: str, operator_public_key: bytes, *,
        checked_on: date, externally_expected_head_sha256: str | None = None,
    ) -> OperatorPolicyAssessment:
        if (
            type(operator_key_id) is not str
            or _NAME.fullmatch(operator_key_id) is None
            or type(operator_public_key) is not bytes
            or len(operator_public_key) != 32
            or type(checked_on) is not date
        ):
            raise ValueError("invalid operator record query")
        db = self._connect()
        try:
            db.execute("BEGIN")
            self._check_schema(db)
            revision, head, history, latest = self._read(db)
            if latest is not None and checked_on < latest:
                raise ValueError("cannot assess history before latest governance event")
            self._check_external_head(head, externally_expected_head_sha256)
            record = history.get(operator_key_id)
            if record is None:
                status = "unknown_operator_record"
            elif not compare_digest(record[0], operator_public_key.hex()):
                status = "key_material_mismatch"
            elif record[2]:
                status = "revoked_operator_record"
            elif checked_on > record[1]:
                status = "expired_operator_record"
            else:
                status = "locally_registered_not_authorized"
            db.execute("COMMIT")
            return OperatorPolicyAssessment(
                record_status=status, revision=revision,
                head_sha256=head, checked_on=checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("governance assessment database error") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def append(
        self, event: SignedOperatorPolicyEvent, *,
        expected_revision: int, expected_head_sha256: str,
        checked_on: date,
    ) -> OperatorPolicyRevision:
        if type(checked_on) is not date:
            raise ValueError("governance write date must be a calendar date")
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            self._check_schema(db)
            revision, head, history, last_date = self._read(db)
            if (
                type(expected_revision) is not int
                or expected_revision != revision
                or type(expected_head_sha256) is not str
                or _SHA.fullmatch(expected_head_sha256) is None
                or not compare_digest(expected_head_sha256, head)
            ):
                raise ValueError("stale governance revision or head")
            if revision >= _MAX_EVENTS:
                raise ValueError("governance event budget exceeded")
            if type(event) is not SignedOperatorPolicyEvent:
                raise ValueError("invalid signed operator policy event")
            if event.issued_on > checked_on:
                raise ValueError("governance cannot publish a future-issued event")
            material = {record[0] for record in history.values()}
            new_head, _ = self._evaluate(
                event, expected_sequence=revision + 1,
                previous_head=head, previous_date=last_date,
                history=history, used_material=material,
            )
            db.execute(
                "INSERT INTO governance_events(sequence,event_json) VALUES (?,?)",
                (revision + 1, _serialize(event)),
            )
            db.execute(
                "UPDATE governance_head SET revision=?,head_sha256=? WHERE id=1",
                (revision + 1, new_head),
            )
            db.execute("COMMIT")
            return OperatorPolicyRevision(
                revision=revision + 1, head_sha256=new_head,
                registered_count=len(history), checked_on=checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("governance transaction failed without commit") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()
