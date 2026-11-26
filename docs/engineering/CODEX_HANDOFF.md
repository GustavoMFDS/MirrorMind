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

## Current independent maintenance — 2026-11-26

- ENG-02 is separate from the open product/review queue and is being handled
  on `codex/eng-02-examples-ruff`, branched from the post-#62 `main` at
  `a456034`. The five original `ruff check examples` findings were reproduced.
  RUF007's `itertools.pairwise` suggestion is being applied only after tests
  prove equivalence for the sorted `list[date]` input and Python 3.11 minimum;
  no forecast or authorization behavior should change. Keep the change
  synthetic-only and separate from #60/#61/#63.

## 1.1 Owner-approved continuation decisions — 2026-11-25

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

### Current owner decisions — 2026-11-25

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
No real UCI/Census bytes were accessed. PR #60/#61 remain separate, and no
remote branch or `main` was changed.

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
