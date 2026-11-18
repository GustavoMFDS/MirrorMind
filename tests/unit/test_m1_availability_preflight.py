"""Synthetic publication-time exclusion must not leak late observations."""
import copy
import json
from pathlib import Path

import pytest

from examples import m1_availability_preflight as availability

ROOT = Path(__file__).resolve().parents[2]


def fixture():
    return json.loads((ROOT / "examples/synthetic-asof-sales.json").read_text(encoding="utf-8"))


def test_late_publication_is_excluded_even_when_event_date_precedes_cutoff():
    original = fixture()
    data = copy.deepcopy(original)
    result = availability.asof_batch(data)
    assert data == original
    assert result["status"] == "synthetic_availability_filtered_not_verified_evidence"
    assert result["as_of_date"] == "2025-01-06"
    assert result["eligible_count"] == 5
    assert result["excluded_late_available_count"] == 1
    assert result["excluded_future_event_count"] == 1
    assert result["gaps_within_eligible_span"] == 1
    assert result["eligible_observed_units"] == 36
    data["records"].reverse()
    assert availability.asof_batch(data) == result


def test_changing_cutoff_to_when_late_value_arrived_makes_it_eligible():
    data = fixture()
    data["as_of_date"] = "2025-01-08"
    result = availability.asof_batch(data)
    assert result["eligible_count"] == 7
    assert result["eligible_observed_units"] == 56
    assert result["gaps_within_eligible_span"] == 0
    assert result["excluded_late_available_count"] == 0
    assert result["excluded_future_event_count"] == 0


def test_unavailable_value_change_cannot_change_eligible_aggregate():
    data = fixture()
    original_result = availability.asof_batch(data)
    # January 3 was not available until January 8, after the cutoff.
    data["records"][2]["units"] = 999
    assert availability.asof_batch(data) == original_result


def test_published_before_observation_rejected():
    data = fixture()
    data["records"][0]["available_on"] = "2024-12-31"
    with pytest.raises(ValueError, match="publication precedes observation"):
        availability.asof_batch(data)


def test_duplicate_dates_fail_even_when_one_row_is_not_available():
    data = fixture()
    data["records"][2]["observed_on"] = "2025-01-02"
    with pytest.raises(ValueError, match="duplicate observed date"):
        availability.asof_batch(data)


@pytest.mark.parametrize("bad", [True, -1, 1.1, "7", None, 1_000_000_001])
def test_units_must_be_exact_bounded_integers(bad):
    data = fixture()
    data["records"][0]["units"] = bad
    with pytest.raises(ValueError, match="exact bounded nonnegative"):
        availability.asof_batch(data)


def test_empty_asof_snapshot_abstains():
    data = fixture()
    data["as_of_date"] = "2024-12-30"
    with pytest.raises(ValueError, match="no eligible"):
        availability.asof_batch(data)


def test_unknown_fields_and_schema_fail_closed():
    data = fixture()
    data["unexpected"] = "ignored?"
    with pytest.raises(ValueError, match="invalid synthetic availability envelope"):
        availability.asof_batch(data)
    data.pop("unexpected")
    data["schema_version"] = "unreviewed-v2"
    with pytest.raises(ValueError, match="unsupported"):
        availability.asof_batch(data)


def test_invalid_dates_are_never_silently_repaired():
    data = fixture()
    data["records"][1]["available_on"] = "2025-02-31"
    with pytest.raises(ValueError, match="valid calendar date"):
        availability.asof_batch(data)


def test_wrong_source_label_rejected_without_authentication_claim():
    data = fixture()
    data["source_id"] = "real-financial-customer-data"
    with pytest.raises(ValueError, match="explicitly labeled synthetic"):
        availability.asof_batch(data)
