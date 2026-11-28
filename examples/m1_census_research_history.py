"""Offline history of fictional experiment commitments, not execution timestamps."""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path

from examples.m1_census_research_observatory import _STYLE, _mapping, _render_split, _text
from examples.m1_census_research_runner import SCENARIOS, Split, build_fixture, prepare_report
from mirrormind.domains.retail.census_experiment import (
    execute_census_experiment,
    prepare_census_experiment,
)
from mirrormind.domains.retail.census_experiment_journal import read_census_journal_snapshot


def _catalog() -> dict[tuple[object, object], str]:
    result = {}
    for scenario in SCENARIOS:
        identity = prepare_report("0" * 40, scenario)
        result[(identity["schedule_sha256"], identity["input_manifest_sha256"])] = scenario
    return result


def _replay(entry: dict[str, object], scenario: str, split: Split) -> str:
    revision = entry["declared_code_revision"]
    eid = entry["experiment_sha256"]
    if not isinstance(revision, str) or not isinstance(eid, str):
        raise TypeError("invalid identity")
    receipts = _mapping(entry["receipts"])
    if split not in receipts:
        raise ValueError("selected receipt not stored")
    rows, plan = build_fixture(scenario)
    spec = prepare_census_experiment(rows, plan=plan, declared_code_revision=revision)
    result = execute_census_experiment(
        rows, plan=plan, spec=spec, expected_experiment_sha256=eid,
        split=split, declared_code_revision=revision,
    )
    if result["receipt_sha256"] != receipts[split]:
        raise ValueError("stored receipt does not match current local replay")
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=True, allow_nan=False).encode("ascii")
    frozen = _mapping(result["evaluation"])
    evaluation = _mapping(_mapping(frozen["evaluation"])["evaluation"])
    return _render_split({
        "split": split, "horizons": evaluation["horizons"],
        "receipt_sha256": result["receipt_sha256"], "receipt_bytes": len(encoded),
        "stored_replay_matched": True,
    }, prefix="replayed-")


def build_history(
    journal_path: Path, *, replay_experiment: str | None = None, split: Split | None = None
) -> str:
    """Read a snapshot; optionally reproduce exactly one explicitly selected receipt."""
    if (replay_experiment is None) != (split is None):
        raise ValueError("explicit experiment and split required together")
    if split is not None and split not in ("validation", "holdout"):
        raise ValueError("invalid replay split")
    entries = read_census_journal_snapshot(journal_path)
    catalog = _catalog()
    blocks: list[str] = []
    replayed = ""
    for entry in entries:
        eid = entry["experiment_sha256"]
        scenario = catalog.get((entry["schedule_sha256"], entry["input_manifest_sha256"]))
        receipts = _mapping(entry["receipts"])
        provenance = "".join(
            f'<dt>{label}</dt><dd><code>{_text(entry[key])}</code></dd>'
            for key, label in (
                ("experiment_sha256", "Experiment"), ("declared_code_revision", "Declared revision"),
                ("schedule_sha256", "Schedule"), ("input_manifest_sha256", "Input manifest"),
            )
        )
        receipt_html = "".join(
            f'<dt>{s.title()} (stored, not replayed on read)</dt><dd><code>'
            f'{_text(receipts[s])}</code></dd>' if s in receipts
            else f'<dt>{s.title()}</dt><dd>Not recorded</dd>'
            for s in ("validation", "holdout")
        )
        blocks.append(
            f'<article class="panel"><h2>{_text(scenario or "Unknown fixture")}</h2>'
            '<details><summary>Identity and stored receipt metadata</summary><dl>'
            + provenance + receipt_html + '</dl></details></article>'
        )
        if eid == replay_experiment:
            if scenario is None or split is None:
                raise ValueError("fixture not reproducible by current catalog")
            replayed = (
                '<section class="panel"><h2>Explicit local replay matched</h2>'
                f'<p>Experiment: <code>{_text(eid)}</code></p>'
                '<p>Current implementation, declared revision only; no historical code attestation.</p>'
                + _replay(entry, scenario, split) + '</section>'
            )
    if replay_experiment is not None and not replayed:
        raise ValueError("experiment not found")
    snapshot = json.dumps(entries, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=True, allow_nan=False).encode("ascii")
    count = sum(len(_mapping(entry["receipts"])) for entry in entries)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; '
        'style-src &apos;unsafe-inline&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
        '<title>MirrorMind | Experiment History</title><style>' + _STYLE + '</style></head>'
        '<body><a class="skip" href="#main">Skip to report</a><main id="main">'
        '<header><p class="eyebrow">MIRRORMIND / EXPERIMENTAL RESEARCH</p>'
        '<h1>Experiment History</h1></header><aside class="notice">'
        '<strong>Fictional research only / Inference abstained</strong>'
        '<p>Stored metadata is not verified on read. No timestamps, execution counts, '
        'independent registration, holdout lock, runtime attestation or action authority.</p></aside>'
        '<section class="panel"><h2>Snapshot overview</h2><div class="grid">'
        f'<div class="stat">Unique commitments<strong>{len(entries)}</strong></div>'
        f'<div class="stat">Stored split digests<strong>{count}</strong></div></div>'
        '<p>Ordered by commitment digest, not chronology. Repeated identical runs are idempotent.</p>'
        f'<p>Snapshot SHA-256: <code>{hashlib.sha256(snapshot).hexdigest()}</code></p></section>'
        + replayed + ("".join(blocks) or '<p>No registered experiments.</p>')
        + '</main></body></html>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect existing fictional research journal")
    parser.add_argument("--journal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-experiment")
    parser.add_argument("--split", choices=("validation", "holdout"))
    args = parser.parse_args()
    try:
        if not args.output.is_absolute() or args.output.suffix.lower() != ".html":
            raise ValueError("absolute HTML output required")
        html = build_history(args.journal, replay_experiment=args.replay_experiment, split=args.split)
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(html)
    except (ValueError, TypeError, OSError, sqlite3.Error):
        parser.exit(2, "Fictional history generation failed; existing output is not overwritten.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
