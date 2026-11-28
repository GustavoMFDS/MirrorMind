"""Offline, fully replayed fictional temporal research report."""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path

from examples import m1_census_temporal_study as study
from examples.m1_census_bivariate_observatory import _FIELDS, _STYLE_EXTRA, _heatmap, _marginals
from examples.m1_census_probability_observatory import _metric
from examples.m1_census_research_observatory import _STYLE, _mapping, _text
from mirrormind.domains.retail.census_bivariate import (
    joint_covariance,
    joint_positive_probability,
)
from mirrormind.domains.retail.census_joint_markov import STATES, TransitionMatrix
from mirrormind.domains.retail.census_temporal_models import (
    fit_temporal_models,
    predict_temporal_models,
)

_LABELS = {
    "iid": "IID empirical",
    "own": "Own-state",
    "cross": "Cross-axis",
    "full": "Full previous pair",
    "oracle": "Oracle (privileged reference)",
}


def _transition(matrix: TransitionMatrix, label: str) -> str:
    header = "".join(f'<th scope="col">({x:+d}, {y:+d})</th>' for x, y in STATES)
    rows = []
    for (x, y), row in zip(STATES, matrix, strict=True):
        cells = "".join(
            f'<td title="Exact: {Fraction(w, sum(row))}" '
            f'style="background:rgba(105,218,196,{0.4 * w / sum(row):.6f})">'
            f"{float(Fraction(w, sum(row))):.2%}<code> {Fraction(w, sum(row))}</code></td>"
            for w in row
        )
        rows.append(f'<tr><th scope="row">({x:+d}, {y:+d})</th>{cells}</tr>')
    return (
        '<div class="scroll" tabindex="0" role="region" aria-label="Transition matrix">'
        f'<table class="transition"><caption>{_text(label)}; previous state rows, next state columns</caption>'
        f'<thead><tr><th scope="col">Previous / next</th>{header}</tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def _example(scenario: str, seed: int) -> str:
    t, h = 52, 6
    path = study._path(scenario, seed, 0)
    history = path[t - 23 : t + 1]
    matrices = fit_temporal_models(history)
    ps = predict_temporal_models(history, h)
    ps["oracle"] = study._reference(scenario, t, h, path[t])
    actual = (
        sum(x for x, _ in path[t + 1 : t + h + 1]),
        sum(y for _, y in path[t + 1 : t + h + 1]),
    )
    blocks = []
    for model in study.MODELS:
        p = ps[model]
        transition = (
            _transition(matrices[model], "Estimated stationary transition law")
            if model != "oracle"
            else ""
        )
        if model == "oracle":
            transition = "".join(
                _transition(study._matrix(scenario, i), f"Privileged transition at index {i}")
                for i in range(t + 1, t + h + 1)
            )
        blocks.append(
            f"<details><summary>{_LABELS[model]}</summary>"
            + transition
            + f"<p>Covariance: {_metric(str(joint_covariance(p)))}. "
            f"Both positive: {_metric(str(joint_positive_probability(p)), percent=True)}.</p>"
            + _heatmap(p, _LABELS[model])
            + _marginals(p)
            + "</details>"
        )
    return (
        '<section class="example"><h3>Fixed conditional forecast example</h3>'
        f"<p>Path 0, origin {t}, horizon {h} months; realized pair "
        f"<strong>({actual[0]:+d}, {actual[1]:+d})</strong>. "
        "The example is fixed in advance, not a separate experiment.</p>"
        + "".join(blocks)
        + "</section>"
    )


def _group(group: dict[str, object]) -> str:
    scenario, seed, rows = group["scenario"], group["seed"], group["rows"]
    if not isinstance(scenario, str) or type(seed) is not int or not isinstance(rows, list):
        raise TypeError("invalid group")
    blocks = []
    for raw in rows:
        row = _mapping(raw)
        model = row["model"]
        if not isinstance(model, str):
            raise TypeError("invalid model")
        cells = "".join(
            f'<td class="num">{_metric(row[k], percent=k in ("predicted_event", "observed_event"))}</td>'
            for k in study.FIELDS
        )
        exact = " / ".join(_text(row[k]) for k in study.FIELDS)
        blocks.append(
            f'<tr><th scope="row">{_text(row["horizon"])}</th><td>{_LABELS[model]}</td>'
            f"{cells}<td>{_text(row['pairs'])}</td></tr>"
            f'<tr><td colspan="11"><details><summary>Exact rational metrics</summary>'
            f"<code>{exact}</code></details></td></tr>"
        )
    headers = "".join(f'<th scope="col">{v}</th>' for v in _FIELDS)
    return (
        f'<article class="panel" id="{_text(scenario)}"><h2>{_text(scenario.title())}</h2>'
        f"<p>Seed {seed}; {_text(group['paths'])} paths.</p>"
        '<div class="scroll" tabindex="0" role="region" aria-label="Group metrics">'
        "<table><caption>Separate descriptive means by horizon; exact values in column order</caption>"
        '<thead><tr><th scope="col">Months</th><th scope="col">Method</th>'
        f'{headers}<th scope="col">Pairs</th></tr></thead><tbody>{"".join(blocks)}</tbody></table></div>'
        + _example(scenario, seed)
        + "<p>Event transcript SHA-256: <code>"
        + _text(group["event_transcript_sha256"])
        + "</code></p></article>"
    )


def build_observatory(revision: str) -> str:
    expected = study.prepare_study(revision)["study_sha256"]
    if not isinstance(expected, str):
        raise TypeError("invalid commitment")
    report = study.execute_study(revision, expected)
    if study.verify_study(revision, expected, study.canonical(report)) != report["report_sha256"]:
        raise ValueError("temporal replay mismatch")
    groups = report["groups"]
    if not isinstance(groups, list):
        raise TypeError("invalid groups")
    sections = "".join(_group(_mapping(g)) for g in groups)
    paths = len(study.SCENARIOS) * study.PATHS
    scores = paths * len(study.ORIGINS) * len(study.HORIZONS) * len(study.MODELS)
    links = " | ".join(f'<a href="#{s}">{s.title()}</a>' for s, _ in study.SCENARIOS)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; '
        'style-src &apos;unsafe-inline&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
        "<title>MirrorMind | Dynamic Network Observatory</title><style>"
        + _STYLE
        + _STYLE_EXTRA
        + ".transition{min-width:500px}.transition code{display:block}.transition td{text-align:center}"
        + '</style></head><body><a class="skip" href="#main">Skip to report</a><main id="main">'
        '<header><p class="eyebrow">MIRRORMIND / EXPERIMENTAL RESEARCH</p>'
        '<h1>Dynamic Network Observatory</h1></header><aside class="notice">'
        "<strong>Synthetic only / Inference abstained</strong>"
        "<p>Paired sign-state Markov dynamics; predictive dependence, not identified causal effects. "
        "No statistical winner, calibration, holdout, independent registration or runtime attestation.</p>"
        '</aside><section class="panel"><h2>Study overview</h2><div class="grid">'
        f'<div class="stat">Paths<strong>{paths}</strong></div>'
        f'<div class="stat">Model-event scores<strong>{scores}</strong></div>'
        '<div class="stat">Local replay<strong>Matched</strong></div></div>'
        "<p>Fixed IID, own-state, cross-axis and full conditional laws; no automatic model selection. Joint Brier ranges from 0 to 2; "
        "reference excess is relative to the supplied generating law. Event means both displacements "
        "strictly positive. The oracle knows the future transition schedule, not outcomes. No pooling across horizons.</p>"
        f'<nav aria-label="Scenario navigation">{links}</nav></section>'
        + sections
        + '<section class="panel"><h2>Provenance</h2><dl>'
        f"<dt>Study</dt><dd><code>{_text(expected)}</code></dd>"
        f"<dt>Report</dt><dd><code>{_text(report['report_sha256'])}</code></dd>"
        f"<dt>Declared revision</dt><dd><code>{_text(revision)}</code></dd>"
        "<dt>Commitment</dt><dd>Self-generated demo, not independent registration.</dd>"
        "</dl></section></main></body></html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline fictional dynamic network observatory")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if not args.output.is_absolute() or args.output.suffix.lower() != ".html":
            raise ValueError("absolute HTML output required")
        html = build_observatory(args.revision)
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(html)
    except (ValueError, TypeError, OSError):
        parser.exit(2, "Fictional temporal observatory failed; existing output not overwritten.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
