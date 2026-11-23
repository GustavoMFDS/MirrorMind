"""Fictional atomic policy-gated publication: revocation and commit share one DB."""
import json
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
from datetime import date, timedelta
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
from mirrormind.modules.evidence.integrated_fence_transcript import (
    SignedIntegratedFenceTransition,
    _canonical_fence_transition_message,
    classify_supplied_fence_fork,
    verify_integrated_fence_transcript,
)
from mirrormind.modules.evidence.integrated_head_fence import (
    SignedIntegratedHeadFence,
    _canonical_fence_message,
    _fence_sha256,
    verify_integrated_head_fence,
)
from mirrormind.modules.evidence.local_checkpoint_publisher import (
    GENESIS_PUBLICATION_HEAD,
    LocalCheckpointPublisher,
    SignedPublicationCommand,
    _canonical_publication_message,
    _decode,
    _packet_json,
    _receipt_digest,
    _serialize,
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
                       sequence, previous_pub_head, policy=None):
    source = case["packet"]
    if policy is None:
        policy = case["gate"].snapshot(source, checked_on=NOW)
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
        expected_policy_revision=policy.policy_revision,
        expected_policy_head_sha256=policy.policy_head_sha256,
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


def test_governed_signatures_are_domain_separated_from_legacy_and_fail_closed(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    bound = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    assert bound.expected_policy_revision == 1
    assert bound.expected_policy_head_sha256 == enrolled.head_sha256
    legacy_proposal = replace(
        bound, expected_policy_revision=None, expected_policy_head_sha256=None,
        operator_signature_hex="0" * 128,
    )
    legacy = replace(
        legacy_proposal,
        operator_signature_hex=case["operator_private"].sign(
            _canonical_publication_message(legacy_proposal)
        ).hex(),
    )
    old_json = _serialize(legacy)
    assert "expected_policy_revision" not in old_json
    assert "expected_policy_head_sha256" not in old_json
    assert _decode(old_json) == legacy
    assert _canonical_publication_message(legacy) != _canonical_publication_message(bound)

    with pytest.raises(ValueError, match="bind current policy"):
        publish(case, legacy, policy=enrolled)
    with pytest.raises(ValueError, match="signature invalid"):
        publish(
            case, replace(bound, operator_signature_hex=legacy.operator_signature_hex),
            policy=enrolled,
        )
    with pytest.raises(ValueError, match="binding must be complete"):
        _serialize(replace(bound, expected_policy_head_sha256=None))
    with pytest.raises(ValueError, match="invalid publication policy binding"):
        _serialize(replace(bound, expected_policy_revision=True))
    assert case["gate"].snapshot(case["packet"], checked_on=NOW).publication_sequence == 0
    assert publish(case, bound, policy=enrolled).publication_sequence == 1


def test_unrevoked_operator_must_resign_after_independent_policy_change(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    originally_signed = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    _, another_public = keypair()
    event = policy_event(
        case, "enroll", sequence=2, previous=enrolled.head_sha256,
        operator_id="OPERATOR_002", operator_public=another_public,
        issued_on=NOW,
    )
    advanced = case["gate"].append_policy(
        event, expected_policy_revision=1,
        expected_policy_head_sha256=enrolled.head_sha256, checked_on=NOW,
    )
    assert advanced.revision == 2
    with pytest.raises(ValueError, match="bind current policy"):
        publish(case, originally_signed, policy=advanced)
    assert case["gate"].snapshot(case["packet"], checked_on=NOW).publication_sequence == 0

    newly_signed = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    assert newly_signed.expected_policy_revision == 2
    result = publish(case, newly_signed, policy=advanced)
    assert reopen(case).snapshot(case["packet"], checked_on=NOW) == result


def test_existing_valid_v1_integrated_history_replays_before_new_v2_publication(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    bound = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    old_proposal = replace(
        bound, expected_policy_revision=None, expected_policy_head_sha256=None,
        operator_signature_hex="0" * 128,
    )
    old_signed = replace(
        old_proposal, operator_signature_hex=case["operator_private"].sign(
            _canonical_publication_message(old_proposal)
        ).hex(),
    )
    # Simulate a pre-upgrade, correctly signed v1 event in an existing v1 DB.
    # The new public API must never admit such an unbound command again.
    old_head = _receipt_digest(old_signed.receipt)
    with sqlite3.connect(case["path"]) as db:
        db.execute(
            "INSERT INTO publication_heads VALUES(?,?,?,?)",
            (case["packet"].declaration_sha256, _packet_json(case["packet"]),
             1, old_head),
        )
        db.execute(
            "INSERT INTO publication_events VALUES(?,?,?)",
            (case["packet"].declaration_sha256, 1, _serialize(old_signed)),
        )
    historical = reopen(case).snapshot(case["packet"], checked_on=NOW)
    assert historical.publication_sequence == 1
    assert historical.publication_head_sha256 == old_head

    second = prepare_second(case, old_head)
    assert second.expected_policy_head_sha256 == enrolled.head_sha256
    current = publish(
        case, second, policy=enrolled, prior_pub_sequence=1,
        prior_pub_head=old_head,
    )
    assert current.publication_sequence == 2
    assert reopen(case).snapshot(case["packet"], checked_on=NOW) == current


def test_standalone_publisher_cannot_accept_policy_bound_v2_command(tmp_path):
    case = fixture(tmp_path)
    enroll(case)
    command = signed_publication(
        case, review_revision=1, review_head=case["review_head"],
        sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
    )
    standalone = LocalCheckpointPublisher(
        tmp_path / "old-style-publisher.db",
        checkpoint_keys=case["checkpoint_keys"],
        witness_keys=case["witness_keys"],
        operator_keys={"OPERATOR_001": case["operator_public"]},
        initial_witness_key_id="WITNESS_KEY_001", create=True,
    )
    with pytest.raises(ValueError, match="requires atomic governed publisher"):
        standalone.publish(
            case["packet"], command, expected_sequence=0,
            expected_receipt_sha256=GENESIS_PUBLICATION_HEAD, checked_on=NOW,
        )
    assert standalone.snapshot(case["packet"], checked_on=NOW).sequence == 0


def test_policy_binding_tampering_in_stored_v2_history_invalidates_signature(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    with sqlite3.connect(case["path"]) as db:
        row = db.execute("SELECT command_json FROM publication_events").fetchone()
        encoded = json.loads(row[0])
        encoded["expected_policy_head_sha256"] = GENESIS_POLICY_HEAD
        db.execute(
            "UPDATE publication_events SET command_json=?",
            (json.dumps(encoded, separators=(",", ":"), sort_keys=True),),
        )
    with pytest.raises(ValueError, match="signature invalid"):
        reopen(case).snapshot(case["packet"], checked_on=NOW)


def signed_integrated_fence(case, signer, *, authority_sequence=1):
    state = case["gate"].snapshot(case["packet"], checked_on=NOW)
    draft = SignedIntegratedHeadFence(
        authority_key_id="INDEPENDENT_FENCE_001",
        authority_sequence=authority_sequence,
        packet_sha256=case["packet"].declaration_sha256,
        snapshot_sha256=case["packet"].snapshot_sha256,
        policy_revision=state.policy_revision,
        policy_head_sha256=state.policy_head_sha256,
        publication_sequence=state.publication_sequence,
        publication_head_sha256=state.publication_head_sha256,
        issued_on=NOW,
        expires_on=NOW + timedelta(days=7),
        signature_hex="0" * 128,
    )
    return replace(
        draft, signature_hex=signer.sign(_canonical_fence_message(draft)).hex()
    )


def check_integrated_fence(case, fence, public, *, gate=None, packet=None,
                           current_sequence=None, current_hash=None,
                           checked_on=NOW, trusted=None):
    return verify_integrated_head_fence(
        case["gate"] if gate is None else gate,
        case["packet"] if packet is None else packet,
        fence,
        trusted_fence_keys=(
            {"INDEPENDENT_FENCE_001": public} if trusted is None else trusted
        ),
        expected_current_authority_sequence=(
            fence.authority_sequence if current_sequence is None else current_sequence
        ),
        expected_current_fence_sha256=(
            _fence_sha256(fence) if current_hash is None else current_hash
        ),
        checked_on=checked_on,
    )


def test_signed_integrated_fence_matches_verified_heads_without_authorizing(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    signing_key, public = keypair()
    fence = signed_integrated_fence(case, signing_key)
    before = case["gate"].snapshot(case["packet"], checked_on=NOW)
    result = check_integrated_fence(case, fence, public)
    after = case["gate"].snapshot(case["packet"], checked_on=NOW)
    assert before == after
    assert result.policy_revision == 1
    assert result.publication_sequence == 1
    assert result.supplied_fence_sha256 == _fence_sha256(fence)
    assert result.receipt()["publication_authorized"] is False
    assert result.receipt()["ingestion_authorized"] is False
    assert result.receipt()["forecast_eligible"] is False
    for sensitive in ("OPERATOR_001", "PRIVATE-SERIES", "INDEPENDENT_FENCE_001"):
        assert sensitive not in str(result.receipt())
    assert reopen(case).snapshot(case["packet"], checked_on=NOW) == after


def test_signed_fence_detects_coherent_old_database_only_given_new_current_fence(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    first = publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    signing_key, public = keypair()
    previous_fence = signed_integrated_fence(case, signing_key, authority_sequence=1)
    old_path = tmp_path / "signed-fence-old-coherent-backup.db"
    shutil.copyfile(case["path"], old_path)
    current = revoke(case, enrolled)
    assert current.revision == 2
    latest_fence = signed_integrated_fence(case, signing_key, authority_sequence=2)
    old = reopen(case, old_path)
    with pytest.raises(ValueError, match="heads differ"):
        check_integrated_fence(case, latest_fence, public, gate=old)
    # Counterexample: stale but self-consistent external pins do NOT give freshness.
    assert check_integrated_fence(
        case, previous_fence, public, gate=old,
    ).policy_revision == 1
    with pytest.raises(ValueError, match="expected external current"):
        check_integrated_fence(
            case, previous_fence, public, gate=old,
            current_sequence=latest_fence.authority_sequence,
            current_hash=_fence_sha256(latest_fence),
        )
    assert first.publication_sequence == 1
    assert check_integrated_fence(case, latest_fence, public).policy_revision == 2


def test_signed_fence_checks_publication_head_even_without_policy_change(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    signing_key, public = keypair()
    empty_fence = signed_integrated_fence(case, signing_key, authority_sequence=1)
    publish(
        case, signed_publication(
            case, review_revision=1, review_head=case["review_head"],
            sequence=1, previous_pub_head=GENESIS_PUBLICATION_HEAD,
        ), policy=enrolled,
    )
    with pytest.raises(ValueError, match="heads differ"):
        check_integrated_fence(case, empty_fence, public)
    full_fence = signed_integrated_fence(case, signing_key, authority_sequence=2)
    assert check_integrated_fence(case, full_fence, public).publication_sequence == 1


def test_signed_fence_wrong_scope_signer_tampering_and_equivocation_fail(tmp_path):
    case = fixture(tmp_path)
    enroll(case)
    signer, public = keypair()
    _, outsider_public = keypair()
    fence = signed_integrated_fence(case, signer)
    with pytest.raises(ValueError, match="signature invalid"):
        check_integrated_fence(case, fence, outsider_public)
    with pytest.raises(ValueError, match="signer or source packet"):
        check_integrated_fence(
            case, fence, public,
            packet=replace(case["packet"], snapshot_sha256="a" * 64),
        )
    with pytest.raises(ValueError, match="expected external current"):
        check_integrated_fence(case, fence, public, current_hash="0" * 64)
    with pytest.raises(ValueError, match="expected external current"):
        check_integrated_fence(case, fence, public, current_sequence=2)
    altered = replace(fence, publication_head_sha256="a" * 64)
    with pytest.raises(ValueError, match="signature invalid"):
        check_integrated_fence(case, altered, public)
    different = replace(
        fence, expires_on=fence.expires_on - timedelta(days=1),
        signature_hex="0" * 128,
    )
    different = replace(
        different, signature_hex=signer.sign(_canonical_fence_message(different)).hex()
    )
    with pytest.raises(ValueError, match="expected external current"):
        check_integrated_fence(
            case, different, public, current_hash=_fence_sha256(fence)
        )
    assert _fence_sha256(different) != _fence_sha256(fence)


def test_signed_fence_bounds_expiry_bad_keys_and_type_confusion_fail(tmp_path):
    case = fixture(tmp_path)
    enroll(case)
    signer, public = keypair()
    fence = signed_integrated_fence(case, signer)
    with pytest.raises(ValueError, match="not yet valid"):
        check_integrated_fence(
            case, fence, public, checked_on=NOW - timedelta(days=1)
        )
    with pytest.raises(ValueError, match="expired"):
        check_integrated_fence(
            case, fence, public, checked_on=NOW + timedelta(days=8)
        )
    with pytest.raises(ValueError, match="invalid fields"):
        _canonical_fence_message(replace(fence, authority_sequence=True))
    with pytest.raises(ValueError, match="invalid fields"):
        _canonical_fence_message(
            replace(fence, expires_on=NOW + timedelta(days=31))
        )
    with pytest.raises(ValueError, match="malformed"):
        _fence_sha256(replace(fence, signature_hex="ff"))
    with pytest.raises(ValueError, match="invalid trusted"):
        check_integrated_fence(
            case, fence, public,
            trusted={"INDEPENDENT_FENCE_001": public, "DUPLICATE_FENCE_001": public},
        )
    with pytest.raises(ValueError, match="expected external current"):
        check_integrated_fence(case, fence, public, current_sequence=True)
    with pytest.raises(ValueError, match="signer or source packet"):
        check_integrated_fence(
            case, fence, public,
            trusted={"ANOTHER_FENCE_001": public},
        )


def dual_fence_keys():
    authority, authority_public = keypair()
    first_witness, first_public = keypair()
    second_witness, second_public = keypair()
    return (
        authority,
        {"INDEPENDENT_FENCE_001": authority_public},
        first_witness, second_witness,
        {"FENCE_WITNESS_001": first_public, "FENCE_WITNESS_002": second_public},
    )


def dual_fence_link(fence, prior_sequence, prior_digest, first, second,
                    *, witnessed_on=NOW):
    draft = SignedIntegratedFenceTransition(
        fence=fence,
        previous_authority_sequence=prior_sequence,
        previous_fence_sha256=prior_digest,
        witnessed_on=witnessed_on,
        witness_key_ids=("FENCE_WITNESS_001", "FENCE_WITNESS_002"),
        witness_signatures_hex=("0" * 128, "0" * 128),
    )
    message = _canonical_fence_transition_message(draft)
    return replace(
        draft, witness_signatures_hex=(
            first.sign(message).hex(), second.sign(message).hex()
        ),
    )


def check_dual_fence_transcript(case, links, authority_roster, witness_roster,
                                *, gate=None, anchor_sequence=0,
                                anchor_digest="0" * 64, current_sequence=None,
                                current_digest=None, checked_on=NOW):
    return verify_integrated_fence_transcript(
        case["gate"] if gate is None else gate,
        case["packet"], links,
        trusted_fence_keys=authority_roster,
        trusted_witness_keys=witness_roster,
        anchor_authority_sequence=anchor_sequence,
        anchor_fence_sha256=anchor_digest,
        expected_current_authority_sequence=(
            (links[-1].fence.authority_sequence if links else 0)
            if current_sequence is None else current_sequence
        ),
        expected_current_fence_sha256=(
            (_fence_sha256(links[-1].fence) if links else "0" * 64)
            if current_digest is None else current_digest
        ),
        checked_on=checked_on,
    )


def test_dual_witness_fence_chain_verified_against_integrated_local_snapshot(tmp_path):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    auth, roster, witness1, witness2, witnesses = dual_fence_keys()
    first_fence = signed_integrated_fence(case, auth, authority_sequence=1)
    first_link = dual_fence_link(first_fence, 0, "0" * 64, witness1, witness2)
    revoke(case, enrolled)
    second_fence = signed_integrated_fence(case, auth, authority_sequence=2)
    second_link = dual_fence_link(
        second_fence, 1, _fence_sha256(first_fence), witness1, witness2,
    )
    before = case["gate"].snapshot(case["packet"], checked_on=NOW)
    result = check_dual_fence_transcript(
        case, (first_link, second_link), roster, witnesses,
    )
    assert case["gate"].snapshot(case["packet"], checked_on=NOW) == before
    assert result.validated_transitions == 2
    assert result.current_authority_sequence == 2
    assert result.current_fence_sha256 == _fence_sha256(second_fence)
    assert result.receipt()["publication_authorized"] is False
    assert result.receipt()["ingestion_authorized"] is False
    assert result.receipt()["forecast_eligible"] is False
    assert result.receipt()["freshness_status"] == "caller_pinned_not_independently_fetched"
    for token in ("OPERATOR_001", "PRIVATE-SERIES", "INDEPENDENT_FENCE_001"):
        assert token not in str(result.receipt())


def test_dual_fence_transcript_rejects_missing_hops_and_old_database_with_new_pin(
    tmp_path,
):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    auth, roster, witness1, witness2, witnesses = dual_fence_keys()
    initial_fence = signed_integrated_fence(case, auth, authority_sequence=1)
    initial_link = dual_fence_link(
        initial_fence, 0, "0" * 64, witness1, witness2
    )
    old_database = tmp_path / "dual-fence-old-backup.db"
    shutil.copyfile(case["path"], old_database)
    revoke(case, enrolled)
    new_fence = signed_integrated_fence(case, auth, authority_sequence=2)
    successor = dual_fence_link(
        new_fence, 1, _fence_sha256(initial_fence), witness1, witness2
    )
    old = reopen(case, old_database)
    with pytest.raises(ValueError, match="SQLite heads differ"):
        check_dual_fence_transcript(
            case, (initial_link, successor), roster, witnesses, gate=old
        )
    # Old pins can still be replayed with the matching old local backup.
    old_result = check_dual_fence_transcript(
        case, (initial_link,), roster, witnesses, gate=old
    )
    assert old_result.current_authority_sequence == 1
    with pytest.raises(ValueError, match="terminal differs"):
        check_dual_fence_transcript(
            case, (initial_link,), roster, witnesses, gate=old,
            current_sequence=2, current_digest=_fence_sha256(new_fence),
        )
    for broken in (
        (successor,),
        (successor, initial_link),
        (initial_link, initial_link),
    ):
        with pytest.raises(ValueError, match="missing, forked or reversed"):
            check_dual_fence_transcript(case, broken, roster, witnesses)
    with pytest.raises(ValueError, match="missing, forked or reversed"):
        check_dual_fence_transcript(
            case, (initial_link, successor), roster, witnesses,
            anchor_digest="f" * 64,
        )
    assert check_dual_fence_transcript(
        case, (initial_link, successor), roster, witnesses,
    ).validated_transitions == 2


def test_dual_fence_transcript_rejects_forged_signatures_and_role_reuse(tmp_path):
    case = fixture(tmp_path)
    enroll(case)
    auth, roster, witness1, witness2, witnesses = dual_fence_keys()
    fence = signed_integrated_fence(case, auth, authority_sequence=1)
    link = dual_fence_link(fence, 0, "0" * 64, witness1, witness2)
    _, outsider_public = keypair()
    forged_authority_fence = replace(fence, policy_head_sha256="f" * 64)
    forged_authority_link = dual_fence_link(
        forged_authority_fence, 0, "0" * 64, witness1, witness2
    )
    with pytest.raises(ValueError, match="authority or dual-witness signature"):
        check_dual_fence_transcript(
            case, (forged_authority_link,), roster, witnesses
        )
    wrong_witness = replace(
        link, witness_signatures_hex=(
            link.witness_signatures_hex[0], "f" * 128
        ),
    )
    with pytest.raises(ValueError, match="authority or dual-witness signature"):
        check_dual_fence_transcript(case, (wrong_witness,), roster, witnesses)
    with pytest.raises(ValueError, match="authority or dual-witness signature"):
        check_dual_fence_transcript(
            case, (link,), roster,
            {"FENCE_WITNESS_001": witnesses["FENCE_WITNESS_001"],
             "FENCE_WITNESS_002": outsider_public},
        )
    with pytest.raises(ValueError, match="signing roles must be distinct"):
        check_dual_fence_transcript(
            case, (link,), roster,
            {"FENCE_WITNESS_001": roster["INDEPENDENT_FENCE_001"],
             "FENCE_WITNESS_002": witnesses["FENCE_WITNESS_002"]},
        )
    with pytest.raises(ValueError, match="key roster"):
        check_dual_fence_transcript(
            case, (link,), roster,
            {"FENCE_WITNESS_001": witnesses["FENCE_WITNESS_001"],
             "FENCE_WITNESS_002": witnesses["FENCE_WITNESS_001"]},
        )
    with pytest.raises(ValueError, match="malformed integrated fence transition"):
        _canonical_fence_transition_message(
            replace(link, witness_key_ids=(
                "FENCE_WITNESS_002", "FENCE_WITNESS_001"
            ))
        )


def test_two_valid_dual_witness_fence_successors_expose_unresolved_conflict(tmp_path):
    case = fixture(tmp_path)
    enroll(case)
    auth, roster, witness1, witness2, witnesses = dual_fence_keys()
    fence = signed_integrated_fence(case, auth, authority_sequence=1)
    first = dual_fence_link(fence, 0, "0" * 64, witness1, witness2)
    alternate_draft = replace(
        fence, expires_on=fence.expires_on - timedelta(days=1),
        signature_hex="0" * 128,
    )
    alternate_fence = replace(
        alternate_draft,
        signature_hex=auth.sign(_canonical_fence_message(alternate_draft)).hex(),
    )
    alternate = dual_fence_link(
        alternate_fence, 0, "0" * 64, witness1, witness2
    )
    conflict = classify_supplied_fence_fork(
        case["packet"], first, alternate,
        trusted_fence_keys=roster, trusted_witness_keys=witnesses,
        checked_on=NOW,
    )
    assert conflict.first_fence_sha256 != conflict.second_fence_sha256
    assert conflict.successor_authority_sequence == 1
    assert conflict.receipt()["status"] == (
        "observed_supplied_signed_fence_conflict_no_resolution"
    )
    assert conflict.receipt()["ingestion_authorized"] is False
    with pytest.raises(ValueError, match="no competing authenticated"):
        classify_supplied_fence_fork(
            case["packet"], first, first,
            trusted_fence_keys=roster, trusted_witness_keys=witnesses,
            checked_on=NOW,
        )
    forged = replace(
        alternate, witness_signatures_hex=("f" * 128, alternate.witness_signatures_hex[1])
    )
    with pytest.raises(ValueError, match="authority or dual-witness signature"):
        classify_supplied_fence_fork(
            case["packet"], first, forged,
            trusted_fence_keys=roster, trusted_witness_keys=witnesses,
            checked_on=NOW,
        )


def test_dual_fence_transcript_rejects_regressing_counters_and_unchanged_revision_fork(
    tmp_path,
):
    case = fixture(tmp_path)
    enrolled = enroll(case)
    auth, roster, witness1, witness2, witnesses = dual_fence_keys()
    first_fence = signed_integrated_fence(case, auth, authority_sequence=1)
    first_link = dual_fence_link(first_fence, 0, "0" * 64, witness1, witness2)
    revoke(case, enrolled)
    second_fence = signed_integrated_fence(case, auth, authority_sequence=2)
    bad_draft = replace(
        second_fence, policy_revision=0, signature_hex="0" * 128
    )
    bad_fence = replace(
        bad_draft, signature_hex=auth.sign(_canonical_fence_message(bad_draft)).hex()
    )
    regressed = dual_fence_link(
        bad_fence, 1, _fence_sha256(first_fence), witness1, witness2
    )
    with pytest.raises(ValueError, match="state counters regressed or forked"):
        check_dual_fence_transcript(
            case, (first_link, regressed), roster, witnesses,
        )
    fork_draft = replace(
        second_fence, policy_revision=1, signature_hex="0" * 128
    )
    same_revision_new_head = replace(
        fork_draft, signature_hex=auth.sign(_canonical_fence_message(fork_draft)).hex()
    )
    forged_head = dual_fence_link(
        same_revision_new_head, 1, _fence_sha256(first_fence),
        witness1, witness2,
    )
    with pytest.raises(ValueError, match="state counters regressed or forked"):
        check_dual_fence_transcript(
            case, (first_link, forged_head), roster, witnesses,
        )


def test_dual_fence_transcript_bounded_dates_types_and_local_expiry(tmp_path):
    case = fixture(tmp_path)
    enroll(case)
    auth, roster, witness1, witness2, witnesses = dual_fence_keys()
    fence = signed_integrated_fence(case, auth, authority_sequence=1)
    link = dual_fence_link(fence, 0, "0" * 64, witness1, witness2)
    with pytest.raises(ValueError, match="bounds or anchor"):
        check_dual_fence_transcript(case, (), roster, witnesses)
    with pytest.raises(ValueError, match="bounds or anchor"):
        check_dual_fence_transcript(
            case, (link,) * 33, roster, witnesses
        )
    with pytest.raises(ValueError, match="bounds or anchor"):
        check_dual_fence_transcript(
            case, (link,), roster, witnesses, anchor_sequence=True
        )
    with pytest.raises(ValueError, match="malformed integrated fence transition"):
        _canonical_fence_transition_message(
            replace(link, witnessed_on=NOW + timedelta(days=8))
        )
    with pytest.raises(ValueError, match="untrusted transition signer"):
        check_dual_fence_transcript(
            case, (link,), roster, witnesses, checked_on=NOW - timedelta(days=1),
        )
    with pytest.raises(ValueError, match="expired"):
        check_dual_fence_transcript(
            case, (link,), roster, witnesses, checked_on=NOW + timedelta(days=8),
        )
    future = dual_fence_link(
        fence, 0, "0" * 64, witness1, witness2,
        witnessed_on=NOW + timedelta(days=1),
    )
    with pytest.raises(ValueError, match="untrusted transition signer"):
        check_dual_fence_transcript(case, (future,), roster, witnesses)
