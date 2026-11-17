# Debugging and recovery playbook

This guide is a **method**, not an automated repair service.

## Evidence-first procedure
1. Define the observed symptom, expected behavior, runtime configuration and a safe reproducer. Preserve the failing input's schema, not private payloads or credentials.
2. Capture timestamp, version/commit, relevant feature flags, sanitized logs, a correlation/job ID if one exists, and stack trace.
3. Find the entrypoint in [SYSTEM_MAP](SYSTEM_MAP.md), then the symbol in the [generated catalog](generated/SYMBOLS.md). Follow callers, state mutations, contracts and related tests.
4. Generate competing root-cause hypotheses. Confirm or falsify with a focused test; never assume the AI-generated explanation is correct.
5. Fix the smallest relevant location, add a regression test for the observed failure, and run relevant broader tests.
6. Document the verified root cause, remediation, limitations, safe rollback and monitoring. Update the associated runbook in the PR.

## Incident note template
```text
Symptom:
Commit/version and environment:
How to reproduce (safe):
Observed / expected:
Relevant modules and stacktrace:
Evidence for root cause:
Mitigation / rollback:
Fix and regression test:
What is still unknown:
```

Never paste secrets, access tokens, user records, raw customer datasets or private prompt contents into agent context or public documentation.

## MirrorMind starting points
- Scenario-validation error: `api/routes/scenarios.py` → `core/contracts.py`; inspect `tests/unit/test_contracts.py`.
- Service/router mismatch: `api/app.py`, `api/routes/system.py`, `tests/integration/test_api.py`.
- Missing capability: check `GET /v1/capabilities` and [ROADMAP](../ROADMAP.md) before diagnosing a future feature as broken.
- Integrating WorldKernel: inspect `modules/simulation/gateway.py` and versioned contracts. An interface is not live execution.
- For planned evidence/agents, design permission-bound provenance, error handling and budget limits before implementing.

Useful local checks:
```bash
python -m pytest -q
python -m ruff check src tests
```
Do not assert connectors, agents, forecasts or simulations are operational without implementation and tests.