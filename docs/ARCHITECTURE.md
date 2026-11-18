# MirrorMind architecture — proposal 3.0

## Product identity
MirrorMind is a **general-purpose, evidence-driven decision-intelligence platform**. Retail inventory is the first bounded reference domain. No domain is hard-coded into the platform core.

## Proposed modules
1. **API/workspaces:** FastAPI, auth, tenant separation and job tracking.
2. **AI orchestration:** goal interpretation and tool workflows (LangGraph candidate); human approval for sensitive actions.
3. **Evidence Engine:** authorized source ingestion, structured data validation, provenance, document retrieval and RAG, freshness and access controls.
4. **Forecast Engine:** time-series baselines, temporal backtesting, calibrated uncertainty and model versioning.
5. **Simulation Gateway:** validates versioned specs, adapts to engines, checks compute budgets and converts results.
6. **Decision/Evaluation:** compares objectives, risks, assumptions, uncertainty and outcomes.
7. **Governance:** model token/call budgets and compute/time/concurrency budgets, audit, security and tracing.

## Separation of truths
- **Observations:** time-bounded recorded facts with source provenance.
- **Forecasts:** model outputs with uncertainty, evaluation history, and cutoff date.
- **Simulations:** consequences *within an explicit world model* under interventions and assumptions.

A generative model must not fabricate measurements, forecasts or business performance. Predictions must come from evaluated statistical/ML models, with data leakage prevented by cutoff rules.

## Dependency direction
MirrorMind → `SimulationGateway` protocol → optional **independent** WorldKernel adapter. WorldKernel must not import MirrorMind. MirrorMind should boot without WorldKernel and its advanced simulation endpoint must report unavailable until configured.

## Initial status
The HTTP application, typed scenario contract, budget **input validation**, and gateway Protocol are implemented. A bounded, deterministic `modules/evidence/snapshots.py` now stages **local CSV bytes in memory** with a non-authorized receipt and an as-of selector; it is **not** authenticated source ingestion or RAG. Standalone synthetic examples under `examples/` are also experimental, not live forecasting. Budgets are **not enforced at execution** yet. No agents, RAG, **operational forecasting**, workers, multi-tenant auth or simulation endpoints exist. The new `modules/forecasting/baselines.py` offers an **offline experimental** comparison of two fixed daily historical heuristics over source-unverified staged data.

## Delivery philosophy
Start as a modular monolith with replaceable workers and strong interface boundaries. Add Redis, Postgres, pgvector, DuckDB, LangGraph, OpenTelemetry, Docker workers and infrastructure only as needed by working features and tests.

## Physical source layout (2026-11-17)
`src/mirrormind/api/` contains HTTP adapters and must not implement forecasts, RAG, simulation or business rules. `src/mirrormind/core/` contains versioned shared contracts. `src/mirrormind/modules/` contains domain-neutral capability modules (currently `simulation/gateway.py`, the experimental `evidence/snapshots.py` structural parser, and experimental `forecasting/baselines.py` offline evaluation). Domain-specific adapters (starting with retail) and UI/workers should be introduced when there are tested implementations, rather than empty speculative directories. See [STRUCTURE.md](STRUCTURE.md).
