"""Bounded exact posterior queries for explicitly scoped modular networks."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, pairwise, product
from math import factorial, prod

State = tuple[int, ...]
History = tuple[State, ...]
Modules = tuple[tuple[int, ...], ...]
Ports = tuple[tuple[int, int], ...]
PMF = tuple[tuple[State, Fraction], ...]
Scope = tuple[tuple[int, ...], ...]
LocalRow = tuple[tuple[tuple[int, ...], Counter[tuple[State, int]], Fraction], ...]
MAX_DIMENSION = 12
MAX_QUERY_AXES = 4
MAX_SCOPE = 8
MAX_PORTS = 24


def _validate(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    balanced: bool,
) -> tuple[Scope, State]:
    if type(history) is not tuple or len(history) not in (24, 48) or type(history[0]) is not tuple:
        raise ValueError("bounded history required")
    d = len(history[0])
    if not 2 <= d <= MAX_DIMENSION or any(
        type(s) is not tuple
        or len(s) != d
        or any(type(x) is not int or x not in (-1, 1) for x in s)
        for s in history
    ):
        raise ValueError("binary states required")
    if (
        type(modules) is not tuple
        or not modules
        or any(
            type(m) is not tuple
            or not 1 <= len(m) <= 6
            or any(type(a) is not int or not 0 <= a < d for a in m)
            for m in modules
        )
    ):
        raise ValueError("bounded module partition required")
    flat = tuple(a for module in modules for a in module)
    if len(flat) != d or set(flat) != set(range(d)):
        raise ValueError("partition must cover every axis once")
    owner = {a: i for i, module in enumerate(modules) for a in module}
    if (
        type(ports) is not tuple
        or len(ports) > MAX_PORTS
        or any(
            type(p) is not tuple
            or len(p) != 2
            or any(type(a) is not int or not 0 <= a < d for a in p)
            or owner[p[0]] == owner[p[1]]
            for p in ports
        )
    ):
        raise ValueError("bounded directed cross-module ports required")
    if len(set(ports)) != len(ports):
        raise ValueError("duplicate port")
    if (
        type(axes) is not tuple
        or not 1 <= len(axes) <= MAX_QUERY_AXES
        or any(type(a) is not int or not 0 <= a < d for a in axes)
        or len(set(axes)) != len(axes)
    ):
        raise ValueError("distinct ordered query axes required")
    if type(horizon) is not int or horizon not in (1, 2) or type(balanced) is not bool:
        raise ValueError("bounded horizon and boolean prior required")
    allowed = tuple(
        tuple(sorted(set(modules[owner[a]]) | {src for src, dst in ports if dst == a}))
        for a in range(d)
    )
    if any(len(p) > MAX_SCOPE for p in allowed):
        raise ValueError("local parent scope exceeds eight axes")
    closure = (
        tuple(sorted(set(axes) | {p for a in axes for p in allowed[a]})) if horizon == 2 else axes
    )
    if len(closure) > MAX_SCOPE:
        raise ValueError("exact closure exceeds eight axes")
    return allowed, closure


def _prepare(
    history: History, scope: Scope, children: State, balanced: bool
) -> dict[int, LocalRow]:
    rows = {}
    for a in children:
        options = tuple(p for size in range(3) for p in combinations(scope[a], size))
        sizes = Counter(map(len, options))
        local = []
        for parents in options:
            counts = Counter(
                (tuple(prev[p] for p in parents), nxt[a]) for prev, nxt in pairwise(history)
            )
            evidence = prod(
                (
                    Fraction(
                        factorial(counts[ctx, -1]) * factorial(counts[ctx, 1]),
                        factorial(counts[ctx, -1] + counts[ctx, 1] + 1),
                    )
                    for ctx in product((-1, 1), repeat=len(parents))
                ),
                start=Fraction(1),
            )
            prior = Fraction(1, len(sizes) * sizes[len(parents)] if balanced else len(options))
            local.append((parents, counts, evidence * prior))
        rows[a] = tuple(local)
    return rows


def _positive(
    row: LocalRow,
    prev: State | dict[int, int],
    *,
    observed_prev: State | None = None,
    child: int | None = None,
) -> Fraction:
    numerator = Fraction()
    den = Fraction()
    for parents, counts, weight in row:
        ctx = tuple(prev[p] for p in parents)
        neg, pos = counts[ctx, -1], counts[ctx, 1]
        if observed_prev is not None:
            if child is None:
                raise ValueError("hypothetical child required")
            old_ctx = tuple(observed_prev[p] for p in parents)
            y = prev[child]
            weight *= Fraction(counts[old_ctx, y] + 1, counts[old_ctx, -1] + counts[old_ctx, 1] + 2)
            if old_ctx == ctx:
                neg += int(y == -1)
                pos += int(y == 1)
        numerator += weight * Fraction(pos + 1, neg + pos + 2)
        den += weight
    return numerator / den


def _law(positive: tuple[Fraction, ...]) -> PMF:
    return tuple(
        (
            state,
            prod(
                (p if x == 1 else 1 - p for x, p in zip(state, positive, strict=True)),
                start=Fraction(1),
            ),
        )
        for state in product((-1, 1), repeat=len(positive))
    )


def predict_modular(
    history: History,
    modules: Modules,
    ports: Ports,
    axes: State,
    horizon: int,
    *,
    balanced: bool = False,
) -> tuple[PMF, State]:
    """Return exact cumulative subset PMF and enumerated first-step axes.

    Each child has at most two lag-one parents in its module or incoming
    ports. Independent local graph and Beta(1,1) context priors persist
    for the hypothetical trajectory. Balanced mode gives equal mass to
    available parent-set sizes. Ports declare candidates, not causal
    edges. No observed future data or fallback approximation.
    """
    scope, closure = _validate(history, modules, ports, axes, horizon, balanced)
    rows = _prepare(history, scope, closure, balanced)
    prev = history[-1]
    initial = _law(tuple(_positive(rows[a], prev) for a in closure))
    if horizon == 1:
        return initial, closure
    mass: dict[State, Fraction] = defaultdict(Fraction)
    for values, w in initial:
        first = dict(zip(closure, values, strict=True))
        positive = tuple(_positive(rows[a], first, observed_prev=prev, child=a) for a in axes)
        for nxt, v in _law(positive):
            mass[tuple(first[a] + x for a, x in zip(axes, nxt, strict=True))] += w * v
    if sum(mass.values()) != 1 or len(mass) != 3 ** len(axes):
        raise ValueError("mass mismatch")
    return tuple(sorted(mass.items())), closure
