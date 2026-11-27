# Blocker and decision register

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | **UCI source evaluation stopped at the approved 250,000-group ceiling; PR #65 remains under independent review.** The owner approved only the local, non-commercial #352 study, bounded ZIP profile, faithful `StockCode` normalization, and UCI-only group override. MM-022 authorizes six-digit IDs as sales candidates, exact uppercase `C` plus six digits as cancellation, and other single ASCII-letter plus six-digit prefixes as unverified transactions excluded before aggregation. Only aggregate exclusion counts may be retained; original invoice IDs are not. Other formats fail closed, and generic readers remain unchanged. The sole source attempt used MM-021, under which both cancellation and unverified classes were already excluded before grouping. It exceeded the cap and returned no projection, complete group/exclusion counts, metrics or model card. MM-022 was not applied to the source attempt and cannot change its accepted rows or observed group bound; the new all-prefix coverage is synthetic. The workbook was not reread. The path-free [manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json) records the exact source hash and private retention deadline. The current synthetic regression covers all 52 ASCII prefixes, aggregate-only redaction and malformed-input rejection. Commit `2413df151fd6baa9bb4de472c713519f2d69937c` passed the exact six-check local gate with 867 tests, zero skips and the reviewed WorldKernel pin; receipt `results/local-quality-gate-2413df151fd6baa9bb4de472c713519f2d69937c.json`. This is not empirical source evidence or official CI. Do not retry, chunk or widen the ceiling; another method needs a distinct bounded-method decision. Raw source remains private until its 30-day deletion deadline. This does not authorize Census acquisition, customer-level/commercial use or M5; M5 remains NO-GO. | Keep UCI stopped under the current source attempt. Prepare only a concrete, separately bounded method for owner review; continue independent synthetic and Census-protocol work without acquiring data. | Project owner / appropriate rights reviewer | Preserve synthetic tests, generic contracts, aggregate-only handling, the documented fail-closed path and independent work |
| B-02 | **Still open for point-in-time claims.** UCI #352 remains event-time retrospective with no verified row-level first-publication timestamp, and its bounded source attempt produced no evaluation. Census first-release artifacts and revision histories have not been acquired or verified. The approved UCI lane has now reached a documented stop, so independent Census source/protocol proposals may proceed, but no vintage or API acquisition is authorized by this status alone. | Never derive `available_on` from UCI `InvoiceDate`. For a separately approved Census lane, verify official first-release bytes/timestamps, preserve gaps/revisions, then freeze chronological origins/holdout and matched baselines. | Project owner with evidence/model reviewer | Maintain synthetic temporal regressions; prepare a concrete free official-source proposal without acquiring vintages or fabricating availability |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | The narrow local M1 runtime is implemented against reviewed WorldKernel commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`: M1E-02 runs its synthetic inventory demo and M1E-04 adds a fixed MirrorMind-owned policy world through the same optional worker. PR #62 was independently reviewed, technically approved and integrated at main commit `a456034c55ed7634ad4768b26788fec09dab1d08`; the owner-reported post-merge gate passed 835 tests, zero skips and six verifiers with the exact engine revision installed. The current local workflow also records WorldKernel selection separately from test-double parity. The integrated local compatibility scope is accepted; broader service acceptance remains open because local process bounds do not provide hostile-code isolation, CPU/memory quotas, deployment controls or a general plugin contract. No WorldKernel repository edit is in scope. | Any future HTTP/service execution needs its own contract, admission, authentication and operational isolation review; any external-repository change needs separate authorization. | Project owner / engine maintainer | Keep the dependency optional and policy world code-owned; use synthetic tests and document broader service limitations |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | The historical full-gate timeout on `8f906b8` remains unexplained. The prior integrated candidate `42560e441f5020a5b4319a0f7b56474ef0485681` passed 828 tests; corrected provenance candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85` passed 832 tests and all five other local checks with the reviewed WorldKernel pin installed. The old timeout did not recur, but its cause is not resolved. This is historical diagnostic uncertainty, not evidence that current code fails. | If the timeout recurs, capture exact SHA, interpreter/dependency paths, a bounded faulthandler/thread dump and environment before changing anything. Do not increase test timeouts or skip the health test. | Codex execution environment / project maintainer | Preserve prior receipts and continue normal exact-head gates; do not infer the old cause from later passes. |
| B-08 | The owner confirms the GitHub Actions allowance is exhausted and authorizes no paid usage or spending-limit increase. PR #57 diagnostics on `1bf178b` and `1cff92c` show pre-job annotations with the payment/spending-limit alternatives, without identifying the subcondition; those jobs had no repository steps. Official GitHub documentation states self-hosted runner usage is free, but that does not prove a self-hosted job would bypass this account-level pre-start gate. It would require an owner-provided machine; GitHub warns that self-hosted runners can be compromised by workflow code and recommends ephemeral runners for autoscaling. No dedicated disposable host is approved, and a shared workstation is not an acceptable substitute. See [billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage), [self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners) and [secure use](https://docs.github.com/en/actions/reference/security/secure-use). | Official Actions must become available within the existing budget, or the owner must separately approve a zero-cost, dedicated and clean ephemeral host after a security and feasibility review. Any required remote check remains a separate gate. | GitHub account owner / repository administrator | Use the owner-approved exact-clean-head local six-check procedure and independent review. Do not register a runner, change workflow labels, rerun identical failures, change protections, spend, raise limits, bypass, impersonate or weaken checks. |

### B-08 diagnostics — PR #65 published MM-022 head 5c1835f, 2026-11-27 UTC

PR #65 head `5c1835f8862bbe12b9028707cfa3b9d893b9eda6` passed the local gate
before publication. Its automatic Python API CI run
[46047574630](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46047574630)
and documentation catalog run
[46047574634](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46047574634)
completed with failure. Job records identify `test` and `symbol-catalog`;
the connector returned no steps or logs, and the combined-status endpoint
returned an empty list. It did not return annotation detail, so the cause is
undetermined. The owner's report of exhausted allowance and zero paid budget
is separate and does not establish the cause of these exact runs. No manual
rerun, workflow change or protection change occurred. Local validation is not
official CI.

### B-08 diagnostics — PR #60 and #61 heads, 2026-11-27 UTC

Exact-head diagnostics were read for PR #60 head
`fafdedae3a76398e0450773065e40384c96d1ed7` and PR #61 head
`f30556ecb9219c1bc4eb0eb720f9c59c3a729b29`. Each head has four failed
check-runs across automatic test and symbol-catalog attempts. All eight
annotations say jobs were not started because recent account payments failed
**or** the spending limit needed to increase. The connector returned no jobs,
steps, logs or combined status. This establishes neither which alternative
applies nor a repository test failure; the owner's quota report is separate.
No manual rerun was made.

- PR #60 runs: [45751965277](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45751965277),
  [45751965252](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45751965252),
  [45751958433](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45751958433),
  [45751958487](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45751958487).
- PR #61 runs: [45756503398](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45756503398),
  [45756503234](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45756503234),
  [45756497802](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45756497802),
  [45756497731](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45756497731).

### B-08 diagnostics — PR #65 status-sync head `7e47844`

The exact PR #65 status-sync head passed the local gate, then produced four
failed Actions check-runs across two automatic attempts: test runs
[45925209232](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45925209232)
and [45925213284](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45925213284),
and symbol-catalog runs
[45925209273](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45925209273)
and [45925213300](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45925213300).
The check-run records report one annotation each, but the available connector
could not retrieve annotation content. All four jobs returned empty step lists,
null log URLs and log-download 404 responses; the combined-status endpoint
returned an empty status list. The evidence confirms failed checks without
repository steps or retrievable logs. It does not establish their cause.
The owner's report of exhausted Actions allowance and zero paid budget remains
separate evidence; no billing-specific cause is inferred from these runs.
No manual rerun was made.

### B-08 diagnostics — PR #65 pre-reconciliation head `b1bd795`

Diagnostics were read against exact head
`b1bd7951ecc80988146eb46362eea99940ef7542`. Two automatic attempts produced
failed `test` and `symbol-catalog` check-runs: [runs
45933362603](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45933362603),
[45933362600](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45933362600),
[45933357995](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45933357995)
and [45933358029](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45933358029).
Check-run IDs are `140290841449`, `140290841429`, `140290826897` and
`140290826195`. All four annotations say the job was not started because
recent account payments failed **or** the spending limit needed to increase.
The detail calls returned no job steps, logs, or combined statuses. This
establishes a pre-start failure, not a repository-test result and not which
annotation alternative applied. The owner separately confirms quota
exhaustion and zero paid budget. No manual retry, spending-limit change, paid
usage, workflow change or protection bypass occurred.

### B-08 diagnostics — PR #65 documentation follow-up `c2410bd`

For exact head
`c2410bdbafbb7a522730d31a304faa8a72b1b097`, automatic runs [45939953770](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45939953770), [45939953729](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45939953729), [45939948905](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45939948905) and [45939948832](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45939948832) failed before repository steps. Check-run IDs are `140311734334`, `140311734200`, `140311718330` and `140311717818`. Each annotation repeats the payment-failure **or** spending-limit message; it does not identify the alternative. Jobs returned no steps or logs, and combined status returned no statuses. The owner's quota report remains separate evidence. No rerun or configuration change was made.

The sandboxed exact-head local gate timed out in pytest after 900 seconds
(exit `124`); receipt:
`results/local-quality-gate-c2410bdbafbb7a522730d31a304faa8a72b1b097-sandbox-timeout.json`.
A 20-second faulthandler trace placed `test_health` in Python 3.13.5's
Windows asyncio `_fallback_socketpair` waiting at `socket.accept`, before
application code. A bounded child-process `asyncio.new_event_loop()` probe
timed out in the sandbox and completed in the authorized local environment.
The same exact SHA then passed all six local checks: 864 tests, zero skips,
with the reviewed WorldKernel pin, at `2026-11-27T04:25:32.503435Z`. Receipt:
`results/local-quality-gate-c2410bdbafbb7a522730d31a304faa8a72b1b097.json`.
This diagnoses the restricted sandbox for that run; it is not official CI or
evidence of an application failure.

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## B-08 exact diagnostics and runner assessment — 2026-11-25

This point-in-time table records the inspected published heads for
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
| #58 | `46b07a0337bbf449d2fd72a90ba240d0e9c9a063` (pre-sync snapshot) | [45522848614](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522848614) | [45522848658](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45522848658) |
| #59 (pre-integration snapshot) | `afce53a8ebc24261ea33ab705394eecb86459781` | [45529860767](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529860767) | [45529860606](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529860606) |
| #60 | `59deef2a780d7802d8b8d29b66dd0189e96365ea` | [45538613621](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538613621) | [45538613716](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538613716) |
| #61 | `8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e` | [45539810679](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45539810679) | [45539810723](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45539810723) |

Local merge commit `5544bc0c2116d825a37d49a3ec75960e9896dd23` integrates #58
with #55 and passed the complete local gate at 2026-11-25 05:12:21 UTC: 768
tests plus Ruff, catalog, atlas, evidence and capability checks. That candidate
was not yet published when the diagnostics above were collected, so its
official checks remain unobserved here. None of the listed failures is a
repository test result.

After PR #58 published exact head `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8`,
its test run [45552758621](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45552758621)
and symbol-catalog run
[45552758221](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45552758221)
failed before repository steps. The exact diagnostics list recent account
payment failure **or** a spending-limit increase as alternatives; detail calls
show a completed failed job with no steps or logs. The condition is unresolved.
The PR #56/#58 integration-base merge
`eb6601ddfec7f021a8377b32abda8934fed02640` separately passed the full local gate
outside the restricted sandbox: 768 tests plus Ruff, catalog, atlas, evidence
and capability checks. These local checks do not count as official Actions.

The current PR #59 integrated head is
`c000ebd3484e1d9a83f1a440a12369361f4a52b1`. Its test run
[45616226536](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45616226536)
and symbol-catalog run
[45616226367](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45616226367)
completed as failures before repository steps; job details contain no steps or
logs. Each check-run record has one annotation, but its text was not available
through the current connector. Do not infer that these exact runs carry the
same alternative account annotation recovered for earlier heads. No remote
tests are evidenced for `c000ebd`.

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

### PR #57 owner continuation and exact-head evidence

The owner’s current decision is to stay within the existing free allowance
and use the repository's temporary local gate. PR #57 comment
[7164856818](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164856818)
records the UCI #352 event-time protocol followed by an independent aggregate
Census release-vintage protocol. Follow-up comments
[7167002881](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7167002881)
and [7169397485](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7169397485)
report synthetic-only implementation and the latest local gate. On exact
head `1cff92c1345ab20c0533281809502a33025cff10`, all 712 tests and five
documentation/style checks passed; receipt status was
`local_gate_passed_not_official_ci`. The four latest recorded check IDs were
`139378962637`, `139378898990`, `139378961707` and `139378900784`; their
annotations say the job was not started because recent payments failed or a
spending limit needs to increase. The wording does not identify which
alternative applies. No paid usage, manual rerun or workflow/protection change
was made. The exact earlier checks at `1bf178b` and the independently passing
head-specific gate are recorded in the same comments; the older `8f906b8`
timeout cause remains unknown.

The owner-controlled GitHub CLI diagnostic recorded in comment
[7164870326](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164870326)
found the repository unprotected and no applicable branch rules at that
inspection time. No protection was changed. Do not infer that the repository
has required checks configured; verify current rules before any future
integration request. The owner has separately directed that existing
protections must be preserved and no required check bypassed.

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
