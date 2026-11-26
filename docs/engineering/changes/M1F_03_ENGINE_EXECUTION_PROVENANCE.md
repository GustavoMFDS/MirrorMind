# Change request — bind selected simulation engines into decision traces

## 1. Goal in plain language

**Current behavior:** The opt-in local WorldKernel CLI receives policy metrics
from WorldKernel and stores them in the response, but `_build_trace` writes the
test-double contract into every `ConditionalOutcome`. The gateway also invokes
the test double to check exact parity, while the response says
`policy_test_double_invoked=false`. The selected output source and the parity
oracle are therefore ambiguous in machine-readable results.

**Desired behavior:** Keep `mirrormind.decision_trace.v1` unchanged. Add a
versioned v2 trace contract for the composed workflow. Each conditional outcome
must link to exactly one selected-output execution record whose contract
matches `engine_contract_ref`. An optional parity-oracle record must be linked
separately and must have the same selected-result digest after the gateway
accepts exact parity. Record the WorldKernel package version, source commit,
world, registered version, result schema and raw worker-result digest in its
provenance reference. Report selected-result source and actual simulator
invocation independently.

**Why:** The independent review reproduced a result whose declared engine was
the test double even though the exact-pin WorldKernel run produced the selected
metrics. Trace identity and outcome digests must preserve that provenance for
replay and review.

**Out of scope:** Real-source acquisition, empirical forecast claims, policy
ranking, HTTP engine execution, WorldKernel repository changes, deployment,
authentication, hostile-code isolation and business writes.

## Capability status change

- Previous and proposed status: `synthetic_retail_decision_workflow` remains
  experimental. No capability is promoted.
- Production behavior versus interface/experiment-only: local synthetic CLI
  execution only; HTTP and default CLI continue using the Python test double.
- Tests: `tests/unit/test_synthetic_decision_workflow.py` checks the selected
  engine contract, output source, execution references and deterministic replay
  for the default engine. `tests/integration/test_worldkernel_policy_world_engine.py`
  checks the exact installed engine, selected engine provenance, separate
  parity-oracle execution and deterministic replay.
- `GET /v1/capabilities` remains unchanged because engine selection remains a
  local experimental workflow capability.

## 2. Acceptance criteria

- [x] The v1 trace model and its accepted payloads remain unchanged.
- [x] The v2 trace adds bounded typed execution evidence and links every
  conditional outcome to one selected-output record.
- [x] The selected execution record's engine contract equals the outcome's
  `engine_contract_ref`.
- [x] Every execution-evidence record is referenced by at least one outcome.
- [x] The test-double workflow records the test double as the selected result
  source and exact replay preserves its trace and result digests.
- [x] The exact-pin WorldKernel workflow records engine-derived results as the
  selected source, binds its registered world and exact source commit, and
  records the test double separately as an invoked parity oracle.
- [x] A mismatch between selected and parity digests or a dangling/mismatched
  execution reference is rejected.
- [x] The local six-check gate passes with the optional reviewed WorldKernel
  pin installed and its integration tests do not skip.
- [x] Architecture, contract, walkthrough, learning, evidence and status docs
  explain how to reproduce and inspect both paths.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m1_retail_decision_workflow.py` | No | Existing explicit `--engine worldkernel` entrypoint |
| Core implementation | `core/decision_trace.py::DecisionTraceV2`, `ConditionalOutcomeV2`, `ExecutionEvidence` | Yes | Trace contract regressions in `tests/unit/test_decision_trace.py` |
| Workflow | `domains/retail/synthetic_decision_workflow.py::_policy_outcomes`, `_build_trace`, `run_synthetic_decision_workflow` | Yes | Both-engine identity, source and execution-reference tests |
| Engine gateway | `modules/simulation/worldkernel_policy_gateway.py::compare` | Yes | Exact-pin gateway and CLI integration regressions |
| State / persistence / API | No persistence changes; CLI/API trace version changes only on shared synthetic workflow | Yes | API default path plus workflow contract tests |
| Calling components | CLI comparator injection | No signature change | Existing CLI integration test and new exact-replay assertions |
| Downstream consumers | Existing v1 examples retain v1; workflow emits v2 | Yes | Version-specific validation tests and docs |
| External project/contracts | WorldKernel pinned runner contract | No | Exact source pin and registered-world metadata checked by integration test |

## Data, modeling and decision review

- Dataset card: not applicable; automated tests continue using generated data.
- Forecast model card: no forecast behavior changes.
- Decision trace: execution evidence describes produced outputs and is kept
  separate from historical input evidence whose availability must precede the
  decision cutoff.
- WorldKernel gate: exact world/version mapping remains strict and unchanged.
- Temporal leakage: no input cutoffs or source availability behavior changes.

## 4. Constraints and risks

Execution evidence is a reproducible local record, not a signature, attestation,
independent scientific validation or human identity. WorldKernel parity still
compares the same modeled transition rules on fictional inputs. The v2 schema is
additive for the workflow but is not accepted by the v1 model; the original v1
class and example remain available. Test-double invocation metadata changes to
report the observed call even when the call serves only as a parity oracle.

## 5. Implementation plan

1. Reproduce the published candidate's selected-engine/contract mismatch and
   parity invocation semantics.
2. Preserve v1 and introduce v2 typed execution provenance linked to outcomes.
3. Emit truthful selected-source and parity fields from both engine paths.
4. Add regressions for v1 compatibility, both-engine replay, provenance,
   mismatched contracts, missing references and parity digest mismatch.
5. Update source walkthroughs, architecture map, evidence references and
   learning exercises.
6. Run the complete exact-clean-head local gate with the reviewed WorldKernel
   pin installed and no skipped engine tests.

## 6. Evidence after implementation

- Commit / PR: code commit `74330d811145f10fcaaddadc56c3f95e7c8b7a85`, consolidated [PR #62](https://github.com/GustavoMFDS/MirrorMind/pull/62); resolves PR #59 review finding [7174402947](https://github.com/GustavoMFDS/MirrorMind/pull/59#issuecomment-7174402947).
- Modified symbols and files: `DecisionTraceV2`, `ConditionalOutcomeV2`, `ExecutionEvidence`; workflow `_policy_outcomes` and `_build_trace`; WorldKernel gateway result metadata; both-engine tests and architecture/learning/reference docs.
- Tests executed, result, environment: full exact-head gate on `74330d8` passed 832 tests with no skips and all six checks, with WorldKernel `0.0.1` installed from source commit `9b133ef873f2b6a7206c9c5742d40df4fccdb04a`. One pre-existing Starlette/httpx TestClient deprecation warning appeared. The final documentation head is gated separately; its JSON receipt is stored under ignored `results/local-quality-gate-<full-head-sha>.json`, and its exact SHA/result is linked from the PR #62 review discussion.
- Claim IDs and cited test path/function: `MM-DTRACE-008` — `tests/unit/test_synthetic_decision_workflow.py::test_trace_rejects_execution_evidence_from_a_different_engine_contract`; `MM-DTRACE-009` — `tests/unit/test_synthetic_decision_workflow.py::test_trace_rejects_unreferenced_execution_evidence_records`; `MM-WKPW-006` — `tests/integration/test_worldkernel_policy_world_engine.py::test_m1_cli_worldkernel_option_runs_end_to_end_with_synthetic_data`; default-engine replay — `tests/unit/test_synthetic_decision_workflow.py::test_successful_workflow_produces_valid_trace_and_explicit_gaps`.
- Evidence/provenance/cutoff and uncertainty: test inputs are generated and fictional. WorldKernel execution metadata binds package version, exact source commit, registered world/version, result schema and raw worker-result digest; selected metrics digest remains distinct. Same-rule parity checks are not independent validation, signatures or installed-file attestation.
- Scope of human review and approval: exact-pin synthetic integration only.
- New or changed contracts: `mirrormind.decision_trace.v2`; v1 remains.
- Docs updated: decision trace contract, API and system walkthroughs, learning guide, system map, debugging guide, evidence map, capability/semantic references, repository atlas, project status, task backlog, blocker register, local gate procedure and handoff.
- Known limitations / follow-up: real-source rights and temporal evidence,
  empirical forecast evaluation, production isolation, official Actions and
  final integration review remain open.
- Independent explanation: review comment `7174402947` reproduced the mismatch on predecessor `995f55d`; the corrected contract now rejects outcome/contract mismatch, dangling/orphan references and parity digest disagreement, and the exact-pin CLI regression proves WorldKernel is the selected source while the test double is separately recorded as the parity oracle.

## 7. Independent review follow-up — v2 execution chronology

The independent review reproduced a v2 deserialization gap: an execution
record with `produced_at` one day after `created_at` is currently accepted,
even though that evidence is part of an already-created immutable trace.

### Follow-up acceptance criteria

- [ ] `DecisionTraceV2` rejects execution evidence whose timezone-aware
  `produced_at` instant is later than trace `created_at`.
- [ ] Equal instants and earlier instants are accepted, including equal times
  written with different timezone offsets; comparison uses absolute instants.
- [ ] The v1 `DecisionTrace` contract and accepted v1 payloads remain unchanged.
- [ ] The synthetic workflow continues to emit valid provenance: its
  `created_at` and `produced_at` values are deterministic logical fixture
  timestamps at the declared cutoff boundary, not wall-clock audit time.
- [ ] Regressions reproduce after-creation rejection, earlier acceptance,
  timezone-equivalent equality and the unchanged v1 fixture.
- [ ] The trace contract guide, M1 workflow guide, system map, debugging and
  learning exercise explain the invariant and the logical-time limitation.
- [ ] The exact-clean-head local six-check gate passes with the reviewed
  WorldKernel pin installed; no official Actions result is inferred.

| Layer | Follow-up impact | Evidence |
| --- | --- | --- |
| Core v2 contract | Add chronological validation to `DecisionTraceV2.check_execution_evidence`; no field/schema change | `tests/unit/test_synthetic_decision_workflow.py` timestamp regressions |
| V1 compatibility | No implementation change | Existing v1 fixture and digest tests in `tests/unit/test_decision_trace.py` |
| Producer | No timestamp generation change; keep logical deterministic fixture time | `test_successful_workflow_produces_valid_trace_and_explicit_gaps` |
| Documentation | Distinguish chronology validation from clock authenticity | Decision trace walkthrough, retail workflow walkthrough, system map, debugging and learning guide |
