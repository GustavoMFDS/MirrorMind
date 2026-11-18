"""Subprocess test: synthetic as-of rolling evaluator refuses unsafe inputs."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CMD = [sys.executable, "-m", "examples.m1_asof_rolling_backtest"]


def test_asof_rolling_cli_scores_only_published_history():
    proc = subprocess.run(
        [*CMD, str(ROOT / "examples/synthetic-asof-weekly-sales.json")],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    result = json.loads(proc.stdout)
    assert result["scored_origins"] == 4
    assert result["abstained_origins"] == 3
    assert result["metrics"]["seasonal_naive_lag7"]["mae"] == 0
    assert result["source_status"] == "synthetic_unverified"
    assert "records" not in result
    assert "usage_note" not in result


def test_asof_rolling_cli_rejects_duplicate_object_keys(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"a": 1, "a": 2}', encoding="utf-8")
    proc = subprocess.run(
        [*CMD, str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert proc.returncode == 2
    assert proc.stdout == ""


def test_asof_rolling_cli_hides_unsafe_payload_and_filename(tmp_path):
    path = tmp_path / "private-record-name.json"
    path.write_text('{"hidden": "do-not-expose-this"}', encoding="utf-8")
    proc = subprocess.run(
        [*CMD, str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert proc.returncode == 2
    assert proc.stdout == ""
    assert "private-record-name" not in proc.stderr
    assert "do-not-expose" not in proc.stderr


def test_asof_rolling_cli_rejects_oversized_input(tmp_path):
    path = tmp_path / "big.json"
    path.write_bytes(b"?" * 1_048_577)
    proc = subprocess.run(
        [*CMD, str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert proc.returncode == 2
    assert proc.stdout == ""
