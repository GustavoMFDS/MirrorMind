"""Run a complete fictional research experiment without external data.

Example: python -m examples.m1_census_research_runner demo --revision <sha>
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sqlite3
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal

from mirrormind.domains.retail.census_evaluation import CensusForecastOrigin
from mirrormind.domains.retail.census_experiment import (
    CensusExperimentSpec,
    census_experiment_sha256,
    execute_census_experiment,
    prepare_census_experiment,
)
from mirrormind.domains.retail.census_experiment_journal import CensusExperimentJournal
from mirrormind.domains.retail.census_split import CensusOriginSchedule
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

SCHEMA = "mirrormind.census.fictional_research_run.v1"
FIXTURE = "fictional-trend-seasonal-v1"
SERIES = "FICTIONAL_RETAIL"
Split = Literal["validation", "holdout"]


def _month(i: int) -> date:
    return date(2000 + i // 12, i % 12 + 1, 1)


def build_fixture() -> tuple[tuple[CensusVintageRecord, ...], CensusOriginSchedule]:
    """Invent every release and value; no source or input-file access."""
    rows = tuple(
        CensusVintageRecord(
            SERIES, _month(i), Decimal(100 + 2 * i + 3 * (i % 12)),
            _month(i + 1), "first_estimate", f"fictional-{i}", f"{i:064x}",
        )
        for i in range(80)
    )
    indices = (*range(12, 42), *range(48, 58), *range(64, 74))
    schedule = CensusOriginSchedule(SERIES, tuple(
        CensusForecastOrigin(_month(i), _month(i + 1) + timedelta(days=1))
        for i in indices
    ))
    return rows, schedule


def _canonical(value: dict[str, object]) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def _prepare(revision: str) -> tuple[
    tuple[CensusVintageRecord, ...], CensusOriginSchedule, CensusExperimentSpec, str
]:
    rows, plan = build_fixture()
    spec = prepare_census_experiment(rows, plan=plan, declared_code_revision=revision)
    return rows, plan, spec, census_experiment_sha256(spec)


def _identity(spec: CensusExperimentSpec, eid: str) -> dict[str, object]:
    return {
        "experiment_sha256": eid,
        "fixture": FIXTURE,
        "schedule_sha256": spec.schedule_sha256,
        "input_manifest_sha256": spec.input_manifest_sha256,
        "declared_code_revision": spec.declared_code_revision,
        "synthetic_only": True,
        "registration_verified": False,
        "runtime_code_attested": False,
        "holdout_lock_verified": False,
        "forecast_eligible": False,
        "ingestion_authorized": False,
        "action_authorized": False,
        "inference_status": "abstained",
    }


def prepare_report(revision: str) -> dict[str, object]:
    _, _, spec, eid = _prepare(revision)
    return dict(_identity(spec, eid), schema_version=SCHEMA, status="prepared_not_executed")


def run_research(
    revision: str,
    *,
    journal_path: Path,
    expected: str,
    splits: tuple[Split, ...],
    commitment_mode: Literal["caller_retained", "self_generated_demo"],
) -> dict[str, object]:
    """Fixed fictional run; each split admits and replays independently."""
    if splits not in (("validation",), ("holdout",), ("validation", "holdout")):
        raise ValueError("invalid split selection")
    if commitment_mode not in ("caller_retained", "self_generated_demo"):
        raise ValueError("invalid commitment mode")
    rows, plan, spec, eid = _prepare(revision)
    if type(expected) is not str or not expected.isascii() or not hmac.compare_digest(expected, eid):
        raise ValueError("experiment fingerprint mismatch")
    journal = CensusExperimentJournal(journal_path)
    journal.register(
        rows, plan=plan, spec=spec, expected_experiment_sha256=eid, declared_code_revision=revision
    )
    summaries: list[dict[str, object]] = []
    for selected in splits:
        split: Split
        if selected == "validation":
            split = "validation"
        elif selected == "holdout":
            split = "holdout"
        else:
            raise ValueError("invalid split")
        result = execute_census_experiment(
            rows, plan=plan, spec=spec, expected_experiment_sha256=eid,
            split=split, declared_code_revision=revision,
        )
        submitted = _canonical(result)
        digest = journal.admit(
            eid, rows, plan=plan, split=split, declared_code_revision=revision, submitted=submitted
        )
        reopened = CensusExperimentJournal(journal_path)
        if reopened.verify_stored(
            eid, rows, plan=plan, split=split, declared_code_revision=revision, submitted=submitted
        ) != digest:
            raise ValueError("stored replay mismatch")
        frozen = result["evaluation"]
        if not isinstance(frozen, dict):
            raise TypeError("invalid frozen result")
        descriptive = frozen["evaluation"]
        if not isinstance(descriptive, dict):
            raise TypeError("invalid descriptive result")
        evaluation = descriptive["evaluation"]
        if not isinstance(evaluation, dict):
            raise TypeError("invalid evaluation result")
        summaries.append({
            "split": split, "receipt_sha256": digest, "receipt_bytes": len(submitted),
            "stored_replay_matched": True, "split_sizes": frozen["split_sizes"],
            "horizons": evaluation["horizons"],
            "confidence_interval": None, "winner": None,
        })
    report = dict(
        _identity(spec, eid), schema_version=SCHEMA, status="synthetic_run_replayed",
        commitment_mode=commitment_mode, splits=summaries,
    )
    report["report_sha256"] = hashlib.sha256(_canonical(report)).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Fictional Census research runner")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("prepare", "demo", "run"):
        sub = commands.add_parser(command)
        sub.add_argument("--revision", required=True, help="Caller-declared Git revision")
        if command != "prepare":
            sub.add_argument("--split", choices=("validation", "holdout", "both"), default="validation")
        if command == "run":
            sub.add_argument("--expected", required=True)
            sub.add_argument("--journal", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            report = prepare_report(args.revision)
        else:
            splits: tuple[Split, ...] = (
                ("validation", "holdout") if args.split == "both"
                else ("holdout",) if args.split == "holdout" else ("validation",)
            )
            if args.command == "demo":
                _, _, _, eid = _prepare(args.revision)
                with TemporaryDirectory(prefix="mm-fictional-research-") as tmp:
                    report = run_research(
                        args.revision, journal_path=Path(tmp) / "journal.sqlite",
                        expected=eid, splits=splits, commitment_mode="self_generated_demo",
                    )
            else:
                report = run_research(
                    args.revision, journal_path=args.journal, expected=args.expected,
                    splits=splits, commitment_mode="caller_retained",
                )
        output = _canonical(report).decode("ascii")
    except (ValueError, TypeError, OSError, sqlite3.Error):
        parser.exit(2, "Fictional research run failed; prior committed splits may remain.\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
