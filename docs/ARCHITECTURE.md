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
The HTTP application, typed scenario contract, budget **input validation**, gateway Protocol and one pure WorldKernel request mapper are implemented. The mapper constructs a strict v1 request for an allowlisted retail-world revision; it does not install or execute WorldKernel. A bounded, deterministic `modules/evidence/snapshots.py` stages **local CSV bytes in memory** with a non-authorized receipt and an as-of selector; it is **not** authenticated source ingestion or RAG. Standalone synthetic examples under `examples/` are also experimental, not live forecasting. Budgets are **not enforced at execution** yet. No agents, RAG, **operational forecasting**, workers, multi-tenant auth or simulation endpoints exist. The new `modules/forecasting/baselines.py` offers an **offline experimental** comparison of two fixed daily historical heuristics over source-unverified staged data.

## Delivery philosophy
Start as a modular monolith with replaceable workers and strong interface boundaries. Add Redis, Postgres, pgvector, DuckDB, LangGraph, OpenTelemetry, Docker workers and infrastructure only as needed by working features and tests.

## Physical source layout (2026-11-17)
`src/mirrormind/api/` contains HTTP adapters and must not implement forecasts, RAG, simulation or business rules. `src/mirrormind/core/` contains versioned shared contracts. `src/mirrormind/modules/` contains domain-neutral capability modules, including the `simulation/gateway.py` interface and pure `simulation/worldkernel_mapping.py` request builder, the experimental `evidence/snapshots.py` structural parser, and experimental `forecasting/baselines.py` offline evaluation. Domain-specific adapters (starting with retail) and UI/workers should be introduced when there are tested implementations, rather than empty speculative directories. See [STRUCTURE.md](STRUCTURE.md).

## Retail-specific transaction projection is not platform-wide ingestion

A new `domains/retail/uci_transactions.py`
experimental offline projection handles only
**already supplied, UCI-shaped fictional
transaction mappings**. It is deliberately
separate from the generic evidence snapshot
module and forecast evaluator. The
[source-method contract](engineering/UCI_RETAIL_PROJECTION.md)
reports positive invoice-line counts, exclusion
reasons and source rights/publication-time uncertainty.
No UCI workbook reader, licensed source ingestion,
historical publisher release evidence, data warehouse,
live forecast, agent or WorldKernel dependency
has been introduced.

## Optional bounded UCI-shaped workbook edge

The retail domain now has an **experimental**
[`uci_workbook.py`](../src/mirrormind/domains/retail/uci_workbook.py)
reader for small caller-selected, locally opened
XLSX streams, using an optional `openpyxl`
dependency. It does not open URLs/paths itself,
authenticate rights, provide a general malicious
file sandbox, or accept the full original
UCI dataset with its current row cap.
It delegates the transaction semantics to
[`uci_transactions.py`](../src/mirrormind/domains/retail/uci_transactions.py),
and deliberately produces no verified
first-availability times or deployable forecast.
See the [source-method guide](engineering/UCI_WORKBOOK_READER.md).
