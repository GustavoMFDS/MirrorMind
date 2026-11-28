"""Versioned fictional bivariate study; no external inputs."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import re
from collections import Counter
from fractions import Fraction
from functools import lru_cache

from examples.m1_census_probability_study import canonical
from mirrormind.domains.retail.census_bivariate import (
    JointPMF,
    canonical_joint_pmf,
    convolve_joint_increments,
    independent_joint_projection,
    joint_brier_score,
    joint_covariance,
    joint_marginal,
    joint_positive_probability,
    reference_joint_brier_excess,
)
from mirrormind.domains.retail.census_probability import score_discrete_pmf

PROTOCOL = "mirrormind.census.fictional_bivariate_study.v1"
SCENARIOS = (("positive", 111001), ("independent", 111002), ("negative", 111003), ("shift", 111004))
CELLS = ((-4, -4), (-4, 4), (4, -4), (4, 4))
POS = (3, 1, 1, 3)
IND = (1, 1, 1, 1)
NEG = (1, 3, 3, 1)
MODELS = ("fixed_independent", "product24", "joint24", "oracle")
HORIZONS = (1, 3, 6)
ORIGINS = tuple(range(48, 58))
PATHS = 16
FIELDS = (
    "joint_brier",
    "reference_excess",
    "marginal_crps_x",
    "marginal_crps_y",
    "event_brier",
    "predicted_event",
    "observed_event",
    "covariance",
)
MAX_RECEIPT_BYTES = 1024 * 1024


def _sha(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def prepare_study(revision: str) -> dict[str, object]:
    if type(revision) is not str or not re.fullmatch("[0-9a-f]{40}", revision):
        raise ValueError("declared Git SHA-1 required")
    design = {
        "protocol": PROTOCOL,
        "declared_code_revision": revision,
        "scenario_seeds": SCENARIOS,
        "paths_per_scenario": PATHS,
        "cells": CELLS,
        "positive_weights": POS,
        "independent_weights": IND,
        "negative_weights": NEG,
        "shift_index": 53,
        "shift_from": "positive",
        "shift_to": "negative",
        "months": 64,
        "origins": ORIGINS,
        "horizons": HORIZONS,
        "models": MODELS,
        "rolling_history": 24,
        "pseudocount_per_cell": 1,
        "draw": "sha256_ascii_seed:path:index_first_byte_mod8",
        "oracle": "privileged_future_law_not_realization",
        "score_fields": FIELDS,
        "event": "both_displacements_strictly_positive",
        "inference_policy": "always_abstain",
        "temporal_structure": "independent_joint_increments",
    }
    return {
        "design": design,
        "study_sha256": _sha(design),
        "status": "prepared_not_executed",
        "registration_verified": False,
        "runtime_code_attested": False,
        "forecast_eligible": False,
        "action_authorized": False,
    }


def _weights(scenario: str, index: int) -> tuple[int, ...]:
    if scenario == "positive" or (scenario == "shift" and index < 53):
        return POS
    if scenario == "negative" or scenario == "shift":
        return NEG
    if scenario == "independent":
        return IND
    raise ValueError("unknown scenario")


def _law(weights: tuple[int, ...]) -> JointPMF:
    return canonical_joint_pmf(tuple((x, y, w) for (x, y), w in zip(CELLS, weights, strict=True)))


def _path(scenario: str, seed: int, path: int) -> tuple[tuple[int, int], ...]:
    result = [(0, 0)]
    for i in range(1, 64):
        weights = _weights(scenario, i)
        draw = hashlib.sha256(f"{seed}:{path}:{i}".encode("ascii")).digest()[0] % 8
        for cell, w in zip(CELLS, weights, strict=True):
            draw -= w * (8 // sum(weights))
            if draw < 0:
                result.append(cell)
                break
        else:
            raise ValueError("draw outside support")
    return tuple(result)


def _candidates(history: tuple[tuple[int, int], ...], h: int) -> dict[str, JointPMF]:
    if (
        type(history) is not tuple
        or len(history) != 24
        or any(
            type(cell) is not tuple or cell not in CELLS or any(type(x) is not int for x in cell)
            for cell in history
        )
        or type(h) is not int
        or h not in HORIZONS
    ):
        raise ValueError("bounded historical pairs and horizon required")
    counts = Counter(history)
    joint = _law(tuple(counts[cell] + 1 for cell in CELLS))
    product = independent_joint_projection(joint)
    return {
        "fixed_independent": convolve_joint_increments((_law(IND),) * h),
        "product24": convolve_joint_increments((product,) * h),
        "joint24": convolve_joint_increments((joint,) * h),
    }


def _reference(scenario: str, origin: int, h: int) -> JointPMF:
    return convolve_joint_increments(
        tuple(_law(_weights(scenario, i)) for i in range(origin + 1, origin + h + 1))
    )


def _scores(p: JointPMF, q: JointPMF, y: tuple[int, int]) -> tuple[Fraction, ...]:
    e = joint_positive_probability(p)
    actual = Fraction(y[0] > 0 and y[1] > 0)
    return (
        joint_brier_score(p, y),
        reference_joint_brier_excess(p, q),
        score_discrete_pmf(joint_marginal(p, 0), y[0]).crps,
        score_discrete_pmf(joint_marginal(p, 1), y[1]).crps,
        (e - actual) ** 2,
        e,
        actual,
        joint_covariance(p),
    )


def _group(scenario: str, seed: int) -> dict[str, object]:
    transcript = hashlib.sha256()
    totals = {(h, m): [Fraction() for _ in FIELDS] for h in HORIZONS for m in MODELS}
    candidates = lru_cache(maxsize=1024)(_candidates)
    references = {(t, h): _reference(scenario, t, h) for t in ORIGINS for h in HORIZONS}
    for k in range(PATHS):
        increments = _path(scenario, seed, k)
        for t in ORIGINS:
            for h in HORIZONS:
                ps = dict(candidates(increments[t - 23 : t + 1], h))
                q = references[t, h]
                ps["oracle"] = q
                y = (
                    sum(x for x, _ in increments[t + 1 : t + h + 1]),
                    sum(y for _, y in increments[t + 1 : t + h + 1]),
                )
                for model in MODELS:
                    p = ps[model]
                    values = _scores(p, q, y)
                    transcript.update(
                        canonical([k, t, h, model, p, y, [str(v) for v in values]]) + b"\n"
                    )
                    for i, v in enumerate(values):
                        totals[h, model][i] += v
    n = PATHS * len(ORIGINS)
    return {
        "scenario": scenario,
        "seed": seed,
        "paths": PATHS,
        "event_transcript_sha256": transcript.hexdigest(),
        "rows": [
            {
                "horizon": h,
                "model": m,
                "pairs": n,
                **{key: str(v / n) for key, v in zip(FIELDS, totals[h, m], strict=True)},
            }
            for h in HORIZONS
            for m in MODELS
        ],
    }


def execute_study(revision: str, expected: str) -> dict[str, object]:
    prepared = prepare_study(revision)
    identity = prepared["study_sha256"]
    if (
        not isinstance(identity, str)
        or type(expected) is not str
        or not re.fullmatch("[0-9a-f]{64}", expected)
        or not hmac.compare_digest(identity, expected)
    ):
        raise ValueError("bivariate study commitment mismatch")
    result: dict[str, object] = {
        "protocol": PROTOCOL,
        "study_sha256": identity,
        "design": prepared["design"],
        "groups": [_group(s, seed) for s, seed in SCENARIOS],
        "synthetic_only": True,
        "holdout_executed": False,
        "holdout_lock_verified": False,
        "registration_verified": False,
        "runtime_code_attested": False,
        "calibration_verified": False,
        "winner": None,
        "confidence_interval": None,
        "inference_status": "abstained",
        "forecast_eligible": False,
        "ingestion_authorized": False,
        "action_authorized": False,
    }
    result["report_sha256"] = _sha(result)
    return result


def verify_study(revision: str, expected: str, submitted: bytes) -> str:
    if type(submitted) is not bytes or not 1 <= len(submitted) <= MAX_RECEIPT_BYTES:
        raise ValueError("bounded canonical bivariate receipt required")
    report = execute_study(revision, expected)
    actual = canonical(report)
    if len(actual) > MAX_RECEIPT_BYTES or not hmac.compare_digest(actual, submitted):
        raise ValueError("bivariate receipt differs from local replay")
    digest = report["report_sha256"]
    if not isinstance(digest, str):
        raise TypeError("invalid report digest")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description="Fixed fictional bivariate study")
    parser.add_argument("mode", choices=("prepare", "demo", "run"))
    parser.add_argument("--revision", required=True)
    parser.add_argument("--expected")
    args = parser.parse_args()
    try:
        if (args.mode == "run") != (args.expected is not None):
            raise ValueError("run requires caller-retained commitment")
        prepared = prepare_study(args.revision)
        result = prepared
        if args.mode != "prepare":
            expected = args.expected if args.mode == "run" else prepared["study_sha256"]
            if not isinstance(expected, str):
                raise TypeError("invalid commitment")
            result = execute_study(args.revision, expected)
            verify_study(args.revision, expected, canonical(result))
        print(canonical(result).decode("ascii"))
    except (ValueError, TypeError):
        parser.exit(2, "Fictional bivariate study failed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
