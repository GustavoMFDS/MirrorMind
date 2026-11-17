# Security, privacy and safety expectations

- Data connector credentials are opt-in and are never committed. `.env` and user datasets are gitignored.
- Ingestion must honor authorization, licenses, tenant access, retention and source freshness. Web search text and RAG documents are **untrusted input**, never instructions with tool privileges.
- Human approval for sensitive writes; simulation must never silently execute business changes.
- Model calls and job execution must have server-side budgets, timeouts, cancellation and audit once they are implemented; prompt-only limits are insufficient.
- Track provenance and evaluated model versions; do not present simulated outcomes as guaranteed forecasts or causal proof.
- Logging must redact credentials and sensitive user content.
- The M0 scaffold has **no real authentication, connectors or execution enforcement** and is not production-ready.
