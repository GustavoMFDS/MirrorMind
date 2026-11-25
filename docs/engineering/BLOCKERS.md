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
| B-07 | A restricted run of integrated source candidate `07c405b0d49ab05611413acce61af1123111fb48` timed out in pytest at 900 seconds. Exact clean integrated SHAs `07c405b`, `4d1d5b9`, `970843e`, `3f9bbb8`, `fd72b76` and `b292db0` passed the complete local gate outside the restricted sandbox: 756 tests and all six stages. The earlier PR #52 implementation SHA `c51ab30370db47e9f7105c97f870008e4fc442c5` remains historical and was not rerun. | For later integrated heads, run the exact clean SHA through the complete gate; do not skip API tests | Codex execution environment / project maintainer | All listed integrated SHAs passed pytest, Ruff, catalog, atlas, evidence and capability checks outside the sandbox with one existing Starlette/httpx deprecation warning. The #54-only docs head `2794abf` separately passed all six gate stages with 728 tests. The restricted timeout is recorded, not hidden; no application code or verifier was changed to avoid it. |
| B-08 | The latest inspected #54 head is `2794abf`; #55 is `b292db0`. On #55, both current required checks and a repeated check pair failed before repository steps with the explicit GitHub annotation that recent account payments failed or the spending limit needs to be increased. The annotation establishes a pre-job account start gate, but not which setting caused it. | Account owner inspects GitHub Billing & plans; then rerun checks on corrected reviewed heads without changing required checks | GitHub account owner / billing administrator | Keep official CI separate from the passing local gate. Evaluate, but do not configure, a hardened ephemeral self-hosted runner unless its trust, admin and cost requirements are accepted. |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## B-08 exact diagnostics and runner assessment — 2026-11-24

This is a point-in-time diagnostic snapshot: #54 was at head `2794abf` and #55
at integrated published head `b292db0` when its latest checks below were
inspected. The exact `b292db0` integrated commit passed the full local gate;
its Actions runs still failed before repository steps. Both required workflows carry an
annotation that the job was not started because recent account payments
failed or the spending limit needs to be increased. These runs provide no
result for repository code. The annotation states the start-gate category but
does not distinguish a payment failure from a spending cap.

| PR | Published head | `test` run | `symbol-catalog` run |
| --- | --- | --- | --- |
| #52 | `5c307e426c43aee4179e3257d7d367214e8c3a63` | [45319452833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452833) | [45319452852](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452852) |
| #53 | `210f0f382938a67e518df688cc4e19c03d3d7af6` | [45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471) | [45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864) |
| #54 | `2794abff855665fb65f32af655415c52dde68872` | [45518440891](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518440891) | [45518440963](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518440963) |
| #55 | `b292db0231d00f307eb4b0694b8e73014bdb9211` | [45519636625](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519636625) (repeat [45519630165](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519630165)) | [45519636706](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519636706) (repeat [45519629914](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519629914)) |
| #56 | `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0` | [45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246) | [45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153) |
| #57 | `646e4db6991b1769c922cf87a0b85630039915da` | [45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005) | [45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950) |
| #58 | `465a2f2c46fb6484aa2f0abea7920953ca4f0d00` | [45447930415](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930415) | [45447930394](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930394) |
| #59 | `a5951e49a78796908ecd1975c65052b5a2548cd7` | [45460098823](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098823) | [45460098802](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098802) |
| #60 | `6374f0bb9a981271cb9340a190dcdebec6263cc9` | [45476173796](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173796) | [45476173736](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173736) |
| #61 | `288021f25e24efc26591b064eafa1d8b4e287ac8` | [45495329331](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329331) | [45495329221](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329221) |

The PR #55 details for all four listed run IDs returned zero workflow steps
and the same explicit annotation. PR #61 diagnostics also showed zero workflow
steps; previous #52–#60 checks carried the same annotation. No repository
workflow log or test execution can be inferred from these statuses.

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
remain unverified. No self-hosted runner or workflow change was made.

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
