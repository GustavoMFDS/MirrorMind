# MirrorMind — system map

Updated on 2026-11-27 against main commit `a456034c55ed7634ad4768b26788fec09dab1d08` plus the UCI pilot branch. Bounded CSV/XLSX staging, retrospective UCI evaluation, the paired policy test double, the synthetic decision workflow and exact-pin local engine adapters remain experimental. The approved UCI #352 snapshot passed metadata preflight; the corrected reader applied the approved invoice-prefix exclusion policy but exceeded the UCI-only 250,000 product-day group cap and returned no projection. No empirical scores exist. UCI results remain event-time retrospective with unverified publication availability and describe units per recognized `StockCode` category, not verified physical-SKU demand. The decision trace result schema remains interface-only as a general capability; its M1F-02 v2 producer is synthetic and non-authorizing. On the explicit WorldKernel CLI path, each outcome links the selected engine result and a separate parity-oracle execution record. The upstream inventory demo and fixed MirrorMind policy handler execute only through the local worker; no HTTP engine execution, production ingestion, agents or production forecasts are deployed.

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

The separate UCI event-time CLI builds a deterministic workbook in memory,
passes it through the bounded XLSX reader and product-day projection, then
calls `evaluate_uci_event_time` for a predeclared validation or holdout split.
The evaluator requires caller-declared complete dates before treating an
absent product-day as zero, freezes its product cohort from fit dates, and
returns ordinal-only product summaries. This path does not fetch real source
bytes and does not convert `InvoiceDate` into publication availability.

The approved local UCI workbook profile is a separate caller-provided stream
path: `read_uci_workbook` verifies the expected digest and finite ZIP limits,
the selective OOXML scanner yields only reviewed projection fields, and
`_normalize_uci_workbook_invoice` classifies the invoice form before the
bounded `project_uci_retail_rows` aggregation. Under MM-022, only exact
uppercase `C` plus six digits marks cancellation; lowercase `c` and other
single ASCII-letter prefixes map to one unverified class whose aggregate count
survives. Other forms fail closed, identifiers do not reach the output, and
generic projection defaults remain unchanged. The real-source attempt used
MM-021 and stopped above the approved group cap. MM-022's full 52-letter
classification and one-counter boundary are covered by the synthetic
`test_all_single_ascii_letter_prefixes_have_one_aggregate_exclusion_class`;
the policy relabeling does not change the source attempt's accepted rows or
group count, and no source reread or empirical metric exists.

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
| Change versioned scenario data | `core/contracts.py`, `api/routes/scenarios.py` | `tests/unit/test_contracts.py`, `tests/integration/test_api.py` |
| Define a reviewable decision result | [`core/decision_trace.py`](../../src/mirrormind/core/decision_trace.py), [result walkthrough](DECISION_TRACE_RESULT.md) | [synthetic contract tests](../../tests/unit/test_decision_trace.py) cover v1 input/reference bounds and review chronology; M1F-02 v2 binds selected-engine/parity evidence and rejects production instants after trace creation; timestamps remain caller-declared logical metadata, with no authenticated producer, trusted engine attestation, public engine API or action execution |
| Evaluate UCI `StockCode`-category/day observations | [`uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py), [event-time research guide](M1_UCI_EVENT_TIME_RESEARCH.md) | [`test_uci_event_time.py`](../../tests/unit/test_uci_event_time.py) and [`test_uci_event_time_cli.py`](../../tests/integration/test_uci_event_time_cli.py) exercise synthetic coverage, cohort, holdout, metrics and redaction; the approved snapshot preflight did not pass the group ceiling, and no empirical score or point-in-time availability is verified |
| Produce an end-to-end synthetic retail comparison | [`synthetic_decision_workflow.py`](../../src/mirrormind/domains/retail/synthetic_decision_workflow.py), [M1F-02 walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) | [`test_synthetic_decision_workflow.py`](../../tests/unit/test_synthetic_decision_workflow.py), API/default CLI test double plus explicit CLI WorldKernel engine regression with linked selected output and parity records; no source authorization, empirical forecast, authenticated review, public transport controls or writes |
| Map a retail scenario to WorldKernel v1 | [`worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py), [mapping walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md) | [strict synthetic mapping tests](../../tests/unit/test_worldkernel_mapping.py) cover revalidation of mutable scenarios and the lower scenario/operator run ceiling; no engine import or execution |
| Execute the M1 policy comparison in WorldKernel | [`worldkernel_policy_world.py`](../../src/mirrormind/domains/retail/worldkernel_policy_world.py), [`worldkernel_policy_gateway.py`](../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py), [M1E-04 guide](WORLDKERNEL_POLICY_WORLD.md) | Synthetic mapper/state/parity regressions plus exact-pin engine and CLI integration tests; no real data, forecast validity, hostile-code isolation or HTTP execution |
| Change health/capabilities | `api/routes/system.py`, `api/app.py` | `tests/integration/test_api.py` |
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
| Read a trusted UCI-shaped XLSX stream offline | [`domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), selective [OOXML reader](../../src/mirrormind/domains/retail/uci_xlsx_xml.py), [source guide](UCI_WORKBOOK_READER.md) | [unit](../../tests/unit/test_uci_workbook.py) and [integration](../../tests/integration/test_uci_workbook_flow.py) remain synthetic-only; XML callbacks are disabled for excluded body text and approved projection columns are decoded. The real #352 call exceeded 250,000 groups and produced no projection or empirical result |
| Introduce real evidence connectors/RAG | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md), [data card](DATASET_CARD_TEMPLATE.md) | Separate source-specific permission/provenance tests required |
| Evaluate local staged rolling baselines | [`modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py), [method guide](M1_STAGED_ROLLING_BASELINES.md) | [unit](../../tests/unit/test_staged_rolling_baselines.py) and [integration](../../tests/integration/test_staged_rolling_flow.py) tests on invented data only |
| Introduce real forecasting service | [RETAIL_MVP](../RETAIL_MVP.md), [ROADMAP](../ROADMAP.md) | Approved snapshot, locked independent holdout, calibrated risk and serving/permission tests |
| Add agents/orchestration | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md) | Tool permissions, cost budgets and audit tests when created |

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
