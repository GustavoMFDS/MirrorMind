import sys
from fractions import Fraction
from html.parser import HTMLParser

import pytest

from examples import m1_census_temporal_observatory as obs
from examples import m1_census_temporal_study as study

REV = "cc1aa3eb926a2d7159a27c73e0a4341e15ec6b1b"


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


@pytest.fixture(scope="module")
def html():
    return obs.build_observatory(REV)


def test_temporal_observatory_replay_and_matrices(html):
    p = Parser()
    p.feed(html)
    tags = p.tags
    assert sum(t == "table" for t, _ in tags) == 104
    assert sum(t == "table" and a.get("class") == "transition" for t, a in tags) == 40
    assert sum(t == "table" and a.get("class") == "heat" for t, a in tags) == 20
    assert sum(t == "details" for t, _ in tags) == 80
    assert not {"script", "iframe", "img", "link", "form"}.intersection(t for t, _ in tags)
    assert all("src" not in a and "srcset" not in a for _, a in tags)
    ids = [a["id"] for _, a in tags if "id" in a]
    assert len(ids) == len(set(ids))
    assert all(a["href"][1:] in ids for _, a in tags if a.get("href", "").startswith("#"))
    assert "Model-event scores<strong>9600</strong>" in html
    assert "Synthetic only" in html and "No statistical winner" in html
    assert html.count("Path 0, origin 52, horizon 6 months") == 4
    report = study.execute_study(REV, study.prepare_study(REV)["study_sha256"])
    assert report["report_sha256"] in html
    for group in report["groups"]:
        assert group["event_transcript_sha256"] in html
        for row in group["rows"]:
            assert all(f"Exact: {row[k]}" in html for k in study.FIELDS)


def test_transition_matrix_exact_row_mass():
    p = Parser()
    p.feed(obs._transition(((1, 2, 3, 4), (0, 1, 0, 0), (5, 1, 1, 1), (1, 1, 1, 1)), "Test"))
    masses = [Fraction(a["title"].removeprefix("Exact: ")) for t, a in p.tags if t == "td"]
    assert len(masses) == 16
    assert masses[:4] == [Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(2, 5)]
    assert all(sum(masses[i : i + 4]) == 1 for i in range(0, 16, 4))


def test_temporal_observatory_exclusive_output(tmp_path, monkeypatch, html):
    target = tmp_path / "report.html"
    monkeypatch.setattr(obs, "build_observatory", lambda _: html)
    monkeypatch.setattr(sys, "argv", ["obs", "--revision", REV, "--output", str(target)])
    assert obs.main() == 0
    original = target.read_bytes()
    with pytest.raises(SystemExit) as exc:
        obs.main()
    assert exc.value.code == 2
    assert target.read_bytes() == original


def test_temporal_observatory_replay_failure(tmp_path, monkeypatch):
    target = tmp_path / "report.html"
    monkeypatch.setattr(study, "verify_study", lambda *args: "f" * 64)
    monkeypatch.setattr(sys, "argv", ["obs", "--revision", REV, "--output", str(target)])
    with pytest.raises(SystemExit) as exc:
        obs.main()
    assert exc.value.code == 2
    assert not target.exists()
