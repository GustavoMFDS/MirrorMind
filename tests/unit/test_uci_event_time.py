"""Synthetic regressions for the fixed UCI event-time retrospective protocol."""
from datetime import date, timedelta

import pytest

from mirrormind.domains.retail.uci_event_time import (
    FIT_END,
    FIT_START,
    SOURCE_END,
    SOURCE_START,
    UciEventTimeEvaluationError,
    evaluate_uci_event_time,
)
from mirrormind.domains.retail.uci_transactions import (
    ProductDayUnits,
    UciRetailProjection,
)
from mirrormind.domains.retail.uci_workbook import UciWorkbookReadResult


def _days(start: date, end: date) -> tuple[date, ...]:
    count = (end - start).days
    return tuple(start + timedelta(days=index) for index in range(count + 1))


def _snapshot(
    *,
    omit_product_day: date | None = None,
    omit_coverage_day: date | None = None,
    holdout_multiplier: int = 1,
    evaluation_rows: bool = True,
) -> tuple[UciWorkbookReadResult, set[date]]:
    projected: list[ProductDayUnits] = []
    accepted = 0
    for event_day in _days(SOURCE_START, SOURCE_END):
        if (event_day <= FIT_END or evaluation_rows) and event_day != omit_product_day:
            multiplier = holdout_multiplier if event_day > date(2011, 10, 1) else 1
            units = event_day.toordinal() % 7 + multiplier
            projected.append(ProductDayUnits("SYNTHETIC-A", event_day, units))
            accepted += 1
        if event_day == date(2011, 9, 1):
            projected.append(ProductDayUnits("SYNTHETIC-B", event_day, 5))
            accepted += 1
    projection = UciRetailProjection(
        days=tuple(projected),
        processed_rows=accepted,
        accepted_rows=accepted,
        cancelled_rows=0,
        negative_quantity_rows=0,
        zero_quantity_rows=0,
    )
    covered = set(_days(SOURCE_START, SOURCE_END))
    if omit_coverage_day is not None:
        covered.remove(omit_coverage_day)
    return UciWorkbookReadResult("a" * 64, projection), covered


def test_event_time_protocol_uses_frozen_cohort_matched_pairs_and_redacts_codes():
    snapshot, coverage = _snapshot(omit_product_day=date(2011, 9, 5))

    result = evaluate_uci_event_time(
        snapshot, complete_event_dates=coverage, split="validation"
    )

    assert result["status"] == "event_time_retrospective_unverified_availability"
    assert result["evaluation_status"] == "metrics_available"
    assert result["cohort_size"] == 1
    assert result["excluded_post_fit_products"] == 1
    assert result["eligible_product_origin_pairs"] == 31
    assert result["scored_product_origin_pairs"] == 31
    assert result["coverage"] == 1.0
    assert result["abstentions"] == {
        "target_coverage_unverified": 0,
        "history_coverage_unverified": 0,
    }
    assert set(result["metrics"]) == {
        "same_weekday_last_week", "trailing_7_calendar_day_mean"
    }
    assert len(result["per_product"]) == 1
    assert result["per_product"][0]["product_ordinal"] == 1
    assert "SYNTHETIC-A" not in str(result)
    assert "SYNTHETIC-B" not in str(result)
    assert result["ingestion_authorized"] is False
    assert result["point_in_time_eligible"] is False


def test_incomplete_target_day_abstains_instead_of_becoming_zero():
    missing_target = date(2011, 9, 5)
    snapshot, coverage = _snapshot(omit_coverage_day=missing_target)

    result = evaluate_uci_event_time(
        snapshot, complete_event_dates=coverage, split="validation"
    )

    assert result["eligible_product_origin_pairs"] == 31
    assert result["scored_product_origin_pairs"] == 23
    assert result["abstentions"]["target_coverage_unverified"] == 1
    assert result["abstentions"]["history_coverage_unverified"] == 7
    assert result["coverage"] == pytest.approx(23 / 31)


def test_incomplete_history_day_abstains_for_each_affected_origin():
    incomplete_history = date(2011, 9, 3)
    snapshot, coverage = _snapshot(omit_coverage_day=incomplete_history)

    result = evaluate_uci_event_time(
        snapshot, complete_event_dates=coverage, split="validation"
    )

    assert result["scored_product_origin_pairs"] < 31
    assert result["abstentions"]["history_coverage_unverified"] > 0


def test_fit_calendar_must_be_complete_before_freezing_product_cohort():
    snapshot, coverage = _snapshot(omit_coverage_day=FIT_START + timedelta(days=3))

    with pytest.raises(UciEventTimeEvaluationError, match="fit period coverage"):
        evaluate_uci_event_time(
            snapshot, complete_event_dates=coverage, split="validation"
        )


def test_all_zero_targets_keep_wape_undefined_without_zero_division():
    snapshot, coverage = _snapshot(evaluation_rows=False)

    result = evaluate_uci_event_time(
        snapshot, complete_event_dates=coverage, split="validation"
    )

    assert result["scored_product_origin_pairs"] == 31
    for scores in result["metrics"].values():
        assert scores["mae"] >= 0
        assert scores["rmse"] >= 0
        assert scores["wape"] is None


def test_validation_scores_do_not_depend_on_locked_holdout_values():
    first, coverage = _snapshot(holdout_multiplier=1)
    second, _ = _snapshot(holdout_multiplier=10_000)

    first_result = evaluate_uci_event_time(
        first, complete_event_dates=coverage, split="validation"
    )
    second_result = evaluate_uci_event_time(
        second, complete_event_dates=coverage, split="validation"
    )

    assert first_result["metrics"] == second_result["metrics"]
    assert first_result["scored_product_origin_pairs"] == 31


def test_event_time_evaluator_rejects_unsupported_split_and_bad_snapshot():
    snapshot, coverage = _snapshot()
    with pytest.raises(UciEventTimeEvaluationError, match="split"):
        evaluate_uci_event_time(snapshot, complete_event_dates=coverage, split="test")
    with pytest.raises(UciEventTimeEvaluationError, match="snapshot"):
        evaluate_uci_event_time(
            object(), complete_event_dates=coverage, split="validation"
        )


def test_fixed_calendar_matches_the_reviewed_source_window():
    assert FIT_START == date(2010, 12, 1)
    assert FIT_END == date(2011, 8, 30)
    assert SOURCE_START == date(2010, 12, 1)
    assert SOURCE_END == date(2011, 12, 9)
