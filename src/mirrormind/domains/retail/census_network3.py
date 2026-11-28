"""Exact bounded conditional propagation for three fictional binary axes."""

from __future__ import annotations

from collections import defaultdict
from itertools import product
from math import gcd, lcm, prod
from typing import TypeVar

State3 = tuple[int, int, int]
PMF3 = tuple[tuple[State3, int], ...]
Matrix3 = tuple[tuple[int, ...], ...]
BinaryRow = tuple[int, int]
BinaryLaw = tuple[BinaryRow, BinaryRow]
FactorStep = tuple[State3, tuple[BinaryLaw, BinaryLaw, BinaryLaw]]
STATES: tuple[State3, ...] = tuple((a, b, c) for a, b, c in product((-1, 1), repeat=3))
MAX_HORIZON = 6
MAX_WEIGHT = 25**3
MAX_BINARY_WEIGHT = 25
_K = TypeVar("_K")


def _start(start: State3) -> None:
    if (
        type(start) is not tuple
        or len(start) != 3
        or any(type(v) is not int or v not in (-1, 1) for v in start)
    ):
        raise ValueError("exact binary triple required")


def _schedule(schedule: tuple[object, ...]) -> None:
    if type(schedule) is not tuple or not 1 <= len(schedule) <= MAX_HORIZON:
        raise ValueError("bounded schedule required")


def _row(row: tuple[int, ...], size: int, bound: int) -> None:
    if (
        type(row) is not tuple
        or len(row) != size
        or any(type(w) is not int or not 0 <= w <= bound for w in row)
        or not sum(row)
    ):
        raise ValueError("bounded nonempty integer row required")


def _reduce(mass: dict[_K, int], den: int) -> tuple[dict[_K, int], int]:
    if not mass or sum(mass.values()) != den:
        raise ValueError("mass not conserved")
    divisor = gcd(den, *mass.values())
    return {key: w // divisor for key, w in mass.items()}, den // divisor


def _project(mass: dict[State3, int], den: int) -> PMF3:
    reduced, total = _reduce(mass, den)
    if len(reduced) > 343 or total.bit_length() > 1024:
        raise ValueError("bounded canonical output required")
    return tuple(sorted(reduced.items()))


def propagate_network3(start: State3, schedule: tuple[Matrix3, ...]) -> PMF3:
    """Joint Markov law of cumulative future states, excluding the start.

    Each immutable matrix has eight rows and columns in STATES order.
    Row weights are independently normalized. Zero transitions allowed.
    """
    _start(start)
    _schedule(schedule)
    for matrix in schedule:
        if type(matrix) is not tuple or len(matrix) != 8:
            raise ValueError("eight transition rows required")
        for row in matrix:
            _row(row, 8, MAX_WEIGHT)
    mass = {(0, 0, 0, STATES.index(start)): 1}
    den = 1
    for matrix in schedule:
        totals = tuple(sum(row) for row in matrix)
        common = lcm(*totals)
        rows = tuple(
            tuple(w * (common // total) for w in row)
            for row, total in zip(matrix, totals, strict=True)
        )
        out: dict[tuple[int, int, int, int], int] = defaultdict(int)
        for (x, y, z, prev), a in mass.items():
            for k, (u, v, w) in enumerate(STATES):
                b = rows[prev][k]
                if b:
                    out[x + u, y + v, z + w, k] += a * b
        mass, den = _reduce(out, den * common)
    projected: dict[State3, int] = defaultdict(int)
    for (x, y, z, _), w in mass.items():
        projected[x, y, z] += w
    return _project(projected, den)


def _factor(step: FactorStep) -> None:
    if type(step) is not tuple or len(step) != 2:
        raise ValueError("invalid factor step")
    parents, rows = step
    if (
        type(parents) is not tuple
        or len(parents) != 3
        or any(type(v) is not int for v in parents)
        or set(parents) != {0, 1, 2}
    ):
        raise ValueError("bijective parents required")
    if type(rows) is not tuple or len(rows) != 3:
        raise ValueError("three binary laws required")
    for axis in rows:
        if type(axis) is not tuple or len(axis) != 2:
            raise ValueError("two conditional rows required")
        for row in axis:
            _row(row, 2, MAX_BINARY_WEIGHT)


def factor_matrix(step: FactorStep) -> Matrix3:
    """Expand a validated factor law into an equivalent joint matrix."""
    _factor(step)
    parents, rows = step
    return tuple(
        tuple(
            prod(rows[a][int(prev[parents[a]] == 1)][int(nxt[a] == 1)] for a in range(3))
            for nxt in STATES
        )
        for prev in STATES
    )


def propagate_lineages3(start: State3, schedule: tuple[FactorStep, ...]) -> PMF3:
    """Exact lineage decomposition for bijective parents at each step.

    Conditional on the fixed start, independent binary innovations and
    unique descendants imply independent lineages. Arbitrary graphs,
    shared parents and correlated innovations are outside this contract.
    """
    _start(start)
    _schedule(schedule)
    for step in schedule:
        _factor(step)
    combined: dict[State3, int] = {(0, 0, 0): 1}
    total = 1
    for root in range(3):
        axis = root
        mass = {(0, 0, 0, start[root]): 1}
        den = 1
        for parents, rows in schedule:
            axis = parents.index(axis)
            a, b = rows[axis]
            u, v = sum(a), sum(b)
            common = lcm(u, v)
            scaled = (tuple(w * (common // u) for w in a), tuple(w * (common // v) for w in b))
            out: dict[tuple[int, int, int, int], int] = defaultdict(int)
            for (x, y, z, previous), p in mass.items():
                for sign, w in zip((-1, 1), scaled[int(previous == 1)], strict=True):
                    if w:
                        vec = [x, y, z]
                        vec[axis] += sign
                        out[vec[0], vec[1], vec[2], sign] += p * w
            mass, den = _reduce(out, den * common)
        marginal: dict[State3, int] = defaultdict(int)
        for (x, y, z, _), p in mass.items():
            marginal[x, y, z] += p
        marginal, den = _reduce(marginal, den)
        convolution: dict[State3, int] = defaultdict(int)
        for (x, y, z), p in combined.items():
            for (u, v, w), q in marginal.items():
                convolution[x + u, y + v, z + w] += p * q
        combined, total = _reduce(convolution, total * den)
    return _project(combined, total)
