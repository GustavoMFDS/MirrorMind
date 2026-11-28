"""Offline fictional observatory generation and rendering regressions."""
import os
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

import pytest

from examples import m1_census_research_observatory as observatory

REV = "026a9dd1c71c9640782c7da7b42d8cba73e53858"


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.attrs.append((tag, dict(attrs)))


def test_observatory_offline_reproducible_report():
    a = observatory.build_observatory(REV, ("validation", "holdout"))
    assert a == observatory.build_observatory(REV, ("validation", "holdout"))
    parser = ReportParser()
    parser.feed(a)
    assert parser.tags.count("meter") == 6
    assert parser.tags.count("details") == 4
    assert parser.tags.count("table") == 4
    assert not {"script", "iframe", "form", "link", "img"}.intersection(parser.tags)
    assert all(
        key not in attrs
        for _, attrs in parser.attrs for key in ("src", "srcset", "action")
    )
    assert "Synthetic only" in a and "Inference abstained" in a
    assert "No statistical winner" in a
    assert "21.20" in a and "24.00" in a and "100.0%" in a
    assert "paired_losses" not in a
    assert "default-src &apos;none&apos;" in a
    assert "Experiment provenance" in a
    assert "Self-generated demo commitment" in a


def test_observatory_default_validation_only():
    report = observatory.build_observatory(REV, ("validation",))
    assert 'id="validation"' in report
    assert 'id="holdout"' not in report


def test_observatory_unavailable_metrics_and_escaping():
    h = {"horizon_months": 1, "coverage": 0.0, "metrics": None,
         "scored_origins": 0, "requested_origins": 10,
         "abstentions": {"<script>": 10}}
    split = {"split": "validation", "horizons": (h,), "receipt_sha256": "<img>",
             "stored_replay_matched": True, "receipt_bytes": 10}
    html = observatory._render_split(split)
    assert html.count("Unavailable") == 6
    assert "0.0%" in html
    assert "<script>" not in html and "<img>" not in html
    assert "&lt;script&gt;" in html and "&lt;img&gt;" in html
    assert observatory._number(0) == "0.00"
    with pytest.raises(TypeError):
        observatory._number(True)
    with pytest.raises(ValueError):
        observatory._number(float("nan"))


def test_observatory_cli_exclusive_output(tmp_path):
    root = Path(__file__).resolve().parents[2]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(root / "src")
    target = tmp_path / "report.html"
    args = [sys.executable, "-m", "examples.m1_census_research_observatory",
            "--revision", REV, "--output", str(target)]
    def invoke(command):
        return subprocess.run(command, cwd=root, env=env, check=False,
                              capture_output=True, text=True, timeout=30)
    assert invoke(args).returncode == 0
    original = target.read_bytes()
    assert b"Research Observatory" in original
    assert invoke(args).returncode == 2
    assert target.read_bytes() == original
    assert invoke(args[:-1] + ["relative.html"]).returncode == 2


def test_comparative_observatory_replays_all_scenarios_and_unique_anchors():
    from examples.m1_census_research_runner import SCENARIOS, prepare_report

    html = observatory.build_comparative_observatory(REV, ("validation", "holdout"))
    assert html == observatory.build_comparative_observatory(REV, ("validation", "holdout"))
    parser = ReportParser()
    parser.feed(html)
    ids = [attrs["id"] for _, attrs in parser.attrs if "id" in attrs]
    assert len(ids) == len(set(ids))
    for _, attrs in parser.attrs:
        if attrs.get("href", "").startswith("#"):
            assert attrs["href"][1:] in ids
        if "aria-labelledby" in attrs:
            assert attrs["aria-labelledby"] in ids
    assert parser.tags.count("article") == 4
    assert parser.tags.count("meter") == 24
    assert parser.tags.count("table") == 18
    assert parser.tags.count("details") == 16
    assert not {"script", "iframe", "form", "link", "img"}.intersection(parser.tags)
    for scenario in SCENARIOS:
        assert scenario in ids
        assert scenario + "-validation" in ids
        assert scenario + "-holdout" in ids
        assert prepare_report(REV, scenario)["experiment_sha256"] in html
    assert "Replayed split receipts<strong>8</strong>" in html
    assert "No statistical winner" in html
    assert "no cross-scenario pooling or ranking" in html
    assert "80.00" in html and "64.20" in html
    assert "0.00" in html
    assert "paired_losses" not in html


def test_comparative_prepares_catalog_before_scoring(monkeypatch):
    from examples.m1_census_research_runner import SCENARIOS

    events = []
    prepare = observatory.prepare_report
    run = observatory.run_research

    def prepare_spy(revision, scenario):
        events.append(("prepare", scenario))
        return prepare(revision, scenario)

    def run_spy(revision, **kwargs):
        events.append(("run", kwargs["scenario"]))
        return run(revision, **kwargs)

    monkeypatch.setattr(observatory, "prepare_report", prepare_spy)
    monkeypatch.setattr(observatory, "run_research", run_spy)
    html = observatory.build_comparative_observatory(REV, ("validation",))
    assert events == [("prepare", s) for s in SCENARIOS] + [("run", s) for s in SCENARIOS]
    assert 'id="compare-validation"' in html
    assert 'id="compare-holdout"' not in html
    assert "Replayed split receipts<strong>4</strong>" in html


def test_comparative_cli_no_partial_output_on_failure(tmp_path, monkeypatch):
    target = tmp_path / "comparison.html"
    run = observatory.run_research

    def fail_second(revision, **kwargs):
        if kwargs["scenario"] == "fictional-flat-v1":
            raise ValueError("synthetic failure")
        return run(revision, **kwargs)

    monkeypatch.setattr(observatory, "run_research", fail_second)
    monkeypatch.setattr(sys, "argv", [
        "observatory", "--revision", REV, "--scenario", "all",
        "--split", "both", "--output", str(target),
    ])
    with pytest.raises(SystemExit) as exc:
        observatory.main()
    assert exc.value.code == 2
    assert not target.exists()
