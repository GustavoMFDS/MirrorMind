"""No-hindsight, monotone scenario-sweep regressions on invented rows."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta
from itertools import pairwise

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.selection_sensitivity import assess_excluded_target_sensitivity
from mirrormind.domains.retail.sensitivity_sweep import sweep_excluded_target_sensitivity
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(number):
    return START + timedelta(days=number - 1)


def fixture(*, missing82=False, missing80=False, late75=False, value75=75, late83=False):
    rows, releases = [], []
    for index in range(1, 85):
        if (missing80 and index == 80) or (missing82 and index == 82):
            continue
        event = day(index)
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "PRIVATE-SKU",
            "InvoiceDate": datetime(event.year, event.month, event.day, 10),
            "Quantity": value75 if index == 75 else index,
            "CustomerID": "DO-NOT-EXPOSE",
        })
        available = (
            day(78) if late75 and index == 75
            else day(85) if late83 and index == 83
            else event
        )
        releases.append(DeclaredProductRelease("PRIVATE-SKU", event, available))
    return project_uci_retail_rows(rows), tuple(releases)


def sweep(projection, releases, ceilings=(0, 100, 1000), **kwargs):
    return sweep_excluded_target_sensitivity(
        projection, releases, stock_code="PRIVATE-SKU", evaluation_on=day(84),
        ceilings=ceilings, **kwargs,
    )


def test_complete_windows_are_independent_of_assumed_ceiling():
    projection, releases = fixture()
    result = sweep(projection, releases)
    assert len(result.scenarios) == 3
    assert all(case.earlier_eligible == case.later_eligible == 7 for case in result.scenarios)
    assert all(case.difference_floor == case.difference_ceiling == 7 for case in result.scenarios)
    assert all(case.direction_status == "positive_under_declared_counterfactual_bounds_only"
               for case in result.scenarios)
    assert result.receipt()["statistical_guarantee"] is None
    receipt = str(result.receipt())
    for forbidden in ("PRIVATE-SKU", "DO-NOT-EXPOSE", "500001"):
        assert forbidden not in receipt
    with pytest.raises(FrozenInstanceError):
        result.scenarios = ()


def test_incomplete_windows_can_lose_direction_robustness_as_ceiling_increases():
    projection, releases = fixture(missing82=True, late75=True, late83=True)
    result = sweep(
        projection, releases, ceilings=(0, 100, 1000),
        minimum_eligible_per_window=2, minimum_coverage_percent=20,
    )
    cases = result.scenarios
    assert all(c.earlier_eligible >= 2 and c.later_eligible >= 2 for c in cases)
    assert all(c.earlier_eligible == cases[0].earlier_eligible for c in cases)
    assert all(c.later_eligible == cases[0].later_eligible for c in cases)
    assert all(a.difference_floor >= b.difference_floor
               for a, b in pairwise(cases))
    assert all(a.difference_ceiling <= b.difference_ceiling
               for a, b in pairwise(cases))
    assert cases[-1].difference_floor < 0 < cases[-1].difference_ceiling
    assert cases[-1].direction_status == "direction_not_robust_to_declared_counterfactual_bounds"
    assert result.receipt()["selection_bias_status"] == "not_identified"


def test_unpublished_earlier_value_does_not_change_any_earlier_scenario():
    initial, releases = fixture(late75=True, value75=75)
    changed, releases_again = fixture(late75=True, value75=999999)
    assert releases == releases_again
    a = sweep(initial, releases, minimum_eligible_per_window=2,
              minimum_coverage_percent=20)
    b = sweep(changed, releases_again, minimum_eligible_per_window=2,
              minimum_coverage_percent=20)
    for x, y in zip(a.scenarios, b.scenarios):
        assert x.earlier_eligible == y.earlier_eligible
        assert x.earlier_mean_floor == y.earlier_mean_floor
        assert x.earlier_mean_ceiling == y.earlier_mean_ceiling


def test_sparse_window_refuses_every_scenario_value():
    projection, releases = fixture(missing80=True, late75=True, late83=True)
    cases = sweep(projection, releases).scenarios
    assert all(case.later_eligible == 1 for case in cases)
    assert all(case.difference_floor is None and case.difference_ceiling is None
               for case in cases)
    assert all(case.direction_status == "abstained_insufficient_declared_coverage"
               for case in cases)


def test_default_coverage_gate_hides_all_scenario_means_but_preserves_denominators():
    projection, releases = fixture(missing82=True, late75=True, late83=True)
    report = sweep(projection, releases)
    assert report.coverage_status == "insufficient_comparable_coverage_abstained"
    assert report.minimum_eligible_per_window == 3
    assert report.minimum_coverage_percent == 80
    receipt = report.receipt()
    assert receipt["earlier_requested"] == receipt["later_requested"] == 7
    assert receipt["earlier_eligible"] < receipt["earlier_requested"]
    assert receipt["later_eligible"] < receipt["later_requested"]
    assert receipt["scenario_count"] == 3
    for case in report.scenarios:
        assert case.earlier_mean_floor is None and case.earlier_mean_ceiling is None
        assert case.later_mean_floor is None and case.later_mean_ceiling is None
        assert case.difference_floor is None and case.difference_ceiling is None
        assert case.direction_status == "abstained_insufficient_declared_coverage"
    assert all(row["difference_floor"] is None for row in receipt["scenarios"])
    assert receipt["statistical_guarantee"] is None


def test_gate_fails_when_only_one_eligible_window_misses_minimum():
    projection, releases = fixture(late75=True)
    permissive = sweep(
        projection, releases, minimum_eligible_per_window=2,
        minimum_coverage_percent=20,
    )
    assert permissive.coverage_status == "eligible_subset_scenario_only"
    higher_minimum = sweep(
        projection, releases, minimum_eligible_per_window=5,
        minimum_coverage_percent=20,
    )
    assert higher_minimum.coverage_status.endswith("abstained")
    assert all(case.difference_floor is None for case in higher_minimum.scenarios)


def test_exact_integer_percentage_threshold_is_not_rounded_up():
    projection, releases = fixture(late75=True)
    pass_at_57 = sweep(
        projection, releases, minimum_eligible_per_window=2,
        minimum_coverage_percent=57,
    )
    fail_at_58 = sweep(
        projection, releases, minimum_eligible_per_window=2,
        minimum_coverage_percent=58,
    )
    assert pass_at_57.scenarios[0].earlier_eligible == 4
    assert pass_at_57.scenarios[0].earlier_requested == 7
    assert pass_at_57.coverage_status == "eligible_subset_scenario_only"
    assert fail_at_58.coverage_status == "insufficient_comparable_coverage_abstained"
    assert all(item.difference_ceiling is None for item in fail_at_58.scenarios)


@pytest.mark.parametrize("key,bad,expected", [
    ("window_days", True, "window_days"),
    ("window_days", 1, "window_days"),
    ("window_days", 31, "window_days"),
    ("minimum_eligible_per_window", True, "minimum_eligible_per_window"),
    ("minimum_eligible_per_window", 1, "minimum_eligible_per_window"),
    ("minimum_eligible_per_window", 8, "minimum_eligible_per_window"),
    ("minimum_coverage_percent", True, "minimum_coverage_percent"),
    ("minimum_coverage_percent", 0, "minimum_coverage_percent"),
    ("minimum_coverage_percent", 101, "minimum_coverage_percent"),
    ("minimum_coverage_percent", 80.0, "minimum_coverage_percent"),
])
def test_strict_gate_configuration_validation(key, bad, expected):
    projection, releases = fixture()
    with pytest.raises(ValueError, match=expected):
        sweep(projection, releases, **{key: bad})


@pytest.mark.parametrize("settings", [
    {},
    {"late75": True},
    {"missing82": True, "late75": True, "late83": True},
])
def test_sweep_scenarios_exactly_match_independent_single_ceiling_results(settings):
    projection, releases = fixture(**settings)
    ceilings = (0, 1, 7, 100, 1000, 1_000_000)
    result = sweep(
        projection, releases, ceilings=ceilings,
        minimum_eligible_per_window=2, minimum_coverage_percent=1,
    )
    for scenario in result.scenarios:
        independent = assess_excluded_target_sensitivity(
            projection, releases, stock_code="PRIVATE-SKU",
            evaluation_on=day(84), excluded_value_ceiling=scenario.excluded_value_ceiling,
        )
        assert scenario == independent


def test_eight_scenarios_run_exactly_two_historical_audits(monkeypatch):
    import mirrormind.domains.retail.selection_sensitivity as module

    projection, releases = fixture(missing82=True, late75=True, late83=True)
    original = module.evaluate_retail_residual_envelopes
    cutoffs = []

    def spy(*args, **kwargs):
        cutoffs.append(kwargs["evaluation_on"])
        return original(*args, **kwargs)

    monkeypatch.setattr(module, "evaluate_retail_residual_envelopes", spy)
    result = sweep(
        projection, releases, ceilings=(0, 1, 2, 3, 4, 5, 6, 7),
        minimum_eligible_per_window=2, minimum_coverage_percent=1,
    )
    assert len(result.scenarios) == 8
    assert cutoffs == [day(77), day(84)]
    assert all(case.earlier_eligible == result.scenarios[0].earlier_eligible
               for case in result.scenarios)


def test_sweep_validation_failure_does_not_evaluate_historical_windows(monkeypatch):
    import mirrormind.domains.retail.selection_sensitivity as module

    projection, releases = fixture()
    def forbidden(*args, **kwargs):
        raise AssertionError("validation must fail before historical evaluation")

    monkeypatch.setattr(module, "evaluate_retail_residual_envelopes", forbidden)
    with pytest.raises(ValueError, match="strictly increasing"):
        sweep(projection, releases, ceilings=(10, 10))


@pytest.mark.parametrize("bad", [
    (), (0,), tuple(range(9)), [0, 10], (0, "10"), (0, True),
    (-1, 10), (0, 1_000_001), (5, 5), (10, 5), (0, 1.5),
])
def test_ceiling_budget_and_monotonicity_are_checked_before_source_data(bad):
    projection, releases = fixture()
    with pytest.raises(ValueError, match="ceiling"):
        sweep(projection, releases, ceilings=bad)


def test_declaration_validation_is_not_bypassed_by_sweep():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        sweep(projection, releases[:-1])
