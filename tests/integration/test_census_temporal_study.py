"""Reproducibility and causal input boundaries of the temporal study."""

import copy
from fractions import Fraction as F

import pytest

from examples import m1_census_temporal_study as s
from mirrormind.domains.retail.census_temporal_models import predict_temporal_models

REV = "f0a496c93b93c1b46573abdaf7dfc8ce900c627e"


@pytest.fixture(scope="module")
def report():
    return s.execute_study(REV, s.prepare_study(REV)["study_sha256"])


def test_temporal_study_exact_replay(report):
    identity = s.prepare_study(REV)["study_sha256"]
    assert identity == "f2ea85a6a066ab5fda21a9786bf70cbe92ffaf02c884d9cf526720cb90ec42e3"
    assert (
        report["report_sha256"]
        == "a78ebecd761ec9e96bcf1778a36a89e3075ae80ec545b60945fb84cf0d309680"
    )
    assert s.verify_study(REV, identity, s.canonical(report)) == report["report_sha256"]
    assert report["winner"] is report["confidence_interval"] is None
    assert report["causal_effect_established"] is report["calibration_verified"] is False
    assert report["holdout_executed"] is report["forecast_eligible"] is False
    count = 0
    assert len(report["groups"]) == 4
    for group in report["groups"]:
        assert len(group["event_transcript_sha256"]) == 64
        assert len(group["rows"]) == 15
        for h in s.HORIZONS:
            rows = {r["model"]: r for r in group["rows"] if r["horizon"] == h}
            assert set(rows) == set(s.MODELS)
            assert rows["oracle"]["reference_excess"] == "0"
            for row in rows.values():
                assert row["pairs"] == 160
                assert 0 <= F(row["joint_brier"]) <= 2
                assert F(row["reference_excess"]) >= 0
                count += row["pairs"]
    assert count == 9600


def test_temporal_study_rehashed_forgery(report):
    changed = copy.deepcopy(report)
    changed["groups"][0]["rows"][0]["joint_brier"] = "0"
    changed["report_sha256"] = s._sha({k: v for k, v in changed.items() if k != "report_sha256"})
    with pytest.raises(ValueError, match="differs from local replay"):
        s.verify_study(REV, report["study_sha256"], s.canonical(changed))


def test_temporal_commitment_precedes_scoring(monkeypatch):
    def forbidden(*args):
        pytest.fail("scored before commitment")

    monkeypatch.setattr(s, "_group", forbidden)
    with pytest.raises(ValueError, match="commitment mismatch"):
        s.execute_study(REV, "f" * 64)
    with pytest.raises(ValueError, match="bounded canonical"):
        s.verify_study(REV, "f" * 64, b"x" * (s.MAX_RECEIPT_BYTES + 1))
    assert s.prepare_study(REV)["status"] == "prepared_not_executed"


@pytest.mark.parametrize("h", s.HORIZONS)
def test_temporal_study_future_invariance(h):
    path = s._path("switch", 131004, 0)
    altered = path[:53] + ((4, 4),) * 11
    assert predict_temporal_models(path[29:53], h) == predict_temporal_models(altered[29:53], h)


def test_temporal_study_switch_boundary():
    prev = (-4, 4)
    assert s._row("switch", 52, prev) == s._row("cross", 52, prev)
    assert s._row("switch", 53, prev) == s._row("own", 53, prev)
    assert s._reference("switch", 52, 1, prev) == s._reference("own", 52, 1, prev)
    with pytest.raises(ValueError):
        s.prepare_study("invalid")
