"""CLI refuses malformed synthetic availability without disclosing input."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CMD = [sys.executable, "-m", "examples.m1_availability_preflight"]


def test_synthetic_asof_cli_reports_only_eligible_aggregate():
    result = subprocess.run(
        [*CMD, str(ROOT / "examples/synthetic-asof-sales.json")],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    summary = json.loads(result.stdout)
    assert summary["eligible_count"] == 5
    assert summary["eligible_observed_units"] == 36
    assert summary["excluded_late_available_count"] == 1
    assert summary["excluded_future_event_count"] == 1
    assert summary["source_status"] == "synthetic_unverified"
    assert "records" not in summary
    assert "usage_note" not in summary


def test_synthetic_asof_cli_rejects_duplicate_json_keys(tmp_path):
    path = tmp_path / "duplicate-keys.json"
    path.write_text('{"x": 1, "x": 2}', encoding="utf-8")
    result = subprocess.run(
        [*CMD, str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 2
    assert result.stdout == ""


def test_synthetic_asof_cli_redacts_filename_and_raw_values(tmp_path):
    path = tmp_path / "private-customer-label.json"
    path.write_text('{"secret": "never-expose-this-sample"}', encoding="utf-8")
    result = subprocess.run(
        [*CMD, str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 2
    assert result.stdout == ""
    assert "private-customer-label" not in result.stderr
    assert "never-expose" not in result.stderr


def test_synthetic_asof_cli_bounded_bytes(tmp_path):
    path = tmp_path / "large.json"
    path.write_bytes(b"?" * 1_048_577)
    result = subprocess.run(
        [*CMD, str(path)], cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 2
    assert result.stdout == ""
