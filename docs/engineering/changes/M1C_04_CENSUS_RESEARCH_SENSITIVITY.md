# Change request - bounded fictional sensitivity grid

## Scope and acceptance
A separate local example evaluates one-factor-at-a-time perturbations of
a shared 80-month fictional seasonal base. Fixed trend, deterministic
volatility amplitude and level shift magnitude grids, five values each.
Zero is a common baseline, reused rather than counted as independent
replication. Precompute all 13 distinct commitments before scoring.
Identical temporal schedule, release timing and baseline methods across
cells. Synthetic snapshot identifiers bind generated month/value, not
source bytes. Evaluate explicitly selected split (validation default),
admit and replay each receipt through temporary journal. Report per-axis,
level and horizon MAE, exact paired mean difference, matched counts,
coverage and receipt/manifest identity. No pooling, winner, p-values,
intervals, optimization or stochastic independence. Deterministic JSON,
optional exclusive offline HTML. No external input, API, persistent
schema, dependencies, source data or new trust.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_research_sensitivity.py | Fixed grid, local replay and report |
| Tests | tests/integration/test_census_research_sensitivity.py | Grid, identity, exact loss and failure regressions |
| Core / API | None | Existing contract reused |

Existing fictional cards apply; B-01/B-02 remain open. Independent review
pending. Designed sensitivity is not generalization or inferential evidence.
