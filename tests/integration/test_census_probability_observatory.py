"""Offline probability observatory report and failure behavior."""
import sys
from html.parser import HTMLParser

import pytest

from examples import m1_census_probability_observatory as obs
from examples import m1_census_probability_study as study

REV = "d8d817d4f7cdd6be497a44e75bea6482f426de73"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_probability_observatory_replayed_metrics_and_examples():
    html = obs.build_observatory(REV)
    assert html == obs.build_observatory(REV)
    parser = Parser()
    parser.feed(html)
    tags = parser.tags
    assert sum(tag == "table" for tag, _ in tags) == 2
    assert sum(tag == "details" for tag, _ in tags) == 40
    assert not {"script", "iframe", "link", "img", "form"}.intersection(tag for tag, _ in tags)
    ids = [a["id"] for _, a in tags if "id" in a]
    assert len(ids) == len(set(ids))
    assert all(a["href"][1:] in ids for _, a in tags if a.get("href", "").startswith("#"))
    assert all("src" not in a and "srcset" not in a for _, a in tags)
    assert "Model-event scores<strong>9600</strong>" in html
    assert "Observed coverage" in html and "Reference coverage" in html
    assert "Synthetic only" in html and "No statistical winner" in html
    assert "Path 0, origin 52, horizon 6 months" in html
    assert html.count("Oracle (privileged reference) distribution") == 2
    expected = study.prepare_study(REV)["study_sha256"]
    report = study.execute_study(REV, expected)
    assert report["report_sha256"] in html
    for group in report["groups"]:
        assert group["event_transcript_sha256"] in html
        for row in group["rows"]:
            for field in study.FIELDS:
                assert f'Exact: {row[field]}' in html
    assert sum(tag == "meter" for tag, _ in tags) > 10
    assert all(0 <= float(a["value"]) <= 1 for tag, a in tags if tag == "meter")


def test_probability_observatory_example_point_mass():
    html = obs._example("stationary", 61001)
    assert "Displacement 0 probability" in html
    assert "100.00%" in html
    assert "10/50/90 quantiles: 0, 0, 0" in html
    path = study._path("stationary", 61001, 0)
    observed = sum(path[53:59])
    assert f"Realized displacement: <strong>{observed:+d}</strong>" in html


def test_probability_observatory_cli_exclusive_output(tmp_path, monkeypatch):
    target = tmp_path / "report.html"
    monkeypatch.setattr(sys, "argv", [
        "observatory", "--revision", REV, "--output", str(target)
    ])
    assert obs.main() == 0
    original = target.read_bytes()
    with pytest.raises(SystemExit) as exc:
        obs.main()
    assert exc.value.code == 2
    assert target.read_bytes() == original


def test_probability_observatory_replay_failure_no_output(tmp_path, monkeypatch):
    target = tmp_path / "report.html"
    monkeypatch.setattr(study, "verify_study", lambda *args: "f" * 64)
    monkeypatch.setattr(sys, "argv", [
        "observatory", "--revision", REV, "--output", str(target)
    ])
    with pytest.raises(SystemExit) as exc:
        obs.main()
    assert exc.value.code == 2
    assert not target.exists()
