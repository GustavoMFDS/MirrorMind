#!/usr/bin/env python3
"""Run a fail-closed local MirrorMind quality gate and emit a revision-bound receipt.

This is a temporary fallback while GitHub Actions is unavailable; it must
never be presented as a successful official GitHub Actions execution.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("pytest", ("-m", "pytest", "-q")),
    ("ruff", ("-m", "ruff", "check", "src", "tests")),
    ("catalog", ("scripts/docs/catalog.py", "--check")),
    ("atlas", ("scripts/docs/coverage.py", "--check")),
    ("evidence", ("scripts/docs/evidence.py", "--check")),
    ("capabilities", ("scripts/docs/capabilities.py", "--check")),
)


def _git(*args: str) -> str:
    """Query local Git metadata without running a shell."""
    result = subprocess.run(
        ("git", *args), cwd=ROOT, capture_output=True, text=True,
        check=True, timeout=30,
    )
    return result.stdout.strip()


def run_gate(expected_head: str) -> dict[str, object]:
    """Run all checks only for an exact clean checkout of the requested SHA."""
    if not re.fullmatch(r"[0-9a-f]{40}", expected_head):
        raise ValueError("expected_head must be an exact full lowercase Git SHA")
    actual_head = _git("rev-parse", "HEAD")
    if actual_head != expected_head:
        raise ValueError("HEAD changed or does not match expected_head")
    # The QA receipt must not attest to locally modified tracked source.
    if _git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("tracked checkout is dirty; refuse quality attestation")
    records: list[dict[str, str | int]] = []
    for name, args in CHECKS:
        command = (sys.executable, *args)
        try:
            completed = subprocess.run(command, cwd=ROOT, check=False, timeout=900)
            result_code = completed.returncode
        except (OSError, subprocess.TimeoutExpired):
            result_code = 124
        records.append({"check": name, "exit_code": result_code})
        if result_code != 0:
            break
    all_passed = (
        len(records) == len(CHECKS)
        and all(item["exit_code"] == 0 for item in records)
    )
    return {
        "status": "local_gate_passed_not_official_ci" if all_passed
                  else "local_gate_failed_or_incomplete",
        "repository": "MirrorMind",
        "head_sha": actual_head,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_executable": Path(sys.executable).name,
        "checks": records,
        "official_github_actions_status": "not_checked_by_this_script",
        "passed": all_passed,
    }


def main(argv: list[str] | None = None) -> int:
    """Reject mismatched commits or failures, optionally save JSON-only metadata."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True, help="Full 40-digit Git commit SHA")
    parser.add_argument("--receipt", type=Path, help="Optional local JSON receipt file")
    options = parser.parse_args(argv)
    try:
        receipt = run_gate(options.expected_head)
    except (ValueError, OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        print(f"Local gate refused: {exc}", file=sys.stderr)
        return 2
    summary = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    print(summary, end="")
    if options.receipt is not None:
        # Do not create files inside tracked source directories automatically.
        options.receipt.write_text(summary, encoding="utf-8")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
