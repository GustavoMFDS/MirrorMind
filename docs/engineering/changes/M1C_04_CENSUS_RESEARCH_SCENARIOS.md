# Change request - bounded fictional scenario library

## Scope and acceptance
Expand the existing runner with a closed set of deterministic fictional
fixtures: original trend/seasonality, flat level, volatile level, abrupt
regime shift. Keep default fixture, normalized records, fingerprints and
previous CLI output unchanged. Each added scenario uses the same 80-month
schedule, fictional series identity and distinct normalized values.
The scenario choice is bound by the normalized manifest; cross-scenario
commitment reuse rejects before database creation. No random seeds,
arbitrary generator parameters, external files, real data or new models.
Both runner and local observatory accept a scenario choice, defaulting to
the original. Show actual scenario name; no metric pooling, selection or
statistical winner. Add deterministic replay, scenario mismatch, unchanged
default and HTML labeling tests. Existing limits and abstention remain.
No API, dependency, persistence schema or authority changes.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_research_runner.py | Closed fictional fixture catalog and scenario selection |
| Example | examples/m1_census_research_observatory.py | Scenario selection and label |
| Tests | tests/integration/test_census_research_scenarios.py | Synthetic identity and replay regressions |

Independent review pending. Source-only rollback; no removal of user files.
Existing fictional cards apply. B-01/B-02 remain open.
