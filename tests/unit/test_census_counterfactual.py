"""Independent finite exogenous oracle and structural ambiguity checks."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import pairwise, product
from math import prod
from random import Random

import pytest

from mirrormind.domains.retail.census_counterfactual import counterfactual, counterfactual_bounds

GRAPHS = (((), (), ()), ((0,), (1,), (2,)), ((2,), (0,), (1,)), ((1, 2), (0, 2), (0, 1)))
MECHANISMS = ("flip", "threshold")


def fixture():
    rng = Random(310300)
    return tuple(tuple(rng.choice((-1, 1)) for _ in range(3)) for _ in range(4))


def structural(prev, ps, u, mode):
    if not ps:
        return 1 if u < 2 else -1
    v = prod(prev[a] for a in ps)
    if mode == "flip":
        return v if u < 3 else -v
    return 1 if u < (3 if v == 1 else 1) else -1


@pytest.mark.parametrize("graph", GRAPHS)
@pytest.mark.parametrize("mode", MECHANISMS)
def test_counterfactual_factual_consistency(graph, mode):
    f = fixture()
    r = counterfactual(f, graph, (2, 0, 1), mechanism=mode)
    assert r.pmf == ((tuple(sum(s[a] for s in f[1:]) for a in (2, 0, 1)), F(1)),)
    assert r.factual_likelihood > 0
    assert not r.forecast_eligible and not r.action_authorized


@pytest.mark.parametrize("graph", GRAPHS)
@pytest.mark.parametrize("mode", MECHANISMS)
def test_counterfactual_exogenous_oracle(graph, mode):
    f = fixture()[:3]
    noise = tuple(
        tuple(u for u in range(4) if structural(prev, ps, u, mode) == nxt[a])
        for prev, nxt in pairwise(f)
        for a, ps in enumerate(graph)
    )
    mass = defaultdict(int)
    count = 0
    for draws in product(*noise):
        prev = f[0]
        totals = [0, 0]
        for t in (1, 2):
            nxt = tuple(
                1 if (t, a) == (1, 0) else structural(prev, ps, draws[(t - 1) * 3 + a], mode)
                for a, ps in enumerate(graph)
            )
            totals[0] += nxt[2]
            totals[1] += nxt[1]
            prev = nxt
        mass[tuple(totals)] += 1
        count += 1
    r = counterfactual(f, graph, (2, 1), ((1, 0, 1),), mechanism=mode)
    assert dict(r.pmf) == {k: F(v, count) for k, v in mass.items()}
    assert r.factual_likelihood == F(count, 4**6)


def test_counterfactual_nonidentification():
    f = ((-1, -1, -1),) * 3
    graph = GRAPHS[2]
    a = ((1, 0, -1),)
    b = ((1, 0, 1),)
    x = counterfactual(f, graph, (1,), b, mechanism="flip")
    y = counterfactual(f, graph, (1,), b, mechanism="threshold")
    assert x.factual_likelihood == y.factual_likelihood == F(3, 4) ** 6
    assert x.pmf == (((0,), F(1)),)
    assert y.pmf == (((-2,), F(1, 3)), ((0,), F(2, 3)))
    r = counterfactual_bounds(f, graph, (1,), (0,), a, b)
    assert (r.lower, r.upper, r.direction) == (F(2, 3), F(1), "positive")


@pytest.mark.parametrize("graph", GRAPHS)
def test_counterfactual_bounds_contain_endpoints(graph):
    f = fixture()
    a = ((1, 0, -1),)
    b = ((1, 0, 1),)
    r = counterfactual_bounds(f, graph, (1,), (0,), a, b)
    for i, mode in enumerate(MECHANISMS):
        p = counterfactual(f, graph, (1,), a, mechanism=mode)
        q = counterfactual(f, graph, (1,), b, mechanism=mode)
        v = sum(w for k, w in q.pmf if k[0] >= 0) - sum(w for k, w in p.pmf if k[0] >= 0)
        assert r.global_endpoints[i] == v and r.lower <= v <= r.upper
    assert r.vertices == 2 ** len(r.keys) <= 64
    assert not r.action_authorized
    zero = counterfactual_bounds(f, graph, (1,), (0,), b, b)
    assert zero.lower == zero.upper == 0 and zero.direction == "zero"


@pytest.mark.parametrize(
    "graph",
    [
        ((0,), (1,)),
        ((True,), (1,), (2,)),
        ((1, 0), (1,), (2,)),
        ((0, 0), (1,), (2,)),
        ((3,), (1,), (2,)),
    ],
)
def test_counterfactual_invalid_graph(graph):
    with pytest.raises(ValueError):
        counterfactual(fixture(), graph, (0,), mechanism="flip")


def test_counterfactual_invalid_inputs():
    with pytest.raises(ValueError):
        counterfactual(fixture(), GRAPHS[2], (True,), mechanism="flip")
    with pytest.raises(ValueError):
        counterfactual(fixture(), GRAPHS[2], (0,), ((4, 0, 1),), mechanism="flip")
    with pytest.raises(ValueError):
        counterfactual_bounds(fixture(), GRAPHS[2], (0,), (True,), (), ())
