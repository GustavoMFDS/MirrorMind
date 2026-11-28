from dataclasses import replace
from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest

from mirrormind.domains.retail.census_evaluation import CensusForecastOrigin
from mirrormind.domains.retail.census_split import (
    CensusOriginSchedule,
    census_schedule_sha256,
    evaluate_frozen_census_split,
)
from mirrormind.domains.retail.census_vintages import CensusVintageRecord


def month(i: int) -> date:
    return date(2000 + i // 12, i % 12 + 1, 1)


def origin(i: int) -> CensusForecastOrigin:
    return CensusForecastOrigin(month(i), month(i + 1) + timedelta(days=1))


def schedule() -> CensusOriginSchedule:
    return CensusOriginSchedule("RSAFS", tuple(
        origin(i) for i in (12, 13, 14, 15, 16, 17, 24, 25, 32, 33)
    ))


def records() -> tuple[CensusVintageRecord, ...]:
    return tuple(
        CensusVintageRecord(
            "RSAFS", month(i), Decimal(100 + i), month(i + 1),
            "first_estimate", f"fictional-{i}", f"{i:064x}",
        )
        for i in range(40)
    )


def evaluate(plan, rows=None, *, split="holdout", digest=None):
    return evaluate_frozen_census_split(
        records() if rows is None else rows,
        plan=plan, expected_schedule_sha256=(
            census_schedule_sha256(plan) if digest is None else digest
        ), split=split,
    )


def test_frozen_split_binds_schedule_and_preserves_abstention():
    plan = schedule()
    a = evaluate(plan)
    b = evaluate(plan, records()[::-1])
    assert a == b
    assert a["split_sizes"] == (6, 2, 2)
    assert a["schedule_digest_matched"] is True
    assert a["registration_verified"] is a["holdout_lock_verified"] is False
    assert a["inference_status"] == "abstained"
    result = a["evaluation"]
    assert result["confidence_interval"] is result["winner"] is None
    assert len(result["paired_losses"]) == 6
    assert {r["reference_month"] for r in result["paired_losses"]} == {
        month(32).isoformat(), month(33).isoformat()
    }
    v = evaluate(plan, split="validation")
    assert v["schedule_sha256"] == a["schedule_sha256"]
    assert v["receipt_sha256"] != a["receipt_sha256"]
    assert {r["reference_month"] for r in v["evaluation"]["paired_losses"]} == {
        month(24).isoformat(), month(25).isoformat()
    }


def test_frozen_split_rejects_schedule_mutation_before_scoring(monkeypatch):
    p = schedule()
    digest = census_schedule_sha256(p)
    altered = replace(p, origins=p.origins[:-1] + (origin(34),))

    def forbidden(*args, **kwargs):
        pytest.fail("scoring should not be reached")

    monkeypatch.setattr(
        "mirrormind.domains.retail.census_split.evaluate_census_vintage_descriptive",
        forbidden,
    )
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        evaluate(altered, digest=digest)


def test_frozen_split_rejects_overlap_and_invalid_schedule():
    p = schedule()
    for bad in (
        replace(p, origins=tuple(origin(i) for i in range(12, 22))),
        replace(p, origins=p.origins[::-1]),
        replace(p, origins=p.origins[:-1] + (p.origins[-2],)),
        replace(p, origins=p.origins[:9]),
        replace(p, origins=tuple(origin(i) for i in range(251))),
        replace(p, origins=(replace(p.origins[0], issued_on=month(12)),) + p.origins[1:]),
        replace(p, origins=(replace(p.origins[0], issued_on=datetime(2001, 3, 1)),) + p.origins[1:]),
        replace(p, series_id="invalid series"),
    ):
        with pytest.raises(ValueError):
            census_schedule_sha256(bad)


@pytest.mark.parametrize("split", ["validation", "holdout"])
def test_frozen_split_rejects_late_same_day_and_missing_prior_labels(split):
    p = schedule()
    rows = records()
    for changed in (
        rows[:23] + rows[24:],
        rows[:23] + (replace(rows[23], published_on=month(25) + timedelta(days=1)),) + rows[24:],
        rows[:23] + (replace(rows[23], published_on=month(27)),) + rows[24:],
    ):
        with pytest.raises(ValueError, match="cross-split target publication"):
            evaluate(p, changed, split=split)


def test_frozen_split_digest_changes_on_issue_date_and_rejects_invalid_split():
    p = schedule()
    altered = replace(p, origins=(replace(
        p.origins[0], issued_on=date(2001, 2, 3)
    ),) + p.origins[1:])
    assert census_schedule_sha256(p) != census_schedule_sha256(altered)
    with pytest.raises(ValueError, match="invalid evaluation split"):
        evaluate(p, split="development")
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        evaluate(p, digest="0" * 64)
