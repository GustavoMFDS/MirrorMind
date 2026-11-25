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
| B-08 | Exact check-run diagnostics on #54 `2794abf`, #59 `afce53a`, #60 `59deef2` and #61 `b9a8151` carry the message that jobs were not started because recent account payments failed or the spending limit needs to be increased. This confirms the stated account-level pre-job gate for those exact heads, but not which account condition applies. Several older #60/#61 heads have one annotation in check-run metadata while their annotation text was not recovered; do not call those heads unannotated or infer the same cause. | Account owner inspects the settings named by the exact annotations; then rerun required checks on reviewed heads without changing workflows or protections | GitHub account owner / repository administrator | Preserve local exact-head receipts, continue tests and documentation gates, keep PRs draft and report Actions status as failed |
| B-09 | Integration of the current review queue: PRs #52–#61 are open drafts and unmerged as of 2026-11-25. Dependent tasks cannot be promoted based on local implementation or tests alone. | Human review and integration decisions for prerequisite PRs; independently inspect required Actions outcomes where workflows run; then reconcile task dependencies against merged heads | Project owner / repository reviewers | Continue genuinely independent ready work, preserve the draft branches and evidence, and do not duplicate slices or assume dependency completion |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## B-08 — workflow run snapshot (2026-11-24 21:48 UTC)

Both configured pull-request workflows completed with failure on the
following pinned heads at snapshot time. This dated evidence is separate from
local quality-gate receipts; later commits may have additional runs.

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
| [#61](https://github.com/GustavoMFDS/MirrorMind/pull/61), `df7b90c` | [45494754309](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45494754309) failed | [45494754332](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45494754332) failed |

PR #57's body records the same payment-or-spending-limit message on its listed
runs. Exact diagnostics now recover that message for the pinned #54, #59, #60
and #61 heads named in B-08, confirming the message only for those exact
revisions. It does not distinguish the specific account condition. On older
heads, missing annotation text or unavailable logs are insufficient to label
a run unannotated or infer its cause.

### Exact-head follow-up (2026-11-25)

- PR #60 earlier documented head `cad28d8c1e38dfd1cf8007c1b50853132d719ee3`
  has test run
  [45534347123](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534347123)
  and symbol-catalog run
  [45534347132](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534347132)
  failed before steps. Exact check diagnostics carry the payment-or-spending-
  limit pre-job message. This establishes the reported account gate on this
  exact revision, not the specific account condition; no repository tests ran.
- PR #61 prior head `288021f` had runs
  [45495329331](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329331)
  (`test`) and
  [45495329221](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329221)
  (`symbol-catalog`) likewise had empty steps and unavailable logs. Check-run
  metadata records one annotation per check, but the text was not recovered.
  The corrected branch head
  `4931e049dcf03a7b3843bb4c12a54ea4d26b533a` has test run
  [45536001576](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536001576)
  and catalog run
  [45536001585](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536001585)
  failed before steps. Both jobs returned empty step lists and log retrieval
  returned `BlobNotFound`. Check-run metadata records one annotation per
  check, but its text was not recovered. Do not call this head unannotated or
  infer a cause from other revisions.
- The final documented PR #61 head at this snapshot,
  `411546a9915ef82e81a5ed6723ce7292d85c3a57`, has test run
  [45536284392](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536284392)
  and catalog run
  [45536284438](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536284438)
  failed before steps. Both job step lists are empty; logs returned
  `BlobNotFound`. Check-run metadata records one annotation per check, but its
  text was not recovered; do not call the head unannotated or infer a cause.
- PR #60 latest documented head
  `59deef2a780d7802d8b8d29b66dd0189e96365ea` has test run
  [45538605875](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538605875)
  and symbol-catalog run
  [45538605893](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538605893).
  Exact diagnostics show the same account-level pre-job message on both
  checks; no repository steps ran and logs were unavailable.
- PR #61 reviewed head before this documentation correction
  `b9a8151269287b7264dc1eed0da7ed02a50202f2` has test runs
  [45536692432](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536692432)
  and [45536687429](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536687429),
  and symbol-catalog runs
  [45536692334](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536692334)
  and [45536687419](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536687419).
  All four exact annotations report the same payment-or-spending-limit
  pre-job message. No repository steps ran; logs were unavailable. The
  message does not identify which account condition applies or demonstrate
  remote test execution.

### Self-hosted runner assessment

GitHub currently lists self-hosted runner usage as free of its per-minute
Actions charge, while the owner still pays for VM compute, clean images,
network isolation, monitoring, log retention and teardown. A self-hosted runner
is **not established as a fix for this B-08 gate**: the observed message says
the job was not started because of account payments or spending limit, and no
evidence shows that changing runner type bypasses this pre-job account check.
Do not change workflows or required-check protections on this evidence.

If the owner later authorizes a bounded pilot, use a dedicated disposable VM
created from a clean image for each job, registered as an ephemeral
just-in-time (JIT) runner that accepts at most one job. Give it no repository
secrets, keep its short-lived JIT registration config out of disk and logs, set
the workflow `GITHUB_TOKEN` to minimum read-only permissions, block access to
private networks and cloud metadata, and assign no cross-repository runner
group. Destroy the VM and disk afterward, forward only scrubbed diagnostic
logs, and verify the exact required checks on a harmless test revision. A
persistent shared runner is unsuitable:
GitHub warns that untrusted pull-request code can compromise self-hosted runner
environments, including in private repositories. Reusing hardware can also
leave state between JIT jobs; a clean disposable VM is part of this proposal.

Sources: GitHub [billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage),
[secure use](https://docs.github.com/en/actions/reference/security/secure-use),
[self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
and [JIT runner removal](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/remove-runners).

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
  see the pinned B-08 run table. Latest exact-head annotations establish the
  stated account payment-or-spending-limit start gate for those revisions,
  not the specific account condition; they do not show source-code tests ran.
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
