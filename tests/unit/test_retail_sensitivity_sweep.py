"""No-hindsight, monotone scenario-sweep regressions on invented rows."""
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
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
    result = sweep(projection, releases, ceilings=(0, 100, 1000))
    cases = result.scenarios
    assert all(c.earlier_eligible >= 2 and c.later_eligible >= 2 for c in cases)
    assert all(c.earlier_eligible == cases[0].earlier_eligible for c in cases)
    assert all(c.later_eligible == cases[0].later_eligible for c in cases)
    assert all(a.difference_floor >= b.difference_floor
               for a, b in zip(cases, cases[1:]))
    assert all(a.difference_ceiling <= b.difference_ceiling
               for a, b in zip(cases, cases[1:]))
    assert cases[-1].difference_floor < 0 < cases[-1].difference_ceiling
    assert cases[-1].direction_status == "direction_not_robust_to_declared_counterfactual_bounds"
    assert result.receipt()["selection_bias_status"] == "not_identified"


def test_unpublished_earlier_value_does_not_change_any_earlier_scenario():
    initial, releases = fixture(late75=True, value75=75)
    changed, releases_again = fixture(late75=True, value75=999999)
    assert releases == releases_again
    a = sweep(initial, releases)
    b = sweep(changed, releases_again)
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
    assert all(case.direction_status == "abstained_insufficient_eligible_reference"
               for case in cases)


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
