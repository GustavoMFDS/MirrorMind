# MM-M1c fix — count observed pre-holdout rows, not dataset age

## Bug and narrowed outcome

Previously `min_history_days` in
`backtest_staged_snapshot` compared the date of
the oldest observation against the first holdout
date minus the threshold. This did not require
that the number of recorded dates actually reach
the configured minimum. One ancient observation
and a few recent values could pass.

The corrected rule checks that at least
`min_history_days` **unique recorded event days
exist before the first target**. The existing
seven-day per-origin availability requirement
remains unchanged: incomplete recent windows
still cause abstention rather than fabricated zeros.

## Acceptance and impacts

- [x] Sparse history with one old row and fewer
  than 14 observations before holdout is rejected.
- [x] A custom threshold of seven accepts
  the same example, while three origins still
  abstain because publication came late.
- [x] Twenty-eight prior rows satisfy a
  threshold of 28; a threshold of 29 fails.
- [x] Dates at the supported calendar minimum
  fail with a controlled `ValueError`, not
  an uncaught date-range overflow.
- [x] The existing baseline metrics, API
  capability status and WorldKernel contracts
  are not changed.
- [ ] Python and documentation CI must be
  verified green before merge.

**Source:** `src/mirrormind/modules/forecasting/baselines.py`.
**Regressions:** `tests/unit/test_staged_rolling_baselines.py`.
**Explanation:** [method guide](../M1_STAGED_ROLLING_BASELINES.md)
and curated [claim map](../EVIDENCE_MAP.json).

## Non-goals and limitations

This is not a new training algorithm, source
ingestion feature, permissions approval or
model performance validation. An observed
date does not authenticate a publisher's
release timestamp; real forecasting remains
planned until authorized sources and
independent holdout evaluation are available.

## Reproduce

```bash
python -m pytest -q tests/unit/test_staged_rolling_baselines.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```
