# Change request — Compose retail evidence into a fixed-split evaluation

## 1. Goal in plain language

**Current behavior:** MirrorMind can prepare a bounded UCI-shaped workbook with review metadata, declared calendar coverage and caller-declared product-day releases through `prepare_retail_uci_evidence_flow`. A separate `backtest_declared_retail_releases` compares two fixed daily baselines and records per-target abstention statuses. Callers must currently join those results and preserve the matching-cutoff and non-authorizing boundaries themselves.

**Desired behavior:** provide one typed-flow consumer that verifies the flow's declared-release audit uses the same evaluation cutoff, reuses the existing matched-origin retail evaluator, and returns a versioned aggregate evaluation receipt. Add a runnable synthetic CLI that constructs a deterministic fictional workbook, explicit release declarations and a fixed holdout, then exercises the complete M1B-02-to-M1C-01 path.

**Why:** M1C-01 is a P0 partial task and the primary M1 objective is a reproducible evidence-to-evaluation slice. This composes existing pieces into an inspectable product path without introducing data acquisition or another forecasting algorithm.

**Out of scope:** real-source rights or ingestion, publisher authentication, trained models, model selection or tuning, calibrated uncertainty, an HTTP forecast route, decision recommendations, simulation, WorldKernel, persistence and automatic business writes.

## Capability status change

- Add `local_retail_evidence_evaluation` as `experimental` in the capability ledger and `/v1/capabilities`; do not promote the broader `forecasting` capability.
- Production behavior: local in-memory composition only. The example CLI generates only fictional rows and caller-declared release dates.
- Narrow evidence: tests must prove matching cutoffs, deterministic fixed split, matched baseline origins, per-origin statuses, no leakage from a withheld target, and sanitized receipts. These are not empirical forecasting claims.
- A restricted run previously timed out before HTTP application code while creating an asyncio socket pair; the full local gate on published PR #53 head `79d3679013576c6a209bed9fa031b7f0fabd0d8d` later ran the API integration module. A direct registered-handler/ledger check remains separate evidence and is not an HTTP runtime test.

## 2. Acceptance criteria

- [x] Given a `RetailUciEvidenceFlow` prepared with an evaluation cutoff, evaluate the last bounded number of calendar targets only when the declared history and targets meet existing release rules.
- [x] Reject an evaluation cutoff that differs from the flow's declared-release audit cutoff; preserve the existing exact-date and holdout bounds.
- [x] Reuse `backtest_declared_retail_releases` and its fixed baseline set. Both baselines score exactly the same eligible target origins; each requested target has one chronological receipt status.
- [x] Missing targets and unavailable history abstain without zero-imputation. Fewer than two scored origins produce null metrics and no winner. Changing an unpublished target value does not change scored metrics or origin statuses.
- [x] The aggregate result includes the composed evidence receipt, fixed split boundaries, aggregate metrics and per-origin statuses, while excluding product identifiers, invoice/customer fields, raw values and review-reference strings.
- [x] A scored evaluation and its nested evidence receipt remain explicitly unverified, unauthorized and not forecast-eligible; regression assertions cover the outer result and child receipt flags.
- [x] The generated CLI uses only a deterministic fictional workbook and explicit release declarations; repeated runs produce identical result JSON under the same Python/openpyxl/zlib toolchain.
- [x] Keep the new capability `experimental`, keep `forecasting` planned, regenerate the symbol catalog, add an atlas link, and update the system map, M1 guide, model/data cards, evidence/capability ledgers, backlog, debugging and learning docs.
- [x] Run focused tests, Ruff, catalog, atlas, evidence and capability guards. Report exact full-gate and CI status; do not weaken tests or use the environment workaround as proof of HTTP execution.
- [x] Complete the canonical exact-head local quality gate on published PR #53 head `79d3679013576c6a209bed9fa031b7f0fabd0d8d`: all 700 tests plus Ruff, symbol catalog, atlas, evidence and capability checks passed at 2026-11-25 04:08:00 UTC. The earlier B-07 environment timeout is historical for PR #52 and is not evidence about this combined state.
- [ ] Required official GitHub Actions execute and pass. B-08 currently prevents repository steps; local success cannot satisfy this criterion.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m1_retail_synthetic_evaluation.py` | Add no-argument fictional fixture CLI | New integration test runs the module and checks stable sanitized output |
| Core implementation | `src/mirrormind/domains/retail/evaluation_flow.py::evaluate_retail_evidence_flow` | Add bounded composition only | New integration tests over prepared flow and adversarial cutoff/withheld-target cases |
| Reused implementation | `RetailUciEvidenceFlow`, `backtest_declared_retail_releases`, `_predict`, `_score` | No algorithm changes | Existing focused unit tests plus new composition tests |
| State / persistence / API | No persistence; `GET /v1/capabilities` | Add one experimental identifier only | Ledger/API parity guard and registered-handler check |
| Calling components | Synthetic example CLI | Add user-reproducible demonstration | CLI integration test; no external input or network |
| Downstream consumers | M1F runnable workflow | None in this slice | Typed aggregate receipt remains a future input |
| External project/contracts | None | No change | No cross-repository or WorldKernel dependency |

## Data, modeling and decision review

- Dataset card: add a card for the generated fictional retail release fixture; no external source bytes are used.
- Model card: document fixed lag-7 seasonal-naive and trailing-mean heuristics, the fixed seven-day holdout, matched origins, abstentions and absence of uncertainty calibration.
- No recommendation or action is produced; no decision trace or human approval is implied.
- All availability dates are explicit fictional declarations. `InvoiceDate` remains event time and never establishes publication time.
- The example's stable output is only reproducibility of this code/toolchain fixture. It does not establish source permission, demand completeness or predictive skill.

## 4. Constraints and risks

The wrapper must not reparse workbooks or duplicate release/forecast validation. The evaluation cutoff must agree with the evidence flow audit. Per-origin receipts can expose dates and statuses but no identifiers or values. A declared release is an unverified assertion. Baseline scores are calculated on a constructed fixture with incomplete calendar observations, not on true demand. Workbook bytes must be canonicalized if the receipt includes the content digest; do not claim byte-identical output until a regression proves it.

## 5. Implementation plan

1. Confirm the declared audit cutoff and result shape contracts in existing source and tests.
2. Add the typed-flow evaluator and a deterministic in-memory fixture CLI using the existing bounded workbook reader and release backtest.
3. Add tests for reproducibility, matched-origin receipts, withheld-target mutation, cutoff mismatch, redaction and abstention.
4. Add the dataset/model cards and engineer/learner guide; update architecture maps, evidence/capability ledgers, backlog and generated references.
5. Run focused checks and the repository gates on the exact final commit; keep local Windows timeout and official CI account restrictions separately reported.

## 6. Evidence after implementation

- Commit / PR: implementation is on `codex/m1c-01-synthetic-retail-evaluation`; merge commit `e922b03` synchronized its dependency to reviewed PR #52 head `b431d11`, and review follow-up commit `1addb7791da42939166c34a2e410737ca97a177b` adds nested receipt assertions and documentation. Draft [PR #53](https://github.com/GustavoMFDS/MirrorMind/pull/53) remains stacked on draft [PR #52](https://github.com/GustavoMFDS/MirrorMind/pull/52); no PR has been merged.
- Modified symbols and files: `evaluate_retail_evidence_flow`, deterministic fixture and CLI helpers in `examples/m1_retail_synthetic_evaluation.py`, capability/API metadata, four integration tests and the guide/cards/maps listed in the impact section.
- Tests executed, result, environment: four focused evaluation integration tests and six existing retail-backtest unit tests passed, including explicit assertions that source status and nested evidence receipts do not imply authorization or forecast eligibility. The exact-head local quality gate passed on `79d3679013576c6a209bed9fa031b7f0fabd0d8d` at 2026-11-25 04:08:00 UTC: 700 tests, Ruff, symbol catalog, atlas, evidence and capability checks. The actual API integration tests ran. One existing Starlette/httpx `TestClient` deprecation warning was emitted. This is local evidence, not official CI.
- Claim IDs and cited test path/function: `MM-REVAL-001` cites `tests/integration/test_retail_synthetic_evaluation.py::test_synthetic_cli_is_reproducible_and_returns_sanitized_origin_receipts`.
- Evidence/provenance/cutoff and uncertainty: in-memory fictional workbook and explicit caller-declared releases only. The default day-35 cutoff uses a fixed last-seven-calendar-day holdout. No publisher availability, source rights, complete demand calendar, empirical skill or uncertainty calibration is established.
- Scope of human review and approval: experimental local evaluation only; no source-use permission, real-world forecast or production approval.
- New or changed contracts: additive Python composition function with schema `mirrormind.retail.evidence_evaluation.v1`, deterministic synthetic CLI and `local_retail_evidence_evaluation` experimental capability. No evaluation HTTP endpoint was added.
- Docs updated: evaluation guide, dataset/model cards, change request, M1 plan, system map, API walkthrough, semantic map, roadmap, capability/evidence ledgers, atlas, backlog, debugging, learning and generated symbol catalog.
- Official CI: current exact PR #53 head `79d3679013576c6a209bed9fa031b7f0fabd0d8d` has failed [test run 45544705354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705354) and [symbol-catalog run 45544705397](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45544705397). Job summaries expose no steps/logs and no specific cause has been established. Prior exact annotations must not be used to infer the condition for this head.
- Known limitations / follow-up: B-01/B-02 still block real-source use and empirical evaluation. The earlier B-07 timeout is historical; the full local gate passes on the synchronized M1B/M1C state. B-08 still blocks official check evidence. Keep both PRs in draft until review and integration decisions.
- Independent explanation: the new evaluator checks the M1B-02 audit cutoff, calls the existing release backtest and wraps its aggregate metrics/status list without exposing product or invoice/customer identifiers. The CLI builds a fixed, normalized XLSX fixture in memory to make digest-bearing output repeatable; update the existing projection and backtest helpers rather than copying their algorithms.
