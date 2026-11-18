# Repository structure — MirrorMind

```text
MirrorMind/
├── .github/workflows/ci.yml
├── .env.example
├── Dockerfile
├── compose.yml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── DECISIONS.md
│   ├── RETAIL_MVP.md
│   ├── ROADMAP.md
│   ├── SECURITY.md
│   └── STRUCTURE.md
├── examples/retail-scenario.json
├── examples/synthetic-daily-sales.json      # Invented observations, not real data
├── examples/m1_observation_preflight.py     # Standalone bounded preflight (experiment)
├── src/mirrormind/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py        # Stable app export for uvicorn
│   │   ├── app.py             # App composition only
│   │   └── routes/
│   │       ├── system.py      # Health and capabilities
│   │       └── scenarios.py   # Scenario validation
│   ├── core/
│   │   └── contracts.py       # Versioned shared Pydantic contracts
│   ├── domains/
│   │   ├── __init__.py
│   │   └── retail/
│   │       ├── __init__.py
│   │       ├── uci_transactions.py  # Offline UCI-shaped invented row aggregation
│   │       └── uci_workbook.py      # Optional bounded local XLSX edge
│   └── modules/
│       ├── evidence/
│       │   ├── __init__.py
│       │   └── snapshots.py    # Local in-memory CSV structure/as-of only
│       ├── forecasting/
│       │   ├── __init__.py
│       │   └── baselines.py    # Offline staged as-of one-step evaluation
│       └── simulation/
│           └── gateway.py     # Engine-neutral simulation interface
├── tests/
│   ├── unit/test_contracts.py
│   ├── unit/test_m1_observation_preflight.py
│   ├── integration/test_api.py
│   └── integration/test_m1_observation_preflight_cli.py
├── pyproject.toml
└── README.md
```

## Architecture policy
- Maintain a **modular monolith**, one installable Python package and thin FastAPI routers.
- HTTP routes do not perform forecasting, RAG, agent orchestration or simulation calculations.
- `core/` holds only cross-module contracts and shared primitives. Avoid a miscellaneous "utils" or global service locator.
- `modules/` adds a new feature package **only when implementation and tests exist** (future evidence, forecasting, agents, decisions, governance).
- Sector-specific logic will live in a separate `domains/` adapter package once the retail MVP is implemented. No retail dependency inside platform modules.
- `modules/simulation/gateway.py` defines the interface to WorldKernel. No WorldKernel import in the platform's core; the optional adapter will be added later.
- `tests/unit/` validates isolated contracts and algorithms; `tests/integration/` validates HTTP and adapters. Add an `e2e/` suite only when a real end-to-end flow exists.
- Future React UI, background workers, and deployment manifests get dedicated `apps/` or `infra/` directories **only when needed**. Do not create empty directories or microservices prematurely.
- Direct endpoint imports remain `uvicorn mirrormind.api:app` for compatibility.

## Experimental examples are not production capabilities

`examples/m1_observation_preflight.py` is intentionally
outside `src/mirrormind/`: it is a reproducible standalone
exercise with no real-data connector, no forecast and no
WorldKernel adapter. It is tested and surfaced as
`experimental` in the reviewed capability ledger,
not as an implemented API evidence module.

The local structural evidence preflight has now been added to
`src/mirrormind/modules/evidence/snapshots.py` with
isolated tests. It **does not** implement permissions.
The first actual **authorized connector** or deployed forecast
must still await validated data rights, availability history,
quality, evaluation and security acceptance criteria. See
[M1 preflight](engineering/M1_DATA_PREFLIGHT.md)
and [the capability gates](engineering/CAPABILITY_GATES.md).

## Experimental one-step backtest

[`examples/m1_temporal_backtest.py`](../examples/m1_temporal_backtest.py)
and [`examples/synthetic-weekly-sales.json`](../examples/synthetic-weekly-sales.json)
are intentionally outside the production forecasting package.
The [M1 evaluation guide](engineering/M1_TEMPORAL_BACKTEST.md)
and [synthetic model card](engineering/model_cards/SYNTHETIC_WEEKLY_BASELINES.md)
describe a fixed one-step toy comparison, not a new API endpoint,
model-serving layer or WorldKernel integration.

## Synthetic-only publication-time experiment

[`examples/m1_availability_preflight.py`](../examples/m1_availability_preflight.py)
and [`examples/synthetic-asof-sales.json`](../examples/synthetic-asof-sales.json)
are local teaching fixtures, not modules inside the
production evidence engine or forecast service.
Read [M1 availability](engineering/M1_AVAILABILITY_PRECHECK.md)
and the corresponding [synthetic dataset card](engineering/datasets/SYNTHETIC_AVAILABILITY_CARD.md).

## As-of availability-aware backtest demonstration

[`examples/m1_asof_rolling_backtest.py`](../examples/m1_asof_rolling_backtest.py)
and [`examples/synthetic-asof-weekly-sales.json`](../examples/synthetic-asof-weekly-sales.json)
reproduce the previously separate toy data-availability
and baseline methods. The
[guide](engineering/M1_ASOF_ROLLING_EVALUATION.md),
[dataset card](engineering/datasets/SYNTHETIC_ASOF_WEEKLY_CARD.md)
and [model card](engineering/model_cards/SYNTHETIC_ASOF_WEEKLY_BASELINES.md)
document their deliberately narrow experimental scope.

## Reusable staged CSV primitive (non-authorized)

[`src/mirrormind/modules/evidence/snapshots.py`](../src/mirrormind/modules/evidence/snapshots.py)
checks bytes, source-declared calendar fields and integrity
against a supplied digest, without any external source,
API, persistence or grant validation. Read the
[method guide](engineering/M1_LOCAL_CSV_STAGING.md).
Its example [CSV](../examples/staged-daily-observations.csv)
is invented, and its tests [unit](../tests/unit/test_evidence_snapshots.py)
and [integration](../tests/integration/test_local_snapshot_flow.py)
do not certify any dataset rights.

## Offline staged forecast evaluation (experimental only)

[`src/mirrormind/modules/forecasting/baselines.py`](../src/mirrormind/modules/forecasting/baselines.py)
evaluates two fixed historical one-step heuristics
against the non-authorized local CSV stage output.
It is tested on [invented weekly rows](../examples/staged-weekly-availability.csv)
with [unit](../tests/unit/test_staged_rolling_baselines.py)
and [integration](../tests/integration/test_staged_rolling_flow.py)
tests. The [source guide](engineering/M1_STAGED_ROLLING_BASELINES.md)
and [model card](engineering/model_cards/STAGED_WEEKLY_BASELINES.md)
document **4/7 availability coverage**, not real
predictive performance or public inference serving.

## Retail-domain offline transformation (no real source reader)

[`src/mirrormind/domains/retail/uci_transactions.py`](../src/mirrormind/domains/retail/uci_transactions.py)
provides bounded transaction-line-to-product-day
aggregation outside the generic evidence and
forecasting packages. It accepts only
caller-supplied row mappings, has no XLSX
reader or data rights policy, and preserves
**unknown** historical publication times.
See the [source guide](engineering/UCI_RETAIL_PROJECTION.md),
[fictional data card](engineering/datasets/SYNTHETIC_UCI_ROWS_CARD.md)
and [unit](../tests/unit/test_uci_retail_projection.py) /
[integration](../tests/integration/test_uci_retail_projection_flow.py)
regressions. This is not a live connector
or WorldKernel simulation adapter.

## Experimental local XLSX edge (not full UCI ingestion)

[`src/mirrormind/domains/retail/uci_workbook.py`](../src/mirrormind/domains/retail/uci_workbook.py)
adds an **optional, read-only** XLSX stream parser
with compressed/uncompressed resource checks,
a source-declared digest and a fixed eight-column
sheet contract. It reuses
[`uci_transactions.py`](../src/mirrormind/domains/retail/uci_transactions.py)
for privacy-minimized, positive-line product/day
aggregates, without inventing historical
`available_on` timestamps.
Read the [method guide](engineering/UCI_WORKBOOK_READER.md)
and [fictional data card](engineering/datasets/SYNTHETIC_UCI_XLSX_CARD.md).
Its present row cap intentionally refuses the
original full UCI dataset; nothing is downloaded
or licensed by the reader itself.
