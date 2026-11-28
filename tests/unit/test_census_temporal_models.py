"""Independent counting oracle and causal input boundary tests."""

from fractions import Fraction as F
from random import Random

import pytest

from mirrormind.domains.retail.census_joint_markov import STATES, propagate_joint_markov
from mirrormind.domains.retail.census_temporal_models import (
    TEMPORAL_MODELS,
    fit_temporal_models,
    predict_temporal_models,
)


def probabilities(row):
    return tuple(F(w, sum(row)) for w in row)


def test_temporal_estimators_direct_counting():
    rng = Random(54321)
    for _ in range(20):
        hist = tuple(rng.choice(STATES) for _ in range(24))
        matrices = fit_temporal_models(hist)
        assert tuple(matrices) == TEMPORAL_MODELS
        for i, previous in enumerate(STATES):
            for name, matrix in matrices.items():
                expected = []
                for nxt in STATES:
                    if name == "iid":
                        p = F(hist.count(nxt) + 1, 28)
                    elif name == "full":
                        seen = [hist[t + 1] for t in range(23) if hist[t] == previous]
                        p = F(seen.count(nxt) + 1, len(seen) + 4)
                    else:
                        p = F(1)
                        for axis in (0, 1):
                            source = 1 - axis if name == "cross" else axis
                            seen = [
                                hist[t + 1][axis]
                                for t in range(23)
                                if hist[t][source] == previous[source]
                            ]
                            p *= F(seen.count(nxt[axis]) + 1, len(seen) + 2)
                    expected.append(p)
                assert probabilities(matrix[i]) == tuple(expected)


def test_temporal_cross_orientation():
    # Both axes copy the other axis, on an alternating asymmetric path.
    history = ((-4, 4), (4, -4)) * 12
    matrices = fit_temporal_models(history)
    assert matrices["cross"][1][2] > matrices["cross"][1][1]
    assert matrices["cross"][2][1] > matrices["cross"][2][2]
    # With no symmetric contexts observed, the full conditional law is uniform.
    assert matrices["full"][0] == (1, 1, 1, 1)
    assert matrices["full"][3] == (1, 1, 1, 1)


def test_temporal_constant_history_and_missing_context():
    matrices = fit_temporal_models((STATES[0],) * 24)
    assert matrices["iid"][0] == (25, 1, 1, 1)
    assert matrices["full"][0] == (24, 1, 1, 1)
    assert matrices["full"][3] == matrices["own"][3] == matrices["cross"][3] == (1, 1, 1, 1)
    assert matrices["own"][0] == (576, 24, 24, 1)


@pytest.mark.parametrize("h", (1, 3, 6))
def test_temporal_forecast_propagation_and_future_invariance(h):
    rng = Random(21)
    path = tuple(rng.choice(STATES) for _ in range(64))
    altered = path[:53] + (STATES[0],) * 11
    history = path[29:53]
    p = predict_temporal_models(history, h)
    assert p == predict_temporal_models(altered[29:53], h)
    for m, matrix in fit_temporal_models(history).items():
        assert p[m] == propagate_joint_markov(history[-1], (matrix,) * h)


def test_temporal_fresh_results():
    history = (STATES[0],) * 24
    a = fit_temporal_models(history)
    a.clear()
    assert tuple(fit_temporal_models(history)) == TEMPORAL_MODELS


@pytest.mark.parametrize(
    "history",
    [
        (),
        (STATES[0],) * 23,
        (STATES[0],) * 25,
        [STATES[0]] * 24,
        ((True, 4),) * 24,
        ((4.0, 4),) * 24,
        ((0, 4),) * 24,
        ([4, 4],) * 24,
        ((4,),) * 24,
    ],
)
def test_temporal_invalid_history(history):
    with pytest.raises(ValueError):
        fit_temporal_models(history)


@pytest.mark.parametrize("h", (True, 1.0, 0, 2, 7))
def test_temporal_invalid_horizon(h):
    with pytest.raises(ValueError):
        predict_temporal_models((STATES[0],) * 24, h)
