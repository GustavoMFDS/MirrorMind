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

## PR reconciliation snapshot at `91fc585` — 2026-11-27 UTC

PR #52 merged at `e922b03666f04bd8c570a0448466d25838e3f84e`; PRs #53–#59
closed without individual merges. Local ancestry checks confirm all eight
published heads, including the #52 merge commit, are ancestors of PR #62's
integrated head `0bed1269613eb689e84ad971c7d8f1878767d6cf`. Main contains
that candidate at `a456034c55ed7634ad4768b26788fec09dab1d08`. These branches
are historical evidence, not open work; no duplicate merge is required.
Implementation rows below record whether each bounded slice is integrated,
while source, empirical, production and official-CI gates remain distinct.

PRs #60, #61, #63 and #64 were rechecked on 2026-11-27 UTC before this
documentation-only reconciliation. PR #65 received the docs-only follow-up
below after its exact-head gate. All five remain open, non-draft and
mergeable against the main commit above; no merge or independent approval is
implied.

| PR | Scope | Verified head | Review state |
| --- | --- | --- | --- |
| [#60](https://github.com/GustavoMFDS/MirrorMind/pull/60) | M2-01 scoped lexical retrieval | `fafdedae3a76398e0450773065e40384c96d1ed7` | Earlier owner-authored finding was corrected; independent review pending |
| [#61](https://github.com/GustavoMFDS/MirrorMind/pull/61) | G-01 current-head responder | `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29` | Earlier owner-authored finding was corrected; independent review pending |
| [#63](https://github.com/GustavoMFDS/MirrorMind/pull/63) | Synthetic Census vintage evaluator and source protocol | `ffd3d770d5c7e9bafba975544de7947bcf20f1fc` | No review submission or inline thread observed |
| [#64](https://github.com/GustavoMFDS/MirrorMind/pull/64) | Existing M1 example lint maintenance | `ca97ab61d15347aa271ee9ac8468a0714bdc3402` | No review submission or inline thread observed |
| [#65](https://github.com/GustavoMFDS/MirrorMind/pull/65) | Bounded UCI #352 workbook pilot | `91fc58553049706c18250ff5f72073fc83658ea6` | Open for independent review; no review submission or inline thread observed |

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
governed the invoice-prefix rule used in the real-source attempt. MM-022
clarifies the current UCI-only rule: exact uppercase `C` marks cancellation;
lowercase `c` and other single ASCII-letter plus six-digit identifiers are
excluded as unverified, with aggregate counts only. The stopped source call
used MM-021, exceeded 250,000 groups and returned no projection or evaluation.
Because MM-021 already excluded lowercase-`c` rows before grouping, MM-022
changes only aggregate classification counts and cannot reduce the group count.
MM-022 has synthetic regression evidence only. The pilot remains stopped at
that bound; do not chunk, retry or widen it without a new decision. Generic
defaults/caps remain unchanged. See the path-free [snapshot
manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json) and [B-01](BLOCKERS.md).

The implementation is published as [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65).
Code-bearing commit `94c60b6ee20adbb5023e11aeded9b8fff90b1176` passed its
focused 113-test UCI suite and the exact six-check local gate (864 tests, zero
skips). The prior documentation-inclusive PR head
`b1bd7951ecc80988146eb46362eea99940ef7542` also passed the exact six-check gate (864 tests, zero skips) at
`2026-11-27T03:17:39.573158Z`, with WorldKernel installed at the reviewed pin.
Its receipt is `results/local-quality-gate-b1bd7951ecc80988146eb46362eea99940ef7542.json`;
both runs are local evidence, not official CI. Current Actions diagnostics on
`b1bd795` had four failed pre-start checks with no job steps, logs or combined
statuses; the exact annotation gave payment-failure **or** spending-limit
alternatives and does not identify the subcause (B-08). PR #65 remains open
without independent review. Neither gate clears the 250,000-group stop or
establishes real metrics.

Published documentation-only follow-up
`c2410bdbafbb7a522730d31a304faa8a72b1b097` passed its exact six-check gate at
`2026-11-27T04:25:32.503435Z` with 864 tests, zero skips and the reviewed
WorldKernel pin; see [PROJECT_STATUS](PROJECT_STATUS.md) for the passing
receipt and [B-08](BLOCKERS.md) for the separate sandbox-timeout diagnosis. Four
At that exact head, four automatic Actions runs failed before steps; annotations
again
show the same unresolved payment-or-spending-limit alternatives. See [B-08](BLOCKERS.md)
for exact run/check IDs. The quota report is separate evidence; there is no
official CI pass or newly resolved empirical result.

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

| ID | Priority | Current status (2026-11-27) | Dependencies | Deliverable and acceptance |
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
| M1B-01 | P0 | partial | None | Synthetic UCI #352 event-time evaluator and fixed split are implemented; separate aggregate Census/ALFRED protocol is prepared. MM-020 approves the UCI-only 250,000-group ceiling; MM-021 governed invoice classification during the stopped source attempt; MM-022 makes exact uppercase `C` the sole cancellation prefix and classifies lowercase `c` and other single-ASCII-letter-plus-six-digit forms as unverified. Since both MM-021 classes were excluded before grouping, MM-022 changes aggregate classification counts only and cannot reduce product-day groups. The real-source call applied MM-021, exceeded the cap and failed closed with no projection or metrics; MM-022 has synthetic regression coverage only. Keep the lane stopped under current scope; no chunking or larger cap. Source remains private until deletion deadline. |
| M1B-02 | P0 | integrated (synthetic slice; M1b remains partial) | None | PR #52/#62 integrate bounded CSV/workbook staging, review-only metadata, calendar/release checks and as-of selection into a deterministic synthetic evidence flow. This completes the fictional slice only; no approved real-source ingestion or publisher availability proof is included. |
| M1B-03 | P0 | blocked | M1B-01, M1B-02, B-01, B-02 | PR #65 contains the UCI #352 adapter, path-free manifest and metadata preflight. Current MM-022 rule excludes lowercase `c` and other single-ASCII-letter-plus-six-digit prefixes as unverified; only exact uppercase `C` marks cancellation. Since lowercase `c` was also excluded under MM-021, the clarification does not change accepted sales rows or the 250,000-group overflow. No complete projection/evaluation exists; MM-022 was not applied to real data. Do not rerun or partition the source without a new scope decision. Keep Census/ALFRED acquisition separate and pending its own exact source/vintage review. |
| M1C-01 | P0 | integrated (synthetic slice) | M1B-02 | PR #53/#62 integrate the offline baselines and retail release backtests into a reproducible synthetic evaluation entrypoint with aligned eligible targets, fixed splits and per-origin receipts. No empirical forecast claim is included. |
| M1C-02 | P0 | covered_by_existing_code | M1C-01 | Existing seasonal-naive and trailing-mean baselines already share eligible targets; do not add a third candidate without a justified need. Final acceptance remains synthetic until M1C-03 is approved. |
| M1C-03 | P0 | blocked | M1B-03, M1C-02, B-02 | Run approved empirical holdout, record actual MAE/RMSE/zero-safe metrics, coverage, abstention and model card; no invented accuracy. |
| M1D-01 | P1 | integrated (experimental) | M1C-01 | PR #56/#62 integrate the residual envelope, drift/sensitivity groundwork and disjoint calibration/holdout semantics with missing/late-data regressions. It remains explicitly uncalibrated without approved empirical observations. |
| M1D-02 | P1 | blocked | M1C-03, M1D-01, B-02 | Evaluate uncertainty on approved held-out observations and document empirical coverage or explicitly uncalibrated limits. The required empirical holdout is unavailable until B-02 is resolved. |
| M1E-01 | P0 | integrated (mapper) | None | PR #55/#62 integrate the versioned gateway and strict allowlisted WorldKernel request mapping: reject unrepresentable state/interventions/refs and bound mapped runs. Mapping constructs a request; it does not execute the engine. |
| M1E-02 | P0 | integrated (local runtime) | M1E-01 | PR #55/#62 integrate the optional exact-pin local worker, timeout/output bounds and strict result checks. SDK compatibility is demonstrated for the registered synthetic inventory demo, not hostile-code isolation or a production lead-time model. Broader service acceptance remains under B-04; official Actions remains B-08. |
| M1E-03 | P0 | integrated (experimental) | M1C-01 | PR #58/#62 integrate the paired fictional three-policy test double and shared day transition; they define synthetic reference semantics and do not establish an empirical policy ranking. |
| M1E-04 | P0 | integrated (local compatibility) | M1E-02, M1E-03 | PR #62 integrates the fixed code-owned WorldKernel policy world, shared transition, strict versioned mapping, bounded operator fan-out, parent-side state/stream checks, synthetic parity and explicit CLI opt-in. HTTP remains on the test double. B-04 continues to track broader service isolation and deployment acceptance. |
| M1F-01 | P0 | integrated (contract only) | None | PR #54/#62 integrate the versioned decision trace/result contract separating facts, forecasts, simulated outcomes, assumptions, missing evidence, costs and human review. The contract itself does not authenticate a producer or authorize execution. |
| M1F-02 | P0 | integrated (synthetic workflow) | M1B-02, M1C-01, M1D-01, M1E-03, M1F-01 | PR #62 integrates the bounded synthetic evidence, fixed-baseline evaluation, residual diagnostics, policy simulation and typed trace through reproducible CLI/API paths. The API/default CLI use the test double; the local CLI can opt into the fixed WorldKernel policy world. Approved-source evidence, empirical forecast validation and production transport controls remain incomplete. |
| M1F-02a | P0 | integrated | M1F-02, M1E-04 | PR #62 resolves the #59 engine-provenance finding: selected engine contract, selected-result source, parity-oracle invocation and exact WorldKernel provenance are independently recorded and validated. Exact replay and adverse reference/digest regressions pass in the integrated gate. B-04 production isolation and B-08 official Actions are outside this synthetic contract. |
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
| M1B-01 / M1C-03 source decision | UCI bounded attempt stopped; empirical evaluation blocked | Codex / `codex/uci352-pilot-20261126`; integrated #52–#59 ancestry in `main` | Synthetic UCI evaluator, approved UCI #352 source preflight, separate Census aggregate-vintage protocol | PR #62 integrated into main at `a456034c`; [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65), code commit `94c60b6ee20adbb5023e11aeded9b8fff90b1176`, prior documentation-inclusive head `b1bd7951ecc80988146eb46362eea99940ef7542`; [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md); [path-free source manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json) | MM-022's uppercase-`C`-only cancellation rule is synthetically tested; lowercase `c` and other single-ASCII-letter-plus-six-digit prefixes are aggregate-only exclusions in the UCI adapter, while generic projection still rejects them. The real-source call used MM-021, exceeded MM-020's 250,000-group cap and returned no projection, complete exclusion count, metrics or model card. No Census data or credential was acquired. Prior head `b1bd795` passed 864 tests, zero skips and all six local checks with the exact WorldKernel pin installed; 113 focused UCI tests passed on code commit `94c60b6`. PR #65 has no independent review yet. Four automatic Actions check-runs on `b1bd795` failed before repository steps; the exact annotation lists payment/spending-limit alternatives without identifying the subcause. See B-08. | B-01: no new UCI processing without a distinct bounded-method decision; B-02 temporal evidence and Census source/vintage review; B-08 official Actions |
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
