# MM-M1c-local — offline baseline assessment over staged observations

## Goal / current behavior

Prior experiments compare invented daily time series via
scripts under `examples/`. Source code now contains a
strict, immutable [staged snapshot](../M1_LOCAL_CSV_STAGING.md)
primitive but no reusable offline scoring module.

**Desired:** one small module under `src/mirrormind/modules/forecasting/`
that composes already staged observations and a retrospective
one-day rolling origin rule. It must refuse missing or
not-yet-published lagged data, score both fixed baselines
on the *same* eligible origin set and preserve honest
abstention counts.

**Not desired:** external ingestion, source authorization,
trained machine learning, real retailer performance,
UI, RAG, WorldKernel or public forecast serving.

## Accepted behavior and tests

- [x] Exact calendar cutoff and 2..100 holdout bounds.
- [x] Minimum 14 event-days before first origin
  by default; no training on target dates.
- [x] Require seven consecutive **previously published**
  daily observations per target.
- [x] Distinguish missing history from unpublished
  evaluation target and report each abstention count.
- [x] Both baselines share the same target set; no
  silently fabricated zeros.
- [x] MAE, RMSE, signed bias, WAPE with null on zero sum.
- [x] If fewer than two origins scored, return null metrics
  and null winner, not an unsupported ranking.
- [x] Local unit and fixture integration checks
  on one invented, deliberately periodic series.
- [ ] CI review green before integration.

## Impact map

| Area | File(s) / function | Boundary |
| --- | --- | --- |
| Offline forecasting | `src/mirrormind/modules/forecasting/baselines.py` | Fixed heuristics, no model training or API |
| Integration with evidence | `modules/evidence/snapshots.py:available_as_of` | Uses declared publication times; still no rights check |
| Invented fixture | `examples/staged-weekly-availability.csv` | No source or retailer dataset |
| Unit and integration | `tests/unit/test_staged_rolling_baselines.py`, `tests/integration/test_staged_rolling_flow.py` | Prove test-specific arithmetic and abstentions |
| API claims | `api/routes/system.py:capabilities` + capability ledger | Add one **experimental** entry; full forecasting stays planned |
| Documentation | AST index, atlas, source guide, synthetic data/model cards, claim map | Teach behavior and limitations in same PR |
| WorldKernel | No change | Project boundary intact |

## Assumptions and unresolved risks

Real source rights, release times, revisions and
training/holdout independence are not established.
No validated statistical skill or uncertainty
calibration is demonstrated. The synthetic series
is designed to favor the naive seven-day model.
Historical source availability could be falsified
by caller-controlled metadata. External rights,
privacy, audit and authenticated data capture
are separate future acceptance gates.

## Reproduce

```bash
python -m pytest -q tests/unit/test_staged_rolling_baselines.py
python -m pytest -q tests/integration/test_staged_rolling_flow.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These commands are instructions; CI results must
be checked before merging.
