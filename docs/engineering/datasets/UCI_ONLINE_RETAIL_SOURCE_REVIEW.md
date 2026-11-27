# UCI Online Retail (352) — approved local research scope and snapshot record

**Source review:** 2026-11-18; owner scope approval and exact snapshot
preflight: 2026-11-26.
**Status:** `approved_scoped_local_research / snapshot_preflighted / evaluation_blocked`.
The owner approved one local, non-commercial UCI #352 event-time run. This is
not a legal opinion or authorization for commercial use, customer-level
analysis, broad ingestion, model promotion, publication-time claims or another
source. The current parser fails closed after the product-day group limit is
exceeded; no complete projection or empirical metric exists.

## 1. Original evidence (not a third-party mirror)

| Item | Official source / directly visible evidence |
| --- | --- |
| Dataset | [UCI Online Retail (ID 352)](https://archive.ics.uci.edu/dataset/352/online-retail) |
| Citation / DOI | Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository. [doi:10.24432/C5BW33](https://doi.org/10.24432/C5BW33) |
| License shown by UCI | [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) — UCI's official page explicitly labels **this dataset** CC BY 4.0 |
| Published license scope | CC BY 4.0 allows copying/adaptation, including commercial use, **provided its attribution, license link and change notice obligations are respected**; it does not waive unrelated privacy, publicity, contract, database or security obligations |
| File | Official archive contains `Online Retail.xlsx`; the verified archive is 23,715,478 bytes and workbook is 23,715,344 bytes |
| Rows and period | UCI reports 541,909 transactions, dated 2010-12-01 through 2011-12-09, for a UK non-store retailer |
| Source fields | `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country` |

These source facts were checked on the official UCI page and the official
Creative Commons license summary on 2026-11-18, and rechecked before the
2026-11-26 acquisition.
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

## 2. Source-specific controls and completed checks

The owner approved this exact research scope on 2026-11-26. The accepted
license terms, attribution and change-notice obligation are recorded in the
[snapshot manifest](UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json). The source
is held outside Git in a private local directory; its path is deliberately
omitted from the manifest. Raw bytes and row-level intermediates must be
deleted no later than 30 days after acquisition.

The adapter uses only `InvoiceNo` transiently for the existing cancellation
rule, `StockCode` as an opaque category key, `Quantity` and `InvoiceDate` as
transaction event time. It never forwards `CustomerID`, `Description`,
`UnitPrice` or `Country` to projection or evaluation. `StockCode` normalization
is limited to exact positive five-digit integer cells and the approved source
strings containing internal ASCII spaces. Those results mean units per
`StockCode` category, not verified physical-SKU demand. Automated tests remain
synthetic-only.

The local metadata preflight matched the publisher row count, dates, sheet and
header. It found blank cells in excluded `CustomerID` and `Description` fields,
despite UCI's page saying there are no missing values. Required projection
fields were complete. The discrepancy is disclosed in the path-free manifest;
excluded values are not used to filter or group rows.

The initial real-source reader attempts used `openpyxl.iter_rows(values_only=True)`
and therefore materialized `Description` body values transiently before
discarding them. This did not satisfy the approved field-read boundary. The
values were not persisted or transferred externally; the old reader path was
removed and replaced with selective OOXML streaming. The corrected parser
does not pass excluded-cell character data to Python callbacks; Expat still
scans XML structure. A synthetic shared-string regression records callback
chunks and proves the excluded marker is absent from application-visible text.

The publisher describes invoice IDs as six-digit numbers and `C`-prefixed
cancellations. The exact workbook also contains at least one other
single-letter ASCII prefix followed by six digits. Under owner decision
MM-021, the UCI-only path treats six-digit IDs normally, retains `C`/`c`
cancellation handling, and excludes other single-letter prefixes into one
aggregate counter before grouping. Other invoice formats still fail closed;
the generic projection contract is unchanged. The original IDs are not
retained.

The owner clarified this rule in MM-022: exact uppercase `C` is the only
cancellation marker, while lowercase `c` joins other letter prefixes in the
unverified class. The owner confirmed the conservative, aggregate-only
exclusion policy on 2026-11-27. Synthetic regressions cover every single ASCII
letter prefix and fail-closed handling of other formats. The real-source
attempt used MM-021 and was not repeated because both cancellation and
unverified classes were excluded before grouping; the clarification cannot
reduce the observed product-day count. No complete exclusion count or
empirical metric exists.

A subsequent owner review reproduced three parser hazards with generated
workbooks: duplicate cell coordinates overwrote prior values, an OOXML error
cell could be interpreted as a valid `StockCode`, and malformed numeric text
could fall back into a category key. The adapter now rejects duplicate
coordinates in all schema columns in both worksheet passes, validates
field-specific types and numeric syntax, and emits only fixed redacted errors.
Regression coverage includes duplicate header, selected and excluded cells;
error and unknown selected types; and malformed, overflowing and underflowing
numeric tokens. This is synthetic evidence only. The private workbook was not
re-read and no source-level anomaly is asserted.

The preflight passed the owner-approved 192 MiB/member and 224 MiB/total ZIP
profile while retaining the generic 64/128 MiB defaults and the 32 MiB
compressed-input, 200:1 ratio and 600,000-row bounds. It stopped at the
unchanged generic 100,000 product-day group ceiling. The owner separately
approved a UCI-workbook-only explicit call cap of 250,000 groups; the default
remains 2,000 and generic callers are unchanged.

The following checklist is retained as pre-acquisition review history.

### Historical pre-acquisition checklist

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

The official UCI source is an Excel transaction workbook, not this daily CSV
contract.
It contains transaction records including customer
and invoice identifiers. A future source-specific
adapter remains a **separate, opt-in and tested**
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

## Current source state and next action

The source-specific local snapshot has been acquired and preflighted. Its
path-free manifest records the exact official artifact hashes, acquisition
time, metadata, approved resource profile and retention deadline. The initial
projection stopped at the generic 100,000-group ceiling. After MM-020 and
MM-021 implementation, one corrected call applied the approved invoice
classification and exceeded 250,000 product-day groups. It failed closed
without returning a partial projection, exact count, exclusion count or
metrics. The UCI lane is stopped at this bound. Do not retry, partition, alter
generic limits or process beyond the approved cap without a new owner scope
decision.

Even after a successful event-time run, there will be no verified
publication-time history. Keep the result label
`event_time_retrospective_unverified_availability`; B-02 remains open.

## 5. Owner-approved research lanes and temporal methods for B-01 / B-02

This section records the research lane order and evaluation contracts. UCI
approval is limited to the acquired local #352 snapshot and scope above. It
does not grant permission to retrieve Census/ALFRED or make a production
capability claim.

### A — UCI Online Retail #352 event-time retrospective

The selected source is UCI [Online Retail #352](https://archive.ics.uci.edu/dataset/352/online-retail),
not Online Retail II #502. Its `InvoiceDate` is transaction event time; no
row-level publication timestamp is supplied. The owner approved one
research-only event-time evaluation, including the local download and
processing within the reviewed limits. Removing `CustomerID` and `InvoiceNo`
is minimization, not proof of anonymization.

**Predeclared protocol:** freeze the `StockCode`-category cohort from fit
history only. Fit and
cohort end 2011-08-30; validation origins run 2011-08-31 through 2011-09-30;
locked one-day-ahead holdout origins run 2011-10-01 through 2011-12-08 with
targets through catalog end 2011-12-09. Compare same-weekday lag-7 and
trailing-seven-calendar-day baselines on identical eligible category/origin
pairs. Report MAE, RMSE, zero-safe WAPE, coverage and abstentions. A zero target
may be materialized only after a reviewed snapshot proves date coverage and
source completeness; otherwise abstain. Restrict output to aggregate metrics
and ordinal-only category summaries. Label all results
`event_time_retrospective_unverified_availability`; never create
`available_on` from `InvoiceDate`.

The adapter and regression tests from [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57)
operate only on synthetic fixtures. A separate approved local source preflight
verified workbook compatibility through schema and field validation; the
projection then refused at its generic group ceiling. No real-data evaluation
or predictive-skill result is available. Synthetic tests still do not prove
rights, source completeness or empirical behavior.

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

- **Accepted:** execute A before considering independent B; keep Census
  aggregate-only and UCI event-time retrospective. Automated tests remain
  synthetic. The UCI source has been acquired locally under the reviewed scope.
- **UCI stop condition reached:** after the approved invoice-classification
  policy was applied, the bounded reader exceeded the owner-approved 250,000
  product-day cap and failed closed. No projection or evaluation exists.
  Do not retry, partition, or raise the cap without a new owner decision.
  The source remains local/private until its recorded deletion deadline;
  never place raw or identifying data in Git, CI, logs, prompts or external
  services.
- **Still required before Census retrieval:** select exact aggregate series,
  release archive and geography; verify rights, source bytes, first-release
  versus revised-vintage semantics, availability timestamps and an immutable
  manifest. Do not reconstruct missing historical vintages from today's
  revised series.
- B-01 is scope-limited and stopped at the approved group bound; B-02 remains
  open because transaction event time is not publication availability and no
  Census vintage has been retrieved. Independent Census protocol preparation
  may proceed, but acquisition requires a separate exact source/vintage review.
  M5 remains NO-GO. No physical SKU demand or inventory-policy validation
  follows from either this UCI protocol or aggregate Census.

Owner direction is recorded in [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818)
and the 2026-11-26 decisions in the [scoped change request](../changes/M1B_01_UCI_REAL_SOURCE_PILOT.md).
**Current status:** A's approved bounded attempt was stopped at 250,000 groups;
no full projection or empirical result is claimed. B's aggregate-vintage
protocol is prepared, but no Census/ALFRED data has been acquired.
