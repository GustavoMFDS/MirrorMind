"""Check deterministic benchmark contracts and release preparation boundaries."""
import hashlib
import json
import re

import pytest

from examples import prepare_alpha_release as release
from examples.synthetic_benchmark import measure


def test_benchmark_reports_fixed_deterministic_workloads():
    report = measure(2)
    assert report["synthetic_only"] is True
    assert report["timing_gate"] is False
    assert report["repeats"] == 2
    assert len(report["workloads"]) == 3
    for workload in report["workloads"]:
        assert len(workload["samples_ns"]) == 2
        assert 0 <= workload["min_ns"] <= workload["median_ns"] <= workload["max_ns"]
        assert re.fullmatch(r"[0-9a-f]{64}", workload["output_sha256"])


@pytest.mark.parametrize("value", [True, 0, 21])
def test_benchmark_rejects_unbounded_repeats(value):
    with pytest.raises(ValueError):
        measure(value)


def test_release_bundle_is_synthetic_and_non_authorizing(tmp_path, monkeypatch):
    sha = "a" * 40
    monkeypatch.setattr(release, "git", lambda *args: sha if args[0] == "rev-parse" else "")
    out = tmp_path / "bundle"
    release.prepare(out, sha)
    assert {p.name for p in out.iterdir()} == {
        "mirror-demo.html", "SHA256SUMS.txt", "release-candidate.json",
    }
    receipt = json.loads((out / "release-candidate.json").read_text(encoding="utf-8"))
    assert receipt["source_sha"] == sha
    assert receipt["synthetic_only"] is True
    assert receipt["publication_authorized"] is False
    assert receipt["official_ci_verified"] is False
    digest = hashlib.sha256((out / "mirror-demo.html").read_bytes()).hexdigest()
    assert receipt["report_sha256"] == digest
    with pytest.raises(ValueError):
        release.prepare(out, sha)


def test_release_rejects_dirty_or_mismatched_checkout(tmp_path, monkeypatch):
    sha = "a" * 40
    out = tmp_path / "bundle"
    monkeypatch.setattr(release, "git", lambda *args: "b" * 40)
    with pytest.raises(ValueError):
        release.prepare(out, sha)
    monkeypatch.setattr(release, "git", lambda *args: sha if args[0] == "rev-parse" else "dirty")
    with pytest.raises(ValueError):
        release.prepare(out, sha)
    assert not out.exists()
