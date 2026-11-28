"""Versioned fixed fictional paired-state temporal study."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import re
from fractions import Fraction
from functools import lru_cache

from examples.m1_census_bivariate_study import FIELDS, _scores
from examples.m1_census_probability_study import canonical
from mirrormind.domains.retail.census_bivariate import JointPMF
from mirrormind.domains.retail.census_joint_markov import (
    STATES,
    State,
    TransitionMatrix,
    TransitionRow,
    propagate_joint_markov,
)
from mirrormind.domains.retail.census_temporal_models import (
    TEMPORAL_MODELS,
    predict_temporal_models,
)

PROTOCOL = "mirrormind.census.fictional_temporal_study.v1"
SCENARIOS = (("independent", 131001), ("own", 131002), ("cross", 131003), ("switch", 131004))
MODELS = (*TEMPORAL_MODELS, "oracle")
HORIZONS = (1, 3, 6)
ORIGINS = tuple(range(48, 58))
PATHS = 16
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
        "states": STATES,
        "months": 64,
        "origins": ORIGINS,
        "horizons": HORIZONS,
        "models": MODELS,
        "rolling_history": 24,
        "pseudocount_per_outcome": 1,
        "switch_index": 53,
        "switch_from": "cross",
        "switch_to": "own",
        "draw": "sha256_ascii_seed:path:index:axis_first_byte_mod4",
        "initial": "independent_symmetric_signs",
        "copy_probability": "3/4",
        "independent_probability": "1/2",
        "update": "simultaneous_from_previous_pair",
        "target": "sum_future_states_excluding_start",
        "oracle": "privileged_future_transition_schedule_not_realization",
        "score_fields": FIELDS,
        "inference_policy": "always_abstain",
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


def _mechanism(scenario: str, index: int) -> str:
    if scenario == "switch":
        return "cross" if index < 53 else "own"
    if scenario in ("independent", "own", "cross"):
        return scenario
    raise ValueError("unknown scenario")


def _row(scenario: str, index: int, prev: State) -> TransitionRow:
    mode = _mechanism(scenario, index)
    if mode == "independent":
        return (1, 1, 1, 1)
    source = prev if mode == "own" else prev[::-1]
    a, b, c, d = ((3 if x == source[0] else 1) * (3 if y == source[1] else 1) for x, y in STATES)
    return a, b, c, d


def _matrix(scenario: str, index: int) -> TransitionMatrix:
    a, b, c, d = (_row(scenario, index, prev) for prev in STATES)
    return a, b, c, d


def _path(scenario: str, seed: int, path: int) -> tuple[State, ...]:
    def draw(t: int, axis: int) -> int:
        return hashlib.sha256(f"{seed}:{path}:{t}:{axis}".encode("ascii")).digest()[0] % 4

    out: list[State] = [(4 if draw(0, 0) < 2 else -4, 4 if draw(0, 1) < 2 else -4)]
    for t in range(1, 64):
        mode = _mechanism(scenario, t)
        if mode == "independent":
            out.append((4 if draw(t, 0) < 2 else -4, 4 if draw(t, 1) < 2 else -4))
        else:
            source = out[-1] if mode == "own" else out[-1][::-1]
            out.append(
                (
                    source[0] if draw(t, 0) < 3 else -source[0],
                    source[1] if draw(t, 1) < 3 else -source[1],
                )
            )
    return tuple(out)


def _reference(scenario: str, origin: int, h: int, start: State) -> JointPMF:
    return propagate_joint_markov(
        start, tuple(_matrix(scenario, t) for t in range(origin + 1, origin + h + 1))
    )


def _group(scenario: str, seed: int) -> dict[str, object]:
    transcript = hashlib.sha256()
    totals = {(h, m): [Fraction() for _ in FIELDS] for h in HORIZONS for m in MODELS}
    # Caches are local to private fixed fixture evaluation, never public inputs.
    candidates = lru_cache(maxsize=1024)(predict_temporal_models)
    reference = lru_cache(maxsize=128)(_reference)
    for k in range(PATHS):
        states = _path(scenario, seed, k)
        for t in ORIGINS:
            for h in HORIZONS:
                ps = dict(candidates(states[t - 23 : t + 1], h))
                q = reference(scenario, t, h, states[t])
                ps["oracle"] = q
                y = (
                    sum(x for x, _ in states[t + 1 : t + h + 1]),
                    sum(y for _, y in states[t + 1 : t + h + 1]),
                )
                for m in MODELS:
                    p = ps[m]
                    values = _scores(p, q, y)
                    transcript.update(
                        canonical([k, t, h, m, p, y, [str(v) for v in values]]) + b"\n"
                    )
                    for i, v in enumerate(values):
                        totals[h, m][i] += v
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
        raise ValueError("temporal study commitment mismatch")
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
        "causal_effect_established": False,
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
        raise ValueError("bounded canonical temporal receipt required")
    report = execute_study(revision, expected)
    actual = canonical(report)
    if len(actual) > MAX_RECEIPT_BYTES or not hmac.compare_digest(actual, submitted):
        raise ValueError("temporal receipt differs from local replay")
    digest = report["report_sha256"]
    if not isinstance(digest, str):
        raise TypeError("invalid report digest")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description="Fixed fictional temporal study")
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
        parser.exit(2, "Fictional temporal study failed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
