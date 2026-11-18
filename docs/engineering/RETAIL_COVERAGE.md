# MM-M1b — internal retail product-day coverage (experimental)

## Purpose and trust boundary

The pure `summarize_retail_coverage` function in
[`coverage.py`](../../src/mirrormind/domains/retail/coverage.py)
consumes a bounded `UciRetailProjection` generated from fictional UCI-shaped
transactions. It counts **internal absent calendar dates per product** between
two strictly positive observed product-days. It does not generate absent rows,
fill gaps with zero, treat absence as a stockout or infer latent demand.

An event day is **not** a verified publication day. The output is unsuitable
for historical as-of training, policy optimization or the WorldKernel gateway
until a separate source-authorized adapter supplies trustworthy availability
and a validated interpretation of missingness.

## Contract and observables

- Input: a `UciRetailProjection` with at most 2,000 product-day groups,
  bounded positive integer units and strictly increasing dates per product.
- Output: frozen aggregate counts for observed product-days, distinct products,
  internal missing product-days, products with gaps and min/max event day.
- Receipt: explicit `not_authorized` status and unknown publication time.
  It omits stock codes, invoices, customer IDs, prices and descriptions.
- No zero generation: cancellation-only, negative-return-only and zero-quantity
  invoice lines do **not** become observed zero-day records.
- No invented exterior window: days before a product's first observed positive
  transaction and after its last one are outside the counted gap interval.
- A product observed once contributes zero **internal** gaps. This is not
  evidence of continuous availability or any complete collection period.
- The function checks input shape, positive units, cumulative unit budget and
  repeated/reversed dates, including directly constructed projections.
  It does not independently authenticate original rows or source rights.

## Reproduce with fictional data

```bash
python -m pytest -q tests/unit/test_retail_coverage.py
python -m pytest -q
python -m ruff check src tests
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

Claim **MM-RCOV-001** is grounded in
`tests/unit/test_retail_coverage.py` and the focused test
`tests/unit/test_retail_coverage.py::test_internal_gaps_are_not_zero_or_imputed_and_receipt_has_no_identifiers`
constructs two products. Product A has positive records on January 1 and 4;
January 2 has a cancellation and January 3 a negative return. The result
reports two *unobserved* internal product-days, not two zero-demand days.
Product B contributes only January 2 and therefore no internal gaps.

Other regressions cover empty projected days (all excluded lines), uncertain
first/last boundaries, duplicate or reversed dates, invalid unit types and
immutability. These tests do not constitute real-dataset or empirical model
validation.

## Remaining decision gates

Before real use, document the original source rights, attribution, privacy
and retention; independently verify snapshot provenance and historical release
times; identify which stock codes denote merchandise; establish whether
no recorded positive sale means closed shop, no demand, stockout, missing
reporting or another cause; and define an observation calendar from an
authorized source. No production, forecast or simulation capability is
promoted by this change.

## Guided review exercise

Add a sale on January 3 in the invented fixture: missing internal product-days
should fall from two to one. Add only a return on January 3: the count must
remain two. Explain why both behaviors are consistent with the explicit
positive-invoice-line proxy but insufficient to determine genuine demand.
