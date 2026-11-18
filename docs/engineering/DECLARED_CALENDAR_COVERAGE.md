# MM-M1b — declared operational calendar comparison (experimental)

## Why another calendar is necessary

The [civil-day coverage module](RETAIL_COVERAGE.md) reports every absent
calendar date between observed positive invoice-line days. A Sunday, holiday
or day when a business was closed **could** be among those dates.
The new [declared calendar module](../../src/mirrormind/domains/retail/calendar_coverage.py)
accepts **only a caller-supplied, strictly ordered tuple of exact dates**
and counts internal missing *declared* dates separately from internal
civil days omitted by that tuple. This is a comparison of assumptions,
not independent proof that a shop was open or data were published.

Input is the existing fictional, bounded `UciRetailProjection`, plus a
tuple of 1–3,660 exact `datetime.date` values. Every observed positive
product-day must occur in the declared calendar; contradictory inputs
are refused, not silently repaired. Per-product gaps are measured
*between* the first and last positive observation only. Calendar dates
before first/after last product observations do not establish exposure.

The immutable result and its receipt expose only counts: declared dates,
positive product-days, distinct products, missing declared internal dates,
internally absent civil dates **not declared** by the caller, and the number
of products with missing declared days. No customer, invoice or stock code
is returned. Receipts say `caller_declared_unverified` and
`unknown_not_derived_from_invoice_date`.

## Important distinctions

- An omitted date is **not confirmed closed**; the caller's calendar may
  itself be wrong, incomplete, revised or limited to a subset of stores.
- A declared date with no positive line is **not a recorded zero**:
  it could represent no demand, a stockout, missing data, excluded returns,
  a cancellation, a store closure or another event.
- A positive invoice-line observation is **not true demand or opening-stock
  evidence**. A calendar alone cannot validate source rights, publication
  vintages, business operating periods, available stock or original license.
- This module does not emit a padded sequence, persist observations, infer
  weekends, connect to WorldKernel or allow a forecasting readiness upgrade.
- Distinct products can have different true opening periods; this simple
  global declared calendar is intentionally not an inferred per-product
  schedule. Validate explicit source-specific schedules before any real use.

## Fictional example and regression

Tests in
[`tests/unit/test_declared_calendar_coverage.py`](../../tests/unit/test_declared_calendar_coverage.py)
construct invented positive sales on January 7 and 10.
Under an explicit calendar containing only the 7th and 10th, two internal
civil dates are not scheduled, and zero *scheduled* dates are missing.
If the caller additionally declares January 8, there is exactly one
missing scheduled date and one omitted civil day. Neither statement
assigns demand to January 8.

Claim **MM-DCAL-001** is illustrated by
`tests/unit/test_declared_calendar_coverage.py::test_closed_day_not_counted_as_missing_declared_observation`.
It demonstrates computation only, not a truthful operational calendar.

```bash
python -m pytest -q tests/unit/test_declared_calendar_coverage.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Review and learning exercise

Take the synthetic January 7–10 example, declare January 8 as a possible
business day and independently explain why the additional missing declared
product-day cannot be interpreted as zero units sold. Then remove January 10
from the declared calendar: the same positive transaction on that day must
cause rejection, because the caller's schedule contradicts observations.

Before any promotion, obtain human-reviewed source rights, canonical source
hash, authenticated original collection and publisher availability calendars,
product/store scoping, retention/privacy clearance and evaluated empirical
outcomes. **M1b authorization and M1c empirical forecasting remain open.**
