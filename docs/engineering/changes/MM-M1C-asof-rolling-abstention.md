# MM-M1c-asof-exp — rolling evaluation with publication-time abstention

**Scope:** generated-data teaching utility. Neither a
production forecast nor actual authorized ingest.

## Motivation

Two experimental tools now exist:
`m1_availability_preflight.py` distinguishes event and
publication dates at one cutoff;
`m1_temporal_backtest.py` evaluates rolling one-step
baselines on event-date-contiguous observations.

Neither standalone tool guarantees that a datum
available in the **final** snapshot existed at
**each earlier rolling prediction origin**.
This experiment joins their contracts by requiring
all seven lagged values to be available by each origin.

## Acceptance criteria

- [x] Use existing synthetic availability validator
  for schema, date, integer and source-label checks.
- [x] For each one-step origin, inspect publication
  dates for exactly seven consecutive past events.
- [x] Abstain when a required historical value was
  not yet published; do not fill it with zero.
- [x] Reject evaluation targets unavailable even
  at the final evaluation cutoff.
- [x] Score both baselines on the same valid origins;
  disclose scored versus abstained coverage.
- [x] If fewer than two origins can be scored, return
  null metrics and no winner.
- [x] Bounded redacted CLI and unit/integration
  adverse-case regressions.
- [ ] Verify independent Python and documentation CI.

## Impact map

| Layer | Change | Scope |
| --- | --- | --- |
| Local experiment | `examples/m1_asof_rolling_backtest.py` | No production forecast module |
| Generated fixture | `examples/synthetic-asof-weekly-sales.json` | Invented dates/release times |
| Tests | `tests/unit/test_m1_asof_rolling_backtest.py`, `tests/integration/test_m1_asof_rolling_backtest_cli.py` | Verify source-code assumptions, not actual provenance |
| Capability API | `src/mirrormind/api/routes/system.py` | Experimental claim only; `forecasting` planned |
| Documentation | Source guide, synthetic data/model cards, atlas, evidence map and roadmap | Explain 4/7 coverage and statistical selection caveats |
| WorldKernel | **No change** | No adapter or real simulation |

## Risks not resolved

Publication timestamps are caller-provided JSON
and not authenticated. Real data could contain
late revisions, hidden future-derived features,
unknown timezones, rights limitations, censored sales
or missing source rows. This exercise does not
prove statistical calibration or predictive ability
on independent data; the constructed repeating
pattern heavily favors seasonal naive.

## Reproducible commands

```bash
python -m examples.m1_asof_rolling_backtest examples/synthetic-asof-weekly-sales.json
python -m pytest -q tests/unit/test_m1_asof_rolling_backtest.py
python -m pytest -q tests/integration/test_m1_asof_rolling_backtest_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These are instructions, not assertions that CI
already passed or that a real-world model works.
