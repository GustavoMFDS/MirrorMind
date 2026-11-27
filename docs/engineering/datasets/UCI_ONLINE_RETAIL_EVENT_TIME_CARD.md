# Dataset card — UCI Online Retail #352 event-time study

**Status:** owner-approved local research scope; source acquired and metadata
preflighted; the corrected projection exceeded the approved 250,000 product-day
group cap and stopped fail-closed, so no evaluation was completed. This card is
not a legal opinion, general permission grant or empirical model card. Owner
clarification MM-024 confirms the conservative invoice classification but does
not change the accepted rows or group count; the empirical lane remains stopped
at the existing cap. Exact snapshot details are in the path-free
[manifest](UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json).

## Purpose and intended use

Prepare a local, research-only retrospective comparison of daily quantities
per `StockCode` category. The study evaluates forecasting baselines on
transaction event time. It does not validate physical-SKU demand, available stock,
lost sales, lead times or replenishment-policy quality. Commercial use is
outside this proposal.

The selected source is [UCI Online Retail #352](https://archive.ics.uci.edu/dataset/352/online-retail).
Do not substitute UCI Online Retail II #502 or combine snapshots. UCI lists
CC BY 4.0 for #352; applicability to the exact acquired bytes, attribution and
other obligations must be rechecked before acquisition. Removing identifiers
is a minimization measure, not proof of anonymization.

## Snapshot and acquisition record

| Field | Proposed value / current state |
| --- | --- |
| Dataset / source ID | UCI Online Retail / 352 |
| Author and citation | Chen, D. (2015), DOI `10.24432/C5BW33`; verify against the source page at acquisition time |
| License shown by publisher | CC BY 4.0; exact record, file URL, attribution and change notice were checked before this one local run |
| File name / format | `Online Retail.xlsx` inside the official `OnlineRetail.zip` archive |
| Source URL | Official UCI record and publisher-linked archive, recorded in the path-free manifest |
| Snapshot SHA-256 | Archive and workbook digests are recorded in the path-free manifest |
| Acquisition time / operator | UTC acquisition time recorded in the manifest; operator identity and local path omitted |
| Retained source version | Exact downloaded archive and workbook hashes recorded; no mixing with dataset #502 |
| Retention / deletion | Owner approved local retention up to 30 days; delete by the UTC deadline in the manifest and record verification. Source path remains outside Git under a private ACL. |

The archive and workbook sizes, publisher metadata comparison, ZIP bounds,
ACL and ignore verification are recorded in the manifest. The source was not
uploaded or sent to an external service.

No field in this table is filled with invented snapshot metadata. A future
private manifest should bind the exact source URL, bytes, SHA-256, acquisition
time, reviewed terms, intended use and deletion deadline. Do not commit the
manifest if it contains local paths or sensitive operational metadata.

## Proposed data minimization and transformation

The narrowly scoped adapter reads the approved workbook only inside the local
process. It keeps the minimum required fields long enough to classify invoice
IDs and aggregate:

- product category key (`StockCode`), transaction event date (`InvoiceDate`),
  `InvoiceNo` only as transient input to the reviewed cancellation rule, and
  signed `Quantity`;
- discard `CustomerID`, `Description`, `UnitPrice`, `Country`, invoice IDs and
  every other field before creating persisted or externally visible output;
- classify cancellation/return rows using a predeclared rule; do not treat a
  return as negative demand or silently discard it without a count;
- normalize only exact positive five-digit integer `StockCode` cells to their
  decimal string; preserve approved internal ASCII-space strings exactly as
  opaque category keys. Do not trim, filter or infer from `Description`;
- process exact six-digit integer/text invoice IDs; only uppercase `C` plus
  six digits is the cancellation class. Exclude lowercase `c` and every other
  single ASCII-letter plus six-digit ID as `unverified_invoice_prefix` before
  grouping, recording only the aggregate class count. Reject every other
  invoice format. Never retain an excluded identifier or use it to group,
  deduplicate or select rows. MM-022 and MM-024 supersede MM-021's
  lowercase-`c` rule. The owner confirmed this conservative exclusion policy
  on 2026-11-27. The stopped real-source attempt used MM-021; MM-024 confirms
  the current implementation, but the previous attempt excluded these rows
  before grouping, so the clarification cannot change its group-limit failure.
  No complete projection, exclusion count or metric exists;
- aggregate eligible positive quantities by `StockCode` category and calendar
  day, and emit only ordinal category summaries plus aggregate metrics;
- do not materialize a missing day as zero unless source completeness and
  date coverage are independently established and approved;
- record `event_time_retrospective_unverified_availability`; never set
  `available_on = InvoiceDate` or claim point-in-time replay.

These are owner-approved constraints for the one local scope. A `StockCode`
category is not verified to be a physical sellable SKU. The projection does not
capture `Description` cell text; the XML parser still scans the worksheet
structure while excluded-cell character callbacks are disabled. No raw
identifiers are persisted. Automated tests and the deterministic workbook
example remain synthetic-only.

The downloaded workbook metadata matched the published 541,909 rows and the
2010-12-01 through 2011-12-09 event-date range; required projection fields were
complete. Preflight found blank cells in excluded `CustomerID` and
`Description` fields even though the UCI record states no missing values. This
discrepancy is disclosed in the manifest. Excluded fields are not used for row
selection or evaluation.

The initial source attempts used a parser that transiently materialized
`Description` values before discarding them. This violated the minimized-read
boundary; no values were persisted or transferred. The implementation was
replaced by selective OOXML parsing, with a synthetic regression for shared
and inline strings. The corrected source call used that parser and stopped at
the approved group ceiling without returning a projection.

A later synthetic review found that duplicate cell coordinates could overwrite
an earlier selected value and that an OOXML error cell could be mistaken for a
valid category. The reader now rejects duplicate coordinates in every schema
column during both worksheet passes. It also validates field-specific cell
types and numeric lexical forms; error/unknown types, malformed numeric text,
overflow and underflow fail with fixed redacted errors. Added fixtures
reproduce each behavior, including a duplicate quantity changing `2` to `99`.
This parser hardening is based only on generated workbooks. It does not imply
that the private source contains duplicate cells, error cells or malformed
numeric values, and the real source was not reread.

## Fixed evaluation protocol prepared in PR #57

The study design is fixed before source inspection or model tuning:

1. Freeze the `StockCode`-category cohort using fit history ending 2011-08-30.
2. Use validation origins 2011-08-31 through 2011-09-30.
3. Lock one-day-ahead holdout origins 2011-10-01 through 2011-12-08, with
   targets through the catalog end date 2011-12-09.
4. Compare same-weekday lag-7 and trailing-seven-calendar-day baselines on
   identical eligible category/origin pairs.
5. Report MAE, RMSE, zero-safe WAPE, coverage, abstentions and the exact
   denominator. A zero target is eligible only if approved snapshot coverage
   proves the date complete; otherwise abstain.
6. Publish only aggregate metrics and ordinal category summaries. Do not tune
   on locked holdout results or claim that transaction event time was
   historically available.

The protocol is implemented and its regression fixtures remain synthetic.
The approved source preflight verified schema compatibility. After MM-020 and
MM-021, the corrected call applied the then-approved conservative invoice
classification but exceeded the 250,000 product-day cap. It returned no
partial projection and no metrics or model card were produced. MM-022 later
made uppercase `C` the sole cancellation marker and was verified with
synthetic tests only; the real source was not read again. Under MM-021,
lowercase-`c` rows were cancellations; under MM-022 they are unverified-prefix
exclusions. Both classes were already excluded before aggregation, so this
clarification changes aggregate classification counts only. It does not change
the recognized sales rows, product-day groups or the cap failure. The lane is
stopped at the unchanged 250,000-group ceiling. Excluding unverified
invoice-prefix rows can reduce category-day totals, change which categories
enter the fit cohort,
alter zero-valued targets, change coverage denominators and change downstream
scores relative to treating those rows as sales; the MM-022 relabeling alone
does not cause that change. Any future metric would describe only records with
recognized invoice IDs and must retain the single aggregate exclusion count.
Coverage would mean eligible pairs on dates declared complete by the UCI
snapshot assertion, using the recognized-ID cohort; it is not ledger
completeness. No metric may be compared with an inclusive run unless the
cohort and denominators are explicitly matched.
Synthetic regressions do not verify source rights, independent ledger
completeness or empirical predictive skill. See the [source
review](UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) and [event-time evaluator
evidence](../EVIDENCE_MAP.json).

## Privacy, security and permissions gate

For the approved UCI run, the owner authorized the narrow local scope and the
snapshot-specific controls recorded in the manifest. The corrected call
exceeded the approved group cap and stopped; this source lane must remain
closed unless a new scope decision authorizes another bounded method. Do not
retry, partition or raise the ceiling under MM-020.

The source and any intermediates remain subject to deletion by the manifest
deadline. No source rows, workbook bytes, local paths or identifiers may enter
Git, CI, fixtures, logs, prompts, support artifacts or external services.

No complete projection or evaluation has been produced. B-01 is stopped at the
current call ceiling; B-02 remains open because no publication-vintage evidence
exists. No external transfer or commercial use is authorized. M5 remains
NO-GO.

## Reproduction, tests and maintenance

Automated tests must use invented rows and generated in-memory workbooks. Run
the source projection, evaluator and workflow regressions described in
[`UCI_RETAIL_PROJECTION.md`](../UCI_RETAIL_PROJECTION.md),
[`M1_RETAIL_SYNTHETIC_EVALUATION.md`](../M1_RETAIL_SYNTHETIC_EVALUATION.md)
and [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57). A passing
synthetic test establishes only the implemented transformation on its fixture.

For a future source-specific change, preserve the source SHA and actual terms
review, add redacted negative tests for forbidden fields and cancellation
cases, regenerate the source catalog, update the atlas/evidence map and run
the six-check local gate on the exact clean head. Re-review this card if the
dataset version, intended use, projection or retention policy changes.
