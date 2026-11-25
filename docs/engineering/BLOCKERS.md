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
| B-07 | The historical restricted-run timeout on `c51ab30370db47e9f7105c97f870008e4fc442c5` is resolved for the integrated PR #52 head `b431d11bf0ac841ff30353a06263d23fb901307c`: its full local exact-head gate passed at 2026-11-25 03:51:25 UTC, including all 696 tests and five additional checks. The earlier run stopped at `tests/integration/test_api.py::test_health` after 900 seconds; a standalone asyncio socket-pair reproduction blocked before application code on Python 3.12 and 3.13.5. Its cause was never established, so the host/sandbox explanation remains a hypothesis and historical evidence only. | Reopen only if a new exact-head gate reproduces a failure; preserve all API tests and the original result | Codex / project maintainer | Keep the exact-head receipt and historical timeout distinct. Do not skip API tests or change application behavior to mask an environment failure. |
| B-08 | Published PR #52 head `b431d11` runs [45542863564](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863564) and [45542863839](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45542863839) failed with no job steps/logs. Published PR #53 head `79d3679` runs [45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354) and [45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397) failed with no job steps/logs. Their specific causes are not established. An exact annotation on an earlier PR #52 head `e3aedaf` listed failed recent account payments **or** a raised spending limit; it did not distinguish which condition applied. The synchronized local PR #54 candidate has not yet been published. | Account owner inspects the exact account state if a diagnostic identifies it; rerun required checks on reviewed heads and establish whether repository steps execute | GitHub account owner / repository administrator | Keep local exact-head receipts current, preserve required checks and protections, and report Actions as failed until repository jobs execute |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

### B-08 — self-hosted runner assessment

GitHub documents self-hosted runner use as free of its per-minute Actions
charge. The owner still pays for compute, clean images, isolation, monitoring,
log retention and teardown. A self-hosted runner is not established as a fix
for the observed B-08 gate: the annotation says the job was not started due to
one of two account conditions, and no evidence shows that changing runner type
bypasses that pre-job check. Do not change workflows or required-check
protections on this evidence.

If the owner later authorizes a bounded pilot, use a dedicated disposable VM
created from a clean image for each job, registered as an ephemeral
just-in-time (JIT) runner that accepts at most one job. Give it no repository
secrets, set workflow token permissions to the minimum, block private-network
and cloud-metadata access, assign no cross-repository runner group, forward
only scrubbed diagnostics and destroy the VM and disk afterward. A persistent
shared runner is unsuitable because untrusted pull-request code can compromise
its environment; reusing hardware can also leave state between JIT jobs. This
is a design assessment, not a deployed runner or a verified B-08 workaround.

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
