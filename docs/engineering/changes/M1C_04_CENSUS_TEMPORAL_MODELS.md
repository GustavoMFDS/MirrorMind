# Change request - bounded paired temporal estimators
Fit four fixed candidate transition matrices from exactly 24 observed
paired sign states: smoothed empirical IID, own-axis, cross-axis and
full previous-pair. One pseudocount per outcome per conditional row.
Immutable matrices, deterministic candidate order, no target argument,
no scenario labels, no adaptive model selection. Conditional forecast
reuses the exact joint Markov core for horizons 1/3/6. Strict nested
type validation before counting; no public cache. Tests compare direct
counting oracles, orientation, unseen contexts, row totals, future
invariance and exact propagation. No external data, causal effects,
calibration, API, journal, or dependency change. Independent review
pending.

| Layer | Path | Impact |
|---|---|---|
| Core | census_temporal_models.py | Fixed estimators and forecast wrapper |
| Tests | test_census_temporal_models.py | Estimation and input contract |
| API/storage | None | Existing contracts unchanged |
