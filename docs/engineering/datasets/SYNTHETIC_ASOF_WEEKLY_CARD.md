# Synthetic dataset card — weekly series with delayed publication

**Status:** generated fixture, **not** a permitted or authenticated
third-party dataset. Dates, delays and counts were invented.

- Snapshot label: `synthetic-asof-weekly-v1`, a Git-tracked
  string and **not** a signed source snapshot.
- File: [`examples/synthetic-asof-weekly-sales.json`](../../../examples/synthetic-asof-weekly-sales.json).
- Count target: arbitrary generated units/day, not actual
  transactions, observed demand or inventory.
- Calendar coverage: 35 consecutive days,
  2025-01-01 through 2025-02-04.
- Synthetic weekly pattern: `[2, 4, 6, 8, 10, 12, 14]`.
- Declared availability: each event is same-day
  except **January 27**, declared first available on
  **January 31**.
- Final retrospective cutoff: 2025-02-04.
- Earlier rolling origins: Jan 28, 29 and 30 are
  deliberately missing an available Jan 27 input.
- Ownership/license: generated teaching values only;
  no rights to any real external dataset are inferred.
- Privacy: no customer or employee records collected.
- Availability provenance: **none**; every date is
  a claim inside the synthetic fixture.
- Missingness: all event dates present in the full
  file, but some event values are unavailable
  at earlier forecasting origins. Missing
  available history is **not** equal to zero units.

## What test evidence means

[`tests/unit/test_m1_asof_rolling_backtest.py`](../../../tests/unit/test_m1_asof_rolling_backtest.py)
verifies observed-calendar continuity, refusal of
unreleased test targets and no-leakage selection
for these *declared* availability dates. The data
card does **not** attest real publication timestamps,
license terms, reporting revisions or collection
rights. The [full template](../DATASET_CARD_TEMPLATE.md)
remains mandatory before any licensed source ingestion.

See the [as-of rolling evaluation guide](../M1_ASOF_ROLLING_EVALUATION.md)
and the accompanying [model card](../model_cards/SYNTHETIC_ASOF_WEEKLY_BASELINES.md).
