# Change request — M1B-01 UCI event-time retrospective pilot

**Status:** implementation prepared against synthetic data; exact-head local gate passed; independent review of this diff remains pending.

## 1. Goal in plain language

**Current behavior:** MirrorMind already has a bounded UCI-shaped row projection and optional local XLSX reader, but no fixed product-day evaluation path. The previous reader cap default was intentionally small and the source review still described the adapter as future work.

**Desired behavior:** Compose the existing projection and reader with a fixed, local-only event-time evaluator and deterministic in-memory workbook. Freeze product cohort and dates before scoring; use matched eligibility for fixed lag-seven and trailing-seven-day baselines; abstain on incomplete target/history coverage; redact product codes from result JSON.

**Why:** The owner approved preparing the A-first UCI pilot, while explicitly withholding permission to acquire or process the original workbook until source-specific rights, attribution, privacy, retention and snapshot controls are reviewed. Synthetic regressions make the protocol inspectable without crossing that boundary.

**Out of scope:** Downloading or parsing the original workbook; real-data or commercial permission; point-in-time forecast claims; causal, inventory or lost-sales inference; API endpoint; source credential; production model; WorldKernel; edits to another repository; any paid resource.

### Capability status

- Previous: UCI projection and XLSX reader are `experimental`; no event-time evaluation capability was declared.
- Proposed: add `local_uci_event_time_research` as `experimental` in the reviewed ledger and `GET /v1/capabilities`.
- Narrow evidence: `tests/integration/test_uci_event_time_cli.py::test_synthetic_cli_is_reproducible_and_keeps_event_time_limitations`; regression details are in the [research guide](../M1_UCI_EVENT_TIME_RESEARCH.md).
- Limitation: only an invented workbook and caller-declared complete dates; not source permission, empirical accuracy or availability history.

## 2. Acceptance criteria

- [x] Fixed fit, validation and locked holdout windows are explicit in source and docs.
- [x] Cohort comes only from positive product-day events within the fit window.
- [x] Baselines share exactly the same eligible product-origin pairs.
- [x] Unknown target or history coverage abstains; no missing date is silently filled.
- [x] Metrics include MAE/RMSE/zero-safe WAPE; WAPE is null for zero denominator.
- [x] Result JSON excludes raw product codes, invoice numbers, customer IDs, descriptions and country.
- [x] Synthetic XLSX example exercises parser and evaluator deterministically.
- [x] Existing small default limits remain; any larger explicit caps remain finite and are not represented as verified original-file support.
- [x] Source review and dataset/model cards make permission and availability limits explicit.
- [x] Exact clean-commit local quality gate passes all six checks (`a42c3e13f73e9499dd505560d2809573fd1a7005`, 712 tests, 2026-11-25 15:24:49 UTC; local only).
- [ ] Independent reviewer inspects the committed diff and exact-head receipt.
- [ ] External reviewer/owner determines separately whether PR #57 is ready; this request does not mark it ready or merge it.

## 3. Impact map

| Layer | Relevant file/symbol | Change | Evidence |
| --- | --- | --- | --- |
| Existing projection | `src/mirrormind/domains/retail/uci_transactions.py::project_uci_retail_rows` | Explicit bounded maximums for reviewed large local research input; default caps unchanged | `tests/unit/test_uci_retail_projection.py` |
| Existing reader | `src/mirrormind/domains/retail/uci_workbook.py::read_uci_workbook` | Allows explicit finite row/group caps while preserving all current schema and archive checks | `tests/unit/test_uci_workbook.py` |
| Evaluation core | `src/mirrormind/domains/retail/uci_event_time.py::evaluate_uci_event_time` | New fixed protocol and aggregate receipt | `tests/unit/test_uci_event_time.py` |
| Runnable example | `examples/m1_uci_event_time_research.py::run_synthetic_evaluation` | Generated in-memory fictional workbook only | `tests/integration/test_uci_event_time_cli.py` |
| Capability API | `src/mirrormind/api/routes/system.py::capabilities` | Truthful experimental capability declaration | `tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger` |
| Data/evaluation contract | `docs/engineering/datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md`; `docs/engineering/model_cards/SYNTHETIC_UCI_EVENT_TIME.md` | Synthetic inputs, temporal split, baseline, metric and privacy limits | Related selectors in the research guide |
| Other project/contracts | WorldKernel repository and generic API contracts | No change | No runtime connection introduced |

## Data, model and decision review

- Dataset card: [synthetic UCI event-time card](../datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md). Original UCI handling remains in the [source review](../datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md).
- Model card: [synthetic event-time baselines](../model_cards/SYNTHETIC_UCI_EVENT_TIME.md). No fitted model or uncertainty estimate.
- Decision trace: not applicable; the code emits no recommendation or operational action.
- WorldKernel gate: not applicable; the evaluator does not invoke a simulation engine.
- Temporal boundary: fixed date windows and mutation regression guard validation from held-out values, but no source release vintage exists, so output remains retrospective.

## 4. Constraints and recovery

The module remains local and opt-in. Public defaults stay at 10,000 input rows and 2,000 product-day groups. Explicit source-size ceilings are finite and were chosen from catalog metadata with margin; the actual original bytes, compressed layout and parser behavior have not been tested. Failure does not write intermediate files. To roll back, remove the new evaluator/example/tests/docs and capability entry, then regenerate the symbol catalog; existing reader defaults and old receipt contracts remain compatible.

## 5. Implementation and verification

Implementation summary: add the evaluator and synthetic example, add normal/adverse regressions, update source-review wording to reflect existing parser capability, write learning/data/model/change documentation, update maps/ledger/atlas/evidence and regenerate the source catalog.

The focused regression set passed in the current working tree: 87 tests, including UCI projection, workbook, event-time, CLI and API capability parity. The exact-head gate then passed on clean commit `a42c3e13f73e9499dd505560d2809573fd1a7005`: 712 pytest tests, Ruff, symbol catalog, repository atlas, evidence map and capability ledger; total 19.32 seconds and one existing Starlette/httpx warning. This is local validation, not GitHub Actions or independent review of the new diff. No real UCI or Census rows were acquired or processed.

## 6. Evidence after implementation

- Commit / PR: implementation `a42c3e13f73e9499dd505560d2809573fd1a7005`; PR #57 remains a draft, with review and integration decisions separate.
- Modified symbols and files: `uci_transactions`, `uci_workbook`, new `uci_event_time`, synthetic example and associated tests/docs.
- Tests and environment: Python 3.13.5; 87 focused tests and exact-head full gate of 712 tests plus all five non-test checks passed; official CI not checked by the script.
- Claim IDs: `MM-UCI-EVAL-001` through `MM-UCI-EVAL-003`, with named functions and limitations in `EVIDENCE_MAP.json`.
- Contracts: experimental JSON result `mirrormind.uci.event_time_evaluation.v1`; no HTTP contract or API data route.
- Known limitations: no source acquisition, owner-verified permission, genuine data, intraday publication time, demand truth, interval calibration or runtime sandbox.
- Independent explanation: the evaluator consumes only a caller-supplied bounded projection plus explicit complete-date declarations. It scores each product and target on shared origins, serializes ordinal-only product summaries and labels the result retrospective because `InvoiceDate` is event time.
