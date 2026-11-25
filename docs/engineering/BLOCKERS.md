# Blocker and decision register

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | M5 remains NO-GO. Owner approved preparation of sequential UCI Online Retail #352 and aggregate Census pilots, not source acquisition or general use. UCI is a local event-time study; Census is aggregate-only. No source bytes were acquired. | Verify original source terms, attribution/change notice, purpose, privacy/minimization, retention/deletion, exact snapshot manifest and accepted dataset card; obtain source-specific approval before processing any real file | Project owner / appropriate rights reviewer | Keep automated tests synthetic; prepare the narrow adapter, permission/privacy plan and aggregate protocol without acquiring source data |
| B-02 | Historical availability remains unverified. Owner approved preparing UCI event-time retrospective evaluation followed by a separate aggregate Census release-vintage study. Event time is not publication time; no vintage was fabricated or materialized. | Verify official first-release/revision vintages and conservative as-of availability; freeze source snapshot and chronological split only after approval; never substitute transaction time for release evidence | Project owner with evidence/model reviewer | Add synthetic delay, missingness, leakage and holdout regressions; prepare source/vintage manifests without downloading or claiming temporal acceptance |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | Narrow local M1E-02 compatibility is now exercised experimentally against exact WorldKernel commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a` with a fictional registered demo, result validation, timeout and bounded output. Broader service/hostile-code isolation, artifact attestation, licensing for redistribution and a lead-time world remain unresolved. | Reviewed separate service/security design, CPU/memory and process-tree isolation evidence, source licensing decision for any redistribution, and a separately reviewed lead-time model before M1E-03/product claims | Project owner / engine maintainer | Preserve local optional SHA pin and synthetic integration; keep API independent and WorldKernel repo read-only; do not describe demo as demand or lead-time model |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | Restricted candidate `07c405b0d49ab05611413acce61af1123111fb48` historically timed out at 900s. Later exact integrated heads through PR #55 passed six local checks. Independent owner-run isolation at PR #57 head `1bf178b5c4b31bcd68072b69748a14249c6c2649` passed `test_health` (1.07s) and the full gate (700 tests, 23.18s); the prior timeout did not reproduce. Its cause remains unknown; no verifier was weakened. | Reopen only if a later exact-head local gate reproduces a failure; do not skip API tests | Codex execution environment / project maintainer | Preserve historical timeout and isolated retest as separate evidence; keep all API tests enabled. |
| B-08 | Owner confirms GitHub Actions allowance is exhausted and authorizes no paid usage/limit increase. On PR #57 head `678755e`, four checks fail with one annotation each; `steps=[]` and job-log fetches return 404. The connector does not expose those annotation texts, so individual cause for `678755e` remains unknown. Exact annotations on head `1bf178b` separately state recent account payments failed **or** spending limit must increase; that text does not identify which account condition applies. No repository test steps ran. | No paid resource or spending-limit change is authorized. Resume official checks only when allowance is available through the owner's existing account decision; verify checks on exact candidate heads. | GitHub account owner / repository administrator | Use authorized exact-head local six-check gate; retain draft PRs and required check definitions; do not disable checks, merge around them, or start a self-hosted runner without separately approved zero-cost isolated infrastructure. |

Blockers are scoped. M1E-02's narrow local synthetic-execution slice has
compatible pin and engine evidence; that does not resolve B-04 for a service,
hostile-code isolation, redistributed package or lead-time model. B-05 remains
about authorized provider use/spend. Neither blocker suspends independent
synthetic design and testing.

## B-08 exact diagnostics and runner assessment — 2026-11-25

This table preserves historical inspected heads. A separate current-head
record below covers PR #57 at `678755e`. Diagnostics for PR #54/#55 and the
owner-recovered PR #57 head `1bf178b` show pre-step failures with the annotation
that recent account payments failed **or** the spending limit needs to be
increased. That annotation does not distinguish those two conditions. The
owner separately confirms the Actions allowance is exhausted and no paid usage
or limit increase is approved. No code-test result or per-head cause is inferred
for checks whose annotation is unavailable.

| PR | Published head | `test` run | `symbol-catalog` run |
| --- | --- | --- | --- |
| #52 | `b431d11bf0ac841ff30353a06263d23fb901307c` | [45542863564](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863564) | [45542863839](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863839) |
| #53 | `79d3679013576c6a209bed9fa031b7f0fabd0d8d` | [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354) | [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397) |
| #54 | `4d220066c3e9ab83a321ac9517bbabc8fc22e293` | [45546742718](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742718) | [45546742695](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45546742695) |
| #55 | `b292db0231d00f307eb4b0694b8e73014bdb9211` | [45519636625](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519636625) | [45519636706](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45519636706) |
| #56 | `c33bd7d480f0b5ebb73f21fb02c10e9a16083fe0` | [45337443246](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443246) | [45337443153](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45337443153) |
| #57 (historical) | `646e4db6991b1769c922cf87a0b85630039915da` | [45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005) | [45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950) |
| #58 | `465a2f2c46fb6484aa2f0abea7920953ca4f0d00` | [45447930415](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930415) | [45447930394](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45447930394) |
| #59 | `a5951e49a78796908ecd1975c65052b5a2548cd7` | [45460098823](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098823) | [45460098802](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45460098802) |
| #60 | `6374f0bb9a981271cb9340a190dcdebec6263cc9` | [45476173796](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173796) | [45476173736](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173736) |
| #61 | `288021f25e24efc26591b064eafa1d8b4e287ac8` | [45495329331](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329331) | [45495329221](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329221) |

Earlier diagnostics for the listed #56–#61 heads also showed failed checks
before repository steps. No repository workflow test pass can be inferred
from any of these statuses.

### Current PR #57 head evidence

On published head `678755e2569939e66358ec482955defca7abf6b8`, the connected
diagnostics returned four failed check runs: test `139317243001` and
`139317187304`; symbol-catalog `139317241892` and `139317186508`. Their
associated Actions runs are [45646056893](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45646056893),
[45646041083](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45646041083),
[45646056856](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45646056856)
and [45646041272](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45646041272).
Each check advertises one annotation, but title, summary, text and annotation
content are empty in the connected diagnostics. All four step queries return
`steps=[]`; bounded log fetches return 404 `BlobNotFound`. The particular
annotation text and exact per-run cause therefore remain unavailable through
this connector. These observations prove no repository test step ran; they do
not independently assign the failures to billing or source code.

The owner-recovered annotations on prior #57 head
`1bf178b5c4b31bcd68072b69748a14249c6c2649` were check IDs
`139259693576`, `139259693712`, `139259664116`, and `139259664989`. Each states:
“The job was not started because recent account payments have failed or your
spending limit needs to be increased. Please check the 'Billing & plans'
section in your settings”. The owner confirms allowance exhaustion, but the
annotation itself does not identify which account condition applied.

An independent owner-run exact-head retest at `1bf178b` in fresh detached
worktree `D:\MirrorMind-review-57` passed
`tests/integration/test_api.py::test_health` (1 passed in 1.07s), then the
complete local gate (700 passed in 23.18s; six checks; one existing
Starlette/httpx warning). Receipt status was
`local_gate_passed_not_official_ci`. The earlier `8f906b8` timeout did not
reproduce in that isolated environment; its cause remains unknown and is not
declared fixed. On `678755e`, a later local full gate passed 712 tests and all
six checks; that evidence is distinct from the failed official workflows.

### Self-hosted runner option

The repository API reported this repository as private at the time of review.
GitHub still warns that private/internal repositories require caution because
read-access users may fork and submit pull requests that compromise a
persistent self-hosted runner, its workspace, secrets or token. GitHub
recommends self-hosted runners for private repositories over public ones, but
its security guide does not treat a private repository as an isolated trust
boundary. See [GitHub's secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
and [runner setup guidance](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners).

This is a design-only option. The owner has not approved new paid compute,
runner installation, credentials or workflow changes. The current allowance
decision and no-step check failures provide no evidence that a self-hosted
runner would clear the account-level start condition. Do not create a runner
or alter workflows now. If a separately authorized zero-cost isolated host is
available later, the candidate design is one
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
No self-hosted runner or workflow change was made. Owner's prior read-only
repository API check reported `Branch not protected` and no applicable branch
rules; no protection was changed. Keep the user's instruction to preserve
existing settings, and never merge or bypass checks as a substitute for an
unavailable official run.

## Source references and precise restrictions

- [M5 review](datasets/M5_ACCESS_REVIEW.md) documents an unresolved
  permission grant. Public accessibility is not permission.
- [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
  records the official license statement and unresolved privacy,
  historical availability, scope and source snapshot issues. Owner approved
  preparing the privacy-minimized UCI event-time pilot followed by a separate
  aggregate Census vintage protocol; source-specific permissions and actual
  vintage evidence remain pending. No real source bytes are in tests or Git.
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
