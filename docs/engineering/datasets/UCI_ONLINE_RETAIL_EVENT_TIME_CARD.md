# Proposed dataset card — UCI Online Retail #352 event-time study

**Status:** proposal only; no source file acquired or processed. This card
records the reviewed scope and the controls needed before a source-specific
run. It is not a license opinion, permission grant, immutable snapshot record
or empirical model card.

## Purpose and intended use

Prepare a local, research-only retrospective comparison of product-level daily
positive-quantity proxies. The study evaluates forecasting baselines on
transaction event time. It does not validate latent demand, available stock,
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
| License shown by publisher | CC BY 4.0; exact file terms and attribution still require source-specific review |
| File name / format | Publisher lists `Online Retail.xlsx`; no local file acquired |
| Source URL | Official UCI record linked above; capture final download URL only in a private local manifest |
| Snapshot SHA-256 | Not available; must be computed from approved bytes before parsing |
| Acquisition time / operator | Not available; must be recorded locally with the manifest |
| Retained source version | Not selected; never infer it from a filename alone |
| Retention / deletion | Owner decision required. Proposal: keep the raw workbook only in access-controlled local storage for the approved study window, delete it when the study closes, and retain no source rows in Git, CI, logs, prompts or external services. Set an explicit maximum retention period before acquisition. |

No field in this table is filled with invented snapshot metadata. A future
private manifest should bind the exact source URL, bytes, SHA-256, acquisition
time, reviewed terms, intended use and deletion deadline. Do not commit the
manifest if it contains local paths or sensitive operational metadata.

## Proposed data minimization and transformation

The narrowly scoped adapter may read the publisher workbook only after the
source and privacy review is approved. Keep the minimum required fields inside
the trusted local process long enough to classify cancellations and aggregate:

- product key (`StockCode`), transaction event date (`InvoiceDate`),
  `InvoiceNo` only as transient input to the reviewed cancellation rule, and
  signed `Quantity`;
- discard `CustomerID`, `Description`, `UnitPrice`, `Country`, invoice IDs and
  every other field before creating persisted or externally visible output;
- classify cancellation/return rows using a predeclared rule; do not treat a
  return as negative demand or silently discard it without a count;
- aggregate eligible positive quantities by product and calendar day, and
  emit only ordinal product summaries plus aggregate metrics;
- do not materialize a missing day as zero unless source completeness and
  date coverage are independently established and approved;
- record `event_time_retrospective_unverified_availability`; never set
  `available_on = InvoiceDate` or claim point-in-time replay.

The exact projection, cancellation classification, field lifetime, storage
location and deletion evidence remain approval gates. The existing automated
tests and deterministic workbook example must remain synthetic-only.

## Evaluation protocol prepared in PR #57

The study design is fixed before source inspection or model tuning:

1. Freeze the product cohort using fit history ending 2011-08-30.
2. Use validation origins 2011-08-31 through 2011-09-30.
3. Lock one-day-ahead holdout origins 2011-10-01 through 2011-12-08, with
   targets through the catalog end date 2011-12-09.
4. Compare same-weekday lag-7 and trailing-seven-calendar-day baselines on
   identical eligible product/origin pairs.
5. Report MAE, RMSE, zero-safe WAPE, coverage, abstentions and the exact
   denominator. A zero target is eligible only if approved snapshot coverage
   proves the date complete; otherwise abstain.
6. Publish only aggregate metrics and ordinal product summaries. Do not tune
   on locked holdout results or claim that transaction event time was
   historically available.

The protocol is implemented against synthetic fixtures and is integrated in
`main` through PR #62, which incorporated PR #57. Synthetic regressions verify
transformation and metric rules; they do not verify actual workbook
compatibility, rights, source completeness or predictive skill. See the
[source review](UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) and
[event-time evaluator evidence](../EVIDENCE_MAP.json).

## Privacy, security and permissions gate

Before downloading or processing real bytes, an accountable reviewer must:

- recheck the original UCI terms, attribution, license link and change notice
  for the exact snapshot and intended local research use;
- approve the field projection, cancellation rule, access-controlled storage,
  retention deadline and deletion process;
- approve a private source manifest with hash and acquisition time;
- confirm that raw rows, workbook bytes, local paths and identifying fields
  cannot enter Git, CI, test fixtures, logs, prompts, support artifacts or
  external services;
- complete and review this card and the forecast model card before running
  the approved study.

The project owner has approved preparing this card and adapter design only.
No real source acquisition, processing, external transfer or commercial use
is authorized here. B-01 and B-02 remain open; M5 remains NO-GO.

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
