# UCI Online Retail (352) — licensed-source candidate, not approved ingestion

**Review date:** 2026-11-18.
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

These facts were checked on the official UCI page and the
official Creative Commons license summary on 2026-11-18.
They **do not imply** that all records are complete, that
customer-identifying fields are safe to redistribute,
or that the dataset contains inventory, lead times,
stockouts, counterfactual demand or source publication
history. The UCI page's dataset license statement
is stronger evidence than a license claim on a mirror,
but a reviewer must still confirm the intended
product processing and attribution requirements.

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

Owner approved preparing a narrow, local research adapter and a separate
aggregate temporal-method protocol. This is not approval to acquire or process
the real workbook. Before any source bytes are handled, complete the exact
terms, attribution/change notice, field-minimization, secure storage,
retention/deletion and manifest checks above and obtain source-specific
approval. Automated tests remain synthetic-only.

**Current source state:** the UCI event-time evaluator from draft PR #57 is
present in the local M1 integration candidate; no real file was acquired. The local 1 MiB XLSX
reader still cannot process UCI's complete 22.6 MB workbook, so a separately
reviewed bounded streaming path would be required before full-file use.
Unverified publication time, empirical performance and source permission are
not delivered.

## 5. Owner-approved preparation plan for B-01 / B-02

This section prepares a source and temporal-method decision. It grants no
permission to download data or make a real-source capability claim.

### A — UCI Online Retail #352 event-time retrospective

The selected source is UCI [Online Retail #352](https://archive.ics.uci.edu/dataset/352/online-retail),
not Online Retail II #502. Its `InvoiceDate` is transaction event time; no
row-level publication timestamp is supplied. The owner approved preparation
of research-only event-time evaluation, not real workbook acquisition or
commercial use. Removing `CustomerID` and `InvoiceNo` is minimization, not
proof of anonymization.

**Predeclared protocol:** freeze product cohort from fit history only. Fit and
cohort end 2011-08-30; validation origins run 2011-08-31 through 2011-09-30;
locked one-day-ahead holdout origins run 2011-10-01 through 2011-12-08 with
targets through catalog end 2011-12-09. Compare same-weekday lag-7 and
trailing-seven-calendar-day baselines on identical eligible product/origin
pairs. Report MAE, RMSE, zero-safe WAPE, coverage and abstentions. A zero target
may be materialized only after a reviewed snapshot proves date coverage and
source completeness; otherwise abstain. Restrict output to aggregate metrics
and ordinal-only product summaries. Label all results
`event_time_retrospective_unverified_availability`; never create
`available_on` from `InvoiceDate`.

The adapter and regression tests on draft [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57)
operate on synthetic fixtures. The official workbook exceeds the existing
parser's row/group bounds and would require a separately reviewed bounded
streaming adapter. A synthetic test proves projection/evaluation behavior,
not rights, source completeness, actual workbook compatibility or real-data
predictive skill.

### Option B — Census MARTS release-vintage method pilot

The U.S. Census Bureau publishes advance and monthly retail release schedules.
Its methodology states that advance national retail estimates appear about
ten business days after the reference month and are revised about one month
later by the larger monthly survey. Those products are monthly U.S. industry
aggregates, not SKU demand, store inventory, or supplier lead times. The
[release schedule](https://www.census.gov/retail/release_schedule.html) and
[MARTS methodology](https://www.census.gov/retail/marts/how_surveys_are_collected.html)
make this a candidate for testing temporal controls, not for validating the
retail policy or WorldKernel mapping.

Before a pilot, locate and preserve the actual first-release value file for
each selected month. A published release date alone does not prove that the
retained historical value is the first release. Record source URL, file bytes
and SHA-256, release timestamp/time zone, retrieval time, revision relation,
series definition and transformation. Where vintages are absent, do not
reconstruct them from today's revised series. [ALFRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html)
describe retrieval by historical knowledge period and may be evaluated as an
alternative vintage source; no API key, access or download is assumed here.

### B — aggregate Census temporal protocol

1. Select one aggregate series and geography, one to three monthly forecast
   horizons, and first-release or revised-final target semantics before
   inspecting holdout performance.
2. Preserve a chronological final holdout of the latest 12–24 eligible
   months, subject to source history and vintage completeness. Use expanding
   origins strictly before that holdout; never shuffle timestamps.
3. At each origin, expose only feature values whose documented release
   timestamp is no later than that origin. Keep reference month and release
   time as separate fields. Do not fill missing targets with zero.
4. Compare against matched seasonal-naive (lag 12) and trailing-three-month
   mean baselines on the same eligible origins. Report MAE, RMSE, MASE where
   defined, coverage, excluded origins, and target vintage. Freeze the split
   and baseline before model tuning; report uncertainty separately and do
   not infer inventory-policy quality from aggregate sales.
5. Store an immutable vintage manifest and dataset card before any run. Use
   free official archived releases first. ALFRED remains conditional on free
   authorized access, series terms and adequate historical-vintage evidence;
   no paid credentials or service are assumed. Retrieve only after a reviewer
   approves rights, terms, retention and exact research-only scope.

### Decision recorded and remaining permission gates

- **Accepted:** prepare A followed by independent B; keep Census aggregate-only
  and UCI event-time retrospective. Synthetic tests remain mandatory and no
  source bytes or credentials are in scope.
- **Still required before UCI processing:** verify original terms and
  attribution/change notice, approve exact field projection and cancellation
  classification, secure local storage, retention/deletion, exact snapshot
  manifest and dataset card. No raw/identifying data in Git, CI, logs, prompts
  or external services.
- **Still required before Census retrieval:** select exact aggregate series,
  release archive and geography; verify rights, source bytes, first-release
  versus revised-vintage semantics, availability timestamps and an immutable
  manifest. Do not reconstruct missing historical vintages from today's
  revised series.
- B-01/B-02 remain open for source authorization and point-in-time acceptance.
  M5 remains NO-GO. No SKU-level demand or inventory-policy validation follows
  from an aggregate Census series.

Owner direction is recorded in [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818).
**Current status:** A's synthetic evaluator is present on the local candidate;
B's protocol is prepared. Neither source was downloaded, no source-specific
processing approval was granted and no empirical result is claimed.
