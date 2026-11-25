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
| B-07 (historical exact SHA) | The previous PR #56 stack passed the canonical local gate on tested docs head `0c2e789256e381c2790c49a14c2acc7802d11b9d`: 700 tests passed including `tests/integration/test_api.py`; standalone `test_health` also passed outside the restricted sandbox. Historical PR #52 SHA `c51ab30370db47e9f7105c97f870008e4fc442c5` timed out at the 900-second pytest limit after verbose replay stopped at `tests/integration/test_api.py::test_health`; standalone loop creation blocked in `socket.accept` inside Python's `_fallback_socketpair` on Python 3.13.5 and installed Python 3.12. This was before the application handler. A sandbox/host loopback restriction remains a hypothesis, not a proven root cause. The historical exact SHA has not been rerun. The current PR #56 merge candidate has not passed its exact-head gate yet. | Re-run the exact historical SHA only if its standalone status is needed; gate the current merge candidate separately | Codex execution environment / project maintainer | Keep the previous passing full-gate result, current candidate and historical timeout distinct; do not generalize results across SHAs or change application behavior to hide the host issue. |
| B-08 | Official checks on PRs #52–#55 repeatedly failed before job execution with annotations stating either recent account payments failed or the spending limit needs to be increased. PR #53 code head `10ee6866f3340c679e0bfe3bfee11e199a32b56a`: `test` [45322594833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45322594833), `symbol-catalog` [45322594817](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45322594817); docs head `210f0f382938a67e518df688cc4e19c03d3d7af6`: [45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471), [45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864). PR #54 code/docs heads `27f1f1c9dec3886299077793a2d42a647313d7ae` / `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029`: runs [45326109821](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109821), [45326109808](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109808), [45326329041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329041), [45326329150](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326329150). PR #55 code/docs heads `87692412606e65b5e1500164b2c8708bb98cf120` / `2330dc50a49bb80abc601b0635e5e7d4916ee283`: runs [45329990098](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45329990098), [45329990164](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45329990164), [45330280291](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45330280291), [45330280468](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45330280468). These prior runs carry the same alternative pre-job annotation. On PR #56 implementation head `10fe58fc3aca45c27288dcc6055ac5d84ab035af`, `test` [45334623041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45334623041) and `symbol-catalog` [45334623086](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45334623086); latest docs head `aa2be84ba135ac93cf75b8f0491318d19757f693`, `test` [45335148902](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148902) and `symbol-catalog` [45335148877](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45335148877), all failed with zero job steps. The connector exposed no cause annotation for the 10fe58f or aa2be84 heads. On tested docs head `0c2e789256e381c2790c49a14c2acc7802d11b9d`, `test` run [45336376803](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45336376803) and `symbol-catalog` run [45336376776](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45336376776) failed before job steps; both expose the same alternative annotation. No repository check executed on those runs, and the cause remains unestablished. | Repository/account owner investigates the exact pre-job condition in GitHub, then reruns checks for the reviewed heads | GitHub account owner / repository administrator | Keep draft PRs and local evidence current; do not claim official CI passed or alter protections |

### B-08 current diagnostics and runner assessment — 2026-11-25

The published exact heads last inspected for this queue were #52 `b431d11`,
#53 `79d3679`, #54 `4d22006`, #55 `56aa92a` and #56 pre-sync `c33bd7d`.
The #52/#53 job summaries expose no steps or logs and no specific cause was
recovered. The latest inspected #54, #55 and #56 test checks have the explicit
pre-job annotation: “recent account payments have failed or your spending
limit needs to be increased.” It directs the owner to Billing & plans but
does not say which condition applies. No code tests ran in those jobs. This is
not evidence that billing is the root cause, and it does not show that a
self-hosted runner bypasses the account gate.

| PR | Published head | Latest `test` run | Latest `symbol-catalog` run |
| --- | --- | --- | --- |
| #52 | `b431d11bf0ac841ff30353a06263d23fb901307c` | [45542863564](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863564) | [45542863839](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863839) |
| #53 | `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354) | [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397) |
| #54 | `4d220066c3e9ab83a321ac9517bbabc8fc22e293` | [45546742718](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742718) | [45546742695](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742695) |
| #55 | `56aa92a6920a429b83458380231642fe59feaf08` | [45548299466](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45548299466) | [45548299391](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45548299391) |
| #56 | `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0` | [45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246) | [45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153) |

The previous exact local gate for #56 was on docs head `0c2e789` and passed
700 tests plus Ruff, catalog, atlas, evidence and capability checks. The
current local #56 candidate is syncing with PR #53 head `79d3679`; it needs a
new exact-head gate. The table does not represent checks on that unpublished
candidate.

GitHub's billing guide states that self-hosted runners do not incur its
per-minute Actions charge; the operator still pays for compute, isolation,
monitoring and teardown. The observed annotation provides no evidence that a
runner-type change bypasses the pre-job account check. If the owner chooses a
pilot, the bounded design is one just-in-time job on a clean disposable VM,
no repository secrets, least-privilege token, no private-network or cloud
metadata access, no cross-repository runner group, and VM/disk destruction
afterward. Private repositories still need a trust boundary for untrusted PR
code; avoid persistent shared runners and `pull_request_target`. This is a
proposal only; no runner or workflow change was made. See GitHub's [billing
and usage](https://docs.github.com/en/actions/concepts/billing-and-usage),
[secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use),
[self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
and [JIT runner removal](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/remove-runners).

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
