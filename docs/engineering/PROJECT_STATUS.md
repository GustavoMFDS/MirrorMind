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

## Live branch reconciliation — 2026-11-24

`git fetch origin main` confirmed that local `main` and `origin/main` both
point to `e4f05a152aefcf68fa8ec22f3baa3b61adb8519d`. The working checkout was
clean on `codex/m2-01-permission-filtered-retrieval` at
`e151f9d9925d83d2b3e27fb88683672a93b48c30` before this documentation
follow-up. GitHub's open-PR listing showed PRs #52–#60 open and in draft;
none is a merged-main delivery.

| PR / task | Current head and verified local evidence | Actual boundary / remaining gate |
| --- | --- | --- |
| [#52 / M1B-02](https://github.com/GustavoMFDS/MirrorMind/pull/52) | Current docs head `5c307e426c43aee4179e3257d7d367214e8c3a63`; implementation SHA `c51ab30370db47e9f7105c97f870008e4fc442c5` passed the exact canonical gate with 696 tests, including API integration. The latest docs-only head has not had its own exact-head gate. | Synthetic local evidence composition only. B-01/B-02 still prevent real-source ingestion/evaluation; current official Actions failures are B-08. |
| [#53 / M1C-01](https://github.com/GustavoMFDS/MirrorMind/pull/53) | Current head `210f0f382938a67e518df688cc4e19c03d3d7af6` passed the exact canonical gate with 700 tests, including API integration, and all six local stages. | Fictional release-aware evaluation only; two fixed baselines share eligible origins. No empirical skill claim. |
| [#54 / M1F-01](https://github.com/GustavoMFDS/MirrorMind/pull/54) | Current head `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029` passed the exact canonical gate with 712 tests and all six stages. | Interface-only decision-trace contract; no producer or decision execution. |
| [#55 / M1E-01](https://github.com/GustavoMFDS/MirrorMind/pull/55) | Current docs head `fcd478130c26c653d0d1d9f4d2f905bf24eaf3a9`; canonical gate on tested docs head `2330dc50a49bb80abc601b0635e5e7d4916ee283` passed 737 tests; later docs-only guards passed. | Strict WorldKernel request mapping only. B-04 still gates a compatible, registered runtime and actual result validation. |
| [#56 / M1D-01](https://github.com/GustavoMFDS/MirrorMind/pull/56) | Current docs head `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0`; canonical gate on tested head `0c2e789256e381c2790c49a14c2acc7802d11b9d` passed 700 tests. Latest docs-only checks are recorded in the PR. | Synthetic calibration/holdout separation only; B-02 still blocks empirical calibration evidence. |
| [#57 / M1B-01](https://github.com/GustavoMFDS/MirrorMind/pull/57) | Current docs head `646e4db6991b1769c922cf87a0b85630039915da`; catalog, atlas, evidence, capability and diff checks passed. No source code changed, so no software tests were run. | Source review is complete as a review task only. UCI remains a candidate; no dataset approval, download or ingestion. |
| [#58 / M1E-03](https://github.com/GustavoMFDS/MirrorMind/pull/58) | Current docs head `465a2f2c46fb6484aa2f0abea7920953ca4f0d00`; implementation SHA `09d047b431cc4c50fb6d1abdb88a494a4c7f6f7f` passed the exact canonical gate with 747 tests and all six stages; docs-only guards passed on the current head. | Fictional paired-policy test double; no WorldKernel execution or actual policy ranking. B-04 remains. |
| [#59 / M1F-02](https://github.com/GustavoMFDS/MirrorMind/pull/59) | Current head `a5951e49a78796908ecd1975c65052b5a2548cd7` passed the exact canonical gate with 766 tests and all six stages; 46 focused workflow/API/CLI tests passed. | Runnable synthetic workflow with explicit abstention, trace and no-write boundaries. Simulation invokes only the local policy test double; actual engine and reviewed-data gates remain. |
| [#60 / M2-01](https://github.com/GustavoMFDS/MirrorMind/pull/60) | Implementation head `e151f9d9925d83d2b3e27fb88683672a93b48c30` passed the exact canonical gate: 720 tests, Ruff, catalog, atlas, evidence and capability checks. The suite includes live HTTP capability parity. | Fictional in-memory retrieval remains experimental; PR is draft. Actions runs 45469182956 and 45469183025 failed before job steps under B-08, so no official CI result exists. |

The earlier sandbox asyncio socket-pair stall is now a historical environment
symptom: exact canonical gates passed on the cited PR #52, #53, #54, #55,
#58, #59 and #60 heads using the approved execution environment; PR #56's
tested code/doc head also passed its full gate, while the latest docs-only
follow-up received its applicable checks. This does not prove the original
root cause. B-08 remains external and prevents official CI execution; it
does not invalidate the recorded local results.

M1 is not complete. Real-source rights and availability (B-01/B-02) and an
actual compatible WorldKernel runtime (B-04) remain open. The existing PR
stack delivers substantial synthetic and contract slices, but those slices
must not be presented as an approved-data or real-engine decision workflow.

PR #54's independent review corrections are now included in the dependency
branch at `2794abff855665fb65f32af655415c52dde68872`. Commit
`f02459d977fd263b03ddf60264b9069ae08b189b` rejects terminal reviews dated
before trace creation, uses context-independent lossless Decimal hashing, and
bounds record sections and references. Its exact-head local gate passed 728
tests and all six stages. Tests and digest checks remain local contract
evidence only: references and reviewer identity are caller assertions, and no
producer, storage, action execution or authenticated approval is provided.
PR #54 remains draft; official CI is tracked separately under B-08.

## Current PR review reconciliation — 2026-11-25

All ten independent review submissions for PRs #52–#61 were re-read. Each is
a top-level `COMMENTED` review; no inline review thread was returned. All ten
PRs remain open drafts. The table below distinguishes implemented corrections
and local evidence from unresolved gates; no merge or ready-for-review action
was taken.

| PR | Review finding and state | Local evidence / remaining boundary |
| --- | --- | --- |
| [#52](https://github.com/GustavoMFDS/MirrorMind/pull/52) | Preserve aggregate-receipt mismatch, missing/late-history and no-authorization regressions; exercise optional extras. No review correction was requested. | Implementation SHA `c51ab30` passed 696 tests; latest docs head `5c307e4` still needs its own exact-head gate. B-01/B-02 block real ingestion. |
| [#53](https://github.com/GustavoMFDS/MirrorMind/pull/53) | Preserve mismatched cutoffs, late feature/target releases, full abstention and provenance limits. | Exact head `210f0f3` passed 700 tests and all six local gate stages; results remain fictional. |
| [#54](https://github.com/GustavoMFDS/MirrorMind/pull/54) | Correct terminal-review chronology, Decimal-context hashing and bounded records/references. | Current head `2794abf` passed 728 tests and all six stages. Its current Actions checks carry an explicit pre-job account annotation; no remote tests ran. Contract remains interface-only. |
| [#55](https://github.com/GustavoMFDS/MirrorMind/pull/55) | Revalidate mutable scenario data and apply the lower scenario/operator run ceiling; retain unsupported-budget limits. | Integrated head `b292db0` passed 756 tests and the full local gate. Mapping is pure; B-04 still blocks actual WorldKernel execution. |
| [#56](https://github.com/GustavoMFDS/MirrorMind/pull/56) | Preserve fixed disjoint calibration semantics, independent oracle, release, empty-calibration and holdout-perturbation tests. | Tested integrated head `0c2e789` passed 700 tests; later docs-only state has guards recorded in the PR. No empirical calibration claim. |
| [#57](https://github.com/GustavoMFDS/MirrorMind/pull/57) | Keep UCI as a source candidate only; rights, privacy, vintages and owner scope remain unresolved. | Documentation review only; no dataset was downloaded or approved. B-01/B-02 remain open. |
| [#58](https://github.com/GustavoMFDS/MirrorMind/pull/58) | Preserve the arrival-day/one-day toy-policy caveat and disclose it in downstream comparison/trace. | Boundary, mass-balance and paired-stream tests remain. #59 binds the caveat into typed trace assumptions; the #59 integrated gate covers this path. No optimized policy or engine result is claimed. |
| [#59](https://github.com/GustavoMFDS/MirrorMind/pull/59) | Correct request-sensitive identity, full-result binding, #58 caveat propagation and explicit exposure limits. | Current head `afce53a` passed 790 tests and all six local stages. Its exact Actions checks fail before steps with the account payment-or-spending-limit annotation; the specific account condition is unknown. |
| [#60](https://github.com/GustavoMFDS/MirrorMind/pull/60) | Reject deserialized excerpts whose exact UTF-8 SHA-256 does not match; preserve caller-declared scope and trusted build-time duplicate invariant. | Two regressions reproduced the defect; after the fix the focused retrieval suite passed 9 tests. Latest #54 base was merged normally. Full integrated gate and publication remain pending. |
| [#61](https://github.com/GustavoMFDS/MirrorMind/pull/61) | Convert typed operational clock/store failures to generic service failure while preserving programming errors. | Review correction and failing-clock regression remain pending on head `288021f`; no persistence or transport expansion is proposed. |

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
