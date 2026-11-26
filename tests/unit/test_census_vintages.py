from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from mirrormind.domains.retail.census_vintages import (
    MAX_VINTAGE_RECORDS,
    CensusVintageRecord,
    select_census_vintage_as_of,
)


def _record(
    reference_month: date,
    published_on: date,
    value: str,
    release_kind: str,
    release_id: str,
    snapshot_sha256: str,
    *,
    series_id: str = "RSAFS",
) -> CensusVintageRecord:
    return CensusVintageRecord(
        series_id=series_id,
        reference_month=reference_month,
        value=Decimal(value),
        published_on=published_on,
        release_kind=release_kind,
        release_id=release_id,
        snapshot_sha256=snapshot_sha256,
    )


def test_selects_latest_revision_per_month_strictly_before_target_release():
    records = (
        _record(date(2020, 4, 1), date(2020, 5, 15), "100.0", "first_estimate",
                "release-may", "a" * 64),
        _record(date(2020, 4, 1), date(2020, 6, 15), "101.0", "monthly_revision",
                "release-june", "b" * 64),
        _record(date(2020, 4, 1), date(2021, 1, 12), "102.0", "annual_revision",
                "release-annual", "c" * 64),
        _record(date(2020, 5, 1), date(2020, 6, 15), "110.0", "first_estimate",
                "release-june", "b" * 64),
    )

    view = select_census_vintage_as_of(
        records, series_id="RSAFS", target_release_on=date(2020, 7, 15)
    )

    assert [(item.reference_month, item.value, item.release_kind) for item in view.records] == [
        (date(2020, 4, 1), Decimal("101.0"), "monthly_revision"),
        (date(2020, 5, 1), Decimal("110.0"), "first_estimate"),
    ]
    assert {item.release_id for item in view.records} == {"release-june"}
    assert {item.snapshot_sha256 for item in view.records} == {"b" * 64}
    assert view.target_release_on == date(2020, 7, 15)


def test_same_day_first_estimate_is_excluded_and_receipt_is_unverified():
    records = (
        _record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                "release-may", "a" * 64),
    )

    view = select_census_vintage_as_of(
        records, series_id="RSAFS", target_release_on=date(2020, 5, 15)
    )

    assert view.records == ()
    receipt = view.receipt()
    assert receipt["status"] == "aggregate_vintage_selection_abstained"
    assert receipt["source_status"] == "caller_supplied_not_source_verified"
    assert receipt["publication_cutoff"] == "2020-05-15"
    assert receipt["ingestion_authorized"] is False
    assert receipt["forecast_eligible"] is False


def test_revision_before_known_first_estimate_is_rejected():
    records = (
        _record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                "release-may", "a" * 64),
        _record(date(2020, 4, 1), date(2020, 5, 14), "99", "monthly_revision",
                "release-before-first", "b" * 64),
    )

    with pytest.raises(
        ValueError,
        match="revision publication must follow first-estimate publication",
    ):
        select_census_vintage_as_of(
            records, series_id="RSAFS", target_release_on=date(2020, 6, 15)
        )


@pytest.mark.parametrize(
    "release_kind", ("first_estimate", "monthly_revision", "annual_revision")
)
def test_release_cannot_precede_close_of_reference_month(release_kind):
    record = _record(
        date(2020, 4, 1), date(2020, 4, 30), "100", release_kind,
        "release-before-period-close", "a" * 64,
    )

    with pytest.raises(ValueError, match="publication date must follow the reference month"):
        select_census_vintage_as_of(
            (record,), series_id="RSAFS", target_release_on=date(2020, 6, 1)
        )


def test_release_on_first_day_after_reference_month_is_valid_boundary():
    record = _record(
        date(2020, 4, 1), date(2020, 5, 1), "100", "first_estimate",
        "release-after-period-close", "a" * 64,
    )

    view = select_census_vintage_as_of(
        (record,), series_id="RSAFS", target_release_on=date(2020, 5, 2)
    )

    assert view.records == (record,)


def test_missing_reference_months_remain_absent_and_replay_is_deterministic():
    records = (
        _record(date(2020, 1, 1), date(2020, 2, 14), "80", "first_estimate",
                "release-feb", "a" * 64),
        _record(date(2020, 3, 1), date(2020, 4, 14), "90", "first_estimate",
                "release-apr", "b" * 64),
    )

    first = select_census_vintage_as_of(
        records, series_id="RSAFS", target_release_on=date(2020, 5, 15)
    )
    replay = select_census_vintage_as_of(
        records, series_id="RSAFS", target_release_on=date(2020, 5, 15)
    )

    assert [item.reference_month for item in first.records] == [
        date(2020, 1, 1), date(2020, 3, 1)
    ]
    assert first == replay
    assert first.receipt() == replay.receipt()


def test_duplicate_period_and_publication_date_is_rejected_as_ambiguous():
    records = (
        _record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                "release-may-a", "a" * 64),
        _record(date(2020, 4, 1), date(2020, 5, 15), "101", "monthly_revision",
                "release-may-b", "b" * 64),
    )

    with pytest.raises(ValueError, match="ambiguous publication date"):
        select_census_vintage_as_of(
            records, series_id="RSAFS", target_release_on=date(2020, 6, 15)
        )


def test_release_id_cannot_bind_conflicting_publication_metadata():
    records = (
        _record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                "release-may", "a" * 64),
        _record(date(2020, 5, 1), date(2020, 6, 15), "110", "first_estimate",
                "release-may", "b" * 64),
    )

    with pytest.raises(ValueError, match="conflicting release metadata"):
        select_census_vintage_as_of(
            records, series_id="RSAFS", target_release_on=date(2020, 7, 15)
        )


@pytest.mark.parametrize(
    "changed, message",
    (
        (replace(_record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                         "release-may", "a" * 64), reference_month=date(2020, 4, 2)),
         "reference_month must be the first day"),
        (replace(_record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                         "release-may", "a" * 64), value=Decimal("NaN")),
         "value must be a finite non-negative Decimal"),
        (replace(_record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                         "release-may", "a" * 64), release_kind="final"),
         "unsupported release_kind"),
        (replace(_record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                         "release-may", "a" * 64), snapshot_sha256="not-a-digest"),
         "snapshot_sha256 must be lowercase SHA-256"),
    ),
)
def test_invalid_normalized_vintage_record_is_rejected(changed, message):
    with pytest.raises(ValueError, match=message):
        select_census_vintage_as_of(
            (changed,), series_id="RSAFS", target_release_on=date(2020, 6, 15)
        )


def test_mixed_series_is_rejected_before_selection():
    records = (
        _record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                "release-may", "a" * 64),
        _record(date(2020, 4, 1), date(2020, 5, 15), "50", "first_estimate",
                "another-series", "b" * 64, series_id="OTHER"),
    )

    with pytest.raises(ValueError, match="records must belong to the selected series"):
        select_census_vintage_as_of(
            records, series_id="RSAFS", target_release_on=date(2020, 6, 15)
        )


def test_input_record_budget_is_enforced_before_selection():
    record = _record(date(2020, 4, 1), date(2020, 5, 15), "100", "first_estimate",
                     "release-may", "a" * 64)
    records = (record,) * (MAX_VINTAGE_RECORDS + 1)

    with pytest.raises(ValueError, match="record limit"):
        select_census_vintage_as_of(
            records, series_id="RSAFS", target_release_on=date(2020, 6, 15)
        )
