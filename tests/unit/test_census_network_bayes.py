"""Persistent Bayes oracle and bounded input checks."""

from fractions import Fraction as F
from itertools import pairwise, product
from random import Random

import pytest

from mirrormind.domains.retail.census_network3 import STATES
from mirrormind.domains.retail.census_network_bayes import predict_persistent_bayes
from mirrormind.domains.retail.census_network_structure import (
    OPTIONS,
    parent_posterior,
    predict_parent_average,
)


def probabilities(pmf):
    total = sum(w for _, w in pmf)
    return {s: F(w, total) for s, w in pmf}


@pytest.mark.parametrize("length", (8, 24))
def test_persistent_bayes_one_step(length):
    rng = Random(71 + length)
    history = tuple(rng.choice(STATES) for _ in range(length))
    assert predict_persistent_bayes(history, 1) == predict_parent_average(history)
    assert predict_persistent_bayes(history, 1, frozen=True) == predict_parent_average(history)


@pytest.mark.parametrize("length", (8, 24))
def test_persistent_bayes_graph_oracle(length):
    rng = Random(72 + length)
    history = tuple(rng.choice(STATES) for _ in range(length))
    weights = parent_posterior(history)
    expected = {}
    for x, y in product(STATES, repeat=2):
        mass = F()
        for indices in product(range(4), repeat=3):
            w = F(1)
            for a, i in enumerate(indices):
                p = OPTIONS[i]
                w *= weights[a][i]
                for past, nxt in ((history, x), (history + (x,), y)):
                    context = None if p is None else past[-1][p]
                    seen = [
                        q[a] for r, q in pairwise(past) if (None if p is None else r[p]) == context
                    ]
                    w *= F(seen.count(nxt[a]) + 1, len(seen) + 2)
            mass += w
        key = tuple(a + b for a, b in zip(x, y, strict=True))
        expected[key] = expected.get(key, F()) + mass
    assert probabilities(predict_persistent_bayes(history, 2)) == expected


@pytest.mark.parametrize("length", (8, 24))
def test_persistent_bayes_canonical_three_steps(length):
    history = (STATES[0],) * length
    p = predict_persistent_bayes(history, 3)
    assert len(p) == 64
    assert sum(probabilities(p).values()) == 1
    assert all(w > 0 for _, w in p)
    assert p == tuple(sorted(p))
    assert p != predict_persistent_bayes(history, 3, frozen=True)


@pytest.mark.parametrize("h", (True, 0, 4, 1.0))
def test_persistent_bayes_bad_horizon(h):
    with pytest.raises(ValueError):
        predict_persistent_bayes((STATES[0],) * 8, h)


def test_persistent_bayes_bad_input():
    with pytest.raises(ValueError):
        predict_persistent_bayes(((True, 1, 1),) * 8, 1)
    with pytest.raises(ValueError):
        predict_persistent_bayes((STATES[0],) * 8, 1, frozen=1)
