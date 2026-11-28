"""Offline portfolio report contract tests; no browser or network required."""

import json
import re

import pytest

from examples.m2_portfolio_demo import build_report, main
from mirrormind.domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)


def embedded_result(html):
    match = re.search(
        r'<script id="workflow-result" type="application/json">(.*?)</script>',
        html, re.DOTALL,
    )
    assert match
    return json.loads(match.group(1))


def test_offline_report_preserves_exact_workflow_result():
    request = SyntheticDecisionWorkflowRequest(replications=2, seed=317)
    expected = run_synthetic_decision_workflow(request)
    html = build_report(request)
    assert embedded_result(html) == json.loads(json.dumps(expected, allow_nan=False))
    assert expected["action_authorized"] is False
    assert expected["writes_performed"] is False
    assert "connect-src 'none'" in html
    assert "textContent" in html
    assert "innerHTML" not in html
    assert "__MIRRORMIND_RESULT_JSON__" not in html
    assert 'id="lead-time"' in html
    assert 'aria-label="Report sections"' in html
    for name in ("Scrollable policy comparison", "Scrollable evidence table"):
        assert f'tabindex="0" role="region" aria-label="{name}"' in html
    assert html.count("<caption>") == 2
    assert html.count('scope="col"') == 10
    assert 'td.scope = "row"' in html
    assert 'm.fill_rate_basis_points === null ? "Not available"' in html


def test_report_escapes_script_terminators(monkeypatch):
    import examples.m2_portfolio_demo as demo

    payload = {"text": "</script><script>alert(1)</script>&"}
    monkeypatch.setattr(demo, "run_synthetic_decision_workflow", lambda _: payload)
    html = build_report(SyntheticDecisionWorkflowRequest())
    assert embedded_result(html) == payload
    assert payload["text"] not in html


def test_report_cli_writes_only_new_explicit_html(tmp_path):
    output = tmp_path / "demo.html"
    args = ["--output", str(output), "--replications", "1", "--seed", "17"]
    assert main(args) == 0
    original = output.read_bytes()
    result = embedded_result(output.read_text(encoding="utf-8"))
    assert result["decision_status"] == "comparison_only_no_policy_selection_or_authorization"
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert exc.value.code == 2
    assert output.read_bytes() == original
    assert list(tmp_path.iterdir()) == [output]


@pytest.mark.parametrize("options", [
    ["--replications", "0"], ["--replications", "999999"],
    ["--as-of", "2026-11-27"], ["--seed", "-1"],
])
def test_invalid_report_request_creates_no_output(tmp_path, options):
    output = tmp_path / "demo.html"
    with pytest.raises(SystemExit) as exc:
        main(["--output", str(output), *options])
    assert exc.value.code == 2
    assert not output.exists()
