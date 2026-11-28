# Change request - bounded exact discrete probability primitives

## Scope and acceptance
Separate experimental pure mathematical module for finite integer-valued
increment distributions, with canonical positive integer weights and
explicit support/weight/horizon bounds. Exact inverse CDF, central
10/90 quantiles, CRPS, mean pinball, median absolute error, inclusive
coverage, interval width and expected coverage under an explicitly
supplied reference distribution. Independent increment convolution and
bounded finite-state first-order Markov propagation using integer dynamic
programming. No learned models, adaptive policy, external data, API,
journal admission, inference or calibration claim. No new dependencies.
Test malformed inputs, exact brute-force scoring and Markov enumeration,
discreteness and mass conservation. Existing protocols unchanged.

| Layer | Path | Impact |
|---|---|---|
| Core | census_probability.py | Pure bounded probability primitives |
| Tests | test_census_probability.py | Exact oracles and rejection |
| API / persistence | None | No external behavior change |

This is a finite discrete research contract, not a general distribution
library. Supports integer increments only. A supplied reference law is
not verified as truth. No empirical evidence, historical attestation or
independent trust. Independent review pending.
