# Task backlog — prioritized execution register

## Integration candidate - 2026-11-27

The separately reviewed heads of PRs #64 (example maintenance), #60
(experimental scoped BM25 retrieval), and #61 (in-process current-head
responder) are included by normal merges, preserving their ancestry. This
candidate is intended for a single ancestry-preserving PR to main; the
independent combined gate and merge decision are recorded in its PR.
Do not infer approval from this document alone. Once integrated, begin M2-02
against the retrieval interface and continue G-02 only within its scoped
offline contract. No authenticated RBAC, deployed authority, empirical
forecast or production readiness is implied.

PR #63 (synthetic Census) and #65 (UCI reader) remain separate. The latter
records the owner's narrow UCI approval MM-017 through MM-022, a source
snapshot held privately, and a fail-closed stop above 250,000 product-day
groups without metrics. No new source processing, partitioning, cap increase
or Census acquisition is authorized by this integration. Preserve the
2026-12-26 deletion deadline and see the live PR #65 and its manifest for the
latest source-specific evidence. B-01/B-02 and B-08 remain open. The
following dated records retain historical gate and branch information;
where they differ from this queue, use the live PRs and current evidence.

**Baseline:** PR #62 merge commit `a456034c55ed7634ad4768b26788fec09dab1d08`,
see [PROJECT_STATUS](PROJECT_STATUS.md). This is
the maintained task register, not a duplicate roadmap or a promise
of completion. Read [MASTER_EXECUTION_PLAN](MASTER_EXECUTION_PLAN.md),
[DEFINITION_OF_DONE](DEFINITION_OF_DONE.md) and [BLOCKERS](BLOCKERS.md).
On resuming work, reconcile with actual branches, open PRs, merged commits and
independently observed evidence. Do not duplicate work already underway.

## Current queue reconciliation — 2026-11-26

| Work | Current state | Evidence / next gate |
| --- | --- | --- |
| M1 synthetic vertical slice | Integrated experimentally in main `a456034`; PR #52–#59 are incorporated by #62 and their branches are retained. Independent merged-main gate: 835 tests, zero skips, six checks, exact WorldKernel pin. | M1 real-data, empirical forecast and production acceptance remain incomplete; do not close M1 overall. |
| Census vintage evaluator | Separate PR #63, open/non-draft at `b5e989314bcdcb566df479931794a5f56c07d477`, based on main. Exact local gate: 877 tests, zero skips, six checks. | Await independent review. Synthetic only; no Census/ALFRED bytes or source authorization. |
| M2-01 retrieval | PR #60, open/non-draft at `fafdedae3a76398e0450773065e40384c96d1ed7`, based on main. Exact local gate: 845 tests, zero skips, six checks. | Await independent review. Retrieval remains experimental and caller-scope is not authenticated authorization. |
| G-01 responder | PR #61 remains separate on main; the ancestry-preserving sync commit is `66fc9fa001eaa6bd3adbc8f8d1606f3743239d21`. Documentation baseline gate `20ce86bde740d5b46d7aeba4d13138884e211dba` passed 841 tests, zero skips and all six checks with the exact WorldKernel pin. | PR #61 is open/non-draft and ready for independent review. Its live body records the latest exact head/receipt; every later commit needs a fresh gate. No route or operational authority. |
| M2-02 retrieval evaluation | Planned; depends on M2-01. | Start after M2-01 review/integration settles. Use fictional/authorized fixtures; measure citation support, lineage and abstention. |
| ENG-02 examples lint maintenance | Ready as a separate maintenance item. `ruff check examples` on this branch reports five findings in three example files; none of these files differ from main. | Handle in a separate scoped PR; do not fold cleanup into #60/#61/#63. |
| Real-source pilots | Preparation only under the approved UCI then aggregate Census/ALFRED sequence. | B-01/B-02 remain open; keep automated tests synthetic and wait for source-specific rights, privacy, snapshot and temporal evidence. |

GitHub Actions remains unavailable under the zero-paid-budget decision. Use
the exact-clean-head six-check local procedure; receipts are local evidence,
never official CI. No required check, workflow or branch protection is
weakened. The PR #62 final comments
[7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)
and [7181477141](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181477141)
are the review record for the incorporated M1 baseline and PR ordering.

## Historical reconciliation at the PR #51 baseline

| State | Items / evidence | Continuation |
| --- | --- | --- |
| Merged foundations, still experimental | PRs #47–#50 added local/offline signed-fence verification and a nonce-challenged HTTPS reader; PR #51 consolidated the engineering handoff. These do not deliver a deployed trust service or source authorization. | Preserve their existing scope and tests; do not rebuild the governance chain as a substitute for the product path. |
| Partially implemented M1 | M1B-02 now composes separate CSV/XLSX readers, intake metadata and declared temporal checks. M1C-01 already had offline baselines and release backtests; the current stacked branch adds the reproducible evidence-to-evaluation entrypoint. | Keep the two changes reviewable as separate PRs; preserve abstention and per-origin receipts. |
| Ready at the PR #51 baseline | DOC-01 reconciliation; G-01 minimal testable server-side current-head response; M1E-01 simulation contract work; M1F-01 decision trace contract. DOC-01 is now in review below. | Keep M1 evidence-to-evaluation work ahead of further experimental governance unless a dependency requires G-01. |
| Pending by dependency | Remaining M1C/M1D/M1E/M1F, M2, M3 and M4 rows marked `planned`. | Start only when named predecessors and acceptance inputs exist. |
| Blocked by external evidence or approval | M1B-03 and M1C-03 require B-01/B-02 real-source rights, original availability and empirical holdout evidence. G-04 and deployment-related scopes also require B-03/B-06. | Advance synthetic slices independently; preserve blockers and do not claim they are solved by generated fixtures. |

## Merged M1 baseline — 2026-11-26

PR #62 is integrated at `a456034c55ed7634ad4768b26788fec09dab1d08`. Its
ancestry preserves the exact published heads of PRs #52–#59; each head was
verified as an ancestor before the stacked PRs #53–#59 were closed as
incorporated. PR #52 was already merged. Their branches remain available.
The independent exact-main gate passed 835 tests, zero skips and all six local
checks with the reviewed WorldKernel pin. This is not official Actions.

The synthetic M1 evidence-to-decision flow is integrated. M1 remains incomplete
because real-source permission, temporal provenance, empirical evaluation,
broader engine isolation and authenticated human review are open. PRs #60
(M2-01) and #61 (G-01) remain separate. #60 now contains `main` through
ancestry-preserving merge `a5186a6`; its first integrated local gate passed,
and the documentation-inclusive head still needs its exact gate before push
and review. #61 still needs the same sync-and-gate sequence. The Census
selector/evaluator remains a separate descendant and PR.

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
| ENG-02 | P2 | review | None | Resolve five pre-existing Ruff findings in `examples/` as separate maintenance. Preserve behavior; review RUF007 semantics and add boundary regression coverage. PR #64 is open on `codex/eng-02-examples-ruff`; exact-head local gate passed on `ca97ab6` (840 tests, zero skips, six checks); independent review remains. |

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
| M1B-01 | P0 | in_progress | None | Synthetic UCI #352 event-time evaluator, fixed validation/holdout protocol, privacy-minimized output and separate aggregate Census/ALFRED vintage protocol are implemented locally. Both lanes are represented in consolidated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85`, whose six-check exact-head gate passed 832 tests without skips and all five other checks with the reviewed WorldKernel pin installed. Keep real-source acquisition/processing blocked until exact terms, attribution, snapshot, minimization, retention and permission are reviewed. No source permission or real processing is claimed. |
| M1B-02 | P0 | partial | None | Compose bounded CSV/workbook staging, review metadata, calendar/release checks and as-of selection into a reusable synthetic evidence flow; deterministic fixture, rejection and abstention tests. |
| M1B-03 | P0 | blocked | M1B-01, M1B-02, B-01, B-02 | Approved real-source adapter with reviewed dataset card, actual source snapshot, permission enforcement, data minimization and provenance; verify temporal availability rather than inventing it. |
| M1C-01 | P0 | partial | M1B-02 | Reuse offline baselines and retail release backtests; build a reproducible synthetic evaluation entrypoint with aligned eligible targets, fixed splits and per-origin receipts. |
| M1C-02 | P0 | covered_by_existing_code | M1C-01 | Existing seasonal-naive and trailing-mean baselines already share eligible targets; do not add a third candidate without a justified need. Final acceptance remains synthetic until M1C-03 is approved. |
| M1C-03 | P0 | blocked | M1B-03, M1C-02, B-02 | Run approved empirical holdout, record actual MAE/RMSE/zero-safe metrics, coverage, abstention and model card; no invented accuracy. |
| M1D-01 | P1 | partial | M1C-01 | Reuse residual envelope, drift and sensitivity code; formalize uncertainty semantics, disjoint calibration/holdout strategy, missing/late data and coverage tests. |
| M1D-02 | P1 | planned | M1C-03, M1D-01 | Evaluate uncertainty on approved held-out observations, document empirical coverage or explicitly uncalibrated limits and sensitivity. |
| M1E-01 | P0 | partial | None | Versioned gateway and strict allowlisted WorldKernel request mapping exist in draft PR #55; reject unrepresentable state/interventions/refs and bound mapped runs. This is request construction, not execution. |
| M1E-02 | P0 | partial | M1E-01 | Optional exact-pin local worker executes the actual registered inventory demo with local timeout/output and result checks; this establishes SDK compatibility for that demo, not the M1 lead-time model or a hostile-code sandbox. Consolidated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85` passed 832 tests without skips and all five other checks locally with the reviewed WorldKernel pin installed; official Actions remain unavailable under B-08. This does not establish hostile-code isolation or a production lead-time model. |
| M1E-03 | P0 | partial | M1C-01 | The paired fictional three-policy test double and shared day transition are implemented and regression-tested; it defines the reference semantics and does not require an external engine. |
| M1E-04 | P0 | review | M1E-02, M1E-03 | The consolidated PR #62 candidate contains the fixed code-owned WorldKernel policy world using the shared transition, strict versioned mapping, bounded operator fan-out, parent-side state/stream checks, exact synthetic parity and explicit CLI opt-in. HTTP remains on the test double. Exact-pin integration and the full clean integrated gate passed on candidate commit `74330d8`; review production isolation separately under B-04. |
| M1F-01 | P0 | partial | None | Draft PR #54 provides a versioned decision trace/result contract separating facts, forecasts, simulated outcomes, assumptions, missing evidence, costs and human review; fixture and invalid-reference tests. No authenticated producer or execution is included. |
| M1F-02 | P0 | review | M1B-02, M1C-01, M1D-01, M1E-03, M1F-01 | Consolidated PR #62 composes synthetic evidence, fixed-baseline evaluation, residual diagnostics, policy simulation and typed decision trace through reproducible CLI/API paths. The API/default CLI use the test double; the local CLI can opt into the fixed WorldKernel policy world. PR #57's synthetic UCI event-time evaluator and aggregate Census protocol are included. Exact integrated six-check gate passed on `74330d8`; approved-source evidence, empirical forecast validation and real/public transport controls remain incomplete. |
| M1F-02a | P0 | review | M1F-02, M1E-04 | PR #62 resolves the #59 engine-provenance finding: selected engine contract, selected-result source, parity-oracle invocation and exact WorldKernel provenance are independently recorded and validated. Exact replay and adverse reference/digest regressions pass in the integrated gate. B-04 production isolation and B-08 official Actions are outside this synthetic contract. |
| M1F-03 | P0 | blocked | M1B-03, M1C-03, M1D-02, M1F-02 | Complete reviewed retail MVP user story using approved observations and evaluated forecasts, actual simulation and documented conditional assumptions; independent replay and review. B-01/B-02/B-04 block this path. |

Read [M1 delivery plan](M1_EXECUTION_PLAN.md), [retail MVP](../RETAIL_MVP.md),
[forecast walkthrough](M1_STAGED_ROLLING_BASELINES.md),
[retail backtest](RETAIL_RELEASE_BACKTEST.md), [uncertainty guide](RETAIL_RESIDUAL_ENVELOPE.md),
[WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md) and
[decision trace](DECISION_TRACE_TEMPLATE.md). Do not discard existing
coverage/selection diagnostic modules merely because they are local.

## C. M2 — grounded AI and usable workflow

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M2-01 | P1 | review | M1F-01 | PR #60 proposes strict typed query/result contracts and bounded in-memory fictional retrieval, filters caller-declared scope before ranking, binds exact excerpts to digests and labels all retrieved text untrusted. No route, identity or real-source permission. |
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

## Current queue — 2026-11-26

| ID | Status | Current state / next action | Blockers |
| --- | --- | --- | --- |
| M1B-02 / M1C-01 / M1D-01 / M1E-01–04 / M1F-01–02 | integrated, synthetic scope | PR #62 merged the end-to-end experimental M1 workflow at `a456034`; this completes the synthetic integration slice, not the licensed/empirical M1 acceptance. | B-01, B-02, B-04, B-08 |
| M1B-01 / M1C-03 | partial / blocked for real evidence | A+B pilot protocols and adapters are prepared; UCI remains event-time retrospective and Census is vintage-based. Do not acquire/process bytes until the source-specific license, privacy, retention and temporal evidence are approved. | B-01, B-02 |
| M1B-04 / M1C-04 | in_progress | Census descendant `codex/m1-census-vintage-adapter` passed its pre-sync gate at `da540a2`; merge commit `55e91f7` includes `a456034`. Re-run the complete gate on this exact reconciled head, then publish it as a separate PR. | B-01, B-02, B-08 |
| M2-01 | review preparation | PR #60 includes `main` via `a5186a680b307c4ecd9d56321321a5b27048731d`. Exact sync head and docs candidate `26e45b4620e9e13e12a745db3c99ead196c656d0` each passed 845 tests, zero skips and all six checks with pinned WorldKernel; the latter receipt is `results/local-quality-gate-26e45b4620e9e13e12a745db3c99ead196c656d0.json`. This status/evidence refresh needs its exact gate before push, retarget to `main`, and independent review. Keep caller-declared scope and fictional-only limits explicit. | B-08 |
| G-01 | ready for sync | PR #61 remains independent on its prior base. Merge `a456034` preserving typed clock-failure behavior and M1 contracts, then run the exact full gate before retargeting and preparing independent review. | B-08 |
| PR queue #52–#59 | reconciled | Exact published heads are ancestors of `a456034`; #52 is merged and #53–#59 are closed as incorporated. All branches are retained. | None for duplicate integration |
| M2-02+ | planned | Start only after M2-01 review/integration; do not grow the feature queue while #60/#61 and Census remain under consolidation. | M2-01 |
| ENG-02 | separately tracked | A scoped `ruff check examples` found 5 diagnostics in `m1_asof_rolling_backtest.py` (I001, RUF007), `m1_observation_preflight.py` (I001) and `m1_temporal_backtest.py` (I001, F401). They are outside the local gate's `src`/`tests` Ruff scope and are not failures of the integrated gate. Handle after PR consolidation in a distinct maintenance change. | None |

The older row-level branch claims below are preserved as historical evidence;
they are not live task ownership or current PR states.

## Historical active claims before PR #62 merge — 2026-11-25

| ID | Status | Owner / branch | Surfaces | PR / commit | Evidence and next action | Blockers |
| --- | --- | --- | --- | --- | --- | --- |
| DOC-01 | review | Codex / `codex/m1b-02-synthetic-evidence-flow` | Baseline reconciliation, semantic map, source/learning/docs navigation | [PR #52 draft](https://github.com/GustavoMFDS/MirrorMind/pull/52) | PR #51 remains the merged baseline; published PR #52 head `b431d11` has exact local gate evidence and its review response is recorded. | No separate docs blocker; official Actions remains unresolved under B-08 |
| M1B-01 / M1C-03 source decision | owner review pending | Codex / `codex/m1-engine-provenance` for integration; source lane remains separate | Synthetic UCI event-time evaluator, data/privacy card, Census aggregate vintage protocol | [PR #57 draft](https://github.com/GustavoMFDS/MirrorMind/pull/57); consolidated ancestry in [PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62); [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) | Owner approved the A+B research sequence: UCI #352 retrospective by product/event-time first, followed separately by aggregate Census/ALFRED release-vintage evaluation. The synthetic evaluator, fixed protocol and privacy controls are present in integrated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85`; its exact six-check local gate passed 832 tests with no skips and all five non-pytest checks, including the pinned WorldKernel path. No real source bytes, API key or credential were acquired. Adapter/protocol preparation may continue synthetically; real download/processing remains blocked pending source-specific rights, attribution, snapshot, minimization and retention approval. PR #57 Actions stopped before repository steps under B-08. | B-01/B-02/B-08 |
| M1B-02 | in_progress | Codex / `codex/m1b-02-synthetic-evidence-flow` | CSV/XLSX local composition, review packet, calendar/release/as-of checks, tests and docs | [PR #52 draft](https://github.com/GustavoMFDS/MirrorMind/pull/52), exact tested commit `b431d11bf0ac841ff30353a06263d23fb901307c` | Full exact-head local gate passed 696 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 03:51:25 UTC. Review reply is recorded; B-01/B-02 remain open. | B-01/B-02 still block real-source rights and availability; B-08 blocks official check evidence; review/integration decision remains open |
| M1C-01 | in_progress | Codex / `codex/m1c-01-synthetic-retail-evaluation` | Prepared UCI-shaped evidence flow, fixed matched-origin baselines, deterministic fictional CLI, per-origin receipts and model/data docs | [PR #53 draft](https://github.com/GustavoMFDS/MirrorMind/pull/53), published exact tested head `79d3679013576c6a209bed9fa031b7f0fabd0d8d`, stacked on PR #52 | Full gate passed 700 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:08:00 UTC. The API suite ran; one existing deprecation warning remains. Current Actions fail without steps/logs; cause is not established. | Depends on M1B-02 in draft PR #52; B-01/B-02 block real-source claims and B-08 blocks official check evidence |
| M1F-01 | in_progress | Codex / `codex/m1f-01-decision-trace-contract` | Versioned immutable result schema, exact-result review binding, synthetic example, tests and learning docs | [PR #54 draft](https://github.com/GustavoMFDS/MirrorMind/pull/54), review correction `f02459d977fd263b03ddf60264b9069ae08b189b`, stacked on PR #53 | Correction reproduced pre-creation review and Decimal-context collision; 28 focused decision-trace tests pass. Merge commit `e493b4c` synchronizes the local branch with PR #53 head `79d3679`, retaining its nested-receipt regressions. Published integrated head `4d22006` passed all 728 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:25:37 UTC. Contract remains interface-only, with no producer or execution. | B-08 remains unresolved on published heads; source rights, empirical forecasts and actual engine outputs remain separate gates |
| M1E-01 | in_progress | Codex / `codex/m1e-01-worldkernel-mapping` | Strict source-version allowlist, unit/state/parameter validation, mutation-safe scenario revalidation, effective scenario/operator run ceilings and walkthrough | [PR #55 draft](https://github.com/GustavoMFDS/MirrorMind/pull/55), implementation `8769241`, review correction `07c405b`, sync merge `b9eba02` with PR #54 head `4d22006`, published head `56aa92a` | Published exact head `56aa92a` passed all 756 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:39:14 UTC. PR #53's nested-receipt regressions remain in the merged state. Actions failed before job steps under B-08. The mapper only builds a request; no WorldKernel import or execution is claimed. | B-04 blocks actual engine acceptance; B-08 blocks official CI evidence |
| M1E-02 | in_progress | Codex / `codex/m1e-02-worldkernel-local-runtime` | Optional exact-SHA local worker, bounded process protocol, strict result validation and synthetic engine example | [PR #55 draft](https://github.com/GustavoMFDS/MirrorMind/pull/55), local runtime implementation `ac52ec9`, exact gate recorded at `f503fcc` | The pinned `retail.inventory.demo@demo-1` engine and failure paths passed on the M1E-02 branch. Consolidated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85` passed 832 tests and all five non-pytest checks with exact-pin synthetic engine regressions and no skips. The PR #57 branch receipt is separate. This is local compatibility evidence for the registered demo, not a hostile-code sandbox or production lead-time model. | B-04 broad service acceptance and production isolation; B-08 official Actions evidence |
| M1D-01 | in_progress | Codex / `codex/m1d-01-disjoint-residual-calibration` | Fixed pre-holdout calibration/holdout target split, origin-specific release checks, uncertainty semantics, dependent tests and engineering docs | [PR #56 draft](https://github.com/GustavoMFDS/MirrorMind/pull/56), merge with PR #53 `b9bb86d`, published head `e993391` | PR #56 exact head `e993391a61a99d63008bc970cb19af673be4c18c` passed 700 tests plus Ruff, catalog, atlas, evidence and capability checks; it is an ancestor of consolidated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85`, whose six-check local gate passed 832 tests. The result remains experimental and does not establish empirical calibration; no approved real observations were used. Actions did not start repository steps under B-08. | B-08 blocks official CI evidence; B-02 blocks empirical evaluation |
| M1E-04 | review | Codex / `codex/m1-engine-provenance` | MirrorMind-owned fixed policy world, versioned mapper, gateway, exact-pin worker, parity tests and learning documentation | [Consolidated PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62); implementation ancestry includes PR #55 and #58 | Candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85` passed 832 tests with no skips plus all five non-pytest local checks while WorldKernel `9b133ef873f2b6a7206c9c5742d40df4fccdb04a` was installed. Selected WorldKernel output and test-double parity execution are separately represented in DecisionTrace v2. No WorldKernel-repository change was made; HTTP/default CLI remain on the test double. | B-04 broader service acceptance and hostile-code isolation; B-08 official Actions; final candidate review |
| M1E-03 | in_progress | Codex / `codex/m1e-03-synthetic-policy-simulation` | Fictional retail policy comparison, paired demand streams, deterministic inventory transitions, cost summaries and modeling caveats | [PR #58 draft](https://github.com/GustavoMFDS/MirrorMind/pull/58), published head `37737c2`, dependency sync merge `5544bc0` with PR #55 head `56aa92a` | Exact published head `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8` passed 768 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 05:18:58 UTC. Arrival-day exclusion remains a documented toy rule. The shared day transition is reused by M1E-04; the test double remains the parity reference. | B-08 blocks official CI evidence; source/model gates remain separate |
| M1F-02 | review | Codex / `codex/m1-engine-provenance` | Compose synthetic evidence, fixed-baseline evaluation, residual diagnostics, policy outcomes and versioned decision trace into one bounded flow | [Consolidated PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62), provenance correction commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85`, preserving exact #52–#59 ancestry | The integrated workflow, #57 evaluator, aggregate Census protocol, pinned local engine and M1F-02a provenance correction are present. Exact local six-check gate passed 832 tests, zero skips and five non-pytest checks with the reviewed WorldKernel pin. `DecisionTrace` v1 remains; workflow v2 binds selected output source separately from parity execution. HTTP remains unauthenticated and does not invoke WorldKernel. No real-source evidence or empirical forecast claim is made. | B-01/B-02 block real-source claims; B-04 broader service isolation; B-08 official Actions; final candidate review |
| M1F-02a | review | Codex / `codex/m1-engine-provenance` | Bind actual selected engine, parity-oracle execution and exact engine provenance to conditional outcomes | [Consolidated PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62), commits `74330d811145f10fcaaddadc56c3f95e7c8b7a85` and `20e7b50f88df046eaf3541c5ea706b2e3b051aad`; resolves PR #59 comment `7174402947` and follow-up chronology finding | Regression tests cover test-double and exact-pin WorldKernel provenance/replay, mismatched/dangling references, parity digest mismatch and v2 execution chronology. Exact code-head gate passed 835 tests, zero skips and all five non-pytest checks with reviewed WorldKernel installed. Final docs-inclusive receipt is required before publishing/review reply. | Final independent review of PR #62; B-04 production isolation and B-08 official Actions remain separate |
| M2-01 | in_progress | Codex / codex/m2-01-permission-filtered-retrieval | Bounded lexical retrieval with caller-declared scope, deterministic excerpt spans and integrity-checked results | [PR #60 draft](https://github.com/GustavoMFDS/MirrorMind/pull/60), correction `73c1910`, published head `59deef2a780d7802d8b8d29b66dd0189e96365ea` | Regression tests reject same-length excerpt tampering and a different valid-looking digest. Exact PR #60 head `6fe64dd572991e905aae60358890c4255081abac` passed 738 tests plus Ruff, catalog, atlas, evidence and capability checks. GitHub metadata inspected 2026-11-25 reports the reviewed base #54 head `4d220066c3e9ab83a321ac9517bbabc8fc22e293` and `mergeable=true`. It remains a separate M2 draft outside the M1 candidate. Scope is caller-declared, not authenticated RBAC; source authenticity and absolute offsets remain unproven. | B-08 official CI; separate M2 review/integration decision |
| G-01 | in_progress | Codex / codex/g01-current-head-service | Read-only in-process current-head responder with typed clock/store failure boundaries | [PR #61 draft](https://github.com/GustavoMFDS/MirrorMind/pull/61), correction `1847e81`, published head `8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e` | Clock regression distinguishes typed operational failures (generic bodyless 503) from unexpected programming errors. Exact head passed 697 tests plus Ruff, catalog, atlas, evidence and capability checks. Review response is recorded; Actions failed before steps. No route, persistence, authentication or deployed authority. | B-08 blocks official CI; service/transport deployment remains outside the reviewed slice |
