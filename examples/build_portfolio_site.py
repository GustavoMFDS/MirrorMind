"""Build only the public portfolio landing page and fictional report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from shutil import copyfile

from examples.m2_portfolio_demo import build_report
from mirrormind.domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
)

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
OUTPUT_FILES = frozenset({
    "index.html", "demo.html", "mirrormind-architecture.svg",
    "mirrormind-synthetic-comparison.svg", ".nojekyll", "build.json",
})


def build_site(output: Path, source_sha: str) -> None:
    """Create a new directory with a fixed, reviewed public file inventory."""
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise ValueError("source SHA must contain 40 lowercase hex digits")
    if output.exists() or not output.parent.is_dir():
        raise ValueError("output must be a new directory with an existing parent")
    home = (ASSETS / "portfolio_site.html").read_text(encoding="utf-8")
    if "__SHA__" not in home:
        raise ValueError("missing source revision marker")
    home = home.replace("__SHA__", source_sha)
    report = build_report(SyntheticDecisionWorkflowRequest(replications=2, seed=317))
    match = re.search(
        r'<script id="workflow-result" type="application/json">(.*?)</script>',
        report, re.DOTALL,
    )
    if match is None:
        raise ValueError("missing report payload")
    result = json.loads(match.group(1))
    if (
        any(result[k] is not False for k in (
            "action_authorized", "writes_performed", "ingestion_authorized",
            "source_forecast_eligible",
        ))
        or result["worldkernel_execution"] != "worldkernel_not_invoked"
        or {e["source_ref"] for e in result["trace"]["evidence"]}
        != {"synthetic_fixture_generator"}
    ):
        raise ValueError("report outside public synthetic scope")
    output.mkdir()
    (output / "index.html").write_text(home, encoding="utf-8")
    (output / "demo.html").write_text(report, encoding="utf-8")
    for name in ("mirrormind-architecture.svg", "mirrormind-synthetic-comparison.svg"):
        copyfile(ASSETS / name, output / name)
    (output / ".nojekyll").touch()
    (output / "build.json").write_text(json.dumps({
        "source_sha": source_sha,
        "trace_sha256": result["trace_sha256"],
        "synthetic_only": True,
        "files": sorted(OUTPUT_FILES),
    }, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    """Build a site from the checked-out source; caller supplies its exact SHA."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    build_site(args.output, args.source_sha)


if __name__ == "__main__":
    main()
