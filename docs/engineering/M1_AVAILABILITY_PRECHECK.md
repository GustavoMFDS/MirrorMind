# MM-M1b-exp — synthetic as-of availability filtering

**Status:** local, experimental teaching example only. The dates and
counts are invented. No source is authenticated; no private or
licensed dataset is ingested; no forecasting or WorldKernel execution
takes place.

See the [retail plan](M1_EXECUTION_PLAN.md),
[synthetic availability dataset card](datasets/SYNTHETIC_AVAILABILITY_CARD.md),
[existing date-only preflight](M1_DATA_PREFLIGHT.md), and
[research/data-card requirements](DATASET_CARD_TEMPLATE.md).

## The distinction this example protects

There are two different timestamps for a historical observation:

- **Observed on:** the calendar date the measured event supposedly happened.
- **Available on:** the first date when a decision maker supposedly
  had access to the reported observation.

For a decision cutoff of **2025-01-06**, a fictional January 3
value published January 8 is **not available**, even though
January 3 is an older event date. A January 7 event is
also unavailable because it happens after the cutoff.
The earlier M1a validator only required event dates not
to exceed cutoff; it could not detect this second kind
of temporal leakage.

This example adds a second declared time axis but **cannot
prove either date is genuine**. An actual dataset must
establish publication or release timestamps, revision
history, source permissions, extraction identity and
applicable privacy boundaries separately.

## Method-by-method contract

| Symbol | Input/output behavior | Failure boundary and limitation |
| --- | --- | --- |
| `asof_batch(payload)` | Validates exact synthetic envelope and per-record keys; separates eligible/late/future; reports aggregate eligible units and calendar gaps | Rejects duplicate dates, invalid dates/counts, publication preceding observation and an empty eligible subset; declared provenance is not authenticated |
| `main()` | Reads no more than 1 MiB + 1 bytes from a local JSON fixture, calls safe duplicate-key parser and emits JSON summary | Invalid input produces code 2 with a generic message; no raw records or path are echoed |

Fields:
`schema_version=mirrormind.synthetic_availability.v1`,
`series_id`, `source_id`, `snapshot_id`,
`usage_note`, `as_of_date`, and records with
`observed_on`, `available_on`, `units`.

The helper checks exact nonnegative bounded integers and
canonical `YYYY-MM-DD` dates. Rows are eligible only when
**both** `observed_on <= as_of_date` and
`available_on <= as_of_date`. It never uses excluded
row values in `eligible_observed_units`; only their
*counts* are reported.

A gap inside the eligible span remains a gap.
The function does **not** convert a missing or
unpublished value into zero units, infer missing
records, create a model-ready continuous series,
or fill from future revisions.

## Hand-worked synthetic case

The [fixture](../../examples/synthetic-asof-sales.json)
declares January 6 as its retrospective decision cutoff.

| Synthetic date | Claimed available | Units | Result |
| --- | --- | ---: | --- |
| Jan 1 | Jan 1 | 2 | Eligible |
| Jan 2 | Jan 2 | 4 | Eligible |
| Jan 3 | **Jan 8** | 6 | Excluded: late publication |
| Jan 4 | Jan 4 | 8 | Eligible |
| Jan 5 | Jan 6 | 10 | Eligible |
| Jan 6 | Jan 6 | 12 | Eligible |
| Jan 7 | Jan 7 | 14 | Excluded: future event |

Expected aggregate:

```json
{
  "status": "synthetic_availability_filtered_not_verified_evidence",
  "source_status": "synthetic_unverified",
  "eligible_count": 5,
  "excluded_late_available_count": 1,
  "excluded_future_event_count": 1,
  "gaps_within_eligible_span": 1,
  "eligible_observed_units": 36
}
```

With the cutoff changed to January 8, all seven
synthetic records become eligible and the total is
56, without gaps. **This is a retrospective
toy example, not evidence that publication metadata
was actually available on those dates.**

## Reproducible code and concrete evidence

```bash
python -m examples.m1_availability_preflight examples/synthetic-asof-sales.json
python -m pytest -q tests/unit/test_m1_availability_preflight.py
python -m pytest -q tests/integration/test_m1_availability_preflight_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

| Reviewed claim | Test and observation | Important limitation |
| --- | --- | --- |
| **MM-AVAIL-001** | `tests/unit/test_m1_availability_preflight.py::test_late_publication_is_excluded_even_when_event_date_precedes_cutoff` checks excluded late/future values | Declared `available_on` is not externally verified |
| **MM-AVAIL-002** | `tests/unit/test_m1_availability_preflight.py::test_unavailable_value_change_cannot_change_eligible_aggregate` proves late value mutation leaves eligible sum unchanged | This does not prevent hidden future-derived features in other fields |
| **MM-AVAIL-003** | `tests/unit/test_m1_availability_preflight.py::test_published_before_observation_rejected` rejects logically impossible publication order | Actual reporting and revisions require separate provenance and authorization |

These are commands for reproducibility, not evidence
of external data authenticity or independent execution.
Review actual CI results before merging.

## Independent exercise

First, predict the January 6 eligible total **without**
using the January 3 value. Next change its units from
6 to 999; the eligible total must stay 36. Then
move the cutoff to January 8 and explain what becomes
eligible and why the gap disappears. Finally explain
what makes `available_on` a *claim supplied by JSON*,
rather than verifiable evidence of an actual
retailer's knowledge at that date.

**M1b remains planned** until real source rights,
snapshots, availability times, revision handling,
privacy and retention are verified on a licensed
dataset. A successful synthetic filter is
not a functioning Evidence Engine.
