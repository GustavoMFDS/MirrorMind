# Living Engineering Knowledge

This is the entry point for **understanding, changing, testing and maintaining** this repository. It is documentation for both engineers and AI coding agents, not a substitute for reading and validating the source.

## Start here
- [System map](SYSTEM_MAP.md) — what runs, key modules, entrypoints, boundaries and cross-project relationships.
- [Repository atlas](REPOSITORY_ATLAS.md) — human-reviewed links to **every tracked code, test, config and document file**; a CI guard fails on missing files/links.
- [Semantic learning map](SEMANTIC_COVERAGE.md) — current implemented, interface-only and planned capability boundaries, source by source.
- [Contracts walkthrough](CONTRACT_WALKTHROUGH.md) — stepwise Pydantic validation and its limits: input shape is not authorized evidence or simulation.
- [API walkthrough](API_WALKTHROUGH.md) — each implemented HTTP route and the interface-only simulation gateway.
- [Curated evidence map](EVIDENCE_MAP.json) — human-reviewed claim IDs mapped to cited pytest functions and explicit limitations.
- [Capability truth ledger](CAPABILITY_LEDGER.json) and [promotion gates](CAPABILITY_GATES.md) — distinguish implemented/experimental/interface-only/planned capabilities; CI and API regressions detect drift.
- [M1 synthetic observation preflight](M1_DATA_PREFLIGHT.md) — source-reviewed local demo of bounded date/cutoff validation, **not** authorized ingestion or forecasting.
- [M1 synthetic rolling backtest](M1_TEMPORAL_BACKTEST.md) — two fixed one-step baselines, true rolling-prefix tests, an independent exercise and honest synthetic [data](datasets/SYNTHETIC_WEEKLY_CARD.md)/[model](model_cards/SYNTHETIC_WEEKLY_BASELINES.md) cards.
- [M1 synthetic as-of availability](M1_AVAILABILITY_PRECHECK.md) — independently test observation date versus declared publication date, with a [toy dataset card](datasets/SYNTHETIC_AVAILABILITY_CARD.md).
- [M1 availability-aware rolling evaluation](M1_ASOF_ROLLING_EVALUATION.md) — join both synthetic exercises, abstain when historical lag data was unpublished, and report coverage alongside metrics.
- [M1 local CSV snapshot staging](M1_LOCAL_CSV_STAGING.md) — reusable source-module parser with content integrity, immutable observations, as-of selection, a **bounded caller-opened binary stream reader** and non-imputing **aggregate quality diagnostics**; **not** source authorization. Includes a [synthetic fixture card](datasets/LOCAL_CSV_STAGING_FIXTURE.md).
- [M1 offline staged rolling baselines](M1_STAGED_ROLLING_BASELINES.md) — reusable source module with as-of lag-7/mean comparisons, abstention, matched metrics and **per-origin audit statuses**; review [synthetic data](datasets/STAGED_WEEKLY_AVAILABILITY_CARD.md)/[model](model_cards/STAGED_WEEKLY_BASELINES.md) cards.
- [M1 delivery plan](M1_EXECUTION_PLAN.md) — evidence-before-model dependency order and independent gates.
- [Dataset card](DATASET_CARD_TEMPLATE.md), [forecast model card](FORECAST_MODEL_CARD_TEMPLATE.md), [decision trace](DECISION_TRACE_TEMPLATE.md) — mandatory future provenance, evaluation and human-review templates.
- [M5 source permission review](datasets/M5_ACCESS_REVIEW.md) — **not approved** for actual ingestion; requires verification of original competition rights and intended research/commercial use.
- [UCI Online Retail source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) — official dataset license states **CC BY 4.0**, but attribution, privacy, source versioning and historical information availability still require approval.
- [UCI-shaped retail transaction projection](UCI_RETAIL_PROJECTION.md) — experimental **offline** product-day aggregation from invented transaction mappings with cancellation/returns rules, privacy-minimized output and **unknown** publication time; [fictional data card](datasets/SYNTHETIC_UCI_ROWS_CARD.md).
- [UCI-shaped local XLSX reader](UCI_WORKBOOK_READER.md) — optional, **bounded and offline**, tested only on [generated Excel fixtures](datasets/SYNTHETIC_UCI_XLSX_CARD.md). Refuses unreviewed schemas and does not establish rights or full official UCI source support.
- [WorldKernel gateway gate](WORLDKERNEL_GATEWAY_GATE.md) — explicit version mapping and fail-closed input compatibility before a real adapter exists.
- [Change request template](CHANGE_REQUEST_TEMPLATE.md) — describe a future feature or correction in plain language before coding; map it to modules, tests and docs.
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
