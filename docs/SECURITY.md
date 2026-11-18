# Security, privacy and safety expectations

- Data connector credentials are opt-in and are never committed. `.env` and user datasets are gitignored.
- Ingestion must honor authorization, licenses, tenant access, retention and source freshness. Web search text and RAG documents are **untrusted input**, never instructions with tool privileges.
- Human approval for sensitive writes; simulation must never silently execute business changes.
- Model calls and job execution must have server-side budgets, timeouts, cancellation and audit once they are implemented; prompt-only limits are insufficient.
- Track provenance and evaluated model versions; do not present simulated outcomes as guaranteed forecasts or causal proof.
- Logging must redact credentials and sensitive user content.
- The M0 scaffold has **no real authentication, connectors or execution enforcement** and is not production-ready.

## Experimental M1 synthetic fixture boundary

The standalone [M1 data preflight](engineering/M1_DATA_PREFLIGHT.md)
is intentionally synthetic-only. It enforces local byte,
row and declared calendar cutoffs but **does not** verify
source authorization, provenance truth or historical data
availability. Do not use private or customer data as a
shortcut demonstration, do not promote its source labels
to verified evidence, and do not describe its numerical
summary as a forecast or business outcome.
