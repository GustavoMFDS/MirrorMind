#!/usr/bin/env python3
"""Repeatable, synthetic-only end-to-end retail residual microbenchmark.

Run this same script against clean checkouts of two known Git revisions.
Only local Python allocations are tracked: tracemalloc is NOT process RSS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import subprocess
import sys
import tracemalloc
from datetime import date, timedelta
from pathlib import Path
from time import perf_counter_ns

SCRIPT_ROOT = Path(__file__).resolve().parents[2]
START = date(2011, 1, 1)


def validate_checkout(root: Path, expected_head: str) -> str:
    """Fail closed on a changed revision or tracked modifications."""
    if re.fullmatch(r"[0-9a-f]{40}", expected_head) is None:
        raise ValueError("expected_head must be a full lowercase 40-digit Git SHA")
    if not (root / "src" / "mirrormind" / "domains" / "retail" /
            "residual_envelope.py").is_file():
        raise ValueError("source checkout has no retail residual evaluator")
    head = subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=root, check=True,
        capture_output=True, text=True, timeout=30,
    ).stdout.strip()
    if head != expected_head:
        raise ValueError("source checkout HEAD differs from expected_head")
    dirty = subprocess.run(
        ("git", "status", "--porcelain", "--untracked-files=no"),
        cwd=root, check=True, capture_output=True, text=True, timeout=30,
    ).stdout.strip()
    if dirty:
        raise ValueError("source checkout contains modified tracked files")
    return head


def invented_inputs(profile: str):
    """Build bounded imaginary positive-line days; no workbook or customer fields."""
    from mirrormind.domains.retail.declared_releases import DeclaredProductRelease
    from mirrormind.domains.retail.uci_transactions import ProductDayUnits, UciRetailProjection

    if profile not in ("dense", "delayed"):
        raise ValueError("profile must be dense or delayed")
    days = []
    releases = []
    for index in range(1, 201):
        if profile == "delayed" and index % 23 == 0:
            continue
        event = START + timedelta(days=index - 1)
        units = ((index * 37 + 17) % 71) + 1
        published = event + timedelta(days=4 if profile == "delayed" and index % 11 == 0
                                      else 0)
        days.append(ProductDayUnits("TOY-ONLY", event, units))
        releases.append(DeclaredProductRelease("TOY-ONLY", event, published))
    projection = UciRetailProjection(
        days=tuple(days), processed_rows=len(days), accepted_rows=len(days),
        cancelled_rows=0, negative_quantity_rows=0, zero_quantity_rows=0,
    )
    return projection, tuple(releases)


def fingerprint(report: dict[str, object]) -> str:
    """Hash a complete, identifier-minimized receipt for parity across revisions."""
    serialized = json.dumps(report, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def measure(root: Path, head: str, profile: str, repetitions: int, warmups: int):
    """Time end-to-end calls separately from tracemalloc peak observations."""
    validate_checkout(root, head)
    if not 5 <= repetitions <= 100 or not 1 <= warmups <= 15:
        raise ValueError("repetitions must be 5..100 and warmups 1..15")
    # A script process measures exactly one checkout; prevent mixed-module imports.
    sys.path.insert(0, str(root / "src"))
    from mirrormind.domains.retail.residual_envelope import evaluate_retail_residual_envelopes

    projection, releases = invented_inputs(profile)
    kwargs = dict(
        stock_code="TOY-ONLY",
        evaluation_on=START + timedelta(days=179),
        holdout_days=30,
        calibration_days=60,
        min_calibration_residuals=5,
    )

    def one():
        return evaluate_retail_residual_envelopes(projection, releases, **kwargs)

    expected = fingerprint(one())
    for _ in range(warmups):
        if fingerprint(one()) != expected:
            raise RuntimeError("benchmark results changed across warmups")
    samples = []
    for _ in range(repetitions):
        start = perf_counter_ns()
        report = one()
        elapsed = perf_counter_ns() - start
        if fingerprint(report) != expected:
            raise RuntimeError("benchmark results changed during measurements")
        samples.append(elapsed / 1_000_000)

    # Memory is measured after timing so the tracer does not alter time samples.
    tracemalloc.start()
    try:
        memory_report = one()
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    if fingerprint(memory_report) != expected:
        raise RuntimeError("memory measurement changed the evaluator report")

    return {
        "status": "synthetic_local_benchmark_not_official_ci",
        "source_head_sha": head,
        "profile": profile,
        "synthetic_product_days": len(projection.days),
        "requested_origins": 30,
        "calibration_days": 60,
        "repetitions": repetitions,
        "warmups": warmups,
        "median_elapsed_ms": round(statistics.median(samples), 5),
        "minimum_elapsed_ms": round(min(samples), 5),
        "maximum_elapsed_ms": round(max(samples), 5),
        "peak_traced_python_kib": round(peak / 1024, 3),
        "peak_memory_metric": "tracemalloc_peak_python_allocations_not_process_rss",
        "report_sha256": expected,
        "evaluated_origins": memory_report["evaluated_origins"],
        "retrospective_covered_origins": memory_report["retrospective_covered_origins"],
        "nominal_coverage": None,
        "calibrated_prediction_interval": None,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=SCRIPT_ROOT)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--profile", choices=("dense", "delayed"), required=True)
    parser.add_argument("--repetitions", type=int, default=21)
    parser.add_argument("--warmups", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        result = measure(
            args.source_root.resolve(), args.expected_head, args.profile,
            args.repetitions, args.warmups,
        )
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        print(f"Benchmark refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
