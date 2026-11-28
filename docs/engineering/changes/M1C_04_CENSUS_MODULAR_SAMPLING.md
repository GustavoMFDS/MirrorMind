# Change request - bounded modular trajectory sampling and precision

Consolidate persistent posterior trajectory sampling and finite-look
event precision with the modular exact query's local priors and
scope validation. Explicit seed, bounded samples and horizon.
Incremental event counts, immutable typed results, explicit abstention.
No automatic fallback from exact queries, new dependencies, API,
storage, external data, calibrated forecasts or operational authority.

| Layer | Path | Impact |
|---|---|---|
| Core | census_modular_sampling.py | Empirical subset PMF and event precision |
| Tests | test_census_modular_sampling.py | Exact reference, nested replay and bound checks |
| API/storage | None | Existing contracts unchanged |

Independent review pending.
