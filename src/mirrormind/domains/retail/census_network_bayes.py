"""Bounded exact persistent-parameter Bayesian prediction for three axes."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import lcm, prod

from mirrormind.domains.retail.census_network3 import PMF3, STATES, State3, _project
from mirrormind.domains.retail.census_network_structure import (
    OPTIONS,
    _context,
    _counts,
    _evidence,
    _history,
)

MAX_BAYES_HORIZON = 3


def _conditional(history: tuple[State3, ...], prev: State3) -> tuple[Fraction, ...]:
    # Private: history includes a bounded hypothetical suffix in the
    # persistent model, or the observed prefix alone in the frozen control.
    positive = []
    for child in range(3):
        ev = tuple(_evidence(history, child, parent) for parent in OPTIONS)
        probabilities = []
        for parent in OPTIONS:
            counts = _counts(history, child, parent)
            ctx = _context(prev, parent)
            probabilities.append(Fraction(counts[ctx, 1] + 1, counts[ctx, 1] + counts[ctx, -1] + 2))
        positive.append(
            sum((e * p for e, p in zip(ev, probabilities, strict=True)), Fraction()) / sum(ev)
        )
    return tuple(
        prod(
            (positive[a] if v == 1 else 1 - positive[a] for a, v in enumerate(state)),
            start=Fraction(1),
        )
        for state in STATES
    )


def predict_persistent_bayes(
    history: tuple[State3, ...], horizon: int, *, frozen: bool = False
) -> PMF3:
    """Integrate persistent graph/parameter uncertainty under local priors.

    Each hypothetical transition updates its own path posterior only.
    The frozen control instead reuses the issuance-time posterior mean
    conditional law. That control is not exact persistent Bayesian
    integration for multiple steps. Neither uses future observations.
    """
    _history(history)
    if type(horizon) is not int or not 1 <= horizon <= MAX_BAYES_HORIZON:
        raise ValueError("one to three future steps required")
    if type(frozen) is not bool:
        raise ValueError("boolean comparison mode required")
    frozen_rows = {state: _conditional(history, state) for state in STATES} if frozen else {}
    masses: dict[State3, Fraction] = defaultdict(Fraction)

    def walk(prefix: tuple[State3, ...], cumulative: State3, weight: Fraction, left: int) -> None:
        if left == 0:
            masses[cumulative] += weight
            return
        row = frozen_rows[prefix[-1]] if frozen else _conditional(prefix, prefix[-1])
        x, y, z = cumulative
        for (u, v, w), p in zip(STATES, row, strict=True):
            walk(prefix + ((u, v, w),), (x + u, y + v, z + w), weight * p, left - 1)

    walk(history, (0, 0, 0), Fraction(1), horizon)
    if sum(masses.values()) != 1 or len(masses) != (horizon + 1) ** 3:
        raise ValueError("posterior predictive mass mismatch")
    denominator = lcm(*(p.denominator for p in masses.values()))
    return _project(
        {k: p.numerator * (denominator // p.denominator) for k, p in masses.items()}, denominator
    )
