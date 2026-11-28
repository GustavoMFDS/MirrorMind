"""Fixed fictional validation catalog; structural break occurs within validation."""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import replace
from decimal import Decimal

from examples.m1_census_research_runner import SCENARIOS, build_fixture
from mirrormind.domains.retail.census_experiment import prepare_census_experiment
from mirrormind.domains.retail.census_models import (
    census_model_comparison_sha256,
    compare_census_models,
    verify_census_model_comparison,
)
from mirrormind.domains.retail.census_split import CensusOriginSchedule
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

BREAK = "fictional-validation-break-v1"
CATALOG = (*SCENARIOS, BREAK)


def fixture(scenario: str) -> tuple[tuple[CensusVintageRecord, ...], CensusOriginSchedule]:
    if scenario != BREAK:
        return build_fixture(scenario)
    rows, plan = build_fixture("fictional-flat-v1")
    # Fixed design: a level step at index 53, inside validation.
    changed = tuple(
        replace(
            record, value=Decimal(230),
            snapshot_sha256=hashlib.sha256(f"fictional-validation-break-v1:{i}:230".encode()).hexdigest(),
        ) if i >= 53 else record
        for i, record in enumerate(rows)
    )
    return changed, plan


def run_catalog(revision: str) -> dict[str, object]:
    prepared = []
    for scenario in CATALOG:
        rows, plan = fixture(scenario)
        spec = prepare_census_experiment(rows, plan=plan, declared_code_revision=revision)
        prepared.append((scenario, rows, plan, spec, census_model_comparison_sha256(spec)))
    reports = []
    for scenario, rows, plan, spec, expected in prepared:
        result = compare_census_models(
            rows, plan=plan, spec=spec, expected_comparison_sha256=expected,
            declared_code_revision=revision,
        )
        submitted = json.dumps(
            result, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
        ).encode("ascii")
        if verify_census_model_comparison(
            rows, plan=plan, spec=spec, expected_comparison_sha256=expected,
            declared_code_revision=revision, submitted=submitted,
        ) != result["comparison_sha256"]:
            raise ValueError("model replay mismatch")
        reports.append({
            "scenario": scenario, "comparison_commitment_sha256": expected,
            "comparison_sha256": result["comparison_sha256"], "horizons": result["horizons"],
            "local_replay_matched": True,
        })
    return {
        "schema": "mirrormind.census.fictional_model_catalog.v1", "synthetic_only": True,
        "split": "validation", "declared_code_revision": revision, "reports": reports,
        "inference_status": "abstained", "winner": None, "confidence_interval": None,
        "registration_verified": False, "runtime_code_attested": False,
        "holdout_lock_verified": False, "action_authorized": False,
        "forecast_eligible": False, "ingestion_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Fictional five-model validation comparison")
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    try:
        report = run_catalog(args.revision)
        print(json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False))
    except (ValueError, TypeError):
        parser.exit(2, "Fictional model comparison failed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
