"""Exact joint probability oracles and contract bounds."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product

import pytest

from mirrormind.domains.retail.census_bivariate import (
    canonical_joint_pmf,
    convolve_joint_increments,
    independent_joint_projection,
    joint_brier_score,
    joint_covariance,
    joint_marginal,
    joint_positive_probability,
    reference_joint_brier_excess,
)

POS = ((-4, -4, 3), (-4, 4, 1), (4, -4, 1), (4, 4, 3))
NEG = ((-4, -4, 1), (-4, 4, 3), (4, -4, 3), (4, 4, 1))
IND = ((-4, -4, 1), (-4, 4, 1), (4, -4, 1), (4, 4, 1))


@pytest.mark.parametrize("h", range(1, 7))
def test_joint_convolution_and_marginal_projection(h):
    for law in (POS, NEG, IND):
        p = convolve_joint_increments((law,) * h)
        brute = defaultdict(int)
        for seq in product(law, repeat=h):
            mass = 1
            for _, _, w in seq:
                mass *= w
            brute[sum(x for x, _, _ in seq), sum(y for _, y, _ in seq)] += mass
        assert p == canonical_joint_pmf(tuple((x, y, w) for (x, y), w in sorted(brute.items())))
        independent = independent_joint_projection(p)
        assert independent == convolve_joint_increments((IND,) * h)
        for axis in (0, 1):
            assert joint_marginal(p, axis) == joint_marginal(independent, axis)
        assert joint_covariance(p) == h * {POS: 8, NEG: -8, IND: 0}[law]


def test_joint_brier_exact_proper_score_identity():
    q = convolve_joint_increments((POS,) * 3)
    for law in (POS, NEG, IND):
        p = convolve_joint_increments((law,) * 3)

        def expected(r):
            total = sum(w for _, _, w in q)
            return sum((F(w, total) * joint_brier_score(r, (x, y)) for x, y, w in q), F())

        assert expected(p) - expected(q) == reference_joint_brier_excess(p, q)
        assert (reference_joint_brier_excess(p, q) == 0) == (law == POS)
    assert joint_positive_probability(POS) == F(3, 8)
    assert joint_positive_probability(NEG) == F(1, 8)
    assert joint_positive_probability(IND) == F(1, 4)


def test_asymmetric_marginals_and_out_of_support_observation():
    p = ((-4, -4, 1), (-4, 4, 2), (4, -4, 3), (4, 4, 5))
    q = independent_joint_projection(p)
    assert joint_covariance(q) == 0
    assert joint_marginal(p, 0) == joint_marginal(q, 0)
    assert joint_marginal(p, 1) == joint_marginal(q, 1)
    assert joint_brier_score(((0, 0, 1),), (1, 1)) == 2
    assert joint_brier_score(((0, 0, 1),), (0, 0)) == 0


@pytest.mark.parametrize(
    "bad",
    [
        (),
        [],
        ((0, 0, 0),),
        ((0, 0, -1),),
        ((True, 0, 1),),
        ((0, True, 1),),
        ((0, 0, True),),
        ((25, 0, 1),),
        ((0, -25, 1),),
        ((0, 0, 1), (0, 0, 2)),
        ((1, 0, 1), (0, 0, 1)),
        ((0, 0, 1 << 512),),
        ((0, 0),),
    ],
)
def test_joint_rejects_invalid_inputs(bad):
    with pytest.raises(ValueError):
        canonical_joint_pmf(bad)
    with pytest.raises(ValueError):
        joint_covariance(bad)


def test_joint_bounds_and_canonical_contract():
    with pytest.raises(ValueError):
        joint_covariance(((0, 0, 2),))
    with pytest.raises(ValueError):
        convolve_joint_increments((POS,) * 7)
    with pytest.raises(ValueError):
        convolve_joint_increments((((5, 0, 1),),))
    with pytest.raises(ValueError):
        convolve_joint_increments((((0, 0, 1), (1, 1, 1 << 64)),))
    with pytest.raises(ValueError):
        joint_marginal(POS, True)
    with pytest.raises(ValueError):
        joint_brier_score(POS, (25, 0))
    with pytest.raises(ValueError):
        joint_brier_score(POS, (0, True))
    assert convolve_joint_increments((((4, -4, 1),),) * 6) == ((24, -24, 1),)
