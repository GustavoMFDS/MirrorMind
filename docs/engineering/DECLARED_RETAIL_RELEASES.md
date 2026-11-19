# MM-M1b — retrospective declared-release audit (experimental)

## Purpose

The [retail transaction projection](UCI_RETAIL_PROJECTION.md) provides
positive product/event-day counts, but deliberately has **no authenticated
publication timestamp**. The new offline
[`declared_releases.py`](../../src/mirrormind/domains/retail/declared_releases.py)
does **not** fill that missing provenance with `InvoiceDate`. Instead, it
requires an explicit release declaration for **every** projected
(product, event-day) key. It counts what would *hypothetically* have been
available as of a caller-selected date.

**These dates are assertions from a caller, not verified publisher history,
source authorization, collection schedules or revision history.** The audit
is useful only for demonstrating the temporal boundary on fictional rows.

## Exact contracts and exclusions

- Input: one already bounded and validated `UciRetailProjection`, a
  `tuple[DeclaredProductRelease, ...]` with no more than 2,000 declarations,
  and an exact `datetime.date` origin.
- An input release includes `stock_code`, `observed_on`, and `available_on`.
  The release key must match exactly one positive product/event-day.
  Every projected key needs one release, and duplicate/unmatched releases
  or `available_on` preceding `observed_on` are rejected.
- Product-days with `observed_on` **after** the origin are classified as
  future events. Earlier event-days with `available_on` after the origin
  are classified as *withheld/unpublished*. Only records meeting **both**
  checks count as available. No unavailable units enter available-unit totals.
- Results are immutable aggregate counts only, without products,
  invoices, customers, descriptions or prices. No raw evidence view,
  persisted model input or forecast is produced.
- The receipt says `declared_release_audit_not_source_verified` and
  `caller_declared_unverified`. Even a structurally valid release map
  cannot authenticate a publisher or authorize use.
- Cancellation/return-only dates remain excluded from the positive-line
  projection; they are not inferred as zero demand. The number of missing
  calendar dates is unaffected by this audit.

## Fictional example

A positive line for product A appears on January 1 (2 units), another on
January 2 (5 units) but is **declared published** on January 5, and a
positive line for product B appears on January 4 (7 units). At the January
3 origin, only the first product-day is available: **1 available,
1 withheld, 1 future**, **2 available positive-line units**.

When the origin moves to January 6, all three become hypothetically
available, totaling 14 positive-line units. This is an invented toy fixture
rather than proof of historical source publication or true demand.

Claim **MM-REL-001** is represented by
`tests/unit/test_declared_retail_releases.py::test_declared_asof_excludes_late_and_future_product_days_without_identifiers`.
The independent negative cases reject unknown, duplicated, missing or
chronologically impossible release declarations, ambiguous origin types,
and invalid release data. They also verify immutable and identifier-free
aggregate receipts.

```bash
python -m pytest -q tests/unit/test_declared_retail_releases.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Review exercise and remaining gates

Modify the January 2 record to be released on January 2. The January 3
origin now includes both A dates, but the January 4 future B event remains
excluded. Next, remove the January 2 release entirely: the auditor must
fail closed, not use the transaction date as a fallback.

A production-quality timeline would require independently verified
publisher snapshots/vintages, source-rights and privacy review, signed
dataset lineage, revision and deletion handling, stable identifier
definitions, a true observation calendar and independently evaluated
temporal holdouts. No real UCI dataset, authorized source, model training,
evidence service or WorldKernel adapter is introduced.
