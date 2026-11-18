# Synthetic dataset card — MM-M1c weekly repetition v1

**Status:** generated fixture only. **Not** a permitted
third-party source or a dataset approved for commercial
decision support.

- **ID:** `synthetic-weekly-repeat-v1`.
- **Owner:** repository demonstration; no third-party
  source, customer, rights grant or external collection.
- **File:** [`examples/synthetic-weekly-sales.json`](../../../examples/synthetic-weekly-sales.json).
- **Purpose:** test chronological preprocessing and baseline
  evaluation with deterministic, deliberately easy data.
- **Scope:** 35 daily, single-series nonnegative integer
  values between 2 and 14, dates 2025-01-01 through
  2025-02-04 inclusive, period seven.
- **Unit:** arbitrary synthetic units/day, **not** observed
  real-world sales, latent demand or stock.
- **Declared cutoff:** 2025-02-04 inclusive. No real
  publication or revision timestamps exist.
- **Identity limitation:** `source_id`, `snapshot_id`
  and `usage_note` are plain JSON text, not cryptographic
  identity, permission proof or tamper-evident lineage.
- **Missingness:** no missing date in this particular
  fixture. All zero counts would be accepted by validation
  and correctly make WAPE undefined.
- **Privacy:** no real individual or business data was
  collected to construct the pattern.
- **License / real-data usage:** not applicable to generated
  classroom numbers; **not** an authorization policy
  for unrelated datasets.

## Review boundaries

The preflight validator checks dates, duplicates, units and
declared cutoff. The toy backtest requires a contiguous
series and protects one-step prediction inputs from
direct future-row access. Neither can verify whether a
business measurement existed at a particular past moment,
whether a provider's dataset can lawfully be used, or
whether hidden future information influenced observed
values. Any genuine snapshot needs a new reviewed
[dataset card](../DATASET_CARD_TEMPLATE.md) recording
permissions, availability timestamps, revisions,
source integrity, retention and a reproducible split.

See [the M1 backtest guide](../M1_TEMPORAL_BACKTEST.md)
and [synthetic model card](../model_cards/SYNTHETIC_WEEKLY_BASELINES.md).

## Concrete evidence

- `tests/unit/test_m1_temporal_backtest.py::test_missing_day_abstains_instead_of_zero_imputation`
- `tests/unit/test_m1_temporal_backtest.py::test_old_cutoff_rejects_future_target`

These tests establish selected **fixture behavior**,
not data authorization or real-world predictive validity.
