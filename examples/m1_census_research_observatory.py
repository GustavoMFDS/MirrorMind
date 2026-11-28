"""Generate a self-contained fictional research report, no network or server."""
from __future__ import annotations

import argparse
import math
import sqlite3
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory

from examples.m1_census_research_runner import (
    FIXTURE,
    SCENARIOS,
    Split,
    prepare_report,
    run_research,
)

_STYLE = """
:root{color-scheme:dark;--bg:#101722;--panel:#182331;--line:#344559;--text:#edf3fa;
--muted:#aebfd0;--blue:#78baff;--teal:#69dac4}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);
font:16px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:32px 20px 56px}
h1{font-size:clamp(1.7rem,4vw,2.8rem);line-height:1.2;margin:.3em 0}
h2{font-size:1.35rem}h3{font-size:1.05rem}p{margin:.5em 0 1em}
.eyebrow{color:var(--teal);font-weight:700;letter-spacing:.12em;font-size:.8rem}
.notice{border-left:4px solid #f7c86a;padding:12px 18px;background:var(--panel)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:20px;margin:20px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}
.stat{padding:12px;border:1px solid var(--line);border-radius:8px}
.stat strong{display:block;font-size:1.45rem}.muted,caption{color:var(--muted)}
table{border-collapse:collapse;width:100%;text-align:left;font-variant-numeric:tabular-nums}
th,td{padding:10px;border-bottom:1px solid var(--line)}td.num{text-align:right}
.scroll{overflow-x:auto}caption{text-align:left;padding:8px 0}
dt{font-weight:650}dd{margin:0 0 12px;overflow-wrap:anywhere}
code{font-size:.88em;overflow-wrap:anywhere}details{margin:12px 0}summary{cursor:pointer}
a{color:var(--blue)}a:focus-visible,summary:focus-visible,.scroll:focus-visible{outline:3px solid var(--teal)}
.skip{position:absolute;top:-100px}.skip:focus{top:8px;background:var(--panel);padding:12px;z-index:2}
.bar{display:flex;align-items:center;gap:10px;margin:5px 0}
.bar span{min-width:110px;font-size:.85rem}meter{width:100%;max-width:440px;height:18px;accent-color:var(--teal)}
@media(max-width:480px){main{padding:20px 12px}.panel{padding:12px}th,td{padding:8px}}
"""


def _text(value: object) -> str:
    return escape(str(value), quote=True)


def _number(value: object, *, percent: bool = False) -> str:
    if value is None:
        return "Unavailable"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("invalid metric")
    if not math.isfinite(value) or value < 0:
        raise ValueError("invalid metric")
    return f"{value * 100:.1f}%" if percent else f"{value:.2f}"


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError("expected report mapping")
    return value


def _render_split(value: object) -> str:
    split = _mapping(value)
    name = _text(split["split"])
    horizons = split["horizons"]
    if not isinstance(horizons, (tuple, list)):
        raise TypeError("expected horizon sequence")
    rows = []
    coverage = []
    abstentions: list[str] = []
    for item in horizons:
        h = _mapping(item)
        month = _text(h["horizon_months"])
        metrics = h["metrics"]
        coverage.append(
            f'<div class="bar"><span>{month} month(s)</span>'
            f'<meter min="0" max="1" value="{_text(h["coverage"])}">'
            f'{_number(h["coverage"], percent=True)}</meter>'
            f'<strong>{_number(h["coverage"], percent=True)}</strong></div>'
        )
        for key, label in (
            ("seasonal_naive_lag12", "Seasonal naive"),
            ("trailing_12_month_mean", "Trailing 12-month mean"),
        ):
            m = {} if metrics is None else _mapping(_mapping(metrics)[key])
            cells = "".join(
                f'<td class="num">{_number(m.get(metric), percent=metric == "wape")}</td>'
                for metric in ("mae", "rmse", "wape")
            )
            rows.append(f'<tr><th scope="row">{month}</th><td>{label}</td>{cells}'
                        f'<td class="num">{_text(h["scored_origins"])} / '
                        f'{_text(h["requested_origins"])}</td></tr>')
        reasons = _mapping(h["abstentions"])
        abstentions.extend(
            f'<tr><th scope="row">{month}</th><td>{_text(k)}</td>'
            f'<td class="num">{_text(v)}</td></tr>' for k, v in reasons.items()
        )
    return (
        f'<section class="panel" aria-labelledby="{name}"><h2 id="{name}">{name.title()}</h2>'
        '<p class="muted">Descriptive metrics in fictional units. WAPE is a percentage.</p>'
        '<div class="scroll" tabindex="0" role="region" aria-label="Metric table"><table>'
        '<caption>Matched origin errors by horizon and baseline</caption><thead><tr>'
        '<th scope="col">Months</th><th scope="col">Baseline</th><th scope="col">MAE</th>'
        '<th scope="col">RMSE</th><th scope="col">WAPE</th><th scope="col">Scored</th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
        '<h3>Evaluation coverage</h3>' + "".join(coverage) +
        '<details><summary>Abstention counts</summary><table><thead><tr>'
        '<th scope="col">Months</th><th scope="col">Reason</th><th scope="col">Count</th>'
        '</tr></thead><tbody>' + "".join(abstentions) + '</tbody></table></details>'
        '<details><summary>Receipt provenance</summary><dl><dt>SHA-256</dt><dd><code>'
        + _text(split["receipt_sha256"]) + '</code></dd><dt>Local replay matched</dt><dd>'
        + _text(split["stored_replay_matched"]) + '</dd><dt>Canonical receipt bytes</dt><dd>'
        + _text(split["receipt_bytes"]) + '</dd></dl></details></section>'
    )


def build_observatory(
    revision: str, splits: tuple[Split, ...], scenario: str = FIXTURE
) -> str:
    """Render only a freshly generated fictional demo; no external report input."""
    expected = prepare_report(revision, scenario)["experiment_sha256"]
    if not isinstance(expected, str):
        raise TypeError("invalid experiment identity")
    with TemporaryDirectory(prefix="mm-observatory-") as tmp:
        report = run_research(
            revision, journal_path=Path(tmp) / "journal.sqlite", expected=expected,
            splits=splits, commitment_mode="self_generated_demo", scenario=scenario,
        )
    values = report["splits"]
    if not isinstance(values, list):
        raise TypeError("invalid split summaries")
    sections = "".join(_render_split(item) for item in values)
    provenance = "".join(
        f'<dt>{label}</dt><dd><code>{_text(report[key])}</code></dd>'
        for key, label in (
            ("experiment_sha256", "Experiment"), ("input_manifest_sha256", "Input manifest"),
            ("schedule_sha256", "Schedule"), ("declared_code_revision", "Declared revision"),
            ("report_sha256", "Runner report"),
        )
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; '
        'style-src &apos;unsafe-inline&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
        '<title>MirrorMind | Research Observatory</title><style>' + _STYLE + '</style></head>'
        '<body><a class="skip" href="#main">Skip to report</a><main id="main">'
        '<header><p class="eyebrow">MIRRORMIND / EXPERIMENTAL RESEARCH</p>'
        '<h1>Research Observatory</h1><p class="muted">Fixed fictional Census experiment</p>'
        f'<p>Scenario: <code>{_text(report["fixture"])}</code></p></header>'
        '<aside class="notice"><strong>Synthetic only · Inference abstained</strong>'
        '<p>No statistical winner or calibrated interval. No real data, independent registration, '
        'holdout lock or runtime attestation. No action authorized.</p></aside>'
        '<section class="panel"><h2>Run overview</h2><div class="grid">'
        '<div class="stat"><span class="muted">Declared origins</span><strong>50</strong></div>'
        '<div class="stat"><span class="muted">Development / validation / holdout</span>'
        '<strong>30 / 10 / 10</strong></div><div class="stat"><span class="muted">Replayed splits</span>'
        f'<strong>{len(values)}</strong></div></div><p>Self-generated demo commitment; '
        'temporary local metadata journal.</p></section>'
        + sections + '<section class="panel"><h2>Experiment provenance</h2><dl>'
        + provenance + '</dl></section><footer class="muted">Offline fictional report. '
        'Digests support local reproducibility, not source authenticity.</footer></main></body></html>\n'
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate fictional research observatory HTML")
    parser.add_argument("--revision", required=True)
    parser.add_argument("--scenario", choices=SCENARIOS, default=FIXTURE)
    parser.add_argument("--split", choices=("validation", "holdout", "both"), default="validation")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if not args.output.is_absolute() or args.output.suffix.lower() != ".html":
            raise ValueError("absolute HTML output required")
        splits: tuple[Split, ...] = (
            ("validation", "holdout") if args.split == "both"
            else ("holdout",) if args.split == "holdout" else ("validation",)
        )
        html = build_observatory(args.revision, splits, args.scenario)
        with args.output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(html)
    except (ValueError, TypeError, OSError, sqlite3.Error):
        parser.exit(2, "Fictional observatory generation failed; existing output is not overwritten.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
