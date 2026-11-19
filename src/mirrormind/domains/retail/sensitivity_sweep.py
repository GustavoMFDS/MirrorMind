"""Bounded counterfactual sensitivity sweep over caller-declared ceilings.

Scenarios are mathematical what-ifs on fictional eligible data, not a
distribution-shift detector or evidence of missing target values.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.selection_sensitivity import (
    ExcludedTargetSensitivity,
    assess_excluded_target_sensitivity,
)
from mirrormind.domains.retail.uci_transactions import UciRetailProjection


@dataclass(frozen=True, slots=True)
class RetailSensitivitySweep:
    """An ordered, bounded list of hypothetical scenario results."""

    scenarios: tuple[ExcludedTargetSensitivity, ...]

    def receipt(self) -> dict[str, object]:
        """Show scenario receipts but never selected source identifiers."""
        return {
            "status": "fictional_retail_sensitivity_sweep_not_authorized",
            "source_status": "caller_declared_release_not_authenticated",
            "scenario_count": len(self.scenarios),
            "scenarios": tuple(case.receipt() for case in self.scenarios),
            "selection_bias_status": "not_identified",
            "distribution_shift_status": "not_identified",
            "statistical_guarantee": None,
        }


def sweep_excluded_target_sensitivity(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    ceilings: tuple[int, ...],
    window_days: int = 7,
    calibration_days: int = 21,
    min_calibration_residuals: int = 5,
) -> RetailSensitivitySweep:
    """Compare two to eight strictly increasing, hypothetical ceilings.

    Every scenario uses the same independently as-of-eligible dates.
    A single sparse window forces abstention across all scenarios.
    """
    if type(ceilings) is not tuple or not 2 <= len(ceilings) <= 8:
        raise ValueError("ceilings must be a tuple containing 2..8 exact integers")
    if any(type(value) is not int or not 0 <= value <= 1_000_000 for value in ceilings):
        raise ValueError("each ceiling must be an exact integer in 0..1000000")
    if any(left >= right for left, right in zip(ceilings, ceilings[1:])):
        raise ValueError("ceilings must be strictly increasing without duplicates")
    scenarios = tuple(
        assess_excluded_target_sensitivity(
            projection, releases, stock_code=stock_code,
            evaluation_on=evaluation_on, excluded_value_ceiling=ceiling,
            window_days=window_days, calibration_days=calibration_days,
            min_calibration_residuals=min_calibration_residuals,
        )
        for ceiling in ceilings
    )
    reference = scenarios[0]
    assert all(
        (item.earlier_requested, item.later_requested,
         item.earlier_eligible, item.later_eligible)
        == (reference.earlier_requested, reference.later_requested,
            reference.earlier_eligible, reference.later_eligible)
        for item in scenarios
    )
    return RetailSensitivitySweep(scenarios=scenarios)
