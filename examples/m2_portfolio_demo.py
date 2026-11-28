"""Generate an offline interactive report from the existing fictional workflow."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from examples.m2_bounded_tool_orchestration import ScriptedSyntheticProvider
from mirrormind.domains.retail.synthetic_decision_workflow import (
    DEFAULT_AS_OF,
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)
from mirrormind.modules.agents.contracts import AgentRunRequest
from mirrormind.modules.agents.orchestrator import run_bounded_tool_orchestration

_TEMPLATE = Path(__file__).with_name("portfolio_demo.html")
_PAYLOAD_MARKER = "__MIRRORMIND_RESULT_JSON__"
_AGENT_PAYLOAD_MARKER = "__MIRRORMIND_AGENT_RESULT_JSON__"


def _script_json(payload: object) -> str:
    """Serialize inert script data and prevent it closing its containing element."""
    encoded = json.dumps(payload, ensure_ascii=True, allow_nan=False, sort_keys=True)
    return encoded.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def build_report(
    request: SyntheticDecisionWorkflowRequest,
    *,
    include_agent_preview: bool = False,
) -> str:
    """Embed exact M1 output and optional bounded, local M2-03 report."""
    if type(include_agent_preview) is not bool:
        raise TypeError("include_agent_preview must be a boolean")
    if include_agent_preview and request.replications > 3:
        raise ValueError("agent preview supports at most three replications")

    result = run_synthetic_decision_workflow(request)
    agent_payload: object = None
    if include_agent_preview:
        agent_request = AgentRunRequest(
            question="Inspect this fictional retail decision workflow.",
        )
        agent_report = run_bounded_tool_orchestration(
            agent_request,
            ScriptedSyntheticProvider(
                as_of=request.as_of,
                replications=request.replications,
                seed=request.seed,
            ),
        )
        agent_payload = agent_report.model_dump(mode="json")

    template = _TEMPLATE.read_text(encoding="utf-8")
    if template.count(_PAYLOAD_MARKER) != 1 or template.count(_AGENT_PAYLOAD_MARKER) != 1:
        raise RuntimeError("invalid local report template")
    template = template.replace(_PAYLOAD_MARKER, _script_json(result), 1)
    return template.replace(_AGENT_PAYLOAD_MARKER, _script_json(agent_payload), 1)


def main(argv: list[str] | None = None) -> int:
    """Write one new local HTML file; never overwrite an existing report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat())
    parser.add_argument("--replications", type=int, default=12)
    parser.add_argument("--seed", type=int, default=317)
    parser.add_argument(
        "--agent-preview",
        action="store_true",
        help="also embed the bounded local scripted M2-03 orchestration report",
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        as_of = date.fromisoformat(args.as_of)
        if as_of.isoformat() != args.as_of or args.output.suffix.lower() != ".html":
            raise ValueError("invalid report options")
        request = SyntheticDecisionWorkflowRequest(
            as_of=as_of, replications=args.replications, seed=args.seed,
        )
        if args.agent_preview and request.replications > 3:
            raise ValueError("agent preview supports at most three replications")
        # Fail before expensive computation if the path already exists.
        if args.output.exists() or not args.output.parent.is_dir():
            raise ValueError("output must be a new HTML file in an existing directory")
        report = build_report(request, include_agent_preview=args.agent_preview)
        with args.output.open("x", encoding="utf-8") as destination:
            destination.write(report)
    except (OSError, TypeError, ValueError):
        parser.exit(2, "Invalid report request or unavailable new output path.\n")
    print("Experimental offline report generated. No business action authorized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
