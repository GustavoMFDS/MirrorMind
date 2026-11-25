"""Exercise the local workbook-to-event-time research path end to end."""
import json
import os
import subprocess
import sys
from pathlib import Path


def test_synthetic_cli_is_reproducible_and_keeps_event_time_limitations():
    repository_root = Path(__file__).resolve().parents[2]
    environment = dict(os.environ)
    source_path = str(repository_root / "src")
    existing_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        source_path + os.pathsep + existing_path if existing_path else source_path
    )
    command = [
        sys.executable, "-m", "examples.m1_uci_event_time_research",
        "--split", "validation",
    ]
    first = subprocess.run(
        command,
        cwd=repository_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    second = subprocess.run(
        command,
        cwd=repository_root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert first.returncode == second.returncode == 0
    assert first.stdout == second.stdout
    result = json.loads(first.stdout)
    assert result["status"] == "event_time_retrospective_unverified_availability"
    assert result["evaluation_status"] == "metrics_available"
    assert result["split"] == "validation"
    assert result["target_start"] == "2011-09-01"
    assert result["target_end"] == "2011-10-01"
    assert result["cohort_size"] == 1
    assert result["excluded_post_fit_products"] == 1
    assert result["projection_receipt"]["processed_rows"] == 377
    assert result["projection_receipt"]["accepted_rows"] == 374
    assert result["projection_receipt"]["cancelled_rows"] == 1
    assert result["projection_receipt"]["negative_quantity_rows"] == 1
    assert result["projection_receipt"]["zero_quantity_rows"] == 1
    assert result["ingestion_authorized"] is False
    assert result["point_in_time_eligible"] is False
    for private_value in (
        "SYNTHETIC-A", "SYNTHETIC-B", "SYNTHETIC-PRIVATE",
        "800000", "900001", "900004", "SYNTHETIC-FUTURE-COHORT",
    ):
        assert private_value not in first.stdout


def test_synthetic_cli_rejects_an_unreviewed_split_argument():
    repository_root = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        [sys.executable, "-m", "examples.m1_uci_event_time_research", "--split", "test"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 2
    assert "invalid choice" in result.stderr
    assert "SYNTHETIC" not in result.stderr
