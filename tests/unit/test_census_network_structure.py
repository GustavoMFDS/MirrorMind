"""Independent sequential evidence and complete graph-mixture oracle."""

from fractions import Fraction as F
from itertools import pairwise, product
from random import Random

import pytest

from mirrormind.domains.retail.census_network3 import STATES, propagate_network3
from mirrormind.domains.retail.census_network_structure import (
    OPTIONS,
    fit_parent_matrix,
    parent_posterior,
    predict_parent_average,
    select_parent_graphs,
)


def probabilities(pmf):
    total = sum(w for _, w in pmf)
    return {s: F(w, total) for s, w in pmf}


@pytest.mark.parametrize("length", (8, 24))
def test_parent_posterior_sequential_evidence(length):
    rng = Random(421 + length)
    for _ in range(8):
        history = tuple(rng.choice(STATES) for _ in range(length))
        rows = parent_posterior(history)
        for child, row in enumerate(rows):
            expected = []
            for parent in OPTIONS:
                counts = {}
                p = F(1)
                for prev, nxt in pairwise(history):
                    context = None if parent is None else prev[parent]
                    c = counts.setdefault(context, {-1: 1, 1: 1})
                    p *= F(c[nxt[child]], sum(c.values()))
                    c[nxt[child]] += 1
                expected.append(p)
            assert row == tuple(v / sum(expected) for v in expected)


@pytest.mark.parametrize("uniform", (False, True))
@pytest.mark.parametrize("length", (8, 24))
def test_parent_average_complete_graph_mixture(length, uniform):
    rng = Random(999 + length)
    history = tuple(rng.choice(STATES) for _ in range(length))
    weights = ((F(1, 4),) * 4,) * 3 if uniform else parent_posterior(history)
    expected = {s: F() for s in STATES}
    for a, b, c in product(range(4), repeat=3):
        graph = (OPTIONS[a], OPTIONS[b], OPTIONS[c])
        weight = weights[0][a] * weights[1][b] * weights[2][c]
        p = probabilities(propagate_network3(history[-1], (fit_parent_matrix(history, graph),)))
        for s, v in p.items():
            expected[s] += weight * v
    actual = probabilities(predict_parent_average(history, uniform=uniform))
    assert actual == expected
    assert sum(actual.values()) == 1


def test_parent_tie_and_constant_history():
    h = (STATES[0],) * 24
    assert parent_posterior(h) == ((F(1, 4),) * 4,) * 3
    assert select_parent_graphs(h) == ((None,) * 3, (None,) * 3)


def test_parent_shared_and_missing_context():
    h = (STATES[0],) * 24
    p = fit_parent_matrix(h, (0, 0, 0))
    assert p[0][0] == 24**3
    assert p[7] == (1,) * 8
    assert sum(probabilities(propagate_network3(h[-1], (p,) * 3)).values()) == 1


@pytest.mark.parametrize(
    "history",
    [
        (),
        (STATES[0],) * 7,
        (STATES[0],) * 25,
        [STATES[0]] * 8,
        ((True, 1, 1),) * 8,
        ((1.0, 1, 1),) * 8,
        ([1, 1, 1],) * 8,
    ],
)
def test_parent_invalid_history(history):
    for fn in (parent_posterior, select_parent_graphs, predict_parent_average):
        with pytest.raises(ValueError):
            fn(history)


@pytest.mark.parametrize("graph", [(True, 0, 1), (0.0, 1, 2), (3, 0, 1), [0, 1, 2], (0, 1)])
def test_parent_invalid_graph(graph):
    with pytest.raises(ValueError):
        fit_parent_matrix((STATES[0],) * 8, graph)


def test_parent_invalid_average_mode():
    with pytest.raises(ValueError):
        predict_parent_average((STATES[0],) * 8, uniform=1)
