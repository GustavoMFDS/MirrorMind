# Change request — Add a versioned decision trace result contract

## 1. Goal in plain language

**Current behavior:** `ScenarioSpec` validates a subset of simulation input
fields. `DECISION_TRACE_TEMPLATE.md` describes a future review record, but no
typed result contract keeps observations, estimates and conditional outcomes
separate.

**Desired behavior:** add a strict, versioned Python result model for a single
reviewable decision trace. Require evidence references for observations,
model-card and observation references for forecasts, forecast and assumption
references for simulated outcomes, explicit missing-evidence entries,
measurement state for costs, and a human-review state tied to the exact result
digest when a decision is recorded. Terminal review time must not precede
trace creation; the canonical cost digest must be independent of Decimal
context; and collections must have explicit field, aggregate and reference
bounds before this contract is consumed by another M1 component.

**Why:** M1F-01 is a ready P0 prerequisite for the eventual end-to-end M1
comparison. A stable result shape lets later forecasting, simulation and review
components exchange traceable records without representing a schema as a
working decision engine.

**Out of scope:** API routes, persistence, signature or identity verification,
source authorization, forecast calculation, simulation execution, policy
ranking, recommendations and external business writes.

### Capability status change

- Add `decision_trace_result_contract` as `interface_only`; leave
  `decision_evaluation` planned. The route does not expose interface-only
  records as executable capabilities.
- The contract is a local Pydantic schema only. It neither authenticates
  evidence references nor proves a model or engine ran.
- Tests prove field separation, local cross-reference validation, cutoff and
  approval-digest consistency for synthetic fixtures only.
- No API capability route change is needed because no runtime endpoint is
  added. Verify route-to-ledger parity for the implemented, experimental and
  planned sets, and run the capability documentation checker.

## 2. Acceptance criteria

- [x] A v1 trace contract represents observations, forecasts, conditional
  outcomes, assumptions, missing evidence, cost measurements and human review
  as distinct typed sections.
- [x] Opaque record identifiers are unique; evidence, fact, forecast,
  assumption and outcome references resolve to the appropriate records.
- [x] Observation availability timestamps are timezone-aware, not earlier
  than their observation times, and no later than the declared trace cutoff.
- [x] Forecasts reference both observed facts and a model-card identifier;
  simulated outcomes reference forecasts, assumptions and a named engine
  contract.
- [x] Costs distinguish measured, declared and unavailable values. Unknown
  amounts cannot be represented as zero.
- [x] Approved or rejected human reviews require reviewer reference, timestamp
  and the SHA-256 digest of the result excluding the review section. A changed
  result cannot retain an approval for its old digest, and a terminal review
  cannot predate trace creation.
- [x] Decimal hashing uses lossless context-independent fixed-point text with
  explicit zero/trailing-zero semantics while preserving the v1 digest for
  ordinary cost values.
- [x] Per-section, aggregate record and per-record reference/metric bounds are
  enforced; fact-to-evidence validation uses a prebuilt evidence-ID map.
- [x] The reviewed evidence map cites each new regression by file and
  top-level test function, with explicit verification limits.
- [x] A deterministic synthetic fixture validates. Adverse tests reject bad
  references, duplicate IDs, invalid temporal ordering, invalid cost states,
  incomplete approvals, mismatched digests, pre-creation review, Decimal
  context collisions and oversized collections.
- [x] Existing `ScenarioSpec` input behavior and public API responses remain
  unchanged. No recommendation, permission grant or external action is
  inferred from an approval state.
- [x] Add a source walkthrough, examples, tests and limitations; update the
  system map, semantic matrix, atlas, backlog, learning/debugging material,
  capability/evidence ledgers and generated symbol catalog.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | None | No HTTP route | Existing API contract test remains unchanged |
| Core implementation | `src/mirrormind/core/decision_trace.py::DecisionTrace` | Add strict immutable result models and digest | New unit tests for valid and invalid traces |
| Existing input contract | `src/mirrormind/core/contracts.py::ScenarioSpec` | No behavior change | Existing `tests/unit/test_contracts.py` |
| Capability/evidence metadata | `CAPABILITY_LEDGER.json`, `EVIDENCE_MAP.json` | Add interface-only claim and bounded test evidence | Documentation guards and exact test selector |
| Calling components | None | No producer or consumer yet | Fixture constructs the contract directly |
| Downstream consumers | M1F-02 | Future only | This contract alone is not an end-to-end workflow |
| External project/contracts | None | No WorldKernel contract change | No cross-repository dependency |

## Data and decision review

- The fixture uses fictional identifiers and scalar values. The type accepts
  references as caller assertions; it does not verify access rights, source
  identity or publisher history.
- Forecast references do not prove a model card is valid or a forecast was
  computed. Engine references do not prove a simulation ran.
- A result digest detects content mismatch when recomputed; it is not a
  signature, reviewer identity proof or authorization grant.
- Approval is a review record only. A separately authorized execution path
  remains out of scope.

## 4. Constraints and risks

The v1 schema is additive and separate from the existing scenario input model.
References are opaque strings and cross-reference checks are local to one
trace; external data, model cards, engine contracts, signatures and identity
providers are not loaded. A result may contain business-sensitive scalar
values or free text, so callers must minimize and protect payloads. The
canonical result digest must use stable JSON serialization and exclude only
the human-review object, otherwise review metadata would create a circular
digest dependency. Contract collection bounds constrain one parsed object but
do not replace HTTP body-size, rate or concurrency controls.

## 5. Implementation plan

1. Confirm `ScenarioSpec`, API capability behavior, and current review/data
   templates; keep the result contract separate from scenario input.
2. Write failing tests for references, temporal cutoffs and review chronology,
   cost status and digest violations, Decimal contexts and collection bounds.
3. Implement the strict Pydantic v1 schema, bounded reference map and canonical
   context-independent digest.
4. Add the engineer walkthrough and learner exercises, then update all
   reviewed maps and capability/evidence records.
5. Regenerate the Python catalog, run focused tests, relevant suite and docs
   guards; record exact local and remote verification separately.

## 6. Evidence after implementation

The records in this section describe the initial implementation snapshot.
The subsequent review-correction evidence below supersedes its original head
and test count for current PR #54 status.

- Commit / PR: source is at
  `27f1f1c9dec3886299077793a2d42a647313d7ae` on
  `codex/m1f-01-decision-trace-contract`; current PR head is
  `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029`. Proposed as draft
  [PR #54](https://github.com/GustavoMFDS/MirrorMind/pull/54), stacked on
  draft PR #53.
- Modified symbols and files: `DecisionTrace`, `EvidenceReference`,
  `ObservedFact`, `ForecastEstimate`, `ModelingAssumption`,
  `ConditionalOutcome`, `MissingEvidence`, `CostMeasurement` and `HumanReview`
  in `src/mirrormind/core/decision_trace.py`; reproducible fixture CLI in
  `examples/m1_decision_trace_contract.py`; 12 pure unit tests.
- Tests executed, result, environment: focused unit suite passed 12 tests in
  0.29 seconds. The canonical exact-head gate on current PR head
  `83c80d865b0eabdfc7e172bc7f43e6c4d2d8b029` passed 712 tests, including the
  API integration module; Ruff, catalog, atlas, evidence and capability
  checks also passed. One existing Starlette/httpx deprecation warning was
  emitted. The earlier restricted-sandbox socket-pair stall is historical
  (B-07); its root cause is unknown.
- Claim IDs and cited test path/function: `MM-DTRACE-001` cites
  `tests/unit/test_decision_trace.py::test_valid_trace_keeps_decision_evidence_categories_separate`.
- Evidence/provenance/cutoff and uncertainty: generated fictional values only;
  no source permission, empirical model quality or real engine output.
- Scope of human review and approval: contract semantics and validation only;
  no operational authorization.
- New or changed contracts: implemented local schema
  `mirrormind.decision_trace.v1`, classified `interface_only`, additive and
  not exposed through HTTP; broader `decision_evaluation` remains planned.
- Docs updated: result walkthrough, system map, semantic coverage, capability
  gates and ledger, evidence map, repository atlas, input-contract guide,
  decision trace template, M1 plan, backlog, project status, debugging,
  learning guide and generated symbol catalog.
- Official CI: M1F implementation head `27f1f1c9dec3886299077793a2d42a647313d7ae` checks
  failed before job start: [test run 45326109821](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109821)
  and [symbol-catalog run 45326109808](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45326109808)
  carry the B-08 account payment/spending-limit annotation. This is not an
  observed test failure; no remote test result is inferred.
- Known limitations / follow-up: M1F-02 must produce and replay an actual
  synthetic evidence/forecast/simulation trace; M1B/M1C and WorldKernel gates
  remain separate. B-07/B-08 still block the exact full gate/official CI
  evidence for the stacked branch.
- Independent explanation: completed in `DECISION_TRACE_RESULT.md` and its
  linked source walkthrough and learning exercises.

## Review correction evidence — 2026-11-24

- Commit: `f02459d977fd263b03ddf60264b9069ae08b189b` on
  `codex/m1f-01-decision-trace-contract`, PR #54.
- Reproduced before correction: an approved/rejected review one second before
  trace creation validated; two distinct amounts hashed identically at Decimal
  precision 3; each record section and a reference list accepted values beyond
  the requested bounds. The corrected red run reported 11 failing assertions
  after fixture timestamps were aligned with existing cutoff data.
- Resolution: compare review timestamps by instant, canonicalize costs with
  context-independent fixed-point formatting, cap each section at 1,000, the
  full trace at 1,000 records, and nested reference/metric tuples at 100;
  resolve evidence IDs through one map. The v1 fixture digest remains
  `fccf54eccb7971ea4731e08df4baae8755a394688d47d19d2c54d8ebe1f5b4ec`.
- Verification on the correction commit: `tests/unit/test_decision_trace.py`
  passed 28 tests; `ruff check src tests`, catalog check, atlas, evidence and
  capability guards passed. The atlas used a temporary local Git excludes file
  for existing untracked Graphify output directories; no guard, project ignore
  rule or artifact was changed.
- Integrated verification: merge commit
  `07c405b0d49ab05611413acce61af1123111fb48` retains both correction commits
  as ancestry and passed the complete local gate on its exact clean SHA:
  756 tests plus Ruff, catalog, atlas, evidence and capability checks. The
  restricted replay timed out at 900 seconds; the full pass ran outside that
  sandbox. One existing Starlette/httpx deprecation warning appeared.
  Documentation follow-up `4d1d5b92e990f6d771209097fde1622c3c88958f` and
  current integrated head `970843edd260d0c794e7959150ab7c76af146ae4` also
  passed the full gate with the same source state.
- Publication / official CI: the correction branch was fast-forward-pushed at
  `9113d861affc2f4a6480f188a093f534196a0766`. On that exact published head,
  Actions [test run 45517352710](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45517352710)
  and [symbol-catalog run 45517352734](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45517352734)
  failed before repository steps with the account payment/spending-limit
  annotation. No remote test ran. A PR follow-up with commits, regressions and
  local gate evidence was posted at
  [issue comment 7148444643](https://github.com/GustavoMFDS/MirrorMind/pull/54#issuecomment-7148444643).
  B-08 remains open; local gate evidence does not substitute for official CI.
- Current PR head and validation: head
  `2794abff855665fb65f32af655415c52dde68872` passed the exact full local gate
  with 728 tests and all six stages. On that same head, Actions `test` runs
  [45518448875](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518448875)
  and [45518440891](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518440891),
  plus `symbol-catalog` runs
  [45518449130](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518449130)
  and [45518440963](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45518440963),
  carry the account payment-or-spending-limit annotation and expose no steps
  or logs. This establishes the pre-job gate category, not the specific
  account condition; no remote tests ran.
- Limits: the local contract does not authenticate reviewer/reference claims,
  trust timestamps, cap HTTP request size or concurrency, or execute a
  decision. `decision_trace_result_contract` remains `interface_only`.
