# Change request - bounded modular mechanism replacement

Consolidate exact interventions and paired trajectory contrasts under the
existing modular graph and parameter priors. Explicit schedules replace
local mechanisms without updating their evidence or urns. Shared draws
preserve each marginal law; no individual counterfactual identification.
No new API, storage, external data, dependency, promotion or authority.

| Layer | Path | Impact |
|---|---|---|
| Core | census_modular_interventions.py | Exact intervention PMF and paired event contrast |
| Tests | test_census_modular_interventions.py | Parity, forced updates, projection, paired reference, bounds |
| API/storage | None | Existing contracts unchanged |

Independent review pending.
