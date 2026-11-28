# Change request - exact bounded bivariate probability core
Pure experimental finite joint PMFs on integer increments, two axes only.
Canonical positive integer weights, sorted distinct support and explicit
mass, increment and horizon bounds. Independent-in-time convolution,
marginal projection, product of marginals, exact covariance, joint
multiclass Brier and supplied-reference expected Brier excess, joint
positive event probability. No fitted model, adaptation, causal
inference, API, storage, new dependency or external data. Existing
univariate contracts unchanged. Tests use enumeration and exact scoring
oracles, marginal preservation, dependence blindness and invalid inputs.
Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Core | census_bivariate.py | Bounded exact joint distributions |
| Tests | test_census_bivariate.py | Mathematical and rejection tests |
| API/storage | None | No external change |
