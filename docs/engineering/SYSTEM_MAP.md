# MirrorMind — system map

Updated on 2026-11-24 against merged main PR #51 (`e4f05a1`) and the current G-01 branch. Main contains the API/contracts, simulation gateway interface and local CSV staging. Draft PRs #52–#59 add experimental synthetic evidence/evaluation/decision slices but are not merged. G-01 adds an in-process challenged-head responder but no deployed service. No authorized ingestion, agents or production forecasts are deployed.

## Current request path

HTTP request → `src/mirrormind/api/app.py` → thin routes `api/routes/system.py` or `api/routes/scenarios.py` → validation with `core/contracts.py` → response. The `modules/simulation/gateway.py` interface defines an engine-neutral boundary; it does **not** execute WorldKernel simulations yet.

Current supported routes: `GET /health`, `GET /v1/capabilities`, and `POST /v1/scenarios/validate`. The externally declared capabilities must match the reviewed [capability ledger](CAPABILITY_LEDGER.json) and [promotion gates](CAPABILITY_GATES.md). See [CONTRACTS](../CONTRACTS.md) and [STRUCTURE](../STRUCTURE.md).

## Change-location guide
| User request | Inspect first | Evidence |
| --- | --- | --- |
| Change versioned scenario data | `core/contracts.py`, `api/routes/scenarios.py` | `tests/unit/test_contracts.py`, `tests/integration/test_api.py` |
| Change health/capabilities | `api/routes/system.py`, `api/app.py` | `tests/integration/test_api.py` |
| Respond to a challenged remote head request (G-01) | [`modules/evidence/remote_fence_head_service.py`](../../src/mirrormind/modules/evidence/remote_fence_head_service.py), [service walkthrough](REMOTE_FENCE_HEAD_SERVICE.md) | [generated-key round-trip and adverse tests](../../tests/unit/test_atomic_governed_publisher.py); in-process only, no HTTP route, persistent store or independent authority |
| Add simulation execution | `modules/simulation/gateway.py`, `core/contracts.py` | New adapter/contract tests; separate WorldKernel integration review |
| Stage and inspect local CSV structure | [`modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py), [staging guide](M1_LOCAL_CSV_STAGING.md) | [unit](../../tests/unit/test_evidence_snapshots.py) and [fixture integration](../../tests/integration/test_local_snapshot_flow.py) tests; no authorization |
| Prepare a source review packet (not approval) | [`modules/evidence/intake_review.py`](../../src/mirrormind/modules/evidence/intake_review.py), [guide](SOURCE_INTAKE_REVIEW.md) | [synthetic unit tests](../../tests/unit/test_source_intake_review.py); binds staged byte digest and opaque review references; never grants ingestion |
| Atomically apply current operator policy to local checkpoint publication (not external authority) | [`modules/evidence/atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py), [guide](ATOMIC_GOVERNED_PUBLISHER.md) | [signed revocation/race tests](../../tests/unit/test_atomic_governed_publisher.py); opt-in single new SQLite file, real identity/currentness missing |
| Record dual-admin operator key policy (not publisher enforcement) | [`modules/evidence/operator_governance.py`](../../src/mirrormind/modules/evidence/operator_governance.py), [policy guide](OPERATOR_GOVERNANCE.md) | [synthetic dual-admin and rollback tests](../../tests/unit/test_operator_governance.py); separate SQLite, no atomic policy+publication integration |
| Retain signer-gated local witness publication metadata (not a live authority) | [`modules/evidence/local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py), [guide](LOCAL_CHECKPOINT_PUBLISHER.md) | [synthetic operator and CAS tests](../../tests/unit/test_local_checkpoint_publisher.py); distinct key roles and local SQLite, no authenticated current head |
| Verify supplied witness receipt succession (no live authority) | [`modules/evidence/authority_transcript.py`](../../src/mirrormind/modules/evidence/authority_transcript.py), [guide](AUTHORITY_TRANSCRIPT.md) | [synthetic handoff and outage tests](../../tests/unit/test_authority_transcript.py); external start/end fences, witness keys and current head not implemented |
| Compare separately signed review-head checkpoint (no live authority) | [`modules/evidence/head_checkpoints.py`](../../src/mirrormind/modules/evidence/head_checkpoints.py), [guide](SIGNED_HEAD_CHECKPOINTS.md) | [fictional replay and rollback tests](../../tests/unit/test_head_checkpoints.py); signer keys and high-water are caller supplied, never authorize source use |
| Persist local signed review history across restarts (not an authority) | [`modules/evidence/sqlite_review_registry.py`](../../src/mirrormind/modules/evidence/sqlite_review_registry.py), [guide](SQLITE_REVIEW_REGISTRY.md) | [synthetic recovery/concurrency tests](../../tests/unit/test_sqlite_review_registry.py); local SQLite transactions only, no trusted external head or authorization |
| Coordinate signed reviews within one process (not an authority) | [`modules/evidence/local_review_registry.py`](../../src/mirrormind/modules/evidence/local_review_registry.py), [local registry guide](LOCAL_REVIEW_REGISTRY.md) | [adversarial tests](../../tests/unit/test_local_review_registry.py); lost on restart, never authorizes source usage |
| Verify signed source-review metadata (not authorization) | [`modules/evidence/review_decisions.py`](../../src/mirrormind/modules/evidence/review_decisions.py), [signatures/expiry guide](SIGNED_SOURCE_REVIEW.md) | [synthetic tests](../../tests/unit/test_signed_source_review.py); reviewer public keys and current head are externally supplied, not managed in MirrorMind |
| Project offline UCI-shaped retail rows | [`domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py), [source guide](UCI_RETAIL_PROJECTION.md) | [unit](../../tests/unit/test_uci_retail_projection.py) and [integration](../../tests/integration/test_uci_retail_projection_flow.py) tests on invented rows only; **no as-of availability assertion** |
| Read a small trusted UCI-shaped XLSX file offline | [`domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), [source guide](UCI_WORKBOOK_READER.md) | [unit](../../tests/unit/test_uci_workbook.py) and [integration](../../tests/integration/test_uci_workbook_flow.py) tests; no real-file access approval or full official dataset support |
| Introduce real evidence connectors/RAG | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md), [data card](DATASET_CARD_TEMPLATE.md) | Separate source-specific permission/provenance tests required |
| Evaluate local staged rolling baselines | [`modules/forecasting/baselines.py`](../../src/mirrormind/modules/forecasting/baselines.py), [method guide](M1_STAGED_ROLLING_BASELINES.md) | [unit](../../tests/unit/test_staged_rolling_baselines.py) and [integration](../../tests/integration/test_staged_rolling_flow.py) tests on invented data only |
| Introduce real forecasting service | [RETAIL_MVP](../RETAIL_MVP.md), [ROADMAP](../ROADMAP.md) | Approved snapshot, locked independent holdout, calibrated risk and serving/permission tests |
| Add agents/orchestration | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md) | Tool permissions, cost budgets and audit tests when created |

## Non-negotiable boundaries
- General-purpose decision platform; retail is the first reference domain, not a hard-coded limitation.
- Keep **observed evidence**, **forecast estimates** and **simulated counterfactuals** conceptually separate.
- No core dependency on WorldKernel. Integrate through an optional, versioned simulation gateway.
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

The [G-01 responder](REMOTE_FENCE_HEAD_SERVICE.md) provides an in-process
implementation of the existing response contract through a read-only store
`Protocol`. It shares canonicalization with the client, but no transport,
persistence, authentication or independent administration is implemented.
The client does not call this responder; the generated-key round trip is
exercised in a local test.
