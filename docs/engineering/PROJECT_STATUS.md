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

## Active branch evidence — 2026-11-24

The composed synthetic evidence flow is implemented at
`c51ab30370db47e9f7105c97f870008e4fc442c5` on
`codex/m1b-02-synthetic-evidence-flow` and is proposed in draft
[PR #52](https://github.com/GustavoMFDS/MirrorMind/pull/52). The PR is
unmerged. Its one new capability is experimental and uses only bounded
local fixtures and caller-declared dates.

Local evidence on that implementation commit: all five focused M1B-02
integration tests passed; 690 tests passed when the entire API integration
module was excluded; and a direct call to the registered capability handler
matched the ledger's implemented, experimental and planned IDs. Ruff and
the catalog, atlas, evidence and capability guards passed. The exact-commit
gate did not pass: pytest exited 124 at its 900-second timeout, before the
other gate stages. Verbose pytest stopped at `test_health`; the request
blocked while asyncio created its local socket pair, before the API handler
ran. The same socket-pair block reproduced with Python 3.12 and 3.13.5. A
host/sandbox loopback restriction is a hypothesis; the root cause is not
confirmed. See [B-07](BLOCKERS.md).

GitHub Actions has no test result for this SHA. Both `test` and
`symbol-catalog` checks failed before their jobs started, with annotations
stating that recent account payments failed or the spending limit needs to
be increased. See [B-08](BLOCKERS.md), [test run](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45318084072)
and [symbol-catalog run](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45318084108).
Do not treat the green local subset as a substitute for the complete gate
or official CI.

The next stacked slice is on `codex/m1c-01-synthetic-retail-evaluation`
at `10ee6866f3340c679e0bfe3bfee11e199a32b56a` and is proposed as draft
[PR #53](https://github.com/GustavoMFDS/MirrorMind/pull/53), based on
PR #52's branch. It composes the staged synthetic evidence flow with the
existing release-aware baseline evaluator and exposes a deterministic
fictional evaluation CLI. This is branch-local and experimental; it does
not add real-data ingestion, an HTTP forecast endpoint or predictive-skill
evidence. Four focused integration tests and six existing retail-backtest
unit tests passed together; 694 tests passed when excluding
`tests/integration/test_api.py`. Ruff for `src`, `tests` and the new example,
the symbol catalog, atlas, evidence and capability guards passed locally.
A direct registered capability-handler/ledger comparison passed, but HTTP
runtime did not run. The full exact-head local gate was not completed due the
previously reproduced B-07 host-side asyncio socket-pair hang. On its latest
documentation head `210f0f382938a67e518df688cc4e19c03d3d7af6`, GitHub Actions
`test` run [45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471)
and `symbol-catalog` run [45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864)
failed before job execution with the account payment/spending-limit
annotation (B-08). Neither local nor remote full-gate success is claimed.

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
changed. The full integrated gate is pending. HTTP runtime was not tested and
no new route was added. The result digest remains a recomputable content hash,
not a signature; all source/model/engine references remain caller assertions.
The task remains interface-only and has no authenticated producer, storage,
decision ranking, execution permission or real engine evidence. The source
walkthrough is in [DECISION_TRACE_RESULT](DECISION_TRACE_RESULT.md). PR #54
remains a draft stacked on #53. Its prior head's GitHub checks failed before
job start with B-08; no official check has yet been inspected for this new
commit.

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
