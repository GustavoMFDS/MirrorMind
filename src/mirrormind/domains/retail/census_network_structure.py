"""Exact local parent evidence and one-step predictive averaging."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import pairwise
from math import factorial, gcd, lcm, prod

from mirrormind.domains.retail.census_network3 import PMF3, STATES, Matrix3, State3

Parent = int | None
Graph = tuple[Parent, Parent, Parent]
ParentRow = tuple[Fraction, ...]
Posterior = tuple[ParentRow, ParentRow, ParentRow]
OPTIONS: tuple[Parent, ...] = (None, 0, 1, 2)


def _history(history: tuple[State3, ...]) -> None:
    if (
        type(history) is not tuple
        or len(history) not in (8, 24)
        or any(
            type(s) is not tuple
            or len(s) != 3
            or any(type(v) is not int for v in s)
            or s not in STATES
            for s in history
        )
    ):
        raise ValueError("eight or 24 observed binary triples required")


def _context(state: State3, parent: Parent) -> int | None:
    return None if parent is None else state[parent]


def _counts(
    history: tuple[State3, ...], child: int, parent: Parent
) -> Counter[tuple[int | None, int]]:
    return Counter((_context(p, parent), q[child]) for p, q in pairwise(history))


def _evidence(history: tuple[State3, ...], child: int, parent: Parent) -> Fraction:
    counts = _counts(history, child, parent)
    contexts = (None,) if parent is None else (-1, 1)
    return prod(
        (
            Fraction(
                factorial(counts[c, -1]) * factorial(counts[c, 1]),
                factorial(counts[c, -1] + counts[c, 1] + 1),
            )
            for c in contexts
        ),
        start=Fraction(1),
    )


def parent_posterior(history: tuple[State3, ...]) -> Posterior:
    """Equal local structure prior; independent Beta(1,1) context priors."""
    _history(history)
    rows = []
    for child in range(3):
        evidence = tuple(_evidence(history, child, parent) for parent in OPTIONS)
        total = sum(evidence)
        rows.append(tuple(v / total for v in evidence))
    a, b, c = rows
    return a, b, c


def select_parent_graphs(history: tuple[State3, ...]) -> tuple[Graph, Graph]:
    """Fixed MAP and conservative rules; no empirical calibration."""
    hard: list[Parent] = []
    conservative: list[Parent] = []
    for row in parent_posterior(history):
        best = max(range(4), key=row.__getitem__)
        hard.append(OPTIONS[best])
        conservative.append(
            OPTIONS[best]
            if best != 0
            and row[best] > 2 * row[0]
            and all(row[best] > row[j] for j in range(4) if j != best)
            else None
        )
    a, b, c = hard
    d, e, f = conservative
    return (a, b, c), (d, e, f)


def fit_parent_matrix(history: tuple[State3, ...], graph: Graph) -> Matrix3:
    """Smoothed conditional laws for an explicitly supplied local graph."""
    _history(history)
    if (
        type(graph) is not tuple
        or len(graph) != 3
        or any(p is not None and (type(p) is not int or p not in (0, 1, 2)) for p in graph)
    ):
        raise ValueError("invalid parent graph")
    counts = tuple(_counts(history, a, p) for a, p in enumerate(graph))
    rows = []
    for prev in STATES:
        row = tuple(
            prod(counts[a][_context(prev, graph[a]), nxt[a]] + 1 for a in range(3))
            for nxt in STATES
        )
        divisor = gcd(*row)
        rows.append(tuple(w // divisor for w in row))
    return tuple(rows)


def predict_parent_average(history: tuple[State3, ...], *, uniform: bool = False) -> PMF3:
    """Integrate local parent choices for exactly one future state.

    Posterior integration is exact under the independent local priors
    and one-parent model assumptions. It is not a multistep posterior
    forecast, causal identification, or calibrated graph confidence.
    """
    _history(history)
    if type(uniform) is not bool:
        raise ValueError("boolean averaging mode required")
    weights = ((Fraction(1, 4),) * 4,) * 3 if uniform else parent_posterior(history)
    positive = []
    for a, row in enumerate(weights):
        probabilities = []
        for p in OPTIONS:
            counts = _counts(history, a, p)
            c = _context(history[-1], p)
            probabilities.append(Fraction(counts[c, 1] + 1, counts[c, -1] + counts[c, 1] + 2))
        positive.append(sum((w * v for w, v in zip(row, probabilities, strict=True)), Fraction()))
    masses = tuple(
        prod(
            (positive[a] if x == 1 else 1 - positive[a] for a, x in enumerate(s)), start=Fraction(1)
        )
        for s in STATES
    )
    den = lcm(*(p.denominator for p in masses))
    integers = tuple(p.numerator * (den // p.denominator) for p in masses)
    divisor = gcd(*integers)
    if sum(integers) != den:
        raise ValueError("probability mass mismatch")
    return tuple((s, w // divisor) for s, w in zip(STATES, integers, strict=True))
