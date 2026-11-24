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
| B-07 | Restricted-sandbox pytest timeout observed on PR #52 implementation SHA `c51ab30370db47e9f7105c97f870008e4fc442c5` and again during the current M1E-03 combined command (which did not complete in 35 seconds after the focused tests). Later unrestricted exact canonical gates passed on `c51ab303...` (696 tests) and PR #53 head `210f0f382938a67e518df688cc4e19c03d3d7af6` (700 tests including API); the separate current API suite passed 6 tests. Root cause remains unknown; no application defect is inferred. | Use the approved unrestricted local execution for the exact canonical gate; keep restricted timeout evidence distinct | Environment / test runner | Do not infer the cause or generalize the workaround beyond executed commands and tested SHAs. |
| B-08 | Official Actions jobs failed before repository steps on the inspected draft heads: PR #52 `5c307e426c43aee4179e3257d7d367214e8c3a63` (`test` [45319452833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452833), `symbol-catalog` [45319452852](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452852)); PR #53 `210f0f382938a67e518df688cc4e19c03d3d7af6` ([45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471), [45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864)); PR #54 `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029` ([45326329041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329041), [45326329150](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329150)); PR #55 `fcd478130c26c653d0d1d9f4d2f905bf24eaf3a9` ([45340088124](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45340088124), [45340088189](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45340088189)); PR #56 `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0` ([45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246), [45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153)); PR #57 `646e4db6991b1769c922cf87a0b85630039915da` ([45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005), [45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950)); and PR #58 code head `09d047b431cc4c50fb6d1abdb88a494a4c7f6f7f` (`test` [45440111223](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45440111223), `symbol-catalog` [45440111132](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45440111132)). For the inspected PR #58 checks, diagnostics state the job was not started because recent account payments failed or the spending limit needs to be increased; no repository job steps ran. | Repository/account owner resolves GitHub billing or spending limit, then reruns checks for reviewed heads | GitHub account owner / billing administrator | Keep draft PRs and local evidence current; do not claim remote CI passed or alter protections |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

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
