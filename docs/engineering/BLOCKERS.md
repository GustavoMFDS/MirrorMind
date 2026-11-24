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
| B-08 | Official GitHub Actions verification: PR #60 head `6374f0bb9a981271cb9340a190dcdebec6263cc9` failed runs `45476173736` (`symbol-catalog`) and `45476173796` (`test`). PR #61 failed on three successive code/documentation heads: `78a4e5e1ea4dda4b14d0b5313affcb9b9f5da1d1` (runs `45490939631`, `45490939756`), `4c7300f88b6425fb144de657f263f8e9979c40ac` (runs `45492040417`, `45492040445`) and `040d160477a5185f40ec9dbe257362990162a109` (runs `45492555578`, `45492555540`). On all inspected #61 heads, jobs completed with failure but exposed no steps; log downloads returned `404 BlobNotFound`, artifacts and combined commit statuses were empty. The cause of these failures is not established. | Successful required workflows on the exact reviewed head, or inspectable diagnostics and a verified resolution; local gates are not a substitute | Project owner / repository or Actions administrator | Preserve local exact-head receipts, continue tests and documentation gates, keep PRs draft and report Actions status as failed |
| B-09 | Integration of the current review queue: PRs #52–#61 are open drafts and unmerged as of 2026-11-24. Dependent tasks cannot be promoted based on local implementation or tests alone. PR #60 also has the separate failed-workflow evidence in B-08. | Human review and integration decisions for prerequisite PRs; independently inspect required Actions outcomes where workflows run; then reconcile task dependencies against merged heads | Project owner / repository reviewers | Continue genuinely independent ready work, preserve the draft branches and evidence, and do not duplicate slices or assume dependency completion |

B-04 and B-05 may be resolved if an already authorized compatible
runtime or provider is available; do not claim they are unavailable
without checking the relevant evidence. They are prerequisites for
the named real integration, not a prohibition on design and tests.

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
- [PR #60](https://github.com/GustavoMFDS/MirrorMind/pull/60) remains
  draft. Its current exact-head Actions runs failed; connected diagnostics
  exposed neither annotations nor logs. Do not infer an account/billing cause
  from the available current-run evidence.
- [PR #61](https://github.com/GustavoMFDS/MirrorMind/pull/61) also has
  repeated failed `test` and `symbol-catalog` runs on heads `78a4e5e`,
  `4c7300f` and `040d160`. All three sets have no step records or artifacts;
  log downloads returned `404 BlobNotFound`. Cause remains unestablished; do
  not infer billing, account or source-code failure from these incomplete
  diagnostics.
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
