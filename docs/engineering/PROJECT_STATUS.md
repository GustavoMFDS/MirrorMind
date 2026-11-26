# Project status — reviewed baseline, not live status

**Baseline:** 2026-11-23 (Brazil local date); main
`e4f05a152aefcf68fa8ec22f3baa3b61adb8519d` (PR #51 merge commit).
This is the latest confirmed merged-main baseline after the handoff-doc
update. PR #50 (`036b8d6`) is its parent. This is not the live status of a
working branch; reconcile active task claims below with Git, open PRs, actual
code and quality receipts before using this document as an execution report.

**Verified baseline on e4f05a1:** 691 pytest tests passed, one existing
Starlette/httpx deprecation warning. Six local gate checks passed
(pytest, Ruff, symbol catalog, atlas, evidence and capabilities) on
that SHA, including after relocation to the permanent Windows
checkout at `D:\MirrorMind`. The checkout was clean at migration
verification. GitHub returned no workflow runs or check statuses for
PR #51's merge commit in the preceding inspection; remote CI is therefore
not represented as passing. No PRs were open at that preceding status
check; this is historical, not a current open-PR inventory.

At this merged baseline the [capability ledger](CAPABILITY_LEDGER.json)
contained 40 entries: 2 implemented, 31 experimental, 1 interface-only
and 6 planned. The active M1B-02 branch adds one experimental composite
evidence-flow declaration; that branch-local addition is not part of the
merged baseline. Regenerate counts from the ledger rather than treating
them as progress percentages. The reviewed API reports a scaffold,
not a production-ready AI platform.

## Current consolidated M1 candidate — 2026-11-25

The review candidate is branch `codex/m1-engine-provenance`, published as
[PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62) against `main`.
Code correction commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85` fixes the
PR #59 provenance finding; the final review head is the exact revision shown
in PR #62 and `results/local-quality-gate-<full-head-sha>.json`.
Its history preserves all exact published heads of PRs #52–#59 as ancestors;
#60 and #61 are excluded. GitHub reports the candidate as mergeable. The
candidate contains the synthetic M1 workflow, pinned local WorldKernel runner
and policy world, plus the UCI event-time evaluator and aggregate Census
protocol. No real source bytes were acquired.

PR #59 review comment
[7174402947](https://github.com/GustavoMFDS/MirrorMind/pull/59#issuecomment-7174402947)
identified an engine-contract mismatch and ambiguous parity invocation in the
prior `995f55d` candidate. Commit `74330d8` adds typed v2 execution evidence,
binds every outcome to its selected-result engine, and represents the Python
test double separately as a parity oracle when WorldKernel supplies selected
metrics. It preserves trace v1. Regression coverage checks both engines,
replay, mismatched/dangling provenance and parity-digest disagreement.

The later independent review found that v2 accepted execution evidence dated
after trace creation. Commit `20e7b50f88df046eaf3541c5ea706b2e3b051aad`
adds UTC-instant chronology validation and regressions for later, earlier and
timezone-equivalent equal timestamps. Its exact-clean-head six-check local
gate passed 835 tests with zero skips, Ruff, catalog, atlas, evidence and
capability checks, with WorldKernel `0.0.1` installed from reviewed commit
`9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. One existing Starlette/httpx
`TestClient` deprecation warning appeared. Receipt:
`results/local-quality-gate-20e7b50f88df046eaf3541c5ea706b2e3b051aad.json`.
This is local evidence, not Actions, independent approval or merge evidence.
After this documentation update, the exact clean candidate head must pass the
same six-check gate; its receipt and full SHA are reported on PR #62. PR #62
remains awaiting review. `main` was not changed, and #60/#61 remain separate.

## Active branch evidence — 2026-11-25

The composed synthetic evidence flow is implemented in the history beginning
at `c51ab30370db47e9f7105c97f870008e4fc442c5`; the latest published PR #52
follow-up is `b431d11bf0ac841ff30353a06263d23fb901307c` on
`codex/m1b-02-synthetic-evidence-flow`, proposed in draft
[PR #52](https://github.com/GustavoMFDS/MirrorMind/pull/52). The PR is
unmerged. Its one new capability is experimental and uses only bounded
local fixtures and caller-declared dates.

The full local quality gate passed on exact published head `b431d11bf0ac841ff30353a06263d23fb901307c`
at 2026-11-25 03:51:25 UTC: all 696 tests, Ruff, symbol catalog, repository
atlas, evidence map and capability checks passed. The focused M1B-02 tests
also passed, including child-to-aggregate receipt equality, missing and late
availability abstention, calendar/release rejection, and digest/declaration
mismatch rejection. This is local evidence on the exact branch head; it is
not official CI or merge evidence.

The prior published heads `c093ba6` and `e3aedaf` also passed complete gates
at 03:48:38 and 03:35:40 UTC. An earlier restricted exact-gate run on
implementation commit `c51ab30`
timed out at 900 seconds while `tests/integration/test_api.py::test_health`
waited during asyncio socket-pair creation before application code. The
standalone reproduction occurred on Python 3.12 and 3.13.5. A host/sandbox
loopback cause was proposed but never established. The subsequent full gate
pass on the current head resolves that timeout as an active blocker for PR #52;
retain the failure as historical evidence only. See [B-07](BLOCKERS.md).

PR #53 is on `codex/m1c-01-synthetic-retail-evaluation`, stacked on PR #52.
Merge commit `e922b03` synchronizes it with PR #52 head `b431d11`; its current
published head is `79d3679013576c6a209bed9fa031b7f0fabd0d8d`. The PR remains a
draft and unmerged. It composes the staged synthetic evidence flow with
release-aware matched-origin baselines and a deterministic fictional CLI; no
real-data ingestion, HTTP forecast endpoint or predictive-skill evidence is
added. Four integration tests plus six retail backtest unit tests pass, and
the exact-head gate passed 700 tests plus Ruff, catalog, atlas, evidence and
capability checks at 2026-11-25 04:08:00 UTC. API tests ran; one existing
Starlette/httpx deprecation warning was emitted. This is local evidence only.
Current Actions runs [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354)
and [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397)
failed with no steps/logs and no specific cause recovered. B-01/B-02 still gate
real data and empirical evaluation; B-08 blocks official CI. The older B-07
timeout on #52 is historical, not evidence of failure on #53.

The active continuation branch `codex/m1f-01-decision-trace-contract`
implements M1F-01 on top of the M1C-01 stack. The local result contract
separates observations, estimates, conditional outcomes, assumptions, missing
evidence, cost measurement states and human review. Review correction commit
`f02459d977fd263b03ddf60264b9069ae08b189b` adds terminal-review chronology,
context-independent lossless Decimal hashing, and field/aggregate/reference
bounds; evidence links now name each regression function. The decision-trace
unit suite passes 28 tests. Ruff, source catalog, atlas, evidence and
capability checks pass locally, as does `git diff --check`. For the atlas
check, only the existing untracked Graphify output was excluded via
a temporary local Git exclude file; no source guard or project ignore rule was
changed. The published integrated candidate `4d220066c3e9ab83a321ac9517bbabc8fc22e293`
passed the complete local gate at 2026-11-25 04:25:37 UTC: 728 tests, Ruff,
catalog, atlas, evidence and capability checks. One existing
Starlette/httpx deprecation warning appeared. HTTP runtime was not tested and
no new route was added. The result digest remains a recomputable content hash,
not a signature; all source/model/engine references remain caller assertions.
The task remains interface-only and has no authenticated producer, storage,
decision ranking, execution permission or real engine evidence. The source
walkthrough is in [DECISION_TRACE_RESULT](DECISION_TRACE_RESULT.md). PR #54
remains a draft stacked on #53. Merge commit `e493b4c` synchronizes the local
branch with published PR #53 head `79d3679`, retaining both histories and the
nested-receipt regressions. The complete local gate passed on this integrated
candidate as recorded above. On published #54 head `4d22006`, the latest test
run [45546742718](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742718)
and symbol-catalog run
[45546742695](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742695)
failed before repository steps with the same alternative account annotation;
no code tests ran remotely. See [B-08](BLOCKERS.md).

## PR #55 review correction and current sync

Draft PR #55's implementation commit `8769241` builds a pure allowlisted
request for the versioned WorldKernel exchange. Review fix `07c405b`
revalidates the mutable `ScenarioSpec` at the mapping boundary and enforces
the effective minimum of scenario and operator `max_runs`. Regression tests
are `test_mapping_revalidates_mutated_scenario_before_budget_mapping` and
`test_mapping_preserves_lower_scenario_or_operator_run_ceiling`. The walkthrough
explains why unrepresentable scenario timeouts/model/output budgets must be
rejected or enforced by a future adapter. No engine is imported or executed;
B-04 remains open.

The prior integrated #52–#55 candidate `fd72b76` passed 756 tests plus all
five non-pytest gate checks. Merge commit `b9eba02` synchronizes PR #55 with
published PR #54 head `4d22006`, preserving both histories and PR #53's
nested-receipt regressions. Merge commit `b9eba02` and documentation head
`cc9bdb4739507baa55cb857579ef70f7c92430d8` both passed the full local gate.
On exact head `cc9bdb4` at 2026-11-25 04:37:00 UTC, all 756 tests, Ruff,
catalog, atlas, evidence and capability checks passed, with one existing
Starlette/httpx deprecation warning.
Published PR #55 head `56aa92a6920a429b83458380231642fe59feaf08` includes the
review correction and docs sync; its exact gate passed 756 tests plus Ruff,
catalog, atlas, evidence and capability checks at 2026-11-25 04:39:14 UTC.
Its latest Actions checks failed before job steps with the alternative account
annotation under B-08; no remote tests ran. The mapper remains request
construction only; no WorldKernel import or execution is claimed.

## PR #56 disjoint residual calibration

Merge `b9bb86d` integrates PR #53's receipt-parity regressions into PR #56.
Published head `e993391a61a99d63008bc970cb19af673be4c18c` passed the exact
local gate at 2026-11-25 05:02:30 UTC: 700 tests plus Ruff, symbol catalog,
atlas, evidence and capability checks. One existing Starlette/httpx
deprecation warning appeared. Its Actions test [45550857405](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45550857405)
and symbol-catalog [45550857276](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45550857276)
checks failed before job steps with an annotation listing alternative account
conditions; no remote tests ran. This remains experimental and does not prove
empirical calibration. The latest change and exact-head gate are recorded in
the [M1D-01 change request on PR #56](https://github.com/GustavoMFDS/MirrorMind/blob/e993391a61a99d63008bc970cb19af673be4c18c/docs/engineering/changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md).

## PR #58 synthetic policy comparison

PR #58's published head is `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8`.
It includes merge `5544bc0` with PR #55 head `56aa92a` and passed its exact
local gate with 768 tests plus Ruff, catalog, atlas, evidence and capability
checks. The arrival-day/one-day behavior stays an explicit toy-policy caveat;
paired streams and item mass balance remain tested. Actions on `37737c2` failed
before repository steps under B-08, with no job steps or logs. No policy
optimization or WorldKernel execution is claimed; actual engine acceptance
remains B-04.

## PR #57 source-review proposal

Draft PR #57 (`codex/m1b-01-source-review`, published head
`646e4db6991b1769c922cf87a0b85630039915da`) records UCI Online Retail II as a
candidate for narrowly scoped retrospective research and compares a no-download
Census/ALFRED release-vintage method. It distinguishes event time from first
availability, does not derive publication dates from `InvoiceDate`, and adds
no dataset bytes. The review task is decision-ready only as a proposal: source
rights, privacy/minimization, retention, exact scope and temporal-vintage
evidence still require owner/reviewer decisions under B-01/B-02. PR #57 remains
draft and must sync with current PR #53 before its documentation gate.

## PR #59 end-to-end synthetic workflow

The corrected PR #59 code integration commit is
`c000ebd3484e1d9a83f1a440a12369361f4a52b1`, with normal merge commit
`c000ebd` bringing in dependency base `35ecc83` and current PR #56/#58 work.
The review fixes include request-sensitive deterministic identity, versioned
artifact digests, a separate whole-response digest, and propagation of #58's
modeling caveats to affected trace outcomes. The exact integrated head passed
the full local gate: 790 tests, Ruff, symbol catalog, atlas, evidence and
capability checks. One existing Starlette/httpx deprecation warning appeared.
Actions runs [45616226536](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45616226536)
and [45616226367](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45616226367)
failed before repository steps; the connector exposed no steps/logs and did not
return the annotation text. This is not remote test evidence. The route remains
experimental, unauthenticated and without body-size/rate/concurrency controls;
WorldKernel execution and real-source claims remain blocked.

## PR #60 and #61 review state

PR #60's excerpt-integrity correction is published at
`59deef2a780d7802d8b8d29b66dd0189e96365ea`; same-length excerpt tampering and
wrong well-formed digest regressions are present, and its prior exact-head gate
passed 738 tests plus all five other checks. It is based on PR #54 and currently
reports a base conflict; sync to published #54 head `4d22006` and re-gate before
review follow-up. Scope filtering remains caller-declared, not authenticated
RBAC.

PR #61's typed clock-failure correction is published at
`8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e`; expected clock errors produce the
generic bodyless 503 while unexpected programming errors remain visible. The
two regressions distinguish those cases, and the exact-head gate passed 697
tests plus all five other checks. Its current branch is independent of M1 and
reported mergeable; it remains draft for separate review. No HTTP adapter,
persistence, authentication or authority is claimed.

The local M1F dependency stack now integrates published PR #56 head `e993391`
and PR #58 head `37737c2` without cherry-picking their commits. Its merge
candidate `eb6601ddfec7f021a8377b32abda8934fed02640` passed the complete local
gate outside the restricted sandbox: 768 tests, Ruff, symbol catalog, atlas,
evidence and capability checks. This candidate validates the #56 calibration
consumer alongside #58's policy result, but PR #59's workflow consumer still
needs to be merged and gated before the #56 review follow-up is complete. See
[B-07](BLOCKERS.md) for the restricted-run limitation and [B-08](BLOCKERS.md)
for official Actions diagnostics. PRs remain drafts pending separate review
and integration decisions.

## Architecture and actual execution boundaries

| Area | Verified implementation / status | Missing product gate |
| --- | --- | --- |
| API and contracts | [FastAPI app](../../src/mirrormind/api/app.py), [system routes](../../src/mirrormind/api/routes/system.py), [scenario validation](../../src/mirrormind/api/routes/scenarios.py), [typed contracts](../../src/mirrormind/core/contracts.py) | No execution pipeline or tenant authorization implied |
| Evidence and retail staging | [CSV snapshots](../../src/mirrormind/modules/evidence/snapshots.py), [UCI-shaped workbook](../../src/mirrormind/domains/retail/uci_workbook.py), [intake packet](../../src/mirrormind/modules/evidence/intake_review.py), [composite retail preflight](../../src/mirrormind/domains/retail/evidence_flow.py), synthetic coverage/release diagnostics | Real permission, original snapshot/provenance, availability and authorized ingestion |
| Forecasting | [Offline baselines](../../src/mirrormind/modules/forecasting/baselines.py), [retail release backtest](../../src/mirrormind/domains/retail/release_backtest.py), [residual envelope](../../src/mirrormind/domains/retail/residual_envelope.py), selection/drift/sensitivity diagnostics | Locked empirical holdout, evaluated models, calibrated or explicitly limited uncertainty, real inference |
| Governance | [Signed review history](SIGNED_SOURCE_REVIEW.md), [atomic governed publisher](ATOMIC_GOVERNED_PUBLISHER.md), [signed fence](INTEGRATED_HEAD_FENCE.md), [two-witness transcript](INTEGRATED_FENCE_TRANSCRIPT.md), [separate local registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md), [HTTPS reader](REMOTE_FENCE_HEAD_CLIENT.md) | Server-side implementation and operational independence/custody, real source authorization |
| Simulation | [Synthetic retail policy comparison](M1_RETAIL_POLICY_SIMULATION.md), [SimulationGateway](../../src/mirrormind/modules/simulation/gateway.py), and strict pure [WorldKernel request mapping](../../src/mirrormind/modules/simulation/worldkernel_mapping.py) | Actual compatible optional engine adapter, execution, result validation and budgets |
| Decision, orchestration and UI | Experimental synthetic M1F-02 CLI/API workflow and typed trace | Approved-source evaluation, actual engine result, authenticated review, production transport controls, agent/RAG workflow and review interface |
| Operations and generalization | Scaffold Docker/CI and reviewed design | Auth, isolation, durable jobs, runtime limits, observability, recovery, second domain |

### Current governance chain

The combined local SQLite publisher checks current operator policy and
signed publication together. A distinct registry replays full signed
integrated fence transitions with two witnesses. The HTTPS reader
validates a fresh nonce-bound service signature and compares the
claimed head to the registry and publisher. These are experimental
metadata mechanisms; they do not authorize ingestion or forecasting.
The remote signer/server has not been deployed or contacted in
baseline tests. Even a fresh signature over a false old head can be
accepted if local state is rolled back to match. See
[protocol details](REMOTE_FENCE_HEAD_CLIENT.md).

## Evidence interpretation

The most recent known gate was local. Reproduce on the actual commit:

```powershell
Set-Location D:\MirrorMind
git status --short --branch
git log -1 --oneline
$head = (git rev-parse HEAD).Trim()
uv run --no-sync --extra dev python scripts/local_quality_gate.py --expected-head $head --receipt (Join-Path $env:TEMP "mirrormind-$($head.Substring(0,12))-quality.json")
```

For an isolated worktree, use its own correctly bound environment and
working directory; never import the canonical checkout by accident.
The [local gate guide](LOCAL_QUALITY_GATE.md) explains what it checks.
If the environment is missing, follow the setup in [README](../../README.md)
and record any dependency changes; do not silently commit generated
lockfiles or reuse an editable environment bound to another worktree.

## What is next

The [master plan](MASTER_EXECUTION_PLAN.md) and
[task backlog](TASK_BACKLOG.md) are the actionable sequence.
The [blocker register](BLOCKERS.md) explains why external source,
infrastructure and empirical claims remain gated. The
[definition of done](DEFINITION_OF_DONE.md) defines closure rather
than assigning a speculative percentage.

After a material change, update this baseline only using the
actual reviewed commit and verification. Distinguish branch-local
evidence, merged-main evidence, actual remote CI and deployment
evidence. Record outstanding work instead of declaring the product
finished because test counts increased.
