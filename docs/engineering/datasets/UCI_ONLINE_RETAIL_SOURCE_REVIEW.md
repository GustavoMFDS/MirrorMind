# UCI Online Retail (352) — licensed-source candidate, not approved ingestion

**Review date:** 2026-11-24.
**Status:** `license-published / privacy-and-use-review-pending`.
**Operational decision:** **NO-GO** for unattended source downloads,
commit of transaction records, model training, customer-level
analytics or a claim of historically available forecasts until
the applicable attribution, privacy and provenance review is
signed off. This document records source information and
risk boundaries; it is not a legal opinion or access authorization.

## 1. Original evidence (not a third-party mirror)

| Item | Official source / directly visible evidence |
| --- | --- |
| Dataset | [UCI Online Retail (ID 352)](https://archive.ics.uci.edu/dataset/352/online-retail) |
| Citation / DOI | Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. [doi:10.24432/C5BW33](https://doi.org/10.24432/C5BW33) |
| License shown by UCI | [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) — UCI's official page explicitly labels **this dataset** CC BY 4.0 |
| Published license scope | CC BY 4.0 allows copying/adaptation, including commercial use, **provided its attribution, license link and change notice obligations are respected**; it does not waive unrelated privacy, publicity, contract, database or security obligations |
| File | UCI lists `Online Retail.xlsx`, about 22.6 MB; this is **larger** than the 1 MiB MirrorMind local parser budget |
| Rows and period | UCI reports 541,909 transactions, dated 2010-12-01 through 2011-12-09, for a UK non-store retailer |
| Source fields | `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country` |

These facts were rechecked on the official UCI page and the
official Creative Commons license summary on 2026-11-24.
They **do not imply** that all records are complete, that
customer-identifying fields are safe to redistribute,
or that the dataset contains inventory, lead times,
stockouts, counterfactual demand or source publication
history. The UCI page's dataset license statement
is stronger evidence than a license claim on a mirror,
but a reviewer must still confirm the intended
product processing and attribution requirements.

### Recheck evidence and limits

The [official UCI record](https://archive.ics.uci.edu/dataset/352/online-retail)
continues to list 541,909 transactions, event dates from 2010-12-01 through
2011-12-09, the 22.6 MB workbook and a CC BY 4.0 license. It gives a catalog
donation date of 2015-11-05; that date is not a row-level release timestamp or
evidence of when a forecaster could first observe each value. The visible
catalog metadata has no versioned publication vintages or source-byte digest.

The official [CC BY 4.0 deed](https://creativecommons.org/licenses/by/4.0/)
permits sharing and adaptation for any purpose, including commercially, when
its terms are followed. Attribution must include appropriate credit, a link
to the license and an indication of changes; the license forbids adding
restrictions to the licensed material. The deed also states that it may not
provide every permission needed for an intended use, including privacy or
publicity rights. UCI's license statement is therefore a useful license
source, but it does not complete customer-data, contractual or product-use
review.

The separate [Online Retail II record](https://archive.ics.uci.edu/dataset/502/online+retail)
lists 1,067,371 transactions, a 43.5 MB workbook and missing values. Keep its
license entry, snapshot and transformations separate from ID 352; it is not a
drop-in substitute.

No workbook was downloaded during this recheck. There is no acquired snapshot
hash, local acquisition timestamp or original-byte verification to record.
The visible UCI metadata describes transaction event time, not row-level
first availability or historical release revisions. Do not synthesize those
fields from `InvoiceDate`.

**Interim candidate recommendation:** retain UCI Online Retail ID 352 as the
preferred source for a future, narrowly scoped permission decision because
its original UCI record states the license. This is a review recommendation,
not permission to acquire, retain, transform or use the records. M5 remains
NO-GO pending its original terms. M1B-01 due diligence is complete; B-01 and
B-02 still gate any real-source adapter or empirical evaluation.

An alternative, longer version is
[UCI Online Retail II (ID 502)](https://archive.ics.uci.edu/dataset/502/online+retail)
with its own UCI-published CC BY 4.0 entry and
about 1.07 million transactions from 2009–2011.
**Do not silently mix the two datasets or their snapshots.**

## 2. Required human review before source adapter operation

- [ ] Verify the original UCI dataset page and linked CC BY 4.0
  license are still applicable to the exact downloaded file.
- [ ] Name an accountable reviewer and intended use:
  research-only, commercial product, or both.
- [ ] Plan and implement attribution for dataset
  source, authors, DOI, license, and transformed
  artifacts, including a changes notice.
- [ ] Review whether `CustomerID`, invoice IDs,
  description, price, country or other fields
  raise privacy or contractual restrictions.
  **Do not move customer IDs into MirrorMind's
  model inputs, prompts or CI fixtures.**
- [ ] Specify the minimal feature projection:
  product (`StockCode`), **transaction date**,
  signed/positive quantity and cancellation policy.
  Exclude all fields unnecessary for the approved task.
- [ ] Approve a local snapshot procedure with an
  independently recorded SHA-256, acquisition timestamp,
  storage scope, retention/deletion policy and no raw
  data committed to Git.
- [ ] Fix the train/test cutoff *before* any model tuning,
  record canceled invoices, invalid and missing keys,
  refunds, returns, possible duplicate rows and product
  coverage explicitly; do not silently count a return
  as negative demand or missing sales as zero demand.
- [ ] Distinguish `InvoiceDate` (transaction event time)
  from historical **first availability or release time**,
  which the UCI page does not supply at row level.
  Do **not** manufacture `available_on=InvoiceDate`
  and call that verified as-of provenance.
- [ ] Independent redacted acceptance tests and a
  complete [dataset card](../DATASET_CARD_TEMPLATE.md)
  must accompany a source-specific converter PR.

## 3. Why this data cannot directly feed today's parser

`read_staged_csv` accepts a **caller-opened**, at-most-1-MiB
CSV containing exactly:

```text
series_id,observed_on,available_on,units
```

The official UCI source is an approximately 22.6 MB
Excel workbook, not this daily CSV contract.
It contains transaction records including customer
and invoice identifiers. A future source-specific
adapter must be a **separate, opt-in and tested**
component that:

1. Opens a locally reviewed, approved, size-bounded
   workbook using a streaming parser and a
   snapshot hash from a trusted reviewed manifest.
2. Drops customer-level fields **before any output**
   and explains cancellation, quantity and aggregation
   semantics; it must not fabricate inventory or
   customer-level facts.
3. Records publication-time uncertainty explicitly.
   The event date is **not** documentary proof that
   the same value was knowable by a forecaster then.
4. Emits a deliberately bounded normalized daily
   subset with tracked transformations and a
   reviewed data card. Never invent or backfill
   missing dates to make the forecast work.
5. Keeps all real raw data **out of Git, example
   fixtures, model prompts and CI** unless a separate
   scoped data/privacy review explicitly approves
   the handling.
6. Marks results as **retrospective research under
   stated assumptions**, not production forecasts or
   policy-grade inventory decisions.

## 4. Scientific interpretation / no-go assumptions

A transaction ledger records sales/returns,
not true unconstrained customer demand, on-hand
stock, lost sales, supplier lead times, inventory
replenishment policy or causal intervention effects.

Historical **release vintages** are not equivalent
to transaction timestamps. Without a verified
feed availability schedule, MirrorMind should
not claim leakage-free real-time backtesting.
A legally usable snapshot can still be
scientifically unsuitable for a particular
forecasting claim.

## Next action

An accountable human reviewer should select the
specific intended research/commercial task and
approve the license attribution and data-minimization
plan. Then a separate source adapter PR can consume
only that approved local source, with negative tests
for mixed datasets, cancellations, time assumptions,
privacy fields, size limits and reproducible output.

**Current result:** a better-documented source
candidate with an official license statement.
**Not yet delivered:** downloaded/verified original
bytes, source-specific adapter, customer-data
review, real historical publication times,
held-out real-data predictive results,
calibrated uncertainty or WorldKernel integration.
