# Change request — Compose the local retail evidence preflight

## 1. Goal in plain language

**Current behavior:** CSV snapshot validation and as-of selection, source review packets, UCI-shaped XLSX projection, declared calendar coverage and declared release audits are available as separate local helpers. Existing tests prove those boundaries separately, but a caller must compose them and preserve their non-authorizing caveats itself. See `snapshots.py`, `intake_review.py`, `uci_workbook.py`, `calendar_coverage.py`, and `declared_releases.py` and their focused tests.

**Desired behavior:** provide one reusable in-memory retail preflight for each supported local format. The CSV path stages and hashes the bytes, binds a review-only packet, summarizes structure, and selects only rows whose declared event and publication dates are no later than the requested origin. The workbook path stages and projects the bounded XLSX, binds a review-only packet, checks the caller-declared calendar, and audits explicit release declarations at an origin. Both return typed components for later offline composition and aggregate receipts that omit raw identifiers and values.

**Why:** M1B-02 is a P0 partial task and M1C-01 depends on it. A composable, tested slice advances the M1 retail path while keeping synthetic assumptions, permissions and source availability explicit.

**Out of scope:** source acquisition, rights verification, authentication, persistence, HTTP routes for data, forecasting, recommendations, publication-time inference from `InvoiceDate`, real-source approval, a production evidence engine and any WorldKernel adapter.

## Capability status change

- Previous and proposed status: no composite flow capability -> `experimental` in `CAPABILITY_LEDGER.json`.
- The implementation remains a local fixture-oriented preflight. It is not an authorized ingestion path, source provenance verifier, forecast or decision capability.
- Tests prove composition, digest/declaration mismatch rejection, declared-cutoff filtering, release withholding and sanitized receipts. They do not prove rights or real publisher availability.
- Add the identifier to the experimental list returned by `GET /v1/capabilities`; keep the scaffold and other capability statuses unchanged.

## 2. Acceptance criteria

- [x] Given the deterministic CSV fixture and matching SHA-256, the composite CSV path returns the review packet, structure summary and only the requested series rows published by the origin.
- [x] Given an origin before any event/publication date, the CSV result reports an empty as-of slice as an abstention; it does not impute zero or mark data forecast-eligible.
- [x] Given a bounded generated UCI-shaped workbook, caller-declared calendar and explicit releases, the workbook path composes projection, calendar coverage and release audit; late and future product-days are withheld/count-only at the origin.
- [x] Digest mismatch, declaration/source mismatch, missing calendar dates and missing release declarations fail closed through existing validators; the underlying helpers retain duplicate/invalid release validation.
- [x] Receipts contain aggregate counts and digest/status metadata only; they exclude source references, series/product identifiers, invoice/customer data and raw values.
- [x] Composite CSV and UCI receipts preserve the exact child source-review, quality, projection, calendar and release receipts; integration assertions compare each nested value to its source component.
- [x] Python API CI explicitly installs `dev`, `uci` and `review` extras; direct imports ensure missing `openpyxl` or `cryptography` fail the test job rather than skip coverage.
- [x] Capability ledger, registered API handler, evidence map, repository atlas, generated symbol catalog and human-written engineering/learning/debugging docs agree structurally; documentation guards and a direct registered-handler/ledger parity check passed locally.
- [ ] The full API integration suite and exact-commit local quality gate pass. The current Windows execution blocked before application code in `tests/integration/test_api.py::test_health`; see B-07. Official Actions is separately blocked by B-08.
- [x] Existing public contracts and helper semantics remain unchanged; no network, disk persistence or authorization behavior is added.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `mirrormind.domains.retail.evidence_flow` | Add local composition functions | New integration tests for CSV and XLSX flows |
| Core implementation | `snapshots.read_staged_csv`, `available_as_of`, `snapshot_quality_summary`; `prepare_source_review_packet`; `read_uci_workbook`; `summarize_declared_calendar_coverage`; `audit_declared_releases_as_of` | Reuse only | Existing focused tests plus new composition tests |
| State / persistence / API | `GET /v1/capabilities`, `CAPABILITY_LEDGER.json` | Declare one experimental library capability only | `test_capabilities_match_reviewed_ledger`; capability guard |
| Calling components | None; library caller supplies streams and declarations | No change | Integration tests call public composition functions and compare aggregate receipts to child receipts |
| CI dependencies | `.github/workflows/ci.yml` | Install explicit `dev`, `uci` and `review` extras | Existing full suite imports `openpyxl`/`cryptography` directly; no optional dependency test skip |
| Downstream consumers | M1C offline evaluation is a future consumer | No consumer wired in this slice | Returned typed staged data; no forecast runs here |
| External project/contracts | None | No change | No external adapter or network access |

## Data, modeling and decision review

- No external dataset is acquired or asserted. Tests use the existing synthetic CSV example and an in-memory generated UCI-shaped workbook. A real-source adapter still requires a reviewed dataset card and blockers B-01/B-02.
- No forecast model is fitted or evaluated; model-card requirements do not apply to this preflight slice.
- No recommendation or action is produced; no decision trace or human action approval is implied.
- No WorldKernel fields are read or translated.
- CSV selection uses caller-declared `available_on`; workbook availability comes only from caller-declared `DeclaredProductRelease`. No timestamp is inferred from UCI `InvoiceDate`. These checks prevent leakage only relative to supplied declarations; they do not authenticate those declarations.

## 4. Constraints and risks

The helpers already bound bytes, rows, groups, workbook archive members and dates. The composite API must preserve those bounds by delegating instead of parsing again. Streams are caller-opened and in-memory results may contain series/product identifiers; receipts must remain identifier-minimized. A valid digest proves byte equality only. Review references, permissions, calendar and releases remain caller assertions. No persistence, network access, source approval, forecast eligibility or operational custody is added.

## 5. Implementation plan

1. Reuse the existing staging, review, calendar/release and as-of functions without duplicating their validation algorithms.
2. Add deterministic integration coverage for normal paths, abstention, malformed declarations, receipt minimization and aggregate-to-child receipt parity.
3. Add one experimental capability and keep API/ledger parity.
4. Explain architecture, data flow, contracts, safety boundaries, diagnostics, tests and follow-up in the engineering hub, system map, debugging notes, learning notes, atlas and evidence map.
5. Regenerate the symbol catalog and run focused tests, full local quality gates and documentation guards on the exact final commit. Report local evidence separately from remote CI.

## 6. Evidence after implementation

- Commit / PR: branch `codex/m1b-02-synthetic-evidence-flow`, commit `c51ab30370db47e9f7105c97f870008e4fc442c5`, draft [PR #52](https://github.com/GustavoMFDS/MirrorMind/pull/52). No merge or production release is claimed.
- Modified symbols: `RetailCsvEvidenceFlow`, `RetailUciEvidenceFlow`, `prepare_retail_csv_evidence_flow`, `prepare_retail_uci_evidence_flow`, and the experimental `/v1/capabilities` entry.
- Tests executed, result, environment: the five focused integration tests passed; a full run excluding `tests/integration/test_api.py` passed 690 tests in 15.60 seconds; direct invocation of the registered `/v1/capabilities` router handler matched the ledger's implemented, experimental and planned sets. Ruff and the catalog, atlas, evidence and capability guards passed locally. The exact-commit gate returned `local_gate_failed_or_incomplete` because its pytest stage exited 124 at the configured 900-second timeout; the remaining gate stages did not run. Verbose pytest collected 696 tests and stopped at `test_health` before application code. A standalone `asyncio.new_event_loop()` reproduced blocking in `socket.accept` inside `_fallback_socketpair` on Python 3.13.5 and the installed Python 3.12; the likely host/sandbox loopback cause is still a hypothesis.
- Claim IDs and cited test path/function: `MM-FLOW-001`–`MM-FLOW-005`, each cites a top-level function in `tests/integration/test_retail_evidence_flow.py`.
- Evidence/provenance/cutoff and uncertainty: generated/synthetic inputs and caller-declared dates only; no real-source or publisher verification.
- Scope of human review and approval: local experimental behavior only; not production permission. PR #52 remains a draft pending exact-commit verification.
- New or changed contracts: additive local Python library API and experimental capability identifier; existing helper and HTTP data contracts remain unchanged.
- Docs updated: M1 flow walkthrough, change request, system map, API walkthrough, semantic map, capability/evidence ledgers, atlas, backlog, status, blocker register, debugging, learning and generated symbol catalog.
- Official GitHub Actions: checks for this SHA failed before starting. Their annotations state recent account payments failed or the spending limit must be increased; see B-08 and [run 45318084072](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45318084072), [run 45318084108](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45318084108). No CI test result is available.
- Known limitations / follow-up: B-07 blocks the Windows API `TestClient` path and full local gate; B-08 blocks official checks. M1B-01/B-01/B-02 still govern genuine data rights and availability; M1C-01 consumer wiring remains separate.
- Independent explanation: the new domain-level entrypoints delegate parsing, review binding, calendar checks, release auditing and as-of selection to existing helpers. To change a parser rule, update its existing module and tests; change only the composition and its integration test when the order or returned contract changes.
