"""Commitment and exact replay of the fixed persistent Bayesian study."""

import copy
from fractions import Fraction as F

import pytest

from examples import m1_census_network_bayes_study as s

REV = "94401e718a6dde8f19aa89b6ead148802bad6c3c"


@pytest.fixture(scope="module")
def report():
    return s.execute_study(REV, s.prepare_study(REV)["study_sha256"])


def test_persistent_study_exact_replay(report):
    identity = s.prepare_study(REV)["study_sha256"]
    assert identity == "404abf049b3cf6429add573f364c8bb79c6e40131235d39823806b25b2ef1fac"
    assert (
        report["report_sha256"]
        == "466b89606a00d78ab9c321c6123791e4db9082b228a8e9bd6e52d02bc59f33d4"
    )
    assert s.verify_study(REV, identity, s.canonical(report)) == report["report_sha256"]
    assert report["winner"] is report["confidence_interval"] is None
    assert report["causal_effect_established"] is report["forecast_eligible"] is False
    count = 0
    for g in report["groups"]:
        assert len(g["rows"]) == 24
        assert len(g["event_transcript_sha256"]) == 64
        for row in g["rows"]:
            assert row["pairs"] == 12
            count += row["pairs"]
            assert 0 <= F(row["joint_brier"]) <= 2
            assert F(row["reference_excess"]) >= 0
            if row["model"] == "oracle":
                assert row["reference_excess"] == "0"
        for length in s.WINDOWS:
            rows = {
                r["model"]: r for r in g["rows"] if r["history"] == length and r["horizon"] == 1
            }
            assert all(rows["integrated"][f] == rows["frozen"][f] for f in s.FIELDS)
    assert count == 1152


def test_persistent_study_rehashed_forgery(report):
    forged = copy.deepcopy(report)
    forged["groups"][0]["rows"][0]["joint_brier"] = "0"
    forged["report_sha256"] = s._sha({k: v for k, v in forged.items() if k != "report_sha256"})
    with pytest.raises(ValueError, match="differs from local replay"):
        s.verify_study(REV, report["study_sha256"], s.canonical(forged))


def test_persistent_study_precommitment(monkeypatch):
    def forbidden(*args):
        pytest.fail("scoring before commitment")

    monkeypatch.setattr(s, "_group", forbidden)
    with pytest.raises(ValueError, match="commitment mismatch"):
        s.execute_study(REV, "f" * 64)
    with pytest.raises(ValueError, match="bounded canonical"):
        s.verify_study(REV, "f" * 64, b"x" * (s.MAX_RECEIPT_BYTES + 1))
    assert s.prepare_study(REV)["status"] == "prepared_not_executed"


def test_persistent_study_switch():
    assert s._matrix("switch", 52) == s._matrix("ring", 52)
    assert s._matrix("switch", 53) == s._matrix("own", 53)
