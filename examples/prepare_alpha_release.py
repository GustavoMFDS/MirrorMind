"""Prepare a reviewable synthetic release bundle without creating tags or releases."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import tomllib
from pathlib import Path

from examples.build_portfolio_site import build_site
from mirrormind import __version__
from mirrormind.api import app

ROOT = Path(__file__).resolve().parents[1]


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, timeout=30
    ).strip()


def prepare(output: Path, expected_sha: str) -> None:
    """Generate only a synthetic report, checksums and a draft manifest."""
    if not re.fullmatch(r"[0-9a-f]{40}", expected_sha):
        raise ValueError("invalid expected SHA")
    if git("rev-parse", "HEAD") != expected_sha:
        raise ValueError("checkout does not match expected SHA")
    if git("status", "--porcelain", "--untracked-files=no"):
        raise ValueError("tracked checkout is dirty")
    if output.exists() or not output.parent.is_dir():
        raise ValueError("output must be a new directory with existing parent")
    meta = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    version = meta["project"]["version"]
    match = re.fullmatch(r"(\d+\.\d+\.\d+)a([1-9]\d*)", version)
    if match is None or version != __version__ or version != app.version:
        raise ValueError("expected consistent alpha package and API version")
    tag = f"v{match[1]}-alpha.{match[2]}"
    with tempfile.TemporaryDirectory() as temp:
        site = Path(temp) / "site"
        build_site(site, expected_sha)
        demo = (site / "demo.html").read_bytes()
        receipt = json.loads((site / "build.json").read_text(encoding="utf-8"))
    if git("rev-parse", "HEAD") != expected_sha or git(
        "status", "--porcelain", "--untracked-files=no"
    ):
        raise ValueError("checkout changed during preparation")
    report_sha = hashlib.sha256(demo).hexdigest()
    output.mkdir()
    (output / "mirror-demo.html").write_bytes(demo)
    (output / "SHA256SUMS.txt").write_text(
        f"{report_sha}  mirror-demo.html\n", encoding="ascii"
    )
    (output / "release-candidate.json").write_text(json.dumps({
        "source_sha": expected_sha,
        "version": version,
        "suggested_tag": tag,
        "report_sha256": report_sha,
        "trace_sha256": receipt["trace_sha256"],
        "synthetic_only": True,
        "publication_authorized": False,
        "official_ci_verified": False,
        "status": "preparation_only",
    }, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-sha", required=True)
    args = parser.parse_args()
    prepare(args.output, args.expected_sha)


if __name__ == "__main__":
    main()
