"""Versioned local fictional probability study, with no external inputs."""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import re
from collections import Counter
from fractions import Fraction
from functools import lru_cache

from mirrormind.domains.retail.census_probability import (
    PMF,
    canonical_pmf,
    convolve_increments,
    reference_interval_coverage,
    score_discrete_pmf,
)

PROTOCOL = "mirrormind.census.fictional_probability_study.v1"
SCENARIOS = (("stationary", 61001), ("variance_shift", 61002))
MODELS = ("point", "narrow", "fixed", "rolling24", "oracle")
HORIZONS = (1, 3, 6)
ORIGINS = tuple(range(48, 58))
PATHS = 32
FIELDS = ("crps", "pinball", "median_mae", "coverage", "width", "reference_coverage")
MAX_RECEIPT_BYTES = 1024 * 1024


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def _sha(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def prepare_study(revision: str) -> dict[str, object]:
    if type(revision) is not str or not re.fullmatch("[0-9a-f]{40}", revision):
        raise ValueError("declared Git SHA-1 required")
    design: dict[str, object] = {
        "protocol": PROTOCOL, "declared_code_revision": revision,
        "scenario_seeds": SCENARIOS, "paths_per_scenario": PATHS,
        "months": 64, "origins": ORIGINS, "horizons": HORIZONS, "models": MODELS,
        "draw": "sha256_ascii_seed:path:index_first_byte_mod4",
        "increment_signs": (-1, 0, 0, 1), "amplitude": 4,
        "shift_index": 53, "shift_amplitude": 12, "narrow_amplitude": 2,
        "rolling_history": 24, "oracle": "privileged_future_law_not_realization",
        "quantiles": ("1/10", "1/2", "9/10"), "score_fields": FIELDS,
        "inference_policy": "always_abstain",
    }
    return {
        "design": design, "study_sha256": _sha(design),
        "status": "prepared_not_executed", "registration_verified": False,
        "runtime_code_attested": False, "holdout_lock_verified": False,
        "forecast_eligible": False, "action_authorized": False,
    }


def _amplitude(scenario: str, index: int) -> int:
    return 12 if scenario == "variance_shift" and index >= 53 else 4


def _law(amplitude: int) -> PMF:
    return ((-amplitude, 1), (0, 2), (amplitude, 1))


def _path(scenario: str, seed: int, path: int) -> tuple[int, ...]:
    return (0,) + tuple(
        _amplitude(scenario, i) * (-1, 0, 0, 1)[
            hashlib.sha256(f"{seed}:{path}:{i}".encode("ascii")).digest()[0] % 4
        ] for i in range(1, 64)
    )


def _candidates(history: tuple[int, ...], horizon: int) -> dict[str, PMF]:
    # Only the observed 24 increments are supplied, never the generator law.
    empirical = canonical_pmf(tuple(sorted(Counter(history).items())))
    return {
        "point": ((0, 1),),
        "narrow": convolve_increments((_law(2),) * horizon),
        "fixed": convolve_increments((_law(4),) * horizon),
        "rolling24": convolve_increments((empirical,) * horizon),
    }


def _group(scenario: str, seed: int) -> dict[str, object]:
    transcript = hashlib.sha256()
    totals = {(h, m): [Fraction() for _ in FIELDS] for h in HORIZONS for m in MODELS}
    # Cache belongs to this run only and is bounded.
    candidates = lru_cache(maxsize=2048)(_candidates)
    truth = {
        (origin, h): convolve_increments(tuple(
            _law(_amplitude(scenario, i)) for i in range(origin + 1, origin + h + 1)
        )) for origin in ORIGINS for h in HORIZONS
    }
    for path in range(PATHS):
        increments = _path(scenario, seed, path)
        for origin in ORIGINS:
            history = increments[origin - 23:origin + 1]
            for h in HORIZONS:
                pmfs = dict(candidates(history, h))
                reference = truth[origin, h]
                pmfs["oracle"] = reference
                observed = sum(increments[origin + 1:origin + h + 1])
                for model in MODELS:
                    pmf = pmfs[model]
                    scores = score_discrete_pmf(pmf, observed)
                    values = (
                        scores.crps, scores.mean_pinball, Fraction(scores.median_absolute_error),
                        Fraction(scores.covered), Fraction(scores.width),
                        reference_interval_coverage(pmf, reference),
                    )
                    transcript.update(canonical([
                        path, origin, h, model, pmf, observed, [str(v) for v in values]
                    ]) + b"\n")
                    for index, value in enumerate(values):
                        totals[h, model][index] += value
    count = PATHS * len(ORIGINS)
    return {
        "scenario": scenario, "seed": seed, "paths": PATHS,
        "event_transcript_sha256": transcript.hexdigest(),
        "rows": [
            {"horizon": h, "model": m, "pairs": count,
             **{k: str(v / count) for k, v in zip(FIELDS, totals[h, m], strict=True)}}
            for h in HORIZONS for m in MODELS
        ],
    }


def execute_study(revision: str, expected: str) -> dict[str, object]:
    prepared = prepare_study(revision)
    identity = prepared["study_sha256"]
    if (
        not isinstance(identity, str) or type(expected) is not str
        or not re.fullmatch("[0-9a-f]{64}", expected) or not hmac.compare_digest(identity, expected)
    ):
        raise ValueError("probability study commitment mismatch")
    result: dict[str, object] = {
        "protocol": PROTOCOL, "study_sha256": identity, "design": prepared["design"],
        "groups": [_group(s, seed) for s, seed in SCENARIOS],
        "synthetic_only": True, "holdout_executed": False, "holdout_lock_verified": False,
        "registration_verified": False, "runtime_code_attested": False,
        "calibration_verified": False, "winner": None, "confidence_interval": None,
        "inference_status": "abstained", "forecast_eligible": False,
        "ingestion_authorized": False, "action_authorized": False,
    }
    result["report_sha256"] = _sha(result)
    return result


def verify_study(revision: str, expected: str, submitted: bytes) -> str:
    if type(submitted) is not bytes or not 1 <= len(submitted) <= MAX_RECEIPT_BYTES:
        raise ValueError("bounded canonical probability receipt required")
    report = execute_study(revision, expected)
    actual = canonical(report)
    if len(actual) > MAX_RECEIPT_BYTES or not hmac.compare_digest(actual, submitted):
        raise ValueError("probability receipt differs from local replay")
    digest = report["report_sha256"]
    if not isinstance(digest, str):
        raise TypeError("invalid report digest")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description="Fixed fictional probability study")
    parser.add_argument("mode", choices=("prepare", "demo", "run"))
    parser.add_argument("--revision", required=True)
    parser.add_argument("--expected")
    args = parser.parse_args()
    try:
        if (args.mode == "run") != (args.expected is not None):
            raise ValueError("run requires caller-retained commitment")
        prepared = prepare_study(args.revision)
        if args.mode == "prepare":
            result = prepared
        else:
            expected = args.expected if args.mode == "run" else prepared["study_sha256"]
            if not isinstance(expected, str):
                raise TypeError("invalid commitment")
            result = execute_study(args.revision, expected)
            verify_study(args.revision, expected, canonical(result))
        print(canonical(result).decode("ascii"))
    except (ValueError, TypeError):
        parser.exit(2, "Fictional probability study failed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
