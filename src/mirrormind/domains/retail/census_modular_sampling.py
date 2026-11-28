"""Bounded persistent posterior sampling and finite-look event precision."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, lcm
from random import Random

from mirrormind.domains.retail.census_modular import (
    PMF,
    History,
    Modules,
    Ports,
    Scope,
    State,
    _prepare,
    _validate,
)

LOOKS = (512, 2048, 8192)
GRID = 10000
MAX_SAMPLES = 8192
MAX_HORIZON = 12
Candidate = tuple[State, tuple[tuple[int, int], ...]]
Compiled = tuple[tuple[tuple[int, ...], tuple[Candidate, ...]], ...]


@dataclass(frozen=True, slots=True)
class EventLook:
    samples: int
    radius: Fraction
    exponent: int
    estimates: tuple[Fraction, ...]
    intervals: tuple[tuple[Fraction, Fraction], ...]


@dataclass(frozen=True, slots=True)
class EventPrecision:
    status: str
    axes: State
    horizon: int
    events: tuple[State, ...]
    seed: int
    balanced: bool
    tolerance: Fraction
    alpha: Fraction
    attempts: tuple[EventLook, ...]
    scope: str = "conditional_model_event_sampling_only"
    forecast_eligible: bool = False
    action_authorized: bool = False


def _request(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    samples: int,
    seed: int,
    balanced: bool,
) -> Scope:
    scope, _ = _validate(history, modules, ports, axes, 1, balanced)
    if type(horizon) is not int or not 1 <= horizon <= MAX_HORIZON:
        raise ValueError("bounded horizon required")
    if type(samples) is not int or not 128 <= samples <= MAX_SAMPLES:
        raise ValueError("bounded sample count required")
    if type(seed) is not int or not 0 <= seed < 2**32:
        raise ValueError("bounded explicit seed required")
    return scope


def _compile(history: History, scope: Scope, balanced: bool) -> Compiled:
    rows = _prepare(history, scope, tuple(range(len(scope))), balanced)
    compiled = []
    for a in range(len(scope)):
        local = rows[a]
        den = lcm(*(weight.denominator for _, _, weight in local))
        weights = tuple(weight.numerator * (den // weight.denominator) for _, _, weight in local)
        divisor = gcd(*weights)
        cumulative = []
        total = 0
        for w in weights:
            total += w // divisor
            cumulative.append(total)
        candidates = tuple(
            (
                parents,
                tuple(
                    (c[ctx, -1] + 1, c[ctx, 1] + 1) for ctx in product((-1, 1), repeat=len(parents))
                ),
            )
            for parents, c, _ in local
        )
        compiled.append((tuple(cumulative), candidates))
    return tuple(compiled)


def _trajectories(
    start: State, rows: Compiled, axes: State, horizon: int, samples: int, seed: int
) -> Iterator[State]:
    rng = Random(seed)
    d = len(start)
    for _ in range(samples):
        graph = []
        urns = []
        for cumulative, candidates in rows:
            draw = rng.randrange(cumulative[-1])
            idx = next(i for i, w in enumerate(cumulative) if draw < w)
            parents, counts = candidates[idx]
            graph.append(parents)
            urns.append([list(v) for v in counts])
        prev = start
        totals = [0] * d
        for _ in range(horizon):
            nxt = []
            for a, parents in enumerate(graph):
                ctx = 0
                for p in parents:
                    ctx = ctx * 2 + int(prev[p] == 1)
                row = urns[a][ctx]
                bit = int(rng.randrange(sum(row)) >= row[0])
                row[bit] += 1
                nxt.append(2 * bit - 1)
            for a, v in enumerate(nxt):
                totals[a] += v
            prev = tuple(nxt)
        yield tuple(totals[a] for a in axes)


def sample_modular(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    *,
    samples: int,
    seed: int,
    balanced: bool = False,
) -> PMF:
    """Empirical subset PMF from persistent graph and Beta-Bernoulli paths.

    Deterministic pseudorandom replay is not exact integration or an
    empirical forecast guarantee. No automatic fallback from exact query.
    """
    scope = _request(history, modules, ports, axes, horizon, samples, seed, balanced)
    counts = Counter(
        _trajectories(history[-1], _compile(history, scope, balanced), axes, horizon, samples, seed)
    )
    if sum(counts.values()) != samples:
        raise ValueError("sample mass mismatch")
    return tuple((k, Fraction(v, samples)) for k, v in sorted(counts.items()))


def event_radius(n: int, m: int, alpha: Fraction) -> tuple[Fraction, int]:
    """Conservative rational Hoeffding/union bound for three fixed looks."""
    if (
        type(n) is not int
        or n not in LOOKS
        or type(m) is not int
        or not 1 <= m <= 4
        or type(alpha) is not Fraction
        or not Fraction(1, 100) <= alpha <= Fraction(1, 10)
    ):
        raise ValueError("invalid bound parameters")
    k = 0
    while Fraction(2 * m * len(LOOKS), 2**k) > alpha:
        k += 1
    target = k * GRID * GRID
    den = 2 * n
    units = isqrt(target // den)
    if units * units * den < target:
        units += 1
    return Fraction(units, GRID), k


def estimate_modular_events(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    events: tuple[State, ...],
    *,
    tolerance: Fraction,
    alpha: Fraction,
    seed: int,
    balanced: bool = False,
) -> EventPrecision:
    """Stream nested samples and stop at a predetermined precision look.

    All thresholds, confidence and tolerance are supplied before drawing.
    Bounds assume ideal iid posterior paths, not PRNG certification or
    calibrated real-world predictions. Abstention is explicit.
    """
    scope = _request(history, modules, ports, axes, horizon, MAX_SAMPLES, seed, balanced)
    if (
        type(events) is not tuple
        or not 1 <= len(events) <= 4
        or any(
            type(e) is not tuple
            or len(e) != len(axes)
            or any(type(t) is not int or not -horizon <= t <= horizon for t in e)
            for e in events
        )
        or len(set(events)) != len(events)
    ):
        raise ValueError("distinct bounded events required")
    if type(tolerance) is not Fraction or not Fraction(1, 100) <= tolerance <= Fraction(1, 10):
        raise ValueError("bounded rational tolerance required")
    radii = tuple(event_radius(n, len(events), alpha) for n in LOOKS)
    counts = [0] * len(events)
    attempts: list[EventLook] = []
    for n, state in enumerate(
        _trajectories(
            history[-1], _compile(history, scope, balanced), axes, horizon, MAX_SAMPLES, seed
        ),
        1,
    ):
        for i, e in enumerate(events):
            counts[i] += int(all(x >= t for x, t in zip(state, e, strict=True)))
        if n in LOOKS:
            r, k = radii[len(attempts)]
            estimates = tuple(Fraction(v, n) for v in counts)
            intervals = tuple((max(Fraction(), v - r), min(Fraction(1), v + r)) for v in estimates)
            attempts.append(EventLook(n, r, k, estimates, intervals))
            if r <= tolerance:
                break
    if not attempts:
        raise ValueError("no sampling checkpoint")
    return EventPrecision(
        "precision_met" if attempts[-1].radius <= tolerance else "abstained",
        axes,
        horizon,
        events,
        seed,
        balanced,
        tolerance,
        alpha,
        tuple(attempts),
    )
