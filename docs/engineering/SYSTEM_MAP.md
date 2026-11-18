# MirrorMind — system map

Updated from the initial scaffold on 2026-11-18. The API/contracts and simulation gateway interface exist; a standalone **local CSV staging primitive** is also implemented in the evidence module. No authorized ingestion, agents or forecasts are deployed.

## Current request path

HTTP request → `src/mirrormind/api/app.py` → thin routes `api/routes/system.py` or `api/routes/scenarios.py` → validation with `core/contracts.py` → response. The `modules/simulation/gateway.py` interface defines an engine-neutral boundary; it does **not** execute WorldKernel simulations yet.

Current supported routes: `GET /health`, `GET /v1/capabilities`, and `POST /v1/scenarios/validate`. The externally declared capabilities must match the reviewed [capability ledger](CAPABILITY_LEDGER.json) and [promotion gates](CAPABILITY_GATES.md). See [CONTRACTS](../CONTRACTS.md) and [STRUCTURE](../STRUCTURE.md).

## Change-location guide
| User request | Inspect first | Evidence |
| --- | --- | --- |
| Change versioned scenario data | `core/contracts.py`, `api/routes/scenarios.py` | `tests/unit/test_contracts.py`, `tests/integration/test_api.py` |
| Change health/capabilities | `api/routes/system.py`, `api/app.py` | `tests/integration/test_api.py` |
| Add simulation execution | `modules/simulation/gateway.py`, `core/contracts.py` | New adapter/contract tests; separate WorldKernel integration review |
| Stage and inspect local CSV structure | [`modules/evidence/snapshots.py`](../../src/mirrormind/modules/evidence/snapshots.py), [staging guide](M1_LOCAL_CSV_STAGING.md) | [unit](../../tests/unit/test_evidence_snapshots.py) and [fixture integration](../../tests/integration/test_local_snapshot_flow.py) tests; no authorization |
| Project offline UCI-shaped retail rows | [`domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py), [source guide](UCI_RETAIL_PROJECTION.md) | [unit](../../tests/unit/test_uci_retail_projection.py) and [integration](../../tests/integration/test_uci_retail_projection_flow.py) tests on invented rows only; **no as-of availability assertion** |
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
