# Change request - fixed fictional temporal study
Versioned offline four-scenario study, 16 paths each, 10 origins,
three horizons. Reuse fixed temporal estimators and exact joint Markov
engine. Compare IID, own, cross, full, privileged oracle on identical
targets. Fixed SHA256 counter fixture, cross-to-own switch at index 53.
Exact joint Brier, reference excess, two marginal CRPS, event Brier
and probability, covariance. Design commitment before scoring,
canonical receipt replay and per-group transcript digests.
No new data, causal effects, selection, holdout, calibration, API,
journal, or dependency change. Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_temporal_study.py | Fixed temporal protocol |
| Tests | tests/integration/test_census_temporal_study.py | Replay and causal input |
| Core/API/storage | None | Existing contracts unchanged |
