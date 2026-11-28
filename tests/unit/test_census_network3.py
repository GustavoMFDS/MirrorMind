"""Independent enumeration and cross-engine exact parity."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from random import Random

import pytest

from mirrormind.domains.retail.census_network3 import (
    STATES,
    factor_matrix,
    propagate_lineages3,
    propagate_network3,
)

COPY = (((3, 1), (1, 3)),) * 3
OWN = ((0, 1, 2), COPY)
RING = ((2, 0, 1), COPY)
UNIFORM = ((1,) * 8,) * 8


def probs(pmf):
    total = sum(w for _, w in pmf)
    return {s: F(w, total) for s, w in pmf}


def oracle(start, schedule):
    result = defaultdict(F)
    for seq in product(STATES, repeat=len(schedule)):
        prev = start
        p = F(1)
        for matrix, nxt in zip(schedule, seq, strict=True):
            row = matrix[STATES.index(prev)]
            p *= F(row[STATES.index(nxt)], sum(row))
            prev = nxt
        if p:
            result[tuple(sum(s[a] for s in seq) for a in range(3))] += p
    return dict(result)


@pytest.mark.parametrize("h", range(1, 4))
def test_network3_enumeration(h):
    schedule = tuple(factor_matrix((OWN, RING)[i % 2]) for i in range(h))
    for start in STATES:
        assert probs(propagate_network3(start, schedule)) == oracle(start, schedule)


@pytest.mark.parametrize("h", range(1, 7))
def test_network3_lineage_parity(h):
    rng = Random(9000 + h)
    for _ in range(3):
        schedule = tuple(
            (
                rng.choice(((0, 1, 2), (2, 0, 1), (1, 2, 0))),
                tuple(
                    tuple((rng.randint(1, 25), rng.randint(0, 25)) for _ in range(2))
                    for _ in range(3)
                ),
            )
            for _ in range(h)
        )
        matrices = tuple(factor_matrix(step) for step in schedule)
        for start in STATES:
            assert propagate_lineages3(start, schedule) == propagate_network3(start, matrices)


def test_network3_deterministic_and_bounds():
    step = ((2, 0, 1), (((1, 0), (0, 1)),) * 3)
    assert propagate_lineages3((-1, 1, 1), (step,) * 6) == (((2, 2, 2), 1),)
    p = propagate_network3(STATES[0], (UNIFORM,) * 6)
    assert len(p) == 343
    assert sum(probs(p).values()) == 1
    assert tuple(sorted(p)) == p


@pytest.mark.parametrize("start", [(True, 1, 1), (1.0, 1, 1), [1, 1, 1], (1, 1), (0, 1, 1)])
def test_network3_invalid_start(start):
    with pytest.raises(ValueError):
        propagate_network3(start, (UNIFORM,))
    with pytest.raises(ValueError):
        propagate_lineages3(start, (OWN,))


@pytest.mark.parametrize(
    "schedule",
    [
        (),
        (UNIFORM,) * 7,
        [UNIFORM],
        (UNIFORM[:-1],),
        (((0,) * 8,) * 8,),
        (((True,) + (1,) * 7,) * 8,),
        (((15626,) + (1,) * 7,) * 8,),
    ],
)
def test_network3_invalid_matrix(schedule):
    with pytest.raises(ValueError):
        propagate_network3(STATES[0], schedule)


@pytest.mark.parametrize(
    "step",
    [
        [],
        None,
        ((0, 0, 1), COPY),
        ((True, 0, 2), COPY),
        ((0.0, 1, 2), COPY),
        ((0, 1, 2), (((0, 0), (1, 3)),) * 3),
        ((0, 1, 2), (((26, 1), (1, 3)),) * 3),
    ],
)
def test_network3_invalid_factor(step):
    with pytest.raises(ValueError):
        factor_matrix(step)
    with pytest.raises(ValueError):
        propagate_lineages3(STATES[0], (step,))
