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
changed. The published integrated candidate `1ecd3acbbebe0473f9d03ac0ee6688a0e4a95401`
passed the complete local gate at 2026-11-25 04:21:50 UTC: 728 tests, Ruff,
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
candidate as recorded above. On published head `1ecd3ac`, Actions test runs
[45546319379](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546319379)
and [45546314259](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546314259)
and symbol-catalog runs [45546319380](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546319380)
and [45546314591](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546314591)
failed before repository steps. Their annotation names failed recent account
payments or a spending limit increase as alternatives; it does not identify
which applies. No code tests ran remotely. See [B-08](BLOCKERS.md).

## PR #60 and #61 review state

### M2-01 permission-filtered retrieval

Draft PR #60 retains the correction from `73c191050865b0865e582f31a78859cc24262efb`:
the result contract hashes the exact UTF-8 excerpt, and regression tests reject
same-length excerpt tampering and a wrong well-formed digest. The branch was
normally merged with the latest published PR #54 head `4d220066` at
`a3a342450b3aa72b69d10b52485175ca497ffd5d`. That merge's first full local
gate exposed one documentation inventory failure after shared status pages
from unrelated PR #55–#59 work were selected; 737 tests passed and
`tests/unit/test_docs_coverage.py::test_live_repository_passes_linked_inventory`
reported two absent M1E links. The shared pages have been restored to PR #54's
dependency scope. The exact corrected integration head
`d1d4f74d69a3d4e772ba3eeb3119493491921875` passed the complete local gate:
738 tests, Ruff, catalog, atlas, evidence and capability checks. One existing
Starlette/httpx TestClient deprecation warning appeared. The initial failure
and correction are both retained here; neither retrieval code nor verifiers
were changed to address the documentation mismatch. Local validation does not
resolve official Actions B-08.

The documentation-only evidence follow-up at published head
`5b0a026cc008bffb953b3a6ae7d3cbdd252bd161` was also gated exactly: 738 tests,
Ruff, catalog, atlas, evidence and capability checks passed with the same
existing warning. See the [retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md)
and [change request](changes/M2_01_PERMISSION_FILTERED_EVIDENCE_RETRIEVAL.md).
The corresponding Actions checks failed before repository steps; their exact
annotation text was not exposed, so this is not CI success or an account-cause
finding.

The scope filter is caller-declared, not authenticated RBAC. The digest binds
the excerpt bytes but does not authenticate the source snapshot or prove
absolute offsets without source bytes. Retrieval remains local, fictional and
experimental; no HTTP route or model call is exposed.

### G-01 current-head service

Draft PR #61's typed clock-failure correction is published at
`8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e`. Expected operational clock errors
produce the generic bodyless 503; unexpected programming errors remain
visible. The regressions distinguish those cases, and the exact-head gate
passed 697 tests plus Ruff, catalog, atlas, evidence and capability checks.
The branch is independent of M1 and remains draft for separate review. No HTTP
adapter, persistence, authentication or authority is claimed.

## Architecture and actual execution boundaries

| Area | Verified implementation / status | Missing product gate |
| --- | --- | --- |
| API and contracts | [FastAPI app](../../src/mirrormind/api/app.py), [system routes](../../src/mirrormind/api/routes/system.py), [scenario validation](../../src/mirrormind/api/routes/scenarios.py), [typed contracts](../../src/mirrormind/core/contracts.py) | No execution pipeline or tenant authorization implied |
| Evidence and retail staging | [CSV snapshots](../../src/mirrormind/modules/evidence/snapshots.py), [UCI-shaped workbook](../../src/mirrormind/domains/retail/uci_workbook.py), [intake packet](../../src/mirrormind/modules/evidence/intake_review.py), [composite retail preflight](../../src/mirrormind/domains/retail/evidence_flow.py), synthetic coverage/release diagnostics | Real permission, original snapshot/provenance, availability and authorized ingestion |
| Forecasting | [Offline baselines](../../src/mirrormind/modules/forecasting/baselines.py), [retail release backtest](../../src/mirrormind/domains/retail/release_backtest.py), [residual envelope](../../src/mirrormind/domains/retail/residual_envelope.py), selection/drift/sensitivity diagnostics | Locked empirical holdout, evaluated models, calibrated or explicitly limited uncertainty, real inference |
| Governance | [Signed review history](SIGNED_SOURCE_REVIEW.md), [atomic governed publisher](ATOMIC_GOVERNED_PUBLISHER.md), [signed fence](INTEGRATED_HEAD_FENCE.md), [two-witness transcript](INTEGRATED_FENCE_TRANSCRIPT.md), [separate local registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md), [HTTPS reader](REMOTE_FENCE_HEAD_CLIENT.md) | Server-side implementation and operational independence/custody, real source authorization |
| Simulation | [SimulationGateway](../../src/mirrormind/modules/simulation/gateway.py) protocol/summary | Actual compatible optional engine adapter, execution, result validation and budgets |
| Decision, orchestration and UI | Design and review templates | Executable comparison, agent/RAG workflow, review interface |
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
