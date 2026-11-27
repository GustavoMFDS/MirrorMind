# M1B-01 — owner-approved UCI #352 local event-time pilot

**Status:** approved scoped local research run; the ZIP profile, source-specific
`StockCode` normalization, group ceiling and invoice-prefix classification are
implemented and published in [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65)
for independent review. Its exact head passed the temporary local gate. The
corrected source call exceeded the approved 250,000 group cap and failed closed
without a projection or evaluation. Do not retry, chunk or widen that cap
under this scope. This approval does not
promote an API capability, authorize commercial use, or establish
point-in-time availability.

## 1. Goal in plain language

**Current behavior:** PR #62 integrates a deterministic synthetic workbook,
the bounded `read_uci_workbook` projection, and the fixed
`evaluate_uci_event_time` protocol. Tests never load publisher data. The reader
does not establish rights; the evaluator labels its results retrospective and
keeps `point_in_time_eligible=false`.

**Desired behavior:** Run that existing path once against the exact official
UCI Online Retail #352 workbook, after validating the source bytes against the
reviewed schema and finite limits. Keep the snapshot local and access-controlled.
Retain only its SHA-256, a path-free approved manifest, aggregate metrics, and
ordinal category summaries. Delete the source and any row-level intermediates no
later than 30 days after acquisition.

**Why:** M1 requires an actual approved source run in addition to synthetic
regressions. The fixed event-time benchmark can test the implementation on
real published rows, while the data source provides no row-level publication
timestamps and cannot support historical as-of claims.

**Out of scope:** Census/ALFRED data acquisition (independent protocol
preparation may continue after the documented UCI stop); M5; commercial or customer-level analysis; API ingestion; model training or
promotion; inventory or policy claims; WorldKernel; external data transfer;
and any change to automated-test fixtures (they remain synthetic).

## 2. Approval and acceptance criteria

The project owner authorized this exact scope in the Codex conversation on
2026-11-26:

- UCI Online Retail dataset #352 only; local, non-commercial research.
- Respect the publisher's CC BY 4.0 attribution, license link, and change
  notice requirements. This is an operational scope decision, not a legal
  opinion or a grant of rights beyond that source and intended use.
- Use a private local snapshot. Keep raw source bytes and row-level
  intermediates out of Git, CI, logs, prompts, and external services.
- Use only the reviewed minimal projection. Under the current MM-022 rule,
  process exact six-digit integer/text invoice IDs normally; only uppercase
  `C` plus six digits marks cancellation. Exclude lowercase `c` and other
  single ASCII-letter plus six-digit forms before aggregation and report only
  one aggregate class count. All other formats fail closed. Never retain
  identifiers. `CustomerID` is never used by the projection, evaluator, output
  or tests. Aggregate by the required
  product key and event date; expose only aggregate receipts and stable
  product ordinals.
- The owner separately approved a source-specific bounded archive profile:
  192 MiB per uncompressed member and 224 MiB total. Keep the existing 64 MiB
  and 128 MiB defaults for every unconfigured caller; preserve the 32 MiB
  compressed-input limit, 200:1 compression-ratio limit, 600,000-row ceiling
  and 100,000-group ceiling for generic row projection. The reader retains its
  2,000 default; the owner separately approved a UCI-workbook-only explicit
  per-call ceiling of 250,000 groups. Stop fail-closed above that cap.
- The owner approved faithful `StockCode` normalization for this workbook:
  convert only exact positive five-digit integer cells to their decimal string
  without padding, and preserve internal ASCII-space strings exactly as
  opaque keys. Do not trim, filter, inspect `Description`, or merge keys. The
  result describes units per `StockCode` category, not physical SKU demand.
- MM-022 clarifies the invoice rule for the UCI reader: process exact
  six-digit integer/text invoice IDs; only uppercase `C` plus six digits is a
  cancellation. Exclude lowercase `c` and other single ASCII-letter plus
  six-digit identifiers as one unverified transaction class before sales
  aggregation. Record only its aggregate count; never retain identifiers.
  Every other format fails closed. This exception is private to the approved
  UCI workbook path; generic row projection behavior remains unchanged.
- Delete source bytes and any row-level intermediate within 30 days. The run
  must record a deletion deadline and later verify deletion.
- The approved UCI workbook call may explicitly select at most 250,000 groups
  under MM-020. Direct/generic projection calls remain capped at 100,000;
  defaults remain 2,000. The corrected call exceeded the approved UCI limit,
  so no projection or metrics exist. Do not retry, partition or raise the
  limit without a separate scope decision.
- Preserve the fixed split and baselines; do not tune on the holdout. Retain
  the `event_time_retrospective_unverified_availability` label and never set
  `available_on` from `InvoiceDate`.
- Process no other source and do not begin Census before this UCI lane reaches
  a documented stop or completion state.

## Approved clarification MM-022 — 2026-11-27

The owner's later instruction makes uppercase `C` the sole cancellation
prefix. Lowercase `c` is now grouped with other ASCII-letter-plus-six-digit
forms as an unverified transaction class. This supersedes only MM-021's
case-insensitive prefix rule. No source read, retry, chunking or limit change is
authorized by this clarification.

Acceptance criteria: (1) the UCI workbook reader treats exact uppercase `C`
plus six digits as cancellation; (2) lowercase `c` and other single ASCII
letters plus six digits are excluded before aggregation and increment only the
aggregate unverified-class count; (3) original IDs do not appear in results or
errors; (4) all other malformed forms fail closed; (5) generic projections
retain their existing contract; (6) synthetic tests cover the uppercase and
lowercase cases. A real-source re-run is prohibited under the existing
250,000-group stop.

Impact map: `_normalize_uci_workbook_invoice` changes only the explicit UCI
reader; `project_uci_retail_rows` and generic callers do not change. The UCI
regression remains in `tests/unit/test_uci_workbook.py`; a lowercase-`c`
compatibility case was added to
`tests/unit/test_uci_retail_projection.py::test_invalid_invoice_format_does_not_get_treated_as_regular_sale`.
Evidence IDs MM-XLSX-006 and MM-XLSX-007 cite these tests. Reader/projection
walkthroughs, dataset card, decision log, status, debugging and learning
materials explain the revised rule. No
public capability, external contract, source permission, metric or group
budget changes. If an invoice value falls outside the reviewed ASCII-prefix
shape, the reader raises the existing redacted `ValueError` without echoing
the value.

Before processing, verify the official UCI terms and exact artifact URL again.
Stop if the archive layout, workbook sheet/header, row count, fields used by
the projection, required cell types, approved ZIP caps, product/group bounds,
or source date coverage conflict with this reviewed contract. Do not widen
the bounds or add a new normalization rule without a separate owner decision.
Record catalog missingness claims against the exact artifact. Missing cells in
excluded fields are reported but never used to filter rows, group results, or
change the approved projection; missingness in a required field is a parser
failure.

The evaluator's all-days coverage input is justified only by the UCI publisher
description that the dataset contains all transactions in its stated date
range. Record this as a publisher completeness assertion, not an independently
audited retailer ledger. If the artifact contradicts the stated range or its
schema, stop. If completeness cannot be supported from the official metadata,
abstain for uncovered days instead of synthesizing zeros.

## 3. Impact map

| Layer | Relevant file/symbol | Change | Evidence |
| --- | --- | --- | --- |
| Bounded parsing | [`uci_workbook.py`](../../../src/mirrormind/domains/retail/uci_workbook.py)::`read_uci_workbook`; [`uci_xlsx_xml.py`](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py)::`iter_uci_projection_rows` | Add separately bounded per-call ZIP/group ceilings, disable Python character callbacks for excluded cells, normalize exact five-digit integer cells, preserve internal-space keys and classify source-specific invoice forms; retain network/path-free behavior | Synthetic tests cover defaults/override bounds, shared-string and inline-string selection, invoice classification, exact normalization, rejection and redaction; approved snapshot preflight and capped stop are in the path-free manifest |
| Projection | [`uci_transactions.py`](../../../src/mirrormind/domains/retail/uci_transactions.py)::`project_uci_retail_rows` | Keep the public generic row contract strict; only the UCI reader passes a private sentinel for the authorized unknown-prefix exclusion | Synthetic classification/count regressions; no complete real-source counters survived the capped call |
| Temporal evaluation | [`uci_event_time.py`](../../../src/mirrormind/domains/retail/uci_event_time.py)::`evaluate_uci_event_time` | Reuse fixed validation/holdout windows, caller-declared coverage and up to 250,000 UCI groups; preserve recognized-ID target semantics | Synthetic split/leakage/redaction regressions; no real-source evaluation result was produced |
| State/API | None | No API, database, persistent row store, capability promotion, or production route | Capability ledger remains unchanged |
| External project | None | No Census or WorldKernel change | Project boundaries unchanged |
| Human-written docs | Source review, dataset/model cards, system map, debugging, learning, status/backlog/blockers/handoff | Record the approval, actual source facts, reproduction, limits and deletion evidence | Docs checks and independent review |

## Data, model and decision review

- Dataset card: [UCI #352 event-time card](../datasets/UCI_ONLINE_RETAIL_EVENT_TIME_CARD.md).
- Source and terms: [UCI source review](../datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md).
- Model card: create a real-source card only after a complete verified evaluation; until then the [synthetic model card](../model_cards/SYNTHETIC_UCI_EVENT_TIME.md) is the only completed score record.
- Snapshot manifest: [path-free UCI #352 record](../datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json); it records the current fail-closed stop, not evaluation evidence.
- Temporal meaning: transaction event time only; no first-publication history.
- Decision trace: not applicable; this run emits benchmark metrics, not a recommendation or action.
- WorldKernel gate: not applicable; no simulation occurs.

## 4. Constraints, privacy and rollback

Use the existing optional XLSX extra and explicit bounded limits. Do not print
source values, row snippets, customer IDs, invoice numbers, product codes,
local paths, or parser/library exceptions containing input. Store the raw
archive only in a private local directory whose ACL is checked; verify Git
ignore status before downloading. Keep no raw workbook in `results/` or the
repository. Do not add a real-data test, fixture, CI download, analytics call,
or network service. The only surviving outputs are an approved metadata
manifest (without local path), source SHA-256, aggregate counters/metrics, and
stable ordinal summaries.

Rollback requires deleting the local source and intermediates, retaining only
the approved aggregate evidence, and correcting the status if validation or
evaluation did not pass. No code migration is required because the pilot
reuses existing contracts. Reconsider the change request before a new source,
intended use, projection, retention period, or point-in-time claim.

## 5. Verification plan

1. Verify official UCI record, CC BY 4.0 link, attribution, file URL, current
   row/date/schema metadata and the owner-approved scope.
2. Create a private local destination, verify ACL and `.gitignore`, download
   only the official archive, compute archive/workbook SHA-256 and acquisition
   time, and set a deletion deadline no later than day 30.
3. Compare archive and workbook structure to the approved finite bounds;
   preserve the stricter default profile for other callers. Apply only the
   owner-approved `StockCode` and invoice-classification rules. The first
   approved call stopped at 100,000 groups. The corrected call applied MM-021
   and exceeded 250,000 groups, stopping without a partial projection,
   complete exclusion count or metrics. Do not retry, chunk or raise the cap
   under this scope; another method requires a separate owner decision.
4. The stopped attempt produced no projection or evaluation output. Keep the
   private source only within its approved retention window and verify deletion
   by the manifest deadline. Any future authorized output may contain only
   aggregate counters and ordinal summaries and must retain the
   point-in-time/non-promotion limitations.
5. Keep automated tests synthetic. Run the full exact-clean-head local gate
   under [`LOCAL_QUALITY_GATE.md`](../LOCAL_QUALITY_GATE.md); this is not
   official Actions. Obtain independent review before publication or merge.

## 6. Evidence after implementation

- Commit / PR: [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65),
  open and awaiting independent review, head
  `75da34fc2cb91d3354cfbe49af43aeb40721164d`, based on main
  `a456034c55ed7634ad4768b26788fec09dab1d08`. No PR is represented as merged
  or accepted by this local snapshot record.
- Modified symbols: `read_uci_workbook`, `_normalize_uci_workbook_invoice`,
  `iter_uci_projection_rows`, the selected OOXML/shared-string streaming
  helpers, the private projection sentinel and UCI-only group ceiling, and
  event-time group/target semantics. No API or capability entry changes.
- Exact source URL, archive/workbook SHA-256, acquisition time, source
  assertions, privacy metadata, current stop reason and deletion deadline:
  recorded in the path-free manifest. No aggregate evaluation counts, split
  metrics or empirical model card exist.
- Tests: 114 focused UCI workbook/projection/evaluator/CLI tests passed after
  MM-021; a later focused reader/projection/event-time/workbook-flow rerun
  passed 112 tests. The exact final PR head
  `75da34fc2cb91d3354cfbe49af43aeb40721164d` passed the complete local gate
  at `2026-11-27T00:38:35.670136Z`: 863 tests, zero skips, all six checks
  (pytest, Ruff, catalog, atlas, evidence and capabilities). Python 3.13.5;
  WorldKernel `0.0.1` installed from reviewed commit
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; one existing Starlette/httpx
  deprecation warning. Receipt:
  `results/local-quality-gate-75da34fc2cb91d3354cfbe49af43aeb40721164d.json`.
  This is local evidence, not Actions. The real-data call exceeded its bound;
  never claim the source attempt as a completed projection or test.
- Official Actions: unavailable under B-08; no CI claim.
- Known limitation: event-time metrics do not establish when observations
  became available, latent demand, stockouts, lead times, causal effect,
  commercial suitability, or general forecast performance.
