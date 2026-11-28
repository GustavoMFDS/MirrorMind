"""Offline portfolio report contract tests; no browser or network required."""

import json
import re
from datetime import date
from hashlib import sha256
from types import SimpleNamespace

import pytest

from examples.m2_portfolio_demo import build_report, main
from mirrormind.domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)


def embedded_script_payload(html, element_id):
    match = re.search(
        rf'<script id="{re.escape(element_id)}" type="application/json">(.*?)</script>',
        html, re.DOTALL,
    )
    assert match
    return match.group(1)


def embedded_result(html):
    return json.loads(embedded_script_payload(html, "workflow-result"))


def embedded_agent_result(html):
    return json.loads(embedded_script_payload(html, "agent-result"))


def test_offline_report_preserves_exact_workflow_result():
    request = SyntheticDecisionWorkflowRequest(replications=2, seed=317)
    expected = run_synthetic_decision_workflow(request)
    html = build_report(request)
    assert embedded_result(html) == json.loads(json.dumps(expected, allow_nan=False))
    expected_payload = json.dumps(
        expected, ensure_ascii=True, allow_nan=False, sort_keys=True,
    ).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    assert embedded_script_payload(html, "workflow-result") == expected_payload
    assert embedded_agent_result(html) is None
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


def test_agent_preview_composes_matching_bounded_workflow_and_digest():
    request = SyntheticDecisionWorkflowRequest(
        as_of=date(2011, 1, 26), replications=2, seed=317,
    )
    expected = run_synthetic_decision_workflow(request)

    html = build_report(request, include_agent_preview=True)
    result = embedded_result(html)
    agent = embedded_agent_result(html)

    assert result == json.loads(json.dumps(expected, allow_nan=False))
    assert result["as_of"] == request.as_of.isoformat()
    assert agent["status"] == "completed"
    assert agent["provider_mode"] == "test_double"
    assert agent["tool_call_count"] == 2
    assert [item["tool_name"] for item in agent["tool_receipts"]] == [
        "search_synthetic_evidence", "run_synthetic_retail_decision",
    ]
    expected_tool_input = json.dumps(
        {
            "as_of": request.as_of.isoformat(),
            "replications": request.replications,
            "seed": request.seed,
        },
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    assert agent["tool_receipts"][1]["input_sha256"] == sha256(expected_tool_input).hexdigest()
    assert agent["draft"]["status"] == "draft_for_human_review"
    assert agent["draft_trust_label"] == "untrusted_provider_draft"
    assert expected["workflow_result_sha256"] in agent["draft"]["summary"]
    assert agent["human_review_required"] is True
    assert agent["action_authorized"] is False
    assert agent["writes_performed"] is False


def test_abstention_payload_and_renderer_guard_handle_missing_success_fields():
    request = SyntheticDecisionWorkflowRequest(
        as_of=date(2011, 2, 4), replications=2, seed=317,
    )
    html = build_report(request, include_agent_preview=True)

    result = embedded_result(html)
    agent = embedded_agent_result(html)

    assert result["status"] == "abstained_required_history_unavailable"
    assert result["trace"] is None
    assert result["simulation"].get("result") is None
    assert result["abstention"]["reason"] == "seven_consecutive_published_days_are_required"
    assert agent["status"] == "refused"
    assert agent["refusal_code"] == "tool_failed"
    assert agent["draft"] is None
    assert "history-abstention" in html
    assert "agent-refusal" in html
    assert "if (!r.trace || !r.simulation?.result)" in html
    assert "innerHTML" not in html
    renderer = html.split("<script>\n", 1)[1].split("</script>", 1)[0]
    assert renderer.index("if (!r.trace || !r.simulation?.result)") < renderer.index("const sim = r.simulation.result")
    assert renderer.index("el(\"history-abstention\").hidden = false") < renderer.index("const sim = r.simulation.result")


def test_agent_preview_escapes_both_embedded_payloads(monkeypatch):
    import examples.m2_portfolio_demo as demo

    workflow_payload = {"text": "</script><script>bad()</script>&"}
    agent_payload = {"summary": "</script><script>bad()</script>&"}
    monkeypatch.setattr(demo, "run_synthetic_decision_workflow", lambda _: workflow_payload)
    monkeypatch.setattr(
        demo,
        "run_bounded_tool_orchestration",
        lambda *_: SimpleNamespace(model_dump=lambda **_: agent_payload),
    )
    request = SyntheticDecisionWorkflowRequest(
        as_of=date(2011, 1, 26), replications=1, seed=17,
    )

    html = build_report(request, include_agent_preview=True)

    assert embedded_result(html) == workflow_payload
    assert embedded_agent_result(html) == agent_payload
    assert workflow_payload["text"] not in html
    assert agent_payload["summary"] not in html


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


def test_agent_preview_cli_embeds_local_orchestration_result(tmp_path):
    output = tmp_path / "agent.html"
    assert main([
        "--output", str(output), "--as-of", "2011-01-26",
        "--replications", "2", "--seed", "317", "--agent-preview",
    ]) == 0
    assert embedded_agent_result(output.read_text(encoding="utf-8"))["status"] == "completed"


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


def test_agent_preview_rejects_more_than_three_replications_before_output(tmp_path):
    output = tmp_path / "agent.html"
    with pytest.raises(SystemExit) as exc:
        main([
            "--output", str(output), "--agent-preview", "--replications", "4",
        ])
    assert exc.value.code == 2
    assert not output.exists()
