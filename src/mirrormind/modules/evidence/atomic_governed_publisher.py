"""Experimental single-SQLite transaction for operator policy and publication.

One local BEGIN IMMEDIATE covers the *current* dual-admin policy check and
a signed checkpoint publication. This is NOT a real identity authority,
externally attested current head, legal data-use grant or production service.
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path

from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.local_checkpoint_publisher import (
    _MAX_EVENTS as MAX_PUBLICATIONS,
)
from mirrormind.modules.evidence.local_checkpoint_publisher import (
    _MAX_PACKETS as MAX_PUBLICATION_PACKETS,
)
from mirrormind.modules.evidence.local_checkpoint_publisher import (
    GENESIS_PUBLICATION_HEAD,
    LocalCheckpointPublisher,
    SignedPublicationCommand,
    _packet_json,
    _serialize,
)
from mirrormind.modules.evidence.operator_governance import (
    _MAX_ADMINS,
    _NAME,
    GENESIS_POLICY_HEAD,
    LocalOperatorGovernance,
    OperatorPolicyRevision,
    SignedOperatorPolicyEvent,
)
from mirrormind.modules.evidence.operator_governance import (
    _MAX_EVENTS as MAX_POLICY_EVENTS,
)
from mirrormind.modules.evidence.operator_governance import (
    _serialize as serialize_policy,
)

_VERSION = 1
_HEX_SHA = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class AtomicGovernedRevision:
    """One local snapshot; does not represent source or production authorization."""

    policy_revision: int
    policy_head_sha256: str
    publication_sequence: int
    publication_head_sha256: str
    review_revision: int
    checked_on: date

    def receipt(self) -> dict[str, str | int | bool]:
        """Only safe local consistency fields; never an access-control token."""
        return {
            "status": "single_database_policy_publication_not_external_authority",
            "policy_revision": self.policy_revision,
            "policy_head_sha256": self.policy_head_sha256,
            "publication_sequence": self.publication_sequence,
            "publication_head_sha256": self.publication_head_sha256,
            "review_revision": self.review_revision,
            "checked_on": self.checked_on.isoformat(),
            "atomicity_status": "one_local_sqlite_begin_immediate_transaction",
            "external_freshness_status": "not_independently_attested",
            "operator_identity_status": "signed_keys_only_no_real_identity",
            "publication_authorized": False,
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


class _HistoricalSignatureVerifier(LocalCheckpointPublisher):
    """Reuse tested signature/history helpers without enabling direct publishing."""

    def __init__(
        self, checkpoint_keys: Mapping[str, bytes],
        witness_keys: Mapping[str, bytes],
        operator_keys: Mapping[str, bytes],
        bootstrap: str,
    ) -> None:
        # Never opens/creates a database: the integrated gate owns the one
        # transaction and the dynamically reconstructed operator key history.
        self._checkpoints = dict(checkpoint_keys)
        self._witnesses = dict(witness_keys)
        self._operators = dict(operator_keys)
        self._bootstrap = bootstrap

    def publish(self, *args: object, **kwargs: object) -> None:
        raise ValueError("integrated verifier cannot publish outside policy transaction")


class AtomicGovernedPublisher:
    """Opt-in local shared schema with serial policy updates and publication.

    No cross-host locking or independent authority. Only this class's publish
    method checks current operator status and writes under the SAME SQLite
    transaction as its policy read. Old standalone publisher refuses this DB.
    """

    def __init__(
        self,
        path: Path,
        *,
        administrator_public_keys: Mapping[str, bytes],
        checkpoint_keys: Mapping[str, bytes],
        witness_keys: Mapping[str, bytes],
        initial_witness_key_id: str,
        create: bool = False,
    ) -> None:
        if (
            not isinstance(path, Path) or not path.is_absolute()
            or not path.parent.is_dir() or path.is_symlink()
        ):
            raise ValueError("integrated gate requires a safe absolute database path")
        if (
            not isinstance(administrator_public_keys, Mapping)
            or not 2 <= len(administrator_public_keys) <= _MAX_ADMINS
        ):
            raise ValueError("at least two administrator keys required")
        admins = dict(administrator_public_keys)
        checkpoints = dict(checkpoint_keys)
        witnesses = dict(witness_keys)
        for roster in (admins, checkpoints, witnesses):
            if not roster or any(
                type(key_id) is not str or _NAME.fullmatch(key_id) is None
                or type(public) is not bytes or len(public) != 32
                for key_id, public in roster.items()
            ) or len(set(roster.values())) != len(roster):
                raise ValueError("invalid signing role roster or duplicate key")
        all_keys = [*admins.values(), *checkpoints.values(), *witnesses.values()]
        if (
            len(set(admins) | set(checkpoints) | set(witnesses))
            != len(admins) + len(checkpoints) + len(witnesses)
            or len(set(all_keys)) != len(all_keys)
        ):
            raise ValueError("integrated signing roles must use distinct keys")
        if type(initial_witness_key_id) is not str or initial_witness_key_id not in witnesses:
            raise ValueError("unrecognized bootstrap witness key")
        if type(create) is not bool:
            raise ValueError("create must be a boolean")
        self._path = path
        self._admins = admins
        self._checkpoints = checkpoints
        self._witnesses = witnesses
        self._bootstrap = initial_witness_key_id
        canonical = json.dumps(
            {
                "admins": {k: v.hex() for k, v in sorted(admins.items())},
                "checkpoints": {k: v.hex() for k, v in sorted(checkpoints.items())},
                "witnesses": {k: v.hex() for k, v in sorted(witnesses.items())},
                "bootstrap": initial_witness_key_id,
            },
            sort_keys=True, separators=(",", ":"),
        )
        self._configured_roster_sha256 = sha256(canonical.encode("utf-8")).hexdigest()
        admin_roster = sha256(json.dumps(
            {k: v.hex() for k, v in sorted(admins.items())},
            sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")).hexdigest()
        if create:
            if path.exists():
                raise ValueError("refusing to overwrite existing integrated gate")
            db = sqlite3.connect(str(path), isolation_level=None, timeout=5)
            try:
                db.execute("PRAGMA foreign_keys = ON")
                db.execute("PRAGMA synchronous = FULL")
                db.execute("BEGIN IMMEDIATE")
                db.execute(
                    "CREATE TABLE atomic_governed_schema("
                    "version INTEGER NOT NULL,roster_sha256 TEXT NOT NULL)"
                )
                db.execute(
                    "INSERT INTO atomic_governed_schema VALUES (?,?)",
                    (_VERSION, self._configured_roster_sha256),
                )
                db.execute(
                    "CREATE TABLE governance_schema("
                    "version INTEGER NOT NULL,admin_roster_sha256 TEXT NOT NULL)"
                )
                db.execute(
                    "INSERT INTO governance_schema VALUES (?,?)",
                    (_VERSION, admin_roster),
                )
                db.execute(
                    "CREATE TABLE governance_head("
                    "id INTEGER PRIMARY KEY CHECK(id=1),"
                    "revision INTEGER NOT NULL,head_sha256 TEXT NOT NULL)"
                )
                db.execute(
                    "INSERT INTO governance_head VALUES (1,0,?)",
                    (GENESIS_POLICY_HEAD,),
                )
                db.execute(
                    "CREATE TABLE governance_events("
                    "sequence INTEGER PRIMARY KEY,event_json TEXT NOT NULL)"
                )
                db.execute(
                    "CREATE TABLE publication_schema("
                    "version INTEGER NOT NULL,initial_witness_key_id TEXT NOT NULL)"
                )
                db.execute(
                    "INSERT INTO publication_schema VALUES (?,?)",
                    (_VERSION, initial_witness_key_id),
                )
                db.execute(
                    "CREATE TABLE publication_heads("
                    "packet_sha256 TEXT PRIMARY KEY,packet_json TEXT NOT NULL,"
                    "sequence INTEGER NOT NULL,receipt_sha256 TEXT NOT NULL)"
                )
                db.execute(
                    "CREATE TABLE publication_events("
                    "packet_sha256 TEXT NOT NULL,sequence INTEGER NOT NULL,"
                    "command_json TEXT NOT NULL,"
                    "PRIMARY KEY(packet_sha256,sequence),"
                    "FOREIGN KEY(packet_sha256) REFERENCES publication_heads(packet_sha256))"
                )
                db.execute("COMMIT")
            except sqlite3.DatabaseError:
                db.rollback()
                raise ValueError("atomic gate initialization failed") from None
            finally:
                db.close()
        if not path.is_file():
            raise ValueError("integrated gate database does not exist")
        # This existing class is only used for its validated policy-event
        # replay and signature checks; the integrated class owns ALL writes.
        self._policy = LocalOperatorGovernance(
            path, administrator_public_keys=admins, create=False,
        )
        db = self._connect()
        try:
            self._schema(db)
        finally:
            db.close()

    def _connect(self) -> sqlite3.Connection:
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("integrated gate database missing or unsafe")
        try:
            db = sqlite3.connect(str(self._path), timeout=5, isolation_level=None)
            db.execute("PRAGMA foreign_keys = ON")
            db.execute("PRAGMA busy_timeout = 5000")
            db.execute("PRAGMA synchronous = FULL")
            return db
        except sqlite3.DatabaseError:
            raise ValueError("integrated gate database unavailable") from None

    def _schema(self, db: sqlite3.Connection) -> None:
        try:
            if db.execute(
                "SELECT version,roster_sha256 FROM atomic_governed_schema"
            ).fetchall() != [(_VERSION, self._configured_roster_sha256)]:
                raise ValueError("integrated gate schema or signing roster mismatch")
            self._policy._check_schema(db)
            if db.execute(
                "SELECT version,initial_witness_key_id FROM publication_schema"
            ).fetchall() != [(_VERSION, self._bootstrap)]:
                raise ValueError("integrated publication schema or bootstrap mismatch")
            for table in ("publication_heads", "publication_events"):
                db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        except sqlite3.DatabaseError:
            raise ValueError("invalid integrated gate schema") from None

    def _read_policy(
        self, db: sqlite3.Connection, checked_on: date,
    ) -> tuple[int, str, dict[str, tuple[str, date, bool]]]:
        if type(checked_on) is not date:
            raise ValueError("integrated check date must be a calendar date")
        revision, head, records, last_date = self._policy._read(db)
        if last_date is not None and checked_on < last_date:
            raise ValueError("cannot read governance before latest signed policy event")
        self._check_policy_role_separation(records)
        return revision, head, records

    def _check_policy_role_separation(
        self, records: Mapping[str, tuple[str, date, bool]],
    ) -> None:
        reserved_ids = set(self._admins) | set(self._checkpoints) | set(self._witnesses)
        reserved_keys = {
            public.hex()
            for public in (*self._admins.values(), *self._checkpoints.values(),
                           *self._witnesses.values())
        }
        if any(key_id in reserved_ids or record[0] in reserved_keys
               for key_id, record in records.items()):
            raise ValueError("operator key conflicts with another signing role")

    def _verifier(
        self, records: Mapping[str, tuple[str, date, bool]],
    ) -> _HistoricalSignatureVerifier:
        # All historically enrolled keys are necessary to reverify old
        # signatures after revocation; only current active keys may publish.
        return _HistoricalSignatureVerifier(
            self._checkpoints, self._witnesses,
            {key_id: bytes.fromhex(record[0]) for key_id, record in records.items()},
            self._bootstrap,
        )

    @staticmethod
    def _expected(expected: int, head: str, current: int, current_head: str) -> None:
        if (
            type(expected) is not int or expected != current
            or type(head) is not str or _HEX_SHA.fullmatch(head) is None
            or not compare_digest(head, current_head)
        ):
            raise ValueError("stale expected policy/publication revision or head")

    def append_policy(
        self, event: SignedOperatorPolicyEvent, *,
        expected_policy_revision: int,
        expected_policy_head_sha256: str,
        checked_on: date,
    ) -> OperatorPolicyRevision:
        """Atomically advance the same-file policy read by future publications."""
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            self._schema(db)
            revision, head, records = self._read_policy(db, checked_on)
            self._expected(
                expected_policy_revision, expected_policy_head_sha256,
                revision, head,
            )
            if revision >= MAX_POLICY_EVENTS:
                raise ValueError("governance event budget exceeded")
            if type(event) is not SignedOperatorPolicyEvent:
                raise ValueError("invalid signed governance event")
            if type(event.issued_on) is not date or event.issued_on > checked_on:
                raise ValueError("future or invalid governance event date")
            copy = dict(records)
            new_head, _ = self._policy._evaluate(
                event, expected_sequence=revision + 1,
                previous_head=head, previous_date=(
                    None if revision == 0 else _last_governance_date(db, revision)
                ),
                history=copy,
                used_material={record[0] for record in records.values()},
            )
            self._check_policy_role_separation(copy)
            db.execute(
                "INSERT INTO governance_events(sequence,event_json) VALUES(?,?)",
                (revision + 1, serialize_policy(event)),
            )
            db.execute(
                "UPDATE governance_head SET revision=?,head_sha256=? WHERE id=1",
                (revision + 1, new_head),
            )
            db.execute("COMMIT")
            return OperatorPolicyRevision(
                revision=revision + 1, head_sha256=new_head,
                registered_count=len(copy), checked_on=checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("integrated policy transaction failed without commit") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def snapshot(
        self, packet: SourceReviewPacket, *, checked_on: date,
        externally_expected_policy_head_sha256: str | None = None,
        externally_expected_publication_head_sha256: str | None = None,
    ) -> AtomicGovernedRevision:
        """Reverify *both* local signed histories in the same read snapshot."""
        if type(packet) is not SourceReviewPacket or type(checked_on) is not date:
            raise ValueError("invalid integrated packet or check date")
        if checked_on < packet.inspected_on:
            raise ValueError("cannot check before packet inspection")
        db = self._connect()
        try:
            db.execute("BEGIN")
            self._schema(db)
            policy_revision, policy_head, records = self._read_policy(db, checked_on)
            pub_seq, pub_head, _, _, review_revision, _, _, _ = self._verifier(
                records
            )._load(db, packet)
            for actual, expected in (
                (policy_head, externally_expected_policy_head_sha256),
                (pub_head, externally_expected_publication_head_sha256),
            ):
                if expected is not None and (
                    type(expected) is not str or _HEX_SHA.fullmatch(expected) is None
                    or not compare_digest(actual, expected)
                ):
                    raise ValueError("integrated head differs from external reference")
            db.execute("COMMIT")
            return AtomicGovernedRevision(
                policy_revision, policy_head, pub_seq, pub_head, review_revision,
                checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("integrated snapshot database error") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def publish(
        self, packet: SourceReviewPacket, command: SignedPublicationCommand, *,
        expected_policy_revision: int, expected_policy_head_sha256: str,
        expected_publication_sequence: int,
        expected_publication_head_sha256: str,
        checked_on: date,
    ) -> AtomicGovernedRevision:
        """Reject revoked/expired keys and append under ONE SQLite write lock."""
        if type(packet) is not SourceReviewPacket or type(checked_on) is not date:
            raise ValueError("invalid integrated publication or check date")
        if checked_on < packet.inspected_on:
            raise ValueError("cannot publish before packet inspection")
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            self._schema(db)
            policy_revision, policy_head, records = self._read_policy(db, checked_on)
            self._expected(
                expected_policy_revision, expected_policy_head_sha256,
                policy_revision, policy_head,
            )
            if type(command) is not SignedPublicationCommand:
                raise ValueError("invalid signed publication command")
            if type(command.operator_key_id) is not str:
                raise ValueError("invalid publishing operator identifier")
            operator = records.get(command.operator_key_id)
            if operator is None:
                raise ValueError("publishing operator is not enrolled")
            if operator[2]:
                raise ValueError("publishing operator has been revoked")
            if checked_on > operator[1]:
                raise ValueError("publishing operator registration has expired")
            # The expected policy state is not merely a caller-supplied CAS:
            # the operator must sign the exact policy epoch and head itself.
            # Legacy v1 commands remain readable as history, never new writes.
            if (
                type(command.expected_policy_revision) is not int
                or command.expected_policy_revision != policy_revision
                or type(command.expected_policy_head_sha256) is not str
                or not compare_digest(command.expected_policy_head_sha256, policy_head)
            ):
                raise ValueError("operator signature must bind current policy head")
            verifier = self._verifier(records)
            (
                pub_seq, pub_head, witness, epoch, review_rev,
                review_head, issued_on, _,
            ) = verifier._load(db, packet)
            self._expected(
                expected_publication_sequence, expected_publication_head_sha256,
                pub_seq, pub_head,
            )
            if pub_seq >= MAX_PUBLICATIONS:
                raise ValueError("publication event budget exceeded")
            serialized = _serialize(command)
            (
                next_head, _, _, next_review_revision, _, new_issue,
            ) = verifier._verify_event(
                packet, command, sequence=pub_seq, previous_hash=pub_head,
                previous_witness=witness, previous_epoch=epoch,
                previous_revision=review_rev, previous_review_head=review_head,
                previous_issue=issued_on,
            )
            if new_issue > checked_on:
                raise ValueError("future checkpoint cannot be published")
            if checked_on > command.receipt.checkpoint.expires_on:
                raise ValueError("expired checkpoint cannot be published")
            if pub_seq == 0:
                if db.execute(
                    "SELECT COUNT(*) FROM publication_heads"
                ).fetchone()[0] >= MAX_PUBLICATION_PACKETS:
                    raise ValueError("publication packet budget exceeded")
                db.execute(
                    "INSERT INTO publication_heads VALUES(?,?,?,?)",
                    (packet.declaration_sha256, _packet_json(packet),
                     0, GENESIS_PUBLICATION_HEAD),
                )
            db.execute(
                "INSERT INTO publication_events VALUES(?,?,?)",
                (packet.declaration_sha256, pub_seq + 1, serialized),
            )
            db.execute(
                "UPDATE publication_heads SET sequence=?,receipt_sha256=? "
                "WHERE packet_sha256=?",
                (pub_seq + 1, next_head, packet.declaration_sha256),
            )
            db.execute("COMMIT")
            return AtomicGovernedRevision(
                policy_revision, policy_head, pub_seq + 1, next_head,
                next_review_revision, checked_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("integrated publication transaction failed without commit") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()


def _last_governance_date(db: sqlite3.Connection, revision: int) -> date:
    """Read only the exact preceding canonical signed event's calendar date."""
    from mirrormind.modules.evidence.operator_governance import _decode
    row = db.execute(
        "SELECT event_json FROM governance_events WHERE sequence=?", (revision,)
    ).fetchone()
    if row is None:
        raise ValueError("integrated governance history is incomplete")
    return _decode(row[0]).issued_on
