"""Fixed probabilistic study identity, replay and causal inputs."""
import json
from fractions import Fraction

import pytest

from examples import m1_census_probability_study as study

REV = "5d8b8bfec1c2d9cca90be83ea37271b05b1ddcd7"


def test_study_identity_and_complete_replay():
    prepared = study.prepare_study(REV)
    expected = prepared["study_sha256"]
    assert expected == "e0cd7cb226cc77292480635b62c2faf8bb437f34996e0656107c11becb7bf4d0"
    assert prepared["status"] == "prepared_not_executed"
    report = study.execute_study(REV, expected)
    assert study.verify_study(REV, expected, study.canonical(report)) == report["report_sha256"]
    assert report["report_sha256"] == "0158324ee8f8bc926638bd94c03fd6b22b3e8438b9311255c633f53c1d9346b1"
    assert report["winner"] is report["confidence_interval"] is None
    assert report["calibration_verified"] is False
    assert report["holdout_executed"] is False
    assert len(report["groups"]) == 2
    for group in report["groups"]:
        assert len(group["rows"]) == 15
        assert all(row["pairs"] == 320 for row in group["rows"])
        assert len(group["event_transcript_sha256"]) == 64
        for row in group["rows"]:
            assert 0 <= Fraction(row["coverage"]) <= 1
            assert Fraction(row["crps"]) >= 0
    stationary = report["groups"][0]["rows"]
    for h in study.HORIZONS:
        fixed = next(r for r in stationary if r["horizon"] == h and r["model"] == "fixed")
        oracle = next(r for r in stationary if r["horizon"] == h and r["model"] == "oracle")
        assert dict(fixed, model="oracle") == oracle


def test_study_rejects_rehashed_forgery():
    expected = study.prepare_study(REV)["study_sha256"]
    report = study.execute_study(REV, expected)
    row = report["groups"][0]["rows"][0]
    assert "crps" in row
    row["crps"] = str(Fraction(row["crps"]) + 1)
    report["report_sha256"] = study._sha({
        k: v for k, v in report.items() if k != "report_sha256"
    })
    with pytest.raises(ValueError, match="differs from local replay"):
        study.verify_study(REV, expected, study.canonical(report))


def test_study_mismatch_before_scoring(monkeypatch):
    def forbidden(*args):
        pytest.fail("uncommitted design reached scoring")
    monkeypatch.setattr(study, "_group", forbidden)
    with pytest.raises(ValueError, match="commitment mismatch"):
        study.execute_study(REV, "f" * 64)
    with pytest.raises(ValueError, match="commitment mismatch"):
        study.execute_study("a" * 40, study.prepare_study(REV)["study_sha256"])
    with pytest.raises(ValueError, match="bounded canonical"):
        study.verify_study(REV, "f" * 64, b"x" * (study.MAX_RECEIPT_BYTES + 1))


def test_study_future_invariance():
    path = study._path("variance_shift", 61002, 0)
    changed = path[:53] + (24,) * 11
    assert path != changed
    for h in study.HORIZONS:
        assert study._candidates(path[29:53], h) == study._candidates(changed[29:53], h)
    assert len(path) == 64


def test_study_cli_prepare_does_not_score(monkeypatch, capsys):
    import sys

    def forbidden(*args):
        pytest.fail("prepare reached scoring")
    monkeypatch.setattr(study, "_group", forbidden)
    monkeypatch.setattr(sys, "argv", ["study", "prepare", "--revision", REV])
    assert study.main() == 0
    assert json.loads(capsys.readouterr().out)["status"] == "prepared_not_executed"
    monkeypatch.setattr(sys, "argv", ["study", "run", "--revision", REV])
    with pytest.raises(SystemExit) as exc:
        study.main()
    assert exc.value.code == 2
