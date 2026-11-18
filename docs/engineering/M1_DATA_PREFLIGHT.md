# MM-M1a — bounded synthetic daily-observation preflight

**Status:** a local, experimental teaching utility. Not authorized
external ingestion, a live evidence engine, a forecasting model,
a data connector, a WorldKernel adapter, an observation truth check
or a production capability.

Implementation:
[`examples/m1_observation_preflight.py`](../../examples/m1_observation_preflight.py).
Sample (invented data):
[`examples/synthetic-daily-sales.json`](../../examples/synthetic-daily-sales.json).
Read the [retail MVP](../RETAIL_MVP.md),
[provenance obligations](../SECURITY.md) and
[capability gates](CAPABILITY_GATES.md) before using real data.

## 1. Why this limited foundation is useful

The eventual M1 evidence/forecast flow must reject unbounded,
ambiguous or future-dated rows **before** evaluating time-series
models. This demonstration proves a few input invariants
without pretending to own ingestion rights or validate
business measurements.

A JSON fixture declares a schema version, series/source/snapshot
labels, usage note, inclusive calendar cutoff and a list
of `{"date":"YYYY-MM-DD","units":int}` rows.
Those **labels are caller supplied** and not verified
permission, attribution or hash provenance.

## 2. Source methods and contracts

| Symbol | Inputs and effects | Failure boundary |
| --- | --- | --- |
| `_day(value, field)` | Parses exact canonical ISO calendar date into `date` | Rejects malformed/nonexistent dates and non-strings |
| `_nonempty(value, field)` | Validates required 1–128-char string | Nonblank check only, no genuine provenance authentication |
| `_no_duplicate_keys(pairs)` | Rejects duplicate keys while `json.loads` reconstructs dicts | Prevents ambiguous override; not an external integrity signature |
| `validate_batch(payload, max_records=10000)` | Checks exact top-level/record fields, schema, inclusive cutoff, unique days, exact nonnegative integer counts, bounded rows; sorts a **local copy** | Raises `ValueError` rather than trying to repair malformed values; no imputation, rights checks, stationarity or model fit |
| `main()` | Reads no more than 1 MiB + 1 bytes from a local fixture, outputs aggregate summary | CLI only. Invalid input exits 2 with generic error; no raw data/filename echoed |

Rows may arrive unsorted; they are sorted internally.
`missing_day_count` is the difference between
the inclusive first/last calendar span and the number
of **observed** dates. It does not insert zeros or
invent missing sales. Dates after the inclusive cutoff
are rejected. The summary contains no original record
payload, customer information or calculated forecast.

Importantly, the script checks only **declared date labels**.
It cannot detect future leakage embedded in a row's
value, source release latency, revised datasets or
hidden future-derived features. A future real ingestion
module must track *when the value was available* as well
as the observation's calendar date.

## 3. Reproduce an independent synthetic example

```bash
python examples/m1_observation_preflight.py examples/synthetic-daily-sales.json
```

The fixture has four synthetic observations on January 1,
2, 4 and 8, with an inclusive cutoff of 2025-01-08.
The output should include:

```json
{
  "status": "synthetic_structure_validated_not_forecast",
  "source_status": "synthetic_unverified",
  "record_count": 4,
  "missing_day_count": 4,
  "total_observed_units": 13,
  "cutoff_date": "2025-01-08"
}
```

These are **sample arithmetic results**, not sales at a real
store. The utility intentionally does not forecast a fifth
day, rank policies or call an LLM.

## 4. Test-backed claims, with their limits

| Claim ID | Test selector | What the test cannot prove |
| --- | --- | --- |
| **MM-DATA-001** | `tests/unit/test_m1_observation_preflight.py::test_synthetic_batch_is_bounded_and_reports_gaps_without_imputation` | It checks synthetic count/gap behavior, not completeness of a real data source |
| **MM-DATA-002** | `tests/unit/test_m1_observation_preflight.py::test_cutoff_rejects_future_dated_observation` | Calendar cutoff alone does not prevent feature leakage or prove historical availability |
| **MM-DATA-003** | `tests/integration/test_m1_observation_preflight_cli.py::test_synthetic_preflight_cli_fails_without_echoing_sensitive_input` | A generic CLI error does not establish production privacy, access control or log security |

Related tests reject duplicate dates, malformed calendar
dates, booleans/non-integers, excess rows and duplicate
JSON keys. Execute:

```bash
python -m pytest -q tests/unit/test_m1_observation_preflight.py
python -m pytest -q tests/integration/test_m1_observation_preflight_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

These commands are reproducibility instructions, not a
claim that a particular external dataset, model or
deployment passed. CI results for this PR must be
checked before integration.

## 5. Acceptance boundaries and next M1 steps

**Delivered by this isolated experiment:** bounded
synthetic input shape, duplicate/date/cutoff checks,
explicit missing-day counts, deterministic summary,
fixed byte ceiling, generic error responses and
unit/integration regressions.

**Still planned:** permitted M5 subset acquisition and
license review, actual snapshot provenance, release-time
and per-tenant authorization, historical train/test
splits, seasonal-naive and second forecasting baseline,
walk-forward backtesting, uncertainty evaluation,
policy simulation through the independent WorldKernel
gateway and decision explanations.

**Independent exercise:** alter the fixture to add
January 9 while keeping the cutoff at January 8,
then another fixture with January 3 missing.
Predict which is rejected and which is accepted,
what `missing_day_count` becomes and why you must not
replace a missing observation with zero demand.
Explain what additional metadata would be needed
to prove a real source's permitted use and temporal
availability.
