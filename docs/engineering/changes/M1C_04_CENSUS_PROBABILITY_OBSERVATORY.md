# Change request - fictional probability observatory
Generate offline HTML from freshly executed and fully replayed fixed study.
Show all group/horizon metrics, exact rational values and provenance;
distinguish observed from supplied-reference coverage. Display fixed
path 0, origin 52, horizon 6 example PMFs for both scenarios and all
methods, with quantiles, realized displacement and score. Example
selection fixed, no cherry-picking or arbitrary input. Explicit oracle
label, no calibration, winner, holdout, trust or operational claim.
Exclusive absolute HTML output; no network, scripts or new dependency.
Tests cover actual metrics, deterministic HTML, replay failure and
exclusive output. Existing protocol and receipt bytes unchanged.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_probability_observatory.py | Offline report |
| Tests | tests/integration/test_census_probability_observatory.py | Report regressions |
| Core/API/storage | None | Reuse existing study and probability core |

Independent review pending; markup checks do not certify accessibility.
