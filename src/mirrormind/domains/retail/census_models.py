"""Experimental five-model fictional validation protocol; not a forecast service."""
from __future__ import annotations

import hashlib
import hmac
import json
import re
from datetime import date
from fractions import Fraction
from typing import TypedDict

from mirrormind.domains.retail.census_evaluation import CENSUS_HORIZONS_MONTHS
from mirrormind.domains.retail.census_experiment import (
    CensusExperimentSpec,
    census_experiment_sha256,
    prepare_census_experiment,
)
from mirrormind.domains.retail.census_split import (
    CensusOriginSchedule,
    evaluate_frozen_census_split,
)
from mirrormind.domains.retail.census_vintages import (
    CensusVintageRecord,
    select_census_vintage_as_of,
)

PROTOCOL = "mirrormind.census.five_model_validation.v1"
MODELS = (
    "seasonal_naive_lag12", "trailing_12_month_mean", "persistence",
    "seasonal_drift_floor_zero", "linear_trend12_floor_zero",
)
MAX_MODEL_RECEIPT_BYTES = 4 * 1024 * 1024
_SHA = re.compile(r"[0-9a-f]{64}")


class _Pair(TypedDict):
    origin: str
    issue: str
    horizon: int
    target_month: str
    target_release_id: str
    target_snapshot_sha256: str
    as_of_manifest_sha256: str
    forecasts: dict[str, str]
    losses: dict[str, str]


def _canonical(payload: dict[str, object]) -> bytes:
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def _digest(payload: dict[str, object]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def census_model_comparison_sha256(spec: CensusExperimentSpec) -> str:
    """Distinct method identity; the legacy two-model receipt cannot substitute."""
    return _digest({
        "protocol": PROTOCOL, "base_experiment_sha256": census_experiment_sha256(spec),
        "models": MODELS, "history_months": 13, "split": "validation",
        "horizons": CENSUS_HORIZONS_MONTHS, "inference_policy": "always_abstain",
    })


def predict_census_models(history: tuple[Fraction, ...], horizon: int) -> dict[str, Fraction]:
    """Predict from 13 ordered consecutive monthly observations ending at origin."""
    if type(history) is not tuple or len(history) != 13 or any(
        type(v) is not Fraction or v < 0 or v.numerator.bit_length() > 2048
        or v.denominator.bit_length() > 2048 for v in history
    ):
        raise ValueError("13 bounded nonnegative exact observations required")
    if type(horizon) is not int or horizon not in CENSUS_HORIZONS_MONTHS:
        raise ValueError("invalid horizon")
    recent = history[1:]
    mean = sum(recent, Fraction()) / 12
    center = Fraction(11, 2)
    slope = sum(
        ((i - center) * v for i, v in enumerate(recent)), Fraction()
    ) / sum(((i - center) ** 2 for i in range(12)), Fraction())
    seasonal = history[horizon]
    return dict(zip(MODELS, (
        seasonal, mean, history[-1],
        max(Fraction(), seasonal + history[-1] - history[0]),
        max(Fraction(), mean + slope * (11 + horizon - center)),
    ), strict=True))


def _offset(month: date, offset: int) -> date:
    year, index = divmod(month.year * 12 + month.month - 1 + offset, 12)
    return date(year, index + 1, 1)


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError("invalid evaluation mapping")
    return value


def _sequence(value: object) -> tuple[object, ...]:
    if not isinstance(value, tuple):
        raise TypeError("invalid evaluation sequence")
    return value


def _string(value: object) -> str:
    if not isinstance(value, str):
        raise TypeError("invalid evaluation string")
    return value


def _integer(value: object) -> int:
    if type(value) is not int:
        raise TypeError("invalid evaluation integer")
    return value


def compare_census_models(
    records: tuple[CensusVintageRecord, ...], *,
    plan: CensusOriginSchedule,
    spec: CensusExperimentSpec,
    expected_comparison_sha256: str,
    declared_code_revision: str,
) -> dict[str, object]:
    """Compare only the validation partition under a retained model commitment."""
    identity = census_model_comparison_sha256(spec)
    if (
        type(expected_comparison_sha256) is not str
        or not _SHA.fullmatch(expected_comparison_sha256)
        or not hmac.compare_digest(identity, expected_comparison_sha256)
    ):
        raise ValueError("model comparison fingerprint mismatch")
    if prepare_census_experiment(
        records, plan=plan, declared_code_revision=declared_code_revision
    ) != spec:
        raise ValueError("model comparison inputs differ from commitment")
    frozen = evaluate_frozen_census_split(
        records, plan=plan, expected_schedule_sha256=spec.schedule_sha256, split="validation"
    )
    descriptive = _mapping(frozen["evaluation"])
    legacy = _mapping(descriptive["evaluation"])
    if legacy["input_manifest_sha256"] != spec.input_manifest_sha256:
        raise ValueError("model comparison manifest mismatch")
    first = {r.reference_month: r for r in records if r.release_kind == "first_estimate"}
    features = tuple(r for r in records if r.reference_month in first)
    pairs: list[_Pair] = []
    for raw in _sequence(descriptive["paired_losses"]):
        row = _mapping(raw)
        origin = date.fromisoformat(_string(row["reference_month"]))
        issue = date.fromisoformat(_string(row["issued_on"]))
        horizon = _integer(row["horizon_months"])
        view = select_census_vintage_as_of(
            features, series_id=plan.series_id, target_release_on=issue
        )
        visible = {r.reference_month: r for r in view.records}
        # At the earliest supported calendar month, the extra month may not exist.
        try:
            months = tuple(_offset(origin, i) for i in range(-12, 1))
        except ValueError:
            continue
        if any(m not in visible for m in months):
            continue
        forecasts = predict_census_models(tuple(Fraction(visible[m].value) for m in months), horizon)
        target = first[date.fromisoformat(_string(row["target_month"]))]
        if (
            target.published_on <= issue or target.release_id != row["target_release_id"]
            or target.snapshot_sha256 != row["target_snapshot_sha256"]
        ):
            raise ValueError("target lineage mismatch")
        losses = {key: abs(value - Fraction(target.value)) for key, value in forecasts.items()}
        if (
            losses[MODELS[0]] != Fraction(_string(row["seasonal_naive_absolute_loss"]))
            or losses[MODELS[1]] != Fraction(_string(row["trailing_mean_absolute_loss"]))
        ):
            raise ValueError("legacy loss parity mismatch")
        pairs.append({
            "origin": origin.isoformat(), "issue": issue.isoformat(), "horizon": horizon,
            "target_month": target.reference_month.isoformat(), "target_release_id": target.release_id,
            "target_snapshot_sha256": target.snapshot_sha256,
            "as_of_manifest_sha256": _string(row["as_of_vintage_manifest_sha256"]),
            "forecasts": {k: str(v) for k, v in forecasts.items()},
            "losses": {k: str(v) for k, v in losses.items()},
        })
    summaries: list[dict[str, object]] = []
    for h in CENSUS_HORIZONS_MONTHS:
        subset = [r for r in pairs if r["horizon"] == h]
        old = next(
            _mapping(r) for r in _sequence(legacy["horizons"])
            if _mapping(r)["horizon_months"] == h
        )
        requested = _integer(old["requested_origins"])
        legacy_scored = _integer(old["scored_origins"])
        means: dict[str, str | None] = {}
        differences: dict[str, str | None] = {}
        for key in MODELS:
            means[key] = (
                str(sum((Fraction(r["losses"][key]) for r in subset), Fraction()) / len(subset))
                if len(subset) >= 2 else None
            )
            differences[key] = (
                str(sum((
                    Fraction(r["losses"][key]) - Fraction(r["losses"][MODELS[0]])
                    for r in subset
                ), Fraction()) / len(subset)) if len(subset) >= 2 else None
            )
        summaries.append({
            "horizon": h, "requested": requested, "legacy_scored": legacy_scored,
            "common_scored": len(subset), "extra_history_abstentions": legacy_scored - len(subset),
            "coverage": len(subset) / requested, "mae_exact": means,
            "mean_loss_difference_vs_seasonal_exact": differences,
        })
    report: dict[str, object] = {
        "protocol": PROTOCOL, "comparison_commitment_sha256": identity,
        "declared_code_revision": declared_code_revision, "models": MODELS, "split": "validation",
        "input_manifest_sha256": spec.input_manifest_sha256, "schedule_sha256": spec.schedule_sha256,
        "legacy_receipt_sha256": descriptive["descriptive_sha256"], "paired": pairs,
        "horizons": summaries, "source_status": "caller_supplied_not_source_verified",
        "inference_status": "abstained", "winner": None, "confidence_interval": None,
        "registration_verified": False, "runtime_code_attested": False, "holdout_lock_verified": False,
        "forecast_eligible": False, "ingestion_authorized": False, "action_authorized": False,
    }
    report["comparison_sha256"] = _digest(report)
    return report


def verify_census_model_comparison(
    records: tuple[CensusVintageRecord, ...], *,
    plan: CensusOriginSchedule, spec: CensusExperimentSpec, expected_comparison_sha256: str,
    declared_code_revision: str, submitted: bytes,
) -> str:
    """Verify bounded complete canonical receipt by local replay; no admission."""
    if type(submitted) is not bytes or not 1 <= len(submitted) <= MAX_MODEL_RECEIPT_BYTES:
        raise ValueError("bounded canonical model receipt required")
    result = compare_census_models(
        records, plan=plan, spec=spec, expected_comparison_sha256=expected_comparison_sha256,
        declared_code_revision=declared_code_revision,
    )
    encoded = _canonical(result)
    if len(encoded) > MAX_MODEL_RECEIPT_BYTES or not hmac.compare_digest(encoded, submitted):
        raise ValueError("model receipt does not match local replay")
    return _string(result["comparison_sha256"])
