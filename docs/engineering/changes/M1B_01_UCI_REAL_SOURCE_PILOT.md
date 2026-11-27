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
retain their existing contract; (6) synthetic tests cover all 52 single ASCII
letter prefixes, preserve one aggregate exclusion counter, and reject
non-ASCII or malformed forms. A real-source re-run is not useful under the
existing 250,000-group stop: MM-021 already excluded both cancellation and
unverified classes before grouping, so this classification clarification
cannot change accepted sales rows or group cardinality.

Impact map: `_normalize_uci_workbook_invoice` changes only the explicit UCI
reader; `project_uci_retail_rows` and generic callers do not change. The UCI
regressions remain in `tests/unit/test_uci_workbook.py`, including
`test_all_single_ascii_letter_prefixes_have_one_aggregate_exclusion_class`;
a lowercase-`c` compatibility case was added to
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

### MM-022 all-prefix regression and exact local gate — 2026-11-27

The owner reconfirmed that exact uppercase `C` is the only cancellation
marker. Commit `2413df151fd6baa9bb4de472c713519f2d69937c` covers all 52 single
ASCII-letter prefixes with synthetic XLSX fixtures: `C` is classified as
cancellation; all other prefixes are excluded as unverified under one
aggregate counter; identifiers are absent from returned results; and
non-ASCII or malformed values fail closed. This behavior is local to
`read_uci_workbook`; the generic projection contract is unchanged. The test
selector is
`tests/unit/test_uci_workbook.py::test_all_single_ascii_letter_prefixes_have_one_aggregate_exclusion_class`.

The exact candidate passed all six temporary local checks at
`2026-11-27T05:47:01.681022+00:00`: 867 tests, zero skips, Ruff, catalog,
atlas, evidence and capability checks. Python 3.13.5 used WorldKernel `0.0.1`
at reviewed source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`.
Receipt: `results/local-quality-gate-2413df151fd6baa9bb4de472c713519f2d69937c.json`.
The earlier restricted-executor run was interrupted and is not evidence; the
passing receipt is from the authorized local executor and is not official CI.

The real-source attempt was made under MM-021 and stopped above the approved
250,000 product-day ceiling. MM-021 already excluded cancellation and
unverified invoice prefixes before grouping; MM-022 therefore cannot change
the sales cohort or group count from that attempt. The workbook was not read
again. No complete projection, source-level exclusion count, metric or model
card exists. Do not retry, partition or widen the source call under current
approval. The local candidate was not yet published when this record was
written; the preceding remote PR #65 head was `6150bfd5dea03d68c5c840fc0e33acea995a7ad8`.

The documentation-inclusive candidate was subsequently published by
fast-forward as PR #65 head
`5c1835f8862bbe12b9028707cfa3b9d893b9eda6`. Its exact-head six-check local
gate passed at `2026-11-27T18:10:41.535466+00:00`: 867 tests, zero skips and
all six checks passed with the reviewed WorldKernel pin; receipt:
`results/local-quality-gate-5c1835f8862bbe12b9028707cfa3b9d893b9eda6.json`.
This remains local evidence, not Actions. The automatic test and catalog
runs failed with no job steps, logs or combined statuses returned by the
configured connector; the cause is undetermined and the owner's quota report
is separate. No official CI pass is claimed.

The later status-sync head `11de60127ab0b31b609d98ada1b764a3dde542f9` also
passed its exact local six-check gate at `2026-11-27T18:17:31.990456+00:00`:
867 tests, zero skips, all checks and the reviewed WorldKernel pin. Receipt:
`results/local-quality-gate-11de60127ab0b31b609d98ada1b764a3dde542f9.json`.
Its automatic test and catalog runs failed without steps, logs or combined
statuses; the cause is undetermined and the quota report remains separate.

## 7. Proposed fit-cohort hash sample — decision required

**Status:** proposal only. This method is not owner-approved, implemented,
tested or run against the private workbook. No source bytes were accessed
while preparing the proposal.

### Objective and scope

The current full-category projection exceeded the authorized
250,000 product-day group cap. A deterministic sample could make one bounded
retrospective evaluation possible while preserving the existing cap and
without changing generic readers. This proposal would reuse only the already
acquired UCI #352 snapshot, if the owner authorizes one additional local
processing attempt before the existing deletion deadline
(`2026-12-26T22:39:45Z`). It authorizes no download, external transfer,
retention extension, Census access, or commercial/customer-level use.

### Proposed selection and execution

1. Keep the current MM-022 invoice classifier, approved `StockCode`
   normalization, date interpretation, parser limits and fixed evaluator
   split. Select candidate categories only from positive, recognized sales
   rows in the existing fit interval, 2010-12-01 through 2011-08-30. Do not
   use validation or holdout values to define the sample.
2. Normalize each candidate category exactly as the UCI adapter already does.
   Rank it using SHA-256 of the bytes
   `b"MirrorMind/UCI352/fit-category-sample/v1\0" + key.encode("utf-8")`;
   retain the 500 lowest ranks. A digest collision
   between distinct keys must fail closed. The namespace, sample size and
   fit interval are fixed before the additional source read. This is a
   deterministic hash sample of fit-active categories, not a claim of
   population representativeness.
3. Add one bounded worksheet pass to discover the sample, then perform the
   existing projection pass for only those categories across the full
   publisher-reported date interval. The current worksheet scan used to find
   selected shared-string indexes remains. Enforce at most 600,000 data rows
   per pass and no more than three passes, for a maximum of 1,800,000
   row-visits. Keep the 32 MiB compressed input limit, 192 MiB member and
   224 MiB archive ceilings, 200:1 ratio, and 600,000 unique-row limit.
4. The manifest bounds the date range to 2010-12-01 through 2011-12-09,
   374 calendar dates inclusive. At most 500 sampled categories times 374
   dates yields 187,000 category-day groups, below the existing 250,000
   group ceiling. Still enforce that ceiling and fail closed if bytes,
   schema, dates, row counts or observed groups violate the reviewed bounds.
   Never return a partial projection after a failure.

The arithmetic is reproducible without reading the source:

```powershell
.\.venv\Scripts\python.exe -c "from datetime import date; days = (date(2011, 12, 9) - date(2010, 12, 1)).days + 1; print(days, 500 * days)"
```

Expected output: `374 187000`. This is a worst-case group bound, not an
observed source count.
5. Keep category keys and sample digests in process memory only. Emit the
   existing aggregate receipt and ordinal category summaries; emit no
   `StockCode`, hash digest, invoice ID, customer ID, description or row.
   Any result must say it is an event-time retrospective over the sampled,
   fit-active category cohort, with availability unverified and no SKU,
   full-population, causal or business-performance claim.
6. Run the existing fixed lag-7 and trailing-7 baselines on matched targets
   and the predeclared validation/holdout windows. Do not tune after seeing
   holdout results. Create a source-specific dataset/model card only after
   an approved evaluation returns complete results; report the sample
   denominator, exclusions, coverage and abstentions. No confidence
   interval or population estimate is proposed.

### Acceptance checks required before any authorized run

- Synthetic XLSX tests prove the selected fit category set is deterministic
  under row reordering and independent of mutations to validation/holdout
  rows; malformed invoice forms still fail closed.
- Tests prove a maximum of 500 fit-active categories, the 187,000-group
  mathematical bound, the existing 250,000 fail-closed guard, and the
  three-pass/1,800,000-row-visit limit.
- Tests and receipts prove sample digests and original category keys never
  leave the process, and public output contains only aggregate values and
  ordinals.
- The exact synthetic local quality gate passes before the owner-approved
  source run. The source run itself remains local, uses the existing snapshot
  and deletion deadline, and does not alter tests or bypass source controls.

### Owner decision

Approve or reject **one additional local processing attempt** using this
500-category fit-cohort hash sample on the existing snapshot, with the limits
above and no retention extension. Rejection leaves the real UCI lane closed;
the synthetic M1 path and separately reviewed Census/ALFRED protocol remain
available without acquiring data.

## 8. PR #65 review correction — duplicate and malformed OOXML cells

**Status:** confirmed and corrected on code head
`c6c1326be9332e51b160931de4dd994d54868793`; exact full-gate evidence is
recorded below. The documentation-inclusive gate and PR review response are
the remaining publication steps. No private source bytes were read for this
correction.

The owner-authored PR review reproduced three fail-open cases using generated
workbooks: appending duplicate coordinate `D2` changed a quantity of `2` to
`99`; an OOXML error cell (`t="e"`) with `SKU-X` was accepted as a category;
and malformed numeric text could fall back to a string category. The new
regressions failed before the fix: 13 selected cases failed, including
duplicates in header, selected and excluded cells, error/unknown selected
types, malformed numeric tokens and overflow. The numeric parameterization
then gained a nonzero-underflow case, which passes after the correction.

### Accepted correction and impact

- `_iter_worksheet_rows` tracks each `(row, column)` coordinate before
  selecting or decoding a cell. It rejects duplicates across the entire
  reviewed eight-column schema, including the excluded `Description` column.
  The same iterator is used for both worksheet passes. Its set is reset per
  row and retains at most eight coordinates.
- `_decode_cell` enforces per-field cell types: invoice and stock-code fields
  accept reviewed text or numeric encodings; `Quantity` accepts numeric cells;
  `InvoiceDate` accepts numeric serials or OOXML ISO date cells. Error/unknown
  types, formulas and invalid date/numeric encodings fail with fixed,
  redacted `ValueError` messages.
- Numeric cells must match a strict decimal/scientific grammar. Decimal
  parsing rejects non-finite values and detects float overflow or nonzero
  underflow before conversion. Malformed numeric payloads cannot become a
  valid-looking string category or identifier.
- The UCI-only MM-022 invoice policy and aggregate-only exclusion count remain
  unchanged. `uci_transactions.project_uci_retail_rows` and generic callers
  are unchanged. No capability, source permission, group/row ceiling or
  empirical claim changes.

### Reproduction, verification and limitations

The regressions are in
[`test_uci_workbook.py`](../../../tests/unit/test_uci_workbook.py):

- `test_duplicate_quantity_cell_is_rejected_instead_of_overwriting_original`
  reproduces the quantity overwrite and proves fail-closed behavior.
- `test_duplicate_header_selected_and_excluded_cells_fail_in_both_passes`
  covers duplicate header, selected and excluded coordinates in both scans.
- `test_error_and_unknown_selected_cell_types_fail_without_echo` covers error
  and unsupported types in invoice and stock-code fields.
- `test_malformed_numeric_cell_encodings_fail_without_becoming_stock_codes`
  covers text, underscore, overflow and underflow encodings without echoing
  values.

The 13 initially selected focused cases failed on the original implementation
and passed after correction; the added underflow parameter also passed. The UCI
workbook unit plus integration tests passed 65 cases. The exact clean code-head
six-check gate passed at `2026-11-27T19:19:54.200355Z`: 881 tests, zero skips,
Ruff, catalog, atlas, evidence and capability checks; Python 3.13.5 with
WorldKernel `0.0.1` from reviewed commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Passing receipt:
`results/local-quality-gate-c6c1326be9332e51b160931de4dd994d54868793-loopback.json`.
The sandbox timeout receipt is preserved separately at
`results/local-quality-gate-c6c1326be9332e51b160931de4dd994d54868793.json`.
An isolated reproduction located the sandbox wait at `test_health`; the same
test and complete gate passed in the loopback-capable local execution without
code or test changes. This is not official Actions and does not explain the
historical B-07 timeout. These fixtures prove parser behavior only; they do
not establish that the private workbook contains such anomalies, source
rights or hostile-file isolation. Do not reread the source under this
correction; the separate fit-cohort sampling proposal above still requires
owner approval. Rerun the exact gate on the documentation-inclusive head
before publication.
