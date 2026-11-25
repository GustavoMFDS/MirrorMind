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

- [ ] The v1 trace model and its accepted payloads remain unchanged.
- [ ] The v2 trace adds bounded typed execution evidence and links every
  conditional outcome to one selected-output record.
- [ ] The selected execution record's engine contract equals the outcome's
  `engine_contract_ref`.
- [ ] Every execution-evidence record is referenced by at least one outcome.
- [ ] The test-double workflow records the test double as the selected result
  source and exact replay preserves its trace and result digests.
- [ ] The exact-pin WorldKernel workflow records engine-derived results as the
  selected source, binds its registered world and exact source commit, and
  records the test double separately as an invoked parity oracle.
- [ ] A mismatch between selected and parity digests or a dangling/mismatched
  execution reference is rejected.
- [ ] The local six-check gate passes with the optional reviewed WorldKernel
  pin installed and its integration tests do not skip.
- [ ] Architecture, contract, walkthrough, learning, evidence and status docs
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

- Commit / PR: pending.
- Modified symbols and files: pending.
- Tests executed, result, environment: pending.
- Claim IDs and cited test path/function: pending.
- Evidence/provenance/cutoff and uncertainty: pending.
- Scope of human review and approval: exact-pin synthetic integration only.
- New or changed contracts: `mirrormind.decision_trace.v2`; v1 remains.
- Docs updated: pending.
- Known limitations / follow-up: real-source rights and temporal evidence,
  empirical forecast evaluation, production isolation, official Actions and
  final integration review remain open.
- Independent explanation: pending.
