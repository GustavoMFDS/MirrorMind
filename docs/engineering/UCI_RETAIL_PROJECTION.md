# MM-M1b — UCI-shaped transaction projection (bounded experimental)

**Status:** experimental domain-specific offline transformation. Automated
tests remain synthetic-only. The one approved UCI snapshot did not finish
projection because the corrected output exceeded the approved 250,000-group
ceiling; there are no empirical results. The UCI source-specific exception
does not alter the generic projection contract.
**Not:** authorized data ingestion, an XLSX reader, a validated
forecast, an inventory engine, a real retailer adapter, or a
WorldKernel dependency.

Source:
[`src/mirrormind/domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py).
Independent tests:
[unit](../../tests/unit/test_uci_retail_projection.py),
[integration](../../tests/integration/test_uci_retail_projection_flow.py).
Before real-data work, read the
[UCI source rights/privacy review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md),
[dataset card template](DATASET_CARD_TEMPLATE.md) and
[M1 gate](M1_EXECUTION_PLAN.md).

## Why this component lives in `domains/retail/`

The generic `evidence/snapshots.py` stores only
event day, *declared first availability day*, series ID
and integer count. The official UCI Online Retail
dataset is a transaction workbook, not that strict
schema, and `InvoiceDate` does **not** establish
historical publication dates.

A transformation from transaction rows to product-day
counts is **sector-specific**. It must not add UCI
fields or retailer assumptions to the platform's
generic evidence, forecasting or simulation packages.

This source module only accepts a **trusted caller's
already-created row mappings**: it does not download,
open or parse `Online Retail.xlsx` and contains
no customer license authorization.

## Accepted input and intentionally missing outputs

Each input mapping must contain the **four**
UCI-style fields `InvoiceNo`, `StockCode`,
`Quantity`, `InvoiceDate`. Extra fields such as
`CustomerID`, `Description`, `UnitPrice` and
`Country` are **not accessed or returned**. For
this narrowly tested contract:

- `InvoiceNo`: numeric positive integer, or 5–12
  ASCII digits with an optional leading `C`
  for cancellation. Other invoice conventions
  are unsupported and rejected.
- `StockCode`: the public generic projection accepts a nonempty ASCII code
  using `[A-Za-z0-9][A-Za-z0-9._-]{0,31}`. Only the private UCI workbook
  adapter can invoke the bounded internal-space grammar, with no
  leading/trailing whitespace and alphanumeric endpoints. It does not trim or
  normalize strings. Public row callers remain strict and cannot opt in.
  A valid code does **not** mean the source entry is necessarily a physical
  merchandise SKU.
- `Quantity`: exact signed Python integer,
  between -1 billion and +1 billion per line.
  A float or boolean is rejected, never
  silently rounded to a sales count.
- `InvoiceDate`: a **timezone-naive Python
  `datetime`**, representing the source's
  purported transaction event time. No string
  or timezone-aware alternative is assumed.
- Default caps: at most 10,000 input rows
  and 2,000 output product-day groups. A
  caller may choose a larger explicit budget, up to
  600,000 input rows and 100,000 product-day groups;
  the limits are not evidence that the original UCI
  workbook has been processed or verified. A
  maximum of 1 billion **accepted positive
  units in total** prevents unbounded aggregation.

The return value is immutable
`UciRetailProjection`, with a sorted tuple of
`ProductDayUnits(stock_code, observed_on, units)`
and counts of processed/accepted/cancelled/
negative/zero rows. The private UCI workbook adapter may also provide one
aggregate count for authorized unverified-prefix exclusions; the public
generic projector always keeps this count at zero. `receipt()` supplies only
aggregate counts and the explicit statuses:

```json
{
  "status": "uci_shaped_projection_not_authorized",
  "publication_time_status": "unknown_not_derived_from_invoice_date"
}
```

These status fields are a small excerpt; the
receipt also reports the selected row counters.
No `available_on` appears on `ProductDayUnits`
because **we have no verified time when a
historical forecaster could know the value**.

**Do not** convert `InvoiceDate` to `available_on`
or feed these records to `backtest_staged_snapshot`
without a separately reviewed source-publication
assumption/provenance contract. The existing
`stage_csv_snapshot` requires complete, explicit
availability timestamps and does not accept this
projection as a direct input.

## Method-by-method behavior

| Symbol | Inputs / outputs | Fail-closed and scientific limits |
| --- | --- | --- |
| `ProductDayUnits` | Frozen stock code, date and positive aggregated invoice-line count | No customer/invoice IDs, inventory, latent demand or publication timestamp |
| `UciRetailProjection` | Frozen grouped days and explicit source row counters, including the UCI-only unverified-prefix count | The generic projector does not populate that source-only counter; the object is not a license grant, deduplicated receipt or signed source snapshot |
| `UciRetailProjection.receipt()` | Aggregate counters, `not_authorized` and `publication_time_unknown` signals | Product codes in the internal `days` tuple remain potentially sensitive and need access control |
| `_invoice_number(value)` | Narrow numeric/string invoice grammar, preserves leading cancellation marker | Unsupported invoice patterns fail rather than being treated as sales |
| `_transaction_day(value)` | Naive `datetime` to source event date | Cannot establish timezone, business-day cutoff or publication vintage |
| `project_uci_retail_rows(rows, max_rows, max_groups)` | Bounded single-pass positive-line aggregation by (`StockCode` category, event day); defaults are 10,000 rows/2,000 groups and ceilings are 600,000/100,000 | Rejects malformed inputs/budgets and excludes cancellation, negative and zero lines with disclosed counters; generic invoice and StockCode grammar remain unchanged |

All row fields are validated **before** classifying
cancellations and negative quantities. An invoice
whose number starts with `C` is excluded and counted
as a cancellation. A non-cancellation row with
negative quantity is excluded and counted as a
negative line; a recorded zero quantity is counted
separately but not treated as a positive sale.
No negative number is silently reclassified as
lost demand. These are **line-based conventions**,
not proof of financial reconciliation, returns
policy, successful payment or net/gross revenue.

The approved workbook reader applies source-specific representation rules
before invoking the bounded internal projector: exact positive five-digit
integer cells become decimal text, and approved internal-ASCII-space strings
remain unchanged. The public generic projector does not expose this option.
Six-digit invoice IDs continue through normal classification;
`C`/`c` plus six digits are cancellation rows; other one-letter ASCII prefixes
plus six digits are replaced by a private sentinel and excluded before the
projector reads stock code, quantity or event date. Only an aggregate
`unverified_invoice_prefix_rows` count survives. Every other invoice format
fails closed. Generic row callers cannot enable this behavior through the
public function. Excluding these rows can change category cohorts, observed
totals, zero targets and downstream scores; any future evaluation would cover
only recognized invoice IDs. The adapter does not inspect `Description` to
infer categories. Results describe units per `StockCode` category, not
physical-SKU demand. The reader's ZIP and UCI-specific group overrides are
separate from generic row budgets; defaults and generic ceilings remain
unchanged.

The source does not include a stable line-item
identifier in the required projection fields.
**Duplicate identical rows are not automatically
deduplicated**: they may represent repeated
valid lines or accidental duplication. This
must be resolved by a separately reviewed source
identity and cancellation policy.

## Reproducible invented walkthrough

```python
from datetime import datetime
from mirrormind.domains.retail.uci_transactions import project_uci_retail_rows

fake_rows = [
    {"InvoiceNo": "536365", "StockCode": "SKU-A", "Quantity": 2,
     "InvoiceDate": datetime(2011, 1, 5, 9), "CustomerID": 12345},
    {"InvoiceNo": "536366", "StockCode": "SKU-A", "Quantity": 3,
     "InvoiceDate": datetime(2011, 1, 5, 17), "CustomerID": 99999},
    {"InvoiceNo": "C536367", "StockCode": "SKU-A", "Quantity": -1,
     "InvoiceDate": datetime(2011, 1, 6, 11)},
]
result = project_uci_retail_rows(fake_rows)
assert result.days[0].units == 5
assert result.receipt()["cancelled_rows"] == 1
assert result.receipt()["publication_time_status"].startswith("unknown_")
```

These are invented rows, not copied
customers, official UCI sample data or
a performance result. The internal
`days` output includes product codes.
It is intended for a trusted local
consumer, **not a public API response**.

## Curated claims and exact regressions

| Claim | Test selector | Important limitation |
| --- | --- | --- |
| **MM-UCI-001** | `tests/unit/test_uci_retail_projection.py::test_positive_rows_aggregate_by_product_calendar_day_without_raw_ids` | Demonstrates positive invoice-line aggregation and counters, not true demand or reconciled sales |
| **MM-UCI-002** | `tests/unit/test_uci_retail_projection.py::test_customer_columns_are_not_accessed_or_serialized` | Local output minimization does not protect upstream file readers, callers, logs or privacy rights |
| **MM-UCI-003** | `tests/unit/test_uci_retail_projection.py::test_row_limit_is_enforced_on_iterator_without_materialization` | Bounded row iteration does not enforce real XLSX compression, byte, time or memory quotas |
| **MM-UCI-004** | `tests/integration/test_uci_retail_projection_flow.py::test_retail_projection_preserves_unknown_release_time_and_cannot_be_staged_directly` | Blocking a fabricated as-of field does not establish authentic historical publication vintages |

Additional tests cover cancelled/nonpositive rows,
invalid dates and product codes, opt-in internal ASCII-space codes,
strict integer
arithmetic, aggregation overflow, deterministic
sorting, duplicates and unsupported direct
staging as verified history.

```bash
python -m pytest -q tests/unit/test_uci_retail_projection.py
python -m pytest -q tests/integration/test_uci_retail_projection_flow.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

## Independent exercise and next evidence gate

Using only fabricated rows, compare two positive
quantities on the same stock-code/day with one
`C` invoice and one negative quantity. Predict
the final count and each exclusion counter.
Then supply a date string instead of a Python
`datetime`; explain why the parser refuses
to guess the original Excel cell type.

Finally, try to find `available_on` in the
projected daily record. Its absence is
**intentional**: the UCI file's transaction
date is not proof of when the transaction
was first available to a forecaster.

The bounded [XLSX reader](UCI_WORKBOOK_READER.md)
and [synthetic event-time evaluator](M1_UCI_EVENT_TIME_RESEARCH.md)
extend this path without adding real rows to tests. The owner-approved source
scope is recorded in the [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md);
the corrected source call exceeded the 250,000-group ceiling and is stopped.
Do not retry, chunk or widen the cap without a new scope decision.
