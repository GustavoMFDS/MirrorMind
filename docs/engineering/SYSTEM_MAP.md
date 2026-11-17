# MirrorMind — system map

Updated from the initial scaffold on 2026-11-17. **Only** the foundational API/contracts and simulation gateway interface exist. Do not describe planned agents or forecasts as shipped.

## Current request path

HTTP request → `src/mirrormind/api/app.py` → thin routes `api/routes/system.py` or `api/routes/scenarios.py` → validation with `core/contracts.py` → response. The `modules/simulation/gateway.py` interface defines an engine-neutral boundary; it does **not** execute WorldKernel simulations yet.

Current supported routes: `GET /health`, `GET /v1/capabilities`, and `POST /v1/scenarios/validate`. See [CONTRACTS](../CONTRACTS.md) and [STRUCTURE](../STRUCTURE.md).

## Change-location guide
| User request | Inspect first | Evidence |
| --- | --- | --- |
| Change versioned scenario data | `core/contracts.py`, `api/routes/scenarios.py` | `tests/unit/test_contracts.py`, `tests/integration/test_api.py` |
| Change health/capabilities | `api/routes/system.py`, `api/app.py` | `tests/integration/test_api.py` |
| Add simulation execution | `modules/simulation/gateway.py`, `core/contracts.py` | New adapter/contract tests; separate WorldKernel integration review |
| Introduce evidence/RAG | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md) | New module, permission/provenance tests **only after implementation** |
| Introduce forecasting | [RETAIL_MVP](../RETAIL_MVP.md), [ROADMAP](../ROADMAP.md) | New evaluation/leakage tests **only after implementation** |
| Add agents/orchestration | [ARCHITECTURE](../ARCHITECTURE.md), [SECURITY](../SECURITY.md) | Tool permissions, cost budgets and audit tests when created |

## Non-negotiable boundaries
- General-purpose decision platform; retail is the first reference domain, not a hard-coded limitation.
- Keep **observed evidence**, **forecast estimates** and **simulated counterfactuals** conceptually separate.
- No core dependency on WorldKernel. Integrate through an optional, versioned simulation gateway.
- Preserve permission provenance and human review; don't claim live agents, RAG, forecasting, connectors or simulations until implemented and tested.
- An interface alone does not establish functioning integration.

See [ARCHITECTURE](../ARCHITECTURE.md), [DECISIONS](../DECISIONS.md), [ROADMAP](../ROADMAP.md), [STRUCTURE](../STRUCTURE.md).