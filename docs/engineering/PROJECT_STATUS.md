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

## M1B-01 source and temporal-evaluation decision proposal

Draft PR #57 remains documentation-only. Its [source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
now gives three explicit choices: (A) UCI Online Retail #352 for
privacy-minimized retrospective product-level research, with CC BY attribution
and privacy/retention decisions still pending; (B) official Census MARTS/MRTS
release archives for an aggregate retail vintage study; or (C) FRED/ALFRED
`RSAFS` for machine-readable Census-sourced monthly retail vintages after
reviewing both FRED API terms and series-owner restrictions. M5 remains
no-go. No data, API key or credentials were acquired.

The B-02 proposal separates reference month from publication time, stores
first/revised/annual releases as immutable hash-verified vintages, and at each
origin uses only a release published before the cutoff (next-day when only a
date is available). It pre-registers a chronological split after archive
completeness review, a locked final 24 monthly origins, 1/3/6-month horizons,
seasonal-naive and trailing-mean baselines, matched eligible origins, MAE,
RMSE, zero-safe WAPE, coverage/abstention, and separate first-release versus
final-revision reporting. This is a proposal, not a completed evaluation.
The UCI proposal now specifies an event-time-only one-day product-day study:
fit/cohort through 2011-08-30, validation origins 2011-08-31 through 2011-09-30,
and locked holdout origins 2011-10-01 through 2011-12-08, with frozen product
cohort, same-weekday and trailing-seven-day baselines, identical target pairs,
and explicit missing-target abstention. The output remains positive invoice
units, not latent demand. Because `InvoiceDate` is event time and the catalog
has no row-level first-publication vintages, this retrospective protocol still
cannot satisfy B-02 point-in-time acceptance. B-01/B-02 remain blocked pending
the owner's scope, terms, privacy, retention and dataset-card decisions.

The published documentation-only PR #57 head is now
`25fb95ee84e1e431e206716355acab70448a5a54`, normally merged with its latest
PR #53 base `79d3679013576c6a209bed9fa031b7f0fabd0d8d`. GitHub reports the PR
open, mergeable and draft. Its exact-head local gate passed 700 tests, Ruff,
symbol-catalog, atlas coverage, evidence and capability checks. Official
`test` and `symbol-catalog` runs
[45623569731](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45623569731)
and [45623569774](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45623569774)
failed before any job steps; each check exposes one annotation, but the
annotation payload and job logs were unavailable. Cause is unknown; no billing
or code-failure attribution is supported. See [B-08](BLOCKERS.md). The source
proposal is decision-ready documentation, not source approval, acquisition or
an empirical evaluation. Keep PR #57 in draft for the separate owner/review
decision.

The documentation-only follow-up commit `8f906b8c0735bb04434c2c0a40efc2c3297df93b`
records the latest B-08 evidence. Its exact-head full local gate returned
pytest exit code 124 after the configured 900-second timeout; Ruff and the
documentation checks did not run. The `src/` and `tests/` trees are unchanged
from `25fb95e`, whose exact-head gate passed 700 tests and the five other
checks. A separate verbose diagnostic reached
`tests/integration/test_api.py::test_health` and remained pending for 30
seconds before manual interruption; no stack or cause was established. Treat
this as a current B-07 verification blocker for the follow-up, separate from
the earlier #52 timeout and pass. Do not infer a code regression or a host/
sandbox cause from the timeout alone.

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
Merge commit `e922b03` synchronizes it with PR #52 head `b431d11`; the PR is
still a draft and remains unmerged. The feature composes the staged synthetic
evidence flow with release-aware matched-origin baselines and a deterministic
fictional evaluation CLI. It is experimental and does not add real-data
ingestion, an HTTP forecast endpoint or predictive-skill evidence. The four
integration tests and six existing retail-backtest unit tests passed, including
new assertions for the unverified source status and false authorization and
eligibility flags at outer and nested receipt levels. The exact-head local gate
passed on `1addb7791da42939166c34a2e410737ca97a177b` at 2026-11-25 04:06:26 UTC:
700 tests, Ruff, catalog, atlas, evidence and capability checks. The API tests
ran; one existing Starlette/httpx `TestClient` deprecation warning was emitted.
This is local evidence only. B-01/B-02 still gate real data and empirical
evaluation; B-08 blocks official CI. The earlier B-07 timeout on #52 was
resolved by later full local passes and is not evidence that this integrated
#53 head fails. The synchronized #53 head has not yet been published at this
evidence snapshot.

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
