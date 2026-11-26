# Decision trace template — keep facts, estimates and simulations apart

> Copy for each reviewable recommendation or comparison.
> This document must never itself trigger a write to an external system.

## 1. Identity and authority

- Decision ID, question, user/workspace, requester:
- Authorization scope and tool permissions (sanitized):
- Review owner, created timestamp, result schema and code revision:
- Status: `draft | evaluated | awaiting_human_review | approved | rejected`:
- What action would require explicit separate human confirmation:

## 2. Observations — what was actually measured?

| Claim / metric | Unit | Authorized snapshot/card | Observation time | Availability/cutoff | Unknowns |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- Missing/late/changed observations and associated caveats:
- Do not convert a simulated state into a sourced observation.
- Verify permissions; a URI or textual citation alone does not grant access.

## 3. Forecasts — what was estimated?

| Target/horizon | Model card/version | Backtest evidence | Point estimate | Interval/calibration | Limitations |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- Training cutoff and permitted features:
- Baseline comparison, model-selection criterion and holdout:
- Drift/unknown uncertainty and appropriate abstention rule:
- No forecast value should be manufactured by an LLM.

## 4. Simulations — what follows only if the assumptions hold?

| Scenario / intervention | Engine/adapter/revision | Initial state and source | Seed, runs, compute budget | Conditional result | Limitations |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- WorldKernel request/response schema and registered world revision:
- Explicit mapping of interventions, units and feasible constraints:
- Randomness/paired exogenous conditions and sensitivity analysis:
- Checkpoint/replay identity, code version and deterministic parameters:
- Model limitations and rejected/unrepresentable conditions:
- Results are **conditional outputs**, not real-world observed effects.

## 5. Tradeoffs and human decision

- Objectives, risk tolerances and who approved them:
- Supported alternatives and why any option was excluded:
- Costs, timeouts, token and simulation compute **actually metered**:
- Sensitivity across assumptions, data gaps and forecast uncertainty:
- Evidence-backed summary plus competing explanations:
- What would make the recommendation invalid:
- Human review: who, timestamp, decision, scope and limits:
- Proposed external action and separate, explicit execution authorization:
- Audit reference, retention and revocation:

## 6. Falsifiable acceptance

- [ ] Every observed fact links to authorized, time-valid evidence.
- [ ] Every numeric forecast links to a model card and a real holdout.
- [ ] Every simulated outcome links to model/version/assumptions.
- [ ] Unsupported or missing inputs were rejected or exposed, not fabricated.
- [ ] Tool privileges and tenant access were checked outside prompt text.
- [ ] Costs/budgets are actual measured constraints or marked unimplemented.
- [ ] No irreversible action is implied by `approved` without a
  separately authorized execution tool.
- [ ] A concrete adverse regression and independent reviewer are recorded.

Use [DATASET_CARD_TEMPLATE](DATASET_CARD_TEMPLATE.md),
[FORECAST_MODEL_CARD_TEMPLATE](FORECAST_MODEL_CARD_TEMPLATE.md),
[CAPABILITY_GATES](CAPABILITY_GATES.md), and
[WorldKernel gateway acceptance](WORLDKERNEL_GATEWAY_GATE.md).

**Current status:** MirrorMind does not create traces automatically. A
local immutable v1 schema exists in
[`core/decision_trace.py`](../../src/mirrormind/core/decision_trace.py);
it validates caller-declared structure and references only. See the
[result contract walkthrough](DECISION_TRACE_RESULT.md). It is
interface-only, not an implemented Decision Engine, source authenticator,
forecast or simulation service.
