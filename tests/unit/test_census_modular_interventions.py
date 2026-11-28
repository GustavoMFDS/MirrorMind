"""Exact and paired modular mechanism replacement checks."""

from fractions import Fraction as F
from random import Random

import pytest

from mirrormind.domains.retail.census_modular import _law, _positive, _prepare, predict_modular
from mirrormind.domains.retail.census_modular_interventions import (
    compare_modular_interventions,
    contrast_radius,
    intervene_modular,
)


def fixture(d):
    rng = Random(310200 + d)
    return tuple(tuple(rng.choice((-1, 1)) for _ in range(d)) for _ in range(48))


@pytest.mark.parametrize("horizon", (1, 2))
@pytest.mark.parametrize("balanced", (True, False))
def test_intervention_observational_parity(horizon, balanced):
    args = (fixture(4), ((0, 1), (2, 3)), ((0, 2),), (3, 1), horizon)
    assert intervene_modular(*args, balanced=balanced) == predict_modular(*args, balanced=balanced)


def test_intervention_no_forced_update():
    history = ((-1, -1),) * 24
    rows = _prepare(history, ((0, 1), (0, 1)), (0, 1), False)
    p = _positive(rows[1], history[-1])
    expected = sum(w * _positive(rows[0], first) for first, w in _law((F(1), p)) if w)
    actual, _ = intervene_modular(history, ((0, 1),), (), (0,), 2, ((1, 0, 1),))
    assert dict(actual)[(2,)] == expected
    wrong = sum(
        w * _positive(rows[0], first, observed_prev=history[-1], child=0)
        for first, w in _law((F(1), p))
        if w
    )
    assert wrong != expected


def test_intervention_projection():
    history = fixture(4)
    modules = ((0, 1), (2, 3))
    ports = ((0, 2),)
    schedule = ((1, 0, 1), (2, 2, -1))
    full, _ = intervene_modular(history, modules, ports, (0, 1, 2, 3), 2, schedule)
    actual, closure = intervene_modular(history, modules, ports, (2,), 2, schedule)
    expected = {}
    for key, w in full:
        expected[(key[2],)] = expected.get((key[2],), F()) + w
    assert dict(actual) == expected and closure == (0, 2, 3)


@pytest.mark.parametrize("coupled", (False, True))
@pytest.mark.parametrize("balanced", (False, True))
def test_intervention_paired_reference(coupled, balanced):
    args = (fixture(4), ((0, 1), (2, 3)), ((0, 2), (3, 1)), (2,), 2)
    a = ((1, 0, -1),)
    b = ((1, 0, 1),)

    def prob(schedule):
        p, _ = intervene_modular(*args, schedule, balanced=balanced)
        return sum(w for k, w in p if k[0] >= 0)

    r = compare_modular_interventions(
        *args, (0,), a, b, samples=8192, seed=240101, coupled=coupled, balanced=balanced
    )
    pa, pb = prob(a), prob(b)
    assert abs(r.p_a - pa) < F(1, 25) and abs(r.p_b - pb) < F(1, 25)
    assert r.interval[0] <= pb - pa <= r.interval[1]
    assert not r.forecast_eligible and not r.action_authorized


def test_intervention_identical_schedule_and_forced_long():
    args = (
        fixture(12),
        ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)),
        ((0, 10),),
        (10,),
        12,
        (0,),
    )
    a = tuple((t, 10, -1) for t in range(1, 13))
    b = tuple((t, 10, 1) for t in range(1, 13))
    kw = {"samples": 128, "seed": 0}
    r = compare_modular_interventions(*args, a, b, **kw)
    assert r.contrast == 1 and r.sample_variance == 0
    assert r == compare_modular_interventions(*args, a, b, **kw)
    r = compare_modular_interventions(*args, a, a, **kw)
    assert r.contrast == r.sample_variance == 0


@pytest.mark.parametrize("n", (128, 512, 2048, 8192))
@pytest.mark.parametrize("alpha", (F(1, 100), F(1, 20), F(1, 10)))
def test_contrast_bound(n, alpha):
    r, k = contrast_radius(n, alpha)
    assert F(2, 2**k) <= alpha < F(2, 2 ** (k - 1))
    assert n * r * r >= 2 * k and n * (r - F(1, 10000)) ** 2 < 2 * k


@pytest.mark.parametrize(
    "schedule",
    [[], ((1, 0, 1), (1, 0, -1)), ((0, 0, 1),), ((3, 0, 1),), ((1, True, 1),), ((1, 0, 0),)],
)
def test_intervention_invalid(schedule):
    with pytest.raises(ValueError):
        intervene_modular(fixture(2), ((0, 1),), (), (0,), 2, schedule)
