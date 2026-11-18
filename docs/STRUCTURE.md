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
