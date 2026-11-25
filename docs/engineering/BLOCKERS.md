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
| B-07 | A restricted run of integrated source candidate `07c405b0d49ab05611413acce61af1123111fb48` timed out in pytest at 900 seconds. Later exact clean integrated heads `07c405b`, `4d1d5b9`, `970843e`, `3f9bbb8` and `fd72b76` passed all six local-gate stages with 756 tests; PR #54 head `4d22006` passed with 728 tests. PR #52 `b431d11` and PR #53 `79d3679` also passed their complete gates. This branch's new post-sync candidate is still pending its own exact-head gate. The timeout remains historical; no application code or test verifier was weakened. | Run the exact new integrated head through the full gate; do not skip API tests | Codex execution environment / project maintainer | Preserve the restricted timeout and exact-head receipts as separate evidence; keep API tests enabled and rerun outside the restricted environment if the timeout recurs. |
| B-08 | Latest published PR #52 head `b431d11` and #53 head `79d3679` each have failed `test`/`symbol-catalog` runs without repository logs. Latest #54 head `4d22006` and #55 head `b292db0` also have failed checks. The exact annotation on #54/#55 says recent account payments failed **or** the spending limit needs to be increased; it does not identify which condition applies. No repository test steps ran. See the head-bound run table below. This does not establish a billing root cause or whether a runner change bypasses the pre-job gate. | Repository/account owner checks the GitHub Billing & plans state named by the diagnostic, identifies the actual condition and restores normal check execution; then verify required runs on reviewed heads | GitHub account owner / repository administrator | Preserve required checks and protections. Keep local gate evidence separate; assess a hardened ephemeral runner without treating it as a proven workaround. |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## B-08 exact diagnostics and runner assessment — 2026-11-25

This table records the latest inspected published heads for #52–#55 and the
last inspected heads for #56–#61. For #54 and #55, diagnostics confirm the
failed runs did not start repository steps; the annotation says recent account
payments failed **or** the spending limit needs to be increased. It explicitly
directs the account owner to Billing & plans but does not distinguish the two
conditions. No code-test result or specific billing cause is inferred.

| PR | Published head | `test` run | `symbol-catalog` run |
| --- | --- | --- | --- |
| #52 | `b431d11bf0ac841ff30353a06263d23fb901307c` | [45542863564](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863564) | [45542863839](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863839) |
| #53 | `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354) | [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397) |
| #54 | `4d220066c3e9ab83a321ac9517bbabc8fc22e293` | [45546742718](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742718) | [45546742695](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742695) |
| #55 | `b292db0231d00f307eb4b0694b8e73014bdb9211` | [45519636625](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519636625) | [45519636706](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519636706) |
| #56 | `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0` | [45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246) | [45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153) |
| #57 | `646e4db6991b1769c922cf87a0b85630039915da` | [45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005) | [45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950) |
| #58 | `465a2f2c46fb6484aa2f0abea7920953ca4f0d00` | [45447930415](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930415) | [45447930394](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930394) |
| #59 | `a5951e49a78796908ecd1975c65052b5a2548cd7` | [45460098823](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098823) | [45460098802](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098802) |
| #60 | `6374f0bb9a981271cb9340a190dcdebec6263cc9` | [45476173796](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173796) | [45476173736](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173736) |
| #61 | `288021f25e24efc26591b064eafa1d8b4e287ac8` | [45495329331](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329331) | [45495329221](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329221) |

Earlier diagnostics for the listed #56–#61 heads also showed failed checks
before repository steps. No repository workflow test pass can be inferred
from any of these statuses.

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
