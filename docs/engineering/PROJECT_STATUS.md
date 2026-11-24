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
previously reproduced B-07 host-side asyncio socket-pair hang. On this exact
SHA, GitHub Actions `test` run [45322594833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45322594833)
and `symbol-catalog` run [45322594817](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45322594817)
failed before job execution with the account payment/spending-limit
annotation (B-08). Neither local nor remote full-gate success is claimed.

M1F-01 has a versioned interface-only decision-trace contract in draft
[PR #54](https://github.com/GustavoMFDS/MirrorMind/pull/54), based on PR #53.
Its code head `27f1f1c9dec3886299077793a2d42a647313d7ae` passed 12 focused
tests, 706 tests excluding the known API module, Ruff and local documentation
guards. The docs head is `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029`.
Both heads' official checks failed before job execution under B-08. This is a
typed result contract and CLI demonstration; decision evaluation is not
implemented.

M1E-01 has a pure strict request mapper in draft [PR #55](https://github.com/GustavoMFDS/MirrorMind/pull/55),
stacked on PR #54. Source commit is
`87692412606e65b5e1500164b2c8708bb98cf120`; latest docs head is
`2330dc50a49bb80abc601b0635e5e7d4916ee283`. Twenty-five focused tests and
731 tests excluding the API module passed with Ruff and local documentation
guards. Official checks on both heads failed before job execution under
B-08. The mapper does not execute WorldKernel; B-04 remains for a pinned SDK
and actual registered-world run.

M1D-01 is implemented in `10fe58fc3aca45c27288dcc6055ac5d84ab035af` on
`codex/m1d-01-disjoint-residual-calibration` and proposed in draft
[PR #56](https://github.com/GustavoMFDS/MirrorMind/pull/56), based on M1C-01
PR #53. It replaces rolling residual labels with fixed pre-holdout calibration
dates and explicit disjoint-window metadata. The late-release regression
proves that a published earlier holdout target cannot refill calibration.
Local evidence on docs head `aa2be84ba135ac93cf75b8f0491318d19757f693`:
81 focused residual tests, 94 dependent consumer tests, and the canonical
`scripts/local_quality_gate.py --expected-head aa2be84ba135ac93cf75b8f0491318d19757f693`
passed. The full suite reported 700 passed, including
`tests/integration/test_api.py`; Ruff and catalog, atlas, evidence and
capability guards also passed. Pytest emitted one existing Starlette/httpx
deprecation warning. `test_health` and the full gate passed outside the
restricted sandbox, resolving B-07 for this stack; the earlier exact PR #52
SHA has not been rerun. Official `test` run
[45335148902](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148902)
and `symbol-catalog` run
[45335148877](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148877)
failed before job steps, without a returned cause annotation (B-08). This
remains experimental and does not establish empirical calibration. See the
active claim in [TASK_BACKLOG](TASK_BACKLOG.md) and the
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
