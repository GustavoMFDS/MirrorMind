"""Fixed fictional persistent Bayesian network study with local replay."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import re
from collections import defaultdict
from fractions import Fraction
from math import prod

from examples.m1_census_probability_study import canonical
from mirrormind.domains.retail.census_network3 import (
    PMF3,
    STATES,
    Matrix3,
    State3,
    propagate_network3,
)
from mirrormind.domains.retail.census_network_bayes import predict_persistent_bayes
from mirrormind.domains.retail.census_network_structure import (
    fit_parent_matrix,
    select_parent_graphs,
)

PROTOCOL = "mirrormind.census.fictional_persistent_bayes.v1"
SCENARIOS = (("independent", 161001), ("own", 161002), ("ring", 161003), ("switch", 161004))
MODELS = ("integrated", "frozen", "map", "oracle")
HORIZONS = (1, 2, 3)
ORIGINS = (48, 52, 56)
WINDOWS = (8, 24)
PATHS = 4
FIELDS = (
    "joint_brier",
    "reference_excess",
    "event_brier",
    "predicted_event",
    "observed_event",
    "mean_marginal_crps",
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
        "states": STATES,
        "months": 64,
        "origins": ORIGINS,
        "windows": WINDOWS,
        "horizons": HORIZONS,
        "models": MODELS,
        "switch_index": 53,
        "switch_from": "ring",
        "switch_to": "own",
        "ring_parents": (2, 0, 1),
        "copy_probability": "3/4",
        "independent_probability": "1/2",
        "initial": "independent_symmetric_signs",
        "draw": "sha256_ascii_seed:path:index:axis_first_byte_mod4",
        "parent_prior": "uniform_none_0_1_2_per_child",
        "parameter_prior": "independent_beta_1_1_per_context",
        "integrated": "persistent_graph_and_parameters_hypothetical_path_updates",
        "frozen": "issuance_time_posterior_mean_conditional_law",
        "map": "fixed_MAP_graph_smoothed_conditional_law",
        "oracle": "privileged_future_transition_schedule_not_realization",
        "target": "sum_future_states_excluding_start",
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


def _parents(scenario: str, t: int) -> State3 | None:
    if scenario == "switch":
        scenario = "ring" if t < 53 else "own"
    if scenario == "independent":
        return None
    if scenario == "own":
        return (0, 1, 2)
    if scenario == "ring":
        return (2, 0, 1)
    raise ValueError("unknown scenario")


def _matrix(scenario: str, t: int) -> Matrix3:
    p = _parents(scenario, t)
    return tuple(
        tuple(
            1 if p is None else prod(3 if nxt[a] == prev[p[a]] else 1 for a in range(3))
            for nxt in STATES
        )
        for prev in STATES
    )


def _path(scenario: str, seed: int, k: int) -> tuple[State3, ...]:
    def draw(t: int, a: int) -> int:
        return hashlib.sha256(f"{seed}:{k}:{t}:{a}".encode("ascii")).digest()[0] % 4

    out: list[State3] = [
        (1 if draw(0, 0) < 2 else -1, 1 if draw(0, 1) < 2 else -1, 1 if draw(0, 2) < 2 else -1)
    ]
    for t in range(1, 64):
        p = _parents(scenario, t)
        prev = out[-1]
        a, b, c = (
            (1 if draw(t, i) < 2 else -1)
            if p is None
            else (prev[p[i]] if draw(t, i) < 3 else -prev[p[i]])
            for i in range(3)
        )
        out.append((a, b, c))
    return tuple(out)


def _prob(pmf: PMF3) -> dict[State3, Fraction]:
    total = sum(w for _, w in pmf)
    return {s: Fraction(w, total) for s, w in pmf}


def _scores(p: PMF3, q: PMF3, y: State3) -> tuple[Fraction, ...]:
    a, b = _prob(p), _prob(q)
    joint = 1 + sum((w * w for w in a.values()), Fraction()) - 2 * a.get(y, Fraction())
    excess = sum(
        ((a.get(k, Fraction()) - b.get(k, Fraction())) ** 2 for k in a.keys() | b.keys()),
        Fraction(),
    )
    event = sum((w for k, w in a.items() if all(x > 0 for x in k)), Fraction())
    observed = Fraction(all(x > 0 for x in y))
    crps = Fraction()
    for i in range(3):
        marginal: dict[int, Fraction] = defaultdict(Fraction)
        for k, w in a.items():
            marginal[k[i]] += w
        crps += sum((w * abs(x - y[i]) for x, w in marginal.items()), Fraction())
        crps -= sum(
            (u * v * abs(x - z) / 2 for x, u in marginal.items() for z, v in marginal.items()),
            Fraction(),
        )
    return joint, excess, (event - observed) ** 2, event, observed, crps / 3


def _group(scenario: str, seed: int) -> dict[str, object]:
    sums = {
        (length, h, m): [Fraction() for _ in FIELDS]
        for length in WINDOWS
        for h in HORIZONS
        for m in MODELS
    }
    audit = hashlib.sha256()
    for k in range(PATHS):
        states = _path(scenario, seed, k)
        for t in ORIGINS:
            for length in WINDOWS:
                history = states[t - length + 1 : t + 1]
                graph, _ = select_parent_graphs(history)
                matrix = fit_parent_matrix(history, graph)
                for h in HORIZONS:
                    q = propagate_network3(
                        states[t], tuple(_matrix(scenario, i) for i in range(t + 1, t + h + 1))
                    )
                    x, y, z = (sum(v[a] for v in states[t + 1 : t + h + 1]) for a in range(3))
                    actual = (x, y, z)
                    ps = {
                        "integrated": predict_persistent_bayes(history, h),
                        "frozen": predict_persistent_bayes(history, h, frozen=True),
                        "map": propagate_network3(states[t], (matrix,) * h),
                        "oracle": q,
                    }
                    if h == 1 and ps["integrated"] != ps["frozen"]:
                        raise ValueError("one-step identity mismatch")
                    for m in MODELS:
                        p = ps[m]
                        vals = _scores(p, q, actual)
                        audit.update(
                            canonical([k, t, length, h, m, p, actual, [str(v) for v in vals]])
                            + b"\n"
                        )
                        for i, v in enumerate(vals):
                            sums[length, h, m][i] += v
    n = PATHS * len(ORIGINS)
    return {
        "scenario": scenario,
        "seed": seed,
        "paths": PATHS,
        "event_transcript_sha256": audit.hexdigest(),
        "rows": [
            {
                "history": length,
                "horizon": h,
                "model": m,
                "pairs": n,
                **{key: str(v / n) for key, v in zip(FIELDS, sums[length, h, m], strict=True)},
            }
            for length in WINDOWS
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
        raise ValueError("persistent study commitment mismatch")
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
        raise ValueError("bounded canonical receipt required")
    result = execute_study(revision, expected)
    actual = canonical(result)
    if len(actual) > MAX_RECEIPT_BYTES or not hmac.compare_digest(actual, submitted):
        raise ValueError("persistent receipt differs from local replay")
    digest = result["report_sha256"]
    if not isinstance(digest, str):
        raise TypeError("invalid report digest")
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description="Fixed fictional persistent Bayesian study")
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
        parser.exit(2, "Fictional persistent study failed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
