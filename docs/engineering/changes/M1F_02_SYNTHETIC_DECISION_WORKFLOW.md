# Change request — M1F-02 synthetic retail decision workflow

> Scope: a reproducible fictional end-to-end CLI and HTTP workflow composed
> from the existing M1B-02, M1C-01, M1D-01, M1E-03 and M1F-01 slices. This
> request does not complete the real-data or actual-engine gates.

## 1. Goal in plain language

**Current behavior:** the repository has separate fictional evidence staging,
fixed-baseline evaluation, residual diagnostics, a policy test double and a
decision-trace schema. The example CLIs do not join them. The API only validates
scenario declarations and does not produce a decision result.

**Desired behavior:** one local service, a CLI and an experimental HTTP route
build the in-memory fictional retail fixture, select observations whose
caller-declared availability is at or before an explicit cutoff, run the
existing retrospective evaluation and uncertainty diagnostics, make a
predeclared 28-day seasonal-naive profile, compare the existing three policy
rules with paired random streams, and serialize a validated `DecisionTrace`.
When the last seven calendar days are not all present and published, the service
returns an explicit abstention and does not run policy simulation.

**Why:** M1F-02 is the next product-facing P0 slice. Its pieces currently exist
only as isolated examples and contracts, so an engineer cannot replay a
single synthetic evidence-to-comparison path or inspect one trace linking its
facts, forecasts, assumptions, conditional outcomes and evidence gaps.

**Out of scope:** real-source permission or ingestion, empirical accuracy or
uncertainty claims, a WorldKernel adapter/runtime call, forecast selection by
holdout score, policy ranking/recommendation, persistence, identity, human
approval, or any operational write. Actual-engine completion remains gated by
B-04 and M1E-02.

### Capability status change

- Previous/proposed: no integrated workflow capability / `experimental` under
  `synthetic_retail_decision_workflow`.
- Behavior: a bounded in-memory fixture, local seasonal-naive projection,
  existing synthetic policy test double, API serialization and CLI output.
  Nothing in this change is production or an authorized forecast.
- Narrow proof: `tests/unit/test_synthetic_decision_workflow.py` and
  `tests/integration/test_retail_synthetic_decision_workflow_cli.py`, plus the
  API cases in `tests/integration/test_api.py`. These prove only deterministic
  local behavior on fictional inputs; they do not establish source rights,
  model quality, calibrated intervals, WorldKernel execution or authority.
- `GET /v1/capabilities` will advertise the new ID only as experimental and
  must match the reviewed capability ledger.

## 2. Acceptance criteria

- [x] CLI and `POST /v1/decision-workflows/retail/synthetic` produce the same
  canonical `mirrormind.synthetic_retail_decision_workflow.v1` result for the
  same bounded request; no result or source bytes are persisted.
- [x] The workflow builds on the declared release audit at the requested
  cutoff. It requires seven distinct consecutive calendar days with positive
  projected units and `available_on <= cutoff`; missing, late or unpublished
  history yields a structured abstention with no forecasts, outcomes or
  policy-simulator invocation. It never substitutes zero for a missing day.
- [x] The successful path predeclares `seasonal_naive_lag7` and produces 28
  integer-unit steps by repeating the last seven eligible values. Model choice
  is not selected from the returned holdout scores. Every trace forecast points
  to its seven observed facts and the versioned synthetic model card.
- [x] The result includes the existing matched-origin evaluation and the
  M1D-01 disjoint residual diagnostic. It labels the diagnostic
  `heuristic_envelope_not_prediction_interval`, has no nominal/calibrated
  interval claim, and does not attach a guarantee to the 28-day forecast.
- [x] The existing M1E-03 three-policy test double receives the predeclared
  profile and bounded inventory/cost assumptions, retains shared stream digests
  across policies and lead-time sensitivities, and emits no ranking. The trace
  represents these outputs as conditional outcomes with references to the
  forecast and all relevant assumptions; human review stays `not_requested`.
- [x] The result and trace identify unauthenticated synthetic evidence,
  unavailable real compute/engine costs, missing source-rights and empirical
  validation evidence, `worldkernel_not_invoked`, and no action authorization.
- [x] Request validation rejects unknown fields, booleans where integers are
  required, invalid cutoffs, out-of-range seed/replication budgets, and malformed
  assumptions before work starts. The endpoint cannot accept arbitrary files,
  URLs, commands or user-defined tools.
- [x] Tests prove byte-stable CLI replay, API/service parity, valid trace
  references/cutoffs, late/missing/unpublished abstentions with zero simulation
  calls, and that changing a post-cutoff synthetic value does not change the
  forecast profile or conditional policy metrics.
- [x] Technical walkthrough, model card, source map, debugging/learning guides,
  status/backlog, capability/evidence records, atlas and generated symbol
  catalog are updated; required catalog, atlas, evidence and capability guards
  pass. M1F-02 remains `partial` until actual-engine acceptance is available.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m1_retail_decision_workflow.py::main` | Add deterministic local CLI | CLI integration replay and error cases |
| Core workflow | `src/mirrormind/domains/retail/synthetic_decision_workflow.py::run_synthetic_decision_workflow` | Compose evidence, evaluation, uncertainty, fixed baseline, simulation and trace | Service unit tests |
| Fixture / shared baseline | `examples/m1_retail_synthetic_evaluation.py`; `src/mirrormind/domains/retail/synthetic_fixtures.py`; `src/mirrormind/modules/forecasting/baselines.py` | Extract fixture for package/API reuse; expose bounded lag-7 profile projection without changing one-step behavior | Existing retail evaluation regressions and new profile tests |
| API | `src/mirrormind/api/routes/decisions.py`; `src/mirrormind/api/app.py`; `src/mirrormind/api/routes/system.py` | Add bounded-request experimental route and truthful capability; no public-exposure controls are provided | `tests/integration/test_api.py` |
| Existing dependencies | `evidence_flow.py`, `evaluation_flow.py`, `residual_envelope.py`, `policy_simulation.py`, `core/decision_trace.py` | Reuse; no duplicate evaluator, residual, policy or trace contract | Dependency tests plus producer assertions |
| State / persistence | None | No files, database, external service or business state | API/CLI tests and architecture walkthrough |
| Downstream consumers | `GET /v1/capabilities`; `CAPABILITY_LEDGER.json`; `EVIDENCE_MAP.json` | Advertise only experimental behavior and bind evidence | Capability/API and evidence guards |
| External project/contracts | WorldKernel remains untouched | Actual execution deferred to B-04/M1E-02 | Trace gap and explicit capability limits |

## Data, modeling and decision review

- Dataset card: only the generated in-memory fixture is used. The existing
  synthetic release declarations do not prove a real publisher's rights or
  availability; no external dataset bytes are read.
- Model card: add a narrow model card for the fixed, integer-valued
  seasonal-naive profile. The only holdout metrics are fixture diagnostics;
  no empirical skill or calibrated uncertainty is claimed.
- Decision trace: use the M1F-01 typed records. Separate observed product-day
  facts, 28 forecast estimates, assumptions, paired conditional outcomes,
  evidence gaps, unavailable runtime cost and not-requested human review.
- WorldKernel gate: no adapter or external engine call is added. Trace and
  result explicitly report `worldkernel_not_invoked`.
- Leakage/evidence: filter each fact by its declared release date at the
  chosen cutoff, require the complete last seven-day input window, and test a
  mutation strictly after the cutoff. No holdout score chooses the model.

## 4. Constraints and risks

Keep compatibility for the existing M1C-01 example's module and function
defaults. Validate strict bounds before building the workbook or running the
three policies. The route has no file upload, URL fetch, persistence, ranking,
review mutation or action execution. The trace's fixture dates and creation
time are synthetic logical timestamps for byte-reproducible artifacts, not a
wall-clock audit record. Policy costs are abstract declared assumptions, not
money or business costs. The API may report a successful synthetic comparison
while the entire real-data/engine MVP remains incomplete. B-04 and B-08 remain
independent blockers.

## 5. Implementation plan

1. Reuse the already-reviewed PR #58 stack and merge the existing PR #56
   implementation locally as a separate dependency base; preserve both PRs.
2. Extract the shared synthetic fixture without changing M1C-01 defaults.
3. Add the bounded fixed-lag forecast profile and the end-to-end service.
4. Add CLI/API entrypoints and normal, abstention, leakage and contract tests.
5. Update technical, educational and capability/evidence documentation,
   regenerate the symbol catalog, and add atlas links for every new path.
6. Run the canonical local gate and report the exact branch/commit; verify
   official Actions separately and retain B-08 if jobs still cannot start.

## 6. Evidence after implementation

- Commit / PR: `6a1c960de684a1786809f61ab7bf919371bf9cd1`, draft [PR #59](https://github.com/GustavoMFDS/MirrorMind/pull/59), based on `codex/m1f-02-dependency-stack`.
- Modified symbols and files: `run_synthetic_decision_workflow`, `_eligible_observation_rows`, `_build_trace`, `SyntheticDecisionWorkflowRequest`, `POST /v1/decision-workflows/retail/synthetic`, `project_seasonal_naive_lag7`, `build_synthetic_evidence_flow`, bounded CLI and shared M1C-01 example exports; see [walkthrough](../M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md) and [atlas section 55](../REPOSITORY_ATLAS.md#55-synthetic-retail-decision-workflow-experimental-no-action-authority).
- Tests executed, result, environment: exact-commit canonical local gate passed 766 pytest tests and all six checks on implementation commit at 2026-11-24 18:15:20 UTC; documentation/evidence follow-up `0e18005d01ce481e7f3aba094649f347ec4b26dc` also passed at 18:26:08 UTC. Focused service/API/CLI set passed 46 tests. Python 3.12 environment; one existing Starlette/httpx `TestClient` deprecation warning.
- Claim IDs and cited test path/function: `MM-MF-001` — `tests/unit/test_synthetic_decision_workflow.py::test_successful_workflow_produces_valid_trace_and_explicit_gaps`; `MM-MF-002` — `::test_incomplete_or_late_history_abstains_without_running_policy_test_double`; `MM-MF-003` — `::test_post_cutoff_fixture_mutation_does_not_change_forecast_or_comparison`; `MM-MF-004` — `tests/integration/test_retail_synthetic_decision_workflow_cli.py::test_synthetic_decision_cli_replays_trace_and_paired_policy_comparison`; `MM-API-004` — `tests/integration/test_api.py::test_synthetic_retail_decision_route_returns_the_shared_service_result`.
- Evidence/provenance/cutoff and uncertainty: fictional fixture only; all
  publication dates are caller-declared and the residual diagnostic is
  uncalibrated.
- Scope of human review and approval: local comparison only; none requested or
  represented as approved.
- New or changed contracts: experimental HTTP request/result schema and
  produced M1F-01 `DecisionTrace`.
- Docs updated: M1F-02 walkthrough/model card/change request, API walkthrough, system and semantic maps, capability/evidence ledgers, atlas, debugging/learning, retail MVP, roadmap, execution plan, project status and backlog.
- Known limitations: actual WorldKernel, authorized data, empirical forecasts,
  uncertainty calibration, human identity/review, persistence and writes remain
  absent.
- Official CI: the first inspected PR #59 test run [45457848087](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45457848087) and symbol-catalog run [45457847930](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45457847930) failed before steps; those historical runs had empty step summaries and log downloads returned 404 `BlobNotFound`. On reviewed PR #59 head `bde8625b90bc7a9bdfe27558514a37c6dcc386e0`, `test` runs [45528710417](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45528710417) and [45528704274](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45528704274), plus `symbol-catalog` runs [45528710354](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45528710354) and [45528704303](https://github.com/GustavoMFDS/MirrorMind/actions/runs/45528704303), all failed before any repository step. Their check-run details include the account payment-or-spending-limit annotation; it does not establish which specific account condition applies. No remote test ran. See [B-08](../BLOCKERS.md).
- Independent explanation: start with the [M1F-02 walkthrough](../M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md), replay the CLI command there, then compare its JSON fields to the trace schema and cited test functions.

## Independent review correction — decision identity and complete result binding

### Goal and motivation

Source review of PR #59 found that `_build_trace` uses only `as_of` and `seed`
for `trace_id` and `decision_ref`, while fixing every revision at 1. Two
requests with the same date and seed but different replication counts therefore
receive the same identity despite different policy outcomes. The successful
response also exposes `trace_sha256`, which binds the serialized M1F-01 trace
only; it does not bind the separate evaluation, residual, fixture-receipt or
simulation result in the surrounding workflow response. After #58, the policy
comparison exposes `modeling_caveats`, but #59 does not yet carry them into the
decision trace.

The correction derives a deterministic decision identity from the validated
request and a set of explicitly versioned result-artifact digests. Exact
replays retain the same identity and revision; a different request or any
different artifact content receives a different identity. Revision `1` means
the first immutable result for this content identity; it is not an incrementing
review or persistence history.

The response retains `trace_sha256` as the digest of the trace alone. It adds
versioned digests for evaluation, uncertainty, forecast evidence, forecast and
simulation artifacts, plus `workflow_result_sha256` over the complete response
including the trace and those digests. These hashes provide reproducible
content binding only: they are not signatures, source authentication or human
approval. `human_review` remains `not_requested` and no action is authorized.
The exact #58 profile-policy caveats become trace `ModelingAssumption` records
referenced by each `forecast_aware_order_up_to` conditional outcome.

The FastAPI route remains part of the experimental API scaffold. Its current
implementation has no identity/tenant authorization, request-body size limit,
rate limit or concurrency control; “local-only” is not enforced by the route.
Do not expose it on a public or production deployment. Adding those operational
controls is outside this correction and remains an explicit exposure gate.

### Acceptance criteria

- [x] Same request and generated artifacts replay to the same trace ID,
  decision reference, revision and trace digest.
- [x] Changing `replications` while keeping `as_of` and `seed` fixed changes
  both trace identity and the result digest; all outcome-affecting result
  artifacts are included in the canonical identity input.
- [x] The response declares a schema version and SHA-256 digest for each
  evaluation, uncertainty, forecast-evidence, forecast and simulation artifact.
- [x] `trace_sha256` independently recomputes from only the serialized
  `DecisionTrace`; `workflow_result_sha256` independently recomputes from the
  complete successful response excluding only its self-referential digest.
- [x] Both policy-model caveats from #58 appear as trace assumptions and
  are referenced by profile-aware conditional outcomes. The existing trace
  schema, API route, non-authorization flags and `not_requested` review state
  remain compatible.
- [x] Tests reproduce an identity collision between different replication
  counts, verify exact replay, mutate a bound nested artifact, and confirm the
  profile-aware caveat is preserved in trace assumptions/references.
- [x] Technical, debugging and learning walkthroughs explain both digests,
  identity semantics, output artifact versions, deployment limits and tests;
  the evidence map, atlas, generated catalog and full local gate pass.

### Impact and constraints

| Layer | Relevant file/symbol | Change | Evidence |
| --- | --- | --- | --- |
| Service identity | `synthetic_decision_workflow.py::_build_trace` | Hash request plus versioned artifact digests; set content-addressed IDs | Identity replay/collision unit tests |
| Workflow envelope | `run_synthetic_decision_workflow` | Add per-artifact digests and whole-response digest | Independent canonical recomputation and tamper test |
| Trace content | `_build_trace`, `_policy_outcomes` | Carry policy caveats as assumptions referenced by applicable outcomes | Trace caveat regression |
| Public route | `api/routes/decisions.py` | No route behavior change beyond additive result fields | Existing service/API parity regression |
| Documentation | M1F-02 walkthrough, trace guide, system map, debugging, learning, CR, evidence/backlog | Explain identity, digest scope, limitations and reproducibility | Documentation guards and exact-head gate |
| Persistence/authority | None | No storage, authentication, signature, approval or write added | Existing non-authorization assertions |

Keep the response schema label at v1 because these are additive result
metadata fields and existing required fields retain their meaning. Do not
interpret `revision=1` as a server-issued history, or either SHA-256 value as
trust in an asserted source, model, policy or human identity. Fixing transport
limits or authorization would be a separate reviewed change.

### Implementation and evidence record

1. Add failing regressions for the replication collision, deterministic replay,
   whole-response digest/tampering and trace caveat propagation.
2. Implement a compact sorted-key UTF-8 JSON digest helper and explicit
   artifact schema identifiers; do not hash arbitrary Python repr output.
3. Keep the trace digest contract separate from the workflow-envelope digest.
4. Update source catalog and the M1F-02/trace learning and debugging docs.
5. Run the focused tests, then the exact integrated canonical local gate.
6. Record the commit, receipt and official Actions outcome separately here and
   in the PR response; do not promote the experimental capability.

**Current evidence state:** the collision, incomplete digest scope and missing
caveat propagation were reproduced by focused red regressions before the
service correction. The corrected workflow unit, CLI and API tests then passed
16 tests, and focused Ruff passed; pytest reported one existing
Starlette/httpx deprecation warning. Normal merge commit
`ffbeb637517f18490571554a1cfa8a3ab9434bb7` includes PR #59's prior head and
the latest PR #58 head. Its exact integrated local gate passed 790 tests and
all six stages; receipt: `C:\Users\gusta\AppData\Local\Temp\mirrormind-ffbeb637-quality.json`.
The earlier 766-test receipt on published PR #59
head `a5951e49a78796908ecd1975c65052b5a2548cd7` predates these corrections and
does not validate them. The documentation follow-up head `bde8625b90bc7a9bdfe27558514a37c6dcc386e0`
also passed the exact full local gate with 790 tests and all six stages; its
receipt is `C:\Users\gusta\AppData\Local\Temp\mirrormind-bde8625b-quality.json`.
The current Actions runs are recorded above and in [B-08](../BLOCKERS.md):
they failed before repository steps with an account payment-or-spending-limit
annotation. The annotation does not identify the specific account condition,
and no remote test executed. Official CI remains unresolved; do not treat the
passing local gate as a substitute.
