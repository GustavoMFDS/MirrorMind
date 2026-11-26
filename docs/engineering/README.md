# Living Engineering Knowledge

This is the entry point for **understanding, changing, testing and maintaining** this repository. It is documentation for both engineers and AI coding agents, not a substitute for reading and validating the source.

## Delegated execution and current priorities

- [Agent handoff](CODEX_HANDOFF.md) — onboarding, safe parallel work,
  source walkthrough and learning documentation standard.
- [Master execution plan](MASTER_EXECUTION_PLAN.md) — target architecture,
  dependency ordering and first runnable product slice.
- [Project status](PROJECT_STATUS.md) — dated, commit-pinned baseline,
  actual implemented/experimental boundaries and verification.
- [Task backlog](TASK_BACKLOG.md) — stable task IDs, priority, dependencies
  and concrete deliverables; reconcile concurrent work before claiming tasks.
- [Definition of done](DEFINITION_OF_DONE.md) — work-item and milestone
  acceptance, tests, truthful capability status and owner review.
- [Blocker register](BLOCKERS.md) — explicit external approval gates,
  safe independent work and evidence required to resolve blockers.

## Start here
- [System map](SYSTEM_MAP.md) — what runs, key modules, entrypoints, boundaries and cross-project relationships.
- [Repository atlas](REPOSITORY_ATLAS.md) — human-reviewed links to **every tracked code, test, config and document file**; a CI guard fails on missing files/links.
- [Semantic learning map](SEMANTIC_COVERAGE.md) — current implemented, interface-only and planned capability boundaries, source by source.
- [Contracts walkthrough](CONTRACT_WALKTHROUGH.md) — stepwise Pydantic validation and its limits: input shape is not authorized evidence or simulation.
- [Decision trace result contract](DECISION_TRACE_RESULT.md) — v1 general result envelope plus v2 selected-engine and parity execution evidence for the M1F-02 synthetic workflow; no real-source or action authority.
- [M1 synthetic retail decision workflow](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) — joins release-aware evidence, historical baseline/uncertainty diagnostics, a fixed 28-day profile, either the default policy test double or an explicit local WorldKernel policy handler, and a referenced trace through the same service.
- [M1E-04 WorldKernel policy world](WORLDKERNEL_POLICY_WORLD.md) — explains the code-owned fixed handler, versioned mapping, paired demand stream, local worker, parent validation, parity tests and limits.
- [Synthetic forecast model card](model_cards/SYNTHETIC_RETAIL_DECISION_WORKFLOW.md) — fixed seasonal-naive profile, split dates, baselines, uncertainty limits and upgrade gates.
- [API walkthrough](API_WALKTHROUGH.md) — health, capability, validation and synthetic decision routes plus the interface-only simulation gateway.
- [Curated evidence map](EVIDENCE_MAP.json) — human-reviewed claim IDs mapped to cited pytest functions and explicit limitations.
- [Capability truth ledger](CAPABILITY_LEDGER.json) and [promotion gates](CAPABILITY_GATES.md) — distinguish implemented/experimental/interface-only/planned capabilities; CI and API regressions detect drift.
- [M1 synthetic observation preflight](M1_DATA_PREFLIGHT.md) — source-reviewed local demo of bounded date/cutoff validation, **not** authorized ingestion or forecasting.
- [M1 synthetic rolling backtest](M1_TEMPORAL_BACKTEST.md) — two fixed one-step baselines, true rolling-prefix tests, an independent exercise and honest synthetic [data](datasets/SYNTHETIC_WEEKLY_CARD.md)/[model](model_cards/SYNTHETIC_WEEKLY_BASELINES.md) cards.
- [M1 synthetic as-of availability](M1_AVAILABILITY_PRECHECK.md) — independently test observation date versus declared publication date, with a [toy dataset card](datasets/SYNTHETIC_AVAILABILITY_CARD.md).
- [M1 availability-aware rolling evaluation](M1_ASOF_ROLLING_EVALUATION.md) — join both synthetic exercises, abstain when historical lag data was unpublished, and report coverage alongside metrics.
- [M1 local CSV snapshot staging](M1_LOCAL_CSV_STAGING.md) — reusable source-module parser with content integrity, immutable observations, as-of selection, a **bounded caller-opened binary stream reader** and non-imputing **aggregate quality diagnostics**; **not** source authorization. Includes a [synthetic fixture card](datasets/LOCAL_CSV_STAGING_FIXTURE.md).
- [M1 synthetic retail evidence flow](M1_SYNTHETIC_EVIDENCE_FLOW.md) — composes bounded CSV/XLSX staging, review-only metadata, declared calendar/release checks and CSV as-of selection; aggregate receipts omit raw IDs and retain false authorization/forecast flags. See the [M1B-02 change request](changes/M1B_02_SYNTHETIC_EVIDENCE_FLOW.md).
- [M1 retail evidence-to-evaluation flow](M1_RETAIL_SYNTHETIC_EVALUATION.md) — composes the reviewed UCI-shaped evidence flow with fixed release-aware baselines, matched origins and per-target receipts; the runnable CLI uses a deterministic fictional workbook. See the [M1C-01 change request](changes/M1C_01_SYNTHETIC_RETAIL_EVALUATION.md), [dataset card](datasets/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md) and [model card](model_cards/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md).
- [M1 synthetic retail policy comparison](M1_RETAIL_POLICY_SIMULATION.md) — compares three 28-day inventory rules on paired seeded demand streams with explicit item/day/cost assumptions and lead-time sensitivity. It is a local test double, not a forecast, recommendation or WorldKernel result; see the [M1E-03 change request](changes/M1E_03_SYNTHETIC_POLICY_TEST_DOUBLE.md).
- [M1 offline staged rolling baselines](M1_STAGED_ROLLING_BASELINES.md) — reusable source module with as-of lag-7/mean comparisons, abstention, matched metrics and **per-origin audit statuses**; review [synthetic data](datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md)/[model](model_cards/STAGED_WEEKLY_BASELINES.md) cards.
- [M1 delivery plan](M1_EXECUTION_PLAN.md) — evidence-before-model dependency order and independent gates.
- [Dataset card](DATASET_CARD_TEMPLATE.md), [forecast model card](FORECAST_MODEL_CARD_TEMPLATE.md), [decision trace](DECISION_TRACE_TEMPLATE.md) — mandatory future provenance, evaluation and human-review templates.
- [M5 source permission review](datasets/M5_ACCESS_REVIEW.md) — **not approved** for actual ingestion; requires verification of original competition rights and intended research/commercial use.
- [UCI Online Retail source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) — owner-approved research preparation only; source terms, attribution, privacy, snapshot and historical availability remain gates before real processing.
- [UCI event-time research](M1_UCI_EVENT_TIME_RESEARCH.md) — fixed, product-level retrospective evaluator using generated XLSX fixtures, frozen cohorts, matched baselines and explicit coverage abstention; no real workbook was acquired or processed.
- [Proposed UCI event-time dataset card](datasets/UCI_ONLINE_RETAIL_EVENT_TIME_CARD.md) — research scope, field minimization, retention proposal, temporal split and pre-acquisition permission gate.
- [Census/ALFRED vintage protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md) — separate aggregate-only temporal study; free authorized source access, archived vintages and source terms remain conditional.
- [UCI-shaped retail transaction projection](UCI_RETAIL_PROJECTION.md) — experimental **offline** product-day aggregation from invented transaction mappings with cancellation/returns rules, privacy-minimized output and **unknown** publication time; [fictional data card](datasets/SYNTHETIC_UCI_ROWS_CARD.md).
- [Atomic policy-gated checkpoint publication](ATOMIC_GOVERNED_PUBLISHER.md) — experimental new single-file SQLite policy+publication transaction, legacy bypass guard; [change record](changes/M1B_ATOMIC_GOVERNED_PUBLISHER.md) and [policy-bound v2 change](changes/M1B_POLICY_BOUND_PUBLICATION.md). New integrated writes require a separately signed policy revision/head; not production authorization or real ingestion.
- [Dual-admin operator-key governance](OPERATOR_GOVERNANCE.md) — experimental local signed enrollment/revocation and replacement, not coupled to publication; [change record](changes/M1B_OPERATOR_GOVERNANCE.md). No identities or permission grant.
- [Local signer-gated checkpoint publisher](LOCAL_CHECKPOINT_PUBLISHER.md) — experimental SQLite metadata journal with separate operator signatures and CAS; [change request](changes/M1B_LOCAL_CHECKPOINT_PUBLISHER.md). Not a live independent authority or legal data-use grant.
- [Witnessed checkpoint transcript](AUTHORITY_TRANSCRIPT.md) — experimental offline linked receipts and dual-signed rotation under caller-supplied fences; [change request](changes/M1B_AUTHORITY_TRANSCRIPT.md). No live external authority or ingestion.
- [Signed review-head checkpoints](SIGNED_HEAD_CHECKPOINTS.md) — experimental offline signature+SQLite equality check against externally supplied sequence minimum; [change request](changes/M1B_SIGNED_HEAD_CHECKPOINTS.md). No independent freshness source or authorization.
- [SQLite signed-review registry](SQLITE_REVIEW_REGISTRY.md) — experimental persistent local transactions and restart/cross-process checks, not independently authenticated authorization; [change request](changes/M1B_SQLITE_REVIEW_REGISTRY.md).
- [Local signed-review registry](LOCAL_REVIEW_REGISTRY.md) — bounded in-process compare-and-swap history with race/replay tests; **not** durable or trusted authorization; [change record](changes/M1B_LOCAL_REVIEW_REGISTRY.md).
- [Signed source review and revocation](SIGNED_SOURCE_REVIEW.md) — experimental Ed25519 metadata check with permanent same-packet revocation and external trust-root dependency; [change request](changes/M1B_SIGNED_REVIEW_REVOCATION.md). No legal authorization or ingestion.
- [Source intake review packet](SOURCE_INTAKE_REVIEW.md) — binds previously staged CSV/XLSX digests to sanitized caller-declared rights/privacy/retention metadata without granting ingestion or verifying historical availability; [change record](changes/M1B_SOURCE_REVIEW_PACKET.md).
- [UCI-shaped local XLSX reader](UCI_WORKBOOK_READER.md) — optional, **bounded and offline**, tested only on [generated Excel fixtures](datasets/SYNTHETIC_UCI_XLSX_CARD.md). Refuses unreviewed schemas and does not establish rights or full official UCI source support.
- [WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md) — strict versioned mappings plus experimental exact-pin local execution for the synthetic inventory demo and one code-owned policy world; no HTTP simulation route or hostile-code sandbox.
- [WorldKernel mapping and runtime walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md) — mapping, subprocess protocol, version checks, result validation, resource bounds, tests, learning exercises and limits.
- [M1E-02 local runtime change request](changes/M1E_02_WORLDKERNEL_LOCAL_RUNTIME.md) — scoped acceptance, impact map, compatibility review and exact-head evidence record.
- [M1E-04 policy-world change request](changes/M1E_04_WORLDKERNEL_POLICY_WORLD.md) — fixed registered handler scope, acceptance, impact map, compatibility review and local evidence.
- [WorldKernel policy-world walkthrough](WORLDKERNEL_POLICY_WORLD.md) — handler architecture, state transition, versioned contract, parity oracle, failure behavior, exact-pin tests and remaining isolation limits.
- [M1F-03 engine-provenance change request](changes/M1F_03_ENGINE_EXECUTION_PROVENANCE.md) — versioned trace behavior, selected-output and parity evidence, regressions, impact map and exact-pin validation.
- [Change request template](CHANGE_REQUEST_TEMPLATE.md) — required scope, acceptance and impact-map structure for meaningful engineering changes.
- [Debugging playbook](DEBUGGING.md) — reproduce a failure, trace behavior, identify evidence, patch and add regression tests.
- [Learning guide](LEARNING.md) — guided source reading and independent practice.
- [Generated symbol catalog](generated/SYMBOLS.md) — AST-based index of Python functions, classes, methods, signatures, locations and local imports. Run the generator if the file is not checked in.
- [Agent instructions](../../AGENTS.md) — mandatory change/documentation protocol.
- Existing canonical architecture and roadmap documents live in the parent [docs](../) directory.

## Two types of documentation
**Generated facts:** syntax-level structure such as function signatures, classes, file paths and static imports. Recreate from code with `python scripts/docs/catalog.py --write`. Static analysis does not prove live call graphs, side effects or correctness.

**Reviewed explanations:** responsibilities, design rationale, contracts, state transitions, recovery behavior, failure modes and worked examples. Maintain these alongside code changes, backed by tests and explicit decisions.

## Routine
1. Write the desired behavior and acceptance criteria in a copy of [the change request template](CHANGE_REQUEST_TEMPLATE.md).
2. Follow [the system map](SYSTEM_MAP.md), symbol index, tests and related design records to determine the actual impact.
3. Implement and test. Keep new behavior and old behavior separate in the change description.
4. Update related documents and regenerate the code index in the same PR.
5. Ask an engineer to explain the change without an agent and make a small independent test or modification.

### Commands
```bash
python scripts/docs/catalog.py --write
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
python -m pytest -q
python -m ruff check src tests
```

Documentation CI requires the **committed** symbol catalog to be current, regenerates it for inspection, and verifies every tracked file has a resolving link in the reviewed atlas and local Markdown links exist. This structural check is intentionally stricter than a filename mention. A separate curated claim-to-test checker requires matching guide claim IDs, cited test paths/functions and explicit limitations. Neither guard executes tests or validates prose semantics, statistical models, privacy or execution safety; these require independent review and actual tests.

## Scope and independence
These conventions are shared across WorldKernel, MirrorMind and NeuroShift, but the repositories remain independent. Shared documentation layout does not create shared runtime dependencies. Changes to the *contracts* between projects require separate, coordinated reviews.

## Experimental signed-fence verification

- [Supplied signed integrated-head fence](INTEGRATED_HEAD_FENCE.md) —
  read-only comparison of a signed policy+publication state to one local
  SQLite snapshot using caller-pinned exact current sequence/digest;
  [scoped change request](changes/M1B_INTEGRATED_HEAD_FENCE.md).
  No independent current-head service, live admission or source rights.

## Experimental dual-witness integrated-head continuation

- [Dual-witness integrated-fence transcript](INTEGRATED_FENCE_TRANSCRIPT.md) —
  bounded read-only forward chain of authority-signed combined heads
  with two witness signatures, conditional offline equality and
  classification of *supplied* competing successors.
  [Change request](changes/M1B_DUAL_WITNESS_FENCE_CONTINUITY.md).
  No trusted independent latest state, key custody, real-source rights,
  live publication admission or source ingestion.

## Experimental locally persisted signed combined-state head

- [Separate local integrated-fence registry](LOCAL_INTEGRATED_FENCE_REGISTRY.md):
  opt-in second SQLite file storing fully signed dual-witness forward
  transitions, bounded history replay and registry-only CAS.
  [Change request](changes/M1B_SEPARATE_DURABLE_FENCE_REGISTRY.md).
  Detects publisher-only rollback **conditionally** with an intact
  registry; it is not an external trusted current-head service, a
  cross-file transaction or an authorization/ingestion feature.

## Challenged external-head reads (experimental, no deployed service)

- [Nonce-bound signed HTTPS head client](REMOTE_FENCE_HEAD_CLIENT.md) —
  optional outbound-only comparison of a signed, short-lived remote
  current-head *claim* against the local fully verified registry.
  [Scoped change request](changes/M1B_CHALLENGED_HTTPS_HEAD_READER.md).
  The service, separate key custody, remote currentness and real
  ingestion permission are **not provided by this repository**.
