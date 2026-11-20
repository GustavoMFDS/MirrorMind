"""Synthetic prequential envelope tests: no hindsight or calibrated claims."""
import random
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.residual_envelope import evaluate_retail_residual_envelopes
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(index):
    return START + timedelta(days=index - 1)


def fixture(*, late60=False, value60=4, missing68=False, withheld70=False):
    rows = []
    releases = []
    for index in range(1, 71):
        if missing68 and index == 68:
            continue
        event = day(index)
        units = value60 if index == 60 else (index % 7) + 1
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "PRIVATE-SKU",
            "InvoiceDate": datetime(event.year, event.month, event.day, 10),
            "Quantity": units,
            "CustomerID": "NEVER-COPY",
        })
        published = (
            day(70) if late60 and index == 60
            else day(71) if withheld70 and index == 70
            else event
        )
        releases.append(DeclaredProductRelease("PRIVATE-SKU", event, published))
    return project_uci_retail_rows(rows), tuple(releases)


def evaluate(projection, releases, **kwargs):
    return evaluate_retail_residual_envelopes(
        projection, releases, stock_code="PRIVATE-SKU",
        evaluation_on=day(70), **kwargs,
    )


def test_fully_published_example_reports_retrospective_not_nominal_coverage():
    projection, releases = fixture()
    result = evaluate(projection, releases)
    assert result["evaluated_origins"] == 7
    assert result["retrospective_coverage_denominator"] == 7
    assert 0 <= result["retrospective_covered_origins"] <= 7
    assert result["calibrated_prediction_interval"] is None
    assert result["nominal_coverage"] is None
    assert result["uncertainty_status"] == "heuristic_envelope_not_prediction_interval"
    assert len(result["origin_audit"]) == result["requested_origins"] == 7
    for forbidden in ("PRIVATE-SKU", "NEVER-COPY", "500001"):
        assert forbidden not in str(result)


def test_delayed_historical_value_is_unavailable_for_forecast_and_calibration():
    first, releases = fixture(late60=True, value60=4, withheld70=True)
    changed, other_releases = fixture(late60=True, value60=999_999, withheld70=True)
    assert releases == other_releases
    initial = evaluate(first, releases)
    mutated = evaluate(changed, other_releases)
    assert initial == mutated
    assert initial["evaluated_origins"] == 2
    assert initial["abstained_forecast_history"] == 4
    assert initial["abstained_unpublished_target"] == 1
    assert initial["retrospective_coverage_denominator"] == 2
    assert initial["calibrated_prediction_interval"] is None


def test_calibration_abstains_instead_of_claiming_small_sample_uncertainty():
    projection, releases = fixture(late60=True)
    result = evaluate(
        projection, releases, holdout_days=2,
        calibration_days=10, min_calibration_residuals=10,
    )
    assert result["evaluated_origins"] == 0
    assert result["abstained_calibration"] == 2
    assert result["retrospective_coverage_denominator"] == 0
    assert result["calibrated_prediction_interval"] is None


def test_missing_target_is_not_zero_and_never_in_denominator():
    projection, releases = fixture(missing68=True)
    result = evaluate(projection, releases, holdout_days=3)
    assert result["abstained_missing_target"] == 1
    assert result["evaluated_origins"] <= 2
    assert any(row["status"] == "target_missing_not_zero"
               for row in result["origin_audit"])


def test_incomplete_release_declarations_fail_closed():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        evaluate(projection, releases[:-1])


@pytest.mark.parametrize("option,value,error", [
    ("holdout_days", True, "holdout_days"),
    ("holdout_days", 31, "holdout_days"),
    ("calibration_days", 61, "calibration_days"),
    ("calibration_days", 4, "calibration_days"),
    ("min_calibration_residuals", 2, "min_calibration_residuals"),
    ("min_calibration_residuals", 22, "min_calibration_residuals"),
])
def test_bounded_exact_configuration(option, value, error):
    projection, releases = fixture()
    with pytest.raises(ValueError, match=error):
        evaluate(projection, releases, **{option: value})


def test_datetime_is_not_accepted_as_calendar_date():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="exact date"):
        evaluate_retail_residual_envelopes(
            projection, releases, stock_code="PRIVATE-SKU",
            evaluation_on=datetime(2011, 3, 11),
        )


def test_each_distinct_prequential_target_prediction_runs_once(monkeypatch):
    """Seven origins with 21 calibration days need 28, not 154 predictions."""
    import mirrormind.domains.retail.residual_envelope as module

    projection, releases = fixture()
    expected = evaluate(projection, releases)
    original = module._predict
    calls = []

    def counting_predict(history):
        calls.append(history)
        return original(history)

    monkeypatch.setattr(module, "_predict", counting_predict)
    actual = evaluate(projection, releases)
    assert actual == expected
    assert len(calls) == 28
    assert actual["evaluated_origins"] == 7


def test_prediction_cache_is_never_shared_between_evaluation_calls(monkeypatch):
    """Call-local caching must not reuse forecasts at a subsequent cutoff."""
    import mirrormind.domains.retail.residual_envelope as module

    projection, releases = fixture()
    original = module._predict
    call_count = 0

    def counting_predict(history):
        nonlocal call_count
        call_count += 1
        return original(history)

    monkeypatch.setattr(module, "_predict", counting_predict)
    earlier = evaluate(projection, releases)
    assert call_count == 28
    later = evaluate(projection, releases)
    assert call_count == 56
    assert earlier == later


@pytest.mark.parametrize("variants", [
    {},
    {"late60": True, "withheld70": True},
    {"missing68": True},
    {"late60": True, "value60": 999_999},
])
def test_cached_residuals_remain_deterministic_with_missing_and_late_data(
    monkeypatch, variants
):
    import mirrormind.domains.retail.residual_envelope as module

    projection, releases = fixture(**variants)
    expected = evaluate(projection, releases)
    original = module._predict
    called = []

    def counting_predict(history):
        called.append(history)
        return original(history)

    monkeypatch.setattr(module, "_predict", counting_predict)
    result = evaluate(projection, releases)
    assert result == expected
    assert 0 <= len(called) <= 28
    assert result["requested_origins"] == len(result["origin_audit"]) == 7
    assert result["nominal_coverage"] is None
    assert result["calibrated_prediction_interval"] is None


def adversarial_fixture(seed):
    """Invented two-product histories with reproducible holes and publication delays."""
    rng = random.Random(seed)
    rows, releases = [], []
    for index in range(1, 85):
        event = day(index)
        for product, prefix in (("PRIVATE-SKU", 500000), ("SECONDARY-SKU", 800000)):
            if product == "PRIVATE-SKU" and seed % 6 and rng.randrange(13) == 0:
                continue
            if product == "PRIVATE-SKU":
                units = (index * 17 + seed * 23) % 41 + 1
                if index == 60 and seed % 3 == 2:
                    units = 999_999
                delay = 0 if seed == 0 else rng.randrange(seed % 6 + 1)
            else:
                units = 12
                delay = rng.randrange(5)
            rows.append({
                "InvoiceNo": str(prefix + index),
                "StockCode": product,
                "InvoiceDate": datetime(event.year, event.month, event.day, 9),
                "Quantity": units,
                "CustomerID": "MUST-NOT-ESCAPE",
            })
            releases.append(DeclaredProductRelease(product, event, event + timedelta(days=delay)))
    return project_uci_retail_rows(rows), tuple(releases)


@pytest.mark.parametrize("seed", range(6))
@pytest.mark.parametrize("evaluation_index,holdout,calibration,minimum", [
    (70, 7, 21, 5),
    (65, 10, 15, 4),
    (78, 14, 30, 8),
])
def test_cached_and_uncached_history_agree_under_adversarial_publication_schedules(
    monkeypatch, seed, evaluation_index, holdout, calibration, minimum,
):
    """An explicit uncached oracle guards reports, not just repeated cached calls."""
    import mirrormind.domains.retail.residual_envelope as module

    projection, releases = adversarial_fixture(seed)
    kwargs = {
        "stock_code": "PRIVATE-SKU",
        "evaluation_on": day(evaluation_index),
        "holdout_days": holdout,
        "calibration_days": calibration,
        "min_calibration_residuals": minimum,
    }
    with monkeypatch.context() as patch:
        patch.setattr(module, "cache", lambda function: function)
        uncached = module.evaluate_retail_residual_envelopes(projection, releases, **kwargs)
    cached = module.evaluate_retail_residual_envelopes(projection, releases, **kwargs)
    assert cached == uncached
    assert len(cached["origin_audit"]) == holdout
    assert cached["retrospective_coverage_denominator"] == cached["evaluated_origins"]
    assert cached["nominal_coverage"] is None
    assert cached["calibrated_prediction_interval"] is None
    for private in ("PRIVATE-SKU", "SECONDARY-SKU", "MUST-NOT-ESCAPE", "500001"):
        assert private not in str(cached)


def test_uncached_and_cached_full_history_predict_calls_match_exact_legacy_count(monkeypatch):
    """Rolling calibration needs 34 uncached calls or 28 with memoization."""
    import mirrormind.domains.retail.residual_envelope as module

    projection, releases = fixture()
    original = module._predict
    calls = {"uncached": 0, "cached": 0}

    def uncached_predict(history):
        calls["uncached"] += 1
        return original(history)

    def cached_predict(history):
        calls["cached"] += 1
        return original(history)

    with monkeypatch.context() as patch:
        patch.setattr(module, "cache", lambda function: function)
        patch.setattr(module, "_predict", uncached_predict)
        baseline = evaluate(projection, releases)

    with monkeypatch.context() as patch:
        patch.setattr(module, "_predict", cached_predict)
        optimized = evaluate(projection, releases)

    assert baseline == optimized
    assert calls == {"uncached": 34, "cached": 28}


def test_different_release_schedules_cannot_share_earlier_cached_predictions(monkeypatch):
    """Changed publisher assertions must be reflected in a new evaluation."""
    import mirrormind.domains.retail.residual_envelope as module

    projection, releases_early = fixture()
    other_projection, releases_late = fixture(late60=True, withheld70=True)
    assert projection == other_projection
    kwargs = {
        "stock_code": "PRIVATE-SKU",
        "evaluation_on": day(70),
    }
    normal = module.evaluate_retail_residual_envelopes(projection, releases_early, **kwargs)
    delayed = module.evaluate_retail_residual_envelopes(projection, releases_late, **kwargs)
    assert normal != delayed
    with monkeypatch.context() as patch:
        patch.setattr(module, "cache", lambda function: function)
        expected_normal = module.evaluate_retail_residual_envelopes(
            projection, releases_early, **kwargs
        )
        expected_delayed = module.evaluate_retail_residual_envelopes(
            projection, releases_late, **kwargs
        )
    assert normal == expected_normal
    assert delayed == expected_delayed
    assert delayed["abstained_unpublished_target"] == 1


def _naive_calibration_oracle(projection, releases, *, evaluation_on, holdout_days,
                              calibration_days, min_calibration_residuals):
    """Independent quadratic reference for the prequential report, test-only."""
    from mirrormind.modules.forecasting.baselines import _predict

    observed = {item.observed_on: item.units for item in projection.days
                if item.stock_code == "PRIVATE-SKU"}
    published = {(item.stock_code, item.observed_on): item.available_on for item in releases}

    def predict(target):
        origin = target - timedelta(days=1)
        history = tuple(origin - timedelta(days=offset) for offset in range(6, -1, -1))
        if any(date_on not in observed
               or published[("PRIVATE-SKU", date_on)] > origin
               for date_on in history):
            return None
        return _predict(tuple(observed[d] for d in history))["seasonal_naive_lag7"]

    start = evaluation_on - timedelta(days=holdout_days - 1)
    audit = []
    covered = 0
    for offset in range(holdout_days):
        target = start + timedelta(days=offset)
        origin = target - timedelta(days=1)
        prefix = {"target_on": target.isoformat(), "origin_on": origin.isoformat()}
        if target not in observed:
            status = "target_missing_not_zero"
        elif published[("PRIVATE-SKU", target)] > evaluation_on:
            status = "target_unpublished_by_evaluation"
        else:
            point = predict(target)
            if point is None:
                status = "forecast_history_unavailable"
            else:
                residuals = []
                for lag in range(calibration_days, 0, -1):
                    previous = target - timedelta(days=lag)
                    if previous not in observed or published[("PRIVATE-SKU", previous)] > origin:
                        continue
                    previous_point = predict(previous)
                    if previous_point is not None:
                        residuals.append(abs(observed[previous] - previous_point))
                if len(residuals) < min_calibration_residuals:
                    status = "insufficient_published_residuals"
                else:
                    radius = max(residuals)
                    if max(0.0, point - radius) <= observed[target] <= point + radius:
                        covered += 1
                    status = "retrospective_envelope_evaluated"
        audit.append({**prefix, "status": status})
    return tuple(audit), covered


@pytest.mark.parametrize("seed", range(10))
@pytest.mark.parametrize("evaluation_index,holdout,calibration,minimum", [
    (70, 7, 21, 5),
    (65, 10, 15, 4),
    (78, 14, 30, 8),
    (83, 30, 60, 3),
])
def test_incremental_calibration_exactly_matches_naive_reference(
    seed, evaluation_index, holdout, calibration, minimum,
):
    """Include delayed and expired targets, incomplete history, and long windows."""
    projection, releases = adversarial_fixture(seed)
    cutoff = day(evaluation_index)
    report = evaluate_retail_residual_envelopes(
        projection, releases, stock_code="PRIVATE-SKU",
        evaluation_on=cutoff, holdout_days=holdout,
        calibration_days=calibration, min_calibration_residuals=minimum,
    )
    origin_audit, covered = _naive_calibration_oracle(
        projection, releases, evaluation_on=cutoff, holdout_days=holdout,
        calibration_days=calibration, min_calibration_residuals=minimum,
    )
    assert report["origin_audit"] == origin_audit
    assert report["evaluated_origins"] == sum(
        item["status"] == "retrospective_envelope_evaluated" for item in origin_audit
    )
    assert report["retrospective_covered_origins"] == covered
    assert report["retrospective_coverage_denominator"] == report["evaluated_origins"]
    assert report["nominal_coverage"] is None
    assert report["calibrated_prediction_interval"] is None


def test_later_publication_does_not_appear_early_even_when_value_changes():
    """Later release activation cannot rewrite a previous time-cutoff report."""
    projection, releases = fixture(late60=True, withheld70=True, value60=4)
    changed, unchanged_releases = fixture(
        late60=True, withheld70=True, value60=999_999,
    )
    assert releases == unchanged_releases
    for end in (day(64), day(66), day(68)):
        kwargs = {
            "stock_code": "PRIVATE-SKU", "evaluation_on": end,
            "holdout_days": 7, "calibration_days": 21,
        }
        initial = evaluate_retail_residual_envelopes(projection, releases, **kwargs)
        altered = evaluate_retail_residual_envelopes(changed, releases, **kwargs)
        assert initial == altered
        assert initial["nominal_coverage"] is None


def test_calibration_release_activates_at_exact_origin_not_one_day_earlier():
    """The pending residual is usable only after its declared release date."""
    projection, releases = fixture()
    delayed = tuple(
        DeclaredProductRelease(r.stock_code, r.observed_on, day(69))
        if r.observed_on == day(49) else r
        for r in releases
    )
    # The altered row's publication date is after its eligible window;
    # exact matching to the independent reference guards expiry semantics.
    for end in (day(67), day(68), day(69), day(70)):
        report = evaluate_retail_residual_envelopes(
            projection, delayed, stock_code="PRIVATE-SKU",
            evaluation_on=end, holdout_days=7,
            calibration_days=21, min_calibration_residuals=5,
        )
        audit, covered = _naive_calibration_oracle(
            projection, delayed, evaluation_on=end,
            holdout_days=7, calibration_days=21, min_calibration_residuals=5,
        )
        assert report["origin_audit"] == audit
        assert report["retrospective_covered_origins"] == covered
