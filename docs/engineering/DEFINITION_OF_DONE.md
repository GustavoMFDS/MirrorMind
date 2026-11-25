# Definition of done — behavior, evidence and review

This document establishes **acceptance criteria**, not a statement
that those criteria have been met. The [master execution plan](MASTER_EXECUTION_PLAN.md)
defines sequence; [task backlog](TASK_BACKLOG.md) records task status.
[AGENTS.md](../../AGENTS.md), [capability gates](CAPABILITY_GATES.md),
[security expectations](../SECURITY.md), and [accepted decisions](../DECISIONS.md)
remain authoritative.

## Every substantive work item / PR

A work item is eligible for completion when all applicable items
below have verifiable evidence:

- Explicit scoped change request, acceptance criteria, impact map,
  touched contracts, failure/recovery plan and non-goals.
- Real implementation, not an empty namespace, fake result or schema
  presented as a feature. Trace its public entrypoint, code, callers,
  storage, downstream consumers and error behavior.
- Unit and integration tests proportionate to the change, including
  happy path, malformed/adverse inputs, failure paths, boundary
  budgets, regressions and authorization/tenant cases as applicable.
- Scientific claims independently tested for cutoff, holdout,
  reproducibility, and uncertainty where relevant. No real source data
  without reviewed permission and minimization.
- Human-readable source walkthrough, architecture/data-flow updates,
  debug/recovery instructions and a learner exercise. See the mandatory
  [documentation standard in the handoff](CODEX_HANDOFF.md).
- Actual source links in the atlas, regenerated symbol catalog when
  needed, evidence IDs with exact pytest selectors and limitations,
  capability ledger and API parity for user-visible changes.
- Backward compatibility or explicitly reviewed migration, including
  rollback/restart tests when state changes. No silent cross-repo edits.
- Meaningful local tests and all applicable gates on an identified SHA;
  exact remote check status, not a fabricated CI approval.
- Reviewable branch/PR, no uncommitted user work discarded, verified
  merge requirements. A task may be implemented but not accepted
  while review, evidence or merge is pending.

### Standard local checks

```powershell
uv run --no-sync --extra dev python scripts/docs/catalog.py --write
uv run --no-sync --extra dev python -m pytest -q
uv run --no-sync --extra dev ruff check src tests
uv run --no-sync --extra dev python scripts/docs/catalog.py --check
uv run --no-sync --extra dev python scripts/docs/coverage.py --check
uv run --no-sync --extra dev python scripts/docs/evidence.py --check
uv run --no-sync --extra dev python scripts/docs/capabilities.py --check
git diff --check
```

For docs-only changes, regenerate symbols only if necessary, never
edit generated files manually. Stage new files before atlas coverage
so the tracked-file inventory includes them. On the committed SHA,
use the [local gate](LOCAL_QUALITY_GATE.md). Record outcomes, exact
selectors and known warnings. If remote CI or an environment is
unavailable, document it as an independent pending check; do not
weaken guards to unblock a PR.

## Milestone exit gates

### M0 — scaffold

- Installable package; health and versioned validation routes work.
- Validation is distinct from execution; gateway interface remains
  optional; reproducible unit/API regressions, CI configuration.
- Architecture and docs accurately describe the narrow scope.

### G — bounded governance service experiment (supports M1b)

- Match the [existing HTTPS wire contract](REMOTE_FENCE_HEAD_CLIENT.md)
  with an experimental server, distinct configured signing roles,
  authenticated and replay-resistant head advancement, strict input
  validation, atomic persistent history/CAS and restart recovery.
- Verify no unsigned, stale, revoked or conflicting update advances
  the head; test unavailable signer, malformed request, wrong scope,
  concurrent writers and interrupted persistence; add actual
  client/server integration on a test-only loopback or equivalent
  isolated transport, with test trust roots.
- Recovery and fork evidence are auditable, and all receipts remain
  non-authorizing until a separate accepted ingestion design exists.
- Separate operational acceptance: human-reviewed deployment,
  independently protected storage and keys, operator identity,
  authenticated access, monitoring, incident response and tested
  backup/restore. Synthetic tests do not establish that acceptance.
  Do not block all synthetic M1 work on operational acceptance.

### M1a-b — authorized evidence

- A bounded, reviewed data-source adapter with immutable snapshot
  identity, schema, units, entity constraints, permission scope,
  provenance, revision semantics, availability-time cutoff and
  retention/privacy controls. No silent imputation of missing values.
- Completed [dataset card](DATASET_CARD_TEMPLATE.md), independent
  rights/availability review and negative authorization/leakage tests.
- A deterministic sanitized fixture and actual approved snapshot run.
  Synthetic-only staging cannot satisfy the actual-source gate.

### M1c-d — forecast and uncertainty

- Two declared evaluated models including seasonal-naive or another
  justified baseline, same eligible targets, predeclared temporal
  train/validation/test split and immutable held-out evaluation.
- Rolling-origin evaluation with cutoff at each origin, MAE/RMSE and
  zero-safe metrics, denominator and coverage/abstention reporting;
  explicit missingness, drift and leakage tests.
- Uncertainty method validated on disjoint data where possible or
  explicitly declared uncalibrated; coverage and sensitivity results
  with assumptions, not promises.
- [Model card](FORECAST_MODEL_CARD_TEMPLATE.md), versions, reproducible
  inputs, actual empirical scores from approved data. A perfect toy
  score is not evidence of real accuracy.

### M1e-f — simulation and decision workflow

- [WorldKernel gateway acceptance](WORLDKERNEL_GATEWAY_GATE.md):
  explicit allowlisted mapping, version compatibility, validated
  units/state, reject unsupported fields/references and independently
  enforced local timeout/output bounds. The exact optional engine is
  actually registered and its result is validated; API boot works without
  the optional dependency. These local bounds do not provide CPU/memory
  isolation or qualify the current demo as a lead-time inventory model.
- At least three inventory policies over the declared 28-day reference
  horizon, paired random streams where appropriate, repeatable seeds,
  risk/cost/stock/service metrics and assumption sensitivity.
- [Decision trace](DECISION_TRACE_TEMPLATE.md) separates verified
  observations, evaluated forecasts, synthetic inputs and conditional
  modeled outcomes; versioned evidence refs, result provenance,
  uncertainty, budgets, limitations and human review.
- A documented runnable user story with an actual engine and approved
  dataset, or explicitly partial synthetic demonstration if gates
  remain open. No automatic ordering/business writes.

### M2 — applied AI

- Retrieval over authorized sources with permission filtering,
  citation/lineage and untrusted-content boundaries. Evaluate retrieval
  quality and citation support against an explicit test set.
- Typed tools and bounded orchestration; tested refusal of unauthorized
  tool use, unsupported evidence, prompt injection and invalid results.
  Model outputs cannot substitute for numeric forecast/simulation
  computation.
- Reproducible decision comparison through a usable workflow;
  uncertainty/abstention, human approval, provenance and audit.
- Provider/model choice justified; test doubles clearly separated from
  live provider evidence. Live credentials and costs require approval.

### M3 — engineering and operation

- Auth and tenant isolation enforced by code at every sensitive read,
  write and job boundary; negative cross-tenant tests.
- Durable idempotent jobs, cancellation/timeouts, retry semantics,
  failure recovery and versioned results; server-enforced model-call
  and compute budgets with overspend and concurrency tests.
- Redacted structured logging/traces, monitored health, secure secret
  handling, deployment/runbook/backup and restoration procedures.
- Measured load/failure/recovery evidence against documented goals,
  reviewed threat model and explicit environment/operational acceptance.
  Production release remains an owner decision.

### M4 — generalization

- A second distinct domain with its own authorized input or clearly
  labeled synthetic reference, contracts, adapter and decision story.
- Core and gateway remain independent of retail; explicit adapter
  versioning, compatibility and regression tests across both domains.
- Actual supported-domain demonstration, not only a new schema or
  stub. Independent release lifecycle for WorldKernel.

## Product completion

A research/engineering prototype, a functional retail MVP, and an
operational production release are distinct levels. Do not invent
progress percentages. Close milestones only against their named
criteria and accepted evidence; document residual blockers and obtain
human review for changes in scope or release readiness.
