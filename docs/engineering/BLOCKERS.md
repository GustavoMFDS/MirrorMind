# Blocker and decision register

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | Real source rights: M5 unresolved; UCI CC BY 4.0 preliminary review, not ingestion approval | Original license/terms, intended use/distribution/attribution, privacy/minimization and retention review, accepted dataset card and source approval | Project owner / appropriate rights reviewer | Review official evidence, compare alternate sources, implement bounded fictional fixtures and adapters |
| B-02 | Historical availability and empirical evaluation | Verified source vintages/revisions or explicitly justified evaluation scope, immutable snapshot, locked split and approved data; never substitute transaction/event timestamp for first availability | Evidence/model reviewer | Synthetic delay, missingness, leakage and holdout regressions; prepare evaluation protocol |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | Optional WorldKernel runtime acceptance | Pinned supported version, actual engine/result schema, approved world mapping, trusted local fixture and resource caps; separate repo owner approval for cross-repo changes | Project owner / engine maintainer | Strict pure mapping, fake gateway tests and disabled-engine paths; no hard dependency or invented engine result |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-08 | Latest observed PR-triggered `test` and `symbol-catalog` runs for every open draft #52–#61 completed with failure; exact run IDs are listed below. PR #57's description records a verified billing/spending-limit annotation on its own earlier runs. That makes a shared Actions billing limit plausible, but does not establish the cause of other runs. On the latest inspected #61 head, both jobs failed without step records; logs returned `404 BlobNotFound`, and artifacts/statuses were empty. | Successful required workflows on the exact reviewed head, or inspectable diagnostics and a verified resolution; local gates are not a substitute | Project owner / repository or Actions administrator | Preserve local exact-head receipts, continue tests and documentation gates, keep PRs draft and report Actions status as failed |
| B-09 | Integration of the current review queue: PRs #52–#61 are open drafts and unmerged as of 2026-11-24. Dependent tasks cannot be promoted based on local implementation or tests alone. PR #60 also has the separate failed-workflow evidence in B-08. | Human review and integration decisions for prerequisite PRs; independently inspect required Actions outcomes where workflows run; then reconcile task dependencies against merged heads | Project owner / repository reviewers | Continue genuinely independent ready work, preserve the draft branches and evidence, and do not duplicate slices or assume dependency completion |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## B-08 — latest observed workflow runs

Both configured pull-request workflows completed with failure on the
following pinned heads. These are official Actions results, separate from
local quality-gate receipts.

| PR / head | Python API CI (`test`) | Engineering documentation catalog (`symbol-catalog`) |
| --- | --- | --- |
| [#52](https://github.com/GustavoMFDS/MirrorMind/pull/52), `5c307e4` | [45319452833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452833) failed | [45319452852](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452852) failed |
| [#53](https://github.com/GustavoMFDS/MirrorMind/pull/53), `210f0f3` | [45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471) failed | [45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864) failed |
| [#54](https://github.com/GustavoMFDS/MirrorMind/pull/54), `83c80d8` | [45326329041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329041) failed | [45326329150](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329150) failed |
| [#55](https://github.com/GustavoMFDS/MirrorMind/pull/55), `fcd4781` | [45340088124](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45340088124) failed | [45340088189](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45340088189) failed |
| [#56](https://github.com/GustavoMFDS/MirrorMind/pull/56), `c33bd7d` | [45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246) failed | [45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153) failed |
| [#57](https://github.com/GustavoMFDS/MirrorMind/pull/57), `646e4db` | [45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005) failed | [45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950) failed |
| [#58](https://github.com/GustavoMFDS/MirrorMind/pull/58), `465a2f2` | [45447930415](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930415) failed | [45447930394](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930394) failed |
| [#59](https://github.com/GustavoMFDS/MirrorMind/pull/59), `a5951e4` | [45460098823](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098823) failed | [45460098802](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098802) failed |
| [#60](https://github.com/GustavoMFDS/MirrorMind/pull/60), `6374f0b` | [45476173796](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173796) failed | [45476173736](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173736) failed |
| [#61](https://github.com/GustavoMFDS/MirrorMind/pull/61), `7d9282d` | [45494216240](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45494216240) failed | [45494216188](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45494216188) failed |

PR #57's body records a verified billing/spending-limit annotation for its
own listed runs and says repository CI steps did not execute. Treat shared
billing as a hypothesis for other PRs: #61 runs on head `7d9282d` also failed
without step records; log downloads return `404 BlobNotFound`, and
artifact/combined-status queries are empty. The connector could not expose a
root-cause annotation.

## Source references and precise restrictions

- [M5 review](datasets/M5_ACCESS_REVIEW.md) documents an unresolved
  permission grant. Public accessibility is not permission.
- [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
  records the official license statement and unresolved privacy,
  historical availability, scope and source snapshot issues.
- [Data card](DATASET_CARD_TEMPLATE.md) and [model card](FORECAST_MODEL_CARD_TEMPLATE.md)
  require evidence before empirical or licensed-ingestion claims.
- [Remote head reader](REMOTE_FENCE_HEAD_CLIENT.md) authenticates a
  configured signer's reply, not independent truth. A service can
  freshly sign stale state; separately protected storage/keys and
  operational review are distinct from local code acceptance.
- [PR #60](https://github.com/GustavoMFDS/MirrorMind/pull/60) and
  [PR #61](https://github.com/GustavoMFDS/MirrorMind/pull/61) remain drafts;
  see the pinned B-08 run table. Current #61 diagnostics do not prove an
  account-level cause or a source-code failure.
- [Gateway gate](WORLDKERNEL_GATEWAY_GATE.md) rejects unrepresentable
  fields; a simulated result must actually come from the named engine.
- [Security expectations](../SECURITY.md) and [decision log](../DECISIONS.md)
  preserve explicit human approval and separate release decisions.

## Reporting and escalation

When a blocker is encountered:

1. Identify the blocked task ID, exact failed precondition and
   observed evidence. Distinguish a reproducible failure from a
   hypothesis, a missing credential or an unreviewed assumption.
2. Record what is needed, the responsible decision-maker and
   the next safe independent task. Do not copy credentials or
   private records into issues, docs or logs.
3. Escalate only the decision that genuinely requires the owner.
   No approval requests for routine reversible implementation.
4. Continue on unblocked work; do not weaken verification, fabricate
   evidence, expand permissions or change the acceptance gate.
5. On resolution, link the actual review/decision, version and
   date, and rerun the affected acceptance checks. Record whether
   resolution applies only to synthetic/test use or also real use.

Local gate receipts and official CI are separate. A transient CI
outage is an additional task-specific verification blocker, not
permission to mark remote checks green. Record such cases with the
actual PR/SHA and observed check state.

## Decision record template

- Blocker / task ID:
- Current condition and evidence:
- Proposed safe resolution and alternatives:
- Required reviewer / external dependency:
- Scope explicitly allowed or denied:
- Remaining independent work:
- Actual reviewed decision / commit / PR / date:
- Revalidation and status:

Keep approved architectural decisions in [DECISIONS](../DECISIONS.md);
do not duplicate or prematurely approve them here.
