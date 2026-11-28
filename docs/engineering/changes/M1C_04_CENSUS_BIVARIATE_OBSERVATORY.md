# Change request - offline bivariate observatory
Render the fixed bivariate study only after complete replay. Display
all scenario/horizon metrics, exact fractions, provenance and
fixed path 0 origin 52 horizon 6 joint examples. Heatmap tables with
explicit row/column axes and text probabilities, exact marginal tables,
covariance and simultaneous-positive probability. No imported report,
network, scripts, overwrite, API, storage, fitted operational model or
calibration claim. Reuse existing report styling. Test output, replay
failure, exact probabilities and exclusive output; browser smoke is
not accessibility certification. Independent review pending.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_bivariate_observatory.py | Offline visualization |
| Tests | tests/integration/test_census_bivariate_observatory.py | Report and failure regressions |
| Core | None | Existing exact contracts unchanged |
