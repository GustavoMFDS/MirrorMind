# MirrorMind — system map

Updated against current `main` `00e6cf11ac05a94055242573fd3cfc18086bad10` on 2026-11-28. PR #88's exact main commit has 11 successful official check-runs. The M2-03 branch is ancestry-synced with that baseline through merge `66b591317b375a270b5d0ed682c94e161d52a956` and remains open as PR #87. Previous published candidate `b931bbe2279dd0865f535e0f56e5165ed402ef96` passed 1,014 local tests, zero skips and six checks; its exact official result was 12 successes and two conditional skips. Independent review reproduced Pydantic `model_copy(update=...)` bypasses in nested provider turns. The current PR candidate adds plain-data reconstruction and strict validation before dispatch or draft handling, with five regression cases; exact current gate evidence and official check state are in the live PR. Local container smoke remains unavailable because this host has no Docker engine; evidence is always SHA-scoped. The approved UCI source call stopped above the unchanged 250,000 product-day-group ceiling without a projection or metric. No authenticated RBAC, public agent route, live provider, production data permission, deployment or empirical forecast is claimed.




## Current request path

HTTP request → `src/mirrormind/api/app.py` → thin routes `api/routes/system.py`, `api/routes/scenarios.py` or `api/routes/decisions.py` → validation and service composition → response. The decision route uses generated fixture bytes and the in-process test double. Separately, trusted local CLI composition can send either an explicitly mapped `ScenarioSpec` through M1E-02 or an M1E-03 policy request through M1E-04 to the fixed, optional WorldKernel worker. These paths are not reachable from HTTP.

The local retail policy test double remains the default library/CLI path: a
caller supplies a strict 28-day profile and inventory/cost assumptions to
`domains/retail/policy_simulation.py`; the shared transition generates paired
demand streams, compares three rules and reports lead-time sensitivity. M1E-04
reuses that transition inside a fixed WorldKernel handler, then validates all
engine states and metrics against the in-process reference. M1F-02 composes
generated evidence and the test double through the experimental HTTP route;
only the CLI can explicitly select WorldKernel. No path grants decision
authority.

The local M2-03 orchestration path is separate from HTTP: a strict request
enters a bounded synchronous loop, admits only the fixed scripted test-double
mode, invokes an immutable registry of fictional retrieval and M1F-02 decision
tools, and emits digest-only receipts plus an untrusted draft for human review.
After each provider turn, the orchestrator serializes the exact `AgentTurn` to
plain data and strictly reconstructs it before dispatch or final-draft handling;
this re-runs nested field and model validators that `model_copy(update=...)`
would otherwise bypass. The adapter statically describes the internal M1F-02
fields it consumes; Pydantic contracts continue to validate the trace and
provider-visible result at runtime. Prompt-like retrieved text remains
untrusted data; it cannot extend the registry. This path has no network
provider, persistent state, public route, write capability or business-action
authority. Citation validation checks observed-reference membership, not
semantic entailment. See the [M2-03 walkthrough](M2_TOOL_ORCHESTRATION.md).

The separate UCI event-time CLI builds a deterministic workbook in memory,
passes it through the bounded XLSX reader and product-day projection, then
calls `evaluate_uci_event_time` for a predeclared validation or holdout split.
The evaluator requires caller-declared complete dates before treating an
absent product-day as zero, freezes its product cohort from fit dates, and
returns ordinal-only product summaries. This path does not fetch real source
bytes and does not convert `InvoiceDate` into publication availability.

Current supported routes: `GET /health`, `GET /v1/capabilities`,
`POST /v1/scenarios/validate`, and the experimental
`POST /v1/decision-workflows/retail/synthetic`. The latter runs only a bounded
fictional fixture through the local service; the scaffold has no
authentication, explicit request body-size limit, rate limit or concurrency
control and is not safe for public exposure. Externally declared capabilities
must match the reviewed [capability ledger](CAPABILITY_LEDGER.json) and
[promotion gates](CAPABILITY_GATES.md). See [CONTRACTS](../CONTRACTS.md) and
[STRUCTURE](../STRUCTURE.md).

## Change-location guide
| User request | Inspect first | Evidence |
| --- | --- | --- |
| Evaluate aggregate Census vintages | [census_evaluation.py](../../src/mirrormind/domains/retail/census_evaluation.py), [evaluation guide](CENSUS_VINTAGE_EVALUATION.md), [model card](model_cards/SYNTHETIC_CENSUS_VINTAGE_EVALUATION.md) | [unit regressions](../../tests/unit/test_census_vintage_evaluation.py) and [CLI integration](../../tests/integration/test_census_vintage_evaluation_cli.py) prove fixed horizons, period-close and revision chronology, context-independent exact arithmetic, unanchored-revision abstention, bounded finite metric conversion and synthetic split replay; no source rights, empirical skill or production use |
| Change versioned scenario data | `core/contracts.py`, `api/routes/scenarios.py` | `tests/unit/test_contracts.py`, `tests/integration/test_api.py` |
| Define a reviewable decision result | [`core/decision_trace.py`](../../src/mirrormind/core/decision_trace.py), [result walkthrough](DECISION_TRACE_RESULT.md) | [synthetic contract tests](../../tests/unit/test_decision_trace.py) cover v1 input/reference bounds and review chronology; M1F-02 v2 binds selected-engine/parity evidence and rejects production instants after trace creation; timestamps remain caller-declared logical metadata, with no authenticated producer, trusted engine attestation, public engine API or action execution |
| Retrieve and evaluate locally scoped fictional evidence | [`modules/retrieval/index.py`](../../src/mirrormind/modules/retrieval/index.py) and [`modules/retrieval/evaluation.py`](../../src/mirrormind/modules/retrieval/evaluation.py), [M2 walkthrough](M2_EVIDENCE_RETRIEVAL.md) | [M2-01 scope/citation regressions](../../tests/unit/test_evidence_retrieval.py), [M2-02 metric/lineage/scope regressions](../../tests/unit/test_evidence_retrieval_evaluation.py) and [query/evaluation CLI replays](../../tests/integration/test_m2_evidence_retrieval_cli.py) plus [evaluation CLI regression](../../tests/integration/test_m2_evidence_retrieval_evaluation_cli.py); synthetic metrics only, caller scope is not authenticated authorization, no public route |
| Evaluate UCI-shaped product-day observations | [`uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py), [event-time research guide](M1_UCI_EVENT_TIME_RESEARCH.md) | [`test_uci_event_time.py`](../../tests/unit/test_uci_event_time.py) and [`test_uci_event_time_cli.py`](../../tests/integration/test_uci_event_time_cli.py) exercise synthetic coverage, cohort, holdout, metrics and redaction; no real source rights, snapshot completeness or point-in-time availability |
| Select an aggregate Census vintage before a target release | [`census_vintages.py`](../../src/mirrormind/domains/retail/census_vintages.py), [adapter walkthrough](CENSUS_VINTAGE_ADAPTER.md), [research protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md) | [`test_census_vintages.py`](../../tests/unit/test_census_vintages.py) exercises the strict date cutoff, publication-after-reference-month lower bound, first-estimate/revision chronology, per-month latest release, ambiguity rejection, missing-period preservation and unverified receipt using generated records; no source parser, bytes, rights, completeness or forecast scoring |
| Produce an end-to-end synthetic retail comparison | [`synthetic_decision_workflow.py`](../../src/mirrormind/domains/retail/synthetic_decision_workflow.py), [M1F-02 walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) | [`test_synthetic_decision_workflow.py`](../../tests/unit/test_synthetic_decision_workflow.py), API/default CLI test double plus explicit CLI WorldKernel engine regression with linked selected output and parity records; no source authorization, empirical forecast, authenticated review, public transport controls or writes |
| Map a retail scenario to WorldKernel v1 | [`worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py), [mapping walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md) | [strict synthetic mapping tests](../../tests/unit/test_worldkernel_mapping.py) cover revalidation of mutable scenarios and the lower scenario/operator run ceiling; no engine import or execution |
| Execute the M1 policy comparison in WorldKernel | [`worldkernel_policy_world.py`](../../src/mirrormind/domains/retail/worldkernel_policy_world.py), [`worldkernel_policy_gateway.py`](../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py), [M1E-04 guide](WORLDKERNEL_POLICY_WORLD.md) | Synthetic mapper/state/parity regressions plus exact-pin engine and CLI integration tests; no real data, forecast validity, hostile-code isolation or HTTP execution |
| Change health/capabilities | `api/routes/system.py`, `api/app.py` | `tests/integration/test_api.py` |
| Respond to a challenged remote head request (G-01) | [`modules/evidence/remote_fence_head_service.py`](../../src/mirrormind/modules/evidence/remote_fence_head_service.py), [service walkthrough](REMOTE_FENCE_HEAD_SERVICE.md) | [generated-key round-trip, typed clock/store failure and programming-error propagation tests](../../tests/unit/test_atomic_governed_publisher.py); in-process only, no HTTP route, persistent store or independent authority |
| Add simulation execution | `modules/simulation/gateway.py`, `core/contracts.py` | New adapter/contract tests; separate WorldKernel integration review |
| Stage and inspect local CSV structure | [`modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py), [staging guide](M1_LOCAL_CSV_STAGING.md) | [unit](../../tests/unit/test_evidence_snapshots.py) and [fixture integration](../../tests/integration/test_local_snapshot_flow.py) tests; no authorization |
| Prepare a source review packet (not approval) | [`modules/evidence/intake_review.py`](../../src/mirrormind/modules/evidence/intake_review.py), [guide](SOURCE_INTAKE_REVIEW.md) | [synthetic unit tests](../../tests/unit/test_source_intake_review.py); binds staged byte digest and opaque review references; never grants ingestion |
| Compose local retail evidence preflight | [`domains/retail/evidence_flow.py`](../../src/mirrormind/domains/retail/evidence_flow.py), [M1 guide](M1_SYNTHETIC_EVIDENCE_FLOW.md), [scoped change request](changes/M1B_02_SYNTHETIC_EVIDENCE_FLOW.md) | [integration tests](../../tests/integration/test_retail_evidence_flow.py); CSV as-of rows use caller-declared dates, UCI checks require explicit calendar/release tuples, and receipts are aggregate-only; no source authorization |
| Evaluate a prepared retail evidence flow | [`domains/retail/evaluation_flow.py`](../../src/mirrormind/domains/retail/evaluation_flow.py), [M1 evaluation guide](M1_RETAIL_SYNTHETIC_EVALUATION.md), [fixed synthetic CLI](../../examples/m1_retail_synthetic_evaluation.py) | [integration tests](../../tests/integration/test_retail_synthetic_evaluation.py) prove fixed split, matched-origin statuses, mutation resistance and sanitized receipts on a generated fixture; no authenticated source, empirical performance or HTTP evaluation endpoint |
| Audit fictional retail residual uncertainty | [`domains/retail/residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py), [uncertainty guide](RETAIL_RESIDUAL_ENVELOPE.md), [M1D-01 change request](changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md) | [unit regressions](../../tests/unit/test_retail_residual_envelope.py) verify fixed disjoint target windows, as-of release eligibility, abstention, numerator/denominator and an independent test oracle; results remain uncalibrated and source-unverified |
| Compare retail replenishment policies on paired fictional demand | [`domains/retail/policy_simulation.py`](../../src/mirrormind/domains/retail/policy_simulation.py), [M1 policy simulation guide](M1_RETAIL_POLICY_SIMULATION.md), [synthetic CLI](../../examples/m1_retail_policy_test_double.py) | [unit tests](../../tests/unit/test_retail_policy_simulation.py) and [CLI integration test](../../tests/integration/test_retail_policy_simulation_cli.py) prove local determinism, paired streams and bounded sensitivity only; no trained forecast, actual engine, recommendation or authorization |
| Atomically apply current operator policy to local checkpoint publication (not external authority) | [`modules/evidence/atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py), [guide](ATOMIC_GOVERNED_PUBLISHER.md) | [signed revocation/race tests](../../tests/unit/test_atomic_governed_publisher.py); opt-in single new SQLite file, real identity/currentness missing |
| Record dual-admin operator key policy (not publisher enforcement) | [`modules/evidence/operator_governance.py`](../../src/mirrormind/modules/evidence/operator_governance.py), [policy guide](OPERATOR_GOVERNANCE.md) | [synthetic dual-admin and rollback tests](../../tests/unit/test_operator_governance.py); separate SQLite, no atomic policy+publication integration |
| Retain signer-gated local witness publication metadata (not a live authority) | [`modules/evidence/local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py), [guide](LOCAL_CHECKPOINT_PUBLISHER.md) | [synthetic operator and CAS tests](../../tests/unit/test_local_checkpoint_publisher.py); distinct key roles and local SQLite, no authenticated current head |
| Verify supplied witness receipt succession (no live authority) | [`modules/evidence/authority_transcript.py`](../../src/mirrormind/modules/evidence/authority_transcript.py), [guide](AUTHORITY_TRANSCRIPT.md) | [synthetic handoff and outage tests](../../tests/unit/test_authority_transcript.py); external start/end fences, witness keys and current head not implemented |
| Compare separately signed review-head checkpoint (no live authority) | [`modules/evidence/head_checkpoints.py`](../../src/mirrormind/modules/evidence/head_checkpoints.py), [guide](SIGNED_HEAD_CHECKPOINTS.md) | [fictional replay and rollback tests](../../tests/unit/test_head_checkpoints.py); signer keys and high-water are caller supplied, never authorize source use |
| Persist local signed review history across restarts (not an authority) | [`modules/evidence/sqlite_review_registry.py`](../../src/mirrormind/modules/evidence/sqlite_review_registry.py), [guide](SQLITE_REVIEW_REGISTRY.md) | [synthetic recovery/concurrency tests](../../tests/unit/test_sqlite_review_registry.py); local SQLite transactions only, no trusted external head or authorization |
| Coordinate signed reviews within one process (not an authority) | [`modules/evidence/local_review_registry.py`](../../src/mirrormind/modules/evidence/local_review_registry.py), [local registry guide](LOCAL_REVIEW_REGISTRY.md) | [adversarial tests](../../tests/unit/test_local_review_registry.py); lost on restart, never authorizes source usage |
| Verify signed source-review metadata (not authorization) | [`modules/evidence/review_decisions.py`](../../src/mirrormind/modules/evidence/review_decisions.py), [signatures/expiry guide](SIGNED_SOURCE_REVIEW.md) | [synthetic tests](../../tests/unit/test_signed_source_review.py); reviewer public keys and current head are externally supplied, not managed in MirrorMind |
| Project offline UCI-shaped retail rows | [`domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py), [source guide](UCI_RETAIL_PROJECTION.md) | [unit](../../tests/unit/test_uci_retail_projection.py) and [integration](../../tests/integration/test_uci_retail_projection_flow.py) tests on invented rows only; **no as-of availability assertion** |
| Read and validate a bounded UCI-shaped XLSX file offline | [`uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), [`uci_xlsx_xml.py`](../../src/mirrormind/domains/retail/uci_xlsx_xml.py), [source guide](UCI_WORKBOOK_READER.md) | [unit](../../tests/unit/test_uci_workbook.py) and [integration](../../tests/integration/test_uci_workbook_flow.py) fixtures prove duplicate-coordinate/scalar rejection, selected-cell type/number validation, mixed-payload rejection in both scans, rich-text compatibility and excluded `Description` privacy; the one approved source attempt stopped above 250,000 product-day groups with no projection or metric |
| Introduce real evidence connectors/RAG | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md), [data card](DATASET_CARD_TEMPLATE.md) | Separate source-specific permission/provenance tests required |
| Evaluate local staged rolling baselines | [`modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py), [method guide](M1_STAGED_ROLLING_BASELINES.md) | [unit](../../tests/unit/test_staged_rolling_baselines.py) and [integration](../../tests/integration/test_staged_rolling_flow.py) tests on invented data only |
| Introduce real forecasting service | [RETAIL_MVP](../RETAIL_MVP.md), [ROADMAP](../ROADMAP.md) | Approved snapshot, locked independent holdout, calibrated risk and serving/permission tests |
| Run bounded local tool orchestration | [`modules/agents/orchestrator.py`](../../src/mirrormind/modules/agents/orchestrator.py), [`modules/agents/registry.py`](../../src/mirrormind/modules/agents/registry.py), [M2-03 walkthrough](M2_TOOL_ORCHESTRATION.md) | [unit regressions](../../tests/unit/test_bounded_tool_orchestration.py) and [CLI integration](../../tests/integration/test_m2_tool_orchestration_cli.py) cover static tools, plain-data revalidation against Pydantic `model_copy(update=...)` bypasses, call/turn/byte limits, immutable registry, sanitized refusals, injection resistance and citation membership; scripted provider only, no route, live provider, semantic entailment or action authority |

## Non-negotiable boundaries
- General-purpose decision platform; retail is the first reference domain, not a hard-coded limitation.
- Keep **observed evidence**, **forecast estimates** and **simulated counterfactuals** conceptually separate.
- No core dependency on WorldKernel. Integrate through an optional, versioned simulation gateway.
- Keep the local synthetic retail test double separate from the actual WorldKernel adapter and from forecast quality claims.
- Preserve permission provenance and human review; don't claim live agents, RAG, forecasting, connectors or simulations until implemented and tested.
- An interface alone does not establish functioning integration.

See [ARCHITECTURE](../ARCHITECTURE.md), [DECISIONS](../DECISIONS.md), [ROADMAP](../ROADMAP.md), [STRUCTURE](../STRUCTURE.md).
## Current local evidence staging path

Trusted local caller -> `stage_csv_snapshot(bytes, expected_sha256)`
-> strict UTF-8 CSV/date/duplicate validation ->
`StagedSnapshot` (in memory, explicitly **not authorized**) ->
`available_as_of(..., origin_on)` filters by both
event and declared publication time. The result
contains original observations and **must not**
be returned through an unauthenticated public endpoint.

This code neither obtains source permission nor calls
WorldKernel, an LLM, a data connector or persistent storage.

## Current offline one-step baseline path

Trusted caller -> local `stage_csv_snapshot`
-> `StagedSnapshot` (explicitly *not authorized*)
-> `backtest_staged_snapshot` for one series and
retrospective cutoff -> per-origin `available_as_of`
-> two fixed one-step estimates -> only matched scored
origins and explicit abstentions. This is **not**
a general forecasting endpoint, configured data
connector or real-world decision engine.

## Experimental retail transaction projection (not an HTTP route)

Trusted caller's **already supplied** UCI-shaped
row mappings -> `domains/retail/uci_transactions.py`
-> strict InvoiceNo/StockCode/Quantity/InvoiceDate
validation -> nonpositive and cancellation accounting
-> immutable daily positive-line units **without**
CustomerID, InvoiceNo, Description, price or
publication time. The input's extra fields must
not become output fields. Missing day is **not**
zero demand.

The output cannot go directly into the
generic as-of staging/forecasting pipeline:
UCI `InvoiceDate` is **event time**, not
verified first availability. A separate licensed,
reviewed source-adapter and publication policy
are required. See [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md).

## Optional UCI-shaped workbook edge (not an API endpoint)

Trusted caller already opens a selected local XLSX
-> `read_uci_workbook` reads bounded compressed
bytes, checks digest/ZIP metadata/sheet/schema ->
passes only `InvoiceNo`, `StockCode`,
`Quantity`, `InvoiceDate` through the
existing bounded retail projection ->
returns a non-authorized digest-coupled
positive-line product/day receipt.

The original UCI source is **not** downloaded
or automatically trusted. Customer and invoice
fields may be parsed inside the workbook library
but are not forwarded to the retail projection.
Event date is still not proven publication
date, so no direct historical forecast
or WorldKernel scenario input is authorized.

## Aggregate monthly vintage selection (synthetic preparation only)

Caller-supplied normalized records ->
`select_census_vintage_as_of(records, series_id, target_release_on)` ->
strict metadata and period-close validation -> reject releases dated inside
or before their `reference_month` -> exclude records where
`published_on >= target_release_on` -> choose the latest remaining record
per `reference_month` -> `CensusVintageView` with release IDs and digest
strings. Empty months remain absent. A date-only same-day publication is
ambiguous and rejected; the selector never uses row order to resolve it.

The selector is a pure in-memory adapter against fictional records. It checks
digest syntax but cannot read source bytes, verify a Census/ALFRED manifest,
authenticate the actual release schedule or authorize ingestion. The
downstream synthetic evaluator is also local-only;
real source parsing, vintage archive verification, rights and empirical
evaluation remain blocked by B-01/B-02. See the
[adapter walkthrough](CENSUS_VINTAGE_ADAPTER.md),
[synthetic fixture card](datasets/SYNTHETIC_CENSUS_VINTAGES.md) and
[protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md).

## Aggregate monthly vintage baseline evaluation (synthetic preparation only)

The [Census vintage evaluator](../../src/mirrormind/domains/retail/census_evaluation.py)
uses each predeclared date-only origin to select the latest visible monthly
vintage, then scores the target first estimate one, three and six reference
months ahead. It compares fixed lag-12 seasonal naive and trailing-12-month
mean baselines on identical eligible targets. Incomplete history, missing
labels and already-published targets abstain; no months are zero-filled.

The validation/holdout example builds a fictional series in memory and emits
metrics plus per-origin vintage fingerprints, publication dates, release IDs
and source digest strings. It omits values and predictions, keeps
authorization/forecast flags false, and cannot verify the caller-provided
snapshot strings. See the [evaluation guide](CENSUS_VINTAGE_EVALUATION.md),
[model card](model_cards/SYNTHETIC_CENSUS_VINTAGE_EVALUATION.md),
[synthetic example](../../examples/m1_census_vintage_evaluation.py) and
[regressions](../../tests/unit/test_census_vintage_evaluation.py).

## Offline combined-head fence — experimental, no authority service

The [integrated head-fence verifier](INTEGRATED_HEAD_FENCE.md) reads
the existing [atomic governed publisher](ATOMIC_GOVERNED_PUBLISHER.md)
through its transactional `snapshot` API. A caller supplies an
Ed25519-signed record covering the source packet, policy revision/head,
publication sequence/head and expiry, plus **separately** pinned
expected current sequence/digest and trusted signer public key.
Nothing is fetched, appended or used for publication admission:
the combined SQLite state remains a local evidence object, not a
globally trusted current state or legal ingestion entitlement.

## Optional dual-witness chain of combined heads (MM-M1b)

The [experimental transcript verifier](INTEGRATED_FENCE_TRANSCRIPT.md)
takes caller-pinned anchors and latest hashes, validates a bounded
sequence of authority-signed integrated-state fences with two separately
configured Ed25519 witness signatures per transition, and calls the
existing combined-state SQLite verifier only for the final head.
The [fork classifier](INTEGRATED_FENCE_TRANSCRIPT.md) can report two
supplied valid competing successors. No external witness node or
current-head discovery service is deployed; neither verifier is a
publisher, forecast engine or permission authority.

## Bounded separate local checkpoint registry

The [local signed integrated-fence registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md)
is an opt-in **second local SQLite file** next to, not within, the
existing [atomic publisher](ATOMIC_GOVERNED_PUBLISHER.md).
It persists fully signed [dual-witness transition JSON](INTEGRATED_FENCE_TRANSCRIPT.md)
and stores a packet/roster/schema marker; every read replays signatures
and each append takes a registry-only `BEGIN IMMEDIATE` lock and
verifies terminal publisher state. A publisher-only coherent backup
restore becomes detectable if the registry is intact. No independent
server, backup custodian, distributed transaction, signer identity
or legally authorized source processing was created.

## MM-M1b experimental challenged remote current-head reader

The [remote head client](REMOTE_FENCE_HEAD_CLIENT.md) is a narrow
optional **outbound HTTPS read** adapter with a random per-request
nonce, fixed DNS endpoint, standard TLS validation and a
domain-separated Ed25519 service signature. It binds exact
source-review declaration/snapshot and compares the returned
sequence/digest with [the separate local signed-fence registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md),
which verifies the [governed publisher](ATOMIC_GOVERNED_PUBLISHER.md).
The code neither deploys an external service nor certifies its
administrative independence, durable latest-state operation, key
custody or honesty. This network read does not grant any access
rights or alter publisher transactions.

The [G-01 responder](REMOTE_FENCE_HEAD_SERVICE.md) provides an in-process
implementation of the existing response contract through a read-only store
`Protocol`. It shares canonicalization with the client, but no transport,
persistence, authentication or independent administration is implemented.
The client does not call this responder; the generated-key round trip is
exercised in a local test. This remains an experimental in-process component, not an
operational service.

## Standalone M1 examples — adjacent-date invariant

The [as-of rolling example](../../examples/m1_asof_rolling_backtest.py)
parses and sorts event dates before evaluating rolling origins. Its private
`_require_contiguous_days` helper checks ordered neighbors with
`itertools.pairwise`; a calendar gap raises the existing fail-closed error
before any forecasts are scored. The helper does not synthesize a date or
count. Python 3.11 is the declared minimum, and `pairwise` preserves the
previous `zip(days, days[1:])` boundaries for empty, singleton and longer
lists. The standalone observation preflight and earlier rolling baseline
remain unchanged apart from import cleanup. Unit and CLI references are
listed in the [repository atlas](REPOSITORY_ATLAS.md); see the [as-of method
guide](M1_ASOF_ROLLING_EVALUATION.md) for evaluation semantics.

This is a local synthetic example, not an API path or source adapter. A
contiguous sequence of declared dates proves neither original publication
availability nor source permission.

## Experimental offline portfolio report

The [report generator](PORTFOLIO_DEMO.md) calls the existing synthetic decision workflow once and embeds its exact result in a new local HTML file. Browser interactions only select existing cases; no extra server route, live simulation, external dependency or production claim.

The synthetic retail workflow reuses its generated XLSX bytes within one
request only. The two release audits and reader invocations remain separate;
see [the M1F-02 walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md).

The experimental local BM25 index performs binary lookups on immutable sorted
frequency tables for query terms only. It retains the original corpus-wide
statistics and scope-first build; see [M2 retrieval](M2_EVIDENCE_RETRIEVAL.md).

The compact local retrieval index retains total token counts and sorted
term frequency/first code-point offset triples, not every token occurrence.
The original excerpt selection is equivalent to the minimum first offset
among matching terms. See [M2 retrieval](M2_EVIDENCE_RETRIEVAL.md).

### Census descriptive companion (M1C-04 experimental)

`evaluate_census_vintage_descriptive` shares the existing scoring pass
and adds matched absolute loss rows plus a complete report fingerprint.
The original v2 entrypoint does not expose those rows. No API, persistence,
inference or authority changes. See [evaluation](CENSUS_VINTAGE_EVALUATION.md).

### Experimental predeclared Census split
The local [schedule wrapper](../../src/mirrormind/domains/retail/census_split.py)
checks a caller-retained fingerprint and target/publication embargo before
calling the descriptive evaluator. No trusted registration or holdout lock
is asserted. See [evaluation guide](CENSUS_VINTAGE_EVALUATION.md).

### Experimental Census experiment commitment
The [pure contract](../../src/mirrormind/domains/retail/census_experiment.py)
binds normalized manifest, schedule, protocol and declared code revision,
executes the split wrapper and compares complete canonical receipt bytes
on explicit replay. It neither persists nor attests execution.

### Experimental Census experiment journal
The [SQLite adapter](../../src/mirrormind/domains/retail/census_experiment_journal.py)
calls the pure commitment and replay contract, writes only identity metadata
and result digests, and rechecks the registered spec in a transaction after
replay. No API or independent trust authority. See
[Census evaluation guide](CENSUS_VINTAGE_EVALUATION.md).

### Fictional Census research runner
The [local CLI](../../examples/m1_census_research_runner.py) connects
a generated fixture, commitment, split evaluation and journal replay.
It emits deterministic summary JSON, not an external service or authority.
See [evaluation guide](CENSUS_VINTAGE_EVALUATION.md).

### Fictional research observatory
The [static HTML generator](../../examples/m1_census_research_observatory.py)
renders the runner's freshly replayed synthetic summary. No external
report input, service, new storage or authority.

### Closed fictional scenario catalog
The [runner](../../examples/m1_census_research_runner.py) generates four
fixed value sequences with the same temporal schedule. Each normalized
manifest binds its scenario to a distinct experiment commitment. The
[observatory](../../examples/m1_census_research_observatory.py) displays
the selected scenario. No new core models or authority.

### Comparative fictional observatory
The [observatory](../../examples/m1_census_research_observatory.py) also
supports an explicit all-catalog mode with independent scenario receipts,
per-split comparison tables and separate provenance. Temporary journal,
no persistent history or new core contracts.

### Fictional experiment history
The [history example](../../examples/m1_census_research_history.py)
renders a bounded read-only snapshot from
[census_experiment_journal.py](../../src/mirrormind/domains/retail/census_experiment_journal.py).
An explicit selected receipt may be reproduced by the current evaluator;
no default scoring, admission, historical runtime attestation or new schema.

### Fictional sensitivity grid
The [sensitivity example](../../examples/m1_census_research_sensitivity.py)
prepares a fixed one-factor grid, deduplicates the shared zero baseline,
executes and replays the existing experiment contract and emits separate
per-horizon summaries. Temporary journal; no model or API change.

### Experimental five-model comparison
The [pure model library](../../src/mirrormind/domains/retail/census_models.py)
adds persistence, seasonal drift and linear trend to the original methods
in a separate validation-only comparison and canonical replay contract.
The [example catalog](../../examples/m1_census_model_comparison.py)
includes a fixed validation break. No changes to legacy receipts or journal.

### Experimental discrete probability core
The [pure probability module](../../src/mirrormind/domains/retail/census_probability.py)
provides bounded canonical mass functions, integer convolution and
Markov propagation, exact quantiles and scores. No connection to
provider dispatch, source ingestion, legacy evaluation or persistence.

### Fixed fictional probabilistic study
The [study example](../../examples/m1_census_probability_study.py)
uses the discrete probability core with a committed fixed design,
exact aggregate scores and streaming event transcript digests.
Explicit complete receipt replay; no journal, API or new authority.

### Fictional probabilistic observatory
The [offline report](../../examples/m1_census_probability_observatory.py)
renders freshly replayed fixed probability study summaries and fixed
example distributions. No new core contracts, API, storage or authority.

### Experimental bivariate probability core
The [pure joint module](../../src/mirrormind/domains/retail/census_bivariate.py)
adds bounded exact two-axis PMFs, convolution, marginal projections and
joint scoring without modifying the univariate protocol. No connection
to data ingestion, provider dispatch, learned models or persistence.

### Fictional bivariate study
The [bivariate study](../../examples/m1_census_bivariate_study.py)
uses the exact joint core, fixed counter-hash scenarios, matched
marginals, exact joint scores and full local receipt replay. No new
API, persistence, source or authority.

### Multivariate research observatory
The [offline bivariate report](../../examples/m1_census_bivariate_observatory.py)
renders fixed-study metrics after full replay and regenerates fixed
joint and marginal examples. No new API, storage or authority.

### Experimental paired-state Markov engine
The [joint Markov module](../../src/mirrormind/domains/retail/census_joint_markov.py)
computes bounded conditional cumulative joint distributions from caller
supplied transition schedules. It reuses the bivariate PMF contract,
without changing existing independent-in-time convolution, API,
persistence or authority.
