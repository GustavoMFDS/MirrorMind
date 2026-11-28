"""Exact conditional counterfactuals within a specified binary response-type class."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import pairwise, product
from math import prod
from typing import Literal

from mirrormind.domains.retail.census_modular import PMF, History, State, _law
from mirrormind.domains.retail.census_modular_interventions import Schedule, _schedule

Graph = tuple[State, ...]
Key = tuple[int, int]
Theta = dict[Key, F]
ZERO = F(0)
QUARTER = F(1, 4)
TYPES = ((-1, -1), (-1, 1), (1, -1), (1, 1))


def _validate(factual: History, graph: Graph, axes: State) -> int:
    if (
        type(factual) is not tuple
        or not 2 <= len(factual) <= 4
        or any(
            type(s) is not tuple
            or len(s) != 3
            or any(type(x) is not int or x not in (-1, 1) for x in s)
            for s in factual
        )
    ):
        raise ValueError("bounded complete factual trajectory required")
    if (
        type(graph) is not tuple
        or len(graph) != 3
        or any(
            type(ps) is not tuple
            or len(ps) > 2
            or any(type(a) is not int or not 0 <= a < 3 for a in ps)
            or tuple(sorted(set(ps))) != ps
            for ps in graph
        )
    ):
        raise ValueError("canonical supplied parent sets required")
    if (
        type(axes) is not tuple
        or not 1 <= len(axes) <= 3
        or any(type(a) is not int or not 0 <= a < 3 for a in axes)
        or len(set(axes)) != len(axes)
    ):
        raise ValueError("ordered distinct axes required")
    return len(factual) - 1


def _sign(prev: State, parents: State) -> int | None:
    return prod(prev[a] for a in parents) if parents else None


def _positive(
    factual_sign: int | None, factual_value: int, alternative_sign: int | None, theta: F
) -> F:
    if factual_sign is None:
        return F(factual_value == 1)
    weights = (theta, F(3, 4) - theta, QUARTER - theta, theta)
    i = int(factual_sign == 1)
    j = int(alternative_sign == 1)
    den = sum((w for r, w in zip(TYPES, weights, strict=True) if r[i] == factual_value), F(0))
    return (
        sum(w for r, w in zip(TYPES, weights, strict=True) if r[i] == factual_value and r[j] == 1)
        / den
    )


def _likelihood(factual: History, graph: Graph) -> F:
    return prod(
        (
            F(1, 2) if not ps else F(3, 4) if _sign(prev, ps) == nxt[a] else QUARTER
            for prev, nxt in pairwise(factual)
            for a, ps in enumerate(graph)
        ),
        start=F(1),
    )


def _distribution(
    factual: History, graph: Graph, axes: State, force: dict[Key, int], theta: Theta
) -> PMF:
    mass = {(factual[0], (0,) * len(axes)): F(1)}
    for t in range(1, len(factual)):
        out: dict[tuple[State, State], F] = defaultdict(F)
        for (prev, total), weight in mass.items():
            positive = tuple(
                F(force[t, a] == 1)
                if (t, a) in force
                else _positive(
                    _sign(factual[t - 1], ps),
                    factual[t][a],
                    _sign(prev, ps),
                    theta.get((t, a), ZERO),
                )
                for a, ps in enumerate(graph)
            )
            for nxt, w in _law(positive):
                if w:
                    key = tuple(v + nxt[a] for a, v in zip(axes, total, strict=True))
                    out[nxt, key] += weight * w
        mass = out
    result: dict[State, F] = defaultdict(F)
    for (_, key), w in mass.items():
        result[key] += w
    if sum(result.values()) != 1:
        raise ValueError("mass mismatch")
    return tuple(sorted(result.items()))


@dataclass(frozen=True, slots=True)
class CounterfactualResult:
    pmf: PMF
    factual_likelihood: F
    mechanism: Literal["flip", "threshold"]
    scope: str = "supplied_structural_model_only"
    forecast_eligible: bool = False
    action_authorized: bool = False


def counterfactual(
    factual: History,
    graph: Graph,
    axes: State,
    interventions: Schedule = (),
    *,
    mechanism: Literal["flip", "threshold"],
) -> CounterfactualResult:
    """Abduct response types from natural factual transitions, then replace mechanisms.

    Known lag-one graph; sign-product contexts; independent response types
    across children and times; P(+|sign -)=1/4 and P(+|sign +)=3/4.
    No-parent children have a shared constant response. Factual likelihood
    is conditional on the observed initial state, not a model fit.
    """
    h = _validate(factual, graph, axes)
    if type(mechanism) is not str or mechanism not in ("flip", "threshold"):
        raise ValueError("unknown supplied mechanism")
    force = _schedule(interventions, 3, h)
    value = ZERO if mechanism == "flip" else QUARTER
    theta = {(t, a): value for t in range(2, h + 1) for a, ps in enumerate(graph) if ps}
    return CounterfactualResult(
        _distribution(factual, graph, axes, force, theta), _likelihood(factual, graph), mechanism
    )


@dataclass(frozen=True, slots=True)
class StructuralBounds:
    lower: F
    upper: F
    lower_witness: tuple[F, ...]
    upper_witness: tuple[F, ...]
    keys: tuple[Key, ...]
    vertices: int
    global_endpoints: tuple[F, F]
    direction: Literal["positive", "negative", "zero", "ambiguous"]
    factual_likelihood: F
    scope: str = "independent_occurrence_response_type_class_only"
    forecast_eligible: bool = False
    action_authorized: bool = False


def counterfactual_bounds(
    factual: History,
    graph: Graph,
    axes: State,
    event: State,
    schedule_a: Schedule,
    schedule_b: Schedule,
) -> StructuralBounds:
    """Sharp contrast bounds over independent occurrence-specific response laws.

    Theta=P(both sign responses positive) in [0,1/4]. The factual
    likelihood is invariant; the conditional contrast is multi-affine
    because each independent response law occurs at most once per path.
    Extremal vertices therefore suffice. Not bounds over arbitrary SCMs.
    """
    h = _validate(factual, graph, axes)
    if (
        type(event) is not tuple
        or len(event) != len(axes)
        or any(type(v) is not int or not -h <= v <= h for v in event)
    ):
        raise ValueError("bounded threshold vector required")
    a = _schedule(schedule_a, 3, h)
    b = _schedule(schedule_b, 3, h)
    keys = tuple((t, i) for t in range(2, h + 1) for i, ps in enumerate(graph) if ps)

    def probability(force: dict[Key, int], theta: Theta) -> F:
        return sum(
            (
                w
                for s, w in _distribution(factual, graph, axes, force, theta)
                if all(x >= v for x, v in zip(s, event, strict=True))
            ),
            F(),
        )

    values = []
    for vertex in product((ZERO, QUARTER), repeat=len(keys)):
        theta = dict(zip(keys, vertex, strict=True))
        values.append((probability(b, theta) - probability(a, theta), vertex))
    lo = min(values)
    hi = max(values)
    direction: Literal["positive", "negative", "zero", "ambiguous"]
    if lo[0] > 0:
        direction = "positive"
    elif hi[0] < 0:
        direction = "negative"
    elif lo[0] == hi[0] == 0:
        direction = "zero"
    else:
        direction = "ambiguous"
    return StructuralBounds(
        lo[0],
        hi[0],
        lo[1],
        hi[1],
        keys,
        len(values),
        (values[0][0], values[-1][0]),
        direction,
        _likelihood(factual, graph),
    )
