"""Descriptive comparison of eligible fictional retail proxy values, not demand shift.

Each window uses its own source-unverified publication cutoff. Excluded
targets cannot be recovered, so population shift and selection bias are
not identifiable from the returned conditional statistics.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from statistics import median

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.residual_envelope import evaluate_retail_residual_envelopes
from mirrormind.domains.retail.uci_transactions import UciRetailProjection


@dataclass(frozen=True, slots=True)
class EligibleRetailValueComparison:
    """Aggregate values conditional on separate retrospective eligibility."""

    earlier_requested: int
    later_requested: int
    earlier_eligible: int
    later_eligible: int
    earlier_missing: int
    later_missing: int
    earlier_unpublished: int
    later_unpublished: int
    earlier_history_unavailable: int
    later_history_unavailable: int
    earlier_calibration_unavailable: int
    later_calibration_unavailable: int
    minimum_eligible_per_window: int
    minimum_coverage_percent: int
    status: str
    earlier_mean: float | None
    later_mean: float | None
    later_minus_earlier_mean: float | None
    earlier_median: float | None
    later_median: float | None

    def receipt(self) -> dict[str, str | int | float | None]:
        """Expose exact eligibility fractions and only conditional statistics."""
        return {
            "status": self.status,
            "source_status": "caller_declared_release_not_authenticated_or_authorized",
            "scope": "eligible_positive_invoice_line_proxies_only",
            "earlier_requested": self.earlier_requested,
            "later_requested": self.later_requested,
            "earlier_eligible": self.earlier_eligible,
            "later_eligible": self.later_eligible,
            "earlier_missing": self.earlier_missing,
            "later_missing": self.later_missing,
            "earlier_unpublished": self.earlier_unpublished,
            "later_unpublished": self.later_unpublished,
            "earlier_history_unavailable": self.earlier_history_unavailable,
            "later_history_unavailable": self.later_history_unavailable,
            "earlier_calibration_unavailable": self.earlier_calibration_unavailable,
            "later_calibration_unavailable": self.later_calibration_unavailable,
            "minimum_eligible_per_window": self.minimum_eligible_per_window,
            "minimum_coverage_percent": self.minimum_coverage_percent,
            "earlier_mean": self.earlier_mean,
            "later_mean": self.later_mean,
            "later_minus_earlier_mean": self.later_minus_earlier_mean,
            "earlier_median": self.earlier_median,
            "later_median": self.later_median,
            "distribution_shift_status": "not_identified",
            "selection_bias_status": "unknown_for_excluded_targets",
            "significance": None,
        }


def compare_eligible_retail_values(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    window_days: int = 7,
    calibration_days: int = 21,
    min_calibration_residuals: int = 5,
    minimum_eligible_per_window: int = 3,
    minimum_coverage_percent: int = 80,
) -> EligibleRetailValueComparison:
    """Compare two disjoint eligible subsets; refuse sparse comparisons.

    Earlier eligibility is evaluated using the earlier window's own cutoff.
    Later publication cannot retroactively change that set. A missing
    product-day is not zero and never enters the descriptive statistics.
    """
    if type(evaluation_on) is not date:
        raise ValueError("evaluation_on must be an exact date")
    if type(window_days) is not int or not 2 <= window_days <= 30:
        raise ValueError("window_days must be an exact integer in 2..30")
    if (type(minimum_eligible_per_window) is not int
            or not 2 <= minimum_eligible_per_window <= window_days):
        raise ValueError("minimum_eligible_per_window must be in 2..window_days")
    if (type(minimum_coverage_percent) is not int
            or not 1 <= minimum_coverage_percent <= 100):
        raise ValueError("minimum_coverage_percent must be an exact integer in 1..100")

    earlier_end = evaluation_on - timedelta(days=window_days)
    earlier = evaluate_retail_residual_envelopes(
        projection, releases, evaluation_on=earlier_end,
        stock_code=stock_code, holdout_days=window_days,
        calibration_days=calibration_days, min_calibration_residuals=min_calibration_residuals,
    )
    later = evaluate_retail_residual_envelopes(
        projection, releases, evaluation_on=evaluation_on,
        stock_code=stock_code, holdout_days=window_days,
        calibration_days=calibration_days, min_calibration_residuals=min_calibration_residuals,
    )
    values = {
        day.observed_on: day.units
        for day in projection.days if day.stock_code == stock_code
    }

    def checked(report: dict[str, object]) -> tuple[int, int, int, int, int, int, list[int]]:
        requested = report["requested_origins"]
        eligible = report["evaluated_origins"]
        missing = report["abstained_missing_target"]
        unpublished = report["abstained_unpublished_target"]
        history = report["abstained_forecast_history"]
        calibration = report["abstained_calibration"]
        assert type(requested) is int
        assert type(eligible) is int
        assert type(missing) is int
        assert type(unpublished) is int
        assert type(history) is int
        assert type(calibration) is int
        assert requested == eligible + missing + unpublished + history + calibration
        audit = report["origin_audit"]
        assert isinstance(audit, tuple)
        selected = [
            values[date.fromisoformat(row["target_on"])]
            for row in audit if row["status"] == "retrospective_envelope_evaluated"
        ]
        assert len(selected) == eligible
        return requested, eligible, missing, unpublished, history, calibration, selected

    a = checked(earlier)
    b = checked(later)
    ready = (
        a[1] >= minimum_eligible_per_window
        and b[1] >= minimum_eligible_per_window
        and a[1] * 100 >= a[0] * minimum_coverage_percent
        and b[1] * 100 >= b[0] * minimum_coverage_percent
    )
    am: float | None
    bm: float | None
    difference: float | None
    if ready:
        am = sum(a[6]) / a[1]
        bm = sum(b[6]) / b[1]
        difference = bm - am
    else:
        am = bm = difference = None
    return EligibleRetailValueComparison(
        earlier_requested=a[0], later_requested=b[0],
        earlier_eligible=a[1], later_eligible=b[1],
        earlier_missing=a[2], later_missing=b[2],
        earlier_unpublished=a[3], later_unpublished=b[3],
        earlier_history_unavailable=a[4], later_history_unavailable=b[4],
        earlier_calibration_unavailable=a[5], later_calibration_unavailable=b[5],
        minimum_eligible_per_window=minimum_eligible_per_window,
        minimum_coverage_percent=minimum_coverage_percent,
        status=("eligible_subset_descriptive_comparison_only" if ready
                else "insufficient_comparable_coverage_abstained"),
        earlier_mean=am, later_mean=bm,
        later_minus_earlier_mean=difference,
        earlier_median=float(median(a[6])) if ready else None,
        later_median=float(median(b[6])) if ready else None,
    )
