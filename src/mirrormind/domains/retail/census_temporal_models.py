"""Fixed, bounded paired sign transition estimators for fictional research."""

from __future__ import annotations

from collections import Counter
from itertools import pairwise
from math import gcd

from mirrormind.domains.retail.census_bivariate import JointPMF
from mirrormind.domains.retail.census_joint_markov import (
    STATES,
    State,
    TransitionMatrix,
    TransitionRow,
    propagate_joint_markov,
)

TEMPORAL_MODELS = ("iid", "own", "cross", "full")
HISTORY_LENGTH = 24
HORIZONS = (1, 3, 6)


def _row(a: int, b: int, c: int, d: int) -> TransitionRow:
    divisor = gcd(a, b, c, d)
    return a // divisor, b // divisor, c // divisor, d // divisor


def _matrix(rows: list[TransitionRow]) -> TransitionMatrix:
    a, b, c, d = rows
    return a, b, c, d


def fit_temporal_models(history: tuple[State, ...]) -> dict[str, TransitionMatrix]:
    """Estimate fixed row laws using only the supplied 24 observed states.

    IID uses all 24 state counts. Own/cross and full use the 23
    consecutive transitions, with one pseudocount per conditional
    binary or paired outcome. Missing contexts receive uniform rows.
    No fitted matrix is selected or promoted.
    """
    if (
        type(history) is not tuple
        or len(history) != HISTORY_LENGTH
        or any(
            type(pair) is not tuple
            or len(pair) != 2
            or any(type(v) is not int for v in pair)
            or pair not in STATES
            for pair in history
        )
    ):
        raise ValueError("exactly 24 observed paired sign states required")
    pairs = tuple(pairwise(history))
    counts = Counter(history)
    iid = _row(*(counts[s] + 1 for s in STATES))
    result: dict[str, TransitionMatrix] = {"iid": (iid, iid, iid, iid)}
    for name, crossed in (("own", False), ("cross", True)):
        binary = Counter(
            (axis, previous[1 - axis if crossed else axis], nxt[axis])
            for previous, nxt in pairs
            for axis in (0, 1)
        )
        rows = []
        for previous in STATES:
            src_x, src_y = previous[::-1] if crossed else previous
            rows.append(
                _row(*((binary[0, src_x, x] + 1) * (binary[1, src_y, y] + 1) for x, y in STATES))
            )
        result[name] = _matrix(rows)
    joint = Counter(pairs)
    result["full"] = _matrix(
        [_row(*(joint[previous, nxt] + 1 for nxt in STATES)) for previous in STATES]
    )
    return result


def predict_temporal_models(history: tuple[State, ...], horizon: int) -> dict[str, JointPMF]:
    """Propagate each fixed estimated law, without selecting a model."""
    if type(horizon) is not int or horizon not in HORIZONS:
        raise ValueError("supported horizon required")
    matrices = fit_temporal_models(history)
    return {
        name: propagate_joint_markov(history[-1], (matrix,) * horizon)
        for name, matrix in matrices.items()
    }
