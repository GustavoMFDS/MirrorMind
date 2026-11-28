"""Offline, fully replayed fictional bivariate research report."""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path

from examples import m1_census_bivariate_study as study
from examples.m1_census_probability_observatory import _metric
from examples.m1_census_research_observatory import _STYLE, _mapping, _text
from mirrormind.domains.retail.census_bivariate import (
    JointPMF,
    joint_covariance,
    joint_marginal,
    joint_positive_probability,
)

_LABELS = {
    "fixed_independent": "Fixed independent",
    "product24": "Matched independent 24",
    "joint24": "Joint empirical 24",
    "oracle": "Oracle (privileged reference)",
}
_FIELDS = (
    "Joint Brier",
    "Reference excess",
    "Marginal CRPS X",
    "Marginal CRPS Y",
    "Event Brier",
    "Predicted event",
    "Observed event",
    "Covariance",
)
_STYLE_EXTRA = """
.heat{width:auto;margin:auto;min-width:420px}.heat td,.heat th{text-align:center}
.heat td{min-width:55px;font-size:.85rem;color:var(--text)}
.marginal{min-width:260px}.example{border-top:1px solid var(--line);margin-top:18px;padding-top:12px}
"""


def _heatmap(pmf: JointPMF, label: str) -> str:
    total = sum(w for _, _, w in pmf)
    masses = {(x, y): Fraction(w, total) for x, y, w in pmf}
    xs = sorted({x for x, _, _ in pmf})
    ys = sorted({y for _, y, _ in pmf}, reverse=True)
    header = "".join(f'<th scope="col">{x:+d}</th>' for x in xs)
    rows = []
    for y in ys:
        cells = []
        for x in xs:
            p = masses.get((x, y), Fraction())
            intensity = float(p) * 0.85
            cells.append(
                f'<td style="background:rgba(105,218,196,{intensity:.6f})" '
                f'title="Exact: {p}">{float(p):.2%}</td>'
            )
        rows.append(f'<tr><th scope="row">{y:+d}</th>{"".join(cells)}</tr>')
    return (
        '<div class="scroll" tabindex="0" role="region" aria-label="Joint probability matrix">'
        f'<table class="heat"><caption>{_text(label)}: Y rows, X columns; '
        "cell intensity represents probability on a common 0 to 100% scale</caption>"
        f'<thead><tr><th scope="col">Y / X</th>{header}</tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def _marginals(pmf: JointPMF) -> str:
    blocks = []
    for axis in (0, 1):
        marginal = joint_marginal(pmf, axis)
        total = sum(w for _, w in marginal)
        rows = "".join(
            f'<tr><th scope="row">{x:+d}</th><td>{float(Fraction(w, total)):.2%}</td>'
            f"<td><code>{Fraction(w, total)}</code></td></tr>"
            for x, w in marginal
        )
        blocks.append(
            f'<div class="scroll" tabindex="0" role="region" aria-label="Marginal {"XY"[axis]}">'
            f'<table class="marginal"><caption>Marginal {"XY"[axis]}</caption>'
            '<thead><tr><th scope="col">Displacement</th><th scope="col">Mass</th>'
            f'<th scope="col">Exact</th></tr></thead><tbody>{rows}</tbody></table></div>'
        )
    return '<div class="grid">' + "".join(blocks) + "</div>"


def _example(scenario: str, seed: int) -> str:
    t, h = 52, 6
    path = study._path(scenario, seed, 0)
    ps = study._candidates(path[t - 23 : t + 1], h)
    ps["oracle"] = study._reference(scenario, t, h)
    actual = (
        sum(x for x, _ in path[t + 1 : t + h + 1]),
        sum(y for _, y in path[t + 1 : t + h + 1]),
    )
    blocks = []
    for model in study.MODELS:
        p = ps[model]
        blocks.append(
            f"<details><summary>{_LABELS[model]}</summary>"
            f"<p>Covariance: {_metric(str(joint_covariance(p)))}. "
            f"Both positive: {_metric(str(joint_positive_probability(p)), percent=True)}.</p>"
            + _heatmap(p, _LABELS[model])
            + _marginals(p)
            + "</details>"
        )
    return (
        '<section class="example"><h3>Fixed joint forecast example</h3>'
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
        raise ValueError("bivariate replay mismatch")
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
        "<title>MirrorMind | Multivariate Research Observatory</title><style>"
        + _STYLE
        + _STYLE_EXTRA
        + '</style></head><body><a class="skip" href="#main">Skip to report</a><main id="main">'
        '<header><p class="eyebrow">MIRRORMIND / EXPERIMENTAL RESEARCH</p>'
        '<h1>Multivariate Research Observatory</h1></header><aside class="notice">'
        "<strong>Synthetic only / Inference abstained</strong>"
        "<p>Bivariate discrete independent-in-time increments, not causal effects or serial dynamics. "
        "No statistical winner, calibration, holdout, independent registration or runtime attestation.</p>"
        '</aside><section class="panel"><h2>Study overview</h2><div class="grid">'
        f'<div class="stat">Paths<strong>{paths}</strong></div>'
        f'<div class="stat">Model-event scores<strong>{scores}</strong></div>'
        '<div class="stat">Local replay<strong>Matched</strong></div></div>'
        "<p>Matched independent and joint models share marginals. Joint Brier ranges from 0 to 2; "
        "reference excess is relative to the supplied generating law. Event means both displacements "
        "strictly positive. The oracle knows the future law, not outcomes. No pooling across horizons.</p>"
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
    parser = argparse.ArgumentParser(description="Offline fictional multivariate observatory")
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
        parser.exit(2, "Fictional bivariate observatory failed; existing output not overwritten.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
