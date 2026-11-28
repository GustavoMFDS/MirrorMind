"""Offline bivariate observatory regressions."""

import sys
from fractions import Fraction
from html.parser import HTMLParser

import pytest

from examples import m1_census_bivariate_observatory as obs
from examples import m1_census_bivariate_study as study

REV = "47e63d9c6e4ffeedcd260e1070f7cccc10be59af"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


@pytest.fixture(scope="module")
def html():
    return obs.build_observatory(REV)


def test_bivariate_observatory_replayed_report_and_matrices(html):
    p = Parser()
    p.feed(html)
    tags = p.tags
    assert sum(t == "table" for t, _ in tags) == 52
    assert sum(t == "details" for t, _ in tags) == 64
    assert sum(t == "table" and a.get("class") == "heat" for t, a in tags) == 16
    assert not {"script", "iframe", "img", "link", "form"}.intersection(t for t, _ in tags)
    assert all("src" not in a and "srcset" not in a for _, a in tags)
    ids = [a["id"] for _, a in tags if "id" in a]
    assert len(ids) == len(set(ids))
    assert all(a["href"][1:] in ids for _, a in tags if a.get("href", "").startswith("#"))
    assert "Model-event scores<strong>7680</strong>" in html
    assert "Synthetic only" in html and "No statistical winner" in html
    assert html.count("Path 0, origin 52, horizon 6 months") == 4
    report = study.execute_study(REV, study.prepare_study(REV)["study_sha256"])
    assert report["report_sha256"] in html
    for group in report["groups"]:
        assert group["event_transcript_sha256"] in html
        for row in group["rows"]:
            assert all(f"Exact: {row[k]}" in html for k in study.FIELDS)


def test_heatmap_exact_mass_and_missing_cell():
    p = Parser()
    p.feed(obs._heatmap(((-4, -4, 1), (4, 4, 3)), "Test"))
    masses = [Fraction(a["title"].removeprefix("Exact: ")) for t, a in p.tags if t == "td"]
    assert sorted(masses) == [0, 0, Fraction(1, 4), Fraction(3, 4)]
    assert sum(masses) == 1


def test_bivariate_observatory_exclusive_output(tmp_path, monkeypatch, html):
    target = tmp_path / "report.html"
    monkeypatch.setattr(obs, "build_observatory", lambda _: html)
    monkeypatch.setattr(sys, "argv", ["obs", "--revision", REV, "--output", str(target)])
    assert obs.main() == 0
    original = target.read_bytes()
    with pytest.raises(SystemExit) as exc:
        obs.main()
    assert exc.value.code == 2
    assert target.read_bytes() == original


def test_bivariate_observatory_replay_failure(tmp_path, monkeypatch):
    target = tmp_path / "report.html"
    monkeypatch.setattr(study, "verify_study", lambda *args: "f" * 64)
    monkeypatch.setattr(sys, "argv", ["obs", "--revision", REV, "--output", str(target)])
    with pytest.raises(SystemExit) as exc:
        obs.main()
    assert exc.value.code == 2
    assert not target.exists()
