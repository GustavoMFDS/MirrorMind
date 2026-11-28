import hashlib
import json
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal
from fractions import Fraction as F

import pytest

from examples.m1_census_model_comparison import BREAK, CATALOG, fixture, run_catalog
from mirrormind.domains.retail import census_models as m
from mirrormind.domains.retail.census_evaluation import CENSUS_HORIZONS_MONTHS
from mirrormind.domains.retail.census_experiment import prepare_census_experiment

REV = "19cc3b72c41942fc1e354f6152576dde83c2d33d"


def commitment(rows, plan):
    spec = prepare_census_experiment(rows, plan=plan, declared_code_revision=REV)
    return spec, m.census_model_comparison_sha256(spec)


def compare(rows, plan, scenario):
    spec, expected = commitment(rows, plan)
    return m.compare_census_models(
        rows,
        plan=plan,
        spec=spec,
        expected_comparison_sha256=expected,
        declared_code_revision=REV,
    )


def scenario_compare(scenario):
    rows, plan = fixture(scenario)
    return compare(rows, plan, scenario)


def canonical(payload):
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


from examples.m1_census_research_runner import SCENARIOS, build_fixture


def test_five_model_flat():
    for h in CENSUS_HORIZONS_MONTHS:
        assert set(m.predict_census_models((F(150),) * 13, h).values()) == {F(150)}


@pytest.mark.parametrize("h", [1, 3, 6])
def test_exact_linear_oracle(h):
    history = tuple(F(10 + 3 * i) for i in range(13))
    p = m.predict_census_models(history, h)
    assert p["seasonal_naive_lag12"] == 10 + 3 * h
    assert p["trailing_12_month_mean"] == F(59, 2)
    assert p["persistence"] == 46
    assert p["seasonal_drift_floor_zero"] == 46 + 3 * h
    assert p["linear_trend12_floor_zero"] == 46 + 3 * h


def test_floor():
    history = tuple(F(12 - i) for i in range(13))
    assert m.predict_census_models(history, 6)["linear_trend12_floor_zero"] == 0
    assert m.predict_census_models(history, 6)["seasonal_drift_floor_zero"] == 0


@pytest.mark.parametrize(
    "history,h",
    [
        ((F(1),) * 12, 1),
        ((F(-1),) * 13, 1),
        ((1,) * 13, 1),
        ((F(1),) * 13, True),
        ((F(1),) * 13, 2),
    ],
)
def test_invalid(history, h):
    with pytest.raises(ValueError):
        m.predict_census_models(history, h)


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_common_sample_and_determinism(scenario):
    a = scenario_compare(scenario)
    rows, plan = build_fixture(scenario)
    assert a == compare(rows[::-1], plan, scenario)
    assert len(a["paired"]) == 30
    assert a["split"] == "validation"
    assert a["winner"] is a["confidence_interval"] is None
    assert a["inference_status"] == "abstained"
    for h in a["horizons"]:
        assert h["common_scored"] == h["legacy_scored"] == 10
        assert h["coverage"] == 1
        assert set(h["mae_exact"]) == set(m.MODELS)
    assert (
        a["comparison_sha256"]
        == hashlib.sha256(
            canonical({k: v for k, v in a.items() if k != "comparison_sha256"})
        ).hexdigest()
    )


def test_future_revision_does_not_change_earlier_predictions():
    rows, plan = build_fixture()
    base = compare(rows, plan, "fixture")
    r = rows[47]
    revision = replace(
        r,
        value=Decimal(999),
        published_on=rows[53].published_on,
        release_kind="monthly_revision",
        release_id="fictional-late-revision",
        snapshot_sha256="f" * 64,
    )
    changed = compare(rows + (revision,), plan, "fixture")
    cutoff = revision.published_on.isoformat()
    early = [p for p in base["paired"] if p["issue"] <= cutoff]
    assert early and early == [p for p in changed["paired"] if p["issue"] <= cutoff]
    assert base["input_manifest_sha256"] != changed["input_manifest_sha256"]


def test_target_not_feature():
    rows, plan = build_fixture()
    a = compare(rows, plan, "fixture")
    # Last target month of validation is never a feature in validation.
    changed = list(rows)
    changed[63] = replace(changed[63], value=changed[63].value + Decimal(10))
    b = compare(tuple(changed), plan, "fixture")
    x = {(p["origin"], p["horizon"]): p for p in a["paired"]}
    y = {(p["origin"], p["horizon"]): p for p in b["paired"]}
    assert x.keys() == y.keys()
    assert all(
        x[k] == y[k] for k in x if x[k]["target_month"] != rows[63].reference_month.isoformat()
    )
    assert all(x[k]["forecasts"] == y[k]["forecasts"] for k in x)
    assert a["comparison_sha256"] != b["comparison_sha256"]


def test_extra_history_abstention_shared_across_models():
    from mirrormind.domains.retail.census_evaluation import CensusForecastOrigin

    rows, plan = build_fixture()
    indices = (12, 13, 14, 15, 16, 17, 36, 37, 50, 51)
    plan = replace(
        plan,
        origins=tuple(
            CensusForecastOrigin(rows[i].reference_month, rows[i].published_on + timedelta(days=1))
            for i in indices
        ),
    )
    result = compare(rows[:24] + rows[25:], plan, "fictional-missing-extra-month")
    assert len(result["paired"]) == 3
    for h in result["horizons"]:
        assert h["legacy_scored"] == 2 and h["common_scored"] == 1
        assert h["extra_history_abstentions"] == 1
        assert h["coverage"] == 0.5
        assert set(h["mae_exact"].values()) == {None}
        assert set(h["mean_loss_difference_vs_seasonal_exact"].values()) == {None}


def test_exact_differences_match_common_sample():
    for scenario in SCENARIOS:
        for h in scenario_compare(scenario)["horizons"]:
            for model, value in h["mae_exact"].items():
                assert F(h["mean_loss_difference_vs_seasonal_exact"][model]) == (
                    F(value) - F(h["mae_exact"][m.MODELS[0]])
                )


def test_model_commitment_and_receipt_replay():
    rows, plan = fixture(BREAK)
    spec, expected = commitment(rows, plan)
    result = compare(rows, plan, BREAK)
    assert (
        m.verify_census_model_comparison(
            rows[::-1],
            plan=plan,
            spec=spec,
            expected_comparison_sha256=expected,
            declared_code_revision=REV,
            submitted=canonical(result),
        )
        == result["comparison_sha256"]
    )
    result["winner"] = "persistence"
    result["comparison_sha256"] = hashlib.sha256(
        canonical({k: v for k, v in result.items() if k != "comparison_sha256"})
    ).hexdigest()
    with pytest.raises(ValueError, match="does not match"):
        m.verify_census_model_comparison(
            rows,
            plan=plan,
            spec=spec,
            expected_comparison_sha256=expected,
            declared_code_revision=REV,
            submitted=canonical(result),
        )


def test_model_mismatches_reject_before_scoring(monkeypatch):
    rows, plan = fixture(BREAK)
    spec, expected = commitment(rows, plan)

    def forbidden(*args, **kwargs):
        pytest.fail("changed commitment reached scoring")

    monkeypatch.setattr(m, "evaluate_frozen_census_split", forbidden)
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        m.compare_census_models(
            rows,
            plan=plan,
            spec=spec,
            expected_comparison_sha256="f" * 64,
            declared_code_revision=REV,
        )
    with pytest.raises(ValueError, match="inputs differ"):
        m.compare_census_models(
            (replace(rows[0], value=Decimal(999)),) + rows[1:],
            plan=plan,
            spec=spec,
            expected_comparison_sha256=expected,
            declared_code_revision=REV,
        )


def test_validation_break_catalog_and_replay():
    report = run_catalog(REV)
    assert report == run_catalog(REV)
    assert len(report["reports"]) == len(CATALOG) == 5
    assert report["split"] == "validation"
    assert all(r["local_replay_matched"] for r in report["reports"])
    assert len({r["comparison_commitment_sha256"] for r in report["reports"]}) == 5
    rows, plan = fixture(BREAK)
    a = compare(rows, plan, BREAK)
    before = [p for p in a["paired"] if p["origin"] < rows[53].reference_month.isoformat()]
    assert any(p["target_month"] >= rows[53].reference_month.isoformat() for p in before)
    assert all(set(p["forecasts"].values()) == {"150"} for p in before)
    assert a["horizons"][2]["mae_exact"]["seasonal_naive_lag12"] == "80"
    assert a["horizons"][2]["mae_exact"]["persistence"] == "40"


def test_model_fraction_bound_and_receipt_bound():
    with pytest.raises(ValueError, match="bounded"):
        m.predict_census_models((F(1 << 2048),) * 13, 1)
    rows, plan = fixture(BREAK)
    spec, expected = commitment(rows, plan)
    with pytest.raises(ValueError, match="bounded canonical"):
        m.verify_census_model_comparison(
            rows,
            plan=plan,
            spec=spec,
            expected_comparison_sha256=expected,
            declared_code_revision=REV,
            submitted=b"x" * (m.MAX_MODEL_RECEIPT_BYTES + 1),
        )
