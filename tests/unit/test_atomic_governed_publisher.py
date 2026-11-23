"""Fictional atomic policy-gated publication: revocation and commit share one DB."""
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
from datetime import date
from hashlib import sha256
from threading import Barrier

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.atomic_governed_publisher import (
    AtomicGovernedPublisher,
)
from mirrormind.modules.evidence.authority_transcript import (
    SignedAuthorityReceipt,
    _canonical_authority_receipt_message,
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
from mirrormind.modules.evidence.operator_governance import (
    GENESIS_POLICY_HEAD,
    OperatorPolicyRevision,
    SignedOperatorPolicyEvent,
    _canonical_event_message,
)
from mirrormind.modules.evidence.review_decisions import (
    GENESIS_HEAD,
    SignedReviewDecision,
    _canonical_review_message,
)
from mirrormind.modules.evidence.snapshots import stage_csv_snapshot
from mirrormind.modules.evidence.sqlite_review_registry import SQLiteReviewRegistry

NOW = date(2026, 11, 21)


def keypair():
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return private, public


def synthetic_packet():
    raw = (
        b"series_id,observed_on,available_on,units\n"
        b"PRIVATE-SERIES,2011-01-05,2011-01-08,7\n"
    )
    staged = stage_csv_snapshot(raw, expected_sha256=sha256(raw).hexdigest())
    return prepare_source_review_packet(
        staged,
        SourceReviewDeclaration(
            source_kind="daily_csv", source_record_ref="SOURCE_REVIEW_001",
            snapshot_sha256=staged.sha256_hex,
            license_evidence_ref="LICENSE_NOTE_001",
            permission_evidence_ref="RIGHTS_REVIEW_001",
            privacy_review_ref="PRIVACY_REVIEW_001",
            intended_use="research_evaluation", retention_days=45,
            captured_on=date(2026, 11, 18),
        ),
        inspected_on=date(2026, 11, 19),
    )


def review_event(source, signer, sequence, previous, decision):
    event = SignedReviewDecision(
        review_ref=f"REVIEW_EVENT_{sequence:03d}",
        reviewer_key_id="REVIEW_KEY_001",
        sequence=sequence, previous_head_sha256=previous,
        packet_sha256=source.declaration_sha256,
        snapshot_sha256=source.snapshot_sha256,
        source_kind=source.source_kind,
        intended_use=source.intended_use,
        decision=decision,
        decided_on=date(2026, 11, 20) if sequence == 1 else NOW,
        expires_on=date(2026, 12, 20) if decision == "approve" else None,
        signature_hex="0" * 128,
    )
    return replace(
        event, signature_hex=signer.sign(_canonical_review_message(event)).hex()
    )


def policy_event(case, action, *, sequence=1, previous=GENESIS_POLICY_HEAD,
                 operator_id="OPERATOR_001", operator_public=None,
                 issued_on=date(2026, 11, 20)):
    event = SignedOperatorPolicyEvent(
        action=action, operator_key_id=operator_id,
        operator_public_key_hex=(
            case["operator_public"] if operator_public is None else operator_public
        ).hex(),
        sequence=sequence, previous_head_sha256=previous,
        issued_on=issued_on,
        expires_on=date(2026, 12, 20) if action == "enroll" else None,
        admin_key_ids=("POLICY_ADMIN_001", "POLICY_ADMIN_002"),
        first_signature_hex="0" * 128, second_signature_hex="0" * 128,
    )
    msg = _canonical_event_message(event)
    return replace(
        event, first_signature_hex=case["admin1"].sign(msg).hex(),
        second_signature_hex=case["admin2"].sign(msg).hex(),
    )


def signed_publication(case, *, review_revision, review_head,
                       sequence, previous_pub_head):
    source = case["packet"]
    checkpoint = SignedReviewHeadCheckpoint(
        anchor_key_id="CHECKPOINT_KEY_001",
        packet_sha256=source.declaration_sha256,
        snapshot_sha256=source.snapshot_sha256,
        source_kind=source.source_kind,
        intended_use=source.intended_use,
        review_revision=review_revision,
        review_head_sha256=review_head,
        anchor_sequence=sequence,
        issued_on=date(2026, 11, 20) if sequence == 1 else NOW,
        expires_on=date(2026, 11, 25),
        signature_hex="0" * 128,
    )
    checkpoint = replace(
        checkpoint,
        signature_hex=case["checkpoint_private"].sign(
            _canonical_checkpoint_message(checkpoint)
        ).hex(),
    )
    receipt = SignedAuthorityReceipt(
        checkpoint=checkpoint, witness_key_id="WITNESS_KEY_001",
        key_epoch=1, previous_receipt_sha256=previous_pub_head,
        witness_signature_hex="0" * 128,
    )
    receipt = replace(
        receipt, witness_signature_hex=case["witness_private"].sign(
            _canonical_authority_receipt_message(receipt)
        ).hex(),
    )
    command = SignedPublicationCommand(
        receipt=receipt, handoff=None,
        operator_key_id="OPERATOR_001",
        expected_sequence=sequence - 1,
        expected_receipt_sha256=previous_pub_head,
        operator_signature_hex="0" * 128,
    )
    return replace(
        command, operator_signature_hex=case["operator_private"].sign(
            _canonical_publication_message(command)
        ).hex(),
    )


def fixture(tmp_path):
    admin1, admin1_pub = keypair()
    admin2, admin2_pub = keypair()
    reviewer, reviewer_pub = keypair()
    checkpoint, checkpoint_pub = keypair()
    witness, witness_pub = keypair()
    operator, operator_pub = keypair()
    source = synthetic_packet()
    policy_admins = {
        "POLICY_ADMIN_001": admin1_pub,
        "POLICY_ADMIN_002": admin2_pub,
    }
    checkpoint_keys = {"CHECKPOINT_KEY_001": checkpoint_pub}
    witness_keys = {"WITNESS_KEY_001": witness_pub}
    path = tmp_path / "atomic-publications.db"
    gate = AtomicGovernedPublisher(
        path, administrator_public_keys=policy_admins,
        checkpoint_keys=checkpoint_keys, witness_keys=witness_keys,
        initial_witness_key_id="WITNESS_KEY_001", create=True,
    )
    review = SQLiteReviewRegistry(
        tmp_path / "review.db", {"REVIEW_KEY_001": reviewer_pub}, create=True,
    )
    first = review.append(
        source, review_event(source, reviewer, 1, GENESIS_HEAD, "approve"),
        expected_revision=0, expected_head_sha256=GENESIS_HEAD, checked_on=NOW,
    )
    return {
        "gate": gate, "path": path, "packet": source, "review": review,
        "reviewer": reviewer, "review_head": first.log_head_sha256,
        "admin1": admin1, "admin2": admin2,
        "admins": policy_admins, "checkpoint_keys": checkpoint_keys,
        "witness_keys": witness_keys, "checkpoint_private": checkpoint,
        "witness_private": witness, "operator_private": operator,
        "operator_public": operator_pub,
    }


def reopen(case, path=None, *, admins=None, checkpoint_keys=None):
    return AtomicGovernedPublisher(
        case["path"] if path is None else path,
        administrator_public_keys=case["admins"] if admins is None else admins,
        checkpoint_keys=(
            case["checkpoint_keys"] if checkpoint_keys is None else checkpoint_keys
        ),
        witness_keys=case["witness_keys"],
        initial_witness_key_id="WITNESS_KEY_001",
    )


def enroll(case):
    return case["gate"].append_policy(
        policy_event(case, "enroll"),
        expected_policy_revision=0,
        expected_policy_head_sha256=GENESIS_POLICY_HEAD,
        checked_on=NOW,
    )


def publish(case, command, *, policy, prior_pub_sequence=0,
            prior_pub_head=GENESIS_PUBLICATION_HEAD, gate=None, checked_on=NOW):
    return (case["gate"] if gate is None else gate).publish(
        case["packet"], command,
        expected_policy_revision=policy.revision,
        expected_policy_head_sha256=policy.head_sha256,
        expected_publication_sequence=prior_pub_sequence,
        expected_publication_head_sha256=prior_pub_head,
        checked_on=checked_on,
    )


def prepare_second(case, prior_head):
    old = case["review"].snapshot(case["packet"], checked_on=NOW)
    revoked = case["review"].append(
        case["packet"],
        review_event(
            case["packet"], case["reviewer"], 2,
            old.log_head_sha256, "revoke",
        ),
        expected_revision=1, expected_head_sha256=old.log_head_sha256,
        checked_on=NOW,
    )
    return signed_publication(
        case, review_revision=2, review_head=revoked.log_head_sha256,
        sequence=2, previous_pub_head=prior_head,
    )


def revoke(case, current):
    return case["gate"].append_policy(
        policy_event(
            case, "revoke", sequence=current.revision + 1,
            previous=current.head_sha256, issued_on=NOW,
        ),
        expected_policy_revision=current.revision,
        expected_policy_head_sha256=current.head_sha256,
        checked_on=NOW,
    )


def test_integrated_transaction_accepts_enrolled_key_and_reopens_without_authorizing(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    published = publish(case, command, policy=enrolled)
    assert published.policy_revision == 1
    assert published.publication_sequence == 1
    assert published.review_revision == 1
    assert published.policy_head_sha256 == enrolled.head_sha256
    assert published.receipt()["publication_authorized"] is False
    assert published.receipt()["ingestion_authorized"] is False
    assert published.receipt()["forecast_eligible"] is False
    reopened = reopen(case)
    assert reopened.snapshot(case["packet"], checked_on=NOW) == published
    with pytest.raises(FrozenInstanceError):
        published.publication_sequence = 9
    for secret in ("OPERATOR_001", "PRIVATE-SERIES", "POLICY_ADMIN_001",
                   "SOURCE_REVIEW_001", "WITNESS_KEY_001"):
        assert secret not in str(published.receipt())


def test_revocation_before_publication_is_terminal_and_history_still_verifies(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    first = publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    next_command = prepare_second(case, first.publication_head_sha256)
    revoked = revoke(case, enrolled)
    assert revoked.revision == 2
    with pytest.raises(ValueError, match="stale"):
        publish(
            case, next_command, policy=enrolled, prior_pub_sequence=1,
            prior_pub_head=first.publication_head_sha256,
        )
    with pytest.raises(ValueError, match="revoked"):
        publish(
            case, next_command, policy=revoked, prior_pub_sequence=1,
            prior_pub_head=first.publication_head_sha256,
        )
    state = reopen(case).snapshot(case["packet"], checked_on=NOW)
    assert state.publication_sequence == 1
    assert state.policy_revision == 2
    assert state.receipt()["publication_authorized"] is False


def test_publication_and_revocation_race_only_admits_if_publication_commits_first(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    first = publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    second = prepare_second(case, first.publication_head_sha256)
    waiting = Barrier(2)
    writer_a = reopen(case)
    writer_b = reopen(case)

    def race_revoke():
        waiting.wait()
        return writer_a.append_policy(
            policy_event(case, "revoke", sequence=2,
                         previous=enrolled.head_sha256, issued_on=NOW),
            expected_policy_revision=1,
            expected_policy_head_sha256=enrolled.head_sha256,
            checked_on=NOW,
        )

    def race_publish():
        waiting.wait()
        try:
            return (
                "published",
                publish(case, second, gate=writer_b, policy=enrolled,
                        prior_pub_sequence=1,
                        prior_pub_head=first.publication_head_sha256),
            )
        except ValueError as error:
            if "stale" not in str(error):
                raise
            return "rejected", None

    with ThreadPoolExecutor(max_workers=2) as pool:
        future_a = pool.submit(race_revoke)
        future_b = pool.submit(race_publish)
        revoked = future_a.result()
        status, _ = future_b.result()
    after = reopen(case).snapshot(case["packet"], checked_on=NOW)
    assert revoked.revision == after.policy_revision == 2
    assert after.publication_sequence == (2 if status == "published" else 1)
    assert after.receipt()["publication_authorized"] is False
    with pytest.raises(ValueError, match="revoked"):
        publish(
            case, second, policy=revoked, prior_pub_sequence=after.publication_sequence,
            prior_pub_head=after.publication_head_sha256,
        )


def test_standalone_static_roster_publisher_cannot_open_guarded_schema(tmp_path):
    case = fixture(tmp_path)
    with pytest.raises(ValueError, match="integrated publisher requires"):
        LocalCheckpointPublisher(
            case["path"], checkpoint_keys=case["checkpoint_keys"],
            witness_keys=case["witness_keys"],
            operator_keys={"OPERATOR_001": case["operator_public"]},
            initial_witness_key_id="WITNESS_KEY_001",
        )


def test_unenrolled_expired_and_mismatched_operator_fail_closed(tmp_path):
    case = fixture(tmp_path)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    empty = case["gate"].snapshot(case["packet"], checked_on=NOW)
    with pytest.raises(ValueError, match="not enrolled"):
        publish(
            case, command,
            policy=OperatorPolicyRevision(
                revision=0, head_sha256=GENESIS_POLICY_HEAD,
                registered_count=0, checked_on=NOW,
            ),
        )
    enrolled = enroll(case)
    revoked = revoke(case, enrolled)
    with pytest.raises(ValueError, match="revoked"):
        publish(case, command, policy=revoked)
    assert empty.publication_sequence == 0


def test_role_conflicts_and_signed_admin_revocation_must_fail_without_mutation(tmp_path):
    case = fixture(tmp_path)
    initial = case["gate"].snapshot(case["packet"], checked_on=NOW)
    for forbidden in (
        case["admins"]["POLICY_ADMIN_001"],
        case["checkpoint_keys"]["CHECKPOINT_KEY_001"],
        case["witness_keys"]["WITNESS_KEY_001"],
    ):
        with pytest.raises(ValueError, match="conflicts|overlap"):
            case["gate"].append_policy(
                policy_event(case, "enroll", operator_public=forbidden),
                expected_policy_revision=0,
                expected_policy_head_sha256=GENESIS_POLICY_HEAD, checked_on=NOW,
            )
    assert case["gate"].snapshot(case["packet"], checked_on=NOW) == initial


def test_invalid_operator_signature_rejected_without_inserting_publication(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    with pytest.raises(ValueError, match="signature invalid"):
        publish(
            case, replace(command, operator_signature_hex="a" * 128),
            policy=enrolled,
        )
    assert case["gate"].snapshot(
        case["packet"], checked_on=NOW,
    ).publication_sequence == 0


def test_failed_sql_publication_update_rolls_back_row_and_head(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    with sqlite3.connect(case["path"]) as db:
        db.execute(
            "CREATE TRIGGER reject_publishing BEFORE UPDATE ON publication_heads "
            "BEGIN SELECT RAISE(ABORT, 'injected-gated-write-error'); END"
        )
    with pytest.raises(ValueError, match="without commit"):
        publish(case, command, policy=enrolled)
    with sqlite3.connect(case["path"]) as db:
        assert db.execute("SELECT COUNT(*) FROM publication_events").fetchone() == (0,)
        assert db.execute("SELECT COUNT(*) FROM publication_heads").fetchone() == (0,)
        db.execute("DROP TRIGGER reject_publishing")
    assert publish(case, command, policy=enrolled).publication_sequence == 1


def test_failed_sql_governance_update_rolls_back_policy_event(tmp_path):
    case = fixture(tmp_path)
    with sqlite3.connect(case["path"]) as db:
        db.execute(
            "CREATE TRIGGER reject_governance BEFORE UPDATE ON governance_head "
            "BEGIN SELECT RAISE(ABORT, 'injected-gated-policy-error'); END"
        )
    with pytest.raises(ValueError, match="without commit"):
        enroll(case)
    assert case["gate"].snapshot(case["packet"], checked_on=NOW).policy_revision == 0


def test_expired_operator_and_expired_checkpoint_are_rejected_at_write(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    with pytest.raises(ValueError, match="expired"):
        publish(
            case, command, policy=enrolled, checked_on=date(2027, 1, 1),
        )


def test_corrupted_policy_or_publication_rows_fail_closed_on_read(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    with sqlite3.connect(case["path"]) as db:
        db.execute("DELETE FROM governance_events WHERE sequence=1")
    with pytest.raises(ValueError, match="gaps"):
        reopen(case).snapshot(case["packet"], checked_on=NOW)


def test_restored_valid_old_integrated_db_needs_independent_head_for_rollback(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    first = publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    old_path = tmp_path / "older-gate.db"
    shutil.copyfile(case["path"], old_path)
    current = revoke(case, enrolled)
    old = reopen(case, old_path)
    assert old.snapshot(case["packet"], checked_on=NOW).policy_revision == 1
    assert old.snapshot(case["packet"], checked_on=NOW).publication_sequence == 1
    with pytest.raises(ValueError, match="external reference"):
        old.snapshot(
            case["packet"], checked_on=NOW,
            externally_expected_policy_head_sha256=current.head_sha256,
        )
    assert reopen(case).snapshot(case["packet"], checked_on=NOW).policy_revision == 2
    assert first.receipt()["ingestion_authorized"] is False


def test_reopen_rejects_changed_roster_and_create_overwrite(tmp_path):
    case = fixture(tmp_path)
    with pytest.raises(ValueError, match="refusing to overwrite"):
        AtomicGovernedPublisher(
            case["path"], administrator_public_keys=case["admins"],
            checkpoint_keys=case["checkpoint_keys"],
            witness_keys=case["witness_keys"],
            initial_witness_key_id="WITNESS_KEY_001", create=True,
        )
    _, unrelated = keypair()
    with pytest.raises(ValueError, match="roster mismatch"):
        reopen(case, checkpoint_keys={"CHECKPOINT_KEY_001": unrelated})


def test_two_publishers_same_head_only_one_winner(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    first = reopen(case)
    second = reopen(case)

    def compete(gate):
        try:
            publish(case, command, policy=enrolled, gate=gate)
            return "won"
        except ValueError as error:
            if "stale" not in str(error):
                raise
            return "stale"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(compete, (first, second)))
    assert sorted(results) == ["stale", "won"]
    assert reopen(case).snapshot(case["packet"], checked_on=NOW).publication_sequence == 1
