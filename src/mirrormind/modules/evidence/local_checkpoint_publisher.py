"""Transactional *local* signer-gated publication ledger, not a live authority.

All receipts forbid data ingestion. This stores a separately signed receipt
history; public keys, role policy, time, database and currentness are supplied
by its operator and are NOT independently trusted by this component.
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

from mirrormind.modules.evidence.authority_transcript import (
    SignedAuthorityReceipt,
    WitnessKeyHandoff,
    _canonical_authority_receipt_message,
    _canonical_handoff_message,
    _keys_valid,
    _verify_signature,
)
from mirrormind.modules.evidence.head_checkpoints import (
    SignedReviewHeadCheckpoint,
    verify_signed_head_checkpoint,
)
from mirrormind.modules.evidence.intake_review import SourceReviewPacket

GENESIS_PUBLICATION_HEAD = "0" * 64
_MAX_PACKETS = 16
_MAX_EVENTS = 32
_MAX_SEQUENCE = 1_000_000_000
_SCHEMA = 1
_SHA = re.compile(r"[0-9a-f]{64}")
_SIG = re.compile(r"[0-9a-f]{128}")
_PUBLISH_DOMAIN = "mirrormind.local-checkpoint-publication.v1"
_GOVERNED_PUBLISH_DOMAIN = "mirrormind.atomic-governed-publication.v2"


@dataclass(frozen=True, slots=True)
class SignedPublicationCommand:
    """Operator authorization of a single exact proposed witness receipt."""

    receipt: SignedAuthorityReceipt
    handoff: WitnessKeyHandoff | None
    operator_key_id: str
    expected_sequence: int
    expected_receipt_sha256: str
    operator_signature_hex: str
    # Optional for historical standalone records. Mandatory for new governed writes.
    expected_policy_revision: int | None = None
    expected_policy_head_sha256: str | None = None


@dataclass(frozen=True, slots=True)
class LocalPublicationRevision:
    """Sanitized local state, NOT an externally witnessed current head."""

    sequence: int
    receipt_sha256: str
    checkpoint_review_revision: int
    checked_on: date
    checkpoint_expired: bool

    def receipt(self) -> dict[str, str | int | bool]:
        return {
            "status": "local_operator_signed_publication_not_external_authority",
            "sequence": self.sequence,
            "receipt_sha256": self.receipt_sha256,
            "checkpoint_review_revision": self.checkpoint_review_revision,
            "checked_on": self.checked_on.isoformat(),
            "checkpoint_expired": self.checkpoint_expired,
            "freshness_status": "local_database_not_independently_attested",
            "operator_status": "supplied_public_key_role_only_not_real_identity",
            "ingestion_authorized": False,
            "forecast_eligible": False,
        }


def _receipt_digest(receipt: SignedAuthorityReceipt) -> str:
    """Exactly the existing witness-transcript receipt hashing convention."""
    return sha256(
        _canonical_authority_receipt_message(receipt)
        + bytes.fromhex(receipt.witness_signature_hex)
    ).hexdigest()


def _canonical_publication_message(command: SignedPublicationCommand) -> bytes:
    """Distinct operator signing domain, binding witness and handoff signatures."""
    handoff_digest = None
    if command.handoff is not None:
        handoff_digest = sha256(
            _canonical_handoff_message(command.handoff)
            + bytes.fromhex(command.handoff.old_signature_hex)
            + bytes.fromhex(command.handoff.new_signature_hex)
        ).hexdigest()
    governed = command.expected_policy_revision is not None
    record = {
        "domain": _GOVERNED_PUBLISH_DOMAIN if governed else _PUBLISH_DOMAIN,
        "receipt_sha256": _receipt_digest(command.receipt),
        "handoff_sha256": handoff_digest,
        "operator_key_id": command.operator_key_id,
        "expected_sequence": command.expected_sequence,
        "expected_receipt_sha256": command.expected_receipt_sha256,
    }
    if governed:
        record["expected_policy_revision"] = command.expected_policy_revision
        record["expected_policy_head_sha256"] = command.expected_policy_head_sha256
    return json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _serialize(command: SignedPublicationCommand) -> str:
    if type(command) is not SignedPublicationCommand:
        raise ValueError("invalid local publication command")
    if type(command.receipt) is not SignedAuthorityReceipt:
        raise ValueError("invalid signed witness receipt")
    checkpoint = command.receipt.checkpoint
    if type(checkpoint) is not SignedReviewHeadCheckpoint:
        raise ValueError("invalid signed review checkpoint")
    if command.handoff is not None and type(command.handoff) is not WitnessKeyHandoff:
        raise ValueError("invalid witness handoff")
    if (type(command.receipt.witness_signature_hex) is not str
            or _SIG.fullmatch(command.receipt.witness_signature_hex) is None
            or type(checkpoint.signature_hex) is not str
            or _SIG.fullmatch(checkpoint.signature_hex) is None
            or type(command.operator_signature_hex) is not str
            or _SIG.fullmatch(command.operator_signature_hex) is None):
        raise ValueError("invalid publication signature encoding")
    if (type(checkpoint.issued_on) is not date
            or type(checkpoint.expires_on) is not date):
        raise ValueError("invalid publication checkpoint date")
    if command.handoff is not None and (
        type(command.handoff.old_signature_hex) is not str
        or _SIG.fullmatch(command.handoff.old_signature_hex) is None
        or type(command.handoff.new_signature_hex) is not str
        or _SIG.fullmatch(command.handoff.new_signature_hex) is None
    ):
        raise ValueError("invalid witness rotation signature encoding")
    has_revision = command.expected_policy_revision is not None
    has_head = command.expected_policy_head_sha256 is not None
    if has_revision != has_head:
        raise ValueError("publication policy binding must be complete")
    if has_revision and (
        type(command.expected_policy_revision) is not int
        or not 0 <= command.expected_policy_revision <= _MAX_SEQUENCE
        or type(command.expected_policy_head_sha256) is not str
        or _SHA.fullmatch(command.expected_policy_head_sha256) is None
    ):
        raise ValueError("invalid publication policy binding")
    data = asdict(command)
    if not has_revision:
        # Retain byte-for-byte canonical encoding of existing v1 records.
        data.pop("expected_policy_revision")
        data.pop("expected_policy_head_sha256")
    data["receipt"]["checkpoint"]["issued_on"] = checkpoint.issued_on.isoformat()
    data["receipt"]["checkpoint"]["expires_on"] = checkpoint.expires_on.isoformat()
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _decode(data: str) -> SignedPublicationCommand:
    """Decode only exact canonical records; never execute or deserialize objects."""
    try:
        fields = json.loads(data)
        checkpoint = fields["receipt"]["checkpoint"]
        checkpoint["issued_on"] = date.fromisoformat(checkpoint["issued_on"])
        checkpoint["expires_on"] = date.fromisoformat(checkpoint["expires_on"])
        signed = SignedReviewHeadCheckpoint(**checkpoint)
        receipt = SignedAuthorityReceipt(
            **{**fields["receipt"], "checkpoint": signed}
        )
        handoff = (
            WitnessKeyHandoff(**fields["handoff"])
            if fields["handoff"] is not None else None
        )
        command = SignedPublicationCommand(
            **{**fields, "receipt": receipt, "handoff": handoff}
        )
        if _serialize(command) != data:
            raise ValueError
        return command
    except (TypeError, ValueError, KeyError, OverflowError):
        raise ValueError("stored signed publication is malformed") from None


def _packet_json(packet: SourceReviewPacket) -> str:
    if type(packet) is not SourceReviewPacket:
        raise ValueError("expected exact source packet")
    if (
        type(packet.declaration_sha256) is not str
        or _SHA.fullmatch(packet.declaration_sha256) is None
        or type(packet.snapshot_sha256) is not str
        or _SHA.fullmatch(packet.snapshot_sha256) is None
        or type(packet.inspected_on) is not date
        or type(packet.captured_on) is not date
    ):
        raise ValueError("invalid source packet")
    data = asdict(packet)
    data["inspected_on"] = packet.inspected_on.isoformat()
    data["captured_on"] = packet.captured_on.isoformat()
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


class LocalCheckpointPublisher:
    """Local DB with configured operator-key admission and atomic per-packet CAS.

    The caller controls the file, public keys and clock. No external witness
    service, principal authentication, protected signer or legal rights exist.
    """

    def __init__(
        self,
        path: Path,
        *,
        checkpoint_keys: Mapping[str, bytes],
        witness_keys: Mapping[str, bytes],
        operator_keys: Mapping[str, bytes],
        initial_witness_key_id: str,
        create: bool = False,
    ) -> None:
        if (
            not isinstance(path, Path)
            or not path.is_absolute()
            or not path.parent.is_dir()
            or path.is_symlink()
        ):
            raise ValueError("publisher needs a safe absolute local database path")
        if not (_keys_valid(checkpoint_keys) and _keys_valid(witness_keys)
                and _keys_valid(operator_keys)):
            raise ValueError("configured checkpoint, witness and operator keys required")
        all_ids = set(checkpoint_keys) | set(witness_keys) | set(operator_keys)
        all_material = (
            list(checkpoint_keys.values())
            + list(witness_keys.values())
            + list(operator_keys.values())
        )
        if (
            len(all_ids) != (
                len(checkpoint_keys) + len(witness_keys) + len(operator_keys)
            )
            or len(set(all_material)) != len(all_material)
        ):
            raise ValueError("publication signing roles must have distinct keys")
        if (
            type(initial_witness_key_id) is not str
            or initial_witness_key_id not in witness_keys
        ):
            raise ValueError("unknown initial publication witness")
        if type(create) is not bool:
            raise ValueError("create flag must be a boolean")
        self._path = path
        self._checkpoints = dict(checkpoint_keys)
        self._witnesses = dict(witness_keys)
        self._operators = dict(operator_keys)
        self._bootstrap = initial_witness_key_id

        if create:
            if path.exists():
                raise ValueError("refusing to replace existing publication registry")
            connection = sqlite3.connect(str(path), timeout=5, isolation_level=None)
            try:
                connection.execute("PRAGMA synchronous = FULL")
                connection.execute("BEGIN IMMEDIATE")
                connection.execute("CREATE TABLE publication_schema(version INTEGER NOT NULL,"
                                   " initial_witness_key_id TEXT NOT NULL)")
                connection.execute("INSERT INTO publication_schema VALUES (?,?)",
                                   (_SCHEMA, self._bootstrap))
                connection.execute(
                    "CREATE TABLE publication_heads("
                    "packet_sha256 TEXT PRIMARY KEY,packet_json TEXT NOT NULL,"
                    "sequence INTEGER NOT NULL,receipt_sha256 TEXT NOT NULL)"
                )
                connection.execute(
                    "CREATE TABLE publication_events("
                    "packet_sha256 TEXT NOT NULL,sequence INTEGER NOT NULL,"
                    "command_json TEXT NOT NULL,PRIMARY KEY(packet_sha256,sequence),"
                    "FOREIGN KEY(packet_sha256) REFERENCES publication_heads(packet_sha256))"
                )
                connection.execute("COMMIT")
            except sqlite3.DatabaseError:
                connection.rollback()
                raise ValueError("publication registry schema initialization failed") from None
            finally:
                connection.close()
        if not path.is_file():
            raise ValueError("publication registry does not exist")
        db = self._connect()
        try:
            self._schema(db)
        finally:
            db.close()

    def _connect(self) -> sqlite3.Connection:
        if not self._path.is_file() or self._path.is_symlink():
            raise ValueError("publication registry path missing or unsafe")
        try:
            db = sqlite3.connect(str(self._path), timeout=5, isolation_level=None)
            db.execute("PRAGMA foreign_keys = ON")
            db.execute("PRAGMA synchronous = FULL")
            db.execute("PRAGMA busy_timeout = 5000")
            return db
        except sqlite3.DatabaseError:
            raise ValueError("cannot open local publication registry") from None

    def _schema(self, db: sqlite3.Connection) -> None:
        try:
            # A shared policy+publication database must never be opened via
            # this standalone class's static operator-key admission path.
            if db.execute(
                "SELECT 1 FROM sqlite_master "
                "WHERE type='table' AND name='atomic_governed_schema'"
            ).fetchone():
                raise ValueError(
                    "integrated publisher requires atomic governed admission"
                )
            metadata = db.execute(
                "SELECT version,initial_witness_key_id FROM publication_schema"
            ).fetchall()
            if metadata != [(_SCHEMA, self._bootstrap)]:
                raise ValueError("publication registry schema or bootstrap changed")
            for table in ("publication_heads", "publication_events"):
                db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        except sqlite3.DatabaseError:
            raise ValueError("invalid publication registry schema") from None

    def _verify_event(
        self,
        packet: SourceReviewPacket,
        command: SignedPublicationCommand,
        *,
        sequence: int,
        previous_hash: str,
        previous_witness: str,
        previous_epoch: int,
        previous_revision: int,
        previous_review_head: str | None,
        previous_issue: date,
    ) -> tuple[str, str, int, int, str, date]:
        receipt = command.receipt
        checkpoint = receipt.checkpoint
        if (
            type(command.operator_key_id) is not str
            or command.operator_key_id not in self._operators
            or type(command.expected_sequence) is not int
            or command.expected_sequence != sequence
            or type(command.expected_receipt_sha256) is not str
            or not compare_digest(command.expected_receipt_sha256, previous_hash)
            or type(receipt.previous_receipt_sha256) is not str
            or not compare_digest(receipt.previous_receipt_sha256, previous_hash)
            or type(checkpoint.anchor_sequence) is not int
            or checkpoint.anchor_sequence != sequence + 1
            or type(receipt.key_epoch) is not int
            or not 1 <= receipt.key_epoch <= _MAX_SEQUENCE
            or type(receipt.witness_key_id) is not str
            or receipt.witness_key_id not in self._witnesses
            or checkpoint.issued_on < previous_issue
        ):
            raise ValueError("publication sequence, role, predecessor or dates invalid")
        verify_signed_head_checkpoint(
            packet, checkpoint,
            trusted_anchor_keys=self._checkpoints,
            minimum_anchor_sequence=sequence + 1,
            checked_on=checkpoint.issued_on,
        )
        if (
            checkpoint.review_revision < previous_revision
            or (previous_review_head is not None and
                (checkpoint.review_revision == previous_revision)
                != (checkpoint.review_head_sha256 == previous_review_head))
        ):
            raise ValueError("published review revision or head regressed or conflicted")
        if (receipt.witness_key_id, receipt.key_epoch) == (
            previous_witness, previous_epoch
        ):
            if command.handoff is not None:
                raise ValueError("unnecessary witness key handoff")
        else:
            handoff = command.handoff
            if (
                type(handoff) is not WitnessKeyHandoff
                or receipt.witness_key_id == previous_witness
                or receipt.key_epoch != previous_epoch + 1
                or handoff.previous_key_id != previous_witness
                or handoff.new_key_id != receipt.witness_key_id
                or handoff.previous_epoch != previous_epoch
                or handoff.new_epoch != receipt.key_epoch
                or handoff.effective_sequence != sequence + 1
                or handoff.previous_receipt_sha256 != previous_hash
            ):
                raise ValueError("witness key change requires exact dual-signed handoff")
            if (
                type(handoff.old_signature_hex) is not str
                or _SIG.fullmatch(handoff.old_signature_hex) is None
                or type(handoff.new_signature_hex) is not str
                or _SIG.fullmatch(handoff.new_signature_hex) is None
            ):
                raise ValueError("invalid witness rotation signatures")
            handoff_message = _canonical_handoff_message(handoff)
            _verify_signature(
                self._witnesses[previous_witness],
                handoff.old_signature_hex, handoff_message,
            )
            _verify_signature(
                self._witnesses[receipt.witness_key_id],
                handoff.new_signature_hex, handoff_message,
            )
        _verify_signature(
            self._witnesses[receipt.witness_key_id],
            receipt.witness_signature_hex,
            _canonical_authority_receipt_message(receipt),
        )
        _verify_signature(
            self._operators[command.operator_key_id],
            command.operator_signature_hex,
            _canonical_publication_message(command),
        )
        return (
            _receipt_digest(receipt), receipt.witness_key_id,
            receipt.key_epoch, checkpoint.review_revision,
            checkpoint.review_head_sha256, checkpoint.issued_on,
        )

    def _load(
        self, db: sqlite3.Connection, packet: SourceReviewPacket,
    ) -> tuple[int, str, str, int, int, str | None, date, date | None]:
        packet_json = _packet_json(packet)
        row = db.execute(
            "SELECT packet_json,sequence,receipt_sha256 FROM publication_heads"
            " WHERE packet_sha256=?", (packet.declaration_sha256,),
        ).fetchone()
        if row is None:
            return (
                0, GENESIS_PUBLICATION_HEAD, self._bootstrap,
                1, -1, None, packet.inspected_on, None,
            )
        stored_packet, stored_sequence, stored_hash = row
        if stored_packet != packet_json:
            raise ValueError("stored publisher source identity mismatch")
        if (
            type(stored_sequence) is not int or not 1 <= stored_sequence <= _MAX_EVENTS
            or type(stored_hash) is not str or _SHA.fullmatch(stored_hash) is None
        ):
            raise ValueError("stored publication sequence or head invalid")
        rows = db.execute(
            "SELECT sequence,command_json FROM publication_events"
            " WHERE packet_sha256=? ORDER BY sequence",
            (packet.declaration_sha256,),
        ).fetchall()
        if len(rows) != stored_sequence or [r[0] for r in rows] != list(
            range(1, stored_sequence + 1)
        ):
            raise ValueError("stored publication log is truncated or has gaps")
        previous_hash = GENESIS_PUBLICATION_HEAD
        previous_witness = self._bootstrap
        epoch = 1
        review_revision = -1
        review_head: str | None = None
        previous_issue = packet.inspected_on
        expires: date | None = None
        for current_seq, command_json in rows:
            cmd = _decode(command_json)
            (
                previous_hash, previous_witness, epoch, review_revision,
                review_head, previous_issue,
            ) = self._verify_event(
                packet, cmd, sequence=current_seq - 1,
                previous_hash=previous_hash,
                previous_witness=previous_witness, previous_epoch=epoch,
                previous_revision=review_revision,
                previous_review_head=review_head, previous_issue=previous_issue,
            )
            expires = cmd.receipt.checkpoint.expires_on
        if not compare_digest(previous_hash, stored_hash):
            raise ValueError("stored publication head differs from signed log")
        return (
            stored_sequence, previous_hash, previous_witness, epoch,
            review_revision, review_head, previous_issue, expires,
        )

    def snapshot(
        self, packet: SourceReviewPacket, *, checked_on: date,
        externally_expected_head_sha256: str | None = None,
    ) -> LocalPublicationRevision:
        """Recheck full local signed history; external head may detect rollback."""
        if type(checked_on) is not date or checked_on < packet.inspected_on:
            raise ValueError("invalid publisher read date")
        db = self._connect()
        try:
            db.execute("BEGIN")
            self._schema(db)
            seq, head, _, _, rev, _, _, expires = self._load(db, packet)
            if externally_expected_head_sha256 is not None and (
                type(externally_expected_head_sha256) is not str
                or _SHA.fullmatch(externally_expected_head_sha256) is None
                or not compare_digest(externally_expected_head_sha256, head)
            ):
                raise ValueError("publisher head differs from independently expected head")
            db.execute("COMMIT")
            return LocalPublicationRevision(
                sequence=seq, receipt_sha256=head,
                checkpoint_review_revision=rev, checked_on=checked_on,
                checkpoint_expired=expires is not None and checked_on > expires,
            )
        except sqlite3.DatabaseError:
            raise ValueError("publisher snapshot database error") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()

    def publish(
        self, packet: SourceReviewPacket, command: SignedPublicationCommand,
        *, expected_sequence: int, expected_receipt_sha256: str,
        checked_on: date,
    ) -> LocalPublicationRevision:
        """Verify exact operator-signed proposal, then atomically commit."""
        if type(checked_on) is not date or checked_on < packet.inspected_on:
            raise ValueError("invalid publisher write date")
        # The standalone static-roster publisher cannot authenticate or enforce
        # policy-bound signatures. It must not accept a governed v2 proposal.
        if type(command) is SignedPublicationCommand and (
            command.expected_policy_revision is not None
            or command.expected_policy_head_sha256 is not None
        ):
            raise ValueError("policy-bound publication requires atomic governed publisher")
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            self._schema(db)
            (
                seq, head, witness, epoch, review_rev,
                review_head, previous_issue, _,
            ) = self._load(db, packet)
            if (
                type(expected_sequence) is not int
                or expected_sequence != seq
                or type(expected_receipt_sha256) is not str
                or _SHA.fullmatch(expected_receipt_sha256) is None
                or not compare_digest(expected_receipt_sha256, head)
            ):
                raise ValueError("stale publication version or head")
            if seq >= _MAX_EVENTS:
                raise ValueError("publisher exceeds bounded event budget")
            serialized = _serialize(command)
            (
                new_hash, _, _, new_revision, _, new_issue,
            ) = self._verify_event(
                packet, command, sequence=seq,
                previous_hash=head, previous_witness=witness,
                previous_epoch=epoch, previous_revision=review_rev,
                previous_review_head=review_head, previous_issue=previous_issue,
            )
            if new_issue > checked_on:
                raise ValueError("publisher cannot accept future-issued checkpoint")
            if seq == 0:
                if db.execute("SELECT COUNT(*) FROM publication_heads").fetchone()[0] >= (
                    _MAX_PACKETS
                ):
                    raise ValueError("publisher exceeds bounded packet budget")
                db.execute(
                    "INSERT INTO publication_heads VALUES (?,?,?,?)",
                    (packet.declaration_sha256, _packet_json(packet),
                     0, GENESIS_PUBLICATION_HEAD),
                )
            db.execute(
                "INSERT INTO publication_events VALUES (?,?,?)",
                (packet.declaration_sha256, seq + 1, serialized),
            )
            db.execute(
                "UPDATE publication_heads SET sequence=?,receipt_sha256=?"
                " WHERE packet_sha256=?",
                (seq + 1, new_hash, packet.declaration_sha256),
            )
            db.execute("COMMIT")
            return LocalPublicationRevision(
                sequence=seq + 1, receipt_sha256=new_hash,
                checkpoint_review_revision=new_revision, checked_on=checked_on,
                checkpoint_expired=checked_on > command.receipt.checkpoint.expires_on,
            )
        except sqlite3.DatabaseError:
            raise ValueError("publication database transaction failed without commit") from None
        finally:
            if db.in_transaction:
                db.rollback()
            db.close()
