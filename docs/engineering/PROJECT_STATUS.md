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

On current published head `b431d11`, the `test` and `symbol-catalog` Actions
runs failed, but their job summaries expose no steps or logs and their specific
cause was not recovered. On prior published head `e3aedaf`, an exact annotation
listed failed recent account payments or an increased spending limit as
alternatives without identifying which condition applied. See [B-08](BLOCKERS.md),
[current test run](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863564)
and [current symbol-catalog run](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863839).
The local pass does not substitute for official CI.

PR #53 is on `codex/m1c-01-synthetic-retail-evaluation`, stacked on PR #52.
Merge commit `e922b03` synchronizes it with PR #52 head `b431d11`; its current
published head is `79d3679013576c6a209bed9fa031b7f0fabd0d8d`. The PR remains a
draft and unmerged. Its experimental evaluator composes the staged synthetic
evidence flow with release-aware matched-origin baselines and a deterministic
fictional CLI; it adds no real-data ingestion or HTTP forecast endpoint. The
exact-head gate passed 700 tests, Ruff, catalog, atlas, evidence and capability
checks at 2026-11-25 04:08:00 UTC. API tests ran; one existing Starlette/httpx
deprecation warning appeared. The added regression assertions keep the outer
result and nested evidence receipt unverified, unauthorized and not forecast
eligible. Actions runs [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354)
and [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397)
failed without job steps/logs and without a recovered specific cause. B-01/B-02
still gate real data and empirical evaluation; B-08 blocks official CI.

M1F-01 has a versioned interface-only decision-trace contract in draft
[PR #54](https://github.com/GustavoMFDS/MirrorMind/pull/54), stacked on PR #53.
Merge commit `e493b4c` synchronizes it with published PR #53 head `79d3679`.
Review fix `f02459d` compares review chronology as timezone-aware instants,
hashes Decimal values losslessly across contexts, bounds collections and
indexes references. The published integrated head `4d22006` passed 728 tests
plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25
04:25:37 UTC. Its latest inspected Actions failed before repository steps with
the unresolved account annotation in B-08. The contract remains interface-only;
decision evaluation is not implemented.

M1E-01 has a pure strict request mapper in draft
[PR #55](https://github.com/GustavoMFDS/MirrorMind/pull/55), stacked on #54.
The published head `56aa92a` includes review fix `07c405b` for post-validation
scenario mutation and the effective minimum of scenario/operator run limits.
Merge `b9eba02` syncs it with PR #54 head `4d22006`; its full gate passed 756
tests and all five other checks at 2026-11-25 04:39:14 UTC. The latest Actions
failed before repository steps with the unresolved account annotation under
B-08. The mapper constructs a request only; B-04 still blocks a pinned SDK
and actual registered-world run.

M1D-01 is implemented in `10fe58fc3aca45c27288dcc6055ac5d84ab035af` on
`codex/m1d-01-disjoint-residual-calibration` and proposed in draft
[PR #56](https://github.com/GustavoMFDS/MirrorMind/pull/56), based on PR #53.
It uses fixed pre-holdout calibration dates and explicit disjoint-window
metadata; the late-release regression proves a published earlier holdout
target cannot refill calibration. On prior tested docs head `0c2e789`, 81
focused residual tests, 94 dependent consumer tests and the canonical full gate
passed. Merge commit `b9bb86d` integrates PR #53's receipt-parity regressions
and passed the exact-head canonical gate: 700 tests including API, Ruff,
catalog, atlas, evidence and capability checks at 2026-11-25 04:52:39 UTC.
Pytest reported one existing Starlette/httpx deprecation warning. The latest
published pre-sync head remains `c33bd7d`; its test run
[45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246)
and symbol-catalog run
[45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153)
failed. Diagnostics on the test check report that recent account payments
failed or the spending limit needs to be increased, without distinguishing the
condition; no repository tests ran remotely. This remains experimental and
does not establish empirical calibration. Official checks for the newly
integrated head remain pending publication and inspection.
See [TASK_BACKLOG](TASK_BACKLOG.md) and the
[M1D-01 change request](changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md).

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
