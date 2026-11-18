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
│   └── modules/
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

The first actual evidence/forecast module should only
be added to `src/mirrormind/modules/` after its
data-rights, availability/cutoff, quality, evaluation
and security acceptance criteria are implemented
and independently tested. See
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
