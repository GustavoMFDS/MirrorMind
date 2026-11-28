# Change request - fictional five-model validation comparison

## Acceptance
Separate versioned pure contract for five fixed models, validation only.
Use existing frozen schedule and legacy eligible pairs, with an additional
13th consecutive visible month required for all five. Exact Fraction
forecasts/losses, nonnegative drift and OLS extrapolation; no tuning.
Bind method version, declared revision, input manifest and schedule before
scoring; compare complete canonical receipt on explicit replay. Legacy
loss parity per matched pair. First-estimate labels and strict cutoff.
At least two common observations per horizon for MAE; report coverage
and extra-history abstentions. No winner, intervals, empirical claims,
new journal admission, API, dependencies, holdout execution or authority.
Add fixed validation break example and regressions; preserve old schemas.
Independent review pending. Caller-supplied records are not authenticated;
receipts are value-bearing and restricted to fictional use.

| Layer | Path | Impact |
|---|---|---|
| Core | census_models.py | Pure prediction, committed comparison and replay |
| Example | examples/m1_census_model_comparison.py | Fixed validation catalog and break |
| Tests | tests/unit/test_census_models.py | Exact oracle, parity, temporal and replay tests |

No real sources, changes to split boundaries, or changes to B-01/B-02.
