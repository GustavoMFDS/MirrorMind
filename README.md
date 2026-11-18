# MirrorMind

**Evidence-driven agentic decision intelligence platform.**

> **Status (2026-11-17):** architecture approved; API scaffold and contract validation implemented. There are **no live agents, RAG pipelines, forecasts, data connectors, simulations, UI or production guarantees** in the API scaffold. A separate, explicitly synthetic observation preflight is now an **experimental local example**, not real ingestion.

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

## M1 experimental synthetic observation preflight

The first independent M1 training example validates bounded,
invented daily count series against calendar cutoffs and
reports missing dates without inventing replacement values:

```bash
python examples/m1_observation_preflight.py examples/synthetic-daily-sales.json
```

It is **not** authorized ingestion, forecasting, a
WorldKernel execution path or production data governance.
See [the source-backed M1 guide](docs/engineering/M1_DATA_PREFLIGHT.md)
and [capability status ledger](docs/engineering/CAPABILITY_LEDGER.json).

## M1 experimental one-step rolling backtest

```bash
python -m examples.m1_temporal_backtest examples/synthetic-weekly-sales.json
```

This local teaching fixture compares a seasonal-naive lag-7
estimate with a seven-day mean using **only preceding
observations** at each of seven one-day origins. Metrics
and assumptions are [documented](docs/engineering/M1_TEMPORAL_BACKTEST.md).
No real-world forecasting, source authorization, model
calibration, RAG or simulation endpoint is implemented.
The API still reports `forecasting` as planned and this
specific script as `experimental`.

## M1 synthetic availability-time preflight

```bash
python -m examples.m1_availability_preflight examples/synthetic-asof-sales.json
```

The local exercise separates **when an invented event
occurred** from **when its value was supposedly available**
and excludes late or future values from an as-of summary.
It neither confirms actual publication dates nor gives
access to any real dataset. The
[guide](docs/engineering/M1_AVAILABILITY_PRECHECK.md)
and [data card](docs/engineering/datasets/SYNTHETIC_AVAILABILITY_CARD.md)
describe the limits. The Evidence Engine remains planned.

## Synthetic availability-aware rolling evaluation

```bash
python -m examples.m1_asof_rolling_backtest examples/synthetic-asof-weekly-sales.json
```

This local toy exercise only scores a one-day baseline when
all seven previous synthetic observations were **declared
available by that origin**. In the invented example,
three origins abstain and four are scored. See the
[source-reviewed guide](docs/engineering/M1_ASOF_ROLLING_EVALUATION.md).
This neither authenticates publication timestamps nor
constitutes a deployed forecast service.


## M1 local CSV staging library (experimental, in memory only)

The [evidence staging module](docs/engineering/M1_LOCAL_CSV_STAGING.md)
validates bounded local CSV **bytes**, compares them with a
caller-provided SHA-256 expectation, and exposes an
event-time-plus-publication-time historical as-of view.
The resulting receipt explicitly says
`local_structure_checked_not_authorized`.

This does **not** download licensed datasets, authenticate a
publisher or source permission, or implement live forecasting,
RAG, secure multi-tenant ingestion, persistence or a
WorldKernel adapter. The
[example CSV](examples/staged-daily-observations.csv) contains
only invented values. A real-data feature still requires
independent permission, provenance, retention and source
availability review.

## M1 offline staged baseline comparison

The [source-level experimental evaluator](docs/engineering/M1_STAGED_ROLLING_BASELINES.md)
compares fixed one-day seasonal-naive lag 7 and
trailing-mean lag 7 using only rows that the
structural staging layer says were available
at each **historical** origin. It reports
missing-history/target abstentions and compares
models on the same scored subset.

This is not trained or production forecasting.
The invented [CSV fixture](examples/staged-weekly-availability.csv)
and [synthetic model card](docs/engineering/model_cards/STAGED_WEEKLY_BASELINES.md)
provide a reproducible learning example, not
permission to process third-party data or
empirical evidence of predictive accuracy.
