"""Offline fictional probability study report; no external report input."""
from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path

from examples import m1_census_probability_study as study
from examples.m1_census_research_observatory import _STYLE, _mapping, _text
from mirrormind.domains.retail.census_probability import convolve_increments, score_discrete_pmf

_LABELS = {
    "point": "Point persistence", "narrow": "Narrow fixed", "fixed": "Fixed law",
    "rolling24": "Rolling empirical 24", "oracle": "Oracle (privileged reference)",
}
_EXAMPLE_PATH = 0
_EXAMPLE_ORIGIN = 52
_EXAMPLE_HORIZON = 6


def _metric(value: object, *, percent: bool = False) -> str:
    if not isinstance(value, str):
        raise TypeError("expected rational metric")
    exact = Fraction(value)
    display = f"{float(exact * 100):.2f}%" if percent else f"{float(exact):.4f}"
    return f'<span title="Exact: {_text(value)}">{display}</span>'


def _example(scenario: str, seed: int) -> str:
    origin, h = _EXAMPLE_ORIGIN, _EXAMPLE_HORIZON
    increments = study._path(scenario, seed, _EXAMPLE_PATH)
    pmfs = study._candidates(increments[origin - 23:origin + 1], h)
    pmfs["oracle"] = convolve_increments(tuple(
        study._law(study._amplitude(scenario, i)) for i in range(origin + 1, origin + h + 1)
    ))
    observed = sum(increments[origin + 1:origin + h + 1])
    blocks = []
    for model in study.MODELS:
        pmf = pmfs[model]
        total = sum(w for _, w in pmf)
        scores = score_discrete_pmf(pmf, observed)
        bars = "".join(
            f'<div class="mass"><span>{x:+d}</span><meter min="0" max="1" '
            f'value="{float(Fraction(w, total)):.12g}" aria-label="Displacement {x} probability">'
            f'{float(Fraction(w, total)):.2%}</meter>'
            f'<span>{float(Fraction(w, total)):.2%}</span>'
            f'<code>{Fraction(w, total)}</code></div>' for x, w in pmf
        )
        blocks.append(
            f'<details><summary>{_LABELS[model]} distribution</summary>'
            f'<p>10/50/90 quantiles: {scores.lower}, {scores.median}, {scores.upper}. '
            f'CRPS: {_metric(str(scores.crps))}. Covered: {scores.covered}.</p>'
            '<div class="scroll" tabindex="0" role="region" aria-label="Probability masses">'
            + bars + '</div></details>'
        )
    return (
        '<section class="panel"><h3>Fixed illustrative forecast</h3>'
        f'<p>Path {_EXAMPLE_PATH}, origin {origin}, horizon {h} months. '
        f'Realized displacement: <strong>{observed:+d}</strong>. '
        'Generated again from the same fixed study design; not an additional study.</p>'
        '<p class="muted">Each bar is probability mass at the indicated integer displacement; '
        'exact mass shown as a fraction. The oracle knows the generating law.</p>'
        + "".join(blocks) + '</section>'
    )


def _group(group: dict[str, object]) -> str:
    scenario = group["scenario"]
    seed = group["seed"]
    rows = group["rows"]
    if not isinstance(scenario, str) or type(seed) is not int or not isinstance(rows, list):
        raise TypeError("invalid group")
    cells = []
    for raw in rows:
        row = _mapping(raw)
        model = row["model"]
        if not isinstance(model, str):
            raise TypeError("invalid model")
        metrics = "".join(
            f'<td class="num">{_metric(row[key], percent=key in ("coverage", "reference_coverage"))}</td>'
            for key in study.FIELDS
        )
        exact = " / ".join(_text(row[key]) for key in study.FIELDS)
        cells.append(
            f'<tr><th scope="row">{_text(row["horizon"])}</th>'
            f'<td>{_LABELS[model]}</td>{metrics}<td>{_text(row["pairs"])}</td></tr>'
            f'<tr><td colspan="9"><details><summary>Exact rational scores</summary>'
            f'<code>{exact}</code></details></td></tr>'
        )
    return (
        f'<article id="{_text(scenario)}" class="panel"><h2>{_text(scenario.replace("_", " ").title())}</h2>'
        f'<p>Seed {seed}; {_text(group["paths"])} paths.</p>'
        '<div class="scroll" tabindex="0" role="region" aria-label="Group metric table">'
        '<table><caption>Separate per-horizon descriptive means; exact scores in column order</caption>'
        '<thead><tr><th scope="col">Months</th><th scope="col">Method</th>'
        '<th scope="col">CRPS</th><th scope="col">Pinball</th><th scope="col">Median MAE</th>'
        '<th scope="col">Observed coverage</th><th scope="col">Width</th>'
        '<th scope="col">Reference coverage</th><th scope="col">Pairs</th></tr></thead>'
        '<tbody>' + "".join(cells) + '</tbody></table></div>'
        + _example(scenario, seed)
        + '<p>Event transcript SHA-256: <code>' + _text(group["event_transcript_sha256"])
        + '</code></p></article>'
    )


def build_observatory(revision: str) -> str:
    expected = study.prepare_study(revision)["study_sha256"]
    if not isinstance(expected, str):
        raise TypeError("invalid study identity")
    report = study.execute_study(revision, expected)
    if study.verify_study(revision, expected, study.canonical(report)) != report["report_sha256"]:
        raise ValueError("study replay mismatch")
    groups = report["groups"]
    if not isinstance(groups, list):
        raise TypeError("invalid group sequence")
    sections = "".join(_group(_mapping(group)) for group in groups)
    evaluations = len(study.SCENARIOS) * study.PATHS * len(study.ORIGINS) * len(study.HORIZONS) * len(study.MODELS)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; '
        'style-src &apos;unsafe-inline&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
        '<title>MirrorMind | Probabilistic Research Observatory</title><style>' + _STYLE
        + '.mass{display:grid;grid-template-columns:45px minmax(70px,1fr) 75px 100px;'
        'gap:8px;align-items:center;min-width:310px;margin:4px 0}.mass code{font-size:.8rem}'
        '</style></head><body><a class="skip" href="#main">Skip to report</a><main id="main">'
        '<header><p class="eyebrow">MIRRORMIND / EXPERIMENTAL RESEARCH</p>'
        '<h1>Probabilistic Research Observatory</h1></header><aside class="notice">'
        '<strong>Synthetic only / Inference abstained</strong>'
        '<p>No statistical winner, calibration certificate, holdout, independent registration '
        'or runtime attestation. Overlapping events are not independent samples.</p></aside>'
        '<section class="panel"><h2>Study overview</h2><div class="grid">'
        f'<div class="stat">Paths<strong>{len(study.SCENARIOS) * study.PATHS}</strong></div>'
        f'<div class="stat">Model-event scores<strong>{evaluations}</strong></div>'
        '<div class="stat">Local report replay<strong>Matched</strong></div></div>'
        '<p>Observed coverage counts actual simulated outcomes. Reference coverage is '
        'probability under the supplied generating law. Discrete central intervals may exceed 80%. '
        'CRPS and width measure different properties; no ranking or pooling.</p>'
        '<nav aria-label="Scenario navigation"><a href="#stationary">Stationary</a> | '
        '<a href="#variance_shift">Variance shift</a></nav></section>'
        + sections + '<section class="panel"><h2>Provenance</h2><dl>'
        f'<dt>Study</dt><dd><code>{_text(expected)}</code></dd>'
        f'<dt>Report</dt><dd><code>{_text(report["report_sha256"])}</code></dd>'
        f'<dt>Declared revision</dt><dd><code>{_text(revision)}</code></dd>'
        '<dt>Commitment</dt><dd>Self-generated demo; not independent registration.</dd>'
        '</dl></section></main></body></html>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline fictional probabilistic observatory")
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
        parser.exit(2, "Fictional probability observatory failed; existing output not overwritten.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
