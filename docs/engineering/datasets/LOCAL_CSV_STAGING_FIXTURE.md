# Local CSV staging fixture card — deliberately invented rows

**Status: local teaching data, not a source-approved dataset.**

- **Fixture:** [`examples/staged-daily-observations.csv`](../../../examples/staged-daily-observations.csv)
- **Origin:** manually written synthetic values for a unit/integration exercise
- **Schema:** exact `series_id,observed_on,available_on,units` CSV
- **Population:** four rows in two fictional series, `item-A` and `item-B`
- **Time:** three January 2025 observation dates; `item-A` January 2
  is declared published on January 5, later than its event date
- **Units:** arbitrary invented nonnegative daily counts; never actual
  retail transactions, demand, stock or approved model features
- **Permissions:** no external source or customer records used;
  **not** an approved license for unrelated data
- **Availability evidence:** solely user-written CSV labels; no
  independent publisher release history exists
- **Snapshot integrity:** SHA-256 can detect mismatches against an
  independently supplied expected digest; computing that digest from
  the same data is *not* an authenticity guarantee
- **Retention/security:** the core stage function does not save,
  transfer or publish data. A later service will need its own
  access controls, deletion policy and audit.

## Reproduction and known gaps

Read [the source-reviewed staging guide](../M1_LOCAL_CSV_STAGING.md)
and its test fixture path
[`tests/integration/test_local_snapshot_flow.py`](../../../tests/integration/test_local_snapshot_flow.py).
When the retrospective origin is January 3, the local as-of
view includes two `item-A` rows: January 1 (2 units)
and January 3 (0 units). January 2's reported 4 units
are **excluded until its declared January 5 publication**.

This proves structural behavior on invented data only.
It cannot prove dataset usage rights, source authenticity,
non-revision of historical records, sensitive-field detection,
model validity or a trusted capture date. Real data requires a
separately reviewed [dataset card template](../DATASET_CARD_TEMPLATE.md)
and source-specific acceptance.
