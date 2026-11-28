"""The local M2-03 example replays without echoing input or retrieved text."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_bounded_tool_orchestration_cli_replays_minimized_receipt() -> None:
    root = Path(__file__).resolve().parents[2]
    completed = subprocess.run(
        [sys.executable, "-m", "examples.m2_bounded_tool_orchestration"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["schema_version"] == "mirrormind.local_tool_orchestration.v1"
    assert payload["status"] == "completed"
    assert payload["provider_mode"] == "test_double"
    assert payload["tool_call_count"] == 2
    assert payload["human_review_required"] is True
    assert payload["action_authorized"] is False
    assert payload["writes_performed"] is False
    assert "seasonal naive baseline" not in completed.stdout
    assert "Fictional baseline note" not in completed.stdout
