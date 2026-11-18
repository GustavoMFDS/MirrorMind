# MM-M1b — bounded UCI-shaped transaction-to-day projection

## Decision and scope

The [official UCI Online Retail candidate](../datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
has a published license, but **no real dataset access,
privacy signoff, original snapshot hash or publisher
availability vintages have yet been approved**. Add a
small retail-domain offline transformation that
**only accepts a trusted caller's already-projected
row mappings**, demonstrated exclusively on invented
transactions. No `Online Retail.xlsx` parsing, download,
external source connector, persistence or implicit
permission is part of this slice.

This **is not** completion of authorized M1b ingestion.
The input is UCI-shaped but can contain extra keys such
as `CustomerID`, `Description`, `UnitPrice`
and `Country`. No such fields may appear in
normalized output or in validation messages.

## Minimum accepted behavior

- [ ] Keep retail-only rules in `domains/retail/`
  rather than the generic evidence and forecasting packages.
- [ ] Validate a bounded iterable of row mappings with
  `InvoiceNo`, `StockCode`, `Quantity`,
  `InvoiceDate` only; reject absent/ambiguous
  required fields and invalid date, quantity or code types.
- [ ] Count but **exclude** cancellation invoices,
  nonpositive quantities, and transactions that cannot
  safely support a positive sales-count proxy.
- [ ] Aggregate strictly positive integer units by
  safe `StockCode` and recorded calendar day,
  with caps on processed rows, groups and cumulative units.
- [ ] Return a deterministic immutable projection
  recording kept/skipped row counts and the
  `not_authorized` / `publication_time_unknown`
  source status; **do not manufacture**
  `available_on=InvoiceDate`.
- [ ] Return no customer IDs, invoice IDs, descriptions,
  prices, countries or raw row mappings.
- [ ] Unit/integration regressions test privacy,
  cancellation/return handling, malformed inputs,
  row/group/quantity limits, determinism and
  unsupported direct forecasting/as-of use.
- [ ] Source catalog regeneration, claims-to-tests,
  method guide, fictional dataset card, atlas,
  model/roadmap/learning docs and CI in the same PR.

## Impact and compatibility

| Area | Effect |
| --- | --- |
| `src/mirrormind/domains/retail/` | New experimental offline projection. No generic package changes |
| `tests/unit/test_uci_retail_projection.py` | Unit/protocol/negative regressions on invented UCI-shaped mappings |
| `tests/integration/test_uci_retail_projection_flow.py` | End-to-end in-memory projection from an invented list; no real workbook |
| `docs/engineering/UCI_RETAIL_PROJECTION.md` | Source-by-source explanation, leakage and privacy limitations, independent exercise |
| Capability ledger and API | Explicit **experimental** capability ID; operational ingestion stays planned |
| WorldKernel | **Unchanged**, no cross-repository dependency |

## Scientific and security limitations

Transactions are not latent demand, inventory,
stockouts or lead times. Missing transaction
dates are not proven zero-sale dates.
The UCI schema has `InvoiceDate` as the event date,
**not independently verified historical publication
time**. Projection must not be accepted by the
existing as-of baseline stage without a future
separate trusted availability evidence policy.

A caller might already have read sensitive rows
before invoking this function; this local
projection cannot enforce upstream permission,
transport, memory clearing or app-wide logging.
A real XLSX reader needs its own data-rights
review, streaming/size caps, signed snapshot,
schema version and privacy tests.

## Verification

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
