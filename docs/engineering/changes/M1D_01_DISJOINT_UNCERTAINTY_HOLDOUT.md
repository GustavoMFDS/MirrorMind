# Change request — Disjoint calibration and holdout targets

## 1. Goal in plain language

**Baseline behavior:** `evaluate_retail_residual_envelopes` evaluated a
prequential one-day holdout and recomputed a trailing residual window at each
origin. Consequently, a target from an earlier holdout origin can become a
calibration residual for a later holdout origin after its release.

**Desired behavior:** freeze a calendar calibration-target window strictly
before the first holdout target. Keep the existing as-of publication checks
and candidate-specific feature origins, but never allow any holdout target to
enter calibration during that evaluation. Return both window boundaries and
an explicit disjointness flag. Continue to report retrospective heuristic
coverage only; this does not create a calibrated prediction interval.

**Why:** M1D-01 requires explicit uncertainty semantics, disjoint calibration
and holdout strategy, safe handling of missing/late observations and coverage
denominators. A fixed split prevents sequentially scored holdout targets from
changing the calibration population for later holdout origins.

**Out of scope:** empirical calibration, nominal coverage targets, conformal
prediction, future performance guarantees, source authorization, new model
fitting, API exposure, decision recommendation or production inference.

### Capability status change

- Keep `local_retail_prequential_residual_envelope` experimental. Its
  historical predictions and released outcomes remain synthetic and
  caller-declared.
- Do not change live API routes or promote `forecasting`.
- The output contract gains explicit calibration/holdout window metadata;
  downstream local diagnostics keep their function signatures and consume
  more conservative eligibility results.

## 2. Acceptance criteria

- [x] Define calibration target dates as the fixed interval immediately before
  the first holdout target: `first_holdout - calibration_days` through
  `first_holdout - 1 day`.
- [x] Define holdout target dates as the requested evaluation interval;
  assert/document calibration and holdout target sets are disjoint.
- [x] Admit a calibration residual only after its declared release is known by
  the current forecast origin and its own seven feature dates were known by
  its own forecast origin.
- [x] Preserve missing-target, unpublished-target, unavailable-history and
  insufficient-calibration abstentions; never impute a missing value as zero.
- [x] Return explicit calibration and holdout boundaries, exact evaluated
  numerator/denominator and no nominal or calibrated interval.
- [x] Add a regression where a prior holdout outcome would have completed a
  later rolling calibration sample, and prove it cannot enter the fixed
  calibration set; retain missing/late-release and independent-oracle tests.
- [x] Keep function signatures and API unchanged; update all affected
  documentation, downstream diagnostic interpretation, capability/evidence
  notes, atlas, catalog and learner exercises.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| API | `api/routes/*` | No | No route invokes the residual diagnostic |
| Core algorithm | `domains/retail/residual_envelope.py::evaluate_retail_residual_envelopes` | Change fixed candidate target window and return split metadata | Existing fixture and new disjoint-target regression |
| Callers | `eligibility_drift.py`, `eligible_values.py`, `selection_sensitivity.py` | Signatures unchanged; stricter residual eligibility flows through | Existing consumer unit suites |
| Tests/oracle | `tests/unit/test_retail_residual_envelope.py::_naive_calibration_oracle` | Update independent quadratic reference to static pre-holdout target dates | Differential schedules, missing/late data, exact boundary case |
| Evidence/capabilities | `EVIDENCE_MAP.json`, `CAPABILITY_LEDGER.json` | Add narrow disjointness evidence; keep experimental status | Documentation guards and test selector |
| Documentation | Residual guide, model/data scope, architecture, backlog, status, debug/learning and atlas | Update semantics and exercises | Atlas/evidence/capability/catalog checks |
| External sources | None | No permission or data change | All tests remain generated and fictional |

## Data, uncertainty and trust review

The holdout is a sequence of rolling one-day forecasts: later origins may use
earlier released observations as forecast features, but no holdout target label
may be used as a calibration residual. Calibration and holdout target dates
are disjoint, and availability is still checked separately at each forecast
origin. This is a software split, not independent-source provenance. All
fixture values and release declarations are synthetic and unauthenticated.

The maximum absolute residual remains a descriptive heuristic. Retrospective
hits divided by evaluated origins do not estimate a nominal confidence level
or guarantee future coverage. Missingness, source revisions, selection bias,
dependence and empirical performance remain unresolved.

## 4. Compatibility and risks

The Python function signature and API remain unchanged. The local experimental
result gains window-boundary metadata and can abstain on origins that previously
borrowed an earlier holdout target as a calibration residual. Downstream
eligibility/selection diagnostics may therefore report fewer eligible
origins. They must retain their exact denominators and must not substitute
missing values with zero.

## 5. Implementation plan

1. Trace current residual activation, consumers and the independent oracle.
2. Add a failing regression showing a prior holdout target cannot repair a
   later insufficient calibration sample.
3. Freeze one pre-holdout calendar target window; preserve as-of release and
   candidate-specific history checks.
4. Update the exact oracle, source guide, evidence claim, capability note,
   debugging/learning, system map, atlas, task record and roadmap.
5. Run focused and dependent consumer tests, full feasible local suite, Ruff
   and all catalog/atlas/evidence/capability checks; record B-07/B-08
   separately.

## 6. Evidence after implementation

Branch `codex/m1d-01-disjoint-residual-calibration`, implementation commit
`10fe58fc3aca45c27288dcc6055ac5d84ab035af`, latest docs commit
`aa2be84ba135ac93cf75b8f0491318d19757f693`, draft [PR #56](https://github.com/GustavoMFDS/MirrorMind/pull/56)
stacked on draft PR #53. Focused residual-envelope tests: 81 passed;
dependent eligibility/value/selection consumer tests: 94 passed. The canonical
local gate passed on the docs head: 700 tests including the API module, Ruff,
symbol catalog, atlas, evidence and capability guards. Pytest reported one
existing Starlette/httpx deprecation warning. The standalone API health test
also passed outside the restricted sandbox. Capability
`local_retail_prequential_residual_envelope` remains experimental.

Reproduce locally from the repository root:

```bash
python scripts/local_quality_gate.py --expected-head aa2be84ba135ac93cf75b8f0491318d19757f693
```

The exact PR #52 SHA associated with B-07 was not rerun. On the current PR #56
stack, both `test_health` and the canonical full gate passed outside the
restricted sandbox, so B-07 is resolved for this stack. The docs-head official
[test run 45335148902](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148902)
and [symbol-catalog run 45335148877](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148877)
failed before job steps; the connector returned no reason annotation for these
runs, so see B-08 for the verified earlier-head billing annotations. Do not
claim calibrated or nominal coverage or official CI success.
