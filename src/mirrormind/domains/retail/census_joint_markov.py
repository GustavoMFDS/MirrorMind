"""Bounded exact propagation of fictional paired sign Markov states."""

from __future__ import annotations

from collections import defaultdict
from math import gcd, lcm

from mirrormind.domains.retail.census_bivariate import JointPMF, canonical_joint_pmf

State = tuple[int, int]
TransitionRow = tuple[int, int, int, int]
TransitionMatrix = tuple[TransitionRow, TransitionRow, TransitionRow, TransitionRow]
STATES: tuple[State, ...] = ((-4, -4), (-4, 4), (4, -4), (4, 4))
MAX_HORIZON = 6
MAX_WEIGHT = 1024


def _validate(start: State, schedule: tuple[TransitionMatrix, ...]) -> None:
    if (
        type(start) is not tuple
        or len(start) != 2
        or any(type(v) is not int for v in start)
        or start not in STATES
    ):
        raise ValueError("invalid paired start state")
    if type(schedule) is not tuple or not 1 <= len(schedule) <= MAX_HORIZON:
        raise ValueError("bounded transition schedule required")
    for matrix in schedule:
        if type(matrix) is not tuple or len(matrix) != 4:
            raise ValueError("four transition rows required")
        for row in matrix:
            if (
                type(row) is not tuple
                or len(row) != 4
                or any(type(w) is not int or not 0 <= w <= MAX_WEIGHT for w in row)
                or sum(row) == 0
            ):
                raise ValueError("bounded nonempty transition row required")


def propagate_joint_markov(start: State, schedule: tuple[TransitionMatrix, ...]) -> JointPMF:
    """Conditional sum of future paired states, excluding the start state.

    Rows and columns follow STATES. Each row is normalized independently.
    One matrix per future step allows caller-supplied time variation.
    No schedule is inferred or authenticated by this mathematical operation.
    """
    _validate(start, schedule)
    masses = {(0, 0, STATES.index(start)): 1}
    denominator = 1
    for matrix in schedule:
        totals = tuple(sum(row) for row in matrix)
        common = lcm(*totals)
        scaled = tuple(
            tuple(w * (common // total) for w in row)
            for row, total in zip(matrix, totals, strict=True)
        )
        out: dict[tuple[int, int, int], int] = defaultdict(int)
        for (x, y, previous), a in masses.items():
            for k, (u, v) in enumerate(STATES):
                b = scaled[previous][k]
                if b:
                    out[x + u, y + v, k] += a * b
        denominator *= common
        if sum(out.values()) != denominator:
            raise ValueError("transition mass not conserved")
        divisor = gcd(denominator, *out.values())
        masses = {key: value // divisor for key, value in out.items()}
        denominator //= divisor
    projected: dict[State, int] = defaultdict(int)
    for (x, y, _), value in masses.items():
        projected[x, y] += value
    if sum(projected.values()) != denominator:
        raise ValueError("projected mass not conserved")
    return canonical_joint_pmf(tuple((x, y, w) for (x, y), w in sorted(projected.items())))
