"""M1a synthetic preflight smoke tests cross the subprocess/JSON boundary."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "examples/m1_observation_preflight.py"


def test_synthetic_preflight_cli_outputs_safe_summary():
    fixture = ROOT / "examples/synthetic-daily-sales.json"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(fixture)],
        text=True,
        capture_output=True,
        check=True,
    )
    summary = json.loads(completed.stdout)
    assert summary["status"] == "synthetic_structure_validated_not_forecast"
    assert summary["record_count"] == 4
    assert summary["missing_day_count"] == 4
    assert summary["source_status"] == "synthetic_unverified"
    assert "usage_note" not in summary
    assert "records" not in summary


def test_synthetic_preflight_cli_fails_without_echoing_sensitive_input(tmp_path):
    fixture = tmp_path / "private-marker.json"
    fixture.write_text('{"secret": "do-not-echo-private-marker"}', encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(fixture)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "private-marker" not in completed.stderr
    assert "do-not-echo" not in completed.stderr


def test_synthetic_preflight_cli_enforces_byte_limit(tmp_path):
    fixture = tmp_path / "oversized.json"
    fixture.write_text("x" * 1_048_577, encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(fixture)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 2
    assert completed.stdout == ""
