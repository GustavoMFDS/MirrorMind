# Change request - bounded joint Markov propagation
Exact four-state paired sign process, with immutable transition matrices
and nonstationary schedules of one through six steps. Forecast cumulative
future displacements conditional on the last observed state. Integer
mass DP with LCM of row denominators, conservation and canonical
projection to existing JointPMF. All nested inputs validated before
arithmetic; no cache, arbitrary state count, fitted model, causal effect,
external data, API, persistence, dependency or deployment change.
Tests: brute-force Fraction path oracle, time-varying schedules, unequal
row totals, deterministic and zero transitions, bounds and type rejection.
Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Core | census_joint_markov.py | Exact bounded transition propagation |
| Tests | test_census_joint_markov.py | Enumeration and invalid input tests |
| API/storage | None | Existing probability contracts unchanged |
