"""Synthetic observation preflight is bounded, deterministic and not an importer."""
import copy
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location("mm_synthetic_preflight", ROOT / "examples/m1_observation_preflight.py")
assert SPEC is not None and SPEC.loader is not None
preflight = module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


def fixture():
    return json.loads((ROOT / "examples/synthetic-daily-sales.json").read_text(encoding="utf-8"))


def test_synthetic_batch_is_bounded_and_reports_gaps_without_imputation():
    original = fixture()
    data = copy.deepcopy(original)
    summary = preflight.validate_batch(data)
    assert summary == {
        "status": "synthetic_structure_validated_not_forecast",
        "series_id": "retail.synthetic.store-01.item-01",
        "source_status": "synthetic_unverified",
        "cutoff_date": "2025-01-08",
        "first_date": "2025-01-01",
        "last_date": "2025-01-08",
        "record_count": 4,
        "missing_day_count": 4,
        "total_observed_units": 13,
    }
    assert data == original
    data["records"].reverse()
    assert preflight.validate_batch(data) == summary


def test_cutoff_rejects_future_dated_observation():
    data = fixture()
    data["records"][-1]["date"] = "2025-01-09"
    with pytest.raises(ValueError, match="exceeds declared cutoff"):
        preflight.validate_batch(data)


def test_duplicate_calendar_day_rejected():
    data = fixture()
    data["records"][-1]["date"] = data["records"][0]["date"]
    with pytest.raises(ValueError, match="duplicate observation date"):
        preflight.validate_batch(data)


@pytest.mark.parametrize("invalid", [True, -1, 3.5, 1_000_000_001, "8", None])
def test_units_require_exact_nonnegative_bounded_integers(invalid):
    data = fixture()
    data["records"][0]["units"] = invalid
    with pytest.raises(ValueError, match="units must be an exact"):
        preflight.validate_batch(data)


@pytest.mark.parametrize("invalid", ["2025-02-30", "2025-1-2", "", None, True])
def test_calendar_date_is_valid_canonical_day(invalid):
    data = fixture()
    data["records"][0]["date"] = invalid
    with pytest.raises(ValueError, match="record 0 date"):
        preflight.validate_batch(data)


def test_missing_extra_and_incompatible_schema_fail_closed():
    data = fixture()
    data["unreviewed"] = 1
    with pytest.raises(ValueError, match="unexpected or missing"):
        preflight.validate_batch(data)
    data.pop("unreviewed")
    data["schema_version"] = "1.0"
    with pytest.raises(ValueError, match="unsupported"):
        preflight.validate_batch(data)


def test_explicit_record_limit_prevents_unbounded_input():
    data = fixture()
    with pytest.raises(ValueError, match="bounded nonempty array"):
        preflight.validate_batch(data, max_records=3)
    with pytest.raises(ValueError, match="exact integer"):
        preflight.validate_batch(data, max_records=True)


def test_duplicate_json_keys_are_not_silently_overwritten():
    with pytest.raises(ValueError, match="duplicate JSON object key"):
        json.loads('{"a": 1, "a": 2}', object_pairs_hook=preflight._no_duplicate_keys)
