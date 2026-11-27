"""Measure fixed synthetic workloads; report timings, never infer real-world skill."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import time
from collections.abc import Callable
from pathlib import Path

from examples.m1_census_vintage_evaluation import run_synthetic_evaluation
from mirrormind.domains.retail.synthetic_decision_workflow import (
    SyntheticDecisionWorkflowRequest,
    run_synthetic_decision_workflow,
)
from mirrormind.modules.retrieval.contracts import EvidenceQuery
from mirrormind.modules.retrieval.fictional_fixture import build_fictional_index


def workloads() -> dict[str, Callable[[], object]]:
    """Each call includes fixture construction and the selected computation."""
    return {
        "retail_28d_2rep": lambda: run_synthetic_decision_workflow(
            SyntheticDecisionWorkflowRequest(replications=2, seed=317)
        ),
        "census_validation": lambda: run_synthetic_evaluation(split="validation"),
        "bm25_build_and_search": lambda: build_fictional_index().search(
            EvidenceQuery(text="inventory", top_k=5)
        ).model_dump(mode="json"),
    }


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, allow_nan=False).encode("utf-8")
    ).hexdigest()


def measure(repeats: int = 5) -> dict[str, object]:
    """Warm each fixed workload once and collect bounded wall-clock samples."""
    if type(repeats) is not int or not 2 <= repeats <= 20:
        raise ValueError("repeats must be an integer between 2 and 20")
    records = []
    for name, run in workloads().items():
        expected = digest(run())
        samples = []
        for _ in range(repeats):
            start = time.perf_counter_ns()
            result = run()
            elapsed = time.perf_counter_ns() - start
            if digest(result) != expected:
                raise RuntimeError("synthetic output changed within benchmark")
            samples.append(elapsed)
        records.append({
            "workload": name,
            "samples_ns": samples,
            "median_ns": statistics.median(samples),
            "min_ns": min(samples),
            "max_ns": max(samples),
            "output_sha256": expected,
        })
    return {
        "schema": "mirrormind.synthetic_benchmark.v1",
        "python": platform.python_version(),
        "platform": platform.system(),
        "machine": platform.machine(),
        "repeats": repeats,
        "warmups_per_workload": 1,
        "synthetic_only": True,
        "timing_gate": False,
        "workloads": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or not args.output.parent.is_dir():
        parser.error("output must be a new file in an existing directory")
    report = measure(args.repeats)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
