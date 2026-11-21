"""SQLite signed-review durability and transaction regressions on invented data."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, asdict, replace
from datetime import date
from hashlib import sha256
import json
import shutil
import sqlite3
import subprocess
import sys

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SignedReviewDecision,
    _canonical_review_message,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry

CHECKED = date(2026, 11, 21)


def packet(units=7, intended_use="research_evaluation"):
    raw = (
        b"series_id,observed_on,available_on,units\n"
        + f"PRIVATE-SERIES,2011-01-05,2011-01-08,{units}\n".encode()
    )
    staged = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
    return prepare_source_review_packet(
        staged, SourceReviewDeclaration(
            source_kind="daily_csv", source_record_ref="SOURCE_REVIEW_001",
            snapshot_sha256=staged.sha256_hex,
            license_evidence_ref="LICENSE_NOTE_001",
            permission_evidence_ref="RIGHTS_REVIEW_001",
            privacy_review_ref="PRIVACY_REVIEW_001",
            intended_use=intended_use, retention_days=45,
            captured_on=date(2026, 11, 18),
        ),
        inspected_on=date(2026, 11, 19),
    )


def temporary_signer():
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return private, {"REVIEW_KEY_001": public}


def signed(source, signer, *, sequence=1, previous_head=GENESIS_HEAD,
           decision="approve", review_ref=None):
    event = SignedReviewDecision(
        review_ref=review_ref or f"REVIEW_EVENT_{sequence:03}",
        reviewer_key_id="REVIEW_KEY_001", sequence=sequence,
        previous_head_sha256=previous_head,
        packet_sha256=source.declaration_sha256,
        snapshot_sha256=source.snapshot_sha256,
        source_kind=source.source_kind, intended_use=source.intended_use,
        decision=decision,
        decided_on=date(2026, 11, 20) if sequence == 1 else CHECKED,
        expires_on=date(2026, 12, 20) if decision == "approve" else None,
        signature_hex="0" * 128,
    )
    return replace(event, signature_hex=signer.sign(_canonical_review_message(event)).hex())


def create(tmp_path, public):
    return SQLiteReviewRegistry(tmp_path / "review.db", public, create=True)


def append(registry, source, event, prior_version=0, prior_head=GENESIS_HEAD):
    return registry.append(
        source, event, expected_revision=prior_version,
        expected_head_sha256=prior_head, checked_on=CHECKED,
    )


def test_database_restart_preserves_signed_history_and_revocation(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    first = create(tmp_path, public)
    approved = append(first, source, signed(source, signer))
    assert approved.revision == 1
    assert approved.receipt()["ingestion_authorized"] is False
    assert approved.receipt()["forecast_eligible"] is False
    assert approved.receipt()["persistence_status"] == (
        "local_sqlite_transactional_not_tamper_proof"
    )
    with pytest.raises(FrozenInstanceError):
        approved.revision = 12
    reopened = SQLiteReviewRegistry(tmp_path / "review.db", public)
    assert reopened.snapshot(source, checked_on=CHECKED) == approved
    revocation = signed(
        source, signer, sequence=2, previous_head=approved.log_head_sha256,
        decision="revoke",
    )
    revoked = append(reopened, source, revocation, 1, approved.log_head_sha256)
    after_restart = SQLiteReviewRegistry(tmp_path / "review.db", public)
    assert after_restart.snapshot(source, checked_on=CHECKED) == revoked
    assert revoked.review_status == "revoked_blocks_reapproval_of_same_packet"
    with pytest.raises(ValueError, match="revoked"):
        append(after_restart, source, signed(
            source, signer, sequence=3, previous_head=revoked.log_head_sha256,
        ), 2, revoked.log_head_sha256)
    with pytest.raises(ValueError, match="stale"):
        append(after_restart, source, signed(source, signer), 0, GENESIS_HEAD)
    for secret in ("PRIVATE-SERIES", "SOURCE_REVIEW_001",
                   "REVIEW_EVENT_001", "REVIEW_KEY_001"):
        assert secret not in str(revoked.receipt())


def test_two_independent_sqlite_connections_race_for_exact_same_revision(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    left = create(tmp_path, public)
    right = SQLiteReviewRegistry(tmp_path / "review.db", public)
    choices = (
        signed(source, signer, review_ref="REVIEW_EVENT_LEFT"),
        signed(source, signer, review_ref="REVIEW_EVENT_RIGHT"),
    )

    def compete(pair):
        registry, event = pair
        try:
            append(registry, source, event)
            return "won"
        except ValueError as exc:
            if "stale" not in str(exc):
                raise
            return "stale"

    with ThreadPoolExecutor(max_workers=2) as pool:
        result = list(pool.map(compete, zip((left, right), choices)))
    assert sorted(result) == ["stale", "won"]
    assert left.snapshot(source, checked_on=CHECKED).revision == 1
    assert right.snapshot(source, checked_on=CHECKED).revision == 1


def test_transaction_rolls_back_packet_and_event_on_failed_final_update(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    with sqlite3.connect(tmp_path / "review.db") as db:
        db.execute(
            "CREATE TRIGGER reject_head BEFORE UPDATE ON packet_heads "
            "BEGIN SELECT RAISE(ABORT, 'test-injected-write-failure'); END"
        )
    with pytest.raises(ValueError, match="write failed without commit"):
        append(registry, source, signed(source, signer))
    with sqlite3.connect(tmp_path / "review.db") as db:
        assert db.execute("SELECT COUNT(*) FROM packet_heads").fetchone() == (0,)
        assert db.execute("SELECT COUNT(*) FROM review_events").fetchone() == (0,)
        db.execute("DROP TRIGGER reject_head")
    assert registry.snapshot(source, checked_on=CHECKED).revision == 0
    assert append(registry, source, signed(source, signer)).revision == 1


def test_external_head_detects_restored_older_snapshot_only_if_independently_supplied(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    approval = append(registry, source, signed(source, signer))
    older_copy = tmp_path / "older-copy.db"
    shutil.copyfile(tmp_path / "review.db", older_copy)
    revocation = signed(source, signer, sequence=2,
                        previous_head=approval.log_head_sha256, decision="revoke")
    revoked = append(registry, source, revocation, 1, approval.log_head_sha256)
    # A valid old database is internally consistent; only an independently
    # retained new head makes rollback detectable.
    old = SQLiteReviewRegistry(older_copy, public)
    assert old.snapshot(source, checked_on=CHECKED).revision == 1
    with pytest.raises(ValueError, match="externally trusted log head"):
        old.snapshot(source, checked_on=CHECKED,
                     externally_expected_head_sha256=revoked.log_head_sha256)
    assert registry.snapshot(
        source, checked_on=CHECKED,
        externally_expected_head_sha256=revoked.log_head_sha256,
    ).revision == 2


def test_tampered_event_and_truncated_history_fail_closed_on_reopen(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    first = append(registry, source, signed(source, signer))
    second = signed(source, signer, sequence=2, previous_head=first.log_head_sha256)
    append(registry, source, second, 1, first.log_head_sha256)
    with sqlite3.connect(tmp_path / "review.db") as db:
        db.execute("DELETE FROM review_events WHERE sequence = 2")
    with pytest.raises(ValueError, match="gaps or missing"):
        SQLiteReviewRegistry(tmp_path / "review.db", public).snapshot(
            source, checked_on=CHECKED
        )


def test_rewritten_event_signature_is_detected_without_identity_leaks(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    append(registry, source, signed(source, signer))
    with sqlite3.connect(tmp_path / "review.db") as db:
        old_json = db.execute("SELECT event_json FROM review_events").fetchone()[0]
        tampered = json.loads(old_json)
        tampered["signature_hex"] = "a" * 128
        db.execute(
            "UPDATE review_events SET event_json = ?",
            (json.dumps(tampered, sort_keys=True, separators=(",", ":")),),
        )
    with pytest.raises(ValueError, match="signature verification failed"):
        registry.snapshot(source, checked_on=CHECKED)


def test_bad_signature_and_wrong_packet_cannot_partially_append(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    fake = replace(signed(source, signer), signature_hex="a" * 128)
    with pytest.raises(ValueError, match="signature verification failed"):
        append(registry, source, fake)
    other_use = packet(intended_use="commercial_product")
    with pytest.raises(ValueError, match="packet"):
        append(registry, source, signed(other_use, signer))
    assert registry.snapshot(source, checked_on=CHECKED).revision == 0


def test_create_rejects_existing_path_and_reopen_requires_existing_schema(tmp_path):
    _, public = temporary_signer()
    create(tmp_path, public)
    with pytest.raises(ValueError, match="refusing to replace"):
        create(tmp_path, public)
    with pytest.raises(ValueError, match="does not exist"):
        SQLiteReviewRegistry(tmp_path / "missing.db", public)
    unrelated = tmp_path / "bad.db"
    with sqlite3.connect(unrelated) as db:
        db.execute("CREATE TABLE unrelated (id INTEGER)")
    with pytest.raises(ValueError, match="schema"):
        SQLiteReviewRegistry(unrelated, public)


def test_sqlite_registry_retention_and_revocation_are_per_packet(tmp_path):
    first, second = packet(), packet(units=8)
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    first_head = append(registry, first, signed(first, signer))
    append(registry, first, signed(first, signer, sequence=2,
           previous_head=first_head.log_head_sha256, decision="revoke"),
           1, first_head.log_head_sha256)
    assert registry.snapshot(second, checked_on=CHECKED).revision == 0
    assert append(registry, second, signed(second, signer)).revision == 1
    later = registry.snapshot(second, checked_on=date(2027, 1, 1))
    assert later.review_status == "signed_approval_expired"
    assert later.receipt()["ingestion_authorized"] is False


def test_missing_trust_and_wrong_public_key_never_recover_authorization(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    first = create(tmp_path, public)
    append(first, source, signed(source, signer))
    other_signer, wrong_keys = temporary_signer()
    assert other_signer is not signer
    reopened = SQLiteReviewRegistry(tmp_path / "review.db", wrong_keys)
    with pytest.raises(ValueError, match="signature verification failed"):
        reopened.snapshot(source, checked_on=CHECKED)
    assert first.snapshot(source, checked_on=CHECKED).receipt()["forecast_eligible"] is False


@pytest.mark.parametrize("mutation", [
    {"revision": 100},
    {"revision": True},
    {"head": "f" * 64},
    {"head": "garbled"},
])
def test_stale_or_malformed_expected_versions_rejected(tmp_path, mutation):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    with pytest.raises(ValueError, match="stale"):
        append(
            registry, source, signed(source, signer),
            mutation.get("revision", 0), mutation.get("head", GENESIS_HEAD),
        )
    assert registry.snapshot(source, checked_on=CHECKED).revision == 0


def test_database_budget_rejects_extra_packets_and_events(monkeypatch, tmp_path):
    import mirrormind.modules.evidence.sqlite_review_registry as mod

    monkeypatch.setattr(mod, "MAX_STORED_PACKETS", 1)
    monkeypatch.setattr(mod, "MAX_STORED_EVENTS", 1)
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    one = append(registry, source, signed(source, signer))
    with pytest.raises(ValueError, match="packet budget"):
        append(registry, packet(units=9), signed(packet(units=9), signer))
    with pytest.raises(ValueError, match="event budget"):
        append(registry, source, signed(source, signer, sequence=2,
               previous_head=one.log_head_sha256), 1, one.log_head_sha256)


def test_separate_interpreters_contend_on_same_database_transaction(tmp_path):
    source = packet()
    signer, public = temporary_signer()
    registry = create(tmp_path, public)
    spec_paths = []
    for index, name in enumerate(("LEFT", "RIGHT")):
        event = signed(source, signer, review_ref=f"REVIEW_EVENT_{name}")
        packet_json = asdict(source)
        packet_json["captured_on"] = source.captured_on.isoformat()
        packet_json["inspected_on"] = source.inspected_on.isoformat()
        event_json = asdict(event)
        event_json["decided_on"] = event.decided_on.isoformat()
        event_json["expires_on"] = event.expires_on.isoformat()
        spec = {
            "db": str(tmp_path / "review.db"), "key": public["REVIEW_KEY_001"].hex(),
            "packet": packet_json, "event": event_json,
        }
        spec_path = tmp_path / f"worker-{index}.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        spec_paths.append(spec_path)
    worker = """
import json
import sys
from datetime import date
from pathlib import Path
from mirrormind.modules.evidence.intake_review import SourceReviewPacket
from mirrormind.modules.evidence.review_decisions import GENESIS_HEAD, SignedReviewDecision
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry
values = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
pkt = values['packet']
pkt['captured_on'] = date.fromisoformat(pkt['captured_on'])
pkt['inspected_on'] = date.fromisoformat(pkt['inspected_on'])
ev = values['event']
ev['decided_on'] = date.fromisoformat(ev['decided_on'])
ev['expires_on'] = date.fromisoformat(ev['expires_on']) if ev['expires_on'] else None
store = SQLiteReviewRegistry(Path(values['db']), {'REVIEW_KEY_001': bytes.fromhex(values['key'])})
try:
    store.append(SourceReviewPacket(**pkt), SignedReviewDecision(**ev),
                 expected_revision=0, expected_head_sha256=GENESIS_HEAD,
                 checked_on=date(2026, 11, 21))
except ValueError as exc:
    if 'stale' not in str(exc):
        raise
    print('stale')
else:
    print('won')
"""
    processes = [
        subprocess.Popen(
            [sys.executable, "-c", worker, str(spec_path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        for spec_path in spec_paths
    ]
    responses = [process.communicate(timeout=20) for process in processes]
    assert all(p.returncode == 0 for p in processes), responses
    assert sorted(out.strip() for out, _ in responses) == ["stale", "won"]
    assert registry.snapshot(source, checked_on=CHECKED).revision == 1
