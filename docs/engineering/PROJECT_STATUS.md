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
evidence, cost measurement states and human review. Twelve focused tests and
the deterministic fictional CLI pass; 706 tests pass when
`tests/integration/test_api.py` is excluded. Ruff, symbol catalog, atlas,
evidence and capability guards pass locally, as does a direct registered
capability-handler/ledger comparison. HTTP runtime was not tested and no new
route was added. The result digest is content binding, not a signature; all
source/model/engine references remain caller assertions. The task remains
interface-only and has no trace producer, storage, decision ranking,
execution permission or real engine evidence. The source and reference
walkthrough are in [DECISION_TRACE_RESULT](DECISION_TRACE_RESULT.md). The
implementation commit is `27f1f1c9dec3886299077793a2d42a647313d7ae` on
`codex/m1f-01-decision-trace-contract`, proposed as draft [PR #54](https://github.com/GustavoMFDS/MirrorMind/pull/54)
stacked on PR #53. Its official `test` run
[45326109821](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109821)
and `symbol-catalog` run
[45326109808](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109808)
failed before job start due the same B-08 account billing annotation. The
later docs head `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029` also failed before
job start on `test` run
[45326329041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329041)
and `symbol-catalog` run
[45326329150](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329150).
Exact-head full local gate remains unverified under B-07; PR remains draft.

The active continuation `codex/m1e-01-worldkernel-mapping` advances M1E-01.
It inspects the separate WorldKernel exchange and adds a pure mapping for
`retail.inventory` `0.1` to `retail.inventory.demo` `demo-1`, with explicit
unit assertions, strict input allowlists and operator-configured request
ceilings. It does not import or execute WorldKernel, so the capability remains
planned and M1E-02 remains gated by B-04. Twenty-five focused tests passed;
the local suite passed 731 tests with `tests/integration/test_api.py` excluded
for B-07. Ruff, catalog, atlas, evidence and capability guards passed, as did
direct capability-handler/ledger parity and a deterministic example replay.
Official CI awaits PR creation and cannot be assumed available under B-08.
See [M1E-01 change request](changes/M1E_01_WORLDKERNEL_REQUEST_MAPPING.md)
and [mapping walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md).

## Architecture and actual execution boundaries

| Area | Verified implementation / status | Missing product gate |
| --- | --- | --- |
| API and contracts | [FastAPI app](../../src/mirrormind/api/app.py), [system routes](../../src/mirrormind/api/routes/system.py), [scenario validation](../../src/mirrormind/api/routes/scenarios.py), [typed contracts](../../src/mirrormind/core/contracts.py) | No execution pipeline or tenant authorization implied |
| Evidence and retail staging | [CSV snapshots](../../src/mirrormind/modules/evidence/snapshots.py), [UCI-shaped workbook](../../src/mirrormind/domains/retail/uci_workbook.py), [intake packet](../../src/mirrormind/modules/evidence/intake_review.py), [composite retail preflight](../../src/mirrormind/domains/retail/evidence_flow.py), synthetic coverage/release diagnostics | Real permission, original snapshot/provenance, availability and authorized ingestion |
| Forecasting | [Offline baselines](../../src/mirrormind/modules/forecasting/baselines.py), [retail release backtest](../../src/mirrormind/domains/retail/release_backtest.py), [residual envelope](../../src/mirrormind/domains/retail/residual_envelope.py), selection/drift/sensitivity diagnostics | Locked empirical holdout, evaluated models, calibrated or explicitly limited uncertainty, real inference |
| Governance | [Signed review history](SIGNED_SOURCE_REVIEW.md), [atomic governed publisher](ATOMIC_GOVERNED_PUBLISHER.md), [signed fence](INTEGRATED_HEAD_FENCE.md), [two-witness transcript](INTEGRATED_FENCE_TRANSCRIPT.md), [separate local registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md), [HTTPS reader](REMOTE_FENCE_HEAD_CLIENT.md) | Server-side implementation and operational independence/custody, real source authorization |
| Simulation | [SimulationGateway](../../src/mirrormind/modules/simulation/gateway.py) Protocol plus [pure WorldKernel mapping](../../src/mirrormind/modules/simulation/worldkernel_mapping.py) | Pinned optional engine adapter, actual execution, result validation and enforced runtime budgets |
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
