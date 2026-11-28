"""Bounded exact bivariate probability primitives for fictional research."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import gcd

from mirrormind.domains.retail.census_probability import PMF, canonical_pmf

JointPMF = tuple[tuple[int, int, int], ...]
MAX_AXIS_INCREMENT = 4
MAX_JOINT_HORIZON = 6
MAX_AXIS_DISPLACEMENT = MAX_AXIS_INCREMENT * MAX_JOINT_HORIZON
MAX_JOINT_SUPPORT = (2 * MAX_AXIS_DISPLACEMENT + 1) ** 2
MAX_JOINT_MASS_BITS = 512


def _validate(pmf: JointPMF, *, canonical: bool = True) -> int:
    if type(pmf) is not tuple or not 1 <= len(pmf) <= MAX_JOINT_SUPPORT:
        raise ValueError("bounded joint support required")
    previous = (-MAX_AXIS_DISPLACEMENT - 1, -MAX_AXIS_DISPLACEMENT - 1)
    total = divisor = 0
    for cell in pmf:
        if type(cell) is not tuple or len(cell) != 3:
            raise ValueError("invalid joint cell")
        x, y, w = cell
        if (
            type(x) is not int
            or type(y) is not int
            or abs(x) > MAX_AXIS_DISPLACEMENT
            or abs(y) > MAX_AXIS_DISPLACEMENT
            or (x, y) <= previous
            or type(w) is not int
            or w <= 0
            or w.bit_length() > MAX_JOINT_MASS_BITS
        ):
            raise ValueError("invalid joint support or mass")
        previous = x, y
        total += w
        divisor = gcd(divisor, w)
    if total.bit_length() > MAX_JOINT_MASS_BITS or (canonical and divisor != 1):
        raise ValueError("bounded canonical joint mass required")
    return total


def canonical_joint_pmf(weights: JointPMF) -> JointPMF:
    """Reduce sorted, unique, positive weights by their common divisor."""
    _validate(weights, canonical=False)
    divisor = gcd(*(w for _, _, w in weights))
    return tuple((x, y, w // divisor) for x, y, w in weights)


def convolve_joint_increments(laws: tuple[JointPMF, ...]) -> JointPMF:
    """Sum up to six independent-in-time paired increment laws."""
    if type(laws) is not tuple or not 1 <= len(laws) <= MAX_JOINT_HORIZON:
        raise ValueError("bounded joint horizon required")
    masses = {(0, 0): 1}
    expected = 1
    for law in laws:
        total = _validate(law)
        if total.bit_length() > 64 or any(
            abs(x) > MAX_AXIS_INCREMENT or abs(y) > MAX_AXIS_INCREMENT for x, y, _ in law
        ):
            raise ValueError("bounded joint increment law required")
        out: dict[tuple[int, int], int] = defaultdict(int)
        for (x, y), a in masses.items():
            for u, v, b in law:
                out[x + u, y + v] += a * b
        masses = out
        expected *= total
    if sum(masses.values()) != expected:
        raise ValueError("joint mass not conserved")
    return canonical_joint_pmf(tuple((x, y, w) for (x, y), w in sorted(masses.items())))


def joint_marginal(pmf: JointPMF, axis: int) -> PMF:
    _validate(pmf)
    if type(axis) is not int or axis not in (0, 1):
        raise ValueError("invalid joint axis")
    out: dict[int, int] = defaultdict(int)
    for x, y, w in pmf:
        out[(x, y)[axis]] += w
    return canonical_pmf(tuple(sorted(out.items())))


def independent_joint_projection(pmf: JointPMF) -> JointPMF:
    """Replace dependence with independence, preserving exact marginals.

    The resulting canonical mass must fit the same joint contract.
    """
    x, y = joint_marginal(pmf, 0), joint_marginal(pmf, 1)
    divisor = gcd(*(a * b for _, a in x for _, b in y))
    return canonical_joint_pmf(tuple((u, v, a * b // divisor) for u, a in x for v, b in y))


def joint_covariance(pmf: JointPMF) -> Fraction:
    total = _validate(pmf)
    sx = sum(x * w for x, _, w in pmf)
    sy = sum(y * w for _, y, w in pmf)
    return Fraction(sum(x * y * w for x, y, w in pmf), total) - Fraction(sx * sy, total**2)


def joint_positive_probability(pmf: JointPMF) -> Fraction:
    total = _validate(pmf)
    return Fraction(sum(w for x, y, w in pmf if x > 0 and y > 0), total)


def joint_brier_score(pmf: JointPMF, observed: tuple[int, int]) -> Fraction:
    total = _validate(pmf)
    if (
        type(observed) is not tuple
        or len(observed) != 2
        or any(type(v) is not int or abs(v) > MAX_AXIS_DISPLACEMENT for v in observed)
    ):
        raise ValueError("bounded joint observation required")
    match = next((w for x, y, w in pmf if (x, y) == observed), 0)
    return 1 - Fraction(2 * match, total) + Fraction(sum(w * w for _, _, w in pmf), total**2)


def reference_joint_brier_excess(pmf: JointPMF, reference: JointPMF) -> Fraction:
    """Squared probability-vector distance to a supplied, unverified reference."""
    total, ref_total = _validate(pmf), _validate(reference)
    p = {(x, y): w for x, y, w in pmf}
    q = {(x, y): w for x, y, w in reference}
    return Fraction(
        sum(
            (p.get(cell, 0) * ref_total - q.get(cell, 0) * total) ** 2
            for cell in p.keys() | q.keys()
        ),
        (total * ref_total) ** 2,
    )
