"""Independent exact oracle for bounded paired-state propagation."""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from random import Random

import pytest

from mirrormind.domains.retail.census_joint_markov import (
    STATES,
    propagate_joint_markov,
)

UNIFORM = ((1, 1, 1, 1),) * 4
IDENTITY = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
FLIP = tuple(tuple(int(i + j == 3) for j in range(4)) for i in range(4))
ASYMMETRIC = ((1, 2, 3, 4), (4, 0, 1, 2), (0, 1, 2, 0), (7, 1, 0, 1))


def oracle(start, schedule):
    result = defaultdict(F)
    for seq in product(STATES, repeat=len(schedule)):
        weight = F(1)
        prev = start
        for matrix, nxt in zip(schedule, seq, strict=True):
            row = matrix[STATES.index(prev)]
            weight *= F(row[STATES.index(nxt)], sum(row))
            prev = nxt
        if weight:
            result[sum(x for x, _ in seq), sum(y for _, y in seq)] += weight
    return dict(result)


def probabilities(pmf):
    total = sum(w for _, _, w in pmf)
    return {(x, y): F(w, total) for x, y, w in pmf}


@pytest.mark.parametrize("h", range(1, 7))
def test_joint_markov_enumeration(h):
    schedule = tuple((ASYMMETRIC, FLIP, UNIFORM)[i % 3] for i in range(h))
    for start in STATES:
        actual = probabilities(propagate_joint_markov(start, schedule))
        assert actual == oracle(start, schedule)
        assert sum(actual.values()) == 1


def test_deterministic_state_sum_excludes_start():
    assert propagate_joint_markov((-4, 4), (IDENTITY,) * 6) == ((-24, 24, 1),)
    assert propagate_joint_markov((-4, 4), (FLIP, IDENTITY)) == ((8, -8, 1),)
    assert propagate_joint_markov((-4, 4), (FLIP, FLIP)) == ((0, 0, 1),)


def test_rows_scale_independently():
    scaled = tuple(tuple(w * (i + 1) for w in row) for i, row in enumerate(ASYMMETRIC))
    assert propagate_joint_markov(STATES[0], (scaled,) * 3) == propagate_joint_markov(
        STATES[0], (ASYMMETRIC,) * 3
    )


def test_random_unequal_row_totals():
    rng = Random(12345)
    for _ in range(12):
        schedule = tuple(
            tuple(tuple(rng.randint(1, 1024) for _ in STATES) for _ in STATES) for _ in range(3)
        )
        for state in STATES:
            assert probabilities(propagate_joint_markov(state, schedule)) == oracle(state, schedule)


@pytest.mark.parametrize("start", [(True, 4), (4.0, 4), [4, 4], (0, 4), (4,)])
def test_invalid_start(start):
    with pytest.raises(ValueError):
        propagate_joint_markov(start, (UNIFORM,))


@pytest.mark.parametrize(
    "schedule",
    [
        (),
        (UNIFORM,) * 7,
        [UNIFORM],
        (UNIFORM[:-1],),
        (((0, 0, 0, 0),) * 4,),
        (((True, 1, 1, 1),) * 4,),
        (((1.0, 1, 1, 1),) * 4,),
        (((-1, 1, 1, 1),) * 4,),
        (((1025, 1, 1, 1),) * 4,),
        (((1, 1, 1),) * 4,),
        (([1, 1, 1, 1],) * 4,),
    ],
)
def test_invalid_schedule(schedule):
    with pytest.raises(ValueError):
        propagate_joint_markov(STATES[0], schedule)


def test_maximum_weight_schedule_and_canonical_output():
    rows = (
        (1024, 1023, 1021, 1019),
        (1024, 1024, 1024, 1023),
        (1024, 1023, 1024, 1022),
        (1021, 1022, 1023, 1024),
    )
    p = propagate_joint_markov(STATES[0], (rows,) * 6)
    assert len(p) == 49
    assert sum(probabilities(p).values()) == 1
    assert probabilities(p) == oracle(STATES[0], (rows,) * 6)
