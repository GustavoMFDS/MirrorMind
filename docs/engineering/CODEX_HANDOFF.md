# Agent handoff — continuous engineering and documentation standard

## Current continuation - 2026-11-27

- Current `main` is `10b94c9d7b01bc7072a18d8124cbc8090a6b1925`, the normal PR #81
  merge after PR #80 (`7efced5`). PR #79's portfolio/index update merged at `5100ebf`;
  PR #77 merged at `540c474`; nine official
  contexts passed on exact reviewed head `df7c450523a8f3475e0a8161936f6ac80e705720`.
  PR #78 / MM-024 merged normally at `291562a`; its final head
  `8c8f8627a7162cb766a70d264569d3fcc2d442c8` passed 968 tests, zero skips,
  six local checks and six observed official jobs. Those jobs are in runs
  `46072345590`, `46072345631` and `46072345603`; combined status for the merge
  and current main was empty, so keep claims scoped to their exact PR heads.
- PR #79 exact head `b5c1bcc3dff7106e2f370c648c836b3251b17f45` passed 970
  tests, zero skips and six local checks; seven observed workflow jobs
  succeeded and the guarded deploy job was skipped. PR #80 exact head
  `e6a28acd5cf0470c8d8628d6ee5957f3815d3f67` passed 976 tests, zero skips
  and six local checks; eight observed jobs succeeded across five workflows,
  with main-only deployment and manual rehearsal skipped. See
  [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md); merge SHA `7efced5` has no
  combined-status entries. PR #80's benchmark is synthetic and release prep
  does not create a release.
- PR #81 / REX-15 exact head `41e6db8618a00c93f3a00ca6638ed96ab623dcbc`
  passed 977 tests, zero skips and six local checks. Five official workflows
  completed with nine applicable jobs successful; main-only deployment and
  release rehearsal were skipped. The CI container smoke passed, although the
  developer's local Docker daemon was unavailable. The merged `10b94c9` SHA
  has no combined-status entries; keep evidence scoped to the PR head.
- The owner approved MM-024's local UCI #352 policy: six-digit IDs are normal;
  only uppercase `C` plus six digits means cancellation; other single ASCII
  letters plus six digits are excluded before sales grouping and represented
  by one aggregate unverified class; all other formats fail closed. Existing
  MM-022 code and synthetic regressions already implement this, including
  identifier redaction and unchanged generic-reader behavior.
- The UCI source call stopped above the 250,000 product-day group ceiling
  without a complete projection, full exclusion counts or metrics. MM-024
  changes an exclusion label, not the set of sales rows or group cardinality.
  Do not reread, chunk, sample or raise the cap. Preserve local snapshot
  deletion by `2026-12-26`; no empirical score is available.
- Continue M2-02 on `codex/m2-02-retrieval-evaluation-20261127`. Its ancestry
  includes feature commit `fc43935`, merge `f74d286` of main `7efced5`, and
  merge `0b4881f` of current main `10b94c9`. Its scope is a bounded offline evaluator for the existing
  fictional M2-01 index. It must keep `evidence_and_rag` planned and local
  retrieval experimental; no route, auth, real data, persistence or RAG claim.
  Source walkthrough, debugging/learning, evidence/atlas/catalog updates are
  drafted and all five focused static checks pass; the targeted retrieval
  suites pass 22 tests. Regression coverage now rejects empty/oversized
  corpora and unsupported document objects before scoring. The clean
  six-check gate passed on exact candidate `4ccff24cbc73045a4d01fdc9a5aa299d69e59038`:
  989 tests, zero skips and all six checks; receipt is in
  `results/local-quality-gate-4ccff24cbc73045a4d01fdc9a5aa299d69e59038-workspace.json`.
  Earlier, the same gate on `e3e55d4` timed out only when sandboxed at
  TestClient's local socketpair setup; unchanged runs outside the sandbox passed.
  See [B-07](BLOCKERS.md). Any final PR head after subsequent tracked changes
  needs its own exact receipt. Local mypy is absent; rely on the candidate's
  official quality job for strict retrieval typing and record its exact status.
- Keep automated tests synthetic. Census bytes, FRED/ALFRED, paid usage and
  new UCI source processing remain unauthorized. M1 synthetic workflow is
  integrated; empirical and production acceptance remain open. Preserve the
  zero-paid budget and all protected-main checks.


## Historical review reconciliation - 2026-11-27

Main `4efba1e830f2836b6d4f9c9b4f5ed776126e55cc` incorporates #60, #61 and
#64 through #66. The independent post-merge gate passed 856 tests, zero skips
and all six checks plus examples Ruff. See [PR #66](https://github.com/GustavoMFDS/MirrorMind/pull/66).
M2-01, G-01 and ENG-02 are integrated within their experimental scopes.
The Census review candidate preserves the exact #63 head and adds the
uppercase Decimal fingerprint fix with a failing-before/passing-after
regression. The candidate is not accepted until the combined gate and
merge decision recorded in the integration PR. No actual Census data or
FRED/ALFRED access is authorized; the direct original Census artifact
proposal requires separate owner decisions under B-01/B-02.

PR #65 was independently accepted and integrated at `51c90d2`. The UCI source
was privately acquired under MM-017 through MM-020; the call stopped above
250,000 product-day groups without a complete projection or score. Parser
review findings have synthetic regressions, and the exact integrated tree
passed its local and official checks as recorded above. MM-024 now confirms
that only exact uppercase `C` plus six digits indicates cancellation; other
single-letter ASCII prefixes are excluded as unverified, with aggregate-only
counts. Existing code and tests already satisfy this rule. Because the
stopped call had already excluded those rows before grouping, the new
classification does not change accepted rows or the group-limit failure.
Preserve the `2026-12-26` deletion deadline; do not chunk, sample or increase
the cap, and do not report empirical metrics without a full projection.
Historical pre-start check diagnostics remain unexplained despite current
green public checks; the zero-paid budget remains. The dated branch and status
records below are historical where inconsistent with this reconciliation and
live PRs.

## Historical integration candidate - 2026-11-27

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

## Historical owner-approved continuation — 2026-11-27

- `main` is `a456034c55ed7634ad4768b26788fec09dab1d08`, the
  ancestry-preserving PR #62 merge. Independent post-merge gate passed 835
  tests, zero skips and six checks with the exact WorldKernel source pin. PR
  #52 is merged; #53–#59 are closed as incorporated and their branches remain
  available. Do not duplicate their integration.
- PR #60 is separate and ready for independent review at
  `fafdedae3a76398e0450773065e40384c96d1ed7`; its local gate passed 845 tests,
  zero skips and six checks. PR #61 is separate and ready at
  `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29`; its gate passed 841 tests, zero
  skips and six checks. Exact #61 receipt, time and pin are in the live PR body.
- Census remains separate as open PR #63 and preserves merge `55e91f7` from
  `main` plus the PR #62 ancestry. Follow-up commit
  `00311c6344e8a70bb72315afc10f4fbd02926d26` rejects first estimates and
  revisions published inside their reference month; selector-boundary and
  public-evaluator regressions cover the original false-scoring case. The
  pre-diagnostic source-policy head
  `47cdb587b0deab19835acd1435e4bd028ba28519` passed the exact clean-head gate
  at `2026-11-27T02:38:46.324939Z`: 882 tests, zero skips and all six checks,
  with WorldKernel `0.0.1` at reviewed source pin
  `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
  `results/local-quality-gate-47cdb587b0deab19835acd1435e4bd028ba28519.json`;
  PR comment [7208332106](https://github.com/GustavoMFDS/MirrorMind/pull/63#issuecomment-7208332106)
  records it. Four automatic Actions checks on that head failed before jobs
  ran. The annotation lists payment failure or a spending-limit increase as
  alternatives; diagnostics expose no jobs, steps, logs or combined status, so
  no cause is inferred. [B-08](BLOCKERS.md) records exact run/check IDs. Keep
  #63 separate from #60/#61/#64 pending independent review; no integration
  decision is implied.
- PR #62 integrated the synthetic UCI event-time evaluator into main. PR #63
  contains only a synthetic Census vintage evaluator. The UCI then aggregate
  Census/ALFRED pilot sequence remains preparation-only; no source file, FRED
  API response or credential was downloaded into the workspace or pilot store.
  Search previews of public Census release summaries incidentally displayed
  published aggregate values; none was retained or used in evaluation. No pilot run
  occurred. B-01/B-02 still require source rights, privacy, retention and
  time-availability evidence before any real run; see the
  [Census protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md).
- Metadata-first due diligence on 2026-11-27 confirms the direct Census MARTS
  archive as the preferred no-credential candidate for national retail and
  food-services sales. Current release text says seasonally adjusted but not
  price-adjusted; its nominal/current-dollar interpretation still needs exact
  table verification. The 2026 annual revision index reaches August 2026 but
  does not establish first-release completeness. The April 2025 removal of
  nonemployers is a documented definition boundary and must be carried in any
  reviewed source manifest. The current FRED Services terms apply to ALFRED
  and the API, forbid storing/caching/archiving FRED content, and the API
  terms additionally prohibit software/AI-development use. FRED/ALFRED is
  therefore NO-GO for the current development and archive route absent
  St. Louis Fed written authorization or changed terms plus separate
  series-owner rights clearance; this does not decide rights for original
  Census files. Census citation guidance and its general employee-created-work
  copyright statement inform the proposal but do not establish rights for a
  specific MARTS file or embedded third-party content; see the [Census
  protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md). The proposed source is direct
  original MARTS release files, subject to project-scope approval, attribution,
  storage, retention and output review. Proposed retention is 30 days for local
  value-bearing artifacts, followed by deletion. The proposed fixed evaluation
  uses a frozen 60/20/20 chronological split, first estimates, 1/3/6-month
  lag-12 and trailing-mean baselines, strict-before date cutoffs, preserved
  gaps, and a 12-month moving-block bootstrap only with 60 matched holdout
  origins per horizon. These are not yet approved. No archive file, API
  response, key, account or workbook was acquired; keep B-01/B-02 open and
  tests synthetic. The complete proposal and owner decision checklist are in
  [the Census vintage protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md).
- The owner confirms Actions quota exhaustion and zero paid budget. Use the
  exact-clean-head local gate, distinguish receipts from CI, and do not
  register a runner, modify workflows/protections or retry prior start failures.
- ENG-02 is separate maintenance in [PR #64](https://github.com/GustavoMFDS/MirrorMind/pull/64),
  head `ca97ab61d15347aa271ee9ac8468a0714bdc3402`; its exact local gate passed
  840 tests, zero skips and all six checks. Two Actions attempts on this head
  failed before job steps; the annotation does not identify a specific cause.
  See [B-08](BLOCKERS.md). M2-02 follows M2-01 (#60) review/integration and
  independent review of #61/#63. Keep the review queue stable before adding
  feature work.

## 1.1 Historical owner-approved continuation decisions — 2026-11-25

## Historical independent maintenance — 2026-11-26

- ENG-02 is separate maintenance in [PR #64](https://github.com/GustavoMFDS/MirrorMind/pull/64),
  branch `codex/eng-02-examples-ruff`, based on post-#62 `main` at `a456034`.
  The five original `ruff check examples` findings were reproduced. RUF007's
  `itertools.pairwise` correction has direct empty/singleton/consecutive/gap
  regressions; no forecast or authorization behavior changed. Exact-head local
  gate passed on `271f01cae5aacf274d3fa9f9ff2ede34796471ef` with 840 tests,
  zero skips and six checks; receipt is
  `results/local-quality-gate-271f01cae5aacf274d3fa9f9ff2ede34796471ef-venv.json`.
  Actions run `45769344631` has no job steps or retrievable logs, so the cause
  is unknown. Keep #64 separate from #60/#61/#63.

## Historical owner-approved continuation — 2026-11-26

- Current `main` is `a456034c55ed7634ad4768b26788fec09dab1d08`, the
  ancestry-preserving PR #62 merge. Independent post-merge verification ran
  the complete temporary local gate: 835 tests, zero skips, six checks and
  the exact WorldKernel source pin. The reviewer recommends preserving this
  merge ancestry. PRs #52–#59 are reconciled as incorporated by #62; retain
  their branches where useful and do not repeat their merges.
- The M1 path on main is a synthetic experimental workflow, not a real-data,
  empirical-forecast or production acceptance. Census remains a separate open
  PR #63. PR #60 is open/non-draft for independent review. PR #61 has been
  synchronized with main through ancestry-preserving merge
  `66fc9fa001eaa6bd3adbc8f8d1606f3743239d21`; its merge-head gate passed 841
  tests, zero skips and six checks. Documentation refresh commit
  `47fdceb58a2c3802f8e66e5aea51318a698ffe62` also passed 841 tests, zero skips
  and all six checks. The documentation baseline
  `20ce86bde740d5b46d7aeba4d13138884e211dba` passed the exact gate again with
  841 tests, zero skips and all six checks. PR #61 is now open/non-draft and
  ready for independent review. Its live PR body carries the current exact
  SHA and receipt; any subsequent commit needs a fresh gate. Keep #60, #61 and
  #63 separate.
- PR #62's final independent comments are
  [7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)
  and [7181477141](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181477141).
  The former approves the experimental synthetic M1 scope and recommends a
  merge commit; the latter verifies `a456034` and the separate Census
  descendant. Neither grants production, scientific-data or official-CI
  approval.
- The owner confirms Actions quota exhaustion, a zero-paid budget and no limit
  increase. Follow [LOCAL_QUALITY_GATE.md](LOCAL_QUALITY_GATE.md) on exact
  clean heads. Local receipts are not CI. Do not register a runner, change a
  workflow, alter protections, or retry known pre-job failures. No new paid
  infrastructure is approved.
- Continue UCI #352 then aggregate Census/ALFRED preparation under B-01/B-02.
  Automated tests stay synthetic. No source bytes, keys or credentials may be
  acquired or processed until source-specific rights, privacy, retention,
  snapshot and temporal-availability conditions are separately satisfied.
- After the remaining PR review queue is prepared, M2-02 retrieval evaluation
  is the next M2 slice and depends on M2-01 (#60) review/integration. Do not
  open disconnected feature work while this queue remains unsettled. ENG-02
  tracks five pre-existing Ruff findings in `examples/` as separate
  maintenance; leave those files out of #60/#61/#63.

## Historical continuation decisions — 2026-11-25 (superseded)

- Research preparation proceeds A then B: UCI Online Retail #352 event-time
  retrospective first, then an aggregate Census release-vintage study.
  This historical decision did not approve acquisition or processing of real
  data. The 2026-11-26 terms review supersedes ALFRED as an active data route:
  current FRED terms block the proposed software-development and local archive
  use absent St. Louis Fed written authorization or changed terms plus
  separate series-owner rights clearance. The direct Census candidate
  also needs source-specific approval. Keep raw data out of Git, CI, logs,
  prompts and external services; automated tests remain synthetic.
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

## 1.2 Historical resumed state before PR #62 merge — 2026-11-25 (superseded)

GitHub review metadata confirms PR #62 remains open, mergeable and directed at
`main`, at published head
`0bed1269613eb689e84ad971c7d8f1878767d6cf`. The branch preserves published
PR #52–#59 ancestry; #60/#61 remain excluded. The exact docs-inclusive head
passed all six checks with 835 tests and zero skips under the reviewed optional
WorldKernel pin. This is local validation, not GitHub Actions or integration
approval.

The independent branch `codex/m1-census-vintage-adapter` is a local descendant
of that head via merge `8560ad6`. Independent review comment `7179081819`
identified four defects across DecisionTrace V2 chronology and the separate
Census evaluator. The DecisionTrace fix is already included in PR #62. Census
fixes are kept outside that PR in commit
`3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6`: exact Decimal-context-independent
metrics, first-estimate/revision chronology, exclusion and counting of
unanchored revisions, and fail-closed overflow/underflow. Public regressions
and technical/learning documentation are included. Its exact clean
implementation-head gate passed 877 tests with zero skips and all six checks;
WorldKernel `0.0.1` was installed from
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. Receipt:
`results/local-quality-gate-3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6.json`.
One existing Starlette/httpx TestClient deprecation warning appeared. The
status/backlog/handoff/gate-documentation commit
`a6e3ed3355a1e52712542e6ae0d80d908885a82b` then passed that exact six-check
gate with 877 tests and zero skips; receipt:
`results/local-quality-gate-a6e3ed3355a1e52712542e6ae0d80d908885a82b.json`.
Any later tracked change requires its own exact-clean-head gate. Do not claim
Actions passed.

Do not push or open a separate Census PR while #62 awaits final independent
review. Preserve the zero-cost Actions decision and synthetic-only tests. B-01
and B-02 still gate acquisition or processing of real UCI/Census records; B-08
still gates official Actions evidence. Continue only no-cost work that directly
advances the M1 acceptance path without duplicating this stack.

## 1.3 Historical resumed state before #61 sync and PR #63 publication — 2026-11-26 (superseded)

PR #62 is merged at `a456034c55ed7634ad4768b26788fec09dab1d08`. The exact
published heads of #52–#59 are its ancestors; #53–#59 are closed as
incorporated and all branches remain available. Independent post-merge
validation passed 835 tests, zero skips and six checks with the reviewed
WorldKernel pin; this is local evidence, not Actions.

PR #60 is now open against `main`, ready for review and mergeable at
`fafdedae3a76398e0450773065e40384c96d1ed7`. Its ancestry-preserving merge
includes the new main, and its exact local gate passed 845 tests, zero skips
and all six checks. Receipt and review finding response are on PR #60 and in
`LOCAL_QUALITY_GATE.md`. Keep it separate from Census and #61; do not merge or
bypass required checks.

The Census branch `codex/m1-census-vintage-adapter` includes `a456034` through
merge `55e91f7d73c67867edaf1aa790242f6cdbc611b9`. Its exact reconciled gate
passed 877 tests, zero skips and all six checks with reviewed WorldKernel;
receipt is in `LOCAL_QUALITY_GATE.md`. The current status/receipt updates need
their own exact gate before the branch is pushed as a separate PR (#63).

PR #61 remains a separate G-01 slice on its prior base. Synchronize it with
`a456034` using an ancestry-preserving merge, preserve clock/store failure
contracts, review conflicts and gate its exact clean head before review. Do not
fold it into PR #60 or the Census branch.

The owner approved preparation for A+B pilots only: UCI #352 event-time
retrospective, then aggregate Census publication-vintage evaluation. Do not
acquire or process real bytes or credentials until exact source rights,
privacy, retention and temporal evidence are approved under B-01/B-02. Keep
automated tests synthetic. GitHub Actions is unavailable within the zero-paid
budget (B-08); do not buy usage, change limits, register a runner or alter
protections.

ENG-02 tracks five pre-existing Ruff findings in three M1 examples separately
from the review queue. Do not auto-apply the unsafe RUF007 suggestion.
Consolidate #60, Census and #61 before expanding M2 beyond M2-01.

## 1.2 Historical resumed state — 2026-11-26

PR #62 is merged into `main` at
`a456034c55ed7634ad4768b26788fec09dab1d08`. Independent post-merge local
validation passed 835 tests, zero skips and all six checks with the exact
reviewed WorldKernel pin. This is local evidence only; GitHub Actions remain
unavailable under the owner's zero-paid-use decision.

The exact published heads of PRs #52–#59 are ancestors of `a456034`. PR #52
was already merged, and #53–#59 were closed as incorporated after those
ancestry checks. Their remote branches remain intact; do not merge or delete
them. PRs #60 and #61 stay separate. PR #60 now includes the new main via
ancestry-preserving merge `a5186a680b307c4ecd9d56321321a5b27048731d`; its
exact sync-head gate passed 845 tests, zero skips and all six checks with the
reviewed WorldKernel pin. Docs candidate `26e45b4620e9e13e12a745db3c99ead196c656d0`
also passed 845 tests, zero skips and all six checks; its receipt is in
`LOCAL_QUALITY_GATE.md`. Rerun the gate after this status refresh, then push
and prepare #60 for independent review. #61 still needs its
ancestry-preserving sync and exact gate. Report local evidence separately
from Actions; keep required protections unchanged.

The local Census branch passed its pre-sync gate at `da540a2` (877 tests,
zero skips and six checks, plus 64 focused tests). Merge commit `55e91f7`
includes `a456034` without discarding Census history. Re-run the exact local
gate on that reconciled state, publish it as a separate PR, and do not add it
to #60 or #61. #60's sync preserved its excerpt-integrity regressions and the
newer M1 contracts; #61 remains an independent G-01 slice.

The local `ruff check examples` inspection found five existing findings in
three M1 example files. ENG-02 tracks that cleanup separately; do not silently
fold it into the queued PRs or apply Ruff's unsafe RUF007 fix without semantic
review.

The approved A+B pilot order permits preparation only: UCI #352 retrospective
by event time, then aggregate Census publication-vintage evaluation. No real
bytes, credentials or source records are authorized until B-01/B-02 are
resolved. Keep automated fixtures synthetic and preserve privacy, licensing,
availability-time and retention boundaries. Do not claim empirical forecast
quality from synthetic results.

M1's synthetic end-to-end flow is now integrated, but M1 is not complete:
source rights, empirical evaluation, broader engine isolation, authenticated
review and production controls remain open. M2-01 retrieval is a local
fictional slice without authentication or an HTTP route. Continue with
reviewable increments; do not broaden M2 while #60/#61 and Census are still
being consolidated.

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

### Historical owner decisions and evidence through 2026-11-25

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
`event_time_retrospective_unverified_availability`. For Census, prefer direct
official archived releases subject to artifact-level review. Current FRED
Services terms apply to ALFRED and prohibit storing/caching/archiving; API
terms also prohibit software/AI-development use, so FRED/ALFRED is NO-GO for
this development/archive route absent St. Louis Fed written authorization or
changed terms plus separate series-owner rights clearance. Do not claim SKU-level
demand or inventory validation. M5 remains
NO-GO; B-01/B-02 remain open.

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

The separate local branch `codex/m1-census-vintage-adapter` prepares a pure
synthetic aggregate-vintage selector on top of PR #62. Its source/docs commit
passed the exact local gate with the reviewed WorldKernel pin installed; a
documentation-only evidence follow-up is gated on its own exact head. Keep it
separate from the consolidated candidate and do not publish it until the
candidate's review state supports a reviewable follow-on. It consumes only caller-supplied normalized records in memory;
source parsing, downloads, credentials, real values, permissions and forecasts
remain outside this slice. The selector's evidence must never be presented as
resolution of B-01/B-02.

The same local Census pilot branch now also contains an experimental fixed
baseline evaluator and generated validation/holdout example. It uses the
normalized selector, records an exact input fingerprint, keeps first-estimate
targets separate from later revisions, and abstains on incomplete history.
The focused evaluator, selector and CLI suite passed 28 tests. Implementation
commit `ce446496616d20a782e0ebcb7e7b0f42cec49e83` passed the exact six-check
local gate with 860 tests, zero skips and the reviewed WorldKernel pin
installed; the receipt is recorded in the change request. This is not official
Actions. The branch remains unpushed, separate from PR #62 and unable to
resolve real-source blockers. Re-run the exact-head gate after later changes.

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
