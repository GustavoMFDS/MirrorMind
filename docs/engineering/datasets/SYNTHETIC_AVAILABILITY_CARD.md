# Synthetic dataset card — publication-delay teaching v1

**Not approved third-party evidence.** This fixture was invented
specifically to demonstrate event time versus reported availability
time. Its metadata is **not authenticated**.

- Dataset ID: `synthetic-delayed-publication-v1`.
- Path: [`examples/synthetic-asof-sales.json`](../../../examples/synthetic-asof-sales.json).
- Source/owner: generated repository demonstration, with no
  collection of customer or real retailer data.
- Declared source: `synthetic-fixture-generator`, a string,
  **not** a permission, source signature or audit trail.
- Granularity: one invented integer count/day.
- Observation dates: 2025-01-01 through 2025-01-07.
- Claimed availability dates: same day except Jan 3
  claimed published on Jan 8 and Jan 5 on Jan 6.
- Retrospective cutoff: 2025-01-06.
- Eligible observed values: five dates, aggregate 36.
- Excluded: Jan 3 (late publication), Jan 7 (future).
- Missingness: Jan 3 remains absent in the eligible
  January 1..6 span; no imputation, revision filling,
  probabilistic modeling or fabricated zero sales.
- Integrity: no cryptographic digest or signed producer
  is claimed; the generated file is versioned in Git.
- External rights: **not applicable** for invented
  fixture values; this is **not a license for real data**.

## What the current tests establish

- `tests/unit/test_m1_availability_preflight.py::test_late_publication_is_excluded_even_when_event_date_precedes_cutoff`
- `tests/unit/test_m1_availability_preflight.py::test_unavailable_value_change_cannot_change_eligible_aggregate`
- `tests/integration/test_m1_availability_preflight_cli.py::test_synthetic_asof_cli_reports_only_eligible_aggregate`

These tests check one declared synthetic as-of convention,
not whether the dates were truly reported or usable at
the claimed time. A real [data card](../DATASET_CARD_TEMPLATE.md)
needs verified source rights, collection contract, publisher
release/revision metadata, access-control requirements,
timestamp semantics, privacy review and retention approval
**before** actual ingestion.

Read [the as-of guide](../M1_AVAILABILITY_PRECHECK.md)
and [M1 delivery plan](../M1_EXECUTION_PLAN.md).
