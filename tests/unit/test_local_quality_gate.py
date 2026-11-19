"""Unit regressions for fail-closed local QA, with no real child checks spawned."""
from pathlib import Path
from subprocess import CompletedProcess, TimeoutExpired
import runpy

import pytest

MODULE = runpy.run_path(str(Path(__file__).resolve().parents[2] /
                            "scripts/local_quality_gate.py"))


def test_quality_check_manifest_contains_all_required_checks():
    assert [name for name, _ in MODULE["CHECKS"]] == [
        "pytest", "ruff", "catalog", "atlas", "evidence", "capabilities",
    ]


def test_exact_head_is_required_before_any_subprocess(monkeypatch):
    invoked = []
    fn = MODULE["run_gate"]
    monkeypatch.setitem(fn.__globals__, "_git", lambda *args: invoked.append(args))
    for bad in ("abc", "A" * 40, "a" * 39, "a" * 41, ""):
        with pytest.raises(ValueError, match="exact full"):
            fn(bad)
    assert not invoked


def test_wrong_or_dirty_head_refuses_before_running_any_check(monkeypatch):
    fn = MODULE["run_gate"]
    head = "a" * 40
    monkeypatch.setitem(fn.__globals__, "_git", lambda *a: "b" * 40)
    with pytest.raises(ValueError, match="HEAD changed"):
        fn(head)
    monkeypatch.setitem(fn.__globals__, "_git", lambda *a: head if a[0] == "rev-parse" else " M x.py")
    with pytest.raises(ValueError, match="dirty"):
        fn(head)


def test_success_receipt_does_not_claim_github_actions_passed(monkeypatch):
    fn = MODULE["run_gate"]
    head = "a" * 40
    monkeypatch.setitem(fn.__globals__, "_git", lambda *a: head if a[0] == "rev-parse" else "")
    calls = []

    def runner(command, **kwargs):
        calls.append((command, kwargs))
        return CompletedProcess(command, 0)

    monkeypatch.setattr(fn.__globals__["subprocess"], "run", runner)
    result = fn(head)
    assert result["passed"] is True
    assert result["status"] == "local_gate_passed_not_official_ci"
    assert result["official_github_actions_status"] == "not_checked_by_this_script"
    assert result["head_sha"] == head
    assert len(calls) == 6
    assert all(c[1]["cwd"] == fn.__globals__["ROOT"] for c in calls)


def test_first_failure_stops_checks_and_receipt_stays_failed(monkeypatch):
    fn = MODULE["run_gate"]
    monkeypatch.setitem(fn.__globals__, "_git", lambda *a: "a" * 40 if a[0] == "rev-parse" else "")
    monkeypatch.setattr(
        fn.__globals__["subprocess"], "run",
        lambda command, **kwargs: CompletedProcess(command, 1),
    )
    result = fn("a" * 40)
    assert result["passed"] is False
    assert result["status"] == "local_gate_failed_or_incomplete"
    assert result["checks"] == [{"check": "pytest", "exit_code": 1}]


def test_check_timeout_is_failure_and_never_runs_later_checks(monkeypatch):
    fn = MODULE["run_gate"]
    monkeypatch.setitem(fn.__globals__, "_git", lambda *a: "a" * 40 if a[0] == "rev-parse" else "")

    def timeout(command, **kwargs):
        raise TimeoutExpired(command, timeout=900)

    monkeypatch.setattr(fn.__globals__["subprocess"], "run", timeout)
    result = fn("a" * 40)
    assert result["passed"] is False
    assert result["checks"] == [{"check": "pytest", "exit_code": 124}]
