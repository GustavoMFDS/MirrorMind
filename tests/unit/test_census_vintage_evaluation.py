from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from mirrormind.domains.retail.census_evaluation import (
    MAX_CENSUS_EVALUATION_ORIGINS,
    CensusForecastOrigin,
    evaluate_census_vintage_backtest,
)
from mirrormind.domains.retail.census_vintages import CensusVintageRecord


def _next_month(month: date) -> date:
    return date(month.year + (month.month == 12), month.month % 12 + 1, 1)


def _add_months(month: date, count: int) -> date:
    ordinal = month.year * 12 + month.month - 1 + count
    return date(ordinal // 12, ordinal % 12 + 1, 1)


def _records(*, values: dict[date, str] | None = None) -> tuple[CensusVintageRecord, ...]:
    values = values or {}
    rows = []
    month = date(2020, 1, 1)
    end = date(2021, 7, 1)
    index = 0
    while month <= end:
        rows.append(CensusVintageRecord(
            series_id="RSAFS",
            reference_month=month,
            value=Decimal(values.get(month, "100")),
            published_on=date(_next_month(month).year, _next_month(month).month, 15),
            release_kind="first_estimate",
            release_id=f"first-{month:%Y-%m}",
            snapshot_sha256=f"{index:064x}",
        ))
        month = _next_month(month)
        index += 1
    return tuple(rows)


def _origins() -> tuple[CensusForecastOrigin, ...]:
    return (
        CensusForecastOrigin(date(2020, 12, 1), date(2021, 1, 16)),
        CensusForecastOrigin(date(2021, 1, 1), date(2021, 2, 16)),
    )


def _evaluate(
    records: tuple[CensusVintageRecord, ...],
    origins: tuple[CensusForecastOrigin, ...] | None = None,
):
    return evaluate_census_vintage_backtest(
        records,
        series_id="RSAFS",
        origins=_origins() if origins is None else origins,
        split="validation",
    )


def _horizon(result: dict[str, object], months: int) -> dict[str, object]:
    horizons = result["horizons"]
    assert isinstance(horizons, tuple)
    match = next(item for item in horizons if item["horizon_months"] == months)
    assert isinstance(match, dict)
    return match


def test_fixed_horizons_use_asof_vintages_and_matched_first_estimates():
    values = {
        date(2021, 1, 1): "110",
        date(2021, 2, 1): "120",
        date(2021, 3, 1): "130",
        date(2021, 4, 1): "140",
        date(2021, 6, 1): "160",
        date(2021, 7, 1): "170",
    }
    result = _evaluate(_records(values=values))

    assert result["status"] == "aggregate_vintage_backtest_unverified"
    assert result["source_status"] == "caller_supplied_not_source_verified"
    assert result["input_record_count"] == 19
    assert result["ingestion_authorized"] is False
    assert result["forecast_eligible"] is False
    assert [item["horizon_months"] for item in result["horizons"]] == [1, 3, 6]
    one_month = _horizon(result, 1)
    assert one_month["scored_origins"] == 2
    assert one_month["coverage"] == 1.0
    assert one_month["metrics"]["seasonal_naive_lag12"]["mae"] == 15.0
    assert one_month["metrics"]["trailing_12_month_mean"]["mae"] == pytest.approx(
        14.583333333333334
    )
    assert one_month["metrics"]["seasonal_naive_lag12"]["wape"] == pytest.approx(
        30 / 230
    )
    assert one_month["metrics"]["trailing_12_month_mean"]["wape"] == pytest.approx(
        (10 + 230 / 12) / 230
    )
    assert set(one_month["metrics"]) == {
        "seasonal_naive_lag12", "trailing_12_month_mean"
    }

    first_origin = result["origin_audit"][0]
    assert first_origin["as_of_vintage_receipt"]["publication_cutoff"] == "2021-01-16"
    assert "as_of_vintage_manifest_sha256" in first_origin["as_of_vintage_receipt"]
    assert "selected_release_ids" not in first_origin["as_of_vintage_receipt"]
    assert "selected_snapshot_sha256s" not in first_origin["as_of_vintage_receipt"]
    assert first_origin["horizon_results"][0]["target_release_id"] == "first-2021-01"
    assert "value" not in repr(result)
    assert "prediction" not in repr(result)


def test_revision_published_before_origin_changes_only_that_asof_vintage():
    records = _records()
    revision = replace(
        records[10],
        value=Decimal(999),
        published_on=date(2021, 2, 1),
        release_kind="monthly_revision",
        release_id="revision-2020-11",
        snapshot_sha256="f" * 64,
    )

    baseline = _evaluate(records)
    revised = _evaluate((*records, revision))
    before, after = baseline["origin_audit"]
    revised_before, revised_after = revised["origin_audit"]

    assert before["as_of_vintage_manifest_sha256"] == revised_before[
        "as_of_vintage_manifest_sha256"
    ]
    assert after["as_of_vintage_manifest_sha256"] != revised_after[
        "as_of_vintage_manifest_sha256"
    ]
    assert _horizon(baseline, 1)["metrics"] != _horizon(revised, 1)["metrics"]


def test_later_revision_does_not_change_any_prior_origin_score():
    records = _records()
    later_revision = replace(
        records[10],
        value=Decimal(999999),
        published_on=date(2021, 3, 1),
        release_kind="monthly_revision",
        release_id="revision-2020-11-later",
        snapshot_sha256="e" * 64,
    )

    baseline = _evaluate(records)
    revised = _evaluate((*records, later_revision))

    assert baseline["horizons"] == revised["horizons"]
    assert baseline["origin_audit"] == revised["origin_audit"]
    assert baseline["input_manifest_sha256"] != revised["input_manifest_sha256"]


def test_same_day_revision_is_excluded_from_date_only_origin():
    records = _records()
    same_day_revision = replace(
        records[10],
        value=Decimal(999),
        published_on=date(2021, 2, 16),
        release_kind="monthly_revision",
        release_id="revision-2020-11-same-day",
        snapshot_sha256="d" * 64,
    )

    baseline = _evaluate(records)
    same_day = _evaluate((*records, same_day_revision))

    assert baseline["horizons"] == same_day["horizons"]
    assert baseline["origin_audit"] == same_day["origin_audit"]


def test_incomplete_trailing_history_abstains_without_filling_months():
    records = tuple(
        record for record in _records()
        if record.reference_month != date(2020, 8, 1)
    )

    result = _evaluate(records)

    assert result["status"] == "aggregate_vintage_backtest_abstained"
    for horizon in result["horizons"]:
        assert horizon["scored_origins"] == 0
        assert horizon["metrics"] is None
        assert horizon["abstentions"]["required_monthly_history_unavailable"] == 2


def test_missing_first_estimate_target_abstains_and_minimum_count_is_two():
    records = tuple(
        record for record in _records()
        if record.reference_month != date(2021, 3, 1)
    )

    result = _evaluate(records)
    three_months = _horizon(result, 3)

    assert three_months["scored_origins"] == 1
    assert three_months["abstentions"]["target_first_estimate_missing"] == 1
    assert three_months["metrics"] is None


def test_zero_actual_denominator_produces_null_wape():
    zero_months = {
        date(2021, 1, 1): "0", date(2021, 2, 1): "0",
        date(2021, 3, 1): "0", date(2021, 4, 1): "0",
        date(2021, 6, 1): "0", date(2021, 7, 1): "0",
    }

    result = _evaluate(_records(values=zero_months))

    for horizon in result["horizons"]:
        for metrics in horizon["metrics"].values():
            assert metrics["wape"] is None


@pytest.mark.parametrize("issued_on", (date(2021, 2, 15), date(2021, 2, 20)))
def test_target_already_published_at_issue_is_not_scored(issued_on):
    late_origin = (CensusForecastOrigin(date(2020, 12, 1), issued_on),)

    result = _evaluate(_records(), late_origin)
    one_month = _horizon(result, 1)

    assert one_month["scored_origins"] == 0
    assert one_month["metrics"] is None
    assert one_month["abstentions"]["target_not_future_at_origin"] == 1


def test_future_reference_rows_outside_requested_targets_fail_closed():
    records = _records()
    impossible_future_row = replace(
        records[15],
        published_on=date(2021, 1, 10),
        release_kind="monthly_revision",
        release_id="future-month-before-origin",
        snapshot_sha256="c" * 64,
    )

    with pytest.raises(ValueError, match="future reference month"):
        _evaluate((*records, impossible_future_row))


def test_origins_must_be_unique_chronological_and_split_is_explicit():
    duplicate = (_origins()[0], _origins()[0])
    with pytest.raises(ValueError, match="unique reference months"):
        _evaluate(_records(), duplicate)

    with pytest.raises(ValueError, match="chronological order"):
        _evaluate(_records(), tuple(reversed(_origins())))

    with pytest.raises(ValueError, match="split must be validation or holdout"):
        evaluate_census_vintage_backtest(
            _records(), series_id="RSAFS", origins=_origins(), split="test"
        )


def test_origin_count_budget_is_enforced_before_evaluation():
    origins = tuple(
        CensusForecastOrigin(
            _add_months(date(2020, 1, 1), index),
            date(
                _next_month(_add_months(date(2020, 1, 1), index)).year,
                _next_month(_add_months(date(2020, 1, 1), index)).month,
                16,
            ),
        )
        for index in range(MAX_CENSUS_EVALUATION_ORIGINS + 1)
    )

    with pytest.raises(ValueError, match="bounded nonempty tuple"):
        _evaluate(_records(), origins)


def test_metric_range_rejects_values_that_cannot_be_scored_safely():
    oversized_targets = {
        date(2021, 1, 1): "1e151",
        date(2021, 2, 1): "1e151",
    }

    with pytest.raises(ValueError, match="supported metric range"):
        _evaluate(_records(values=oversized_targets))


def test_two_first_estimate_labels_for_one_month_are_rejected():
    records = _records()
    duplicate_label = replace(
        records[12],
        published_on=date(2021, 2, 16),
        release_id="second-first-estimate",
        snapshot_sha256="b" * 64,
    )

    with pytest.raises(ValueError, match="unique first-estimate label"):
        _evaluate((*records, duplicate_label))


def test_origin_first_estimate_must_be_available_before_issue():
    same_day_origin = (CensusForecastOrigin(date(2020, 12, 1), date(2021, 1, 15)),)

    result = _evaluate(_records(), same_day_origin)

    assert _horizon(result, 1)["scored_origins"] == 0
    assert _horizon(result, 1)["abstentions"]["origin_not_published_at_issue"] == 1
