"""Synthetic prequential envelope tests: no hindsight or calibrated claims."""
from datetime import date, datetime, timedelta

import pytest

from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
from mirrormind.domains.retail.residual_envelope import evaluate_retail_residual_envelopes
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

START = date(2011, 1, 1)


def day(index):
    return START + timedelta(days=index - 1)


def fixture(*, late60=False, value60=4, missing68=False, withheld70=False):
    rows = []
    releases = []
    for index in range(1, 71):
        if missing68 and index == 68:
            continue
        event = day(index)
        units = value60 if index == 60 else (index % 7) + 1
        rows.append({
            "InvoiceNo": str(500000 + index),
            "StockCode": "PRIVATE-SKU",
            "InvoiceDate": datetime(event.year, event.month, event.day, 10),
            "Quantity": units,
            "CustomerID": "NEVER-COPY",
        })
        published = (
            day(70) if late60 and index == 60
            else day(71) if withheld70 and index == 70
            else event
        )
        releases.append(DeclaredProductRelease("PRIVATE-SKU", event, published))
    return project_uci_retail_rows(rows), tuple(releases)


def evaluate(projection, releases, **kwargs):
    return evaluate_retail_residual_envelopes(
        projection, releases, stock_code="PRIVATE-SKU",
        evaluation_on=day(70), **kwargs,
    )


def test_fully_published_example_reports_retrospective_not_nominal_coverage():
    projection, releases = fixture()
    result = evaluate(projection, releases)
    assert result["evaluated_origins"] == 7
    assert result["retrospective_coverage_denominator"] == 7
    assert 0 <= result["retrospective_covered_origins"] <= 7
    assert result["calibrated_prediction_interval"] is None
    assert result["nominal_coverage"] is None
    assert result["uncertainty_status"] == "heuristic_envelope_not_prediction_interval"
    assert len(result["origin_audit"]) == result["requested_origins"] == 7
    for forbidden in ("PRIVATE-SKU", "NEVER-COPY", "500001"):
        assert forbidden not in str(result)


def test_delayed_historical_value_is_unavailable_for_forecast_and_calibration():
    first, releases = fixture(late60=True, value60=4, withheld70=True)
    changed, other_releases = fixture(late60=True, value60=999_999, withheld70=True)
    assert releases == other_releases
    initial = evaluate(first, releases)
    mutated = evaluate(changed, other_releases)
    assert initial == mutated
    assert initial["evaluated_origins"] == 2
    assert initial["abstained_forecast_history"] == 4
    assert initial["abstained_unpublished_target"] == 1
    assert initial["retrospective_coverage_denominator"] == 2
    assert initial["calibrated_prediction_interval"] is None


def test_calibration_abstains_instead_of_claiming_small_sample_uncertainty():
    projection, releases = fixture(late60=True)
    result = evaluate(
        projection, releases, holdout_days=2,
        calibration_days=10, min_calibration_residuals=10,
    )
    assert result["evaluated_origins"] == 0
    assert result["abstained_calibration"] == 2
    assert result["retrospective_coverage_denominator"] == 0
    assert result["calibrated_prediction_interval"] is None


def test_missing_target_is_not_zero_and_never_in_denominator():
    projection, releases = fixture(missing68=True)
    result = evaluate(projection, releases, holdout_days=3)
    assert result["abstained_missing_target"] == 1
    assert result["evaluated_origins"] <= 2
    assert any(row["status"] == "target_missing_not_zero"
               for row in result["origin_audit"])


def test_incomplete_release_declarations_fail_closed():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="each positive product-day"):
        evaluate(projection, releases[:-1])


@pytest.mark.parametrize("option,value,error", [
    ("holdout_days", True, "holdout_days"),
    ("holdout_days", 31, "holdout_days"),
    ("calibration_days", 61, "calibration_days"),
    ("calibration_days", 4, "calibration_days"),
    ("min_calibration_residuals", 2, "min_calibration_residuals"),
    ("min_calibration_residuals", 22, "min_calibration_residuals"),
])
def test_bounded_exact_configuration(option, value, error):
    projection, releases = fixture()
    with pytest.raises(ValueError, match=error):
        evaluate(projection, releases, **{option: value})


def test_datetime_is_not_accepted_as_calendar_date():
    projection, releases = fixture()
    with pytest.raises(ValueError, match="exact date"):
        evaluate_retail_residual_envelopes(
            projection, releases, stock_code="PRIVATE-SKU",
            evaluation_on=datetime(2011, 3, 11),
        )
