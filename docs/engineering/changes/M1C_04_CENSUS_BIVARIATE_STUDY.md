# Change request - fixed fictional bivariate study
Versioned offline study of four fixed generator designs, one deterministic
seed each, 16 paths per group, ten origins and three horizons. Compare
fixed independent, smoothed last24 joint and its matched independent
projection, and privileged oracle. Exact marginal CRPS, joint Brier,
reference excess, simultaneous-positive event Brier/probability and
covariance. Bind fixed design and declared revision before scoring.
Streaming event transcript digests, complete canonical replay, bounded
receipt. No arbitrary inputs, fitted operational model, holdout,
calibration, causal inference, API, journal or new dependencies.
Independent review pending. Existing protocols unchanged.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_bivariate_study.py | Fixed study and replay |
| Tests | tests/integration/test_census_bivariate_study.py | Matched marginals, causal input, forgery rejection |
| Core/API/storage | None | Reuse existing mathematical core |
