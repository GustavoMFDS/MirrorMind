# MM-M1C-EXP — synthetic one-step rolling-origin baseline test

**Accepted goal:** build a reproducible local exercise comparing two
simple historical-only estimators on a **synthetic** daily series.
This is not the full M1c requirement for independent, licensed
empirical data and temporal evaluation, nor a production forecast.

## Current versus desired behavior

Current M1a:
`examples/m1_observation_preflight.py` validates a generated
daily fixture and reports missing dates but **does not forecast**.

New, deliberately narrow behavior:
`examples/m1_temporal_backtest.py` compares a fixed lag-7
seasonal naive baseline and 7-day trailing mean on
one-step rolling origins, with no future-target access.
It must refuse gaps, malformed dates, unsupported labels,
insufficient history and unsafe inputs. Emit only
aggregate synthetic metrics, no real-world forecast.

## Acceptance criteria

- [x] 35 consecutive explicitly synthetic daily records
  with predeclared 7-day repetition and cutoff.
- [x] Fixed seven-day holdout; at each origin only previous
  observations are used to issue the one-day-ahead estimate.
- [x] MAE, RMSE, signed bias and zero-denominator-safe
  WAPE computed on identical held-out targets.
- [x] Synthetic pattern makes seasonal lag 7 exact;
  second baseline remains meaningfully different.
- [x] Missing date, late cutoff, bad budget and insufficient
  training history fail closed with no silent imputation.
- [x] Local CLI has bounded input and generic errors.
- [ ] CI green on both Python/test and full documentary checks
  (verify before integration).

## Impact map

| Surface | Source / test | Boundary |
| --- | --- | --- |
| Standalone algorithm | `examples/m1_temporal_backtest.py` | Local synthetic evaluation, no production prediction endpoint |
| Fixture | `examples/synthetic-weekly-sales.json` | Invented numbers, not a real retailer dataset |
| Unit tests | `tests/unit/test_m1_temporal_backtest.py` | Prove selected temporal input and metric invariants |
| CLI tests | `tests/integration/test_m1_temporal_backtest_cli.py` | Subprocess JSON summary/size/redaction behavior |
| Capability API | `src/mirrormind/api/routes/system.py` | Add separate experimental entry; keep `forecasting` planned |
| Audit | Ledger, evidence map, atlas, reviewed model/data cards | Explicit source limitations and reproducible checks |
| WorldKernel | **No change** | No adapter or simulated retailer business result |

## Trust, scientific and security risks

The fixture is generated to make seasonal naive look
perfect. No real data license, acquisition, publication
timestamp, revision history, forecast calibration or
held-out real-world predictive value is demonstrated.
A sequence with no gaps does not prove latent demand
was observed. Fixing/tuning models after examining
the holdout would invalidate an untouched holdout
claim. Treat any real business input as outside scope.

## Independent reader reproduction

```bash
python -m examples.m1_temporal_backtest examples/synthetic-weekly-sales.json
python -m pytest -q tests/unit/test_m1_temporal_backtest.py
python -m pytest -q tests/integration/test_m1_temporal_backtest_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These are reproduction instructions, not claims that
test execution already succeeded. The summary is
**synthetic model-comparison arithmetic only**.
