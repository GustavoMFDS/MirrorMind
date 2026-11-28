# Change request - bounded local parent learning

Exact integrated Bernoulli evidence for four parent choices per
child, uniform structure priors and Beta(1,1) context priors. Fixed
MAP and conservative candidate graphs, smoothed matrix fitting,
one-step posterior predictive and uniform parent averaging.
Eight or 24 observed binary triples. Shared parents permitted in
joint matrices, no causal identification or multistep Bayesian
integration. Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Core | census_network_structure.py | Exact local structure estimators |
| Tests | test_census_network_structure.py | Sequential evidence and 64-graph mixture |
| API/storage | None | Existing contracts unchanged |
