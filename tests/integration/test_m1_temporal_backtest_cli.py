"""CLI reproduction: synthetic only, safe failures and bounded input."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMAND = [sys.executable, "-m", "examples.m1_temporal_backtest"]


def test_synthetic_weekly_fixture_cli_reports_held_out_metrics():
    result = subprocess.run(
        [*COMMAND, str(ROOT / "examples/synthetic-weekly-sales.json")],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["status"] == "synthetic_rolling_backtest_not_production_forecast"
    assert payload["metrics"]["seasonal_naive_lag7"]["mae"] == 0.0
    assert payload["metrics"]["trailing_mean_lag7"]["mae"] > 0.0
    assert payload["source_status"] == "synthetic_unverified"
    assert "records" not in payload
    assert "usage_note" not in payload


def test_cli_rejects_unauthorized_looking_file_without_echo(tmp_path):
    path = tmp_path / "private-token-123.json"
    path.write_text('{"private": "do-not-disclose-this-value"}', encoding="utf-8")
    process = subprocess.run(
        [*COMMAND, str(path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert process.returncode == 2
    assert process.stdout == ""
    assert "private-token" not in process.stderr
    assert "do-not-disclose" not in process.stderr


def test_cli_rejects_duplicate_json_keys_without_echo(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"x": 1, "x": 2}', encoding="utf-8")
    process = subprocess.run(
        [*COMMAND, str(path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert process.returncode == 2
    assert process.stdout == ""


def test_cli_rejects_file_exceeding_byte_cap(tmp_path):
    path = tmp_path / "too-large.json"
    path.write_bytes(b"?" * 1_048_577)
    process = subprocess.run(
        [*COMMAND, str(path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert process.returncode == 2
    assert process.stdout == ""
