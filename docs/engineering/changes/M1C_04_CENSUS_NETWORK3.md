# Change request - bounded three-axis propagation

Exact conditional cumulative distributions for three binary sign states.
Two explicit engines: general eight-state joint Markov schedules and
bijective-parent factorized schedules with conditionally independent
innovations. One to six steps, immutable bounded inputs and canonical
integer output. No automatic dispatch, graph learning, causal claim,
API, persistence, external data or new dependency. Independent review
pending. Tests use rational path enumeration and cross-engine parity.

| Layer | Path | Impact |
|---|---|---|
| Core | census_network3.py | Bounded joint and lineage propagation |
| Tests | test_census_network3.py | Enumeration, parity and rejection |
| API/storage | None | Existing contracts unchanged |
