"""Generate an offline interactive report from the existing fictional workflow."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from mirrormind.domains.retail.synthetic_decision_workflow import (
    DEFAULT_AS_OF,
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)

_TEMPLATE = Path(__file__).with_name("portfolio_demo.html")
_PAYLOAD_MARKER = "__MIRRORMIND_RESULT_JSON__"


def build_report(request: SyntheticDecisionWorkflowRequest) -> str:
    """Render the exact workflow result without changing its metrics or authority."""
    result = run_synthetic_decision_workflow(request)
    payload = json.dumps(result, ensure_ascii=True, allow_nan=False, sort_keys=True)
    # Prevent a JSON string from terminating the inert script element.
    payload = payload.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = _TEMPLATE.read_text(encoding="utf-8")
    if template.count(_PAYLOAD_MARKER) != 1:
        raise RuntimeError("invalid local report template")
    return template.replace(_PAYLOAD_MARKER, payload, 1)


def main(argv: list[str] | None = None) -> int:
    """Write one new local HTML file; never overwrite an existing report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", default=DEFAULT_AS_OF.isoformat())
    parser.add_argument("--replications", type=int, default=12)
    parser.add_argument("--seed", type=int, default=317)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        as_of = date.fromisoformat(args.as_of)
        if as_of.isoformat() != args.as_of or args.output.suffix.lower() != ".html":
            raise ValueError("invalid report options")
        request = SyntheticDecisionWorkflowRequest(
            as_of=as_of, replications=args.replications, seed=args.seed,
        )
        # Fail before expensive computation if the path already exists.
        if args.output.exists() or not args.output.parent.is_dir():
            raise ValueError("output must be a new HTML file in an existing directory")
        report = build_report(request)
        with args.output.open("x", encoding="utf-8") as destination:
            destination.write(report)
    except (OSError, TypeError, ValueError):
        parser.exit(2, "Invalid report request or unavailable new output path.\n")
    print("Experimental offline report generated. No business action authorized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
