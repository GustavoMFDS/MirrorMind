# Change request - persistent Bayesian engine and fixed study

Integrate persistent graph and binary parameter uncertainty over
hypothetical future paths, 8 or 24 observations and 1..3 steps.
Frozen posterior-mean control. Exact rational computation and bounded
canonical integer PMFs. Fixed fictional four-scenario study with
local commitment and replay, reusing exploratory fixtures.
No real data, calibrated inference, causal claim, new dependency,
API, storage, or automatic promotion. Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Core | census_network_bayes.py | Exact persistent and frozen predictions |
| Example | m1_census_network_bayes_study.py | Fixed commitment and replay |
| Tests | test_census_network_bayes.py; test_census_network_bayes_study.py | Explicit graph oracle, replay and input rejection |
| API/storage | None | Existing contracts unchanged |
