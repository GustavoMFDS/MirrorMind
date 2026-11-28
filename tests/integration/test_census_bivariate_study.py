"""Exact bivariate study replay and commitment regressions."""

from fractions import Fraction as F

import pytest

from examples import m1_census_bivariate_study as s
from mirrormind.domains.retail.census_bivariate import joint_marginal

REV = "dd63db4d7186b873c27151a2ac4702a648966ec5"


@pytest.fixture(scope="module")
def report():
    identity = s.prepare_study(REV)["study_sha256"]
    return s.execute_study(REV, identity)


def test_bivariate_study_exact_replay_and_matched_marginals(report):
    identity = s.prepare_study(REV)["study_sha256"]
    assert identity == "86e4ae0c05b2a41f5b423fe8e7a7c616b9835e19d5e0b2effd0f619ba91b2a9b"
    assert (
        report["report_sha256"]
        == "56e342dafd510883273e72cc6dc2563b6d2a6e969b8438cb331e98f76a432420"
    )
    assert s.verify_study(REV, identity, s.canonical(report)) == report["report_sha256"]
    assert report["winner"] is report["confidence_interval"] is None
    assert report["calibration_verified"] is report["holdout_executed"] is False
    count = 0
    for group in report["groups"]:
        assert len(group["event_transcript_sha256"]) == 64
        assert len(group["rows"]) == 12
        for h in s.HORIZONS:
            rows = {r["model"]: r for r in group["rows"] if r["horizon"] == h}
            assert len(rows) == 4
            assert rows["oracle"]["reference_excess"] == "0"
            for field in ("marginal_crps_x", "marginal_crps_y"):
                assert rows["joint24"][field] == rows["product24"][field]
            for row in rows.values():
                assert row["pairs"] == 160
                assert 0 <= F(row["joint_brier"]) <= 2
                assert F(row["reference_excess"]) >= 0
                count += row["pairs"]
    assert count == 7680


def test_bivariate_forgery_rejected(report):
    import copy

    changed = copy.deepcopy(report)
    changed["groups"][0]["rows"][0]["joint_brier"] = "0"
    changed["report_sha256"] = s._sha({k: v for k, v in changed.items() if k != "report_sha256"})
    with pytest.raises(ValueError, match="differs from local replay"):
        s.verify_study(REV, report["study_sha256"], s.canonical(changed))


def test_bivariate_commitment_before_scoring(monkeypatch):
    def forbidden(*args):
        pytest.fail("uncommitted study scored")

    monkeypatch.setattr(s, "_group", forbidden)
    with pytest.raises(ValueError, match="commitment mismatch"):
        s.execute_study(REV, "f" * 64)
    with pytest.raises(ValueError, match="bounded canonical"):
        s.verify_study(REV, "f" * 64, b"x" * (s.MAX_RECEIPT_BYTES + 1))
    assert s.prepare_study(REV)["status"] == "prepared_not_executed"


@pytest.mark.parametrize("h", s.HORIZONS)
def test_bivariate_future_invariance(h):
    path = s._path("shift", 111004, 0)
    changed = path[:53] + ((4, 4),) * 11
    p = s._candidates(path[29:53], h)
    assert p == s._candidates(changed[29:53], h)
    for axis in (0, 1):
        assert joint_marginal(p["joint24"], axis) == joint_marginal(p["product24"], axis)


def test_bivariate_invalid_inputs():
    with pytest.raises(ValueError):
        s.prepare_study("invalid")
    with pytest.raises(ValueError):
        s._candidates(((0, 0),) * 24, 1)
    with pytest.raises(ValueError):
        s._candidates(((4, 4),) * 24, True)
