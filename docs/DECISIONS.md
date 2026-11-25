# Architecture Decision Log — 2026-11-17

Status: **Accepted**, **Proposed**, **Deferred**. Accepted describes design intent, not a completed feature.

| ID | Status | Decision | Rationale |
| --- | --- | --- | --- |
| MM-001 | Accepted | MirrorMind is general-purpose decision intelligence; retail is first reference adapter. | Demonstrate a concrete case without domain lock-in. |
| MM-002 | Accepted | Evidence, forecast and simulation remain separate bounded responsibilities. | Avoid false certainty and misleading causal claims. |
| MM-003 | Accepted | WorldKernel is fully independent and accessed through versioned gateway contracts. | Multiple clients and independent release lifecycle. |
| MM-004 | Accepted | LLM orchestrates tools; statistical/ML models generate numeric forecasts. | Grounding, reproducibility and audit. |
| MM-005 | Accepted | Treat model-call cost and simulation compute cost as separate, enforceable budgets. | Production engineering and safety. |
| MM-006 | Accepted | Provenance, source permissions, temporal leakage controls and human approval are core requirements. | Data and operational trust. |
| MM-007 | Proposed | LangGraph, PostgreSQL, pgvector, Redis workers, StatsForecast and OpenTelemetry. | Candidates, not irrevocable dependencies. |
| MM-008 | Accepted | Modular monolith for MVP before splitting services. | Scope and operational simplicity. |
| MM-009 | Deferred | Production claims, licensing, hosting and real-company integrations. | Require evidence, tests and owner decisions. |
| MM-010 | Accepted | Starting demonstration: replenishment-policy comparison under forecast uncertainty. | Measurable without pretending to estimate price-promotion causality. |
| MM-011 | Accepted | Source uses one installable Python package: thin HTTP routes in `api/`, shared contracts in `core/`, independent feature modules in `modules/`, and tests split by unit/integration boundary. | Keep the modular monolith extensible without premature microservices or empty feature trees. |
| MM-012 | Accepted | Prepare two independent source-research lanes in sequence: UCI Online Retail #352 event-time retrospective, then aggregate Census release-vintage evaluation; preparation does not authorize real-source acquisition/processing, M5 remains NO-GO, and `InvoiceDate` is never treated as publication availability. | UCI product-level rows and Census aggregate release vintages answer different questions; privacy, permissions and temporal evidence must remain source-specific. Owner direction recorded in [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818). |
| MM-013 | Accepted | Keep WorldKernel one-way and optional; the M1E-02 compatibility slice may execute one trusted registered synthetic demo in a local subprocess at an exact reviewed source SHA. No HTTP execution, arbitrary code, production/sandbox claim or edit to the independent repository follows from this decision. | Test the versioned exchange against a real pinned engine without making API/core depend on WorldKernel or conflating a demo with an inventory model. Owner-approved scope, 2026-11-25. |
| MM-014 | Accepted | While GitHub Actions is unavailable under the owner's no-paid-spend decision, use the documented exact-clean-head six-check local gate, independent review and a separate integrated-candidate gate. Preserve check definitions and protections; local evidence is never CI evidence. | Continue safe work within budget while retaining reproducible verification. Owner direction, 2026-11-25, recorded in [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818). |
