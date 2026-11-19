"""Bounded counterfactual sensitivity sweep over caller-declared ceilings.

Scenarios are mathematical what-ifs on fictional eligible data, not a
distribution-shift detector or evidence of missing target values.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date
from itertools import pairwise

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.selection_sensitivity import (
    ExcludedTargetSensitivity,
    _collect_eligible_window_totals,
    _scenario_from_eligible_totals,
)
from mirrormind.domains.retail.uci_transactions import UciRetailProjection


@dataclass(frozen=True, slots=True)
class RetailSensitivitySweep:
    """An ordered, bounded list of hypothetical scenario results."""

    scenarios: tuple[ExcludedTargetSensitivity, ...]
    minimum_eligible_per_window: int
    minimum_coverage_percent: int
    coverage_status: str

    def receipt(self) -> dict[str, object]:
        """Show scenario receipts but never selected source identifiers."""
        return {
            "status": "fictional_retail_sensitivity_sweep_not_authorized",
            "source_status": "caller_declared_release_not_authenticated",
            "scenario_count": len(self.scenarios),
            "coverage_status": self.coverage_status,
            "minimum_eligible_per_window": self.minimum_eligible_per_window,
            "minimum_coverage_percent": self.minimum_coverage_percent,
            "earlier_requested": self.scenarios[0].earlier_requested,
            "later_requested": self.scenarios[0].later_requested,
            "earlier_eligible": self.scenarios[0].earlier_eligible,
            "later_eligible": self.scenarios[0].later_eligible,
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
    minimum_eligible_per_window: int = 3,
    minimum_coverage_percent: int = 80,
) -> RetailSensitivitySweep:
    """Compare two to eight strictly increasing, hypothetical ceilings.

    All scenarios reuse the same two independently as-of-eligible windows.
    A sparse window forces abstention across all scenarios, even if the
    underlying single-ceiling diagnostic could compute a small-sample mean.
    """
    if type(window_days) is not int or not 2 <= window_days <= 30:
        raise ValueError("window_days must be an exact integer in 2..30")
    if (type(minimum_eligible_per_window) is not int
            or not 2 <= minimum_eligible_per_window <= window_days):
        raise ValueError("minimum_eligible_per_window must be in 2..window_days")
    if (type(minimum_coverage_percent) is not int
            or not 1 <= minimum_coverage_percent <= 100):
        raise ValueError("minimum_coverage_percent must be an exact integer in 1..100")
    if type(ceilings) is not tuple or not 2 <= len(ceilings) <= 8:
        raise ValueError("ceilings must be a tuple containing 2..8 exact integers")
    if any(type(value) is not int or not 0 <= value <= 1_000_000 for value in ceilings):
        raise ValueError("each ceiling must be an exact integer in 0..1000000")
    if any(left >= right for left, right in pairwise(ceilings)):
        raise ValueError("ceilings must be strictly increasing without duplicates")
    earlier, later = _collect_eligible_window_totals(
        projection, releases, stock_code=stock_code,
        evaluation_on=evaluation_on, window_days=window_days,
        calibration_days=calibration_days,
        min_calibration_residuals=min_calibration_residuals,
    )
    # Publication and history eligibility is audited twice total,
    # irrespective of the bounded number of hypothetical ceilings.
    scenarios = tuple(
        _scenario_from_eligible_totals(earlier, later, ceiling)
        for ceiling in ceilings
    )
    reference = scenarios[0]
    adequate = (
        reference.earlier_eligible >= minimum_eligible_per_window
        and reference.later_eligible >= minimum_eligible_per_window
        and reference.earlier_eligible * 100
            >= reference.earlier_requested * minimum_coverage_percent
        and reference.later_eligible * 100
            >= reference.later_requested * minimum_coverage_percent
    )
    if not adequate:
        # Do not return per-scenario means or differences for thin subsets.
        scenarios = tuple(replace(
            case,
            earlier_mean_floor=None, earlier_mean_ceiling=None,
            later_mean_floor=None, later_mean_ceiling=None,
            difference_floor=None, difference_ceiling=None,
            direction_status="abstained_insufficient_declared_coverage",
        ) for case in scenarios)
    return RetailSensitivitySweep(
        scenarios=scenarios,
        minimum_eligible_per_window=minimum_eligible_per_window,
        minimum_coverage_percent=minimum_coverage_percent,
        coverage_status=("eligible_subset_scenario_only" if adequate
                         else "insufficient_comparable_coverage_abstained"),
    )
