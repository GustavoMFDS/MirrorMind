# Task backlog — prioritized execution register

**Baseline:** PR #51 merge commit `e4f05a152aefcf68fa8ec22f3baa3b61adb8519d`,
see [PROJECT_STATUS](PROJECT_STATUS.md). This is
the maintained task register, not a duplicate roadmap or a promise
of completion. Read [MASTER_EXECUTION_PLAN](MASTER_EXECUTION_PLAN.md),
[DEFINITION_OF_DONE](DEFINITION_OF_DONE.md) and [BLOCKERS](BLOCKERS.md).
On resuming work, reconcile with actual branches, open PRs, merged
commits and independently observed evidence. Do not duplicate work
already underway.

## Reconciled state at the PR #51 baseline

| State | Items / evidence | Continuation |
| --- | --- | --- |
| Merged foundations, still experimental | PRs #47–#50 added local/offline signed-fence verification and a nonce-challenged HTTPS reader; PR #51 consolidated the engineering handoff. These do not deliver a deployed trust service or source authorization. | Preserve their existing scope and tests; do not rebuild the governance chain as a substitute for the product path. |
| Partially implemented M1 | M1B-02 now composes separate CSV/XLSX readers, intake metadata and declared temporal checks. M1C-01 already had offline baselines and release backtests; the current stacked branch adds the reproducible evidence-to-evaluation entrypoint. | Keep the two changes reviewable as separate PRs; preserve abstention and per-origin receipts. |
| Ready at the PR #51 baseline | DOC-01 reconciliation; G-01 minimal testable server-side current-head response; M1E-01 simulation contract work; M1F-01 decision trace contract. DOC-01 is now in review below. | Keep M1 evidence-to-evaluation work ahead of further experimental governance unless a dependency requires G-01. |
| Pending by dependency | Remaining M1C/M1D/M1E/M1F, M2, M3 and M4 rows marked `planned`. | Start only when named predecessors and acceptance inputs exist. |
| Blocked by external evidence or approval | M1B-03 and M1C-03 require B-01/B-02 real-source rights, original availability and empirical holdout evidence. G-04 and deployment-related scopes also require B-03/B-06. | Advance synthetic slices independently; preserve blockers and do not claim they are solved by generated fixtures. |

## Conventions

- `ready`: dependencies for the proposed bounded slice are satisfied.
- `partial`: existing implementation/evidence must be reused; only
  remaining acceptance work is open.
- `planned`: named prerequisite tasks or milestone gates remain.
- `blocked`: an external/owner gate prevents the named acceptance.
- `in_progress`, `review`, `done`: update only after a real claim,
  PR or accepted evidence; do not infer them from file names.
- P0 = unblock the functional MVP or resolve material correctness risk;
  P1 = deliver/strengthen the next functional slice; P2 = later
  hardening or generalization. Within a priority, respect dependencies
  rather than the row order. A prerequisite marked "synthetic" does not
  permit real-data or production claims.

Work item IDs below are stable; subdivide with suffixes when necessary.
A blocker applies to the stated scope, not automatically the whole
repository. Do not work on the same files/branch simultaneously without
coordination.

## A. Engineering and bounded checkpoint governance

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| DOC-01 | P0 | ready | None | Reconcile stale introductory status, semantic map and current source/ledger; preserve dated evidence, resolve conflicting instructions, verify linked atlas. |
| G-01 | P0 | ready | PR #50 | Review existing protocol and implement a minimal testable service-side signed current-head response and independent storage contract; no live deployment. Use existing verifier and canonical signing domain; negative wire/nonce/scope/key tests. |
| G-02 | P0 | planned | G-01 | Authenticated, replay-resistant signed head advance, persistent transactional CAS and exact predecessor checks; reject stale/conflicting/unauthorized writes and test two concurrent writers, interrupted commit and reopen. |
| G-03 | P0 | planned | G-01, G-02 | Actual client/server integration with fictional data, isolated test trust, outages, expiry and failure cases; verify signed remote head mismatch and no permission grants; audit recovery and supplied forks. |
| G-04 | P1 | blocked | G-03, B-03 | Operational trust review: separately administered storage, key custody, identities, monitoring, authenticated access and restore evidence. Do not deploy or claim independence without approval. |
| ENG-01 | P1 | ready | None | Keep canonical checkout clean; record exact gates, check remote CI and improve reproducibility without lowering protections. Review dependency and warning changes separately. |

Use the existing [publisher](ATOMIC_GOVERNED_PUBLISHER.md),
[dual-witness transcript](INTEGRATED_FENCE_TRANSCRIPT.md),
[registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md) and
[HTTPS contract](REMOTE_FENCE_HEAD_CLIENT.md). G-01–03 are a bounded
experimental target, not permission to invent another authority hierarchy.
Complete a tested client/server slice, then spend the main effort on
the vertical product path.

## B. M1 — evidence, forecasts and runnable decision comparison

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M1B-01 | P0 | ready | None | Audit candidate M5/UCI or alternate source permission/provenance, privacy, snapshot and original availability-time evidence; prepare decision-ready review without downloading restricted data. |
| M1B-02 | P0 | partial | None | Compose bounded CSV/workbook staging, review metadata, calendar/release checks and as-of selection into a reusable synthetic evidence flow; deterministic fixture, rejection and abstention tests. |
| M1B-03 | P0 | blocked | M1B-01, M1B-02, B-01, B-02 | Approved real-source adapter with reviewed dataset card, actual source snapshot, permission enforcement, data minimization and provenance; verify temporal availability rather than inventing it. |
| M1C-01 | P0 | partial | M1B-02 | Reuse offline baselines and retail release backtests; build a reproducible synthetic evaluation entrypoint with aligned eligible targets, fixed splits and per-origin receipts. |
| M1C-02 | P0 | planned | M1C-01 | Add justified second candidate model only if needed; predeclare split, parameters, leakage checks and model evaluation contract; compare to seasonal-naive or justified baseline on identical eligible targets. |
| M1C-03 | P0 | blocked | M1B-03, M1C-02, B-02 | Run approved empirical holdout, record actual MAE/RMSE/zero-safe metrics, coverage, abstention and model card; no invented accuracy. |
| M1D-01 | P1 | partial | M1C-01 | Reuse residual envelope, drift and sensitivity code; formalize uncertainty semantics, disjoint calibration/holdout strategy, missing/late data and coverage tests. |
| M1D-02 | P1 | planned | M1C-03, M1D-01 | Evaluate uncertainty on approved held-out observations, document empirical coverage or explicitly uncalibrated limits and sensitivity. |
| M1E-01 | P0 | ready | None | Inspect versioned gateway and actual WorldKernel contract; define strict allowlisted mapping, reject unrepresentable state/interventions/refs, enforce server-owned budgets; test disabled adapter without hard dependency. |
| M1E-02 | P0 | planned | M1E-01, B-04 | Implement optional compatible adapter and execute actual registered test world using pinned compatible engine; deterministic seeds, result validation and missing-engine/failure tests. |
| M1E-03 | P0 | partial | M1E-02, M1C-01 | Three 28-day synthetic policies, paired exogenous streams, explicit units/stock/lead-time/cost assumptions and sensitivity. Do not present synthetic inputs as measured facts. |
| M1F-01 | P0 | ready | None | Versioned decision trace/result contract separating facts, forecasts, simulated outcomes, assumptions, missing evidence, costs and human approval; fixture and invalid-reference tests. |
| M1F-02 | P0 | planned | M1B-02, M1C-01, M1D-01, M1E-03, M1F-01 | Runnable synthetic end-to-end CLI/API with real optional engine when configured; reproducible comparison, no automatic writes, transparent unavailable/abstention outcomes. A test double is explicitly partial. |
| M1F-03 | P0 | planned | M1B-03, M1C-03, M1D-02, M1F-02 | Complete reviewed retail MVP user story using approved observations and evaluated forecasts, actual simulation and documented conditional assumptions; independent replay and review. |

Read [M1 delivery plan](M1_EXECUTION_PLAN.md), [retail MVP](../RETAIL_MVP.md),
[forecast walkthrough](M1_STAGED_ROLLING_BASELINES.md),
[retail backtest](RETAIL_RELEASE_BACKTEST.md), [uncertainty guide](RETAIL_RESIDUAL_ENVELOPE.md),
[WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md) and
[decision trace](DECISION_TRACE_TEMPLATE.md). Do not discard existing
coverage/selection diagnostic modules merely because they are local.

## C. M2 — grounded AI and usable workflow

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M2-01 | P1 | planned | M1F-01 | Typed evidence query and retrieval contracts; permission-filtered indexing and citation mapping using authorized or fictional fixtures; deny untrusted instructions. |
| M2-02 | P1 | planned | M2-01 | Retrieval evaluation with a declared test set, citation support and abstention; preserve document lineage and access constraints. |
| M2-03 | P1 | planned | M1F-02, M2-01 | Typed tool registry and bounded agent orchestration over actual evidence/forecast/simulation tools; provider test double, invalid-tool/input/output and prompt-injection regressions; justified framework choice. |
| M2-04 | P1 | planned | M2-02, M2-03 | Real provider evaluation only with B-05 approval; trace tool calls, model/call budgets, evidence refs, limitations and human confirmation; no unsupported numeric claims. |
| M2-05 | P1 | planned | M1F-02, M2-03 | Usable local/API/UI decision workflow with status, reproducible reports, uncertainty and review; demonstrate normal and failure paths. |
| M2-06 | P1 | planned | M1F-03, M2-04, M2-05 | Reviewed applied-AI acceptance with approved data, grounded comparison and explicit human approval. |

Security and budget controls cannot be postponed until after an
untrusted provider/tool is exposed. Build the required narrow controls
with each executable slice; M3 consolidates operational enforcement.

## D. M3 — durable and secure operations

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M3-01 | P1 | planned | M1F-01 | Reviewed identity/tenant model, authenticated authorization at data/tool/job boundaries and cross-tenant deny tests. |
| M3-02 | P1 | planned | M1F-02, M3-01 | Durable bounded job execution, idempotency, cancellation, timeout, crash recovery and versioned persisted outcomes. |
| M3-03 | P1 | planned | M2-03, M3-02 | Enforced server budgets for model calls/tokens and separate compute/simulation work; concurrency, overspend and denial tests. |
| M3-04 | P1 | planned | M3-01, M3-02 | Redacted logs/tracing, secret handling, health, operational metrics, recovery runbook and backup validation. |
| M3-05 | P2 | planned | M3-03, M3-04, B-06 | Measured performance/load and failure/recovery, documented target environment, reviewed threat model and release readiness; no production guarantee from unit tests. |

## E. M4 — generalization

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M4-01 | P2 | planned | M1F-02 | Compare core contracts against a distinct candidate domain, justify a reference workflow and choose with owner review if scope changes. |
| M4-02 | P2 | planned | M4-01, M2-05 | Add a second domain adapter, appropriate data/model/decision contracts and actual reproducible reference workflow; core has no retail-specific dependencies. |
| M4-03 | P2 | planned | M4-02, M3-05 | Verify version compatibility, optional-engine separation, regression across domains and reproducible release acceptance; owner release decision remains separate. |

## Task claim and update format

For each active task, add a short row/note below (or link its scoped
change request) with owner/agent, branch or worktree, expected touched
surfaces, current status, exact PR/commit, evidence, next action and
blocker IDs. Change status only when supported. Keep temporary details
in the task PR instead of accumulating duplicated logs here.

Example (**format only, not an actual claimed task**):
`M1B-02 | in_progress | agent / feat/... | source staging, tests | PR pending | next: negative cutoff test`.

To mark a task `done`, link reviewed implementation and actual test
results satisfying the relevant [definition of done](DEFINITION_OF_DONE.md).
If a gate fails, preserve the failure and choose the next safe
independent slice. A blocker resolved for a synthetic fixture does
not automatically resolve real-source, deployment or product gates.

## Active claims — reconciled 2026-11-24

| ID | Status | Owner / branch | Surfaces | PR / commit | Evidence and next action | Blockers |
| --- | --- | --- | --- | --- | --- | --- |
| DOC-01 | done | Codex / `codex/m1e-03-synthetic-policy-simulation` | Reconcile PR #51 baseline, current code/PRs, blocker evidence, architecture, learning maps and Graphify docs index | Current continuation, M1E-03 change request | PRs #52–#58 and exact inspected heads were reconciled; the selected docs/engineering graph covers 107 files, 200 nodes, 343 edges and 13 communities. Generated Graphify artifacts remain local and ignored by Git. | No local reconciliation work remains; B-08 affects official PR checks, not this task |
| M1B-01 | partial | Codex / `codex/m1b-01-source-review` | M5/UCI rights, privacy, availability and snapshot due diligence | [PR #57 draft](https://github.com/GustavoMFDS/MirrorMind/pull/57), `646e4db6991b1769c922cf87a0b85630039915da` | Review records M5 no-go and UCI as a candidate only; documentation guards passed and no software tests were needed. Human permission decision and PR review remain open. | B-01/B-02; B-08 |
| M1B-02 | partial | Codex / `codex/m1b-02-synthetic-evidence-flow` | CSV/XLSX local composition, review metadata, calendar/release/as-of checks, tests and docs | [PR #52 draft](https://github.com/GustavoMFDS/MirrorMind/pull/52), code SHA `c51ab30370db47e9f7105c97f870008e4fc442c5`, latest PR head `5c307e426c43aee4179e3257d7d367214e8c3a63` | Canonical gate on exact implementation SHA passed 696 tests including API and all six local stages. Latest head is documentation-only; run its exact-head gate, then review/merge externally. | B-01/B-02 for real data; B-08 |
| M1C-01 | partial | Codex / `codex/m1c-01-synthetic-retail-evaluation` | Prepared UCI-shaped flow, matched fixed baselines, fictional CLI and sanitized origin receipts | [PR #53 draft](https://github.com/GustavoMFDS/MirrorMind/pull/53), exact head `210f0f382938a67e518df688cc4e19c03d3d7af6`, stacked on #52 | Canonical local gate passed 700 tests including API, Ruff, catalog, atlas, evidence and capability guards. Official checks failed before jobs with B-08; retain draft pending review and CI. | B-01/B-02 for empirical claims; B-08 |
| M1C-02 | done (synthetic method comparison only) | Existing baseline implementation and PR #53 consumer | Two fixed retail baselines, shared eligible origins, predeclared fixed split and model card | Source/test on merged-main baseline plus [PR #53](https://github.com/GustavoMFDS/MirrorMind/pull/53) | `tests/unit/test_retail_release_backtest.py::test_missing_late_and_unpublished_days_abstain_and_models_share_origins` proves matched eligible origins; `M1_RETAIL_SYNTHETIC_EVALUATION.md` explains the fixed fictional split and parameters. This does not satisfy M1C-03. | B-01/B-02 still block empirical evaluation |
| M1C-03 | blocked | Project owner / evidence reviewer | Approved source, locked empirical holdout, metrics and model card | No implementation PR | No eligible approved snapshot or verified historical availability is present. Resume only with reviewed source rights, vintage evidence and immutable snapshot. | B-01/B-02 |
| M1D-01 | partial | Codex / `codex/m1d-01-disjoint-residual-calibration` | Disjoint synthetic calibration/holdout, release-aware uncertainty diagnostics and tests | [PR #56 draft](https://github.com/GustavoMFDS/MirrorMind/pull/56), code `10fe58fc3aca45c27288dcc6055ac5d84ab035af`, latest `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0` | Exact gate on tested docs head `0c2e789256e381c2790c49a14c2acc7802d11b9d` passed 700 tests; docs-only current head passed structural guards. Official checks failed before jobs; PR remains draft. | B-02 for empirical calibration; B-08 |
| M1D-02 | blocked | Project owner / model reviewer | Empirical uncertainty coverage and sensitivity on approved held-out observations | No implementation PR | Requires the approved M1C-03 snapshot and held-out outcomes; synthetic envelopes remain uncalibrated. | B-01/B-02 |
| M1E-01 | partial | Codex / `codex/m1e-01-worldkernel-mapping` | Strict versioned request mapping, unit/state/parameter validation, operator ceilings | [PR #55 draft](https://github.com/GustavoMFDS/MirrorMind/pull/55), latest `fcd478130c26c653d0d1d9f4d2f905bf24eaf3a9` | 25 mapping tests and canonical gate passed 737 tests on `2330dc50a49bb80abc601b0635e5e7d4916ee283`; latest docs-only head passed catalog/atlas/evidence/capability guards. Pure mapping only; no engine call. | B-04 for actual execution; B-08 |
| M1E-02 | blocked | Project owner / WorldKernel maintainer | Pinned optional SDK, registered-world execution, validated output and enforced runtime bounds | No implementation PR | Read-only environment check found no compatible SDK/runtime available in this checkout; no cross-repository changes are authorized by this task. | B-04 |
| M1E-03 | partial | Codex / `codex/m1e-03-synthetic-policy-simulation` | Three synthetic 28-day policies, paired seeded streams, explicit units/stock/lead-time/cost assumptions, sensitivity, tests and walkthrough | [PR #58 draft](https://github.com/GustavoMFDS/MirrorMind/pull/58), code commit `09d047b431cc4c50fb6d1abdb88a494a4c7f6f7f` | Canonical local gate passed 747 tests and all six stages, including atlas/evidence/capability. Review remains; this test double is partial until M1E-02 engine acceptance. Official PR checks failed before steps on B-08. | B-04 for actual-engine completion; B-08 for official CI |
| M1F-01 | partial | Codex / `codex/m1f-01-decision-trace-contract` | Versioned result contract and exact-result human review binding | [PR #54 draft](https://github.com/GustavoMFDS/MirrorMind/pull/54), tested head `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029` | 12 focused tests and canonical full gate passed 712 tests including API; capability remains `interface_only`, with no producer or action execution. Official checks failed before jobs. | B-08; real evidence/engine gates remain independent |
| M1F-02 | partial | Codex / `codex/m1f-02-synthetic-decision-workflow` | Bounded synthetic retail evidence-to-trace service, CLI/API, abstentions, forecast profile, tests and walkthrough | PR pending; based on local dependency stack `c17d505` (#58 + #56) | Focused and canonical local evidence pending final run. No permitted data, empirical forecast, calibrated uncertainty, WorldKernel call, human approval, persistence or business write. | B-04 for actual engine; B-01/B-02 for real data; B-08 for official CI |
