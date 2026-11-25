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
| B-04 | M1E-02 actual WorldKernel runtime is not available in the checked MirrorMind environment. On 2026-11-24 the project `.venv` had no importable `worldkernel` module or installed distribution, and MirrorMind `pyproject.toml` declares no optional engine extra. Read-only inspection of WorldKernel `main` at [`9b133ef`](https://github.com/GustavoMFDS/WorldKernel/commit/9b133ef873f2b6a7206c9c5742d40df4fccdb04a) found package version `0.0.1` in [`pyproject.toml`](https://github.com/GustavoMFDS/WorldKernel/blob/9b133ef873f2b6a7206c9c5742d40df4fccdb04a/pyproject.toml), no published GitHub releases when checked, and a local JSON v1 SDK/CLI contract. The [`exchange guide`](https://github.com/GustavoMFDS/WorldKernel/blob/9b133ef873f2b6a7206c9c5742d40df4fccdb04a/docs/EXCHANGE.md) explicitly says there is no direct MirrorMind integration or network listener. This does not rule out a compatible approved runtime elsewhere. | Pin an approved package/revision and compatibility target; confirm the retail world/revision, trusted fixture, resource limits and cross-repository contract before adapter execution. Verify actual registered-engine result handling with integration tests. | Project owner / WorldKernel maintainer | Preserve the versioned fail-closed mapping, fake-gateway and disabled-engine paths. Do not add a hard dependency, install an unreviewed source, or guess unsupported fields. |
| B-05 | Live LLM/provider use and spend | Explicit credentials, permitted provider/data transfer, price/budget approval, evaluation and safe tool access; keep secrets out of Git | Project owner | Fake provider, retrieval fixtures, tool contracts, safety and budget tests |
| B-06 | Production environment and release | Approved hosting, identities/tenancy, security and privacy review, budget, operational targets, measured load/failure/backup/restore evidence and license/release decision | Project owner / deployment operator | Local integration, reproducibility, auth/isolation, job/monitoring/recovery tests |
| B-07 | Historical restricted-sandbox runs on PR #52 implementation SHA `c51ab30370db47e9f7105c97f870008e4fc442c5` timed out at the 900-second pytest limit. Verbose replay stopped at `tests/integration/test_api.py::test_health`; a standalone loop creation blocked in `socket.accept` inside Python's `_fallback_socketpair` on Python 3.13.5 and also blocked on Python 3.12. The root cause remains unconfirmed. The canonical gate later passed on that exact implementation SHA (696 tests) and on M2-01 SHA `e151f9d9925d83d2b3e27fb88683672a93b48c30` (720 tests, including HTTP capability parity), both using the approved execution environment. B-07 no longer blocks those exact local validations; later docs-only heads still need their own applicable checks. | If a future canonical gate stalls, rerun the exact SHA in an environment where asyncio can create its local socket pair; preserve the failure and do not change app behavior to mask it | Codex execution environment / project maintainer | Use exact-HEAD gates. The M2-01 result is recorded in its change request; the sandbox symptom is historical, not evidence of an application defect. |
| B-08 | Exact check-run diagnostics for #54 `2794abf`, #59 `afce53a`, #60 `cb47456` and #61 `b9a8151` carry the pre-job message that recent account payments failed or the spending limit must be increased. This message does not identify which condition applies. Older #60/#61 heads have one annotation recorded in check-run metadata, but their annotation text was not recovered; do not call those heads unannotated or infer the same message without the text. | Account owner inspects the settings named by the exact annotations; then rerun checks on reviewed heads without changing required workflows or protections | GitHub account owner / repository administrator | Keep exact-head local validation separate from CI; distinguish an explicit payment-or-limit start gate from a confirmed specific account condition; do not claim remote tests ran |


Previously verified B-08 runs: PR #52 latest head `5c307e426c43aee4179e3257d7d367214e8c3a63`
[test 45319452833](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452833) and
[symbol-catalog 45319452852](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45319452852);
PR #53 head `210f0f382938a67e518df688cc4e19c03d3d7af6` runs
[45323540471](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540471) and
[45323540864](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45323540864);
PR #54 runs [45326109821](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109821) and
[45326109808](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109808);
PR #57 runs [45339076005](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339076005) and
[45339075950](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45339075950).
Each was observed with the same account billing/spending-limit annotation.
On 2026-11-24, an initial focused `tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger` attempt in the restricted sandbox produced no output for 60 seconds and was interrupted. A later exact-HEAD canonical gate on M2-01 SHA `e151f9d9925d83d2b3e27fb88683672a93b48c30` passed all 720 tests, including that HTTP parity test. The earlier sandbox symptom does not establish an application failure; its root cause remains unknown.

Exact-head check diagnostics distinguish recovered annotation text from metadata-only evidence:

- PR #54 head `2794abff855665fb65f32af655415c52dde68872`: `test` runs
  [45518448875](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518448875)
  and [45518440891](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518440891),
  and `symbol-catalog` runs
  [45518449130](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518449130)
  and [45518440963](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518440963)
  each have the explicit account annotation, no workflow steps and no logs.
- PR #59 head `afce53a8ebc24261ea33ab705394eecb86459781`: `test` runs
  [45529860767](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529860767)
  and [45529847764](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529847764),
  and `symbol-catalog` runs
  [45529860606](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529860606)
  and [45529847784](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45529847784)
  carry the same annotation and expose no repository steps or logs. The
  annotation text is: “The job was not started because recent account payments
  have failed or your spending limit needs to be increased. Please check the
  'Billing & plans' section in your settings”. It does not distinguish those
  account conditions.
- PR #60's historical head `6374f0bb9a981271cb9340a190dcdebec6263cc9` runs
  [45476173796](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173796)
  (`test`) and
  [45476173736](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45476173736)
  (`symbol-catalog`) failed before repository steps and logs were unavailable.
  Check-run metadata records one annotation per check, but its text was not
  recovered. PR #61
  head `288021f25e24efc26591b064eafa1d8b4e287ac8` runs
  [45495329331](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329331)
  and [45495329221](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45495329221)
  likewise failed before repository steps with logs unavailable; check-run
  metadata records one annotation per check, but its text was not recovered.
  Do not call either head unannotated or infer a cause or remote test execution.
- PR #60 review-correction head `cd9542156d8ab3cec2876ab07f3aa1c22dd00c37`
  runs [45534005860](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534005860)
  (`test`) and
  [45534005856](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534005856)
  (`symbol-catalog`) completed as failures before any job step. Both job
  records have empty step lists; log retrieval returned `BlobNotFound`. The
  check-run API reports one annotation per check, but the annotation text for
  this historical head was not retrieved. Do not infer its cause from a
  different head.
- PR #60 earlier documented head
  `cad28d8c1e38dfd1cf8007c1b50853132d719ee3` has `test` runs
  [45534347123](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534347123)
  and [45534341307](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534341307),
  and `symbol-catalog` runs
  [45534347132](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534347132)
  and [45534341412](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45534341412).
  The check-run annotations state: “The job was not started because recent
  account payments have failed or your spending limit needs to be increased.
  Please check the 'Billing & plans' section in your settings”. This is an
  explicit account-level pre-job gate, but it does not distinguish payment
  failure from spending-limit state. No repository job steps ran; log retrieval
  for the latest pair returned `BlobNotFound`.
- PR #60 follow-up docs head
  `cb4745635be7d57994d8766b59b40312a6b1702e` has `test` runs
  [45538255051](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538255051)
  and [45538248713](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538248713),
  plus `symbol-catalog` runs
  [45538255077](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538255077)
  and [45538248727](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45538248727).
  Exact diagnostics for all four checks show the same account-level pre-job
  annotation quoted above. No repository job steps ran; no logs were returned.
  The annotation does not distinguish which account condition applies and
  does not represent remote test execution.
- PR #61 documented head
  `b9a8151269287b7264dc1eed0da7ed02a50202f2` has `test` runs
  [45536692432](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536692432)
  and [45536687429](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536687429),
  and `symbol-catalog` runs
  [45536692334](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536692334)
  and [45536687419](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45536687419).
  Their annotations carry the same payment-or-spending-limit pre-job message
  quoted above. No repository job steps ran; logs were unavailable. This does
  not establish which account condition applies or provide remote test results.

### Self-hosted runner assessment

GitHub documents no per-minute GitHub runner charge for self-hosted runners;
the owner still carries VM, isolation, monitoring and teardown costs. A private
repository is not an isolated trust boundary for a persistent runner because
read-access users may submit pull requests. See [secure use](https://docs.github.com/en/actions/reference/security/secure-use),
[runner setup](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)
and [Actions billing](https://docs.github.com/en/actions/concepts/billing-and-usage).
If chosen, the candidate is one just-in-time runner in a disposable VM per
check, destroyed afterward; use existing workflow job names/commands, no
secrets, read-only short-lived token, no host credentials or private-network
access, and retain image/egress/teardown evidence. This design has not been
implemented or security-tested, and there is no evidence it bypasses the
account pre-job gate. No runner or workflow change was made.

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
