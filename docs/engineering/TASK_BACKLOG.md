# Task backlog — prioritized execution register

## Current checkpoint - 2026-11-28

Remote `main` is `00e6cf11ac05a94055242573fd3cfc18086bad10`, merged through
PR #88 as a child of `d41e661`; its exact SHA has 11 successful official check-runs.
At sync start, PR #87 was open and unmerged at published head
`48fc51db949cf5626b50d3f97b5304388a9b1076`. The latest synchronized
published head before the review correction was `b931bbe2279dd0865f535e0f56e5165ed402ef96`.
The local `codex/m2-03-tool-orchestration-20261127` branch preserves that
history and incorporates `main` through merge `66b591317b375a270b5d0ed682c94e161d52a956`.
The exact merge checkpoint passed the full local gate: 1,014 tests, zero
skips, six checks. That earlier receipt used cryptography 46.0.7. The local
venv is now aligned to 50.0.0. Exact `b931bbe` then passed the local gate with
1,014 tests and zero skips; its exact check query returned 12 successes and
two workflow-conditional skips. Independent review found a `model_copy`
validation bypass. The current M2-03 candidate adds strict plain-data
revalidation and regression coverage; use the live PR for its exact commit,
gate receipt and check state. Correction commit `48e7efe` passed 1,019 tests,
zero skips and six local checks. Re-query after each later push.

| Work | Current state | Next acceptance gate |
| --- | --- | --- |
| M1 synthetic vertical slice | Integrated experimentally through PR #62; M1 empirical evaluation and production acceptance remain incomplete. | Keep claims synthetic until approved source rights, availability evidence, empirical evaluation and service controls are satisfied. |
| UCI #352 empirical pilot | Blocked after the approved call exceeded the 250,000 product-day group limit; no complete projection, exclusion counts or metrics. MM-024 invoice classification is already implemented and documented. | Do not reread, chunk, sample or increase limits. Preserve private-snapshot deletion by `2026-12-26`. |
| B-01/B-02 Census lane | Metadata/protocol preparation only; no Census or FRED/ALFRED values acquired. | Continue no-byte diligence. Exact Census artifact rights and owner decisions precede even file-byte inspection; FRED/ALFRED remains NO-GO absent written permission and series rights. |
| [PR #87 / M2-03 bounded orchestration](https://github.com/GustavoMFDS/MirrorMind/pull/87) | Main sync completed at `66b5913`; independent review correction revalidates nested provider turns before dispatch. Regression tests, walkthrough, debug/learning docs and evidence map are updated. | Exact candidate gate/check status is in the live PR. Obtain independent re-review; keep #87 unmerged until normal review and protections approve. |
| M2-05 usable decision workflow | Planned; depends on M1F-02 and M2-03. | After #87 review/integration, advance the local/API/UI workflow: run status, reproducible report, uncertainty and human review across normal/failure paths. Keep M2-04 real-provider work gated on B-05. |

## Historical review reconciliation - 2026-11-27

Current `main` is `d41e661d298255957979779691c2f9f4dbf36461`, following PR #82's
normal merge at `c31ecd6dbf3f68be8726bdba2b23a813226c2618` and the subsequent
typing-debt/public-coverage-floor commit `128c266`, public dependency-lock
commit `c8b93da` and package-typing gate commit `d41e661`. PR #79 merged at `5100ebf42265e01b65856e7ba91b659ff1b487c7`
with the curated portfolio/index update; PR #80 adds bounded synthetic
benchmarks and read-only release preparation. PR #77 merged normally at
`540c474`, preserving reviewed head `df7c450523a8f3475e0a8161936f6ac80e705720`;
nine official contexts passed on that PR head. PR #78's final head
`8c8f8627a7162cb766a70d264569d3fcc2d442c8` passed the exact local gate (968
tests, zero skips, six local checks) and six observed official jobs across
documentation catalog, Python API test/compatibility, and repository
quality/package workflows (runs [46072345590](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345590),
[46072345631](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345631),
and [46072345603](https://github.com/GustavoMFDS/MirrorMind/actions/runs/46072345603)).
Combined-status queries for `540c474`, the #78 merge and current `main` returned
no entries; do not transfer PR-head results to merge commits. Receipts and
scope notes remain in [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md) and
[REX_QUALITY_PACKAGING](REX_QUALITY_PACKAGING.md).

PR #79's exact head `b5c1bcc3dff7106e2f370c648c836b3251b17f45` passed its
local gate (970 tests, zero skips, six checks); seven observed workflow jobs
succeeded and the main-only `deploy` job was skipped. PR #80's exact head
`e6a28acd5cf0470c8d8628d6ee5957f3815d3f67` passed 976 tests, zero skips and
six local checks; eight observed jobs succeeded, while only the main-only
deployment and manual release rehearsal jobs were skipped. Their workflow
records are linked in [LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md). Combined
status for current merge `7efced5` returned no entries. The benchmark is
observational, and release preparation does not create or authorize a release.

PR #81's exact head `41e6db8618a00c93f3a00ca6638ed96ab623dcbc` passed 977
tests, zero skips, and six local checks. Nine applicable jobs succeeded across
five workflows: docs catalog, public site build, quality/package/container
smoke, API test and Python 3.12/3.13 compatibility, and synthetic research
benchmark. Main-only deployment and release rehearsal were skipped.
Combined-status queries for the PR head and merge `10b94c9` returned no
entries; preserve official workflow evidence at its exact head in
[LOCAL_QUALITY_GATE](LOCAL_QUALITY_GATE.md).

PR #77 resolves the MM-009 wording follow-up alongside REX-09/10. The active
candidate now records the owner's MM-024 UCI clarification. Its branch
`codex/mm009-mm023-reconcile-20261127` is ancestry-merged with current main
at `ccd74d72b7d30cafaef10d36ac44857c629b6a08`. No parser code is needed:
MM-022 already implements the approved UCI-only classification, with synthetic
regressions for supported and rejected formats, aggregate-only exclusion
counts and redaction. This increment updates the decision, dataset/source
records, status and learning material. It is merged through
[PR #78](https://github.com/GustavoMFDS/MirrorMind/pull/78) at
`291562a`; its final head `8c8f862` passed the local gate and six observed
official jobs. It changed no parser contract and did not reread the workbook.

The UCI #352 source call exceeded the owner-approved 250,000 product-day group
ceiling before returning a complete projection. It produced no complete
exclusion count or metrics. MM-024 reclassifies a subset of rows already
excluded before sales grouping, so accepted rows and cardinality do not change.
Do not retry, chunk, sample or raise the cap under this decision. Preserve
snapshot deletion by `2026-12-26`. M1 synthetic end-to-end is integrated;
M1 empirical and production acceptance remain incomplete.

**Baseline:** main `d41e661d298255957979779691c2f9f4dbf36461`. PR #52–#59 were
incorporated through #62; #60/#61/#64 through #66; Census #63 through #67;
#77–#81 are integrated. The portfolio/index, synthetic benchmark/release
preparation and developer-onboarding updates are present. Merged branches
preserve ancestry and must not be replayed. See [PROJECT_STATUS](PROJECT_STATUS.md),
[MASTER_EXECUTION_PLAN](MASTER_EXECUTION_PLAN.md),
[DEFINITION_OF_DONE](DEFINITION_OF_DONE.md) and [BLOCKERS](BLOCKERS.md).

## Current follow-up queue

| Work | Current state | Next acceptance gate |
| --- | --- | --- |
| PR #78 / MM-024 UCI policy | Merged normally at `291562a`; final head `8c8f862` passed 968 tests, zero skips, six local checks and six observed official jobs. | Preserve the no-reread/no-partition/no-cap-increase stop and snapshot deletion deadline. |
| UCI empirical pilot | Blocked after the approved call stopped above 250,000 product-day groups; no projection, complete exclusion counts or metrics. | Requires a separately reviewed evaluation design and explicit owner/model-review approval before changing the call strategy or bounds. Keep tests synthetic and snapshot deletion deadline. |
| B-01/B-02 Census lane | Metadata/protocol preparation only; no Census or FRED/ALFRED values acquired. | Continue no-byte due diligence; artifact-specific rights review and owner approval are required before acquiring Census bytes. FRED/ALFRED remains NO-GO absent written permission and series rights. |
| M2-02 retrieval evaluation / PR #82 | Merged normally at `c31ecd6` into main `d41e661`. Exact PR head `f6fa2ed` passed 989 local tests, zero skips, six checks and 12 official head checks; two guarded jobs were skipped. | M2-02 slice delivered as fictional/experimental. Preserve exact-head evidence; do not infer a check result for the merge SHA or later main. |
| [PR #87 / M2-03 bounded tool orchestration](https://github.com/GustavoMFDS/MirrorMind/pull/87) | Implemented on `codex/m2-03-tool-orchestration-20261127`, ancestry-synced through main `d41e661`; PR is open and unmerged. Exact local gate at `2d71d39` passed 1,014 tests, zero skips and all six checks. Code-identical `07a6cdc0` passed 86.92% coverage, whole-package/strict-retrieval mypy and package wheel smoke. | At exact PR head `2d71d39`, 12 official check-runs succeeded and deploy/release rehearsal were skipped by conditions; container smoke passed. Re-query any later head. No live provider, route, persistence or action authority. |
| G-02 offline continuity work | Existing fictional/local scope remains available; deployment, live credentials and external services are not authorized. | Continue a bounded implementation slice only where it satisfies an existing backlog criterion; record tests and operational limits. |

## Historical queue reconciliation — 2026-11-26

| Work | Current state | Evidence / next gate |
| --- | --- | --- |
| M1 synthetic vertical slice | Integrated experimentally in main `a456034`; PR #52–#59 are incorporated by #62 and their branches are retained. Independent merged-main gate: 835 tests, zero skips, six checks, exact WorldKernel pin. | M1 real-data, empirical forecast and production acceptance remain incomplete; do not close M1 overall. |
| Census vintage evaluator | Separate PR #63, open/non-draft at `b5e989314bcdcb566df479931794a5f56c07d477`, based on main. Exact local gate: 877 tests, zero skips, six checks. | Await independent review. Synthetic only; no Census/ALFRED bytes or source authorization. |
| M2-01 retrieval | PR #60, open/non-draft at `fafdedae3a76398e0450773065e40384c96d1ed7`, based on main. Exact local gate: 845 tests, zero skips, six checks. | Await independent review. Retrieval remains experimental and caller-scope is not authenticated authorization. |
| G-01 responder | PR #61 remains separate on main; the ancestry-preserving sync commit is `66fc9fa001eaa6bd3adbc8f8d1606f3743239d21`. Documentation baseline gate `20ce86bde740d5b46d7aeba4d13138884e211dba` passed 841 tests, zero skips and all six checks with the exact WorldKernel pin. | PR #61 is open/non-draft and ready for independent review. Its live body records the latest exact head/receipt; every later commit needs a fresh gate. No route or operational authority. |
| M2-02 retrieval evaluation | Planned; depends on M2-01. | Start after M2-01 review/integration settles. Use fictional/authorized fixtures; measure citation support, lineage and abstention. |
| ENG-02 examples lint maintenance | Ready as a separate maintenance item. `ruff check examples` on this branch reports five findings in three example files; none of these files differ from main. | Handle in a separate scoped PR; do not fold cleanup into #60/#61/#63. |
| Real-source pilots | Preparation only under the approved UCI then aggregate Census/ALFRED sequence. | B-01/B-02 remain open; keep automated tests synthetic and wait for source-specific rights, privacy, snapshot and temporal evidence. |

At this 2026-11-26 snapshot, GitHub Actions was unavailable under the
zero-paid-budget decision. The local six-check procedure remained separate
from official CI; no required check or protection was weakened. The PR #62 final comments
[7181452369](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181452369)
and [7181477141](https://github.com/GustavoMFDS/MirrorMind/pull/62#issuecomment-7181477141)
are the review record for the incorporated M1 baseline and PR ordering.

## Historical reconciliation at the PR #51 baseline

| State | Items / evidence | Continuation |
| --- | --- | --- |
| Merged foundations, still experimental | PRs #47–#50 added local/offline signed-fence verification and a nonce-challenged HTTPS reader; PR #51 consolidated the engineering handoff. These do not deliver a deployed trust service or source authorization. | Preserve their existing scope and tests; do not rebuild the governance chain as a substitute for the product path. |
| Partially implemented M1 | M1B-02 now composes separate CSV/XLSX readers, intake metadata and declared temporal checks. M1C-01 already had offline baselines and release backtests; the current stacked branch adds the reproducible evidence-to-evaluation entrypoint. | Keep the two changes reviewable as separate PRs; preserve abstention and per-origin receipts. |
| Ready at the PR #51 baseline | DOC-01 reconciliation; G-01 minimal testable server-side current-head response; M1E-01 simulation contract work; M1F-01 decision trace contract. DOC-01 is now in review below. | Keep M1 evidence-to-evaluation work ahead of further experimental governance unless a dependency requires G-01. |
| Pending by dependency | Remaining M1C/M1D/M1E/M1F, M2, M3 and M4 rows marked `planned`. | Start only when named predecessors and acceptance inputs exist. |
| Blocked by external evidence or approval | M1B-03 and M1C-03 require B-01/B-02 real-source rights, original availability and empirical holdout evidence. G-04 and deployment-related scopes also require B-03/B-06. | Advance synthetic slices independently; preserve blockers and do not claim they are solved by generated fixtures. |

## Historical consolidated review candidate before PR #62 merge — 2026-11-25

`codex/m1-engine-provenance`, published as
[PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62) to `main`, contains
provenance correction commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85` and
chronology correction `20e7b50f88df046eaf3541c5ea706b2e3b051aad`. It preserves
the exact published ancestry of #52–#59 and excludes #60/#61. The chronology
correction passed 835 tests without skips, plus Ruff, catalog, atlas, evidence
and capability checks, with reviewed WorldKernel pin installed. Receipt:
`results/local-quality-gate-20e7b50f88df046eaf3541c5ea706b2e3b051aad.json`.
The published PR #62 docs-inclusive head is `0bed1269613eb689e84ad971c7d8f1878767d6cf`;
its exact six-check gate passed 835 tests, zero skips. The PR remains open and
mergeable pending final independent review and the owner's integration
decision. PR #59 provenance comment `7174402947` and the #62 chronology finding
are addressed in the published candidate. The separate Census descendant and
its later fixes are not part of #62. No branch was merged and `main` was not
changed. PR #60 remains a separate M2 draft; PR #61 remains a separate G-01
draft.

## Historical queue — 2026-11-26

| ID | Status | Current state / next action | Blockers |
| --- | --- | --- | --- |
| M1 synthetic flow | integrated, experimental | PR #62 is merged at `a456034`; published #52–#59 heads are ancestors. #53–#59 are closed as incorporated and their branches remain available. Synthetic end-to-end integration is complete; empirical/source and production acceptance are not. | B-01, B-02, B-04, B-08 |
| M1B-01 / M1C-03 | prepared, real-data work blocked | Synthetic UCI evaluator is integrated through PR #62. Exact source terms, attribution, snapshot, privacy, retention and publication-availability evidence remain unresolved; keep tests synthetic and do not acquire/process bytes. | B-01, B-02 |
| M1B-04 / M1C-04 | independent review | Separate PR #63 branch `codex/m1-census-vintage-adapter` preserves main `a456034` through merge `55e91f7d73c67867edaf1aa790242f6cdbc611b9`. Chronology correction `00311c6344e8a70bb72315afc10f4fbd02926d26` rejects first estimates and revisions published before reference-month close; boundary and public-evaluator regressions pass. Pre-diagnostic source-policy head `47cdb587b0deab19835acd1435e4bd028ba28519` passed 882 tests, zero skips and all six local checks with reviewed WorldKernel pin; receipt `results/local-quality-gate-47cdb587b0deab19835acd1435e4bd028ba28519.json`, with summary in PR comment [7208332106](https://github.com/GustavoMFDS/MirrorMind/pull/63#issuecomment-7208332106). Four automatic Actions checks on that head failed before jobs ran; their annotation lists payment failure or spending-limit increase as alternatives, but identifies no cause and returns no jobs, steps, logs or combined status. See [B-08](BLOCKERS.md). The source proposal is direct Census MARTS with bounded scope and temporal protocol. Official citation guidance and the Census employee-work copyright policy are documented as general policy context, not file-specific rights clearance. Evaluator remains synthetic; no source parser or real-data processing is included. Independent review remains pending. | B-01, B-02, B-08 |
| M2-01 | ready for independent review | PR #60 is retargeted to `main`, mergeable and ready at `fafdedae3a76398e0450773065e40384c96d1ed7`; its exact local gate passed 845 tests, zero skips and all six checks. No official CI claim. Await independent review and required protections; do not merge locally. | B-08 |
| G-01 | ready for independent review | PR #61 is open/non-draft at `f30556ecb9219c1bc4eb0eb720f9c59c3a729b29`, targets `main`, and preserves its old head plus merge commit `66fc9fa`. Exact gate: 841 tests, zero skips, all six checks; final receipt is in PR body. | B-08 official Actions only |
| M2-02+ | planned | Start after M2-01 review/integration and independent reviews of #61/#63 are complete. Census status reconciliation is complete in PR #63; keep the active review queue stable and do not stack a new feature now. | M2-01 |
| ENG-02 | independent review | Five pre-existing Ruff findings are corrected on PR #64, head `ca97ab61d15347aa271ee9ac8468a0714bdc3402`. Exact local gate: 840 tests, zero skips, six checks; `ruff check examples` passes. The original date-gap exception and no-imputation behavior remain covered. Current Actions attempts stopped before job steps under the alternatives-only account annotation; see [B-08](BLOCKERS.md). | Independent review; B-08 official Actions |

### Pilot due-diligence update — 2026-11-26

Metadata-only review proposes direct original MARTS release files for one
verified national seasonally adjusted Retail and Food Services total. Exact
table, unit, methodology edition and artifact rights remain for owner review.
The annual-revision index exposes January 1992 through August 2026 but does
not prove original first-release completeness; the current advance schedule
states 8:30 a.m. without a timezone in its table. The April 2025 removal of
nonemployers is a population-definition boundary.

FRED/ALFRED is NO-GO for this MirrorMind development/archive route under
currently posted terms: FRED Services terms cover ALFRED and forbid storing,
caching or archiving service content; API terms additionally prohibit use in
connection with software/AI development. The separate Census files still need
artifact-specific rights review. The concrete proposed use is non-commercial
internal research with attribution, no redistribution, access-controlled
local storage and 30-day retention/deletion of value-bearing artifacts. The
temporal proposal fixes a 60/20/20 chronological development/validation/locked
holdout split before scores, first-estimate targets, 1/3/6-month fixed
baselines, strict-before date-only availability, gap abstention, and a
12-month moving-block bootstrap only if each horizon has at least 60 matched
holdout origins. These decisions remain pending; no source file, API response,
account or credential was acquired. B-01/B-02 remain open; see the detailed
[Census/ALFRED protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md).

## Merged M1 baseline — 2026-11-26

PR #62 is integrated at `a456034c55ed7634ad4768b26788fec09dab1d08`. Its
ancestry preserves the exact published heads of PRs #52–#59; each head was
verified as an ancestor before the stacked PRs #53–#59 were closed as
incorporated. PR #52 was already merged. Their branches remain available.
The independent exact-main gate passed 835 tests, zero skips and all six local
checks with the reviewed WorldKernel pin. This is not official Actions.

The synthetic M1 evidence-to-decision flow is integrated. M1 remains incomplete
because real-source permission, temporal provenance, empirical evaluation,
broader engine isolation and authenticated human review are open. PRs #60
(M2-01) and #61 (G-01) remain separate. #60 now contains `main` through
ancestry-preserving merge `a5186a6`; its first integrated local gate passed,
and the documentation-inclusive head still needs its exact gate before push
and review. #61 still needs the same sync-and-gate sequence. The Census
selector/evaluator remains a separate descendant and PR.

## Conventions

- `ready`: dependencies for the proposed bounded slice are satisfied.
- `partial`: existing implementation/evidence must be reused; only
  remaining acceptance work is open.
- `planned`: named prerequisite tasks or milestone gates remain.
- `blocked`: an external/owner gate prevents the named acceptance.
- `in_progress`, `review`, `done`: update only after a real claim,
  PR or accepted evidence; do not infer them from file names.
- P0 = unblock the functional MVP or resolve material correctness risk;
  P1 = deliver/strengthen the next functional slice; P2 = later
  hardening or generalization. Within a priority, respect dependencies
  rather than the row order. A prerequisite marked "synthetic" does not
  permit real-data or production claims.

Work item IDs below are stable; subdivide with suffixes when necessary.
A blocker applies to the stated scope, not automatically the whole
repository. Do not work on the same files/branch simultaneously without
coordination.

## A. Engineering and bounded checkpoint governance

| ID | Priority | Current status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| DOC-01 | P0 | ready | None | Reconcile stale introductory status, semantic map and current source/ledger; preserve dated evidence, resolve conflicting instructions, verify linked atlas. |
| G-01 | P0 | ready | PR #50 | Review existing protocol and implement a minimal testable service-side signed current-head response and independent storage contract; no live deployment. Use existing verifier and canonical signing domain; negative wire/nonce/scope/key tests. |
| G-02 | P0 | planned | G-01 | Authenticated, replay-resistant signed head advance, persistent transactional CAS and exact predecessor checks; reject stale/conflicting/unauthorized writes and test two concurrent writers, interrupted commit and reopen. |
| G-03 | P0 | planned | G-01, G-02 | Actual client/server integration with fictional data, isolated test trust, outages, expiry and failure cases; verify signed remote head mismatch and no permission grants; audit recovery and supplied forks. |
| G-04 | P1 | blocked | G-03, B-03 | Operational trust review: separately administered storage, key custody, identities, monitoring, authenticated access and restore evidence. Do not deploy or claim independence without approval. |
| ENG-01 | P1 | ready | None | Keep canonical checkout clean; record exact gates, check remote CI and improve reproducibility without lowering protections. Review dependency and warning changes separately. |
| ENG-02 | P2 | review | None | Resolve five pre-existing Ruff findings in `examples/` as separate maintenance. Preserve behavior; review RUF007 semantics and add boundary regression coverage. PR #64 is open on `codex/eng-02-examples-ruff`; exact-head local gate passed on `ca97ab6` (840 tests, zero skips, six checks); independent review remains. |

Use the existing [publisher](ATOMIC_GOVERNED_PUBLISHER.md),
[dual-witness transcript](INTEGRATED_FENCE_TRANSCRIPT.md),
[registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md) and
[HTTPS contract](REMOTE_FENCE_HEAD_CLIENT.md). G-01–03 are a bounded
experimental target, not permission to invent another authority hierarchy.
Complete a tested client/server slice, then spend the main effort on
the vertical product path.

## B. M1 — evidence, forecasts and runnable decision comparison

| ID | Priority | Current status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M1B-01 | P0 | integrated (synthetic protocol) | None | PR #62 integrates the UCI #352 event-time evaluator, fixed validation/holdout protocol, privacy-minimized outputs and synthetic aggregate Census/ALFRED vintage protocol. No complete real UCI projection or Census/FRED/ALFRED values exist; B-01/B-02 still gate empirical claims. |
| M1B-02 | P0 | integrated (synthetic) | None | PR #62 composes bounded CSV/workbook staging, review metadata, calendar/release checks and as-of selection into a deterministic synthetic evidence flow with rejection and abstention coverage. Real-source permission, availability and retention remain separate gates. |
| M1B-03 | P0 | blocked | M1B-01, M1B-02, B-01, B-02 | Approved real-source adapter with reviewed dataset card, actual source snapshot, permission enforcement, data minimization and provenance; verify temporal availability rather than inventing it. |
| M1B-04 | P1 | integrated (synthetic) | M1B-01 | PR #67 integrates the immutable aggregate-vintage contract and bounded synthetic as-of selector. It enforces strict date-only publication cutoffs, latest eligible revisions, retained release metadata, fail-closed ambiguity and no zero filling. It is not a Census/ALFRED parser or real-data permission. |
| M1C-01 | P0 | integrated (synthetic) | M1B-02 | PR #62 provides the reproducible retail evaluation entrypoint with shared eligible targets, fixed splits, per-origin receipts, offline baselines and release backtests. Empirical scores remain blocked by B-01/B-02. |
| M1C-02 | P0 | covered_by_existing_code | M1C-01 | Existing seasonal-naive and trailing-mean baselines already share eligible targets; do not add a third candidate without a justified need. Final acceptance remains synthetic until M1C-03 is approved. |
| M1C-03 | P0 | blocked | M1B-03, M1C-02, B-02 | Run approved empirical holdout, record actual MAE/RMSE/zero-safe metrics, coverage, abstention and model card; no invented accuracy. |
| M1C-04 | P1 | integrated (synthetic) | M1B-04 | PR #67 integrates fixed lag-12 and trailing-12-month baselines over synthetic publication vintages at horizons 1, 3 and 6. It uses strict as-of selection, first-estimate targets, disjoint validation/holdout origins, 12 visible months, matched metrics, abstention and replay receipts. This validates temporal mechanics only; B-01/B-02 still block empirical evaluation. |
| M1D-01 | P1 | integrated (experimental) | M1C-01 | PR #62 integrates the residual envelope, drift/sensitivity diagnostics and disjoint synthetic calibration/holdout mechanics with explicit uncalibrated limits. No empirical coverage claim is made. |
| M1D-02 | P1 | blocked | M1C-03, M1D-01, B-02 | Evaluate uncertainty on approved held-out observations, document empirical coverage or explicitly uncalibrated limits and sensitivity. No approved empirical holdout is currently available. |
| M1E-01 | P0 | integrated (experimental) | None | PR #62 integrates the versioned gateway and strict allowlisted WorldKernel request mapping. It rejects unrepresentable state/interventions/references and bounds mapped runs; mapping alone is not execution or production acceptance. |
| M1E-02 | P0 | integrated (experimental) | M1E-01 | PR #62 integrates the optional exact-pin local worker with timeout/output/result checks for the registered inventory demo. This proves local compatibility for that demo, not hostile-code isolation or a production lead-time model. |
| M1E-03 | P0 | integrated (synthetic) | M1C-01 | PR #62 integrates the paired fictional three-policy test double and shared deterministic day transition as the reference semantics. No external engine is required for this test-double path. |
| M1E-04 | P0 | integrated (experimental) | M1E-02, M1E-03 | PR #62 integrates the code-owned WorldKernel policy world using the shared transition, strict versioned mapping, bounded fan-out, parent-side state/stream checks, exact synthetic parity and explicit local CLI opt-in. HTTP/default CLI remain on the test double; B-04 still gates broader isolation and production acceptance. |
| M1F-01 | P0 | integrated (experimental contract) | None | PR #62 integrates the versioned decision trace/result contract separating facts, forecasts, simulated outcomes, assumptions, missing evidence, costs and human review. No authenticated producer or approval authority is included. |
| M1F-02 | P0 | integrated (synthetic) | M1B-02, M1C-01, M1D-01, M1E-03, M1F-01 | PR #62 composes synthetic evidence, fixed-baseline evaluation, residual diagnostics, policy simulation and typed trace through reproducible CLI/API paths. API/default CLI use the test double; the local CLI may opt into the fixed WorldKernel policy world. Empirical forecast, source and production transport gates remain open. |
| M1F-02a | P0 | integrated (synthetic provenance) | M1F-02, M1E-04 | PR #62 resolves the #59 engine-provenance finding: selected engine contract/result source, parity-oracle invocation and exact WorldKernel provenance are independently recorded and validated. Exact replay and adverse reference/digest regressions pass. B-04 production isolation remains outside this contract. |
| M1F-03 | P0 | blocked | M1B-03, M1C-03, M1D-02, M1F-02 | Complete reviewed retail MVP user story using approved observations and evaluated forecasts, actual simulation and documented conditional assumptions; independent replay and review. B-01/B-02/B-04 block this path. |

Read [M1 delivery plan](M1_EXECUTION_PLAN.md), [retail MVP](../RETAIL_MVP.md),
[forecast walkthrough](M1_STAGED_ROLLING_BASELINES.md),
[retail backtest](RETAIL_RELEASE_BACKTEST.md), [uncertainty guide](RETAIL_RESIDUAL_ENVELOPE.md),
[WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md) and
[decision trace](DECISION_TRACE_TEMPLATE.md). Do not discard existing
coverage/selection diagnostic modules merely because they are local.

## C. M2 — grounded AI and usable workflow

| ID | Priority | Current status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M2-01 | P1 | integrated (experimental) | M1F-01 | PR #60 capability merged through PR #66: strict typed query/result contracts and bounded in-memory fictional retrieval, filters caller-declared scope before ranking, binds exact excerpts to digests and labels all retrieved text untrusted. No route, identity or real-source permission. |
| M2-02 | P1 | integrated (experimental) | M2-01 | PR #82 merged at `c31ecd6`: bounded synthetic evaluation with citation support, abstention, lineage and scope regressions; no real-corpus quality claim. |
| M2-03 | P1 | review correction; re-review pending | M1F-02, M2-01 | PR #87 implements typed local orchestration over fixed fictional retrieval and decision tools. Commit `48e7efe` serializes the exact provider `AgentTurn` into plain data and strictly reconstructs nested contracts before use; regressions reproduce empty summaries, status/citation mismatch, malformed tool calls and missing payloads. That exact commit passed 1,019 tests, zero skips and six local checks. Current published SHA and official checks are in the live PR. No live provider, route, persistence or action authority. |
| M2-04 | P1 | planned | M2-02, M2-03 | Real provider evaluation only with B-05 approval; trace tool calls, model/call budgets, evidence refs, limitations and human confirmation; no unsupported numeric claims. |
| M2-05 | P1 | planned | M1F-02, M2-03 | Usable local/API/UI decision workflow with status, reproducible reports, uncertainty and review; demonstrate normal and failure paths. |
| M2-06 | P1 | planned | M1F-03, M2-04, M2-05 | Reviewed applied-AI acceptance with approved data, grounded comparison and explicit human approval. |

Security and budget controls cannot be postponed until after an
untrusted provider/tool is exposed. Build the required narrow controls
with each executable slice; M3 consolidates operational enforcement.

## D. M3 — durable and secure operations

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M3-01 | P1 | planned | M1F-01 | Reviewed identity/tenant model, authenticated authorization at data/tool/job boundaries and cross-tenant deny tests. |
| M3-02 | P1 | planned | M1F-02, M3-01 | Durable bounded job execution, idempotency, cancellation, timeout, crash recovery and versioned persisted outcomes. |
| M3-03 | P1 | planned | M2-03, M3-02 | Enforced server budgets for model calls/tokens and separate compute/simulation work; concurrency, overspend and denial tests. |
| M3-04 | P1 | planned | M3-01, M3-02 | Redacted logs/tracing, secret handling, health, operational metrics, recovery runbook and backup validation. |
| M3-05 | P2 | planned | M3-03, M3-04, B-06 | Measured performance/load and failure/recovery, documented target environment, reviewed threat model and release readiness; no production guarantee from unit tests. |

## E. M4 — generalization

| ID | Priority | Initial status | Dependencies | Deliverable and acceptance |
| --- | --- | --- | --- | --- |
| M4-01 | P2 | planned | M1F-02 | Compare core contracts against a distinct candidate domain, justify a reference workflow and choose with owner review if scope changes. |
| M4-02 | P2 | planned | M4-01, M2-05 | Add a second domain adapter, appropriate data/model/decision contracts and actual reproducible reference workflow; core has no retail-specific dependencies. |
| M4-03 | P2 | planned | M4-02, M3-05 | Verify version compatibility, optional-engine separation, regression across domains and reproducible release acceptance; owner release decision remains separate. |

## Task claim and update format

For each active task, add a short row/note below (or link its scoped
change request) with owner/agent, branch or worktree, expected touched
surfaces, current status, exact PR/commit, evidence, next action and
blocker IDs. Change status only when supported. Keep temporary details
in the task PR instead of accumulating duplicated logs here.

Example (**format only, not an actual claimed task**):
`M1B-02 | in_progress | agent / feat/... | source staging, tests | PR pending | next: negative cutoff test`.

To mark a task `done`, link reviewed implementation and actual test
results satisfying the relevant [definition of done](DEFINITION_OF_DONE.md).
If a gate fails, preserve the failure and choose the next safe
independent slice. A blocker resolved for a synthetic fixture does
not automatically resolve real-source, deployment or product gates.

## Historical queue — 2026-11-26

| ID | Status | Current state / next action | Blockers |
| --- | --- | --- | --- |
| M1B-02 / M1C-01 / M1D-01 / M1E-01–04 / M1F-01–02 | integrated, synthetic scope | PR #62 merged the end-to-end experimental M1 workflow at `a456034`; this completes the synthetic integration slice, not the licensed/empirical M1 acceptance. | B-01, B-02, B-04, B-08 |
| M1B-01 / M1C-03 | partial / blocked for real evidence | A+B pilot protocols and adapters are prepared; UCI remains event-time retrospective and Census is vintage-based. Do not acquire/process bytes until the source-specific license, privacy, retention and temporal evidence are approved. | B-01, B-02 |
| M1B-04 / M1C-04 | in_progress | Census descendant `codex/m1-census-vintage-adapter` passed its pre-sync gate at `da540a2`; merge commit `55e91f7` includes `a456034`. Re-run the complete gate on this exact reconciled head, then publish it as a separate PR. | B-01, B-02, B-08 |
| M2-01 | review preparation | PR #60 includes `main` via `a5186a680b307c4ecd9d56321321a5b27048731d`. Exact sync head and docs candidate `26e45b4620e9e13e12a745db3c99ead196c656d0` each passed 845 tests, zero skips and all six checks with pinned WorldKernel; the latter receipt is `results/local-quality-gate-26e45b4620e9e13e12a745db3c99ead196c656d0.json`. This status/evidence refresh needs its exact gate before push, retarget to `main`, and independent review. Keep caller-declared scope and fictional-only limits explicit. | B-08 |
| G-01 | ready for sync | PR #61 remains independent on its prior base. Merge `a456034` preserving typed clock-failure behavior and M1 contracts, then run the exact full gate before retargeting and preparing independent review. | B-08 |
| PR queue #52–#59 | reconciled | Exact published heads are ancestors of `a456034`; #52 is merged and #53–#59 are closed as incorporated. All branches are retained. | None for duplicate integration |
| M2-02+ | planned | Start only after M2-01 review/integration; do not grow the feature queue while #60/#61 and Census remain under consolidation. | M2-01 |
| ENG-02 | separately tracked | A scoped `ruff check examples` found 5 diagnostics in `m1_asof_rolling_backtest.py` (I001, RUF007), `m1_observation_preflight.py` (I001) and `m1_temporal_backtest.py` (I001, F401). They are outside the local gate's `src`/`tests` Ruff scope and are not failures of the integrated gate. Handle after PR consolidation in a distinct maintenance change. | None |

The older row-level branch claims below are preserved as historical evidence;
they are not live task ownership or current PR states.

## Historical active claims before PR #62 merge — 2026-11-25

| ID | Status | Owner / branch | Surfaces | PR / commit | Evidence and next action | Blockers |
| --- | --- | --- | --- | --- | --- | --- |
| M1C-04 | in_progress | Codex / local Census pilot branch | Fixed synthetic vintage backtest, chronology validation, exact bounded metrics, disjoint validation/holdout example, unit/CLI regressions, data/model cards and learning documentation | Local-only continuation on descendant of PR #62; no push or separate PR while consolidated candidate awaits review | Independent review findings on Decimal-context dependence, first-release/revision chronology, unanchored revisions and non-finite metrics are corrected in `3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6`. Output schema is v2 with an explicit unanchored-revision count. The focused Census suite passed 42 tests. Exact code-head gate passed 877 tests, zero skips and all six checks with WorldKernel `0.0.1` at reviewed source `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`; receipt `results/local-quality-gate-3c7603677a9ca7fb9f00bc0e959986e5fbb5a3f6.json`. The status/backlog/handoff/gate-doc commit `a6e3ed3355a1e52712542e6ae0d80d908885a82b` also passed the exact gate with 877 tests and zero skips; receipt `results/local-quality-gate-a6e3ed3355a1e52712542e6ae0d80d908885a82b.json`. Both are local-only. No parser, real-data bytes, API or capability promotion is included. | B-01/B-02 block real-source and empirical validation; B-08 blocks official Actions |
| DOC-01 | review | Codex / `codex/m1b-02-synthetic-evidence-flow` | Baseline reconciliation, semantic map, source/learning/docs navigation | [PR #52 draft](https://github.com/GustavoMFDS/MirrorMind/pull/52) | PR #51 remains the merged baseline; published PR #52 head `b431d11` has exact local gate evidence and its review response is recorded. | No separate docs blocker; official Actions remains unresolved under B-08 |
| M1B-01 / M1C-03 source decision | owner review pending | Codex / `codex/m1-engine-provenance` for integration; source lane remains separate | Synthetic UCI event-time evaluator, data/privacy card, Census aggregate vintage protocol | [PR #57 draft](https://github.com/GustavoMFDS/MirrorMind/pull/57); consolidated ancestry in [PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62); [UCI source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) | Owner approved the A+B research sequence: UCI #352 retrospective by product/event-time first, followed separately by aggregate Census/ALFRED release-vintage evaluation. The synthetic evaluator, fixed protocol and privacy controls are present in integrated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85`; its exact six-check local gate passed 832 tests with no skips and all five non-pytest checks, including the pinned WorldKernel path. No real source bytes, API key or credential were acquired. Adapter/protocol preparation may continue synthetically; real download/processing remains blocked pending source-specific rights, attribution, snapshot, minimization and retention approval. PR #57 Actions stopped before repository steps under B-08. | B-01/B-02/B-08 |
| M1B-04 | in_progress | Codex / `codex/m1-census-vintage-adapter` | Normalized Census vintage selector, synthetic fixture card, contract, chronology regressions, evaluator v2, and learning docs | Separate open PR #63; preserves PR #62 ancestry via merge `8560ad6` and main via merge `55e91f7` | Existing correction `3c76036` covers Decimal-context independence, first-estimate/revision ordering, unanchored-revision exclusion/counting and finite bounded metrics. Follow-up `00311c6` adds the period-close lower bound with selector and public-evaluator regressions; exact code-head gate passed 882 tests, zero skips, all six checks, with the reviewed WorldKernel pin. The final documentation-inclusive head is gated before publication, with its exact receipt in PR #63. Selector/evaluator use normalized fictional records only; no source parser, file/network access, credential or real data. UCI pilot remains covered by merged PR #62 and its synthetic evaluator/protocol; no real UCI ingestion is authorized. | B-01/B-02 still gate source rights, retention and empirical evaluation; B-08 gates official Actions |
| M1B-02 | in_progress | Codex / `codex/m1b-02-synthetic-evidence-flow` | CSV/XLSX local composition, review packet, calendar/release/as-of checks, tests and docs | [PR #52 draft](https://github.com/GustavoMFDS/MirrorMind/pull/52), exact tested commit `b431d11bf0ac841ff30353a06263d23fb901307c` | Full exact-head local gate passed 696 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 03:51:25 UTC. Review reply is recorded; B-01/B-02 remain open. | B-01/B-02 still block real-source rights and availability; B-08 blocks official check evidence; review/integration decision remains open |
| M1C-01 | in_progress | Codex / `codex/m1c-01-synthetic-retail-evaluation` | Prepared UCI-shaped evidence flow, fixed matched-origin baselines, deterministic fictional CLI, per-origin receipts and model/data docs | [PR #53 draft](https://github.com/GustavoMFDS/MirrorMind/pull/53), published exact tested head `79d3679013576c6a209bed9fa031b7f0fabd0d8d`, stacked on PR #52 | Full gate passed 700 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:08:00 UTC. The API suite ran; one existing deprecation warning remains. Current Actions fail without steps/logs; cause is not established. | Depends on M1B-02 in draft PR #52; B-01/B-02 block real-source claims and B-08 blocks official check evidence |
| M1F-01 | in_progress | Codex / `codex/m1f-01-decision-trace-contract` | Versioned immutable result schema, exact-result review binding, synthetic example, tests and learning docs | [PR #54 draft](https://github.com/GustavoMFDS/MirrorMind/pull/54), review correction `f02459d977fd263b03ddf60264b9069ae08b189b`, stacked on PR #53 | Correction reproduced pre-creation review and Decimal-context collision; 28 focused decision-trace tests pass. Merge commit `e493b4c` synchronizes the local branch with PR #53 head `79d3679`, retaining its nested-receipt regressions. Published integrated head `4d22006` passed all 728 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:25:37 UTC. Contract remains interface-only, with no producer or execution. | B-08 remains unresolved on published heads; source rights, empirical forecasts and actual engine outputs remain separate gates |
| M1E-01 | in_progress | Codex / `codex/m1e-01-worldkernel-mapping` | Strict source-version allowlist, unit/state/parameter validation, mutation-safe scenario revalidation, effective scenario/operator run ceilings and walkthrough | [PR #55 draft](https://github.com/GustavoMFDS/MirrorMind/pull/55), implementation `8769241`, review correction `07c405b`, sync merge `b9eba02` with PR #54 head `4d22006`, published head `56aa92a` | Published exact head `56aa92a` passed all 756 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 04:39:14 UTC. PR #53's nested-receipt regressions remain in the merged state. Actions failed before job steps under B-08. The mapper only builds a request; no WorldKernel import or execution is claimed. | B-04 blocks actual engine acceptance; B-08 blocks official CI evidence |
| M1E-02 | in_progress | Codex / `codex/m1e-02-worldkernel-local-runtime` | Optional exact-SHA local worker, bounded process protocol, strict result validation and synthetic engine example | [PR #55 draft](https://github.com/GustavoMFDS/MirrorMind/pull/55), local runtime implementation `ac52ec9`, exact gate recorded at `f503fcc` | The pinned `retail.inventory.demo@demo-1` engine and failure paths passed on the M1E-02 branch. Consolidated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85` passed 832 tests and all five non-pytest checks with exact-pin synthetic engine regressions and no skips. The PR #57 branch receipt is separate. This is local compatibility evidence for the registered demo, not a hostile-code sandbox or production lead-time model. | B-04 broad service acceptance and production isolation; B-08 official Actions evidence |
| M1D-01 | in_progress | Codex / `codex/m1d-01-disjoint-residual-calibration` | Fixed pre-holdout calibration/holdout target split, origin-specific release checks, uncertainty semantics, dependent tests and engineering docs | [PR #56 draft](https://github.com/GustavoMFDS/MirrorMind/pull/56), merge with PR #53 `b9bb86d`, published head `e993391` | PR #56 exact head `e993391a61a99d63008bc970cb19af673be4c18c` passed 700 tests plus Ruff, catalog, atlas, evidence and capability checks; it is an ancestor of consolidated candidate `74330d811145f10fcaaddadc56c3f95e7c8b7a85`, whose six-check local gate passed 832 tests. The result remains experimental and does not establish empirical calibration; no approved real observations were used. Actions did not start repository steps under B-08. | B-08 blocks official CI evidence; B-02 blocks empirical evaluation |
| M1E-04 | review | Codex / `codex/m1-engine-provenance` | MirrorMind-owned fixed policy world, versioned mapper, gateway, exact-pin worker, parity tests and learning documentation | [Consolidated PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62); implementation ancestry includes PR #55 and #58 | Published candidate head `0bed1269613eb689e84ad971c7d8f1878767d6cf` passed 835 tests with no skips plus all five non-pytest local checks while WorldKernel `9b133ef873f2b6a7206c9c5742d40df4fccdb04a` was installed. Selected WorldKernel output and test-double parity execution are separately represented in DecisionTrace v2. No WorldKernel-repository change was made; HTTP/default CLI remain on the test double. | B-04 broader service acceptance and hostile-code isolation; B-08 official Actions; final candidate review |
| M1E-03 | in_progress | Codex / `codex/m1e-03-synthetic-policy-simulation` | Fictional retail policy comparison, paired demand streams, deterministic inventory transitions, cost summaries and modeling caveats | [PR #58 draft](https://github.com/GustavoMFDS/MirrorMind/pull/58), published head `37737c2`, dependency sync merge `5544bc0` with PR #55 head `56aa92a` | Exact published head `37737c2ab329309fffb7dc3c8d8cdc6eee6c89a8` passed 768 tests plus Ruff, catalog, atlas, evidence and capability checks at 2026-11-25 05:18:58 UTC. Arrival-day exclusion remains a documented toy rule. The shared day transition is reused by M1E-04; the test double remains the parity reference. | B-08 blocks official CI evidence; source/model gates remain separate |
| M1F-02 | review | Codex / `codex/m1-engine-provenance` | Compose synthetic evidence, fixed-baseline evaluation, residual diagnostics, policy outcomes and versioned decision trace into one bounded flow | [Consolidated PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62), provenance correction commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85`, preserving exact #52–#59 ancestry | The integrated workflow, #57 evaluator, aggregate Census protocol, pinned local engine and M1F-02a provenance correction are present in published head `0bed1269613eb689e84ad971c7d8f1878767d6cf`. Exact six-check local gate passed 835 tests, zero skips and all checks with reviewed WorldKernel installed. `DecisionTrace` v1 remains; workflow v2 binds selected output source separately from parity execution. HTTP remains unauthenticated and does not invoke WorldKernel. No real-source evidence or empirical forecast claim is made. | B-01/B-02 block real-source claims; B-04 broader service isolation; B-08 official Actions; final candidate review |
| M1F-02a | review | Codex / `codex/m1-engine-provenance` | Bind actual selected engine, parity-oracle execution and exact engine provenance to conditional outcomes | [Consolidated PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62), commits `74330d811145f10fcaaddadc56c3f95e7c8b7a85` and `20e7b50f88df046eaf3541c5ea706b2e3b051aad`; resolves PR #59 comment `7174402947` and #62 chronology finding | Regression tests cover both engines, provenance replay, mismatched/dangling references, parity digest mismatch and v2 execution chronology. Published docs-inclusive #62 head `0bed1269613eb689e84ad971c7d8f1878767d6cf` passed 835 tests, zero skips and all six local checks with reviewed WorldKernel installed. Census decimal/chronology/metric corrections are in separate descendant commit `3c76036`, not #62. | Final independent review of PR #62; B-04 production isolation and B-08 official Actions remain separate |
| M2-01 | in_progress | Codex / codex/m2-01-permission-filtered-retrieval | Bounded lexical retrieval with caller-declared scope, deterministic excerpt spans and integrity-checked results | [PR #60 draft](https://github.com/GustavoMFDS/MirrorMind/pull/60), correction `73c1910`, published head `59deef2a780d7802d8b8d29b66dd0189e96365ea` | Regression tests reject same-length excerpt tampering and a different valid-looking digest. Exact PR #60 head `6fe64dd572991e905aae60358890c4255081abac` passed 738 tests plus Ruff, catalog, atlas, evidence and capability checks. GitHub metadata inspected 2026-11-25 reports the reviewed base #54 head `4d220066c3e9ab83a321ac9517bbabc8fc22e293` and `mergeable=true`. It remains a separate M2 draft outside the M1 candidate. Scope is caller-declared, not authenticated RBAC; source authenticity and absolute offsets remain unproven. | B-08 official CI; separate M2 review/integration decision |
| G-01 | in_progress | Codex / codex/g01-current-head-service | Read-only in-process current-head responder with typed clock/store failure boundaries | [PR #61 draft](https://github.com/GustavoMFDS/MirrorMind/pull/61), correction `1847e81`, published head `8101bc78dfa6a0f96bdfabe3dd8c9dc46d19a93e` | Clock regression distinguishes typed operational failures (generic bodyless 503) from unexpected programming errors. Exact head passed 697 tests plus Ruff, catalog, atlas, evidence and capability checks. Review response is recorded; Actions failed before steps. No route, persistence, authentication or deployed authority. | B-08 blocks official CI; service/transport deployment remains outside the reviewed slice |
