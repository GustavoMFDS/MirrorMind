import hashlib
import json
from dataclasses import replace
from datetime import date, timedelta
from decimal import Decimal, localcontext

import pytest

from mirrormind.domains.retail.census_evaluation import (
    CensusForecastOrigin,
    census_evaluation_manifest_sha256,
)
from mirrormind.domains.retail.census_experiment import (
    MAX_CENSUS_RECEIPT_BYTES,
    census_experiment_sha256,
    execute_census_experiment,
    prepare_census_experiment,
    verify_census_experiment_receipt,
)
from mirrormind.domains.retail.census_split import CensusOriginSchedule
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

REV = "c1aee53224d8604bf22e9be28334443f68847707"


def month(i):
    return date(2000 + i // 12, i % 12 + 1, 1)


def fixture():
    rows = tuple(
        CensusVintageRecord(
            "RSAFS", month(i), Decimal(100 + i), month(i + 1),
            "first_estimate", f"fictional-{i}", f"{i:064x}",
        )
        for i in range(40)
    )
    plan = CensusOriginSchedule("RSAFS", tuple(
        CensusForecastOrigin(month(i), month(i + 1) + timedelta(days=1))
        for i in (12, 13, 14, 15, 16, 17, 24, 25, 32, 33)
    ))
    spec = prepare_census_experiment(rows, plan=plan, declared_code_revision=REV)
    return rows, plan, spec, census_experiment_sha256(spec)


def execute(rows, plan, spec, expected, split="holdout", revision=REV):
    return execute_census_experiment(
        rows, plan=plan, spec=spec, expected_experiment_sha256=expected,
        split=split, declared_code_revision=revision,
    )


def encode(receipt):
    return json.dumps(receipt, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def verify(rows, plan, spec, expected, submitted, split="holdout"):
    return verify_census_experiment_receipt(
        rows, plan=plan, spec=spec, expected_experiment_sha256=expected,
        split=split, declared_code_revision=REV, submitted=submitted,
    )


def test_experiment_commitment_and_complete_replay():
    rows, plan, spec, expected = fixture()
    a = execute(rows, plan, spec, expected)
    b = execute(rows, plan, spec, expected, "validation")
    assert a == execute(rows[::-1], plan, spec, expected)
    assert a["experiment_sha256"] == b["experiment_sha256"] == expected
    assert a["receipt_sha256"] != b["receipt_sha256"]
    assert verify(rows, plan, spec, expected, encode(a)) == a["receipt_sha256"]
    assert a["inference_status"] == "abstained"
    for key in ("registration_verified", "holdout_lock_verified", "runtime_code_attested",
                "forecast_eligible", "ingestion_authorized", "action_authorized"):
        assert a[key] is False
    assert spec.input_manifest_sha256 == (
        a["evaluation"]["evaluation"]["evaluation"]["input_manifest_sha256"]
    )


@pytest.mark.parametrize("change", ["value", "date", "release", "snapshot", "missing", "schedule", "code"])
def test_experiment_rejects_changed_inputs_before_evaluation(change, monkeypatch):
    rows, plan, spec, expected = fixture()
    revision = REV

    def forbidden(*args, **kwargs):
        pytest.fail("changed commitment reached scoring")

    monkeypatch.setattr(
        "mirrormind.domains.retail.census_experiment.evaluate_frozen_census_split", forbidden
    )
    if change == "value":
        rows = (replace(rows[0], value=Decimal(99)),) + rows[1:]
    elif change == "date":
        rows = (replace(rows[0], published_on=month(1) + timedelta(days=1)),) + rows[1:]
    elif change == "release":
        rows = (replace(rows[0], release_id="changed"),) + rows[1:]
    elif change == "snapshot":
        rows = (replace(rows[0], snapshot_sha256="f" * 64),) + rows[1:]
    elif change == "missing":
        rows = rows[:-1]
    elif change == "schedule":
        plan = replace(plan, origins=plan.origins[:-1] + (
            replace(plan.origins[-1], issued_on=plan.origins[-1].issued_on + timedelta(days=1)),
        ))
    else:
        revision = "f" * 40
    with pytest.raises(ValueError, match="inputs differ"):
        execute(rows, plan, spec, expected, revision=revision)


@pytest.mark.parametrize("change", ["authority", "loss", "split", "extra"])
def test_experiment_rejects_rehashed_forgery(change):
    rows, plan, spec, expected = fixture()
    receipt = execute(rows, plan, spec, expected)
    if change == "authority":
        receipt["holdout_lock_verified"] = True
    elif change == "loss":
        receipt["evaluation"]["evaluation"]["paired_losses"][0]["paired_loss_difference"] = "999"
    elif change == "split":
        receipt["split"] = "validation"
    else:
        receipt["extra"] = True
    receipt["receipt_sha256"] = hashlib.sha256(encode({
        k: v for k, v in receipt.items() if k != "receipt_sha256"
    })).hexdigest()
    with pytest.raises(ValueError, match="does not match"):
        verify(rows, plan, spec, expected, encode(receipt))


@pytest.mark.parametrize("submitted", [b"", b"{}", b"x" * (MAX_CENSUS_RECEIPT_BYTES + 1), "bad"])
def test_experiment_rejects_invalid_receipt(submitted):
    rows, plan, spec, expected = fixture()
    with pytest.raises(ValueError):
        verify(rows, plan, spec, expected, submitted)


def test_experiment_manifest_context_and_validation():
    rows, plan, spec, expected = fixture()
    rows = (replace(rows[0], value=Decimal("1E+2")),) + rows[1:]
    with localcontext() as context:
        context.capitals = 0
        a = prepare_census_experiment(rows, plan=plan, declared_code_revision=REV)
    with localcontext() as context:
        context.capitals = 1
        b = prepare_census_experiment(rows[::-1], plan=plan, declared_code_revision=REV)
    assert a == b
    with pytest.raises(ValueError):
        census_evaluation_manifest_sha256(
            (replace(rows[0], value=Decimal("1E+151")),) + rows[1:],
            series_id="RSAFS", cutoff=plan.origins[0].issued_on,
        )
    with pytest.raises(ValueError):
        execute(rows, plan, spec, "f" * 64)
    with pytest.raises(ValueError):
        execute(rows, plan, spec, expected, "development")
