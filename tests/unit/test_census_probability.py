"""Exact probability oracles and fail-closed bound regressions."""
import random
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

import pytest

from mirrormind.domains.retail.census_probability import (
    canonical_pmf,
    convolve_increments,
    discrete_quantile,
    propagate_markov,
    reference_interval_coverage,
    score_discrete_pmf,
)

LAW = ((-4, 1), (0, 2), (4, 1))
ROWS = ((-4, ((-4, 3), (4, 1))), (4, ((-4, 1), (4, 3))))


def test_canonical_weights_and_discrete_quantiles():
    assert canonical_pmf(((-4, 3), (0, 6), (4, 3))) == LAW
    assert [discrete_quantile(LAW, q) for q in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))] == [
        -4, -4, 0, 0, 4,
    ]
    assert reference_interval_coverage(LAW, LAW) == 1
    assert reference_interval_coverage(((-2, 1), (0, 2), (2, 1)), LAW) == F(1, 2)


@pytest.mark.parametrize("horizon", range(1, 7))
def test_convolution_against_enumeration(horizon):
    actual = convolve_increments((LAW,) * horizon)
    counts = defaultdict(int)
    for sequence in product((-4, 0, 0, 4), repeat=horizon):
        counts[sum(sequence)] += 1
    assert actual == canonical_pmf(tuple(sorted(counts.items())))


@pytest.mark.parametrize("last", (-4, 4))
@pytest.mark.parametrize("horizon", range(1, 7))
def test_markov_against_enumeration(last, horizon):
    counts = defaultdict(int)
    for sequence in product((-4, 4), repeat=horizon):
        previous = last
        weight = 1
        for value in sequence:
            weight *= 3 if value == previous else 1
            previous = value
        counts[sum(sequence)] += weight
    assert propagate_markov(last, ROWS, horizon) == canonical_pmf(tuple(sorted(counts.items())))


def test_markov_distinct_row_denominators():
    rows = ((-4, ((-4, 1), (4, 2))), (4, ((-4, 3), (4, 2))))
    for horizon in range(1, 7):
        actual = dict(propagate_markov(4, rows, horizon))
        truth = defaultdict(F)
        for sequence in product((-4, 4), repeat=horizon):
            previous = 4
            weight = F(1)
            for value in sequence:
                row = dict(dict(rows)[previous])
                weight *= F(row[value], sum(row.values()))
                previous = value
            truth[sum(sequence)] += weight
        assert {x: F(w, sum(actual.values())) for x, w in actual.items()} == truth


def test_crps_against_direct_pair_and_cdf_oracles():
    rng = random.Random(41028)
    for _ in range(60):
        pmf = canonical_pmf(tuple((x, rng.randint(1, 10)) for x in sorted(rng.sample(range(-24, 25), 7))))
        total = sum(w for _, w in pmf)
        observed = rng.randint(-30, 30)
        score = score_discrete_pmf(pmf, observed)
        direct = sum((F(w * abs(x - observed), total) for x, w in pmf), F()) - sum((
            F(a * b * abs(x - y), 2 * total * total) for x, a in pmf for y, b in pmf
        ), F())
        cdf = sum((
            (F(sum(w for x, w in pmf if x <= k), total) - (observed <= k)) ** 2
            for k in range(-30, 30)
        ), F())
        assert score.crps == direct == cdf
        assert score.crps >= 0
        assert score.lower <= score.median <= score.upper
        assert score.width == score.upper - score.lower
        assert score.covered == (score.lower <= observed <= score.upper)


def test_point_mass_and_pinball_exact():
    score = score_discrete_pmf(((4, 1),), -2)
    assert score.crps == 6
    assert score.mean_pinball == 3
    assert score.median_absolute_error == 6
    assert score.width == 0
    assert not score.covered
    assert score_discrete_pmf(((4, 1),), 4).covered
    assert score_discrete_pmf(LAW, 0).crps == F(1, 2)
    assert score_discrete_pmf(LAW, 0).mean_pinball == F(4, 15)


@pytest.mark.parametrize("bad", [
    (), [], ((0, 0),), ((0, -1),), ((True, 1),), ((0, True),),
    ((145, 1),), ((-145, 1),), ((4, 1), (0, 1)), ((0, 1), (0, 2)),
    ((0, 1 << 1024),), ((0, 1 << 1023), (1, 1 << 1023)), ((0,),),
])
def test_invalid_pmf_rejected(bad):
    with pytest.raises(ValueError):
        canonical_pmf(bad)
    with pytest.raises(ValueError):
        score_discrete_pmf(bad, 0)


def test_operations_require_canonical_and_bounded_laws():
    with pytest.raises(ValueError):
        score_discrete_pmf(((0, 2),), 0)
    for laws in ((), (LAW,) * 7, (((25, 1),),), (((0, 1), (1, 1 << 64)),)):
        with pytest.raises(ValueError):
            convolve_increments(laws)
    for q in (F(-1), F(2), F(1, 1 << 64), 0.5):
        with pytest.raises(ValueError):
            discrete_quantile(LAW, q)
    for observation in (145, -145, True, 0.5):
        with pytest.raises(ValueError):
            score_discrete_pmf(LAW, observation)
    for last, rows, h in (
        (True, ROWS, 1), (0, ROWS, 1), (4, ROWS, True), (4, ROWS, 7),
        (4, ((4, ((0, 1),)),), 1),
        (4, ((4, ((4, 65536), (5, 1))), (5, ((5, 1),))), 1),
        (4, tuple((x, ((x, 1),)) for x in range(10)), 1),
    ):
        with pytest.raises(ValueError):
            propagate_markov(last, rows, h)


def test_support_boundary_and_deterministic_transition():
    assert convolve_increments((((24, 1),),) * 6) == ((144, 1),)
    assert propagate_markov(-24, ((-24, ((-24, 1),)),), 6) == ((-144, 1),)
    assert score_discrete_pmf(((144, 1),), -144).crps == 288
