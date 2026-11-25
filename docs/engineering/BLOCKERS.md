# Blocker and decision register

This register identifies **specific acceptance dependencies**, not
reasons to suspend all development. Baseline is
[PROJECT_STATUS](PROJECT_STATUS.md). Task dependencies live in
[TASK_BACKLOG](TASK_BACKLOG.md). Verify new evidence before changing a
status; never record permission, secret material or deployment approval
that has not actually been granted.

| ID | Scope / current state | Evidence required to resolve | Decision owner | Safe work while blocked |
| --- | --- | --- | --- | --- |
| B-01 | Source-specific rights and handling remain conditional. Owner accepted A+B preparation: UCI #352 event-time research first, then aggregate Census releases; no real source has been acquired or approved for processing. The current PR #57 work adds only a synthetic UCI evaluator and source/privacy plan. M5 remains NO-GO. | Before UCI acquisition/processing: recheck original terms; record attribution/change notice, exact source manifest, minimal projection, local-only storage, retention/deletion and privacy review. Census needs its own terms, attribution, snapshot and handling review. | Project owner / appropriate rights reviewer | Keep automated tests synthetic; improve offline adapters, cards, manifests and privacy controls. No data in Git, CI, logs, prompts or external services. |
| B-02 | UCI `InvoiceDate` is event time, not historical availability. The prepared UCI evaluator cannot make a point-in-time claim. Census point-in-time evaluation is not evidenced by reviewed, complete original release vintages; a protocol exists, but no vintage data was acquired. | For UCI, keep `event_time_retrospective_unverified_availability`; point-in-time remains blocked. For Census/conditional ALFRED, verify release dates, original bytes, vintage completeness, revision boundaries and a locked temporal protocol before scoring. | Evidence/model reviewer | Synthetic cutoffs, leakage and abstention regressions; use the prepared UCI and Census protocols. Do not infer availability or fabricate missing vintages. |
| B-03 | Independent checkpoint authority operation | G-01–03 implementation evidence, actual separately protected storage, signer key custody, operator identity/access policy, monitoring, recovery and audit review | Owner / infrastructure and security operator | Local test service, generated keys, fake/loopback transport, bounded CAS, restore and fork tests; no external deployment |
| B-04 | Optional WorldKernel runtime acceptance. A strict request mapper already exists in PR #55; no MirrorMind-to-engine execution is verified. | Pin the reviewed WorldKernel commit; run its local versioned exchange with a registered synthetic inventory world; enforce timeout and MirrorMind operator caps; validate `worldkernel.result.v1` and test missing/runtime-error paths. Cross-repository source changes remain out of scope. | Project owner / engine maintainer | Continue compatibility inspection and local optional-adapter work against a read-only upstream checkout. No hard dependency, service deployment, real forecast or invented result. |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | PR #57 follow-up `8f906b8c0735bb04434c2c0a40efc2c3297df93b` timed out in the full pytest gate after 900 seconds; the separate exact-head `1bf178b` review passed 700 tests and all six checks. In this checkout, a focused API capability test under the restricted sandbox produced a faulthandler stack at Windows Proactor `_fallback_socketpair` / `socket.accept`; the same command in an elevated local process passed in 0.57 s. This demonstrates a sandbox-correlated local hang, but does not establish the cause of the historical 8f906b8 timeout or prove every full run passes. | Preserve historical and current failures separately. Run the exact gate where local socketpair creation is permitted; if it recurs there, capture bounded thread diagnostics on the exact interpreter/dependencies without skipping or extending tests. | Codex / project maintainer | Use the documented exact-head gate under the already approved local execution path; do not infer a product-code cause from the restricted-sandbox stack. |
| B-08 | GitHub Actions allowance is exhausted per owner; no paid usage or spending-limit increase is authorized. At PR #57 head `1bf178b5c4b31bcd68072b69748a14249c6c2649`, four checks failed before job start with the account message recorded below. Official CI is not a code test result. The owner-controlled branch-protection API reported `Branch not protected` and applicable rules `[]`; no settings were changed. | Ordinary official execution needs an owner-selected no-cost path. Keep repository settings and checks unchanged; no paid usage, limit increase, CI impersonation or weakened verifier. | GitHub account owner / repository administrator | Use the temporary local gate on exact clean heads and independently review the integrated candidate. A no-cost self-hosted option was assessed below but is not selected; do not repeatedly rerun the same pre-job failure. |

On PR #57's published head `25fb95ee84e1e431e206716355acab70448a5a54`, official
`test` [45623569731](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45623569731)
and `symbol-catalog` [45623569774](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45623569774)
both failed. Their check records each report one annotation, but the jobs expose
zero steps and `logs_url: null`; downloading either job log returned `BlobNotFound`.
At that time, the configured GitHub connector rejected the annotations
endpoint and the local GitHub CLI could not reach `api.github.com`; this was
an evidence gap on that earlier head, not a cause finding. The later exact
diagnostic below applies to head `1bf178b` only.

The later published head `fa1307b8e8a6dd8fc0f3fe54a072a1a4d5582da7` produced
failed `push` runs for `test` [45629175027](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45629175027)
and `symbol-catalog` [45629175149](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45629175149),
and failed `pull_request` runs for `symbol-catalog`
[45629185787](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45629185787)
and `test` [45629185886](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45629185886).
All four jobs expose zero steps and null log URLs; download attempts returned
`BlobNotFound`. Each check advertised one annotation, but the configured
connector rejected the annotations endpoint during that earlier inspection.
This records the verified `fa1307b` runs, not a claim about later heads.

### Latest PR #57 evidence — head `1bf178b`

The owner recovered annotations for checks `139259693576`, `139259693712`,
`139259664116` and `139259664989`. Each says: “The job was not started because
recent account payments have failed or your spending limit needs to be
increased. Please check the 'Billing & plans' section in your settings”. The
owner separately confirms exhausted Actions allowance and no paid usage
authorization. The annotation's alternative wording does not prove which
account subcondition applied. All four checks started zero workflow steps;
they are not test or catalog results. The owner-controlled branch-protection
API reported `Branch not protected` and applicable rules `[]`; no settings
were changed. See the owner's
[diagnostic note](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164870326).

### B-01/B-02 accepted research direction; source gates remain open

The owner accepted the sequential A+B plan described in the
[UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md): first prepare
UCI #352's privacy-minimized event-time retrospective pilot, then prepare an
aggregate Census release-vintage pilot. ALFRED is conditional on free
authorized access, applicable series terms and adequate archive evidence.
No data or credentials were acquired. Before processing UCI bytes, verify the
exact original terms and attribution/change notice, project only product/day/
positive quantity after cancellation classification, record a private local
snapshot manifest, retention/deletion plan and reviewer. Keep raw records out
of Git, CI, logs, prompts and external services. UCI `InvoiceDate` remains
event-time only. Census as-of evaluation needs original release files and
complete per-vintage evidence; do not use current time-series exports as
historical vintages or fabricate gaps. M5 remains NO-GO. A+B is a research
direction, not source-use approval; B-01/B-02 remain open.

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

### B-07 — exact-head timeout evidence

The previous `8f906b8` gate timed out in pytest after 900 seconds, and a
focused diagnostic had remained pending at
`tests/integration/test_api.py::test_health` for 30 seconds without a stack.
The independent exact-head review then used a fresh detached worktree at
`1bf178b5c4b31bcd68072b69748a14249c6c2649`, Python 3.13.5 and its own
offline-synced environment. Focused `test_health` passed (1 test in 1.07 s).
The documented gate passed 700 tests and all six checks in 23.18 s, with one
existing Starlette/httpx warning. Its receipt was recorded at
`%TEMP%\\mirrormind-independent-pr57-1bf178b.json` at
`2026-11-25T14:11:19.775672+00:00`. The original checkout was untouched.
The timeout did not reproduce in this environment; its cause remains unknown,
so neither a code fix nor a fixed environment cause is claimed. The subsequent
UCI change also passed 87 focused tests in the current working tree; this is
not an exact-commit full-gate receipt, which remains pending until the change
is committed. See the
[independent verification note](https://github.com/GustavoMFDS/MirrorMind/pull/57#issuecomment-7164895449).

### B-08 — local gate; self-hosted runner assessed, not selected

Use [LOCAL_QUALITY_GATE.md](LOCAL_QUALITY_GATE.md) for temporary local
validation. GitHub's current billing docs say self-hosted runner usage is free
and does not draw from included compute minutes. That makes it a plausible
no-cost way to execute these workflows, but does **not** prove it would bypass
the recovered pre-start account annotation on this repository: the checks
show zero steps and do not document whether runner assignment was reached.
No workflow or account change was made to test this hypothesis.

A self-hosted runner would execute the PR's checkout and test code on a
project-controlled machine. GitHub warns that self-hosted runners are not
guaranteed to be clean ephemeral VMs and can be persistently compromised by
untrusted workflow code, including code in pull requests against private
repositories. A safer candidate needs a separately authorized, disposable
VM/host, a single-job ephemeral/JIT registration, no secrets or source data,
minimal token permissions, restricted network, image reset and verified
teardown. It still requires a connected runner process, network access,
maintenance and cleanup. No such isolated host is currently selected or
verified in this work context; registering against the owner's workstation
would expose its host and credentials. Therefore do not configure a runner or
edit workflows now. This is a risk/feasibility assessment, not a claim that a
self-hosted route cannot work.

For each reviewable PR head, retain the exact local receipt and independent
review. After stack reconciliation, run a separate six-check gate on the
exact integrated candidate. Keep official Actions status failed or not
executed until GitHub actually executes the workflows.

Sources: GitHub [billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage),
[detailed Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions),
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
