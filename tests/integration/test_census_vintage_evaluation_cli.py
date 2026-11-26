"""Exercise deterministic synthetic Census vintage evaluation end to end."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import examples.m1_census_vintage_evaluation as census_example


def _run(split: str) -> subprocess.CompletedProcess[str]:
    repository_root = Path(__file__).resolve().parents[2]
    environment = dict(os.environ)
    source_path = str(repository_root / "src")
    existing_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        source_path + os.pathsep + existing_path if existing_path else source_path
    )
    return subprocess.run(
        [
            sys.executable, "-m", "examples.m1_census_vintage_evaluation",
            "--split", split,
        ],
        cwd=repository_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_synthetic_validation_and_holdout_cli_are_reproducible_and_disjoint():
    validation_first = _run("validation")
    validation_replay = _run("validation")
    holdout = _run("holdout")

    assert validation_first.returncode == validation_replay.returncode == 0
    assert validation_first.stdout == validation_replay.stdout
    assert holdout.returncode == 0
    validation_result = json.loads(validation_first.stdout)
    holdout_result = json.loads(holdout.stdout)
    assert validation_result["status"] == "aggregate_vintage_backtest_unverified"
    assert validation_result["schema_version"] == "mirrormind.census.vintage_backtest.v2"
    assert validation_result["unanchored_revision_count"] == 0
    assert holdout_result["schema_version"] == validation_result["schema_version"]
    assert holdout_result["unanchored_revision_count"] == 0
    assert validation_result["evaluation_split"] == "validation"
    assert holdout_result["evaluation_split"] == "holdout"
    assert validation_result["input_manifest_sha256"] == holdout_result[
        "input_manifest_sha256"
    ]
    assert validation_result["origin_audit"][0]["reference_month"] == "2020-12-01"
    assert holdout_result["origin_audit"][0]["reference_month"] == "2021-02-01"
    assert {
        item["reference_month"] for item in validation_result["origin_audit"]
    }.isdisjoint({
        item["reference_month"] for item in holdout_result["origin_audit"]
    })
    assert all(item["scored_origins"] == 2 for item in validation_result["horizons"])
    assert all(item["scored_origins"] == 2 for item in holdout_result["horizons"])
    assert validation_result["ingestion_authorized"] is False
    assert validation_result["forecast_eligible"] is False
    assert "actual" not in validation_first.stdout
    assert "prediction" not in validation_first.stdout
    assert "999" not in validation_first.stdout


def test_synthetic_census_cli_refuses_non_finite_json(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["m1_census_vintage_evaluation", "--split", "validation"])
    monkeypatch.setattr(
        census_example,
        "run_synthetic_evaluation",
        lambda *, split: {"split": split, "metric": float("inf")},
    )

    with pytest.raises(SystemExit) as error:
        census_example.main()

    captured = capsys.readouterr()
    assert error.value.code == 2
    assert captured.out == ""
    assert captured.err == "Invalid synthetic Census vintage evaluation input.\n"


def test_synthetic_census_cli_rejects_unknown_split():
    result = _run("test")

    assert result.returncode == 2
    assert "invalid choice" in result.stderr
    assert "999" not in result.stderr
