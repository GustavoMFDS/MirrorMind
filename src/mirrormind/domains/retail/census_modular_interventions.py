"""Bounded model-implied mechanism replacements, exact and paired."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt, lcm
from random import Random

from mirrormind.domains.retail.census_modular import (
    PMF,
    History,
    Modules,
    Ports,
    State,
    _law,
    _positive,
    _prepare,
    _validate,
)
from mirrormind.domains.retail.census_modular_sampling import (
    Compiled,
    _compile,
    _request,
)

Schedule = tuple[tuple[int, int, int], ...]
Urns = list[list[list[int]]]


def _schedule(value: Schedule, d: int, horizon: int) -> dict[tuple[int, int], int]:
    if type(value) is not tuple or len(value) > d * horizon:
        raise ValueError("bounded intervention schedule required")
    out = {}
    for item in value:
        if type(item) is not tuple or len(item) != 3 or any(type(x) is not int for x in item):
            raise ValueError("integer intervention triple required")
        t, a, v = item
        if not 1 <= t <= horizon or not 0 <= a < d or v not in (-1, 1) or (t, a) in out:
            raise ValueError("invalid or duplicate intervention")
        out[t, a] = v
    return out


def intervene_modular(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    interventions: Schedule = (),
    *,
    balanced: bool = False,
) -> tuple[PMF, State]:
    """Exact conditional-model intervention PMF, not identified causal effects.

    Forced outcomes replace the mechanism and never update its likelihood.
    Unforced outcomes update branch-local posterior evidence. The closure
    is conservatively retained even when some mechanisms are forced.
    """
    scope, closure = _validate(history, modules, ports, axes, horizon, balanced)
    forced = _schedule(interventions, len(history[0]), horizon)
    rows = _prepare(history, scope, closure, balanced)
    prev = history[-1]

    def positive(t: int, a: int, state: State | dict[int, int]) -> Fraction:
        if (t, a) in forced:
            return Fraction(forced[t, a] == 1)
        if t == 1 or (1, a) in forced:
            return _positive(rows[a], state)
        return _positive(rows[a], state, observed_prev=prev, child=a)

    initial = _law(tuple(positive(1, a, prev) for a in closure))
    if horizon == 1:
        return tuple((key, w) for key, w in initial if w), closure
    mass: dict[State, Fraction] = defaultdict(Fraction)
    for values, w in initial:
        if not w:
            continue
        first = dict(zip(closure, values, strict=True))
        for nxt, v in _law(tuple(positive(2, a, first) for a in axes)):
            if v:
                mass[tuple(first[a] + x for a, x in zip(axes, nxt, strict=True))] += w * v
    if sum(mass.values()) != 1:
        raise ValueError("mass mismatch")
    return tuple(sorted(mass.items())), closure


def _draw(rows: Compiled, rng: Random) -> tuple[tuple[State, ...], Urns]:
    graph = []
    urns = []
    for cumulative, candidates in rows:
        draw = rng.randrange(cumulative[-1])
        idx = next(i for i, w in enumerate(cumulative) if draw < w)
        parents, counts = candidates[idx]
        graph.append(parents)
        urns.append([list(v) for v in counts])
    return tuple(graph), urns


def _context(prev: State, parents: State) -> int:
    ctx = 0
    for p in parents:
        ctx = ctx * 2 + int(prev[p] == 1)
    return ctx


def contrast_radius(n: int, alpha: Fraction) -> tuple[Fraction, int]:
    """Single fixed-look conservative Hoeffding radius on [-1,1]."""
    if (
        type(n) is not int
        or not 128 <= n <= 8192
        or type(alpha) is not Fraction
        or not Fraction(1, 100) <= alpha <= Fraction(1, 10)
    ):
        raise ValueError("invalid bound parameters")
    k = 0
    while Fraction(2, 2**k) > alpha:
        k += 1
    grid = 10000
    target = 2 * k * grid * grid
    units = isqrt(target // n)
    if units * units * n < target:
        units += 1
    return Fraction(units, grid), k


@dataclass(frozen=True, slots=True)
class InterventionContrast:
    axes: State
    horizon: int
    event: State
    schedule_a: Schedule
    schedule_b: Schedule
    samples: int
    seed: int
    coupled: bool
    balanced: bool
    counts: tuple[tuple[int, int, int], ...]
    p_a: Fraction
    p_b: Fraction
    contrast: Fraction
    sample_variance: Fraction
    radius: Fraction
    exponent: int
    interval: tuple[Fraction, Fraction]
    alpha: Fraction
    scope: str = "conditional_model_event_contrast_only"
    forecast_eligible: bool = False
    action_authorized: bool = False


def compare_modular_interventions(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    event: State,
    schedule_a: Schedule,
    schedule_b: Schedule,
    *,
    samples: int,
    seed: int,
    coupled: bool = True,
    balanced: bool = False,
    alpha: Fraction = Fraction(1, 20),
) -> InterventionContrast:
    """Estimate P(event|B)-P(event|A) with optional shared random draws.

    Coupling preserves each marginal path law; it is a computational
    choice, not an identified cross-world or individual counterfactual.
    The bound assumes ideal iid pairs and a single predeclared query.
    """
    scope = _request(history, modules, ports, axes, horizon, samples, seed, balanced)
    d = len(scope)
    if type(coupled) is not bool:
        raise ValueError("boolean coupling required")
    if (
        type(event) is not tuple
        or len(event) != len(axes)
        or any(type(v) is not int or not -horizon <= v <= horizon for v in event)
    ):
        raise ValueError("invalid event")
    radius, k = contrast_radius(samples, alpha)
    forced = (_schedule(schedule_a, d, horizon), _schedule(schedule_b, d, horizon))
    rows = _compile(history, scope, balanced)
    rng = Random(seed)
    counts: Counter[tuple[int, ...]] = Counter()
    for _ in range(samples):
        ga, ua = _draw(rows, rng)
        if coupled:
            gb = ga
            ub = [[row.copy() for row in child] for child in ua]
        else:
            gb, ub = _draw(rows, rng)
        prev = [history[-1], history[-1]]
        totals = [[0] * d, [0] * d]
        graphs = (ga, gb)
        urns = (ua, ub)
        for t in range(1, horizon + 1):
            nxt: list[list[int]] = [[], []]
            for a in range(d):
                local = [urns[j][a][_context(prev[j], graphs[j][a])] for j in (0, 1)]
                den = [sum(row) for row in local]
                if coupled:
                    common = lcm(*den)
                    u = rng.randrange(common)
                    bits = [
                        int(u >= row[0] * (common // n)) for row, n in zip(local, den, strict=True)
                    ]
                else:
                    bits = [
                        int(rng.randrange(n) >= row[0]) for row, n in zip(local, den, strict=True)
                    ]
                for j in (0, 1):
                    if (t, a) in forced[j]:
                        value = forced[j][t, a]
                    else:
                        bit = bits[j]
                        local[j][bit] += 1
                        value = 2 * bit - 1
                    nxt[j].append(value)
                    totals[j][a] += value
            prev = [tuple(v) for v in nxt]
        flags = tuple(
            int(all(totals[j][a] >= v for a, v in zip(axes, event, strict=True))) for j in (0, 1)
        )
        counts[flags] += 1
    pa = Fraction(sum(v for (a, b), v in counts.items() if a), samples)
    pb = Fraction(sum(v for (a, b), v in counts.items() if b), samples)
    contrast = pb - pa
    second = Fraction(counts[0, 1] + counts[1, 0], samples)
    variance = (second - contrast * contrast) * Fraction(samples, samples - 1)
    if sum(counts.values()) != samples or variance < 0:
        raise ValueError("invalid counts")
    return InterventionContrast(
        axes,
        horizon,
        event,
        schedule_a,
        schedule_b,
        samples,
        seed,
        coupled,
        balanced,
        tuple((a, b, counts[a, b]) for a in (0, 1) for b in (0, 1)),
        pa,
        pb,
        contrast,
        variance,
        radius,
        k,
        (max(Fraction(-1), contrast - radius), min(Fraction(1), contrast + radius)),
        alpha,
    )
