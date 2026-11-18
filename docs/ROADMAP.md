# Milestones

- **MM-M0 — Completed scaffold:** FastAPI, `/health`, `/v1/capabilities`, scenario contract validation, tests, Docker and CI, decision log.
- **MM-M1 — Planned retail fundamentals:** ingest permitted M5 subset, validate cutoff, backtest two demand models, run first inventory simulation through gateway.
- **MM-M2 — Planned AI application:** evidence/RAG, agent tool workflow, traceable scenario analysis, UI and human review.
- **MM-M3 — Planned engineering:** durable async jobs, token/call and compute budgets enforced, tracing, RBAC, tenant separation, failure recovery and load tests.
- **MM-M4 — Planned generalization:** at least one *different* domain adapter, versioned contracts and validated WorldKernel integration.

Acceptance gates: working runnable example, tests, clear metrics, provenance, resource limits and a truthful status statement. No production claims until validated.

- **MM-DOC-A1 — Completed (documentation and Python CI validated):** enforce a committed
  AST index, human-reviewed linked repository atlas, real tracked-file inventory
  and local Markdown link integrity in documentation CI. This is strictly
  structural; it does not certify semantic understanding, data lineage,
  privacy, quality of forecasts or security. Next gates: source-reviewed
  method lessons, curated test evidence and stricter claim/decision traceability.

- **MM-DOC-A2 — In progress (semantic and evidence teaching):** source-reviewed
  [ScenarioSpec walkthrough](engineering/CONTRACT_WALKTHROUGH.md),
  [API walkthrough](engineering/API_WALKTHROUGH.md) and 11-module
  [semantic map](engineering/SEMANTIC_COVERAGE.md). A curated
  [claim-to-test index](engineering/EVIDENCE_MAP.json) records precise
  pytest function references and limitations; CI checks structural
  integrity only, not reasoning validity or product readiness.

- **MM-DOC-A3 — Capability truth guard (CI validation required):**
  maintain a reviewed [capability ledger](engineering/CAPABILITY_LEDGER.json)
  with strict implemented/experimental/interface-only/planned statuses,
  source/test evidence and explicit caveats. A structural checker and
  live API regression must catch claims that diverge from the actual
  `GET /v1/capabilities` response. This protects against overclaiming,
  but does not certify the implementation, scientific validity or security.

- **MM-M1a — Experimental groundwork (not the M1 acceptance gate):**
  standalone, bounded [synthetic daily-observation preflight](engineering/M1_DATA_PREFLIGHT.md)
  with canonical dates, future-cutoff rejection, duplicate and
  missing-day diagnosis, safe CLI errors and regression tests.
  No source license/provenance verification, real-data connector,
  temporal backtest, demand forecast, AI agent or WorldKernel
  integration. `GET /v1/capabilities` labels the example
  **experimental**; all real evidence/forecast functionality stays
  planned until independently validated.
