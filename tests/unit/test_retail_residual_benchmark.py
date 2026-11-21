"""Guards for a local-only, revision-bound retrospective benchmark."""
import runpy
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/benchmarks/retail_residual.py"
MODULE = runpy.run_path(str(SCRIPT))


@pytest.mark.parametrize("profile,expected_count", [("dense", 200), ("delayed", 192)])
def test_benchmark_inputs_are_bounded_fictional_release_days(profile, expected_count):
    projection, releases = MODULE["invented_inputs"](profile)
    assert len(projection.days) == len(releases) == expected_count
    assert len({item.observed_on for item in projection.days}) == expected_count
    assert all(item.stock_code == "TOY-ONLY" and 1 <= item.units <= 71
               for item in projection.days)
    assert all(release.observed_on <= release.available_on for release in releases)
    assert "CustomerID" not in str(projection)
    assert "InvoiceNo" not in str(projection)
    assert MODULE["invented_inputs"](profile) == (projection, releases)


def test_benchmark_unknown_profile_fails_before_input_creation():
    with pytest.raises(ValueError, match="dense or delayed"):
        MODULE["invented_inputs"]("real_data")


def test_benchmark_requires_exact_sha_before_git_operations(monkeypatch, tmp_path):
    module = MODULE["validate_checkout"]
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(args)
        raise AssertionError("should not spawn git on malformed sha")

    monkeypatch.setattr(module.__globals__["subprocess"], "run", forbidden)
    with pytest.raises(ValueError, match="40-digit"):
        module(tmp_path, "a" * 39)
    assert calls == []


def test_receipt_fingerprint_is_stable_and_detects_changes():
    fp = MODULE["fingerprint"]
    assert fp({"x": 1, "y": [2, 3]}) == fp({"y": [2, 3], "x": 1})
    assert fp({"x": 1}) != fp({"x": 2})
