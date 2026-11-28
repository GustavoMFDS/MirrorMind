# Change request - offline temporal observatory

Render the fixed temporal study after exact replay. Reuse bivariate
visualization helpers for joint and marginal distributions. Add explicit
conditional transition tables, fitted stationary matrices and each
privileged oracle step. Fixed path 0, origin 52, horizon six.
No imported reports, network, scripts, overwrite, new dependencies,
API or storage. Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_temporal_observatory.py | Offline temporal visualization |
| Tests | tests/integration/test_census_temporal_observatory.py | Exact row masses and replay/failure tests |
| Core | None | Existing mathematical contracts unchanged |
