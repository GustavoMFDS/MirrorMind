"""Pure fictional experiment identity and local replay; no trusted registry."""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from typing import Literal

from mirrormind.domains.retail.census_evaluation import (
    CENSUS_BACKTEST_SCHEMA,
    census_evaluation_manifest_sha256,
)
from mirrormind.domains.retail.census_split import (
    CensusOriginSchedule,
    census_schedule_sha256,
    evaluate_frozen_census_split,
)
from mirrormind.domains.retail.census_vintages import CensusVintageRecord

CENSUS_EXPERIMENT_PROTOCOL = "mirrormind.census.fictional_experiment.v1"
MAX_CENSUS_RECEIPT_BYTES = 4 * 1024 * 1024
_SHA256 = re.compile(r"[0-9a-f]{64}")
_GIT_SHA1 = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True, slots=True)
class CensusExperimentSpec:
    """Caller-retained commitment; declared revision is not attestation."""

    schedule_sha256: str
    input_manifest_sha256: str
    declared_code_revision: str


def _canonical(payload: dict[str, object]) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def _digest(payload: dict[str, object]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def census_experiment_sha256(spec: CensusExperimentSpec) -> str:
    """Bind exact input, schedule and declared revision to the fixed protocol."""
    if type(spec) is not CensusExperimentSpec:
        raise ValueError("exact experiment specification required")
    for value, pattern in (
        (spec.schedule_sha256, _SHA256),
        (spec.input_manifest_sha256, _SHA256),
        (spec.declared_code_revision, _GIT_SHA1),
    ):
        if type(value) is not str or not pattern.fullmatch(value):
            raise ValueError("malformed experiment identity")
    return _digest({
        "protocol": CENSUS_EXPERIMENT_PROTOCOL,
        "evaluation_schema": CENSUS_BACKTEST_SCHEMA,
        "descriptive_schema": "mirrormind.census.descriptive.v1",
        "split_schema": "mirrormind.census.frozen_split.v1",
        "schedule_sha256": spec.schedule_sha256,
        "input_manifest_sha256": spec.input_manifest_sha256,
        "declared_code_revision": spec.declared_code_revision,
        "inference_policy": "always_abstain",
    })


def prepare_census_experiment(
    records: tuple[CensusVintageRecord, ...],
    *,
    plan: CensusOriginSchedule,
    declared_code_revision: str,
) -> CensusExperimentSpec:
    """Create a local commitment; does not evaluate or register a holdout."""
    schedule = census_schedule_sha256(plan)
    manifest = census_evaluation_manifest_sha256(
        records, series_id=plan.series_id, cutoff=plan.origins[0].issued_on
    )
    spec = CensusExperimentSpec(schedule, manifest, declared_code_revision)
    census_experiment_sha256(spec)
    return spec


def execute_census_experiment(
    records: tuple[CensusVintageRecord, ...],
    *,
    plan: CensusOriginSchedule,
    spec: CensusExperimentSpec,
    expected_experiment_sha256: str,
    split: Literal["validation", "holdout"],
    declared_code_revision: str,
) -> dict[str, object]:
    """Evaluate only after matching the caller-retained commitment."""
    actual = census_experiment_sha256(spec)
    if (
        type(expected_experiment_sha256) is not str
        or not _SHA256.fullmatch(expected_experiment_sha256)
        or not hmac.compare_digest(actual, expected_experiment_sha256)
    ):
        raise ValueError("experiment fingerprint mismatch")
    if type(split) is not str or split not in ("validation", "holdout"):
        raise ValueError("invalid split")
    if prepare_census_experiment(
        records, plan=plan, declared_code_revision=declared_code_revision
    ) != spec:
        raise ValueError("experiment inputs differ from commitment")
    result = evaluate_frozen_census_split(
        records, plan=plan, expected_schedule_sha256=spec.schedule_sha256, split=split
    )
    descriptive = result["evaluation"]
    if not isinstance(descriptive, dict):
        raise TypeError("invalid descriptive evaluation")
    evaluation = descriptive.get("evaluation")
    if not isinstance(evaluation, dict) or (
        evaluation.get("input_manifest_sha256") != spec.input_manifest_sha256
    ):
        raise ValueError("evaluation manifest mismatch")
    payload: dict[str, object] = {
        "protocol": CENSUS_EXPERIMENT_PROTOCOL,
        "experiment_sha256": actual,
        "split": split,
        "evaluation": result,
        "input_commitment_matched": True,
        "runtime_code_attested": False,
        "registration_verified": False,
        "holdout_lock_verified": False,
        "inference_status": "abstained",
        "action_authorized": False,
        "ingestion_authorized": False,
        "forecast_eligible": False,
    }
    payload["receipt_sha256"] = _digest(payload)
    return payload


def verify_census_experiment_receipt(
    records: tuple[CensusVintageRecord, ...],
    *,
    plan: CensusOriginSchedule,
    spec: CensusExperimentSpec,
    expected_experiment_sha256: str,
    split: Literal["validation", "holdout"],
    declared_code_revision: str,
    submitted: bytes,
) -> str:
    """Compare bounded canonical bytes to local replay, never parse submission."""
    if type(submitted) is not bytes or not 1 <= len(submitted) <= MAX_CENSUS_RECEIPT_BYTES:
        raise ValueError("bounded canonical receipt bytes required")
    expected = execute_census_experiment(
        records, plan=plan, spec=spec, expected_experiment_sha256=expected_experiment_sha256,
        split=split, declared_code_revision=declared_code_revision,
    )
    encoded = _canonical(expected)
    if len(encoded) > MAX_CENSUS_RECEIPT_BYTES or not hmac.compare_digest(encoded, submitted):
        raise ValueError("receipt does not match local replay")
    digest = expected["receipt_sha256"]
    if not isinstance(digest, str) or not _SHA256.fullmatch(digest):
        raise ValueError("invalid expected receipt digest")
    return digest
