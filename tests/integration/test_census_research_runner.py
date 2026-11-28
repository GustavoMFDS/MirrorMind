"""End-to-end fictional runner, including process boundaries."""
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from examples import m1_census_research_runner as runner

REV = "27ca278e6c41ef79790c6492f94c25b179439958"


def invoke(command, *args):
    root = Path(__file__).resolve().parents[2]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root / "src")
    return subprocess.run(
        [sys.executable, "-m", "examples.m1_census_research_runner",
         command, "--revision", REV, *map(str, args)],
        cwd=root, env=env, capture_output=True, text=True, timeout=30, check=False,
    )


def parse(result):
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_runner_demo_replays_both_splits_and_reports_actual_metrics():
    a = invoke("demo", "--split", "both")
    b = invoke("demo", "--split", "both")
    report = parse(a)
    assert a.stdout == b.stdout
    assert report["commitment_mode"] == "self_generated_demo"
    assert report["status"] == "synthetic_run_replayed"
    assert report["synthetic_only"] is True
    assert report["inference_status"] == "abstained"
    for key in ("registration_verified", "runtime_code_attested", "holdout_lock_verified",
                "forecast_eligible", "ingestion_authorized", "action_authorized"):
        assert report[key] is False
    validation, holdout = report["splits"]
    assert validation["split"] == "validation"
    assert holdout["split"] == "holdout"
    for split in (validation, holdout):
        assert split["split_sizes"] == [30, 10, 10]
        assert split["stored_replay_matched"] is True
        assert split["winner"] is split["confidence_interval"] is None
        assert [h["horizon_months"] for h in split["horizons"]] == [1, 3, 6]
        assert all(h["scored_origins"] == 10 and h["coverage"] == 1 for h in split["horizons"])
    assert [h["metrics"]["seasonal_naive_lag12"]["mae"] for h in holdout["horizons"]] == [24]*3
    assert [h["metrics"]["trailing_12_month_mean"]["mae"] for h in holdout["horizons"]] == [15,17,21.2]
    assert "paired_losses" not in a.stdout
    digest = report.pop("report_sha256")
    assert digest == hashlib.sha256(json.dumps(
        report, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")).hexdigest()


def test_runner_prepare_and_persistent_replay(tmp_path):
    prepared = parse(invoke("prepare"))
    assert prepared["status"] == "prepared_not_executed"
    assert "splits" not in prepared
    path = tmp_path / "research.sqlite"
    args = ("--expected", prepared["experiment_sha256"], "--journal", path)
    a = invoke("run", *args)
    b = invoke("run", *args)
    result = parse(a)
    assert a.stdout == b.stdout
    assert result["commitment_mode"] == "caller_retained"
    assert [s["split"] for s in result["splits"]] == ["validation"]
    assert result["experiment_sha256"] == prepared["experiment_sha256"]
    c = parse(invoke("run", *args, "--split", "holdout"))
    assert c["experiment_sha256"] == prepared["experiment_sha256"]
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT count(*) FROM experiments").fetchone()[0] == 1
        assert db.execute("SELECT count(*) FROM receipts").fetchone()[0] == 2
        assert {r[0] for r in db.execute("SELECT digest FROM receipts")} == {
            result["splits"][0]["receipt_sha256"], c["splits"][0]["receipt_sha256"]
        }


def test_runner_mismatch_does_not_create_journal(tmp_path):
    path = tmp_path / "never-created.sqlite"
    result = invoke("run", "--expected", "0"*64, "--journal", path)
    assert result.returncode == 2
    assert not path.exists()
    assert result.stdout == ""
    assert "prior committed splits may remain" in result.stderr


def test_runner_refuses_foreign_db_and_relative_path(tmp_path):
    path = tmp_path / "foreign.sqlite"
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE unrelated(x)")
    expected = parse(invoke("prepare"))["experiment_sha256"]
    for bad in (path, "relative.sqlite"):
        result = invoke("run", "--expected", expected, "--journal", bad)
        assert result.returncode == 2
        assert result.stdout == ""
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT name FROM sqlite_master").fetchall() == [("unrelated",)]


def test_runner_partial_split_failure_preserves_prior_receipt(tmp_path, monkeypatch):
    path = tmp_path / "journal.sqlite"
    expected = runner.prepare_report(REV)["experiment_sha256"]
    execute = runner.execute_census_experiment

    def fail_holdout(*args, **kwargs):
        if kwargs["split"] == "holdout":
            raise ValueError("synthetic test failure")
        return execute(*args, **kwargs)

    monkeypatch.setattr(runner, "execute_census_experiment", fail_holdout)
    with pytest.raises(ValueError, match="synthetic test failure"):
        runner.run_research(
            REV, journal_path=path, expected=expected,
            splits=("validation", "holdout"), commitment_mode="caller_retained",
        )
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT split FROM receipts").fetchall() == [("validation",)]


def test_runner_invalid_options_rejected():
    result = invoke("demo", "--split", "development")
    assert result.returncode == 2
    assert result.stdout == ""
