# Forecast model card template — reproducible evaluation, not marketing

> Create one reviewed card per **model revision and dataset snapshot**.
> Required before claiming that MirrorMind can forecast a metric.
> A model card is documentation; passing this checklist alone does
> not establish predictive quality or production safety.

## 1. Target, version and provenance

- Model ID, release/version, code commit and reviewer:
- Intended users and **out-of-scope uses**:
- Predicted variable, units, granularity and forecast horizon:
- Input snapshot and [dataset card](DATASET_CARD_TEMPLATE.md) ID/hash:
- Prediction cutoff and data availability rule:
- Source license and approved processing purpose:
- Target proxy caveat (e.g. **sales are not latent demand**):

## 2. Temporal evaluation design

- Historical time windows and series/entity grouping:
- Train cutoff(s) and rolling-origin validation windows:
- Untouched final holdout range and lock date:
- Feature computation limited to data **available at each origin**:
- Missing date/zero/null policy (no silent fabrication):
- Cold-start and unseen entity evaluation:
- Revisions, late-published data and lookahead adversarial test:

Choose and justify baselines *before* complex models.
For daily retail counts, a **seasonal-naive lag-7**
baseline may be reasonable when seven historical days
are available; evaluate it honestly on the same test
windows as a second, independently specified model.

## 3. Metrics and uncertainty

| Evaluation field | Definition/decision | Caveat |
| --- | --- | --- |
| MAE | Mean absolute error on aligned held-out targets | Unit-dependent; misses risk of extreme errors |
| RMSE | Root mean square error | Sensitive to outliers and high-volume series |
| WAPE | Sum absolute errors / sum absolute observed values | Undefined for zero denominator; define an explicit policy |
| Bias | Mean signed prediction error | Can hide cancellation across entities |
| Coverage | Empirical fraction inside stated prediction interval | Needs interval-generation method and per-horizon evaluation |
| Calibration | Reliability across horizons/series | A nominal interval is **not** guaranteed coverage |
| Compute | Runtime, resource and model-call/token budget | Must be measured, not merely declared |

- Per-series and aggregate scores with sample sizes:
- Naive baseline versus candidate, with paired time-window comparison:
- Uncertainty method and observed coverage/calibration:
- Comparison under zeros, gaps, shocks and distribution shift:
- Confidence bounds on differences, if justified:
- Reproducibility settings, seeds and library versions:

No single metric proves business value. Avoid declaring
one model "better" without a predeclared criterion,
statistically meaningful held-out comparison and
reported limitations.

## 4. Leakage and adverse-case tests

- [ ] Future observation not visible at older origin.
- [ ] Late publication/revision does not leak backwards.
- [ ] Target series cannot be reused as future feature.
- [ ] Missing days stay missing until explicitly modeled.
- [ ] Zero-denominator WAPE is handled and reported.
- [ ] Inference rejects unsupported horizon or schema version.
- [ ] Uncertainty claims correspond to observed calibration.
- [ ] Fallback behavior is defined for unseen series/insufficient history.
- [ ] No unauthorized input is sent to a model or external service.

Exact test selectors, environment and actual status:
- Known limitations, failure modes and expected drift:
- Human reviewer, approval and next re-evaluation date:

## 5. Decision-use boundary

A forecast is a **conditional model estimate**, not a
recorded fact, real inventory count or causal effect.
When a forecast is consumed by the simulation gateway,
record its version, cutoff, uncertainty representation,
source snapshot and assumptions. Keep approval of any
real business action separate from running the model.

See [the capability truth gates](CAPABILITY_GATES.md),
[M1 delivery plan](M1_EXECUTION_PLAN.md),
and [decision trace template](DECISION_TRACE_TEMPLATE.md).
