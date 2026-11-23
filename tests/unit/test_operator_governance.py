"""Synthetic, two-administrator operator key policy and rollback regressions."""
import shutil
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError, replace
from datetime import date

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from mirrormind.modules.evidence.operator_governance import (
    GENESIS_POLICY_HEAD,
    LocalOperatorGovernance,
    SignedOperatorPolicyEvent,
    _canonical_event_message,
)

CHECKED = date(2026, 11, 21)


def generate():
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return private, public


def fixtures(tmp_path):
    admin_left, left_pub = generate()
    admin_right, right_pub = generate()
    one, one_pub = generate()
    two, two_pub = generate()
    admins = {"POLICY_ADMIN_LEFT": left_pub, "POLICY_ADMIN_RIGHT": right_pub}
    path = tmp_path / "governance.db"
    registry = LocalOperatorGovernance(
        path, administrator_public_keys=admins, create=True,
    )
    return {
        "registry": registry, "path": path,
        "left": admin_left, "right": admin_right, "admins": admins,
        "one": one_pub, "two": two_pub,
    }


def signed(case, *, action="enroll", operator_id="OPERATOR_FIRST",
           operator_public=None, sequence=1, previous=GENESIS_POLICY_HEAD,
           issued_on=date(2026, 11, 20), expires_on=date(2027, 1, 1)):
    value = SignedOperatorPolicyEvent(
        action=action,
        operator_key_id=operator_id,
        operator_public_key_hex=(operator_public or case["one"]).hex(),
        sequence=sequence, previous_head_sha256=previous,
        issued_on=issued_on, expires_on=expires_on if action == "enroll" else None,
        admin_key_ids=("POLICY_ADMIN_LEFT", "POLICY_ADMIN_RIGHT"),
        first_signature_hex="0" * 128,
        second_signature_hex="0" * 128,
    )
    message = _canonical_event_message(value)
    return replace(
        value,
        first_signature_hex=case["left"].sign(message).hex(),
        second_signature_hex=case["right"].sign(message).hex(),
    )


def append(case, event, *, revision=0, head=GENESIS_POLICY_HEAD):
    return case["registry"].append(
        event, expected_revision=revision,
        expected_head_sha256=head, checked_on=CHECKED,
    )


def assess(case, *, operator_id="OPERATOR_FIRST", public=None, when=CHECKED):
    return case["registry"].assess_operator(
        operator_id, case["one"] if public is None else public,
        checked_on=when,
    )


def test_dual_admin_enrollment_survives_restart_but_never_authorizes(tmp_path):
    case = fixtures(tmp_path)
    first = append(case, signed(case))
    assert first.revision == 1
    assert first.registered_count == 1
    assert first.head_sha256 != GENESIS_POLICY_HEAD
    assert first.receipt()["publication_authorized"] is False
    assert first.receipt()["ingestion_authorized"] is False
    assert first.receipt()["forecast_eligible"] is False
    with pytest.raises(FrozenInstanceError):
        first.revision = 42
    check = assess(case)
    assert check.record_status == "locally_registered_not_authorized"
    assert check.receipt()["publication_authorized"] is False
    assert assess(case, public=case["two"]).record_status == "key_material_mismatch"
    assert assess(case, operator_id="UNKNOWN_OPERATOR").record_status == (
        "unknown_operator_record"
    )
    restored = LocalOperatorGovernance(
        case["path"], administrator_public_keys=case["admins"]
    )
    assert restored.snapshot(checked_on=CHECKED) == first
    for secret in ("OPERATOR_FIRST", "POLICY_ADMIN_LEFT", "POLICY_ADMIN_RIGHT"):
        assert secret not in str(first.receipt())
        assert secret not in str(check.receipt())


def test_revocation_is_terminal_and_replacement_needs_fresh_key_and_id(tmp_path):
    case = fixtures(tmp_path)
    first = append(case, signed(case))
    revoked = signed(
        case, action="revoke", sequence=2, previous=first.head_sha256,
        issued_on=CHECKED,
    )
    second = append(case, revoked, revision=1, head=first.head_sha256)
    assert second.revision == 2
    assert assess(case).record_status == "revoked_operator_record"
    assert assess(case).receipt()["publication_authorized"] is False
    with pytest.raises(ValueError, match="already used"):
        append(case, signed(
            case, sequence=3, previous=second.head_sha256,
            issued_on=CHECKED,
        ), revision=2, head=second.head_sha256)
    with pytest.raises(ValueError, match="already used"):
        append(case, signed(
            case, operator_id="OPERATOR_REPLACEMENT",
            sequence=3, previous=second.head_sha256, issued_on=CHECKED,
        ), revision=2, head=second.head_sha256)
    new = signed(
        case, operator_id="OPERATOR_REPLACEMENT", operator_public=case["two"],
        sequence=3, previous=second.head_sha256, issued_on=CHECKED,
    )
    third = append(case, new, revision=2, head=second.head_sha256)
    assert third.revision == 3
    assert case["registry"].assess_operator(
        "OPERATOR_REPLACEMENT", case["two"], checked_on=CHECKED,
    ).record_status == "locally_registered_not_authorized"
    assert assess(case).record_status == "revoked_operator_record"
    reopened = LocalOperatorGovernance(
        case["path"], administrator_public_keys=case["admins"]
    )
    assert reopened.snapshot(checked_on=CHECKED).head_sha256 == third.head_sha256


def test_lost_signature_or_unrecognized_administrator_is_fail_closed(tmp_path):
    case = fixtures(tmp_path)
    original = signed(case)
    forged = replace(original, first_signature_hex="a" * 128)
    with pytest.raises(ValueError, match="administrator signature invalid"):
        append(case, forged)
    forged = replace(original, second_signature_hex="b" * 128)
    with pytest.raises(ValueError, match="administrator signature invalid"):
        append(case, forged)
    unknown = replace(original, admin_key_ids=(
        "POLICY_ADMIN_LEFT", "UNKNOWN_ADMIN",
    ))
    with pytest.raises(ValueError, match="roles"):
        append(case, unknown)
    same_admin = replace(original, admin_key_ids=(
        "POLICY_ADMIN_LEFT", "POLICY_ADMIN_LEFT",
    ))
    with pytest.raises(ValueError, match="identity"):
        append(case, same_admin)
    assert case["registry"].snapshot(checked_on=CHECKED).revision == 0


def test_tampering_signed_operator_public_key_cannot_reuse_admin_sigs(tmp_path):
    case = fixtures(tmp_path)
    changed = replace(signed(case), operator_public_key_hex=case["two"].hex())
    with pytest.raises(ValueError, match="administrator signature invalid"):
        append(case, changed)
    assert case["registry"].snapshot(checked_on=CHECKED).revision == 0


def test_expiration_recomputed_and_invalid_future_policy_rejected(tmp_path):
    case = fixtures(tmp_path)
    append(case, signed(case))
    assert assess(case, when=date(2027, 1, 2)).record_status == (
        "expired_operator_record"
    )
    assert assess(case, when=date(2027, 1, 2)).receipt()[
        "publication_authorized"
    ] is False
    first = case["registry"].snapshot(checked_on=CHECKED)
    bad = signed(
        case, operator_id="OPERATOR_SECOND", operator_public=case["two"],
        sequence=2, previous=first.head_sha256,
        issued_on=date(2026, 12, 1), expires_on=date(2027, 1, 1),
    )
    with pytest.raises(ValueError, match="future-issued"):
        append(case, bad, revision=1, head=first.head_sha256)


@pytest.mark.parametrize("expiry", [
    date(2026, 11, 20), date(2028, 1, 1),
])
def test_invalid_enrollment_expiry_rejected(tmp_path, expiry):
    case = fixtures(tmp_path)
    with pytest.raises(ValueError, match="expiration"):
        append(case, signed(case, expires_on=expiry))


def test_stale_cas_and_simultaneous_separate_connections_have_one_winner(tmp_path):
    case = fixtures(tmp_path)
    second_connection = LocalOperatorGovernance(
        case["path"], administrator_public_keys=case["admins"],
    )
    first = signed(case)
    alternative = signed(
        case, operator_id="OPERATOR_SECOND", operator_public=case["two"],
    )

    def attempt(pair):
        instance, event = pair
        try:
            instance.append(
                event, expected_revision=0,
                expected_head_sha256=GENESIS_POLICY_HEAD, checked_on=CHECKED,
            )
            return "won"
        except ValueError as error:
            if "stale" not in str(error):
                raise
            return "stale"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(attempt, (
            (case["registry"], first), (second_connection, alternative),
        )))
    assert sorted(results) == ["stale", "won"]
    assert case["registry"].snapshot(checked_on=CHECKED).revision == 1
    with pytest.raises(ValueError, match="stale"):
        append(case, first)


def test_mid_transaction_failure_rolls_back_event_and_policy_head(tmp_path):
    case = fixtures(tmp_path)
    with sqlite3.connect(case["path"]) as db:
        db.execute(
            "CREATE TRIGGER reject_policy_head BEFORE UPDATE ON governance_head "
            "BEGIN SELECT RAISE(ABORT, 'injected-policy-failure'); END"
        )
    with pytest.raises(ValueError, match="without commit"):
        append(case, signed(case))
    with sqlite3.connect(case["path"]) as db:
        assert db.execute("SELECT COUNT(*) FROM governance_events").fetchone() == (0,)
        assert db.execute(
            "SELECT revision FROM governance_head WHERE id=1"
        ).fetchone() == (0,)
        db.execute("DROP TRIGGER reject_policy_head")
    assert append(case, signed(case)).revision == 1


def test_corrupt_or_truncated_policy_cannot_pass_restart_check(tmp_path):
    case = fixtures(tmp_path)
    append(case, signed(case))
    with sqlite3.connect(case["path"]) as db:
        db.execute("DELETE FROM governance_events WHERE sequence=1")
    with pytest.raises(ValueError, match="gaps"):
        case["registry"].snapshot(checked_on=CHECKED)


def test_tampered_signatures_in_persisted_event_are_caught(tmp_path):
    import json

    case = fixtures(tmp_path)
    append(case, signed(case))
    with sqlite3.connect(case["path"]) as db:
        value = db.execute(
            "SELECT event_json FROM governance_events WHERE sequence=1"
        ).fetchone()[0]
        decoded = json.loads(value)
        decoded["second_signature_hex"] = "a" * 128
        db.execute(
            "UPDATE governance_events SET event_json=? WHERE sequence=1",
            (json.dumps(decoded, sort_keys=True, separators=(",", ":")),),
        )
    with pytest.raises(ValueError, match="administrator signature invalid"):
        case["registry"].snapshot(checked_on=CHECKED)


def test_coherent_old_backup_needs_independent_head_to_detect_revocation_rollback(tmp_path):
    case = fixtures(tmp_path)
    enrolled = append(case, signed(case))
    backup = tmp_path / "governance-old.db"
    shutil.copyfile(case["path"], backup)
    revoked = append(
        case, signed(case, action="revoke", sequence=2,
                     previous=enrolled.head_sha256, issued_on=CHECKED),
        revision=1, head=enrolled.head_sha256,
    )
    old = LocalOperatorGovernance(
        backup, administrator_public_keys=case["admins"],
    )
    assert old.assess_operator(
        "OPERATOR_FIRST", case["one"], checked_on=CHECKED,
    ).record_status == "locally_registered_not_authorized"
    with pytest.raises(ValueError, match="independently expected head"):
        old.assess_operator(
            "OPERATOR_FIRST", case["one"], checked_on=CHECKED,
            externally_expected_head_sha256=revoked.head_sha256,
        )
    assert assess(case).record_status == "revoked_operator_record"


def test_reopen_rejects_changed_admin_key_roster_and_create_overwrite(tmp_path):
    case = fixtures(tmp_path)
    with pytest.raises(ValueError, match="refusing to replace"):
        LocalOperatorGovernance(
            case["path"], administrator_public_keys=case["admins"],
            create=True,
        )
    _, other_pub = generate()
    wrong_roster = {**case["admins"], "POLICY_ADMIN_RIGHT": other_pub}
    with pytest.raises(ValueError, match="roster mismatch"):
        LocalOperatorGovernance(
            case["path"], administrator_public_keys=wrong_roster,
        )
    with pytest.raises(ValueError, match="does not exist"):
        LocalOperatorGovernance(
            tmp_path / "absent.db", administrator_public_keys=case["admins"],
        )


def test_admin_keys_and_operator_keys_must_remain_distinct(tmp_path):
    case = fixtures(tmp_path)
    cmd = signed(
        case, operator_public=case["admins"]["POLICY_ADMIN_LEFT"],
    )
    with pytest.raises(ValueError, match="roles"):
        append(case, cmd)
    with pytest.raises(ValueError, match="distinct"):
        LocalOperatorGovernance(
            tmp_path / "duplicate.db",
            administrator_public_keys={
                "POLICY_ADMIN_LEFT": case["admins"]["POLICY_ADMIN_LEFT"],
                "POLICY_ADMIN_RIGHT": case["admins"]["POLICY_ADMIN_LEFT"],
            }, create=True,
        )


def test_distinct_signatures_required_from_distinct_keys(tmp_path):
    case = fixtures(tmp_path)
    original = signed(case)
    with pytest.raises(ValueError, match="administrator signature invalid"):
        append(case, replace(original,
                             second_signature_hex=original.first_signature_hex))


def test_revoke_unknown_or_mismatched_key_fails_closed(tmp_path):
    case = fixtures(tmp_path)
    with pytest.raises(ValueError, match="previously active"):
        append(case, signed(case, action="revoke"))
    first = append(case, signed(case))
    with pytest.raises(ValueError, match="previously active"):
        append(case, signed(
            case, action="revoke", operator_public=case["two"],
            sequence=2, previous=first.head_sha256, issued_on=CHECKED,
        ), revision=1, head=first.head_sha256)


def test_operator_record_budget_is_bounded(tmp_path, monkeypatch):
    import mirrormind.modules.evidence.operator_governance as module

    monkeypatch.setattr(module, "_MAX_OPERATORS", 1)
    case = fixtures(tmp_path)
    first = append(case, signed(case))
    with pytest.raises(ValueError, match="budget"):
        append(case, signed(
            case, operator_id="OPERATOR_SECOND", operator_public=case["two"],
            sequence=2, previous=first.head_sha256, issued_on=CHECKED,
        ), revision=1, head=first.head_sha256)
