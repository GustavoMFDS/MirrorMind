# Blocker and decision register

## Current B-07/B-08 reconciliation after PR #92 - 2026-11-28

Current `main` is `843fc5f4ea8310947f2626f486561de56401f3e2`; PRs #87–#92 are
merged. The complete local gate on this exact integrated SHA passed 1,027
tests, zero skips and all six checks with the reviewed WorldKernel pin; the
receipt is recorded in [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md). This is
local validation, not official Actions. The owner reports GitHub Actions' included allowance exhausted; no
paid spend, purchased capacity or limit increase is authorized. Current
exact-head queries found workflows on #93 (`76f0402`) and #99 (`b8695a3`),
with 12 successes and two conditional skips each. The missing
runs on #94–#98 and #100 have a separate, source-confirmed explanation: every
repository `pull_request` workflow currently filters `branches: [main]` in
[`ci.yml`](../../.github/workflows/ci.yml),
[`docs.yml`](../../.github/workflows/docs.yml),
[`quality.yml`](../../.github/workflows/quality.yml),
[`pages.yml`](../../.github/workflows/pages.yml), and
[`research-maintenance.yml`](../../.github/workflows/research-maintenance.yml).
GitHub evaluates that filter against the PR target/base branch, and #94–#98
and #100 target parent feature branches. Their missing checks are therefore
expected from the configured filter; they are not evidence of billing failure
or successful validation. This does not explain historical pre-start failures
or establish current account allowance. Preserve the local gate for the
stacked PRs; do not alter workflow filters, spend, runners, checks or
protections without a separate decision.

Use the temporary complete local gate in
[LOCAL_QUALITY_GATE.md](LOCAL_QUALITY_GATE.md). No check, verifier, branch
protection or workflow was disabled. A self-hosted runner remains an evaluated
but unconfigured option: it would require a trusted maintained host, runner
registration credentials, patch/isolation design and repository-administrator
action. Current local validation is authorized and sufficient for independent
review preparation, so no runner registration or external permission is
needed for this increment. Do not expose registration tokens or attach a
persistent runner without a separate owner decision.

B-07 now has a reproduced local boundary: on exact candidate SHA
`2d592bd50b15c3b0d463c94e58a70be78553e8a6`, pytest stalled in the first
`TestClient` request while Python 3.13's Windows Proactor created its local
socketpair (`socket.accept`). The same isolated `test_health` passed in 1.38s
outside the restricted sandbox, and the unchanged complete gate passed
1,032 tests, zero skips and all six checks in 45.01s with loopback available.
The sandbox timeout is not attributed to product behavior. The permanent
local gate remains fail-closed and unchanged; see the exact receipt in
[LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md). Preserve zero paid spend and do
not infer official Actions state from this local result.

PR #99's current published head is
`b8695a37ccb8ec68aebc75003f5d3c0ed3879e5b`. Its local six-check gate passed
1,032 tests, zero skips and all six checks; GitHub recorded 12 completed
successes and two workflow-conditional skips (`deploy`,
`release-rehearsal`). A local CLI smoke on that SHA parsed the success and
history-abstention reports and confirmed action authority remained false. This
evidence applies only to that PR SHA and does not establish a billing cause or
a result for later commits. The live PR body holds current evidence:
[PR #99](https://github.com/GustavoMFDS/MirrorMind/pull/99).

## Historical pre-#87 B-07/B-08 reconciliation - 2026-11-28

PR #88 merged the cryptography 50 lock update at exact `main` commit
`00e6cf11ac05a94055242573fd3cfc18086bad10`. Its exact-SHA query returned 11
completed official check-runs, all successful: [test and Python compatibility](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46094517994),
[quality, package and container smoke](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46094518014),
[symbol catalog](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46094517959),
[CodeQL analyses](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46094517866),
[dependency graph](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46094523742),
and [Dependabot](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46094626219).
This is evidence for that exact main SHA only. It does not establish billing
state or explain earlier pre-start failures. Preserve the owner's zero-paid-
spend limit and do not change protections, workflow checks or runners.

PR #87 is open at published head
`c69f93b5428b0b1bb265c7039e38d1d99ea90d10`, which includes the latest `main`
through merge `66b591317b375a270b5d0ed682c94e161d52a956`, the provider-turn
correction and its documentation. Its exact local gate passed 1,019 tests,
zero skips and all six checks. Its exact official query returned 12 successful
check-runs and two workflow-conditional skips (`deploy`, `release-rehearsal`).
The independent review thread remains unresolved. These results do not
constitute reviewer approval or merge authorization; never transfer evidence
between SHAs.

On exact local SHA `66b5913`, the restricted sandbox attempt produced no
output and was interrupted before the local gate's 900-second limit; no
receipt was emitted, so this attempt is not a pass or a test failure. The
unchanged full gate then passed on the same clean SHA with loopback permitted
in the authorized local environment in 34.21 seconds. This is consistent
with the known `TestClient`/Windows loopback limitation for this run; it does
not resolve the separate historical `8f906b8` incident. See [B-07 below](#b-07-pr-65-restricted-sandbox-diagnostic---c6c1326)
and [the gate record](LOCAL_QUALITY_GATE.md).

## Historical B-08 reconciliation before #87 merge - 2026-11-28

The exact published M2-03 head `c69f93b5428b0b1bb265c7039e38d1d99ea90d10`
received 12 successful official check-runs and two conditional skips on
2026-11-28. These runs show Actions executed on that SHA but do not explain
historical pre-start failures or identify an account billing cause. B-08's
historical cause remains unresolved; the current M2-03 review correction is
not blocked on hosted checks. Do not spend, change spending limits, alter
protections or infer a remedy from this observation.

GitHub-hosted Actions are operational on reviewed PR head
`df7c450523a8f3475e0a8161936f6ac80e705720` for PR #77: all nine observed
contexts succeeded, including the new `quality` and `package` jobs. See the
[exact-head run record](LOCAL_QUALITY_GATE.md). PR #77 merged normally as
`540c47411898cc820ac651c19430017ecd8c20fe`; the combined-status query for
that merge SHA returned no individual entries, so the PR-head result is not
presented as exact-merge CI. PR #78's final docs-only head
`8c8f8627a7162cb766a70d264569d3fcc2d442c8` later passed six observed jobs
across documentation catalog, Python API test/compatibility and repository
quality/package workflows (runs `46072345590`, `46072345631` and
`46072345603`) before merging at `291562a`. Combined-status queries for its
merge SHA and current `main` returned no entries; keep that evidence scoped to
the PR head. PR #79's exact head also ran the public site build, docs catalog,
Python API and quality workflows; all applicable jobs succeeded and the
main-only deployment was skipped. PR #80's exact head ran docs catalog,
research benchmark, public site, Python API and quality workflows; all
observed applicable jobs succeeded, while main-only deployment and manual
release rehearsal were skipped by their conditions. Exact run links and local
receipts are in [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md). PR #81's exact
head `41e6db8618a00c93f3a00ca6638ed96ab623dcbc` ran five workflows: all nine
applicable jobs passed, including repository quality, strict retrieval typing,
package smoke, container smoke and Python 3.12/3.13 suites. Its main-only
deployment and release rehearsal were skipped. PR #81 merged normally as
`10b94c9d7b01bc7072a18d8124cbc8090a6b1925`; the combined-status query for that
merge SHA returned no entries. Earlier pre-start failures remain unexplained;
their alternative account annotations do not establish a cause.
PR #82's initial exact head `d542e5e129e091dc649e1a187c96e18c59ccc695` then
completed 12 successful official checks, including strict retrieval typing;
deployment and release-rehearsal jobs were skipped by their conditions. One
Node.js 20 deprecation annotation was non-blocking. These results are scoped to
that PR head, not later commits or `main`.
PR #82 later merged normally at `c31ecd6dbf3f68be8726bdba2b23a813226c2618`;
its 12-check result remains scoped to exact PR head
`f6fa2edd80b38b42c3374813816929c2c9d8b2cc`, not the merge commit or current
`main` `d41e661d298255957979779691c2f9f4dbf36461`. Historical pre-start
failures remain unexplained; no billing cause is established.

The owner-reported included-allowance exhaustion and zero-paid-budget decision
remain constraints, and no spending setting, paid service, self-hosted runner,
protection or verifier was changed. However, the exact PR #87 head
`2d71d3931cff494ddf0788f663de89efc2bc649f` did run on GitHub Actions: 12 of 14
check-runs succeeded; `deploy` and `release-rehearsal` were skipped by their
workflow conditions. The successful checks include test, Python 3.12/3.13
compatibility, repository quality/package, container smoke, symbol catalog,
site build, benchmark, CodeQL and both CodeQL language analyses. Its workflows
use public `ubuntu-latest` standard runners; GitHub documents those runners as
free for public repositories ([billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage),
[runner selection](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job?apiVersion=2022-11-28)).
This observed run does not reveal account billing state and does not explain
the historical pre-start failures. The local host still has no Docker engine
pipe, although the official container-smoke check passed for this exact PR
head. The exact-head links and local receipts are in
[LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md). Keep local validation separate
from check-run evidence; query the exact PR head before recording new status.
No self-hosted runner or protection change is needed for the observed PR run.
Preserve the local six-check gate and pinned WorldKernel validation.

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | UCI #352 local non-commercial research is owner-approved in MM-017–MM-024, with CC BY 4.0 attribution, local-only retention and a 2026-12-26 deletion deadline. The 2026-11-27 clarification classifies six-digit identifiers as normal, uppercase `C` plus six digits as cancellation, and other single-ASCII-letter-plus-six-digit identifiers as an aggregate-only unverified class; unsupported forms fail closed. The unchanged 250,000 product-day group ceiling was exceeded before a complete projection, so no evaluation or metrics exist. The clarification changes only exclusion counts, not accepted sales rows/group cardinality; it does not permit chunking, sampling or a larger cap. Census remains preparation-only. Direct Census original-release files are the proposed route; the current one-file inspection candidate is the October 2026 Advance MARTS report PDF (CB26-181, release November 17), with September 2026 now in the historical archive. This identifies a candidate only, not permission. Census public-use guidance calls for attribution when deriving estimates, and a general policy says employee-created works are generally not copyright-protected in the United States, with exceptions; neither resolves notices, provenance or third-party rights for a specific MARTS artifact. FRED/ALFRED is NO-GO under current posted FRED Services/API terms for MirrorMind development and local archival use: ALFRED is within the Services terms, which prohibit storage/cache/archive and software/AI development; the API also prohibits these uses. Reconsider only if the St. Louis Fed authorizes the intended service/API use in writing or changes its terms, and separate series-owner rights are cleared. This does not determine rights for original Census files. M5 remains NO-GO. | Preserve the UCI snapshot controls and do not claim empirical results without a complete projection. Any design that changes the source-call bounds, samples/partitions observations, or resumes after another fail-closed stop needs separate owner approval and model-review acceptance. For Census, preflight the public publisher index, landing pages, posted notices and available provenance. Before acquiring any file bytes, the owner must approve the exact October 2026 report artifact listed in the [Census vintage protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md) for quarantined local inspection of embedded notices, provenance and schema only; no value parsing or evaluation. Delete the inspection copy immediately after review and no later than the expressly approved retention limit. Then obtain artifact-specific rights review for ambiguity and a separate owner go/no-go for processing, including bounded purpose, attribution, access-controlled storage, proposed 30-day maximum retention/deletion and outputs. Citation guidance is not a file-specific license. Do not create a FRED API key, fetch FRED/ALFRED values or retain service content unless the St. Louis Fed authorizes the intended service/API use in writing or changes its terms, and separate underlying series rights permit the use and retention. | Project owner / appropriate rights reviewer | Keep automated tests synthetic; refine direct-source manifest, archive completeness checks, deletion checklist and privacy controls without retrieving real Census bytes |
| B-02 | Point-in-time availability and empirical evaluation remain open. UCI `InvoiceDate` is event time with no verified first-publication field; all UCI output stays `event_time_retrospective_unverified_availability`. Census's annual-revision index spans January 1992 through August 2026 but does not prove first-release completeness. The current Census sales page identifies the October 2026 advance release dated November 17, while the historical release page explicitly omits current data and presently lists September as its newest month; neither establishes a complete first-release vintage set. The schedule says 8:30 a.m.; the current release-specific metadata indicates Eastern Standard Time, but historical same-day corrections may still be ambiguous. The April 2025 annual revision removed nonemployers, creating a source-definition boundary. | For UCI, retain event-time labeling and never derive `available_on` from `InvoiceDate`. Before Census acquisition, approve and inventory original first-release artifacts and exact publication boundaries, methodology edition, and a pre-registered chronological 60/20/20 development/validation/locked-holdout split. Use date-only strict-before cutoffs where timestamps/timezones cannot be authenticated; preserve gaps and abstain. Compare first estimates against fixed lag-12 and trailing-12-month baselines at 1/3/6 horizons; keep later revisions separate. Require 60 matched holdout origins per horizon for proposed 12-month block-bootstrap uncertainty, or report descriptive metrics only. Same-day corrections without orderable timestamps/original bytes remain ambiguous. | Project owner with evidence/model reviewer | Maintain synthetic delay, missingness, leakage and holdout regressions; refine the Census release inventory and versioned manifest without fabricating vintages |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | The narrow local M1 runtime is implemented against reviewed WorldKernel commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`: M1E-02 runs its synthetic inventory demo and M1E-04 adds a fixed MirrorMind-owned policy world through the same optional worker. PR #62 was independently approved and merged at `a456034`; its post-merge exact-main gate passed 835 tests, zero skips and six checks with the reviewed pin (final review evidence: [comment 7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)). Broader service acceptance remains open: local process bounds do not provide hostile-code isolation, CPU/memory quotas, deployment controls or a general plugin contract. No WorldKernel repository edit is in scope. | Broader service acceptance needs its own contract, admission, authentication and operational isolation review; any external-repository change needs separate authorization. | Project owner / engine maintainer | Keep the dependency optional and policy world code-owned; use synthetic tests and document broader service limitations |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Local M2-03 scripted provider, fixed synthetic retrieval/decision tools, strict contracts, refusal and prompt-injection regressions; no live provider or provider-data transfer |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | The historical timeout on `8f906b8` remains unexplained. On integrated candidate `e3e55d4635a2ee0dd355de995ff704cca4afe0e3`, the sandboxed gate timed out in `pytest` at its 900-second limit (receipt `results/local-quality-gate-e3e55d4635a2ee0dd355de995ff704cca4afe0e3.json`). A diagnostic faulthandler trace on `tests/integration/test_api.py::test_health` stopped in Starlette TestClient -> AnyIO -> Windows asyncio Proactor self-pipe initialization at `socket.accept`; an isolated `socketpair()` probe also failed to return within five seconds in the sandbox. Without source or test changes, that exact test passed outside the sandbox (one existing Starlette deprecation warning), and the complete exact-head gate passed 989 tests, zero skips and all six checks (receipt `results/local-quality-gate-e3e55d4635a2ee0dd355de995ff704cca4afe0e3-workspace.json`). This reproduces a sandbox loopback-socket restriction for this run; it does not explain the earlier `8f906b8` incident or establish an application defect. | If the symptom recurs, capture the exact SHA, interpreter/dependency paths and a bounded faulthandler/thread dump. Run the unchanged gate with local loopback access only after confirming tests do not use external services; do not raise its 900-second check timeout or skip the health test. | Codex execution sandbox / project maintainer | Preserve both receipts, use the documented six-check gate, and distinguish this environment-specific timeout from a code failure; do not weaken checks or infer the old timeout's cause. |
| B-08 | The owner reports included allowance exhaustion, but exact PR head #93 (`76f0402`) and PR #99 head `b8695a3` each had 12 successful runs and two conditional skips. Current `pull_request` workflows filter target branch `main`; #94–#98/#100 target parent branches and therefore have no workflow runs under these filters. This explains those missing runs, but not historical pre-start failures or account allowance. No paid spend or limit increase is authorized. | Preserve exact-SHA evidence; if a failure recurs, collect the run annotation/state before assigning a cause. | GitHub account owner / repository administrator | Use authorized temporary local full gate for stacked branches. No runner, protection, workflow or verifier changes; do not spend, register runner or infer billing cause. |

## PR #65 parser-review reconciliation - 2026-11-27

The latest independent synthetic review reproduced two structural cases after
the first correction: a repeated `<v>` inside one selected quantity cell could
overwrite the earlier value, and a selected cell could mix scalar `<v>` and
inline `<is>` payloads. Commit `6df8af1` rejects repeated scalar values and
ambiguous mixed payloads in both worksheet passes, while preserving valid
ordered rich-text runs. It does not change the UCI-only invoice policy, generic
projection contracts, bounds, or excluded `Description` handling.

The 9 targeted structural regressions failed on the pre-fix parser; the 10
focused cases passed after correction, including the rich-text compatibility
control. The UCI workbook unit and integration suites passed 75 tests; Ruff
passed on the changed Python files. These are synthetic parser tests. The
source stopped above 250,000 groups and has no complete projection, exclusion
count or empirical score. The later MM-024 owner clarification matches the
existing parser policy and does not reduce group cardinality; the independent
review accepted the bounded result and PR #65 merged normally at `51c90d2`.
The complete local
gate on code head `35bff7824970ebc511e05add240088b2ffd74057` and documented
head `d454b48477af4691a363622ecf8b2fd85a7e5a60` passed
(968 tests, zero skips, six checks, reviewed WorldKernel pin), and all seven
observed GitHub checks succeeded. Comment `7227559961` records the correction
and evidence for review finding `7226309300`; independent acceptance is in
comment `7227890501`. Any later tracked change needs its own exact-head gate and check
observation. See the [reader walkthrough](UCI_WORKBOOK_READER.md),
[change request](changes/M1B_01_UCI_REAL_SOURCE_PILOT.md) and
[PR #65](https://github.com/GustavoMFDS/MirrorMind/pull/65).

### B-07 PR #65 restricted-sandbox diagnostic - `c6c1326`

A restricted-sandbox full-gate attempt on exact code head
`c6c1326be9332e51b160931de4dd994d54868793` timed out in
`tests/integration/test_api.py::test_health`. An isolated run of that test
waited in the restricted executor and passed in 1.27 seconds with loopback
permitted. The unchanged exact SHA then passed its full 881-test, zero-skip
six-check gate; see the two receipts in
[LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md). This supports a loopback
restriction for this reproduction only. It does not explain the historical
`8f906b8` timeout, GitHub Actions or the newer parser candidate.

### PR #63 pre-start checks — head `2764e60` — 2026-11-26

Two automatic workflow attempts created four failed checks on exact head
`2764e60e445281d4dbe56715a5f71fd4640c0f1d`:

| Check | Run | Job | Result |
| --- | --- | --- | --- |
| `test` | [45876594693](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45876594693) | `140105112634` | Failed before repository steps |
| `symbol-catalog` | [45876594601](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45876594601) | `140105111098` | Failed before repository steps |
| `test` | [45876583141](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45876583141) | `140105071567` | Failed before repository steps |
| `symbol-catalog` | [45876583156](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45876583156) | `140105071542` | Failed before repository steps |

All four check annotations contain the same message: “The job was not started
because recent account payments have failed or your spending limit needs to be
increased. Please check the 'Billing & plans' section in your settings”. This
states alternatives, not a diagnosis. The owner separately reported exhausted
Actions quota and a zero-paid budget; do not infer a payment failure or a
specific account setting from the annotation. Job records have no executed
steps or log URLs; the commit has no combined status entries. Therefore these
checks provide no test or catalog execution evidence. The local exact-head
gate is separate: it passed 882 tests, zero skips and six checks at
`2026-11-26T18:30:26.772586Z` with WorldKernel at the reviewed source pin;
receipt `results/local-quality-gate-2764e60e445281d4dbe56715a5f71fd4640c0f1d.json`.
No manual rerun, paid usage, workflow/protection change or runner registration
was made.

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

### PR #63 Actions diagnostics — head `44b128c` — 2026-11-27 UTC

On documentation commit `44b128c4f7768117148dc23f7c71b3e2e9cd86a4`, two
automatic workflow attempts produced four failed checks. Runs
[45921268652](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921268652),
[45921268535](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921268535),
[45921262108](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921262108)
and [45921262111](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921262111)
reported check runs `140252309005` (`test`), `140252308963` (`symbol-catalog`),
`140252287687` (`symbol-catalog`) and `140252287561` (`test`). Each annotation
says the job was not started because recent account payments failed **or**
the spending limit needed to increase. The annotation does not distinguish
those alternatives. The diagnostics show no jobs, steps, logs or combined
status entries; no repository test/catalog command ran. Owner-reported quota
exhaustion and zero paid budget remain separate evidence. The exact-head local
gate passed 882 tests, zero skips and all six checks at
`2026-11-27T01:12:07.694019Z` with WorldKernel `0.0.1` at reviewed source
commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; receipt
`results/local-quality-gate-44b128c4f7768117148dc23f7c71b3e2e9cd86a4.json`.
This is local evidence, not official Actions success. No manual rerun, paid
use, runner registration, spending-limit change or workflow/protection change
was made.

### PR #63 Actions diagnostics — pre-source-policy head `0a24c` — 2026-11-27 UTC

On published head `0a24c01c914592a718380a350dc35f56ce59d9ef`, two automatic
workflow attempts produced four failed checks: test runs
[45921856066](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921856066)
and [45921861735](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921861735),
and symbol-catalog runs
[45921856041](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921856041)
and [45921861784](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45921861784).
Their check runs (`140254188569`, `140254205500`, `140254188611`,
`140254205791`) each report one annotation. The connected diagnostics could
not retrieve annotation text. All four jobs returned empty step lists and log
downloads returned 404; the combined-status endpoint returned no statuses.
This establishes failed checks without retrievable execution evidence, not a
specific cause. The owner's allowance report remains separate evidence. No
manual rerun, paid use, runner registration or workflow/protection change was
made. PR #63 exact local gate on this head passed 882 tests, zero skips and all
six checks; its receipt is `results/local-quality-gate-0a24c01c914592a718380a350dc35f56ce59d9ef.json`.
Local evidence is not official Actions success.

### PR #63 source-policy head Actions diagnostics — `47cdb58` — 2026-11-27 UTC

Two automatic workflow attempts on exact head
`47cdb587b0deab19835acd1435e4bd028ba28519` produced four failed pre-start
checks:

| Check | Run | Check run |
| --- | --- | --- |
| `test` | [45929648150](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45929648150) | `140279056393` |
| `symbol-catalog` | [45929648298](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45929648298) | `140279056864` |
| `test` | [45929642603](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45929642603) | `140279038223` |
| `symbol-catalog` | [45929642649](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45929642649) | `140279039566` |

Each check annotation says the job was not started because recent account
payments had failed **or** the spending limit needed to increase. It does not
identify which alternative applies. Diagnostic responses returned no jobs,
steps, logs or combined status; no repository tests or catalog checks ran.
The owner separately confirms Actions allowance exhaustion and zero paid
budget. That is separate evidence, not proof of which annotation condition
triggered. No cause is inferred. The exact local gate on this SHA passed 882
tests, zero skips and six checks at `2026-11-27T02:38:46.324939Z`; receipt:
`results/local-quality-gate-47cdb587b0deab19835acd1435e4bd028ba28519.json`.
It is local evidence, not official Actions success. No manual rerun, paid use,
runner registration or workflow/protection change was made.

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

### B-01/B-02 source proposal update — 2026-11-27 UTC

The reviewed direct-source candidate is the original Census MARTS historical
release file for national seasonally adjusted Retail and Food Services total
sales. The exact table row, units, source notices and rights must be verified
from the selected artifact before processing. A concrete inspection candidate
is the September 2026 first-release PDF [`adv2609.pdf`](https://www2.census.gov/retail/releases/historical/marts/adv2609.pdf),
linked from the official archive and dated October 15, 2026 in release
metadata. It is a one-file inspection proposal only, not rights clearance or
approval to process values or acquire a vintage set. Census's index lists known
missing releases and an interval when advance sales were not produced; its
current release schedule says 8:30 a.m. but does not state a timezone in the
table. Index and search-result excerpts are not an artifact-specific license
or complete vintage inventory.

Official Census [citation guidance](https://www.census.gov/about/policies/citation.html)
directs users who derive estimates from disseminated tables to cite Census as
the source of the original data and says analytical conclusions are the user's
responsibility. The [Research Transparency and Public Access policy](https://www2.census.gov/foia/ds_policies/ds027.pdf)
states that Census employee-created works are generally not protected by U.S.
copyright, while noting exceptions for foreign copyright and non-Census
creators. These sources support a concrete attribution pattern, but do not
establish the creator or notices of a selected MARTS file and do not grant
third-party rights. Search previews displayed published release content, but
no exact artifact was downloaded into the workspace or pilot store for review;
no blanket rights or redistribution claim is made. See the [Census protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md)
for the artifact review and citation checklist.

Current FRED Services terms apply to ALFRED and the API and prohibit storage,
caching or archiving service content. API-specific terms additionally prohibit
access in connection with software/AI development and API-associated storage.
The FRED `RSAFS` page names Census as the source; it does not establish rights
to retain FRED/ALFRED content or settle rights for the original Census files.
Accordingly, do not use FRED/ALFRED for this pilot unless written permission or
revised terms explicitly allow the intended development and retention.

Concrete proposed approval package: (1) direct Census MARTS original files,
one verified national seasonally adjusted total-sales row; (2) non-commercial
internal research with Census attribution and explicit analyst-responsibility
disclaimer, no redistribution of files or row-level values;
(3) preflight publisher metadata, then seek explicit owner approval for one exact
artifact to be fetched into local quarantine for embedded notice, provenance
and schema inspection only; do no parsing or evaluation, delete it immediately
after review and no later than the approved retention limit; request artifact-
specific rights review for ambiguity, then obtain separate owner go/no-go
before processing;
(4) access-controlled local storage, no Git/CI/log/prompt or external-service
copies, and 30-day source/value-bearing-artifact retention followed by
deletion, keeping only rights/citation metadata, hashes and sanitized audit
results; (5) chronological 60/20/20 development/validation/locked holdout,
first estimates as primary targets, fixed 1/3/6-month lag-12 and trailing-mean
baselines, and separate revised-value sensitivity; and (6) date-only
strict-before cutoffs, preserved archive gaps and abstention on ambiguous
same-day corrections. A proposed 12-month moving-block bootstrap requires 60
matched holdout origins per horizon; below that, results would be descriptive
without a winner claim. These conditions remain proposals, not owner
authorization or evaluation evidence. No Census source was acquired.

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

### PR #64 exact-head CI observations — 2026-11-26

For head `aec18f6f8a21be7069fab3ed2409fe68540c45a0`, GitHub reported the
`test` run [45768693223](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45768693223)
and `symbol-catalog` run
[45768693542](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45768693542)
as failed. The job records `139735795282` and `139735795951` have no steps;
the connector returned no log artifact (`BlobNotFound`). Therefore no
repository tests or catalog check are evidenced remotely, and this observation
does not establish a specific failure cause. The owner's separate quota
decision remains in force, but it is not attributed as the cause of these
exact runs. No workflow, required check, protection, runner or spending limit
was changed.

The documentation-only head `271f01cae5aacf274d3fa9f9ff2ede34796471ef`
also has a failed `Python API CI` run
[45769344631](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45769344631).
Its `test` job `139737946303` returned no steps, and the log endpoint returned
`BlobNotFound`; the combined commit status contained no status entries. This
second observation likewise exposes no repository test output or specific
cause. The exact-head local gate passed separately; it is not official CI.

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
