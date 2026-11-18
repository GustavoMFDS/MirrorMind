# MM-M1c — deterministic origin audit for offline staged evaluation

## Problem and accepted narrow scope

The existing `backtest_staged_snapshot` reports aggregated
`scored_origins` and abstention totals, but not *which*
holdout days were excluded or whether a target was genuinely
missing versus merely not yet published by the evaluation cutoff.

Add one lightweight, bounded, deterministic **internal**
origin status per requested day without exposing raw
observations, fitted model outputs, confidential records,
untrusted prompts or secret source identifiers. Keep
existing counter fields and metrics stable.

## Acceptance and negative tests

- [x] Each requested one-step target has exactly one
  `target_on`, `origin_on`, `status` record,
  in chronological order, without data values.
- [x] Distinguish `scored`,
  `required_history_unavailable`, `target_missing`
  and `target_not_published_by_cutoff`.
- [x] Keep legacy aggregated target unavailability
  counter and partition it into missing/unpublished.
- [x] Repeated evaluation of unchanged staged
  fixture produces identical diagnostic output.
- [x] All origins abstained -> null scores/winner;
  no fabricated conclusions.
- [ ] Verify Python CI and docs CI before merge.

## Impact map

| Layer | Reviewed code path | Limitation |
| --- | --- | --- |
| Forecasting | `src/mirrormind/modules/forecasting/baselines.py:backtest_staged_snapshot` | Bounded offline status events, no logged audit store |
| Evidence | `available_as_of` unchanged | Declared availability timestamps remain unverified |
| Unit tests | `tests/unit/test_staged_rolling_baselines.py` | Distinguishes three adverse cases on synthetic fixture |
| Docs | Method guide, evidence map, learning, atlas, roadmap | Structural claim checks only |
| API, WorldKernel | Unchanged | No new source connector or execution adapter |

## Trust and retention boundary

Dates, series ID and snapshot digest are still
potentially identifying metadata. The status array
is a **local diagnostic**, not permission, a durable
audit trail, evidence provenance, an authorization
token or a legally admissible record. Real dataset
permissions remain blocked until independent review
of the original source.

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

Commands are reproducibility instructions, not
a substitute for actual CI results.
