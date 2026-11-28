"""Independent exact and bounded contract checks for modular predictions."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import pairwise, product
from random import Random

import pytest

from mirrormind.domains.retail.census_modular import predict_modular


def fixture(d, length=48):
    rng = Random(310000 + d + length)
    return tuple(tuple(rng.choice((-1, 1)) for _ in range(d)) for _ in range(length))


@pytest.mark.parametrize("balanced", (False, True))
@pytest.mark.parametrize("length", (24, 48))
def test_modular_graph_oracle(balanced, length):
    history = fixture(2, length)
    opts = ((), (0,), (1,), (0, 1))
    states = tuple(product((-1, 1), repeat=2))
    weights = []
    for child in range(2):
        evidence = []
        for parents in opts:
            counts = {}
            w = F(1, 3 * (2 if len(parents) == 1 else 1)) if balanced else F(1, 4)
            for prev, nxt in pairwise(history):
                ctx = tuple(prev[p] for p in parents)
                row = counts.setdefault(ctx, {-1: 1, 1: 1})
                w *= F(row[nxt[child]], sum(row.values()))
                row[nxt[child]] += 1
            evidence.append(w)
        weights.append(tuple(v / sum(evidence) for v in evidence))
    expected = defaultdict(F)
    for x, y in product(states, repeat=2):
        for i, j in product(range(4), repeat=2):
            mass = weights[0][i] * weights[1][j]
            for a, k in enumerate((i, j)):
                parents = opts[k]
                for prefix, target in ((history, x), (history + (x,), y)):
                    ctx = tuple(prefix[-1][p] for p in parents)
                    seen = [
                        v[a] for u, v in pairwise(prefix) if tuple(u[p] for p in parents) == ctx
                    ]
                    mass *= F(seen.count(target[a]) + 1, len(seen) + 2)
            expected[(x[1] + y[1], x[0] + y[0])] += mass
    result, closure = predict_modular(history, ((0, 1),), (), (1, 0), 2, balanced=balanced)
    assert dict(result) == expected
    assert closure == (0, 1)


@pytest.mark.parametrize("horizon", (1, 2))
@pytest.mark.parametrize("balanced", (False, True))
def test_modular_disconnected_product(horizon, balanced):
    history = fixture(6)
    p, _ = predict_modular(
        tuple(s[:3] for s in history), ((0, 1, 2),), (), (1,), horizon, balanced=balanced
    )
    q, _ = predict_modular(
        tuple(s[3:] for s in history), ((0, 1, 2),), (), (2,), horizon, balanced=balanced
    )
    result, _ = predict_modular(
        history, ((0, 1, 2), (3, 4, 5)), (), (1, 5), horizon, balanced=balanced
    )
    assert result == tuple(((x[0], y[0]), a * b) for (x, a), (y, b) in product(p, q))


@pytest.mark.parametrize("horizon", (1, 2))
def test_modular_projection_and_port_orientation(horizon):
    history = fixture(4)
    modules = ((0, 1), (2, 3))
    ports = ((0, 2),)
    full, _ = predict_modular(history, modules, ports, (0, 1, 2, 3), horizon)
    actual, closure = predict_modular(history, modules, ports, (2,), horizon)
    expected = defaultdict(F)
    for key, p in full:
        expected[(key[2],)] += p
    assert dict(actual) == expected
    assert closure == ((2,) if horizon == 1 else (0, 2, 3))
    _, reverse = predict_modular(history, modules, ((2, 0),), (2,), horizon)
    assert reverse == ((2,) if horizon == 1 else (2, 3))


def test_modular_twelve_axis_exact_closure():
    history = fixture(12)
    modules = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11))
    result, closure = predict_modular(history, modules, (), (10,), 2)
    expected, _ = predict_modular(tuple(s[9:] for s in history), ((0, 1, 2),), (), (1,), 2)
    assert result == expected and closure == (9, 10, 11)
    with pytest.raises(ValueError, match="closure"):
        predict_modular(history, modules, (), (0, 3, 6), 2)


def test_modular_singleton_balanced_prior():
    history = fixture(2)
    p, _ = predict_modular(history, ((0,), (1,)), (), (0, 1), 2)
    q, _ = predict_modular(history, ((0,), (1,)), (), (0, 1), 2, balanced=True)
    assert p == q and sum(v for _, v in p) == 1


@pytest.mark.parametrize(
    "modules,ports,axes,horizon",
    [
        (((0, 1), (1, 2)), (), (0,), 2),
        (((0,), (1,)), (), (0,), 2),
        (((0, 1), (2,)), ((0, 1),), (2,), 2),
        (((0, 1), (2,)), ((0, 2), (0, 2)), (2,), 2),
        (((0, 1), (2,)), ((True, 2),), (2,), 2),
        (((0, 1), (2,)), (), (True,), 2),
        (((0, 1), (2,)), (), (2,), 3),
        (((0, 1), (2,)), (), (2, 2), 2),
        (((0, 1), (2,)), (), (2,), True),
    ],
)
def test_modular_invalid(modules, ports, axes, horizon):
    with pytest.raises(ValueError):
        predict_modular(fixture(3), modules, ports, axes, horizon)


def test_modular_invalid_history_and_prior():
    with pytest.raises(ValueError):
        predict_modular(((True, 1),) * 24, ((0, 1),), (), (0,), 1)
    with pytest.raises(ValueError):
        predict_modular(fixture(2), ((0, 1),), (), (0,), 1, balanced=1)
