"""Conservative coverage gate over an unverified, fictional retail backtest.

This prevents model ranking on a tiny eligible subset. It does NOT calibrate
uncertainty, authenticate release histories or estimate real demand.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.release_backtest import backtest_declared_retail_releases
from mirrormind.domains.retail.uci_transactions import UciRetailProjection


@dataclass(frozen=True, slots=True)
class RetailBacktestCoverageGate:
    """Identifier-free summary: eligibility is not accuracy or calibration."""

    requested_origins: int
    scored_origins: int
    missing_target: int
    unpublished_target: int
    unavailable_history: int
    minimum_coverage_percent: int
    comparison_status: str
    conditional_lower_mae: str | None

    def receipt(self) -> dict[str, str | int | None]:
        """Expose exact coverage fractions and never invent intervals."""
        return {
            "status": "fictional_retail_coverage_gate_not_authorized",
            "publication_authority": "caller_declared_unverified",
            "requested_origins": self.requested_origins,
            "scored_origins": self.scored_origins,
            "coverage_numerator": self.scored_origins,
            "coverage_denominator": self.requested_origins,
            "missing_target": self.missing_target,
            "unpublished_target": self.unpublished_target,
            "unavailable_history": self.unavailable_history,
            "minimum_coverage_percent": self.minimum_coverage_percent,
            "comparison_status": self.comparison_status,
            "conditional_lower_mae": self.conditional_lower_mae,
            "uncertainty_status": "not_estimated_or_calibrated",
            "prediction_interval": None,
        }


def assess_retail_backtest_coverage(
    projection: UciRetailProjection,
    releases: tuple[DeclaredProductRelease, ...],
    *,
    stock_code: str,
    evaluation_on: date,
    holdout_days: int = 7,
    minimum_coverage_percent: int = 80,
) -> RetailBacktestCoverageGate:
    """Gate conditional model ranking by eligible-origin count and fraction.

    The cutoff and all releases are validated by the underlying evaluator.
    A minimum of two scored origins is *always* necessary for any ranking.
    Percentage comparison uses exact integer arithmetic (no rounding).
    """
    if (
        type(minimum_coverage_percent) is not int
        or not 1 <= minimum_coverage_percent <= 100
    ):
        raise ValueError("minimum_coverage_percent must be an exact integer in 1..100")
    result = backtest_declared_retail_releases(
        projection, releases, stock_code=stock_code,
        evaluation_on=evaluation_on, holdout_days=holdout_days,
    )
    requested = result["holdout_days"]
    scored = result["scored_origins"]
    missing = result["abstained_missing_target"]
    unpublished = result["abstained_unpublished_target"]
    history = result["abstained_history"]
    assert all(type(value) is int for value in (
        requested, scored, missing, unpublished, history
    ))
    assert scored + missing + unpublished + history == requested
    if scored < 2:
        status = "insufficient_scored_origins"
        winner = None
    elif scored * 100 < requested * minimum_coverage_percent:
        status = "insufficient_coverage_for_comparison"
        winner = None
    else:
        status = "eligible_for_conditional_comparison_only"
        winner = result["lower_mae_on_matched_origins_only"]
        assert winner is not None
    return RetailBacktestCoverageGate(
        requested_origins=requested,
        scored_origins=scored,
        missing_target=missing,
        unpublished_target=unpublished,
        unavailable_history=history,
        minimum_coverage_percent=minimum_coverage_percent,
        comparison_status=status,
        conditional_lower_mae=winner,
    )
