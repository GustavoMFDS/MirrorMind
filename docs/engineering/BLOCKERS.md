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
| B-07 (historical exact SHA) | Resolved for current PR #56 stack by the canonical local gate on docs head `aa2be84ba135ac93cf75b8f0491318d19757f693`: 700 tests passed including `tests/integration/test_api.py`; standalone `test_health` also passed outside the restricted sandbox. Historical PR #52 SHA `c51ab30370db47e9f7105c97f870008e4fc442c5` timed out at the 900-second pytest limit after verbose replay stopped at `tests/integration/test_api.py::test_health`; standalone loop creation blocked in `socket.accept` inside Python's `_fallback_socketpair` on Python 3.13.5 and installed Python 3.12. This was before the application handler. A sandbox/host loopback restriction remains a hypothesis, not a proven root cause. The historical exact SHA has not been rerun. | No action blocks the current stack; rerun the exact historical SHA only if its standalone status is needed | Codex execution environment / project maintainer | Keep the current passing full-gate result and historical timeout distinct; do not generalize the current pass to the old SHA or change application behavior to hide the host issue. |
| B-08 | Official checks on PRs #52–#55 repeatedly failed before job execution with annotations stating recent account payments failed or the spending limit needs to be increased. PR #53 code head `10ee6866f3340c679e0bfe3bfee11e199a32b56a`: `test` [45322594833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45322594833), `symbol-catalog` [45322594817](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45322594817); docs head `210f0f382938a67e518df688cc4e19c03d3d7af6`: [45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471), [45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864). PR #54 code/docs heads `27f1f1c9dec3886299077793a2d42a647313d7ae` / `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029`: runs [45326109821](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109821), [45326109808](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109808), [45326329041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329041), [45326329150](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329150). PR #55 code/docs heads `87692412606e65b5e1500164b2c8708bb98cf120` / `2330dc50a49bb80abc601b0635e5e7d4916ee283`: runs [45329990098](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45329990098), [45329990164](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45329990164), [45330280291](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45330280291), [45330280468](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45330280468). These prior runs carry the same billing/spending-limit annotation. On PR #56 implementation head `10fe58fc3aca45c27288dcc6055ac5d84ab035af`, `test` [45334623041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45334623041) and `symbol-catalog` [45334623086](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45334623086); latest docs head `aa2be84ba135ac93cf75b8f0491318d19757f693`, `test` [45335148902](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148902) and `symbol-catalog` [45335148877](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148877), all failed with zero job steps. The connector exposed no cause annotation for either PR #56 head, so the specific billing cause is not independently re-confirmed there. No official repository check executed on these heads. | Repository/account owner resolves GitHub billing or spending limit, then reruns checks for the reviewed heads | GitHub account owner / billing administrator | Keep draft PRs and local evidence current; do not claim remote CI passed or alter protections |

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
