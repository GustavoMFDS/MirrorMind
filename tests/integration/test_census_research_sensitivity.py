"""One-factor sensitivity grid and exact paired loss regressions."""
from fractions import Fraction

import pytest

from examples import m1_census_research_sensitivity as sensitivity

REV = "12bcc02d0c7f423dcfd053ab2b4e54355169b003"


def test_sensitivity_grid_replays_unique_cells_and_preserves_reference():
    report = sensitivity.run_sensitivity(REV, split="holdout")
    assert report == sensitivity.run_sensitivity(REV, split="holdout")
    assert report["grid_cells"] == 15
    assert report["unique_experiments"] == 13
    assert report["winner"] is report["confidence_interval"] is None
    assert report["inference_status"] == "abstained"
    assert report["holdout_lock_verified"] is False
    cells = report["cells"]
    assert len({c["experiment_sha256"] for c in cells}) == 13
    assert len({c["receipt_sha256"] for c in cells}) == 13
    assert len({c["schedule_sha256"] for c in cells}) == 1
    assert len({c["experiment_sha256"] for c in cells if c["level"] == 0}) == 1
    for cell in cells:
        assert cell["stored_replay_matched"] is True
        for horizon in cell["horizons"]:
            assert horizon["scored_origins"] == 10
            assert horizon["coverage"] == 1
            assert float(Fraction(horizon["paired_mean_difference_exact"])) == pytest.approx(
                horizon["seasonal_mae"] - horizon["trailing_mae"]
            )
    six = {(c["axis"], c["level"]): c["horizons"][2] for c in cells}
    assert six[("trend", 0)]["paired_mean_difference_exact"] == "-9"
    assert six[("trend", 8)]["seasonal_mae"] == 96
    assert six[("volatility", 4)]["paired_mean_difference_exact"] == "184/3"
    assert six[("shift", 120)]["seasonal_mae"] == 120


def test_sensitivity_cell_changes_only_value_and_fictional_snapshot():
    base = sensitivity.build_cell("trend", 0)
    assert base == sensitivity.build_cell("shift", 0)
    assert base == sensitivity.build_cell("volatility", 0)
    shifted = sensitivity.build_cell("shift", 80)
    assert base[:68] == shifted[:68]
    for a, b in zip(base[68:], shifted[68:], strict=True):
        assert b.value - a.value == 80
        assert b.snapshot_sha256 != a.snapshot_sha256
        assert a.reference_month == b.reference_month
        assert a.published_on == b.published_on


@pytest.mark.parametrize("axis,level", [("unknown", 0), ("trend", True), ("shift", 21)])
def test_sensitivity_rejects_unregistered_cells(axis, level):
    with pytest.raises(ValueError, match="unknown sensitivity cell"):
        sensitivity.build_cell(axis, level)


def test_sensitivity_html_and_exclusive_cli(tmp_path, monkeypatch):
    import sys

    report = sensitivity.run_sensitivity(REV)
    assert report["split"] == "validation"
    html = sensitivity.build_html(report)
    assert html.count("<table>") == 3
    assert "No pooled winner" in html
    assert "<script" not in html
    assert report["report_sha256"] in html
    target = tmp_path / "sensitivity.html"
    monkeypatch.setattr(sys, "argv", [
        "sensitivity", "--revision", REV, "--output", str(target),
    ])
    assert sensitivity.main() == 0
    assert target.read_text(encoding="utf-8") == html
    before = target.read_bytes()
    with pytest.raises(SystemExit) as exc:
        sensitivity.main()
    assert exc.value.code == 2
    assert target.read_bytes() == before


def test_sensitivity_prepares_all_cells_before_scoring(monkeypatch):
    events = []
    prepare = sensitivity.prepare_census_experiment
    execute = sensitivity.execute_census_experiment

    def prepare_spy(*args, **kwargs):
        events.append("prepare")
        return prepare(*args, **kwargs)

    def execute_spy(*args, **kwargs):
        events.append("execute")
        return execute(*args, **kwargs)

    monkeypatch.setattr(sensitivity, "prepare_census_experiment", prepare_spy)
    monkeypatch.setattr(sensitivity, "execute_census_experiment", execute_spy)
    sensitivity.run_sensitivity(REV)
    assert events == ["prepare"] * 15 + ["execute"] * 13
