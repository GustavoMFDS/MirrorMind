# Blocker and decision register

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | Real source rights: M5 unresolved; UCI Online Retail II shows CC BY 4.0, which is not project-use or privacy approval. UCI and aggregate Census/ALFRED options are documented for owner decision; no data was downloaded. | Original license/terms, intended research or commercial use, attribution, privacy/minimization, retention, accepted dataset card and explicit source approval | Project owner / appropriate rights reviewer | Keep synthetic fixtures; choose/reject the no-download aggregate method pilot and decide separately on UCI handling |
| B-02 | Historical availability and empirical evaluation: event time is not first availability. A concrete Census/ALFRED release-vintage protocol is proposed; retained first-release values remain unverified. | Verified source vintages/revisions, immutable snapshot, locked chronological split and approved data; never substitute transaction/event timestamp for first availability | Project owner with evidence/model reviewer | Implement synthetic delay, missingness, leakage and holdout regressions; prepare exact source manifest only after decision |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | Optional WorldKernel runtime acceptance | Pinned supported version, actual engine/result schema, approved world mapping, trusted local fixture and resource caps; separate repo owner approval for cross-repo changes | Project owner / engine maintainer | Strict pure mapping, fake gateway tests and disabled-engine paths; no hard dependency or invented engine result |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | A restricted run of integrated source candidate `07c405b0d49ab05611413acce61af1123111fb48` timed out in pytest at 900 seconds. Later exact clean integrated heads `07c405b`, `4d1d5b9`, `970843e`, `3f9bbb8` and `fd72b76` passed all six local-gate stages with 756 tests; PR #54 head `4d22006` passed with 728 tests. PR #55 sync merge `b9eba02` and its documentation follow-up `cc9bdb4` each passed the complete exact-head gate with 756 tests and all five other stages. The timeout remains historical; no application code or test verifier was weakened. | Reopen only if a later exact-head gate reproduces a failure; do not skip API tests | Codex execution environment / project maintainer | Preserve the restricted timeout and exact-head receipts as separate evidence; keep API tests enabled and rerun outside the restricted environment if the timeout recurs. |
| B-08 | The latest inspected `test` and `symbol-catalog` checks for published PR heads #52–#61 all failed before repository steps. Their exact annotations list recent account payment failure **or** a spending-limit increase as alternatives; the message does not identify the actual condition or underlying root cause. No repository test steps or logs were returned. See the head-bound table below. This is evidence of a pre-job block, not proof that account billing is the root cause or that a runner change will bypass it. | Account/repository owner inspects the exact GitHub account and Actions state named by the diagnostic, restores normal check execution, then verifies required runs on reviewed heads | GitHub account owner / repository administrator | Preserve required checks and protections. Keep local gate evidence separate; assess a hardened ephemeral runner without treating it as a proven workaround. |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## B-08 exact diagnostics and runner assessment — 2026-11-25

This point-in-time table records the latest inspected published heads for
#52–#61 before the local PR #58 sync. Detail calls for both required checks on
each head returned the same pre-job annotation and no job or log records. The
message says recent account payments failed **or** the spending limit needs to
be increased, and directs the owner to Billing & plans. It does not distinguish
the alternatives. No code-test result or specific account cause is inferred.

| PR | Published head | `test` run | `symbol-catalog` run |
| --- | --- | --- | --- |
| #52 | `b431d11bf0ac841ff30353a06263d23fb901307c` | [45542863564](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863564) | [45542863839](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863839) |
| #53 | `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354) | [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397) |
| #54 | `4d220066c3e9ab83a321ac9517bbabc8fc22e293` | [45546742718](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742718) | [45546742695](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742695) |
| #55 | `56aa92a6920a429b83458380231642fe59feaf08` | [45548299466](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45548299466) | [45548299391](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45548299391) |
| #56 | `e993391a61a99d63008bc970cb19af673be4c18c` | [45550857405](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45550857405) | [45550857276](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45550857276) |
| #57 | `646e4db6991b1769c922cf87a0b85630039915da` | [45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005) | [45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950) |
| #58 | `46b07a0337bbf449d2fd72a90ba240d0e9c9a063` | [45522848614](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522848614) | [45522848658](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522848658) |
| #59 | `afce53a8ebc24261ea33ab705394eecb86459781` | [45529860767](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529860767) | [45529860606](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529860606) |
| #60 | `59deef2a780d7802d8b8d29b66dd0189e96365ea` | [45538613621](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538613621) | [45538613716](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538613716) |
| #61 | `8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e` | [45539810679](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45539810679) | [45539810723](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45539810723) |

Local merge commit `5544bc0c2116d825a37d49a3ec75960e9896dd23` integrates #58
with #55 and passed the complete local gate at 2026-11-25 05:12:21 UTC: 768
tests plus Ruff, catalog, atlas, evidence and capability checks. That candidate
was not yet published when the diagnostics above were collected, so its
official checks remain unobserved here. None of the listed failures is a
repository test result.

### Self-hosted runner option

The repository API reported this repository as private at the time of review.
GitHub still warns that private/internal repositories require caution because
read-access users may fork and submit pull requests that compromise a
persistent self-hosted runner, its workspace, secrets or token. GitHub
recommends self-hosted runners for private repositories over public ones, but
its security guide does not treat a private repository as an isolated trust
boundary. See [GitHub's secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
and [runner setup guidance](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners).

If the account owner chooses this path, the candidate design is one
just-in-time runner in a disposable VM per check, destroyed after the job;
no persistent workstation or shared runner. Keep the existing job IDs,
commands, test selection and required-check names. Restrict assignment to this
repository and the two required workflows; accept only `pull_request` jobs,
never run pull-request code through `pull_request_target`; provide no
repository secrets and a read-only short-lived `GITHUB_TOKEN`; block access to
host credentials, sibling projects, Docker control sockets and private
networks; allow only dependency/artifact endpoints required by the existing
workflows; retain an auditable image, egress and teardown record. A clean
single-use VM is a proposed containment boundary, not a demonstrated security
guarantee or a confirmed way to clear the current account-level start gate.
Cloud runner costs, repository-admin setup, fork policy and billing behavior
remain unverified. GitHub documents that self-hosted runners do not incur its
per-minute Actions charge, but the owner still pays for compute and operation.
No evidence shows that changing runner type clears the observed pre-job account
gate. See [billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage),
[self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
and [JIT runner removal](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/remove-runners).
No self-hosted runner or workflow change was made.

## Source references and precise restrictions

- [M5 review](datasets/M5_ACCESS_REVIEW.md) documents an unresolved
  permission grant. Public accessibility is not permission.
- [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
  records the official license statement and unresolved privacy,
  historical availability, scope and source snapshot issues. Its B-01/B-02
  section compares UCI retrospective research with a no-download
  Census/ALFRED temporal-method proposal; owner approval remains pending.
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
