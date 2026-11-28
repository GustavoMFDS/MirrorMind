"""Bounded exact discrete probability primitives for fictional research."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, lcm

PMF = tuple[tuple[int, int], ...]
TransitionRows = tuple[tuple[int, PMF], ...]
MAX_INCREMENT = 24
MAX_HORIZON = 6
MAX_DISPLACEMENT = MAX_INCREMENT * MAX_HORIZON
MAX_WEIGHT_BITS = 1024
MAX_STATES = 9
MAX_TRANSITION_WEIGHT = 65535


def _validate(pmf: PMF) -> int:
    if type(pmf) is not tuple or not 1 <= len(pmf) <= 2 * MAX_DISPLACEMENT + 1:
        raise ValueError("bounded probability support required")
    total = 0
    previous = -MAX_DISPLACEMENT - 1
    divisor = 0
    for pair in pmf:
        if type(pair) is not tuple or len(pair) != 2:
            raise ValueError("invalid probability pair")
        value, weight = pair
        if (
            type(value) is not int or not previous < value <= MAX_DISPLACEMENT
            or type(weight) is not int or weight <= 0 or weight.bit_length() > MAX_WEIGHT_BITS
        ):
            raise ValueError("invalid support or weight")
        total += weight
        divisor = gcd(divisor, weight)
        previous = value
    if total.bit_length() > MAX_WEIGHT_BITS or divisor != 1:
        raise ValueError("canonical bounded probability weights required")
    return total


def _normalized(masses: dict[int, int]) -> PMF:
    divisor = gcd(*masses.values())
    result = tuple(sorted((x, w // divisor) for x, w in masses.items()))
    _validate(result)
    return result


def canonical_pmf(weights: PMF) -> PMF:
    """Normalize sorted unique positive weights; reject invalid input before arithmetic."""
    if type(weights) is not tuple or not 1 <= len(weights) <= 2 * MAX_DISPLACEMENT + 1:
        raise ValueError("bounded probability support required")
    masses: dict[int, int] = {}
    previous = -MAX_DISPLACEMENT - 1
    total = 0
    for pair in weights:
        if type(pair) is not tuple or len(pair) != 2:
            raise ValueError("invalid probability pair")
        value, weight = pair
        if (
            type(value) is not int or not previous < value <= MAX_DISPLACEMENT
            or type(weight) is not int or weight <= 0 or weight.bit_length() > MAX_WEIGHT_BITS
        ):
            raise ValueError("invalid support or weight")
        masses[value] = weight
        total += weight
        previous = value
    if total.bit_length() > MAX_WEIGHT_BITS:
        raise ValueError("bounded probability mass required")
    return _normalized(masses)


def _horizon(horizon: int) -> None:
    if type(horizon) is not int or not 1 <= horizon <= MAX_HORIZON:
        raise ValueError("invalid probability horizon")


def convolve_increments(laws: tuple[PMF, ...]) -> PMF:
    """Distribution of the sum of up to six independent integer increments."""
    if type(laws) is not tuple:
        raise ValueError("exact tuple of increment laws required")
    _horizon(len(laws))
    masses = {0: 1}
    for law in laws:
        total = _validate(law)
        if law[0][0] < -MAX_INCREMENT or law[-1][0] > MAX_INCREMENT or total.bit_length() > 64:
            raise ValueError("bounded increment law required")
        out: dict[int, int] = defaultdict(int)
        for x, a in masses.items():
            for y, b in law:
                out[x + y] += a * b
        masses = out
    return _normalized(masses)


def propagate_markov(last: int, transitions: TransitionRows, horizon: int) -> PMF:
    """Exact cumulative displacement conditional on a finite observed state."""
    _horizon(horizon)
    if type(transitions) is not tuple or not 1 <= len(transitions) <= MAX_STATES:
        raise ValueError("bounded transition rows required")
    rows: dict[int, PMF] = {}
    totals: dict[int, int] = {}
    previous = -MAX_INCREMENT - 1
    for pair in transitions:
        if type(pair) is not tuple or len(pair) != 2:
            raise ValueError("invalid transition row")
        state, row = pair
        if type(state) is not int or not previous < state <= MAX_INCREMENT:
            raise ValueError("invalid transition state")
        total = _validate(row)
        if total > MAX_TRANSITION_WEIGHT or len(row) > MAX_STATES:
            raise ValueError("bounded transition weights required")
        rows[state] = row
        totals[state] = total
        previous = state
    if type(last) is not int or last not in rows or any(
        x not in rows for row in rows.values() for x, _ in row
    ):
        raise ValueError("transition states must be closed")
    common = lcm(*totals.values())
    scaled = {
        state: tuple((x, w * (common // totals[state])) for x, w in row)
        for state, row in rows.items()
    }
    states = {(0, last): 1}
    for _ in range(horizon):
        nxt: dict[tuple[int, int], int] = defaultdict(int)
        for (total, state), mass in states.items():
            for x, weight in scaled[state]:
                nxt[total + x, x] += mass * weight
        states = nxt
    masses: dict[int, int] = defaultdict(int)
    for (total, _), mass in states.items():
        masses[total] += mass
    if sum(masses.values()) != common ** horizon:
        raise ValueError("probability mass not conserved")
    return _normalized(masses)


def _quantile(pmf: PMF, total: int, q: Fraction) -> int:
    cumulative = 0
    for value, weight in pmf:
        cumulative += weight
        if cumulative * q.denominator >= q.numerator * total:
            return value
    raise ValueError("invalid probability mass")


def discrete_quantile(pmf: PMF, q: Fraction) -> int:
    """Inverse discrete CDF, with q=0 defined as minimum support."""
    total = _validate(pmf)
    if (
        type(q) is not Fraction or not 0 <= q <= 1
        or q.denominator.bit_length() > 64
    ):
        raise ValueError("bounded exact quantile required")
    return _quantile(pmf, total, q)


_Q = (Fraction(1, 10), Fraction(1, 2), Fraction(9, 10))


@dataclass(frozen=True, slots=True)
class DiscreteScores:
    lower: int
    median: int
    upper: int
    crps: Fraction
    mean_pinball: Fraction
    median_absolute_error: int
    covered: bool
    width: int


def score_discrete_pmf(pmf: PMF, observed: int) -> DiscreteScores:
    """Exact CRPS and three fixed quantile scores; no calibration claim."""
    total = _validate(pmf)
    if type(observed) is not int or abs(observed) > MAX_DISPLACEMENT:
        raise ValueError("bounded integer observation required")
    lo, med, hi = (_quantile(pmf, total, q) for q in _Q)
    prefix_w = prefix_x = pairs = 0
    for x, w in pmf:
        pairs += w * (x * prefix_w - prefix_x)
        prefix_w += w
        prefix_x += x * w
    crps = Fraction(sum(w * abs(x - observed) for x, w in pmf), total) - Fraction(
        pairs, total * total
    )
    pinball = sum((
        q * (observed - x) if observed >= x else (1 - q) * (x - observed)
        for q, x in zip(_Q, (lo, med, hi), strict=True)
    ), Fraction()) / 3
    return DiscreteScores(lo, med, hi, crps, pinball, abs(observed - med),
                          lo <= observed <= hi, hi - lo)


def reference_interval_coverage(pmf: PMF, reference: PMF) -> Fraction:
    """Mass of an explicitly supplied reference law inside inclusive 10/90 bounds."""
    total = _validate(pmf)
    ref_total = _validate(reference)
    lo, hi = (_quantile(pmf, total, q) for q in (_Q[0], _Q[2]))
    return Fraction(sum(w for x, w in reference if lo <= x <= hi), ref_total)
