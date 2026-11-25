# Architecture Decision Log — 2026-11-25

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
| MM-012 | Accepted | Research sequence is A then B: prepare a privacy-minimized, local UCI Online Retail #352 event-time retrospective pilot, then an independent aggregate Census release-vintage pilot; ALFRED is conditional on free authorized access, series terms and adequate archive evidence. | UCI has no row-level publication vintages, while aggregate published releases can support a separate, explicitly scoped temporal study. This authorizes preparation only, not acquisition or processing of either source. |
| MM-013 | Accepted | While GitHub Actions quota is exhausted and no paid usage or limit increase is authorized, use the exact-head six-check local gate as temporary evidence. Keep official CI status distinct and preserve repository settings and checks. | Continue independent work without presenting local results as CI or changing protection and verification policy. |
| MM-014 | Accepted | Keep UCI Online Retail evaluation explicitly event-time retrospective: freeze cohort and splits, compare fixed baselines on matched pairs, and abstain when date coverage is unverified. Census release-vintage research remains a separate protocol and dataset. | `InvoiceDate` does not establish historical availability. The two source classes have different targets and temporal evidence; neither may stand in for the other. |
