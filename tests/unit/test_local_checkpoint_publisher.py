"""Fictional operator-signed local publication integrity and recovery tests."""
import json
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
from datetime import date
from hashlib import sha256

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.authority_transcript import (
    SignedAuthorityReceipt,
    WitnessKeyHandoff,
    _canonical_authority_receipt_message,
    _canonical_handoff_message,
)
from mirrormind.modules.evidence.head_checkpoints import (
    SignedReviewHeadCheckpoint,
    _canonical_checkpoint_message,
)
from mirrormind.modules.evidence.intake_review import (
    SourceReviewDeclaration,
    prepare_source_review_packet,
)
from mirrormind.modules.evidence.local_checkpoint_publisher import (
    GENESIS_PUBLICATION_HEAD,
    LocalCheckpointPublisher,
    SignedPublicationCommand,
    _canonical_publication_message,
)
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SignedReviewDecision,
    _canonical_review_message,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry

NOW = date(2026, 11, 21)


def keypair(key_id):
    key = Ed25519PrivateKey.generate()
    public = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return key, {key_id: public}


def packet(units=7):
    data = (
        b"series_id,observed_on,available_on,units\n"
        + f"PRIVATE-SERIES,2011-01-05,2011-01-08,{units}\n".encode()
    )
    staged = stage_csv_snapshot(data, expected_sha256=sha256(data).hexdigest())
    declaration = SourceReviewDeclaration(
        source_kind="daily_csv", source_record_ref="SOURCE_REVIEW_001",
        snapshot_sha256=staged.sha256_hex,
        license_evidence_ref="LICENSE_NOTE_001",
        permission_evidence_ref="RIGHTS_REVIEW_001",
        privacy_review_ref="PRIVACY_REVIEW_001",
        intended_use="research_evaluation",
        retention_days=45,
        captured_on=date(2026, 11, 18),
    )
    return prepare_source_review_packet(
        staged, declaration, inspected_on=date(2026, 11, 19)
    )


def review_event(source, signer, *, seq=1, previous=GENESIS_HEAD, decision="approve"):
    value = SignedReviewDecision(
        review_ref=f"REVIEW_EVENT_{seq:03}", reviewer_key_id="REVIEW_KEY_001",
        sequence=seq, previous_head_sha256=previous,
        packet_sha256=source.declaration_sha256, snapshot_sha256=source.snapshot_sha256,
        source_kind=source.source_kind, intended_use=source.intended_use,
        decision=decision,
        decided_on=date(2026, 11, 20) if seq == 1 else NOW,
        expires_on=date(2026, 12, 20) if decision == "approve" else None,
        signature_hex="0" * 128,
    )
    return replace(value, signature_hex=signer.sign(
        _canonical_review_message(value)
    ).hex())


def checkpoint(source, signer, revision, head, seq, issued):
    value = SignedReviewHeadCheckpoint(
        anchor_key_id="CHECKPOINT_KEY_001",
        packet_sha256=source.declaration_sha256,
        snapshot_sha256=source.snapshot_sha256,
        source_kind=source.source_kind,
        intended_use=source.intended_use,
        review_revision=revision,
        review_head_sha256=head,
        anchor_sequence=seq,
        issued_on=issued,
        expires_on=date(2026, 11, 25),
        signature_hex="0" * 128,
    )
    return replace(value, signature_hex=signer.sign(
        _canonical_checkpoint_message(value)
    ).hex())


def witnessed(cp, signer, key_id, epoch, previous):
    value = SignedAuthorityReceipt(
        checkpoint=cp, witness_key_id=key_id, key_epoch=epoch,
        previous_receipt_sha256=previous, witness_signature_hex="0" * 128,
    )
    return replace(value, witness_signature_hex=signer.sign(
        _canonical_authority_receipt_message(value)
    ).hex())


def transition(old, new, previous, sequence=2):
    value = WitnessKeyHandoff(
        previous_key_id="WITNESS_OLD", new_key_id="WITNESS_NEW",
        previous_epoch=1, new_epoch=2,
        effective_sequence=sequence, previous_receipt_sha256=previous,
        old_signature_hex="0" * 128, new_signature_hex="0" * 128,
    )
    msg = _canonical_handoff_message(value)
    return replace(value, old_signature_hex=old.sign(msg).hex(),
                   new_signature_hex=new.sign(msg).hex())


def signed_command(receipt, operator, *, expected_seq=0,
                   previous=GENESIS_PUBLICATION_HEAD, handoff=None):
    value = SignedPublicationCommand(
        receipt=receipt, handoff=handoff, operator_key_id="PUBLISHER_OPERATOR_001",
        expected_sequence=expected_seq, expected_receipt_sha256=previous,
        operator_signature_hex="0" * 128,
    )
    return replace(value, operator_signature_hex=operator.sign(
        _canonical_publication_message(value)
    ).hex())


def setup(tmp_path):
    source = packet()
    reviewer, reviewer_keys = keypair("REVIEW_KEY_001")
    signer, checkpoint_keys = keypair("CHECKPOINT_KEY_001")
    witness_old, old_public = keypair("WITNESS_OLD")
    witness_new, new_public = keypair("WITNESS_NEW")
    operator, operator_keys = keypair("PUBLISHER_OPERATOR_001")
    review = SQLiteReviewRegistry(tmp_path / "review.db", reviewer_keys, create=True)
    approved = review.append(
        source, review_event(source, reviewer),
        expected_revision=0, expected_head_sha256=GENESIS_HEAD, checked_on=NOW,
    )
    pub_path = tmp_path / "publisher.db"
    pub = LocalCheckpointPublisher(
        pub_path, checkpoint_keys=checkpoint_keys,
        witness_keys={**old_public, **new_public}, operator_keys=operator_keys,
        initial_witness_key_id="WITNESS_OLD", create=True,
    )
    cp = checkpoint(source, signer, 1, approved.log_head_sha256, 1,
                    date(2026, 11, 20))
    signed_receipt = witnessed(cp, witness_old, "WITNESS_OLD", 1, GENESIS_PUBLICATION_HEAD)
    initial_command = signed_command(signed_receipt, operator)
    return {
        "packet": source, "pub": pub, "path": pub_path, "review": review,
        "reviewer": reviewer, "check_signer": signer,
        "old": witness_old, "new": witness_new, "operator": operator,
        "checkpoint_keys": checkpoint_keys,
        "witness_keys": {**old_public, **new_public},
        "operator_keys": operator_keys, "initial": initial_command,
    }


def publish(case, command, *, version=0, head=GENESIS_PUBLICATION_HEAD):
    return case["pub"].publish(
        case["packet"], command,
        expected_sequence=version, expected_receipt_sha256=head, checked_on=NOW,
    )


def revoke_command(case, first, *, rotation=False):
    source = case["packet"]
    review = case["review"]
    old_state = review.snapshot(source, checked_on=NOW)
    revoked = review.append(
        source, review_event(
            source, case["reviewer"], seq=2,
            previous=old_state.log_head_sha256, decision="revoke",
        ), expected_revision=1, expected_head_sha256=old_state.log_head_sha256,
        checked_on=NOW,
    )
    cp = checkpoint(source, case["check_signer"], 2,
                    revoked.log_head_sha256, 2, NOW)
    if rotation:
        witness = witnessed(cp, case["new"], "WITNESS_NEW", 2, first.receipt_sha256)
        handoff = transition(case["old"], case["new"], first.receipt_sha256)
    else:
        witness = witnessed(cp, case["old"], "WITNESS_OLD", 1, first.receipt_sha256)
        handoff = None
    return signed_command(witness, case["operator"], expected_seq=1,
                          previous=first.receipt_sha256, handoff=handoff)


def test_publisher_reopens_verified_signed_head_and_never_grants_ingestion(tmp_path):
    case = setup(tmp_path)
    initial = case["pub"].snapshot(case["packet"], checked_on=NOW)
    assert initial.sequence == 0
    assert initial.receipt_sha256 == GENESIS_PUBLICATION_HEAD
    state = publish(case, case["initial"])
    assert state.sequence == 1
    assert state.receipt_sha256 != GENESIS_PUBLICATION_HEAD
    assert state.receipt()["ingestion_authorized"] is False
    assert state.receipt()["forecast_eligible"] is False
    with pytest.raises(FrozenInstanceError):
        state.sequence = 99
    reopened = LocalCheckpointPublisher(
        case["path"], checkpoint_keys=case["checkpoint_keys"],
        witness_keys=case["witness_keys"],
        operator_keys=case["operator_keys"], initial_witness_key_id="WITNESS_OLD",
    )
    assert reopened.snapshot(case["packet"], checked_on=NOW) == state
    assert reopened.snapshot(case["packet"], checked_on=date(2026, 11, 26)).checkpoint_expired
    for identifier in ("PRIVATE-SERIES", "SOURCE_REVIEW_001",
                       "PUBLISHER_OPERATOR_001", "WITNESS_OLD", "CHECKPOINT_KEY_001"):
        assert identifier not in str(state.receipt())


@pytest.mark.parametrize("rotate", [False, True])
def test_publisher_persists_revocation_checkpoint_and_dual_signed_rotation(tmp_path, rotate):
    case = setup(tmp_path)
    first = publish(case, case["initial"])
    command = revoke_command(case, first, rotation=rotate)
    second = publish(case, command, version=1, head=first.receipt_sha256)
    assert second.sequence == 2
    after_restart = LocalCheckpointPublisher(
        case["path"], checkpoint_keys=case["checkpoint_keys"],
        witness_keys=case["witness_keys"],
        operator_keys=case["operator_keys"], initial_witness_key_id="WITNESS_OLD",
    )
    assert after_restart.snapshot(case["packet"], checked_on=NOW) == second
    assert second.receipt()["ingestion_authorized"] is False


def test_stale_and_conflicting_same_sequence_fork_is_blocked(tmp_path):
    case = setup(tmp_path)
    first = publish(case, case["initial"])
    with pytest.raises(ValueError, match="stale"):
        publish(case, case["initial"])
    fork = replace(case["initial"], operator_signature_hex="a" * 128)
    with pytest.raises(ValueError, match="stale"):
        publish(case, fork)
    assert case["pub"].snapshot(case["packet"], checked_on=NOW) == first


def test_competing_independent_connections_yield_only_one_winner(tmp_path):
    case = setup(tmp_path)
    second = LocalCheckpointPublisher(
        case["path"], checkpoint_keys=case["checkpoint_keys"],
        witness_keys=case["witness_keys"],
        operator_keys=case["operator_keys"], initial_witness_key_id="WITNESS_OLD",
    )
    def race(publisher):
        try:
            publisher.publish(
                case["packet"], case["initial"], expected_sequence=0,
                expected_receipt_sha256=GENESIS_PUBLICATION_HEAD, checked_on=NOW,
            )
            return "won"
        except ValueError as error:
            if "stale" not in str(error):
                raise
            return "stale"
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(race, (case["pub"], second)))
    assert sorted(results) == ["stale", "won"]
    assert case["pub"].snapshot(case["packet"], checked_on=NOW).sequence == 1


def test_wrong_operator_key_and_absent_roles_cannot_publish(tmp_path):
    case = setup(tmp_path)
    cmd = replace(case["initial"], operator_signature_hex="b" * 128)
    with pytest.raises(ValueError, match="signature invalid"):
        publish(case, cmd)
    cmd = replace(case["initial"], operator_key_id="NOT_A_PUBLISHER")
    with pytest.raises(ValueError, match="role"):
        publish(case, cmd)
    with pytest.raises(ValueError, match="distinct"):
        LocalCheckpointPublisher(
            tmp_path / "bad-roles.db",
            checkpoint_keys=case["checkpoint_keys"],
            witness_keys=case["witness_keys"],
            operator_keys={"WITNESS_OLD": case["witness_keys"]["WITNESS_OLD"]},
            initial_witness_key_id="WITNESS_OLD", create=True,
        )
    assert case["pub"].snapshot(case["packet"], checked_on=NOW).sequence == 0


def test_operator_signature_binds_handoff_exact_checkpoint_and_predecessor(tmp_path):
    case = setup(tmp_path)
    command = case["initial"]
    forged_checkpoint = replace(
        command.receipt.checkpoint, signature_hex="a" * 128
    )
    forged_receipt = replace(command.receipt, checkpoint=forged_checkpoint)
    with pytest.raises(ValueError, match="checkpoint signature failed"):
        publish(case, replace(command, receipt=forged_receipt))
    wrong_scope = replace(command.receipt.checkpoint, intended_use="commercial_product")
    with pytest.raises(ValueError, match="source identity"):
        publish(case, replace(command, receipt=replace(command.receipt, checkpoint=wrong_scope)))
    assert case["pub"].snapshot(case["packet"], checked_on=NOW).sequence == 0


def test_missing_and_forged_witness_handoff_fail_without_partial_write(tmp_path):
    case = setup(tmp_path)
    first = publish(case, case["initial"])
    cmd = revoke_command(case, first, rotation=True)
    with pytest.raises(ValueError, match="handoff"):
        publish(case, replace(cmd, handoff=None), version=1, head=first.receipt_sha256)
    with pytest.raises(ValueError, match="signature invalid"):
        publish(case, replace(
            cmd, handoff=replace(cmd.handoff, new_signature_hex="c" * 128)
        ), version=1, head=first.receipt_sha256)
    assert case["pub"].snapshot(case["packet"], checked_on=NOW) == first


def test_failed_sql_update_rolls_back_receipt_and_head(tmp_path):
    case = setup(tmp_path)
    with sqlite3.connect(case["path"]) as db:
        db.execute(
            "CREATE TRIGGER reject_head BEFORE UPDATE ON publication_heads "
            "BEGIN SELECT RAISE(ABORT, 'test-publisher-write-abort'); END"
        )
    with pytest.raises(ValueError, match="without commit"):
        publish(case, case["initial"])
    with sqlite3.connect(case["path"]) as db:
        assert db.execute("SELECT COUNT(*) FROM publication_heads").fetchone() == (0,)
        assert db.execute("SELECT COUNT(*) FROM publication_events").fetchone() == (0,)
        db.execute("DROP TRIGGER reject_head")
    assert publish(case, case["initial"]).sequence == 1


def test_truncated_or_modified_saved_publication_is_rejected_on_read(tmp_path):
    case = setup(tmp_path)
    first = publish(case, case["initial"])
    cmd = revoke_command(case, first)
    publish(case, cmd, version=1, head=first.receipt_sha256)
    with sqlite3.connect(case["path"]) as db:
        db.execute("DELETE FROM publication_events WHERE sequence=2")
    with pytest.raises(ValueError, match="truncated|gaps"):
        case["pub"].snapshot(case["packet"], checked_on=NOW)


def test_signature_tampering_in_stored_json_fails_closed(tmp_path):
    case = setup(tmp_path)
    publish(case, case["initial"])
    with sqlite3.connect(case["path"]) as db:
        encoded = db.execute("SELECT command_json FROM publication_events").fetchone()[0]
        parsed = json.loads(encoded)
        parsed["operator_signature_hex"] = "a" * 128
        db.execute("UPDATE publication_events SET command_json=?",
                   (json.dumps(parsed, sort_keys=True, separators=(",", ":")),))
    with pytest.raises(ValueError, match="signature invalid"):
        case["pub"].snapshot(case["packet"], checked_on=NOW)


def test_old_coherent_publisher_db_is_not_independently_fresh(tmp_path):
    case = setup(tmp_path)
    first = publish(case, case["initial"])
    previous_copy = tmp_path / "publisher-old.db"
    shutil.copyfile(case["path"], previous_copy)
    cmd = revoke_command(case, first)
    current = publish(case, cmd, version=1, head=first.receipt_sha256)
    old = LocalCheckpointPublisher(
        previous_copy, checkpoint_keys=case["checkpoint_keys"],
        witness_keys=case["witness_keys"],
        operator_keys=case["operator_keys"], initial_witness_key_id="WITNESS_OLD",
    )
    assert old.snapshot(case["packet"], checked_on=NOW).sequence == 1
    with pytest.raises(ValueError, match="independently expected head"):
        old.snapshot(case["packet"], checked_on=NOW,
                     externally_expected_head_sha256=current.receipt_sha256)
    assert case["pub"].snapshot(case["packet"], checked_on=NOW).sequence == 2


def test_wrong_key_map_or_missing_existing_database_refuses_reopen(tmp_path):
    case = setup(tmp_path)
    publish(case, case["initial"])
    with pytest.raises(ValueError, match="refusing to replace"):
        LocalCheckpointPublisher(
            case["path"], checkpoint_keys=case["checkpoint_keys"],
            witness_keys=case["witness_keys"], operator_keys=case["operator_keys"],
            initial_witness_key_id="WITNESS_OLD", create=True,
        )
    with pytest.raises(ValueError, match="does not exist"):
        LocalCheckpointPublisher(
            tmp_path / "missing.db", checkpoint_keys=case["checkpoint_keys"],
            witness_keys=case["witness_keys"], operator_keys=case["operator_keys"],
            initial_witness_key_id="WITNESS_OLD",
        )
    other, wrong = keypair("PUBLISHER_OPERATOR_001")
    assert other is not None
    reopened = LocalCheckpointPublisher(
        case["path"], checkpoint_keys=case["checkpoint_keys"],
        witness_keys=case["witness_keys"], operator_keys=wrong,
        initial_witness_key_id="WITNESS_OLD",
    )
    with pytest.raises(ValueError, match="signature invalid"):
        reopened.snapshot(case["packet"], checked_on=NOW)


def test_publisher_event_budget_is_bounded(monkeypatch, tmp_path):
    import mirrormind.modules.evidence.local_checkpoint_publisher as module

    monkeypatch.setattr(module, "_MAX_EVENTS", 1)
    case = setup(tmp_path)
    first = publish(case, case["initial"])
    with pytest.raises(ValueError, match="event budget"):
        publish(case, case["initial"], version=1, head=first.receipt_sha256)
