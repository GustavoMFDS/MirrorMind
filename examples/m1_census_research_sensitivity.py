"""Bounded one-factor fictional sensitivity analysis; no statistical inference."""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from dataclasses import replace
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory

from examples.m1_census_research_observatory import _STYLE, _mapping, _number, _text
from examples.m1_census_research_runner import Split, build_fixture
from mirrormind.domains.retail.census_experiment import (
    CensusExperimentSpec,
    census_experiment_sha256,
    execute_census_experiment,
    prepare_census_experiment,
)
from mirrormind.domains.retail.census_experiment_journal import CensusExperimentJournal
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

GRID = (
    ("trend", (0, 1, 2, 4, 8)),
    ("volatility", (0, 1, 2, 3, 4)),
    ("shift", (0, 20, 40, 80, 120)),
)
SCHEMA = "mirrormind.census.fictional_sensitivity.v1"


def _canonical(payload: dict[str, object]) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def _value(i: int, axis: str, level: int) -> int:
    base = 200 + 3 * (i % 12)
    if axis == "trend":
        return base + level * i
    if axis == "volatility":
        return base + level * (((37 * i * i + 17 * i + 11) % 101) - 50)
    if axis == "shift":
        return base + (level if i >= 68 else 0)
    raise ValueError("unknown sensitivity axis")


def build_cell(axis: str, level: int) -> tuple[CensusVintageRecord, ...]:
    """One fixed factor varies; zero levels intentionally share the same input."""
    allowed = dict(GRID)
    if type(axis) is not str or axis not in allowed or type(level) is not int or level not in allowed[axis]:
        raise ValueError("unknown sensitivity cell")
    rows, _ = build_fixture()
    result = []
    for i, record in enumerate(rows):
        value = _value(i, axis, level)
        marker = hashlib.sha256(f"fictional-sensitivity-v1:{i}:{value}".encode("ascii")).hexdigest()
        result.append(replace(record, value=Decimal(value), snapshot_sha256=marker))
    return tuple(result)


def _summarize(result: dict[str, object]) -> list[dict[str, object]]:
    frozen = _mapping(result["evaluation"])
    descriptive = _mapping(frozen["evaluation"])
    evaluation = _mapping(descriptive["evaluation"])
    horizons = evaluation["horizons"]
    losses = descriptive["paired_losses"]
    if not isinstance(horizons, (tuple, list)) or not isinstance(losses, (tuple, list)):
        raise TypeError("invalid evaluation sequences")
    summaries: list[dict[str, object]] = []
    for item in horizons:
        h = _mapping(item)
        paired = [
            Fraction(str(_mapping(row)["paired_loss_difference"]))
            for row in losses if _mapping(row)["horizon_months"] == h["horizon_months"]
        ]
        if len(paired) != h["scored_origins"]:
            raise ValueError("paired count mismatch")
        metrics = h["metrics"]
        seasonal = trailing = None
        if metrics is not None:
            seasonal = _mapping(_mapping(metrics)["seasonal_naive_lag12"])["mae"]
            trailing = _mapping(_mapping(metrics)["trailing_12_month_mean"])["mae"]
        summaries.append({
            "horizon_months": h["horizon_months"],
            "requested_origins": h["requested_origins"],
            "scored_origins": h["scored_origins"],
            "coverage": h["coverage"],
            "seasonal_mae": seasonal,
            "trailing_mae": trailing,
            "paired_mean_difference_exact": str(sum(paired, Fraction(0)) / len(paired)) if paired else None,
        })
    return summaries


def run_sensitivity(revision: str, *, split: Split = "validation") -> dict[str, object]:
    """Prepare the entire grid before evaluation; replay each distinct cell once."""
    if split not in ("validation", "holdout"):
        raise ValueError("invalid split")
    _, plan = build_fixture()
    prepared: list[tuple[str, int, str]] = []
    unique: dict[str, tuple[tuple[CensusVintageRecord, ...], CensusExperimentSpec]] = {}
    for axis, levels in GRID:
        for level in levels:
            rows = build_cell(axis, level)
            spec = prepare_census_experiment(rows, plan=plan, declared_code_revision=revision)
            eid = census_experiment_sha256(spec)
            unique[eid] = (rows, spec)
            prepared.append((axis, level, eid))
    completed: dict[str, dict[str, object]] = {}
    with TemporaryDirectory(prefix="mm-sensitivity-") as tmp:
        path = Path(tmp) / "journal.sqlite"
        journal = CensusExperimentJournal(path)
        for eid, (rows, spec) in unique.items():
            journal.register(
                rows, plan=plan, spec=spec, expected_experiment_sha256=eid,
                declared_code_revision=revision,
            )
            result = execute_census_experiment(
                rows, plan=plan, spec=spec, expected_experiment_sha256=eid,
                split=split, declared_code_revision=revision,
            )
            submitted = _canonical(result)
            digest = journal.admit(
                eid, rows, plan=plan, split=split, declared_code_revision=revision, submitted=submitted
            )
            if CensusExperimentJournal(path).verify_stored(
                eid, rows, plan=plan, split=split, declared_code_revision=revision, submitted=submitted
            ) != digest:
                raise ValueError("stored replay mismatch")
            completed[eid] = {
                "experiment_sha256": eid, "input_manifest_sha256": spec.input_manifest_sha256,
                "schedule_sha256": spec.schedule_sha256, "receipt_sha256": digest,
                "stored_replay_matched": True, "horizons": _summarize(result),
            }
    report: dict[str, object] = {
        "schema_version": SCHEMA, "declared_code_revision": revision, "split": split,
        "design": "one_factor_at_a_time_shared_zero_baseline",
        "grid_cells": len(prepared), "unique_experiments": len(unique),
        "cells": [
            dict(completed[eid], axis=axis, level=level) for axis, level, eid in prepared
        ],
        "synthetic_only": True, "registration_verified": False, "runtime_code_attested": False,
        "holdout_lock_verified": False, "forecast_eligible": False, "ingestion_authorized": False,
        "action_authorized": False, "inference_status": "abstained",
        "winner": None, "confidence_interval": None,
    }
    report["report_sha256"] = hashlib.sha256(_canonical(report)).hexdigest()
    return report


def build_html(report: dict[str, object]) -> str:
    cells = report["cells"]
    if not isinstance(cells, list):
        raise TypeError("invalid cells")
    sections: list[str] = []
    for axis, _ in GRID:
        rows: list[str] = []
        provenance: list[str] = []
        for raw in cells:
            cell = _mapping(raw)
            if cell["axis"] != axis:
                continue
            horizons = cell["horizons"]
            if not isinstance(horizons, list):
                raise TypeError("invalid horizons")
            for h in horizons:
                row = _mapping(h)
                rows.append(
                    f'<tr><th scope="row">{_text(cell["level"])}</th>'
                    f'<td>{_text(row["horizon_months"])}</td>'
                    f'<td>{_number(row["seasonal_mae"])}</td><td>{_number(row["trailing_mae"])}</td>'
                    f'<td>{_text(row["paired_mean_difference_exact"])}</td>'
                    f'<td>{_text(row["scored_origins"])}/{_text(row["requested_origins"])}</td>'
                    f'<td>{_number(row["coverage"], percent=True)}</td></tr>'
                )
            provenance.append(
                f'<dt>Level {_text(cell["level"])}</dt><dd>Experiment: <code>'
                f'{_text(cell["experiment_sha256"])}</code><br>Manifest: <code>'
                f'{_text(cell["input_manifest_sha256"])}</code><br>Schedule: <code>'
                f'{_text(cell["schedule_sha256"])}</code><br>Receipt: <code>'
                f'{_text(cell["receipt_sha256"])}</code></dd>'
            )
        sections.append(
            f'<section class="panel"><h2>{axis.title()}</h2>'
            '<div class="scroll" tabindex="0" role="region" aria-label="Sensitivity table">'
            '<table><caption>One-factor descriptive comparison</caption><thead><tr>'
            '<th scope="col">Level</th><th scope="col">Months</th><th scope="col">Seasonal MAE</th>'
            '<th scope="col">Trailing MAE</th><th scope="col">Exact mean difference</th>'
            '<th scope="col">Scored</th><th scope="col">Coverage</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div><details><summary>Cell provenance</summary><dl>'
            + "".join(provenance) + '</dl></details></section>'
        )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; '
        'style-src &apos;unsafe-inline&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
        '<title>MirrorMind | Sensitivity Analysis</title><style>' + _STYLE + '</style></head>'
        '<body><a class="skip" href="#main">Skip to report</a><main id="main">'
        '<header><p class="eyebrow">MIRRORMIND / EXPERIMENTAL RESEARCH</p>'
        '<h1>Sensitivity Analysis</h1></header><aside class="notice">'
        '<strong>Fictional only / Inference abstained</strong>'
        '<p>One-factor designed sequences, not independent samples. No pooled winner, intervals, '
        'independent registration, holdout lock, code attestation or action authority.</p></aside>'
        '<section class="panel"><h2>Design</h2>'
        f'<p>Split: {_text(report["split"])}. Grid cells: {_text(report["grid_cells"])}. '
        f'Unique replayed experiments: {_text(report["unique_experiments"])}.</p>'
        '<p>Zero levels share a baseline. Difference is seasonal minus trailing absolute loss.</p>'
        f'<p>Declared revision: <code>{_text(report["declared_code_revision"])}</code></p>'
        f'<p>Report SHA-256: <code>{_text(report["report_sha256"])}</code></p></section>'
        + "".join(sections) + '</main></body></html>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fixed fictional sensitivity grid")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--split", choices=("validation", "holdout"), default="validation")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.output is not None and (
            not args.output.is_absolute() or args.output.suffix.lower() != ".html"
        ):
            raise ValueError("absolute HTML output required")
        report = run_sensitivity(args.revision, split=args.split)
        if args.output is not None:
            html = build_html(report)
            with args.output.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(html)
        else:
            print(_canonical(report).decode("ascii"))
    except (ValueError, TypeError, OSError, sqlite3.Error):
        parser.exit(2, "Fictional sensitivity analysis failed; existing output is not overwritten.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
