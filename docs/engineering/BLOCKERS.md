# Blocker and decision register

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | Real source rights and privacy remain open. The owner selected UCI Online Retail #352 as a research-only event-time pilot followed by an independent aggregate Census pilot; this authorizes preparation, not workbook acquisition, processing, commercial use or a blanket data grant. M5 remains NO-GO. | Recheck original UCI terms and attribution/change notice for the exact snapshot; approve minimal projection, cancellation classification, secure local storage, retention/deletion, manifest and dataset card before any bytes are acquired or processed. For Census, approve the exact aggregate series, geography, archive and terms. | Project owner / appropriate rights reviewer | Keep automated tests synthetic; refine the protocols, source manifests and privacy controls without retrieving real source bytes |
| B-02 | Point-in-time availability and empirical evaluation remain open. UCI `InvoiceDate` is event time with no verified first-publication field; all UCI output stays `event_time_retrospective_unverified_availability`. Census first-release archives and revision histories have not been acquired or verified. | For UCI, retain the declared event-time split and never derive `available_on` from `InvoiceDate`; any point-in-time claim needs external publication evidence. For Census, preserve actual first-release/revision bytes and conservative release timestamps, then freeze chronological origins/holdout and matched baselines. | Project owner with evidence/model reviewer | Maintain synthetic delay, missingness, leakage and holdout regressions; exercise the normalized Census selector and prepare manifests without fabricating vintages |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | The narrow local M1 runtime is implemented against reviewed WorldKernel commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`: M1E-02 runs its synthetic inventory demo and M1E-04 adds a fixed MirrorMind-owned policy world through the same optional worker. PR #62 was independently approved and merged at `a456034`; its post-merge exact-main gate passed 835 tests, zero skips and six checks with the reviewed pin (final review evidence: [comment 7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)). Broader service acceptance remains open: local process bounds do not provide hostile-code isolation, CPU/memory quotas, deployment controls or a general plugin contract. No WorldKernel repository edit is in scope. | Broader service acceptance needs its own contract, admission, authentication and operational isolation review; any external-repository change needs separate authorization. | Project owner / engine maintainer | Keep the dependency optional and policy world code-owned; use synthetic tests and document broader service limitations |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | The historical full-gate timeout on `8f906b8` remains unexplained. The prior integrated candidate `42560e441f5020a5b4319a0f7b56474ef0485681` passed 828 tests; corrected provenance candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85` passed 832 tests and all five other local checks with the reviewed WorldKernel pin installed. The old timeout did not recur, but its cause is not resolved. This is historical diagnostic uncertainty, not evidence that current code fails. | If the timeout recurs, capture exact SHA, interpreter/dependency paths, a bounded faulthandler/thread dump and environment before changing anything. Do not increase test timeouts or skip the health test. | Codex execution environment / project maintainer | Preserve prior receipts and continue normal exact-head gates; do not infer the old cause from later passes. |
| B-08 | The owner confirms the Actions allowance is exhausted and authorizes no paid usage or spending-limit increase. Exact local gates exist for merged main `a456034c55ed7634ad4768b26788fec09dab1d08` (835 tests), PR #60 `fafdedae3a76398e0450773065e40384c96d1ed7` (845), PR #61 `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29` (841), PR #63 published head `5ec904dc0be6555d3651f947ef1f02fdd6ce20f7` (877), and PR #64 `ca97ab61d15347aa271ee9ac8468a0714bdc3402` (840). Each local receipt reports zero skips and six passing checks; none is official Actions. Four #63 check runs on prior heads `42a9746` and `3bc7162`, four #63 runs on `5ec904d`, and four #64 runs on `ca97ab6`, failed before repository steps. Their annotations list payment failure or spending-limit increase as alternatives and do not identify which condition applies. No repository tests/catalog steps ran; job steps and logs are absent and combined status was empty. The owner's allowance report is separate evidence. No runner is registered; the zero-cost ephemeral-host option still needs a dedicated host and security/feasibility approval. | Official Actions can run within the existing zero-paid budget, or the owner separately approves a zero-cost dedicated ephemeral host after feasibility and security review. Any required remote check remains a separate gate. | GitHub account owner / repository administrator | Use the owner-approved exact-clean-head local six-check procedure and independent review. Do not register a runner, change workflow labels, rerun identical failures, change protections, spend, raise limits, bypass, impersonate or weaken checks. |

### PR #63 exact-head Actions diagnostics — 2026-11-26

On head `42a9746d7925e023a97445a6fe6cd4db324173fa`, GitHub returned failed
test and catalog check-runs in two attempts: [45764104638](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45764104638),
[45764104610](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45764104610),
[45764097863](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45764097863),
and [45764097859](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45764097859).
The four job records (`139720744840`, `139720745028`, `139720723424`,
`139720723296`) each have one pre-start annotation with the alternatives quoted
above, no executed steps, and no retrievable log (`BlobNotFound`). The combined
status has no entries. This is direct evidence of an account-level pre-start
gate, but it does not determine whether recent payments or the spending limit
caused it. Do not claim that repository tests ran or assign one alternative as
the specific cause. The exact-head local receipt is separate evidence.

### PR #63 documentation-status head Actions diagnostics — 2026-11-26

On exact head `3bc7162d54ad3ed8a9bdeb158abdb07ccb5b1f66`, GitHub reported two
attempts for the `Python API CI` and `Engineering documentation catalog`
workflows:
[45849519063](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45849519063),
[45849519064](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45849519064),
[45849506095](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45849506095), and
[45849506083](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45849506083).
The associated `test` and `symbol-catalog` check runs were `140011906243`,
`140011905569`, `140011859186` and `140011859295`. All failed before job
steps. Each annotation says: “The job was not started because recent account
payments have failed or your spending limit needs to be increased. Please
check the 'Billing & plans' section in your settings.” The records contain no
executed steps, no retrievable logs and no combined status entries. This is
direct evidence of an account-level pre-start gate, but it does not determine
which stated alternative applies. The owner separately confirms quota
exhaustion and zero paid budget; do not attribute these runs to a specific
payment or spending-limit cause.

### PR #63 latest published-head Actions diagnostics — 2026-11-26

On published head
`5ec904dc0be6555d3651f947ef1f02fdd6ce20f7`, GitHub returned two attempts
covering the `Python API CI` and `Engineering documentation catalog`
workflows: [45851811554](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45851811554),
[45851811257](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45851811257),
[45851800821](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45851800821),
and [45851800917](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45851800917).
The check runs were `140019827805`, `140019828418`, `140019790347` and
`140019789961`. All four failed before job steps with the annotation: “The job
was not started because recent account payments have failed or your spending
limit needs to be increased. Please check the 'Billing & plans' section in your
settings.” Their records have no executed steps, no retrievable logs and no
combined status entries. This does not identify which stated alternative
applies; the owner's separate report confirms quota exhaustion and a zero-paid
budget. No repository checks ran in these attempts. The exact-head local gate
receipt is separate evidence.

### PR #64 exact-head Actions diagnostics — 2026-11-26

On exact head `ca97ab61d15347aa271ee9ac8468a0714bdc3402`, GitHub reported two
attempts for the `Python API CI` and `Engineering documentation catalog`
workflows:
[45769634991](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45769634991),
[45769634949](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45769634949),
[45769627687](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45769627687), and
[45769627689](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45769627689).
The `test` and `symbol-catalog` check runs were `139738897979`,
`139738898075`, `139738873183` and `139738873424`. All failed before job
steps. Each annotation says: “The job was not started because recent account
payments have failed or your spending limit needs to be increased. Please
check the 'Billing & plans' section in your settings.” Job records have no
steps, no retrievable logs and no combined status entries. This is an
account-level pre-start annotation; it does not establish which stated
alternative applies. No specific payment or spending-limit cause is inferred.

Metadata-only review of the official Census archives on 2026-11-26 found a
2022 annual-revision notice that its sales spreadsheet was updated at 12:45
p.m. after the 10:00 a.m. release. This confirms that a same-day corrected file
cannot be ordered safely by date alone. Preserve original and corrected file
versions separately and abstain when timestamps cannot distinguish them. No
Census release file was downloaded; see the [Census vintage protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md).

While B-01/B-02 remain open, independent synthetic pilot work now includes
the normalized vintage selector and the fixed-origin, first-estimate Census
baseline evaluator. Both are local and use generated records only. Their
passing tests do not resolve source rights, source-vintage authenticity,
archive completeness or empirical validation.

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

## Historical B-08 diagnostics and runner assessment — 2026-11-25

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
