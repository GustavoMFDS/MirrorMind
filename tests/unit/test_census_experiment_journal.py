import json
import sqlite3
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from decimal import Decimal

import pytest
from test_census_experiment import REV, execute, fixture

from mirrormind.domains.retail.census_experiment_journal import CensusExperimentJournal


def registered(tmp_path):
    rows, plan, spec, eid = fixture()
    path = tmp_path / "census.sqlite"
    journal = CensusExperimentJournal(path)
    assert journal.register(
        rows, plan=plan, spec=spec, expected_experiment_sha256=eid, declared_code_revision=REV
    ) == eid
    return journal, path, rows, plan, spec, eid


def encode(receipt):
    return json.dumps(receipt, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def admit(journal, rows, plan, eid, submitted, split="holdout"):
    return journal.admit(
        eid, rows, plan=plan, split=split, declared_code_revision=REV, submitted=submitted
    )


def test_journal_reopen_and_replay(tmp_path):
    journal, path, rows, plan, spec, eid = registered(tmp_path)
    a = execute(rows, plan, spec, eid)
    b = execute(rows, plan, spec, eid, "validation")
    assert admit(journal, rows, plan, eid, encode(a)) == a["receipt_sha256"]
    assert admit(journal, rows[::-1], plan, eid, encode(a)) == a["receipt_sha256"]
    assert admit(journal, rows, plan, eid, encode(b), "validation") == b["receipt_sha256"]
    journal = CensusExperimentJournal(path)
    assert journal.verify_stored(
        eid, rows, plan=plan, split="holdout", declared_code_revision=REV, submitted=encode(a)
    ) == a["receipt_sha256"]
    result = journal.read(eid)
    assert result["receipts"] == {"holdout": a["receipt_sha256"], "validation": b["receipt_sha256"]}
    assert result["stored_receipts_verified_on_read"] is False
    assert result["holdout_lock_verified"] is False
    assert result["inference_status"] == "abstained"
    with sqlite3.connect(path) as db:
        assert len(db.execute("SELECT * FROM experiments").fetchone()) == 4
        assert all(len(row) == 3 for row in db.execute("SELECT * FROM receipts"))


def test_journal_rejects_forgery_and_changed_input(tmp_path):
    journal, _, rows, plan, spec, eid = registered(tmp_path)
    a = execute(rows, plan, spec, eid)
    altered = (replace(rows[0], value=Decimal(99)),) + rows[1:]
    with pytest.raises(ValueError, match="inputs differ"):
        admit(journal, altered, plan, eid, encode(a))
    with pytest.raises(ValueError, match="does not match"):
        admit(journal, rows, plan, eid, b"{}")
    with pytest.raises(ValueError, match="does not match"):
        admit(journal, rows, plan, eid, encode(a), "validation")
    assert journal.read(eid)["receipts"] == {}


def test_journal_external_digest_edit_requires_replay(tmp_path):
    journal, path, rows, plan, spec, eid = registered(tmp_path)
    a = execute(rows, plan, spec, eid)
    admit(journal, rows, plan, eid, encode(a))
    with sqlite3.connect(path) as db:
        db.execute("UPDATE receipts SET digest=?", ("f" * 64,))
    assert journal.read(eid)["receipts"] == {"holdout": "f" * 64}
    with pytest.raises(ValueError, match="stored receipt does not match"):
        journal.verify_stored(
            eid, rows, plan=plan, split="holdout", declared_code_revision=REV, submitted=encode(a)
        )
    with pytest.raises(ValueError, match="receipt conflict"):
        admit(journal, rows, plan, eid, encode(a))


def test_journal_concurrent_identical_admission(tmp_path):
    journal, path, rows, plan, spec, eid = registered(tmp_path)
    a = execute(rows, plan, spec, eid)

    def worker(_):
        return admit(CensusExperimentJournal(path), rows, plan, eid, encode(a))

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert list(pool.map(worker, range(2))) == [a["receipt_sha256"]] * 2
    assert journal.read(eid)["receipts"] == {"holdout": a["receipt_sha256"]}


def test_journal_abrupt_exit_and_recovery(tmp_path):
    journal, path, rows, plan, spec, eid = registered(tmp_path)
    child = """
import os,sqlite3,sys
db=sqlite3.connect(sys.argv[1],isolation_level=None)
db.execute("BEGIN IMMEDIATE")
db.execute("INSERT INTO receipts VALUES(?,?,?)",(sys.argv[2],"holdout","f"*64))
os._exit(73)
"""
    result = subprocess.run([sys.executable, "-c", child, str(path), eid], timeout=15, check=False)
    assert result.returncode == 73
    journal = CensusExperimentJournal(path)
    assert journal.read(eid)["receipts"] == {}
    a = execute(rows, plan, spec, eid)
    assert admit(journal, rows, plan, eid, encode(a)) == a["receipt_sha256"]


def test_journal_registration_and_capacity(tmp_path, monkeypatch):
    rows, plan, spec, eid = fixture()
    journal = CensusExperimentJournal(tmp_path / "journal.sqlite")
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        journal.register(
            rows, plan=plan, spec=spec, expected_experiment_sha256="f" * 64, declared_code_revision=REV
        )
    with pytest.raises(ValueError, match="not registered"):
        journal.read(eid)
    monkeypatch.setattr(
        "mirrormind.domains.retail.census_experiment_journal.MAX_CENSUS_JOURNAL_EXPERIMENTS", 1
    )
    assert journal.register(
        rows, plan=plan, spec=spec, expected_experiment_sha256=eid, declared_code_revision=REV
    ) == eid
    from mirrormind.domains.retail.census_experiment import (
        census_experiment_sha256,
        prepare_census_experiment,
    )
    other = prepare_census_experiment(rows, plan=plan, declared_code_revision="a" * 40)
    with pytest.raises(ValueError, match="capacity"):
        journal.register(
            rows, plan=plan, spec=other, expected_experiment_sha256=census_experiment_sha256(other),
            declared_code_revision="a" * 40,
        )


def test_journal_rejects_foreign_schema_and_schema_drift(tmp_path):
    foreign = tmp_path / "foreign.sqlite"
    with sqlite3.connect(foreign) as db:
        db.execute("CREATE TABLE unrelated(x)")
    with pytest.raises(ValueError, match="incompatible journal"):
        CensusExperimentJournal(foreign)
    journal, path, _, _, _, eid = registered(tmp_path)
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE unrelated(x)")
    with pytest.raises(ValueError, match="incompatible journal"):
        journal.read(eid)
    with pytest.raises(ValueError, match="incompatible journal"):
        CensusExperimentJournal(path)


def test_journal_rejects_sqlite_like_noninternal_object(tmp_path):
    journal, path, _, _, _, eid = registered(tmp_path)
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE sqliteXforeign(x)")
    with pytest.raises(ValueError, match="incompatible journal"):
        journal.read(eid)
