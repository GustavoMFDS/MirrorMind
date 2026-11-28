"""Read-only fictional research history and explicit replay."""
import hashlib
import sqlite3

import pytest

from examples import m1_census_research_history as history
from examples import m1_census_research_runner as runner
from mirrormind.domains.retail.census_experiment_journal import (
    CensusExperimentJournal,
    read_census_journal_snapshot,
)

REV = "6d1c0bdafc5e794e19670adcb3de7bfda3f907c9"


def populate(path, scenario, revision=REV, splits=("validation",)):
    eid = runner.prepare_report(revision, scenario)["experiment_sha256"]
    runner.run_research(
        revision, journal_path=path, expected=eid, splits=splits,
        commitment_mode="caller_retained", scenario=scenario,
    )
    return eid


def test_history_snapshot_replay_does_not_write(tmp_path, monkeypatch):
    path = tmp_path / "journal.sqlite"
    eid = populate(path, runner.FIXTURE)
    other = populate(path, "fictional-flat-v1", "a" * 40, ("validation", "holdout"))
    original = hashlib.sha256(path.read_bytes()).hexdigest()
    entries = read_census_journal_snapshot(path)
    assert [e["experiment_sha256"] for e in entries] == sorted([eid, other])
    assert all(e["stored_receipts_verified_on_read"] is False for e in entries)
    html = history.build_history(path)
    assert html == history.build_history(path)
    assert "Unique commitments<strong>2</strong>" in html
    assert "Stored split digests<strong>3</strong>" in html
    assert "Explicit local replay matched" not in html
    assert "not chronology" in html
    assert "Not recorded" in html
    replayed = history.build_history(path, replay_experiment=other, split="holdout")
    assert "Explicit local replay matched" in replayed
    assert 'id="replayed-holdout"' in replayed
    assert "0.00" in replayed
    assert hashlib.sha256(path.read_bytes()).hexdigest() == original

    def forbidden(*args, **kwargs):
        pytest.fail("metadata view must not score")

    monkeypatch.setattr(history, "execute_census_experiment", forbidden)
    assert history.build_history(path) == html


def test_history_rejects_missing_or_tampered_receipt(tmp_path):
    path = tmp_path / "journal.sqlite"
    eid = populate(path, runner.FIXTURE)
    with pytest.raises(ValueError, match="not stored"):
        history.build_history(path, replay_experiment=eid, split="holdout")
    with pytest.raises(ValueError, match="together"):
        history.build_history(path, replay_experiment=eid)
    with sqlite3.connect(path) as db:
        db.execute("UPDATE receipts SET digest=?", ("f" * 64,))
    assert "f" * 64 in history.build_history(path)
    with pytest.raises(ValueError, match="does not match"):
        history.build_history(path, replay_experiment=eid, split="validation")


def test_snapshot_rejects_missing_foreign_and_changed_commitment(tmp_path):
    path = tmp_path / "missing.sqlite"
    with pytest.raises(ValueError, match="existing absolute"):
        read_census_journal_snapshot(path)
    assert not path.exists()
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE unrelated(x)")
    original = path.read_bytes()
    with pytest.raises(ValueError, match="incompatible journal"):
        read_census_journal_snapshot(path)
    assert path.read_bytes() == original
    other = tmp_path / "journal.sqlite"
    populate(other, runner.FIXTURE)
    with sqlite3.connect(other) as db:
        db.execute("UPDATE experiments SET manifest=?", ("f" * 64,))
    with pytest.raises(ValueError, match="stored commitment mismatch"):
        read_census_journal_snapshot(other)


def test_history_empty_and_cli_exclusive_output(tmp_path, monkeypatch):
    import sys

    path = tmp_path / "empty.sqlite"
    CensusExperimentJournal(path)
    assert "No registered experiments" in history.build_history(path)
    target = tmp_path / "history.html"
    monkeypatch.setattr(sys, "argv", [
        "history", "--journal", str(path), "--output", str(target),
    ])
    assert history.main() == 0
    original = target.read_bytes()
    with pytest.raises(SystemExit) as exc:
        history.main()
    assert exc.value.code == 2
    assert target.read_bytes() == original


def test_snapshot_bound(tmp_path, monkeypatch):
    path = tmp_path / "journal.sqlite"
    populate(path, runner.FIXTURE)
    populate(path, "fictional-flat-v1")
    monkeypatch.setattr(
        "mirrormind.domains.retail.census_experiment_journal.MAX_CENSUS_JOURNAL_EXPERIMENTS", 1
    )
    with pytest.raises(ValueError, match="capacity"):
        read_census_journal_snapshot(path)
