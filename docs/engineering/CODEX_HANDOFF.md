# Agent handoff — continuous engineering and documentation standard

## 1. Mission and safe starting point

Continue MirrorMind as a modular, domain-neutral evidence-driven
decision intelligence platform, not just a growing collection of
experimental primitives. Deliver a reproducible functional retail MVP,
then applied AI, operational hardening and domain generalization.

Canonical Windows checkout: `D:\MirrorMind`. GitHub:
`https://github.com/GustavoMFDS/MirrorMind`. Use the existing checkout
when appropriate, not an obsolete temporary copy. Another agent may
be working simultaneously. Read [AGENTS.md](../../AGENTS.md) before
any edits; the owner controls approvals. This document supplies
execution guidance and does not broaden the agent's permissions.

## 1.1 Historical owner decisions — 2026-11-25

- Research preparation proceeds A then B: UCI Online Retail #352 event-time
  retrospective first, then an aggregate Census release-vintage study.
  ALFRED is conditional on free authorized access, acceptable series terms and
  adequate archive evidence. This is not approval to acquire or process real
  data. Keep raw data out of Git, CI, logs, prompts and external services;
  automated tests remain synthetic.
- Before processing the original UCI workbook, verify original terms,
  attribution/change notice, minimal product/day/positive-quantity projection
  after cancellation classification, private local storage,
  retention/deletion and the exact source manifest. Do not derive availability
  from `InvoiceDate`; preserve the event-time retrospective label.
- GitHub Actions allowance is exhausted. No paid usage, paid runner or
  spending-limit increase is approved. The no-cost self-hosted option is
  evaluated in [B-08](BLOCKERS.md); no isolated ephemeral host is selected,
  and existing job annotations do not prove that runner substitution would
  bypass the pre-start account gate. Do not register a runner or change a
  workflow. Use [the temporary local gate](LOCAL_QUALITY_GATE.md) on exact
  clean heads, keep local and official evidence separate, and gate the exact
  reconciled candidate. Do not retry identical pre-job failures.
- Continue M1E-02 using the existing M1E-01 WorldKernel request mapper. Inspect
  the separate WorldKernel repository read-only, pin a reviewed revision,
  validate the actual local `worldkernel.result.v1` exchange, and keep the
  optional dependency and project boundary intact. No changes to WorldKernel
  or production deployment are authorized.

The self-hosted option was checked against current official GitHub
documentation: runner usage itself is free, but that does not prove it bypasses
the observed pre-start account gate or eliminate the cost of its host. GitHub
recommends ephemeral runners for autoscaling and warns that workflow code can
compromise a self-hosted machine. No dedicated, clean, zero-cost ephemeral host
is approved; do not use the shared workstation, register a runner or change
workflow labels. See [billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage),
[self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
and [secure use](https://docs.github.com/en/actions/reference/security/secure-use).

The latest owner-recovered PR #57 comment records that the test and
symbol-catalog job records on published head 678755e had no steps and
runner_id=0; the exact annotations remain unavailable, so do not infer their
individual start cause. The exact-head local gate on that PR head passed 712
tests and all six checks, which is not official CI. See
[comment 7167002881](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7167002881).

The separate, unsubmitted M1E-02 branch has a pinned synthetic engine run and
a passing exact-head local gate. Its restricted-sandbox timeout was traced to
local asyncio socket-pair creation; the same test and full gate passed outside
that restriction. This does not retroactively explain the historical 8f906b8
timeout. Preserve both the scope and limits in the blocker register.

Read in order:

1. [Master plan](MASTER_EXECUTION_PLAN.md) — desired architecture,
   dependency order and functional priorities.
2. [Project status](PROJECT_STATUS.md) — commit-pinned baseline;
   reconcile with actual main/PRs before use.
3. [Task backlog](TASK_BACKLOG.md) — stable IDs, dependencies and
   bounded deliverables.
4. [Definition of done](DEFINITION_OF_DONE.md) and
   [blockers](BLOCKERS.md) — acceptance evidence and owner gates.
5. [Architecture](../ARCHITECTURE.md), [accepted decisions](../DECISIONS.md),
   [contracts](../CONTRACTS.md), [security](../SECURITY.md),
   [roadmap](../ROADMAP.md), [M1 plan](M1_EXECUTION_PLAN.md).
6. [Engineering hub](README.md), [system map](SYSTEM_MAP.md),
   [semantic map](SEMANTIC_COVERAGE.md), [atlas](REPOSITORY_ATLAS.md),
   [symbols](generated/SYMBOLS.md) and related source guides.
7. [Capability ledger](CAPABILITY_LEDGER.json),
   [capability gates](CAPABILITY_GATES.md), [evidence map](EVIDENCE_MAP.json),
   tests, actual source, CI workflows and recent history.

Use the actual implementation and tests to resolve stale prose. An
accepted architecture is design intent, an interface is not an
implementation, and a local synthetic regression is not a production
or empirical validation. Correct stale summaries in a reviewed change;
do not silently weaken accepted requirements.

## 2. Concurrent work and git safety

Before changing files, inspect `git status --short --branch`,
`git worktree list`, current HEAD, remote main and open PRs. Check
whether the task or files are already being changed by another agent.
Prefer separate task branches and worktrees. Do not switch, reset,
stash, clean, overwrite or force-push another agent's working tree,
uncommitted changes or shared branches. Never delete worktrees that
may contain another person's work. Avoid a second concurrent
environment install in the canonical checkout.

Each worktree needs its own properly bound Python environment;
verify the interpreter and imported source path. An editable install
from another worktree can make passing tests misleading. Keep
generated caches, credentials, datasets and local receipts out of
commits unless explicitly reviewed. Use explicit Git staging paths.
Fetch and reconcile current main before PR creation or merge; do not
auto-resolve substantive contract or security conflicts by dropping
changes. Follow actual branch protections and required human review.

If a handoff document is modified by another agent, reconcile its
task IDs, evidence and status before updating it. Claim the task
in the backlog or PR before large overlapping changes. When a blocker
affects one lane, continue independent tasks instead of repeatedly
asking permission for routine reversible decisions.

## 3. Execution cycle and autonomy

- Pick the highest-priority ready bounded task that advances an
  acceptance gate; reuse existing implementation before adding more
  abstraction. Identify dependencies, impacted source and consumers.
- Fill in [change request template](CHANGE_REQUEST_TEMPLATE.md)
  for meaningful behavior/contract/state/architecture changes.
  Include task ID, constraints, non-goals, acceptance, code impact,
  test plan and recovery/compatibility.
- Implement incrementally. Add real normal/adverse regression tests,
  then update the required learning/documentation surfaces.
- Run the applicable [quality checks](DEFINITION_OF_DONE.md);
  report actual SHA and outcome. Open a reviewable PR, respecting
  owner instructions on merge authority and repository protections.
- Update task state/evidence and residual blockers. A proposed or
  open PR is not a merged-main delivery. Continue unblocked tasks
  within the approved execution scope.

The default delegation is routine implementation, testing, docs,
branch/commit/PR creation and conflict diagnosis. Do not assume
permission to merge, deploy externally, spend money, access secrets
or real datasets, modify other repos, change approved architecture,
perform destructive operations or relax gates. Ask the owner for
only the decision or permission needed. Do not manufacture approvals
or official CI results.

### Historical owner decisions — 2026-11-25

Owner comments on [PR #57](https://github.com/GustavoMFDS/MirrorMind/pull/57)
approve preparing two independent research lanes in sequence: A, the narrow
UCI Online Retail #352 event-time retrospective, then B, aggregate Census
release-vintage evaluation. This approves preparation of adapters, protocols,
dataset/privacy documentation and synthetic tests; it does **not** authorize
acquiring or processing the real workbook or Census vintages. Before UCI bytes
are handled, verify original terms, attribution/change notice, minimized fields
(product/day/positive quantity after cancellation classification), secure
local storage, retention/deletion and a source manifest. Do not put raw or
identifying rows in Git, CI, logs, prompts or external services. Never infer
publication availability from `InvoiceDate`; retain
`event_time_retrospective_unverified_availability`. For Census, prefer free
official archived releases; use ALFRED only if access is free/authorized and
series terms plus historical-vintage evidence suffice. Do not claim SKU-level
demand or inventory validation. M5 remains NO-GO; B-01/B-02 remain open.

Owner confirms GitHub Actions allowance is exhausted, with no paid usage or
spending-limit increase authorized. Follow
[`LOCAL_QUALITY_GATE.md`](LOCAL_QUALITY_GATE.md) on a clean exact head; report
all six local checks as local evidence, not CI. Require independent review and
a separate final gate on the integrated candidate before any integration
decision. The owner's exact-head retest at `1bf178b` passed; the older
`8f906b8` timeout cause remains unknown. On the separate M1E-02 commit
`ac52ec9`, a restricted Windows sandbox reproduced a `test_health` wait in
asyncio loopback socket-pair creation; a five-second event-loop probe
reproduced the wait, and the same test plus full six-check gate passed outside
that socket restriction. Do not generalize this diagnosis to the older
`8f906b8` event. The latest `678755e` owner-recovered job records show
`steps=[]` and `runner_id=0` for the `test` and `symbol-catalog` jobs, but the
exact annotation remains unavailable; do not infer its per-check cause. Do
not disable checks, change protections, or start a self-hosted runner without
separate zero-cost isolated infrastructure approval. See comments
[7164856818](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818),
[7164870326](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164870326),
[7164895449](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164895449)
and [7167002881](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7167002881).

The later PR #57 update on exact head `1cff92c` reports a complete six-check
local gate: 712 pytest tests, Ruff, catalog, atlas, evidence and capability
checks passed; Actions failed before repository steps with the same
payment-or-spending-limit alternative. The independent retest at `1bf178b`
passed 700 tests and the same six local checks. The integrated candidate at
`42560e441f5020a5b4319a0f7b56474ef0485681` subsequently passed its own exact
six-check gate with 828 tests; receipt and limitations are in
[`LOCAL_QUALITY_GATE.md`](LOCAL_QUALITY_GATE.md). This remains local evidence,
not CI. See comment
[7169397485](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7169397485).

The consolidated candidate is `codex/m1-engine-provenance`, published as
[PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62) against
`main`. Commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85` preserves the exact
published ancestry of #52–#59; #60/#61 are excluded. It fixes PR #59 review
comment
[7174402947](https://github.com/GustavoMFDS/MirrorMind/pull/59#issuecomment-7174402947):
WorldKernel is named as the selected source when it supplies metrics, while
the invoked Python test double is recorded separately as parity oracle. V1
trace remains supported; composed workflow uses v2 typed execution evidence.
Commit `20e7b50f88df046eaf3541c5ea706b2e3b051aad` addresses the new #62
DecisionTrace V2 chronology finding: later execution instants fail, earlier
instants and timezone-equivalent equality pass. V1 remains unchanged. Its
exact-head gate passed 835 tests, zero skips and all six checks with
WorldKernel source pin `9b133ef873f2b6a7206c9c5742d40df4fccdb04a` installed.
The code-head receipt is
`results/local-quality-gate-20e7b50f88df046eaf3541c5ea706b2e3b051aad.json`.
After tracked status/backlog/handoff updates, repeat the full gate on the clean
documentation-inclusive SHA and report that exact receipt on PR #62. All such
results remain local evidence, not official Actions or merge approval.

The package remains SHA-pinned and optional; API startup and HTTP workflow
remain independent. The inventory demo's `demo-1` registry label is not
artifact attestation. The policy world preserves the M1E-03 transition and
exact parity on synthetic inputs. Do not edit WorldKernel, claim real demand
or calibrated outcomes, or describe the subprocess as a hostile-code sandbox.
At the time of PR #62 validation, no real UCI/Census bytes had been accessed.
PR #60/#61 remained separate then; main has since advanced through the PR #62
merge. The current baseline and UCI source state follow.

### Current owner decisions and local evidence — 2026-11-26

Main is `a456034c55ed7634ad4768b26788fec09dab1d08`, where PR #62 is integrated.
PRs #52–#59 are ancestors of that merge and must not be merged again. PRs #60
and #61 remain separate. Continue on `codex/uci352-pilot-20261126`; the prior
`codex/integration-pr63-pr64-349b77e` worktree was preserved.

The owner authorized one local, non-commercial UCI Online Retail #352
event-time run, a source-specific ZIP profile (192 MiB/member, 224 MiB total,
while generic defaults stay 64/128 MiB), and faithful `StockCode` handling:
exact positive five-digit integer cells become decimal text; internal ASCII
spaces remain untouched opaque category keys. Do not trim, filter or infer
from `Description`; report units per category, not physical-SKU demand.
Automated tests must remain synthetic.

The exact source archive and workbook were acquired from the official UCI
endpoint, hash-recorded, ignored by Git and stored under a verified private
local ACL. The path-free manifest records source metadata, byte hashes, the
UCI-reported date range, excluded-field missingness discrepancy, limits and
the 30-day deadline (`2026-12-26T22:39:45Z`). No raw rows or row-level
intermediates are in Git or docs. Schema and metadata preflight passed. The
first reader attempt stopped at the generic 100,000-group ceiling and
transiently materialized Description values before discarding them; none were
persisted or transferred. That path was replaced by selective OOXML streaming
with a regression proving excluded-cell text is not sent to Python character
callbacks. MM-020 authorizes up to 250,000 UCI-only groups. MM-021 governed the
stopped source attempt: it treated `C`/`c` as cancellations and excluded other
single-ASCII-letter-plus-six-digit invoice IDs. The owner later clarified in
MM-022 that only exact uppercase `C` is a cancellation; lowercase `c` and other
single-ASCII-letter-plus-six-digit IDs join the aggregate unverified class.
Synthetic regressions cover this
current rule. No real-source retry occurred. The earlier call exceeded
250,000 groups and returned no projection. Do not retry, chunk or widen the cap
without a new decision. No full projection, complete exclusion count,
empirical metric or real-source model card exists. Keep all results
retrospective and availability-unverified.

The synthetic invoice-classification regression now encodes MM-022: six-digit
IDs continue through the projection, exact uppercase `C` is cancellation, and
lowercase `c` plus other single-ASCII-letter-plus-six-digit IDs are excluded before
sales aggregation under one aggregate-only class count. Other formats fail
closed; generic projection remains unchanged. The real-source attempt used
MM-021 and was not repeated after this clarification. Because MM-021 also
excluded lowercase-`c` rows before aggregation, MM-022 only changes aggregate
classification counts; it cannot reduce the product-day group count or
resolve the existing cap failure. MM-022 does not raise MM-020's 250,000-group
ceiling.

Current code-bearing commit for [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65):
`94c60b6ee20adbb5023e11aeded9b8fff90b1176`, on
`codex/uci352-pilot-20261126` and based on `main` at
`a456034c55ed7634ad4768b26788fec09dab1d08`. Its focused UCI reader,
projection, workbook-flow and event-time suites passed 113 tests. The exact
clean-head gate passed 864 tests, zero skips and all six checks at
`2026-11-27T03:09:46.301016Z`; WorldKernel `0.0.1` was installed from reviewed
commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-94c60b6ee20adbb5023e11aeded9b8fff90b1176.json`.
This is local evidence, not Actions. The source attempt still reflects MM-021
and the 250,000-group stop; MM-022 has synthetic-only evidence and no source
retry or empirical result. A receipt for this code-bearing commit does not
cover later documentation commits; the exact final PR-head receipt is recorded
separately in the PR discussion.

Earlier published [PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65)
candidate was `75da34fc2cb91d3354cfbe49af43aeb40721164d` on
`codex/uci352-pilot-20261126`, based on main `a456034c55ed7634ad4768b26788fec09dab1d08`.
It passed the exact clean-head six-check local gate at
`2026-11-27T00:38:35.670136Z`: 863 tests, zero skips and all six checks.
Python 3.13.5; WorldKernel `0.0.1` installed from reviewed source commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; one existing Starlette/httpx
deprecation warning. A focused rerun passed 112 workbook, projection,
event-time and workbook-flow tests. Receipt:
`results/local-quality-gate-75da34fc2cb91d3354cfbe49af43aeb40721164d.json`.
PR #65 is open and awaits independent review. Actions diagnostics show only
automatic pre-start failures with the generic alternatives-only annotation;
no repository steps ran. Local receipts are not CI evidence. Do not change
gates, spend or modify the separate Census or WorldKernel repositories. See
the [change request](changes/M1B_01_UCI_REAL_SOURCE_PILOT.md),
[manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json),
[source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) and [B-01/B-02](BLOCKERS.md).

### Separate PR review state — 2026-11-27 UTC

PR #60 is open, non-draft and mergeable against `main` at
`a456034c55ed7634ad4768b26788fec09dab1d08`; current head is
`fafdedae3a76398e0450773065e40384c96d1ed7`. Its exact local gate passed 845
tests, zero skips and all six checks. The review correction and response are
in the [PR conversation](https://github.com/GustavoMFDS/MirrorMind/pull/60#issuecomment-7151002830).

PR #61 is also open, non-draft and mergeable against the same main; current
head is `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29`. Its exact local gate passed
841 tests, zero skips and all six checks. Its typed clock-failure correction
and response are in the [PR conversation](https://github.com/GustavoMFDS/MirrorMind/pull/61#issuecomment-7151371714).
Both remain separate from the M1/UCI/Census candidates and await independent
review. Their automatic Actions failed before repository steps under the
generic alternatives-only annotation; see [B-08](BLOCKERS.md). No official CI
success or merge is claimed.

The subsequent PR #65 status-sync head
`7e478440dc7661ebf35483073bad46ab290051c5` passed the exact local gate:
863 tests, zero skips and all six checks, with reviewed WorldKernel commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a` installed. Receipt:
`results/local-quality-gate-7e478440dc7661ebf35483073bad46ab290051c5.json`.
Its four automatic Actions checks failed without retrievable steps or logs;
the connector could not retrieve annotation text, so no specific cause is
assigned. The owner separately reports exhausted allowance and zero paid
budget. Local evidence is not official CI; see [B-08](BLOCKERS.md).

### Verified pre-reconciliation M1 and PR state — 2026-11-27 UTC

Before this documentation-only reconciliation, main was
`a456034c55ed7634ad4768b26788fec09dab1d08`, with PR #62 integrated and #52–#59
retained in its ancestry. PRs #60, #61, #63, #64 and #65 were open, non-draft
and mergeable against that main. Snapshot heads were #60
`fafdedae3a76398e0450773065e40384c96d1ed7`, #61
`f30556ecb9219c1bc4eb0eb720f9c59c3a729b29`, #63
`ffd3d770d5c7e9bafba975544de7947bcf20f1fc`, #64
`ca97ab61d15347aa271ee9ac8468a0714bdc3402` and #65
`b1bd7951ecc80988146eb46362eea99940ef7542`. #60/#61 have only the earlier
owner-authored `COMMENTED` findings, which their branches address; no new
independent approvals or unresolved inline threads were present. #63–#65 had
no review submissions or inline threads. Do not merge or close these PRs
without the separately scheduled review/integration decision.

PR #65 code commit `94c60b6ee20adbb5023e11aeded9b8fff90b1176` implements the
MM-022 UCI-only correction: exact uppercase `C` means cancellation; lowercase
`c` and other single-ASCII-letter-plus-six-digit prefixes are excluded as
unverified before aggregation, with aggregate counts only. The real-source
attempt used MM-021, exceeded the approved 250,000-group cap and returned no
projection or metrics. MM-022 has synthetic regressions only. Do not retry,
chunk or raise the cap under the current decision.

Prior documentation-inclusive PR #65 head
`b1bd7951ecc80988146eb46362eea99940ef7542`
passed the exact temporary local six-check gate at
`2026-11-27T03:17:39.573158Z`: 864 tests, zero skips and all six checks, with
WorldKernel `0.0.1` installed from reviewed commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-b1bd7951ecc80988146eb46362eea99940ef7542.json`.
This is local evidence, not official Actions. On that same prior head, direct CLI
replays for both the policy test double and explicit WorldKernel mode were
byte-identical per mode; each had 28 forecast steps and nine outcomes. The
WorldKernel result was `exact_match` with a separate parity-oracle record;
no write or action authorization occurred. This is the fictional experimental
workflow, not empirical or production acceptance.

Two automatic Actions attempts on `b1bd795` produced four failed pre-start
checks. The annotation lists recent payment failure **or** a spending-limit
increase; no job steps, logs or combined statuses were returned, so the
subcause is not established. The owner separately confirms exhausted quota
and zero paid budget. No rerun or protections/workflow change was made; see
the exact IDs in [B-08](BLOCKERS.md). Documentation-only follow-up
`c2410bdbafbb7a522730d31a304faa8a72b1b097` was pushed to PR #65 and passed
the exact six-check local gate at `2026-11-27T04:25:32.503435Z`: 864 tests,
zero skips, all six checks and the reviewed WorldKernel pin. Receipt:
`results/local-quality-gate-c2410bdbafbb7a522730d31a304faa8a72b1b097.json`.
The first sandboxed attempt timed out after 900 seconds in pytest; faulthandler
and a bounded event-loop child probe isolated the wait to Windows asyncio's
fallback socket pair before application code. The same SHA passed in the
authorized local environment without changing tests or code. Preserve the
timeout record at
`results/local-quality-gate-c2410bdbafbb7a522730d31a304faa8a72b1b097-sandbox-timeout.json`.
This local pass is not official Actions evidence.

A separate isolated invocation of
`tests/integration/test_api.py::test_synthetic_retail_decision_route_returns_the_shared_service_result`
produced no pytest output within 30 seconds and was interrupted. No stack was
captured and no cause is assigned. Do not treat that attempt as a pass; the
exact-head full-gate receipt above remains the independent suite evidence.

## 4. Mandatory documentation standard

MirrorMind documentation is both **engineering knowledge and a
learning resource**. Every substantive capability change must retain
the explanatory standard in the existing source-reviewed guides,
not merely append a changelog sentence or generated symbol list.
Technical prose, code comments and docs are in English. Report to
the project owner in Brazilian Portuguese.

### Required shape for a source-reviewed capability guide

Adapt the following structure to the change. Small changes may
extend the relevant existing guide rather than create a redundant
document. A new module/capability needs a clear guide and real links.

| Section | Content required |
| --- | --- |
| Purpose / status | What problem the feature solves; actual implemented, experimental, interface-only or planned scope; explicit non-goals |
| Architecture and dependency flow | Where it belongs, entrypoint, callers, downstream consumers, module boundaries, external dependencies; diagram or sequence when it materially clarifies flow |
| Source walkthrough | Real relative paths, exact classes/functions and responsibility; trace input through validation, computation/state mutation, output and failure. Explain **why** decisions exist, not line-by-line paraphrase |
| Contracts and semantics | Field meaning/types, units, versioning, canonical representations, state invariants, date/availability semantics, error handling, resource limits and compatibility |
| Worked example | Reproducible small example with commands/inputs/expected output based on actual implementation; clearly label invented fixtures, real vs simulated behavior and assumptions |
| Safety and failure modes | Trust boundaries, permissions, privacy, budgets, concurrency, rollback/recovery, timeouts, abuse and uncertainty as relevant; what a successful check does not prove |
| Testing and evidence | Exact test file and top-level selectors, what each normal/adverse test demonstrates, commands, actual observed results/SHA and limitations; do not label unexecuted examples as passed |
| Learner exercise | A small independent exercise that changes inputs, traces a symbol, predicts a failure and verifies behavior against actual code; include reasoning or expected observations |
| Evolution / recovery | Impact of compatibility changes, migration/rollback, troubleshooting, remaining work and linked scoped change request |

A walkthrough should answer: What does the code actually do? Why is
it structured this way? Which upstream inputs can it trust? Which
invariants must be preserved? What happens on failure? Which test
would falsify a claim? How can a new engineer reproduce the behavior?
Do not write textbook filler or copy entire source files into prose;
link relevant code and explain the non-obvious decisions.

### Required cross-reference updates

- [SYSTEM_MAP](SYSTEM_MAP.md): current data/control flow and boundaries.
- [SEMANTIC_COVERAGE](SEMANTIC_COVERAGE.md): actual guided/interface
  coverage for changed and new source modules. Do not confuse guided
  prose with tested or deployed functionality.
- [DEBUGGING](DEBUGGING.md): concrete symptoms, safe diagnostic
  steps, error/recovery paths; preserve failed evidence.
- [LEARNING](LEARNING.md): independent exercise or update an existing
  relevant lesson, with source/tests and expected observation.
- [REPOSITORY_ATLAS](REPOSITORY_ATLAS.md): a resolving relative link
  for every new tracked file, including tests and docs.
- [generated/SYMBOLS](generated/SYMBOLS.md): regenerate with
  `python scripts/docs/catalog.py --write` after source changes;
  never manually edit the generated catalog.
- [EVIDENCE_MAP](EVIDENCE_MAP.json): unique reviewed claim IDs, actual
  guide paths, exact top-level pytest function selectors and explicit
  limitations for relevant new claims.
- [CAPABILITY_LEDGER](CAPABILITY_LEDGER.json) and
  [system capability route](../../src/mirrormind/api/routes/system.py):
  truthful status parity for externally visible capabilities.
- [Engineering hub](README.md): add useful navigation to new guides.
  Update [roadmap](../ROADMAP.md), backlog and relevant status/blocker
  entries for actual progress, not speculative claims.
- [DECISIONS](../DECISIONS.md): record architectural decisions only
  after genuine approval; mark proposals honestly.

Use existing [atomic publisher guide](ATOMIC_GOVERNED_PUBLISHER.md),
[remote head client guide](REMOTE_FENCE_HEAD_CLIENT.md) and
[staged rolling baselines guide](M1_STAGED_ROLLING_BASELINES.md) as
examples of actual source contracts, worked methods, tests, threat
boundaries and limitations. Preserve their style, not necessarily
their length. Keep one source of truth for each mutable claim.

For real data, complete the [dataset card](DATASET_CARD_TEMPLATE.md).
For forecasting, complete the [model card](FORECAST_MODEL_CARD_TEMPLATE.md)
with temporal evaluation and uncertainty. For decision results,
complete a [decision trace](DECISION_TRACE_TEMPLATE.md). These are
substantive reviews, not a checkbox or synthetic permission token.

### Documentation review checks

A reviewer must be able to navigate from a product claim to the
actual function, find its callers, trace the state or value through
the system, locate the matching test, reproduce an example, and
identify which parts remain hypothetical. If that is impossible,
documentation is incomplete even if Markdown links and AST guards
pass. Replace stale summary claims rather than endlessly appending
contradictory notes. Never erase relevant historic evidence or
rewrite a planned feature as if it already executes.

## 5. Reporting format for each delivery

- Task ID and scoped goal; baseline and final SHA; branch/PR and merge
  state.
- Actual implementation, impacted modules/functions and how the
  architectural flow changed; existing interfaces preserved or
  explicit reviewed migration.
- Test commands, exact outcomes, environment, local receipt and
  separately observed official CI status.
- Documentation walkthrough/learning/evidence updates and links.
- Security, scientific and operational limitations, outstanding
  dependencies, owner decisions and next safe task.
- Reproduction instructions another engineer can run independently.

Never count files, tests, documents or PRs as a percentage of product
completion. Continue towards the next functional gate, especially
the M1 runnable decision workflow, and preserve truthful status.

## 6. Resume prompt

When a new agent starts or loses context, give it the following
short instruction instead of repeating the entire product specification:

> Continue MirrorMind in the authorized local checkout at
> D:\MirrorMind. Read AGENTS.md and docs/engineering/CODEX_HANDOFF.md,
> then the master plan, project status, backlog, definition of done
> and blockers linked there. Reconcile the current Git state and
> concurrent work; select the highest-priority unblocked bounded task
> that advances the functional MVP, follow the source walkthrough
> and evidence/documentation requirements, run the actual gates and
> open a reviewable PR. Preserve all existing protections, report
> limitations and continue independent tasks when an external decision
> is required. Do not invent acceptance or deployment approvals.

If the owner provides newer or narrower instructions, follow those
within the repository's safeguards.
