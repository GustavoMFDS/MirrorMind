# Task backlog — prioritized execution register

**Baseline:** main commit `a456034c55ed7634ad4768b26788fec09dab1d08` after PR #62,
see [PROJECT_STATUS](PROJECT_STATUS.md). PR #51 rows below are retained as
historical reconciliation. This is
the maintained task register, not a duplicate roadmap or a promise
of completion. Read [MASTER_EXECUTION_PLAN](MASTER_EXECUTION_PLAN.md),
[DEFINITION_OF_DONE](DEFINITION_OF_DONE.md) and [BLOCKERS](BLOCKERS.md).
On resuming work, reconcile with actual branches, open PRs, merged
commits and independently observed evidence. Do not duplicate work
already underway.

## Current PR reconciliation — 2026-11-27 UTC

PR #52 merged at `e922b03666f04bd8c570a0448466d25838e3f84e`; PRs #53–#59
closed without individual merges. Local ancestry checks confirm all eight
published heads, including the #52 merge commit, are ancestors of PR #62's
integrated head `0bed1269613eb689e84ad971c7d8f1878767d6cf`. Main contains
that candidate at `a456034c55ed7634ad4768b26788fec09dab1d08`. These branches
are historical evidence, not open work; no duplicate merge is required.
Implementation rows below record whether each bounded slice is integrated,
while source, empirical, production and official-CI gates remain distinct.

## Historical reconciliation at the PR #51 baseline

| State | Items / evidence | Continuation |
| --- | --- | --- |
| Merged foundations, still experimental | PRs #47–#50 added local/offline signed-fence verification and a nonce-challenged HTTPS reader; PR #51 consolidated the engineering handoff. These do not deliver a deployed trust service or source authorization. | Preserve their existing scope and tests; do not rebuild the governance chain as a substitute for the product path. |
| Partially implemented M1 | M1B-02 now composes separate CSV/XLSX readers, intake metadata and declared temporal checks. M1C-01 already had offline baselines and release backtests; the current stacked branch adds the reproducible evidence-to-evaluation entrypoint. | Keep the two changes reviewable as separate PRs; preserve abstention and per-origin receipts. |
| Ready at the PR #51 baseline | DOC-01 reconciliation; G-01 minimal testable server-side current-head response; M1E-01 simulation contract work; M1F-01 decision trace contract. DOC-01 is now in review below. | Keep M1 evidence-to-evaluation work ahead of further experimental governance unless a dependency requires G-01. |
| Pending by dependency | Remaining M1C/M1D/M1E/M1F, M2, M3 and M4 rows marked `planned`. | Start only when named predecessors and acceptance inputs exist. |
| Blocked by external evidence or approval | M1B-03 and M1C-03 require B-01/B-02 real-source rights, original availability and empirical holdout evidence. G-04 and deployment-related scopes also require B-03/B-06. | Advance synthetic slices independently; preserve blockers and do not claim they are solved by generated fixtures. |

## UCI pilot reconciliation — snapshot 2026-11-27 UTC

PR #62 is integrated in `main` at `a456034c55ed7634ad4768b26788fec09dab1d08`.
The current worktree is the separate `codex/uci352-pilot-20261126` branch; an
earlier local integration branch remains preserved. The owner-approved UCI
snapshot passed metadata/schema preflight. Its former `openpyxl.values_only`
reader transiently materialized Description values, so it was replaced with
selective OOXML streaming that disables Python text callbacks for excluded
body cells. MM-020 authorized the 250,000 UCI-only group ceiling; MM-021
authorized aggregate-only exclusion of non-`C` single-letter invoice prefixes.
The corrected real-source call exceeded 250,000 groups and returned no
projection or evaluation. The pilot is stopped at that bound; do not chunk,
retry or widen it without a new decision. Generic defaults/caps remain
unchanged. See the path-free [snapshot manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json)
and [B-01](BLOCKERS.md).

The implementation is published as [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65).
The last published and gated head before this status refresh is
`9899cffaaf05e5bb9ffcf6fcac02edaa6bd8efa9`, based on the merged main baseline
above. PR #65 is open, non-draft and mergeable; independent review is pending.
Its exact-head temporary local gate passed 863 tests with zero skips and all
six checks; the focused UCI reader/projection/evaluator/workbook-flow rerun
passed 112 tests. Receipt:
`results/local-quality-gate-9899cffaaf05e5bb9ffcf6fcac02edaa6bd8efa9.json`.
GitHub Actions did not start repository steps on this head; see B-08. These
receipts do not clear the 250,000-group source stop or establish real metrics.

## Historical consolidated review candidate — 2026-11-25 (PR #62 later integrated)

`codex/m1-engine-provenance`, published as
[PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62) to `main`, contains
provenance correction commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85` and
chronology correction `20e7b50f88df046eaf3541c5ea706b2e3b051aad`. It preserves
the exact published ancestry of #52–#59 and excludes #60/#61. The chronology
code head passed 835 tests without skips, plus Ruff, catalog, atlas, evidence
and capability checks, with reviewed WorldKernel pin installed. Receipt:
`results/local-quality-gate-20e7b50f88df046eaf3541c5ea706b2e3b051aad.json`.
The exact documentation-inclusive head must be gated again and its receipt
reported on PR #62; see [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md) for gate
semantics. PR #59 provenance comment `7174402947` and the newer #62 chronology
finding are addressed in code. This was an unmerged candidate snapshot; PR #62
was later merged to `main`. PR #60 and #61 remain separate from that ancestry
and are now open, non-draft candidates based on the merged `main`.

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
| M1B-01 | P0 | partial | None | Synthetic UCI #352 event-time evaluator and fixed split are implemented; separate aggregate Census/ALFRED protocol is prepared. Owner decisions MM-020/MM-021 authorize a UCI-only 250,000-group call and conservative invoice-prefix classification. The corrected call exceeded that cap and failed closed with no projection or metrics. Keep the lane stopped under current scope; no chunking or larger cap. Source remains private until deletion deadline. |
| M1B-02 | P0 | partial | None | Compose bounded CSV/workbook staging, review metadata, calendar/release checks and as-of selection into a reusable synthetic evidence flow; deterministic fixture, rejection and abstention tests. |
| M1B-03 | P0 | blocked | M1B-01, M1B-02, B-01, B-02 | UCI #352 adapter, path-free manifest and metadata preflight are present. The reader excludes non-`C` single-letter invoice prefixes under MM-021 and the bounded call exceeds 250,000 groups. No complete projection/evaluation exists. Do not rerun or partition the source without a new scope decision. Keep Census/ALFRED acquisition separate and pending its own exact source/vintage review. |
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

## Historical PR-branch evidence — snapshot 2026-11-25

PR #62 was subsequently integrated into `main` at `a456034c55ed7634ad4768b26788fec09dab1d08`.
The PR-specific rows below preserve branch-level receipts and ancestry only;
their snapshot statuses do not represent current PR states or open work.
PR #52 is merged; PRs #53–#59 are closed unmerged with their published heads
integrated through #62. PRs #60 and #61 remain separate from the #62 ancestry.
Current UCI pilot state is recorded above and in B-01.

## Historical branch claims

| ID | Status | Owner / branch | Surfaces | PR / commit | Evidence and next action | Blockers |
| --- | --- | --- | --- | --- | --- | --- |
| DOC-01 | integrated | Codex / `codex/m1b-02-synthetic-evidence-flow` | Baseline reconciliation, semantic map, source/learning/docs navigation | [PR #52 merged](https://github.com/GustavoMFDS/MirrorMind/pull/52); ancestry retained in #62 | PR #52 merge `e922b03` and head `b431d11` are ancestors of the integrated #62 head. Exact branch-level local gate and review reply remain historical evidence. | Official Actions remains unresolved under B-08 |
| M1B-01 / M1C-03 source decision | UCI bounded attempt stopped; empirical evaluation blocked | Codex / `codex/uci352-pilot-20261126`; integrated #52–#59 ancestry in `main` | Synthetic UCI evaluator, approved UCI #352 source preflight, separate Census aggregate-vintage protocol | PR #62 integrated into main at `a456034c`; [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65) last gated head `9899cffa`; [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md); [path-free source manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json) | Metadata preflight and MM-021 synthetic invoice-classification regressions pass. The corrected real-source call exceeded MM-020's 250,000-group cap and returned no projection, complete exclusion count, metrics or model card. No Census data or credential was acquired. PR #65 exact head passed 863 tests, zero skips and all six local checks with exact WorldKernel pin installed; 112 focused UCI tests also passed. Receipt is in `LOCAL_QUALITY_GATE.md`. Independent review is pending; Actions did not start repository steps. | B-01 requires a separately approved bounded method before any new UCI processing; B-02 temporal evidence and Census source/vintage review; B-08 official Actions |
| M1B-02 | integrated (synthetic slice) | Codex / `codex/m1b-02-synthetic-evidence-flow` | CSV/XLSX local composition, review packet, calendar/release/as-of checks, tests and docs | [PR #52 merged](https://github.com/GustavoMFDS/MirrorMind/pull/52); exact tested head `b431d11bf0ac841ff30353a06263d23fb901307c`, also ancestor of #62 | Full exact-head local gate passed 696 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 03:51:25 UTC. Review reply is recorded; #52 merge is present in main via the #62 ancestry. | Real-source rights/availability remain B-01/B-02; official Actions remains B-08 |
| M1C-01 | integrated (synthetic slice) | Codex / `codex/m1c-01-synthetic-retail-evaluation` | Prepared UCI-shaped evidence flow, fixed matched-origin baselines, deterministic fictional CLI, per-origin receipts and model/data docs | [PR #53 closed; head integrated via #62](https://github.com/GustavoMFDS/MirrorMind/pull/53), head `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | Full gate passed 700 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:08:00 UTC. The API suite ran; one existing deprecation warning remains. Current Actions failed before repository steps; exact diagnostic is in B-08. | B-01/B-02 block real-source claims; B-08 blocks official CI evidence |
| M1F-01 | integrated (contract only) | Codex / `codex/m1f-01-decision-trace-contract` | Versioned immutable result schema, exact-result review binding, synthetic example, tests and learning docs | [PR #54 closed; head integrated via #62](https://github.com/GustavoMFDS/MirrorMind/pull/54), correction `f02459d977fd263b03ddf60264b9069ae08b189b` | Correction reproduced pre-creation review and Decimal-context collision; 28 focused decision-trace tests pass. Published head `4d22006` passed 728 tests plus Ruff, catalog, atlas, evidence and capability checks. Contract remains interface-only, with no producer or execution. | B-08 official Actions; source rights, empirical forecasts and actual engine outputs remain separate gates |
| M1E-01 | integrated (mapper) | Codex / `codex/m1e-01-worldkernel-mapping` | Strict source-version allowlist, unit/state/parameter validation, mutation-safe scenario revalidation, effective scenario/operator run ceilings and walkthrough | [PR #55 closed; head integrated via #62](https://github.com/GustavoMFDS/MirrorMind/pull/55), implementation `8769241`, published head `56aa92a` | Published exact head passed 756 tests plus Ruff, catalog, atlas, evidence and capability checks. The mapper only builds a request; no WorldKernel import or execution is claimed by this slice. | B-04 blocks broader engine acceptance; B-08 official CI evidence |
| M1E-02 | integrated (local runtime) | Codex / `codex/m1e-02-worldkernel-local-runtime` | Optional exact-SHA local worker, bounded process protocol, strict result validation and synthetic engine example | [PR #55 closed; head integrated via #62](https://github.com/GustavoMFDS/MirrorMind/pull/55), implementation `ac52ec9`, tested ancestry `f503fcc` | Published integration's exact gate passed 832 tests and all five non-pytest checks with exact-pin synthetic engine regressions and no skips. Compatibility is demonstrated for the registered demo, not a hostile-code sandbox or production lead-time model. | B-04 broad service acceptance/production isolation; B-08 official Actions |
| M1D-01 | integrated (experimental) | Codex / `codex/m1d-01-disjoint-residual-calibration` | Fixed pre-holdout calibration/holdout target split, origin-specific release checks, uncertainty semantics, dependent tests and engineering docs | [PR #56 closed; head integrated via #62](https://github.com/GustavoMFDS/MirrorMind/pull/56), merge with PR #53 `b9bb86d`, published head `e993391` | Its exact head passed 700 tests and is an ancestor of #62. Integrated gate passed 832 tests with no skips. No approved real observations were used; empirical calibration is not established. | B-02 blocks empirical evaluation; B-08 official CI evidence |
| M1E-04 | integrated (local compatibility) | Codex / `codex/m1-engine-provenance` | MirrorMind-owned fixed policy world, versioned mapper, gateway, exact-pin worker, parity tests and learning documentation | [PR #62 merged](https://github.com/GustavoMFDS/MirrorMind/pull/62); implementation ancestry includes #55 and #58 | Candidate passed 832 tests with no skips and all five non-pytest checks with reviewed WorldKernel pin installed. DecisionTrace v2 separates selected WorldKernel output from parity execution. No WorldKernel-repository change was made; HTTP/default CLI remain on the test double. | B-04 broader service acceptance/hostile-code isolation; B-08 official Actions |
| M1E-03 | integrated (experimental) | Codex / `codex/m1e-03-synthetic-policy-simulation` | Fictional retail policy comparison, paired demand streams, deterministic inventory transitions, cost summaries and modeling caveats | [PR #58 closed; head integrated via #62](https://github.com/GustavoMFDS/MirrorMind/pull/58), head `37737c2` | Exact published head passed 768 tests plus Ruff, catalog, atlas, evidence and capability checks. Arrival-day exclusion remains a documented toy rule; no empirical policy evidence is claimed. | B-08 blocks official CI; source/model gates remain separate |
| M1F-02 | integrated (synthetic workflow) | Codex / `codex/m1-engine-provenance` | Compose synthetic evidence, fixed-baseline evaluation, residual diagnostics, policy outcomes and versioned decision trace into one bounded flow | [PR #62 merged](https://github.com/GustavoMFDS/MirrorMind/pull/62), preserving #52–#59 ancestry | The integrated workflow, #57 evaluator, aggregate Census protocol, pinned local engine and provenance correction are present. Exact local six-check gate passed 832 tests, zero skips. `DecisionTrace` v1 remains; workflow v2 binds selected output source separately from parity execution. No empirical claim is made. | B-01/B-02 real-source gates; B-04 service isolation; B-08 official Actions |
| M1F-02a | integrated | Codex / `codex/m1-engine-provenance` | Bind actual selected engine, parity-oracle execution and exact engine provenance to conditional outcomes | [PR #62 merged](https://github.com/GustavoMFDS/MirrorMind/pull/62), changes resolve PR #59 comment `7174402947` and follow-up chronology finding | Regression tests cover test-double and exact-pin WorldKernel provenance/replay, mismatched/dangling references, parity digest mismatch and v2 chronology. Historical code-head gate passed 835 tests, zero skips and all five non-pytest checks with reviewed WorldKernel installed. Integrated PR #62 review is recorded; B-04 production isolation and B-08 Actions remain separate. | B-04 production isolation; B-08 official Actions |
| M2-01 | review | Codex / `codex/m2-01-permission-filtered-retrieval` | Bounded lexical retrieval, caller-declared scope and integrity-checked citation envelopes | [PR #60](https://github.com/GustavoMFDS/MirrorMind/pull/60), open/non-draft/mergeable, head `fafdedae3a76398e0450773065e40384c96d1ed7`, based on main `a456034c` | Exact gate passed 845 tests, zero skips and all six checks; receipt `results/local-quality-gate-fafdedae3a76398e0450773065e40384c96d1ed7.json`. Review response covers same-length tampering and wrong well-formed digest. Actions failed before steps with the alternatives-only account annotation. Await independent review. Scope is caller-declared, not authenticated RBAC; source authenticity and absolute offsets remain unproven. | B-08 official Actions; separate M2 review/integration decision |
| G-01 | review | Codex / `codex/g01-current-head-service` | Read-only in-process current-head responder with typed clock/store failure boundaries | [PR #61](https://github.com/GustavoMFDS/MirrorMind/pull/61), open/non-draft/mergeable, head `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29`, based on main `a456034c` | Exact gate passed 841 tests, zero skips and all six checks; receipt `results/local-quality-gate-f30556ecb9219c1bc4eb0eb720f9c59c3a729b29.json`. Review response covers typed clock failure without swallowing programming errors. Actions failed before steps with the alternatives-only account annotation. Await independent review. No route, persistence, authentication or deployed authority. | B-08 official Actions; service/transport deployment remains outside the reviewed slice |
