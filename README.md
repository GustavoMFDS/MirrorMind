# MirrorMind

**Evidence-driven agentic decision intelligence platform.**

> **Status (2026-11-17):** architecture approved; API scaffold and contract validation implemented. There are **no live agents, RAG pipelines, forecasts, data connectors, simulations, UI or production guarantees** in this initial commit.

MirrorMind is a **general-purpose** platform for grounded decisions: authorized data → evidence + forecasting → alternative scenarios → simulation → traceable comparison and human review. **Retail inventory planning is the first reference use case, not a hard-coded product limitation.**

## Why it matters
- Separate **observed facts**, **predictions with uncertainty**, and **simulated outcomes based on assumptions**.
- Govern AI model costs *and* compute/simulation budgets.
- Reproduce evaluations, preserve provenance and expose model limitations.
- Support domain adapters rather than tying the platform to retail.

## Architecture
- FastAPI application and typed, versioned scenario contracts.
- Future modules: evidence engine (authorized sources and RAG), forecast engine (time-series backtesting), agentic orchestration (candidate: LangGraph), decision evaluation, security and observability.
- Simulation gateway with a replaceable adapter. **WorldKernel is an independent Python engine** and an optional integration, not a module inside MirrorMind.

## Repository organization
The API has thin routes; shared contracts live in `core/`; business capabilities are isolated under `modules/`. **Only simulation-gateway interfaces exist today; evidence, forecasting, agents and decisions are future modules.** See [structure](docs/STRUCTURE.md).

## Run the scaffold
```bash
python -m venv .venv
# activate the environment, then:
python -m pip install -e ".[dev]"
uvicorn mirrormind.api:app --reload
python -m pytest
```

Open `http://127.0.0.1:8000/docs`. Current routes:
- `GET /health`: application heartbeat.
- `GET /v1/capabilities`: explicitly reports what is not implemented.
- `POST /v1/scenarios/validate`: validates a versioned scenario **without running anything**.

Alternatively: `docker compose up --build` (requires Docker). Only the API scaffold is started.

## Reference documentation
- [Repository structure](docs/STRUCTURE.md)
- [Architecture and boundaries](docs/ARCHITECTURE.md)
- [Accepted decisions](docs/DECISIONS.md)
- [Scenario contract](docs/CONTRACTS.md)
- [First use case — retail](docs/RETAIL_MVP.md)
- [Roadmap and acceptance criteria](docs/ROADMAP.md)
- [Security and evidence handling](docs/SECURITY.md)

## Living engineering documentation

The [engineering knowledge hub](docs/engineering/README.md) explains how to trace features, locate functions, diagnose failures, propose changes to coding agents and learn the implementation. For future changes, copy the [change request template](docs/engineering/CHANGE_REQUEST_TEMPLATE.md), follow [AGENTS.md](AGENTS.md) and regenerate the Python symbol catalog with `python scripts/docs/catalog.py --write`. These docs do not change runtime capabilities or project scope.

## License
Not selected yet. Repository is private; a release/license decision is deferred.
