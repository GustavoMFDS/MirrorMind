"""Hypothetical excluded-target sensitivity, never an estimate of true demand.

Unknown ineligible days are not imputed. Caller bounds describe explicit
counterfactual scenarios, not actual inventory, source completeness or data.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.residual_envelope import evaluate_retail_residual_envelopes
from mirrormind.domains.retail.uci_transactions import UciRetailProjection


@dataclass(frozen=True, slots=True)
class ExcludedTargetSensitivity:
    """Two-window counterfactual mean bounds with eligibility denominators."""

    earlier_requested: int
    later_requested: int
    earlier_eligible: int
    later_eligible: int
    excluded_value_ceiling: int
    earlier_mean_floor: float | None
    earlier_mean_ceiling: float | None
    later_mean_floor: float | None
    later_mean_ceiling: float | None
    difference_floor: float | None
    difference_ceiling: float | None
    direction_status: str

    def receipt(self) -> dict[str, str | int | float | None]:
        """Report counterfactual bounds without any excluded target values."""
        return {
            "status": "fictional_excluded_target_sensitivity_not_authorized",
            "assumption": "each_excluded_day_hypothetically_between_zero_and_ceiling",
            "source_status": "caller_declared_release_not_authenticated",
            "earlier_requested": self.earlier_requested,
            "later_requested": self.later_requested,
            "earlier_eligible": self.earlier_eligible,
            "later_eligible": self.later_eligible,
            "earlier_excluded": self.earlier_requested - self.earlier_eligible,
            "later_excluded": self.later_requested - self.later_eligible,
            "excluded_value_ceiling": self.excluded_value_ceiling,
            "earlier_mean_floor": self.earlier_mean_floor,
            "earlier_mean_ceiling": self.earlier_mean_ceiling,
            "later_mean_floor": self.later_mean_floor,
            "later_mean_ceiling": self.later_mean_ceiling,
            "difference_floor": self.difference_floor,
            "difference_ceiling": self.difference_ceiling,
            "direction_status": self.direction_status,
            "selection_bias_status": "not_identified",
            "population_shift_status": "not_identified",
        }


def assess_excluded_target_sensitivity(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    excluded_value_ceiling: int,
    window_days: int = 7,
    calibration_days: int = 21,
    min_calibration_residuals: int = 5,
) -> ExcludedTargetSensitivity:
    """Vary hypothetical excluded day values, preserving each window cutoff.

    Excluded values are never accessed, even if present in the supplied
    projection but not yet published by that window's evaluation cutoff.
    A window with fewer than two eligible values abstains, preventing
    disclosure of single observed values through reconstructed totals.
    """
    if type(excluded_value_ceiling) is not int or not 0 <= excluded_value_ceiling <= 1_000_000:
        raise ValueError("excluded_value_ceiling must be an exact integer in 0..1000000")
    earlier, later = _collect_eligible_window_totals(
        projection, releases, stock_code=stock_code, evaluation_on=evaluation_on,
        window_days=window_days, calibration_days=calibration_days,
        min_calibration_residuals=min_calibration_residuals,
    )
    return _scenario_from_eligible_totals(earlier, later, excluded_value_ceiling)


def _collect_eligible_window_totals(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    window_days: int,
    calibration_days: int,
    min_calibration_residuals: int,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    """Collect integer totals once at each declared as-of evaluation cutoff.

    The third integer is a sum only over eligible, released positive-line
    observations. No per-origin values or unpublished targets are returned.
    """
    if type(evaluation_on) is not date:
        raise ValueError("evaluation_on must be an exact date")
    if type(window_days) is not int or not 2 <= window_days <= 30:
        raise ValueError("window_days must be an exact integer in 2..30")
    if type(calibration_days) is not int or not 5 <= calibration_days <= 60:
        raise ValueError("calibration_days must be an exact integer in 5..60")
    if (type(min_calibration_residuals) is not int
            or not 3 <= min_calibration_residuals <= calibration_days):
        raise ValueError("min_calibration_residuals must be in 3..calibration_days")
    if evaluation_on.toordinal() <= 2 * window_days + calibration_days + 7:
        raise ValueError("evaluation calendar precedes supported two-window history")
    earlier_cutoff = evaluation_on - timedelta(days=window_days)
    kwargs = {
        "stock_code": stock_code,
        "holdout_days": window_days,
        "calibration_days": calibration_days,
        "min_calibration_residuals": min_calibration_residuals,
    }
    earlier = evaluate_retail_residual_envelopes(
        projection, releases, evaluation_on=earlier_cutoff, **kwargs
    )
    later = evaluate_retail_residual_envelopes(
        projection, releases, evaluation_on=evaluation_on, **kwargs
    )
    observed = {
        row.observed_on: row.units
        for row in projection.days if row.stock_code == stock_code
    }

    def selected(report: dict[str, object]) -> tuple[int, int, int]:
        requested = report["requested_origins"]
        eligible = report["evaluated_origins"]
        audits = report["origin_audit"]
        assert type(requested) is int and type(eligible) is int
        assert isinstance(audits, tuple) and len(audits) == requested
        days = [
            date.fromisoformat(row["target_on"])
            for row in audits if row["status"] == "retrospective_envelope_evaluated"
        ]
        assert len(days) == eligible and eligible <= requested
        return requested, eligible, sum(observed[day] for day in days)

    return selected(earlier), selected(later)


def _scenario_from_eligible_totals(
    earlier: tuple[int, int, int],
    later: tuple[int, int, int],
    excluded_value_ceiling: int,
) -> ExcludedTargetSensitivity:
    """Apply a caller's assumption to validated eligible totals, without I/O."""
    a_n, a_ok, a_total = earlier
    b_n, b_ok, b_total = later
    ready = a_ok >= 2 and b_ok >= 2
    a_low = a_total / a_n if ready else None
    b_low = b_total / b_n if ready else None
    a_high = (a_total + (a_n - a_ok) * excluded_value_ceiling) / a_n if ready else None
    b_high = (b_total + (b_n - b_ok) * excluded_value_ceiling) / b_n if ready else None
    diff_low = b_low - a_high if ready else None
    diff_high = b_high - a_low if ready else None
    if not ready:
        direction = "abstained_insufficient_eligible_reference"
    elif diff_low > 0:
        direction = "positive_under_declared_counterfactual_bounds_only"
    elif diff_high < 0:
        direction = "negative_under_declared_counterfactual_bounds_only"
    else:
        direction = "direction_not_robust_to_declared_counterfactual_bounds"
    return ExcludedTargetSensitivity(
        earlier_requested=a_n, later_requested=b_n,
        earlier_eligible=a_ok, later_eligible=b_ok,
        excluded_value_ceiling=excluded_value_ceiling,
        earlier_mean_floor=a_low, earlier_mean_ceiling=a_high,
        later_mean_floor=b_low, later_mean_ceiling=b_high,
        difference_floor=diff_low, difference_ceiling=diff_high,
        direction_status=direction,
    )
