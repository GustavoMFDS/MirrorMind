"""Consecutive-window eligibility drift audit for fictional retail diagnostics.

This measures changes in which dates can be evaluated, NOT actual demand
distribution drift, selection-bias corrections, or future model validity.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.residual_envelope import (
    evaluate_retail_residual_envelopes,
)
from mirrormind.domains.retail.uci_transactions import UciRetailProjection


@dataclass(frozen=True, slots=True)
class RetailEligibilityDrift:
    """Two disjoint retrospective eligibility windows with honest denominators."""

    earlier_requested: int
    later_requested: int
    earlier_evaluated: int
    later_evaluated: int
    earlier_missing: int
    later_missing: int
    earlier_unpublished: int
    later_unpublished: int
    earlier_history_abstained: int
    later_history_abstained: int
    earlier_calibration_abstained: int
    later_calibration_abstained: int

    def receipt(self) -> dict[str, str | int | None]:
        """Expose aggregate eligibility changes only, never performance or identities."""
        return {
            "status": "fictional_retail_eligibility_drift_not_authorized",
            "source_status": "caller_declared_release_not_authenticated",
            "earlier_evaluated": self.earlier_evaluated,
            "earlier_requested": self.earlier_requested,
            "later_evaluated": self.later_evaluated,
            "later_requested": self.later_requested,
            "eligible_origin_change": self.later_evaluated - self.earlier_evaluated,
            "earlier_missing": self.earlier_missing,
            "later_missing": self.later_missing,
            "earlier_unpublished": self.earlier_unpublished,
            "later_unpublished": self.later_unpublished,
            "earlier_history_abstained": self.earlier_history_abstained,
            "later_history_abstained": self.later_history_abstained,
            "earlier_calibration_abstained": self.earlier_calibration_abstained,
            "later_calibration_abstained": self.later_calibration_abstained,
            "selection_bias_status": "not_identifiable_from_eligible_only_targets",
            "distribution_shift_status": "not_measured",
            "statistical_significance": None,
        }


def audit_retail_eligibility_drift(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    window_days: int = 7,
    calibration_days: int = 21,
    min_calibration_residuals: int = 5,
) -> RetailEligibilityDrift:
    """Compare independent adjacent windows at THEIR OWN evaluation cutoffs.

    Both calls retain the original release assertions. Later publication
    cannot retroactively improve earlier-window historical eligibility.
    """
    if type(evaluation_on) is not date:
        raise ValueError("evaluation_on must be an exact date")
    if type(window_days) is not int or not 2 <= window_days <= 30:
        raise ValueError("window_days must be an exact integer in 2..30")
    earlier_cutoff = evaluation_on - timedelta(days=window_days)
    common = {
        "stock_code": stock_code,
        "holdout_days": window_days,
        "calibration_days": calibration_days,
        "min_calibration_residuals": min_calibration_residuals,
    }
    earlier = evaluate_retail_residual_envelopes(
        projection, releases, evaluation_on=earlier_cutoff, **common
    )
    later = evaluate_retail_residual_envelopes(
        projection, releases, evaluation_on=evaluation_on, **common
    )

    def number(report: dict[str, object], key: str) -> int:
        value = report[key]
        assert type(value) is int
        return value

    fields = {
        "earlier_requested": number(earlier, "requested_origins"),
        "later_requested": number(later, "requested_origins"),
        "earlier_evaluated": number(earlier, "evaluated_origins"),
        "later_evaluated": number(later, "evaluated_origins"),
        "earlier_missing": number(earlier, "abstained_missing_target"),
        "later_missing": number(later, "abstained_missing_target"),
        "earlier_unpublished": number(earlier, "abstained_unpublished_target"),
        "later_unpublished": number(later, "abstained_unpublished_target"),
        "earlier_history_abstained": number(earlier, "abstained_forecast_history"),
        "later_history_abstained": number(later, "abstained_forecast_history"),
        "earlier_calibration_abstained": number(earlier, "abstained_calibration"),
        "later_calibration_abstained": number(later, "abstained_calibration"),
    }
    for prefix in ("earlier", "later"):
        assert fields[f"{prefix}_requested"] == sum(
            fields[key] for key in (
                f"{prefix}_evaluated", f"{prefix}_missing",
                f"{prefix}_unpublished", f"{prefix}_history_abstained",
                f"{prefix}_calibration_abstained",
            )
        )
    return RetailEligibilityDrift(**fields)
