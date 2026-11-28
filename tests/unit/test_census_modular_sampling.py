"""Bounded modular sampling and precision checks."""

from dataclasses import FrozenInstanceError
from fractions import Fraction as F
from random import Random

import pytest

from mirrormind.domains.retail.census_modular import predict_modular
from mirrormind.domains.retail.census_modular_sampling import (
    LOOKS,
    estimate_modular_events,
    event_radius,
    sample_modular,
)


def fixture(d):
    rng = Random(310100 + d)
    return tuple(tuple(rng.choice((-1, 1)) for _ in range(d)) for _ in range(48))


def event(pmf, thresholds):
    return sum((v for s, v in pmf if all(x >= t for x, t in zip(s, thresholds, strict=True))), F())


@pytest.mark.parametrize("balanced", (False, True))
@pytest.mark.parametrize("horizon", (1, 2))
def test_sampling_exact_reference(balanced, horizon):
    history = fixture(4)
    modules = ((0, 1), (2, 3))
    ports = ((0, 2), (3, 1))
    axes = (2, 1)
    exact, _ = predict_modular(history, modules, ports, axes, horizon, balanced=balanced)
    sample = sample_modular(
        history, modules, ports, axes, horizon, samples=8192, seed=310101, balanced=balanced
    )
    a, b = dict(exact), dict(sample)
    assert sum(abs(a.get(k, F()) - b.get(k, F())) for k in a.keys() | b.keys()) / 2 < F(1, 20)


def test_sampling_replay_and_projection():
    history = fixture(6)
    modules = ((0, 1, 2), (3, 4, 5))
    ports = ((0, 3),)
    args = (history, modules, ports)
    kw = {"samples": 512, "seed": 42}
    p = sample_modular(*args, (0, 1, 3, 5), 6, **kw)
    assert p == sample_modular(*args, (0, 1, 3, 5), 6, **kw)
    expected = {}
    for k, v in p:
        key = (k[3], k[0])
        expected[key] = expected.get(key, F()) + v
    assert dict(sample_modular(*args, (5, 0), 6, **kw)) == expected


def test_sampling_twelve_axis_long_horizon():
    history = fixture(12)
    modules = tuple(tuple(range(a, a + 3)) for a in range(0, 12, 3))
    p = sample_modular(
        history, modules, ((0, 10), (3, 10), (6, 10)), (10, 2), 12, samples=512, seed=42
    )
    assert sum(v for _, v in p) == 1
    assert all(all(-12 <= x <= 12 and x % 2 == 0 for x in k) for k, _ in p)


@pytest.mark.parametrize("m", range(1, 5))
@pytest.mark.parametrize("alpha", (F(1, 100), F(1, 20), F(1, 10)))
def test_sampling_conservative_radius(m, alpha):
    for n in LOOKS:
        r, k = event_radius(n, m, alpha)
        assert F(2 * m * len(LOOKS), 2**k) <= alpha
        assert F(2 * m * len(LOOKS), 2 ** (k - 1)) > alpha
        assert 2 * n * r * r >= k
        assert 2 * n * (r - F(1, 10000)) ** 2 < k


@pytest.mark.parametrize(
    "tolerance,status,final",
    [
        (F(1, 10), "precision_met", 512),
        (F(1, 20), "precision_met", 2048),
        (F(1, 40), "precision_met", 8192),
        (F(1, 100), "abstained", 8192),
    ],
)
def test_sampling_streamed_looks(tolerance, status, final):
    args = (fixture(3), ((0, 1, 2),), (), (0, 1), 2)
    events = ((0, 0), (2, 2), (-2, 2))
    r = estimate_modular_events(*args, events, tolerance=tolerance, alpha=F(1, 20), seed=42)
    assert r.status == status and r.attempts[-1].samples == final
    assert not r.forecast_eligible and not r.action_authorized
    for look in r.attempts:
        p = sample_modular(*args, samples=look.samples, seed=42)
        assert look.estimates == tuple(event(p, e) for e in events)
        assert all(
            0 <= lo <= v <= hi <= 1
            for v, (lo, hi) in zip(look.estimates, look.intervals, strict=True)
        )
    with pytest.raises(FrozenInstanceError):
        r.status = "changed"


@pytest.mark.parametrize(
    "samples,seed,horizon",
    [
        (True, 0, 1),
        (127, 0, 1),
        (8193, 0, 1),
        (128, True, 1),
        (128, -1, 1),
        (128, 2**32, 1),
        (128, 0, 13),
    ],
)
def test_sampling_invalid(samples, seed, horizon):
    with pytest.raises(ValueError):
        sample_modular(fixture(2), ((0, 1),), (), (0,), horizon, samples=samples, seed=seed)


@pytest.mark.parametrize("events", [(), ((0,), (0,)), ((True,),), ((3,),), ((0, 1),), [(0,)]])
def test_sampling_invalid_events(events):
    with pytest.raises(ValueError):
        estimate_modular_events(
            fixture(2), ((0, 1),), (), (0,), 2, events, tolerance=F(1, 20), alpha=F(1, 20), seed=0
        )
