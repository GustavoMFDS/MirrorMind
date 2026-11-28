# Change request — bounded synthetic tool orchestration

> Scope: M2-03 local orchestration over the already integrated fictional
> retrieval and M1 synthetic decision workflow. No live provider or external
> data is used.

## 1. Goal in plain language

**Current behavior:** M2-01 supplies scope-filtered, citation-bearing fictional
retrieval, and M1F-02 supplies one reproducible evidence-to-forecast-to-policy
comparison. No module coordinates these operations through typed tool calls.
The API validates requests but does not run an agent.

**Desired behavior:** a bounded in-process orchestrator accepts a provider
protocol implementation, validates every turn and tool payload, and exposes
only two code-owned tools: fictional evidence search and the fixed M1F-02
synthetic retail workflow. A scripted test provider demonstrates the normal
path. Tool results remain untrusted data; citations in a draft must resolve to
citations actually returned by the visible synthetic search. Every completed
draft requires human review and grants no action authority.

**Why:** M2-03 depends on the integrated M1F-02 and M2-01 components. This
connects them through a real typed execution boundary while keeping the
zero-paid budget and current no-provider authorization intact.

**Out of scope:** a live LLM/provider, credentials or provider spending,
real-source retrieval, HTTP agent execution, persistent conversations,
arbitrary/plugin/user-defined tools, business writes, automated approval,
policy selection, or semantic entailment verification. `agentic_orchestration`
remains planned for a live/usable provider workflow; the local scripted slice
is separately labeled experimental.

**Framework choice:** no orchestration framework is added. Two static tools
and a three-turn synchronous loop need no plugin loading, retries, graph
runtime or provider abstraction beyond the strict protocol in this change.
Direct Python dispatch keeps limits and refusal paths visible and avoids a new
dependency; revisit only for a concrete approved capability that the current
contracts cannot provide.

### Capability status

- Existing `agentic_orchestration`: remains `planned`.
- New `local_synthetic_tool_orchestration`: `experimental`; source and narrow
  regression are linked in the capability ledger and `/v1/capabilities`.
- The scripted provider is a test/demo double. A citation membership check
  proves reference integrity only; it does not prove that draft prose is
  entailed by the cited excerpt.
- No decision-log entry is required: no new external provider, authorization,
  persistence or framework decision is being made.

## 2. Acceptance criteria

- [x] A fixed, immutable registry exposes only fictional evidence search and
  the existing M1F-02 workflow; it adds no file, URL, command or action tool.
- [x] Strict typed inputs, exact result contracts and bounded JSON/context
  sizes are enforced before a tool result reaches the provider.
- [x] Provider turns, unique tool calls and total tool calls are bounded; an
  unknown or caller-disallowed tool is refused without execution.
- [x] Invalid tool arguments, invalid tool output, provider errors, duplicate
  calls, unsupported citation refs and exhausted budgets fail closed without
  exposing raw exception details.
- [x] An injection-like retrieved excerpt remains explicitly untrusted; a
  provider attempt to use a nonexistent private-data/action tool is refused.
  This proves registry enforcement, not immunity of a live model to injection.
- [x] Forecast and policy numbers come only from the existing M1F-02 service;
  the provider cannot replace numeric computation. The report is synthetic,
  query-free, non-persisting, human-review-required and non-authorizing.
- [x] The adapter's consumed M1F-02 result shape passes whole-package mypy
  without replacing or bypassing its runtime Pydantic contract validation.
- [x] The CLI example replays deterministically with the scripted provider;
  unit and integration regressions cover normal and adverse paths.
- [x] Source walkthrough, architecture map, debugging guide, learning
  exercise, backlog/status/handoff, atlas, symbol catalog, evidence map and
  capability ledger are updated; all repository checks pass.

### Independent-review correction — revalidate provider-owned model instances

Review reproduced a Pydantic trust-boundary gap: `model_copy(update=...)`
does not run validation. A provider can return an exact `AgentTurn` containing
an `AgentDraft` with an empty summary or a review status with no citations;
the first was reported as an abstention and the second escaped as an
uncaught `ValidationError`. A final turn with its payload removed also reached
an assertion. Before reading any discriminant or nested field, the orchestrator
must serialize the provider model into plain Python data and validate that
data again against the strict contract. Serialization or validation errors
must become the fixed `invalid_provider_turn` refusal without echoing details.

- [x] Revalidate exact `AgentTurn` instances and every nested contract from
  plain serialized data before dispatch or final-draft handling.
- [x] Refuse malformed nested values and missing/mismatched payloads with
  `invalid_provider_turn`; do not expose validation details or raise.
- [x] Add regressions for empty summary, draft status/citation mismatch,
  malformed tool call and missing tool/final payloads, each constructed with
  `model_copy(update=...)`.
- [x] Update the walkthrough, debugging and learning guides, architecture map,
  repository atlas, evidence map, and handoff/status records; retain the
  experimental capability status and existing no-action boundary.
- [x] Run the focused regressions and complete local gate on exact commit
  `48e7efe98aae2df3811302fbf7875a2bd8a48dc4`: 25 focused tests, 1,019 full
  tests, zero skips and all six checks passed; receipt is recorded in
  `LOCAL_QUALITY_GATE.md`.
- [ ] Query applicable official checks for the published correction head and
  request independent re-review after recording those exact-SHA results.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Contracts | `src/mirrormind/modules/agents/contracts.py` | Add strict run, provider-turn, tool-call, observation and report models | Unit validation and bounds tests |
| Registry | `src/mirrormind/modules/agents/registry.py` | Add immutable code-owned registry, exact input/output validation and digest receipts | Unknown-tool, invalid-input/output, duplicate and size regressions |
| Composition | `src/mirrormind/modules/agents/orchestrator.py` | Add synchronous bounded provider loop, strict plain-data revalidation of provider turns and citation-reference check | Unit tests for success, refusal, abstention, budgets, provider failures and Pydantic `model_copy` bypass regressions |
| Tool adapters | `src/mirrormind/modules/agents/synthetic_tools.py` | Wrap existing M2-01 search and M1F-02 workflow; declare the consumed internal response shape for static checking; no copied algorithms | Service-output parity and scope/injection tests; whole-package mypy |
| Demo | `examples/m2_bounded_tool_orchestration.py` | Add fixed scripted provider and query-free deterministic receipt CLI | CLI replay integration test |
| API capability | `src/mirrormind/api/routes/system.py` | Advertise only the local experimental capability; no orchestration route | Capability parity and status regression |
| Tests | `tests/unit/test_bounded_tool_orchestration.py`; `tests/integration/test_m2_tool_orchestration_cli.py`; `tests/integration/test_api.py` | Add behavior and adverse-case evidence | Named pytest selectors in `EVIDENCE_MAP.json` |
| Documentation | M2 walkthrough, change request, system map, learning, debugging, semantic coverage, hub, atlas, evidence/capability maps and handoff docs | Explain source behavior, limits and reproduction | Docs guards and source walkthrough |
| Persistence / external services | None | No state, network, credential, provider or WorldKernel call | CLI and unit tests assert deterministic local behavior |

## 4. Constraints and risks

The provider protocol is a local composition boundary, not an authentication
or safety boundary. The registered tools are read/compute only, but caller
allowlists remain caller-declared. The orchestration checks that citations
exist in observed retrieval output; it cannot determine whether arbitrary
draft wording is semantically supported. There is no live model, token/cost
meter, network timeout or durable cancellation behavior. A future provider
requires B-05 approval and a separate security/evaluation review.

## 5. Implementation plan

1. Preserve the base `main` commit and verify actual M1F-02/M2-01 callers.
2. Add regressions first for the accepted demo path and each fail-closed
   boundary.
3. Implement the fixed registry and bounded composition over existing
   contracts; do not duplicate retrieval, forecasting or simulation logic.
4. Add the deterministic demo and source-linked technical/learning guide.
5. Regenerate the symbol catalog, stage new paths before checking atlas
   coverage, and run the complete local quality gate.
6. Publish one M2-03 review PR; do not merge it or #82.

## 6. Evidence after implementation

### Independent-review correction

Independent review reproduced nested Pydantic validation bypasses in the
provider-returned `AgentTurn` path on the earlier source candidate. The fix
serializes the exact model into plain Python data and strictly reconstructs
the complete nested contract before dispatch or draft consumption. Five
regressions cover an empty summary, a draft status/citation invariant, an
invalid nested tool call, and missing final/tool payloads. The exact correction
commit, complete local-gate receipt and current official check state are
recorded in the live [PR #87](https://github.com/GustavoMFDS/MirrorMind/pull/87);
do not transfer prior checkpoint results to that commit.

- Commit / PR: implementation checkpoint `0922c72`; the open review PR is
  [#87](https://github.com/GustavoMFDS/MirrorMind/pull/87). Exact local gate
  checkpoints `07a6cdc0` and `2d71d39` passed; independent review and
  integration remain separate acceptance decisions.
- Modified symbols and files: `modules/agents/contracts.py`,
  `modules/agents/registry.py`, `modules/agents/synthetic_tools.py`, the
  focused unit test, and source walkthrough/learning/debugging/evidence docs.
- Tests executed, result, environment: focused suite passes 21 tests; exact
  commit `2d71d39` passed 1,014 tests, zero skips and all six local checks with
  the reviewed WorldKernel pin. Code-identical commit `07a6cdc0` passed 86.92%
  coverage and both mypy jobs. The queried exact PR #87 head `2d71d39` had 12
  successful official check-runs and two conditionally skipped jobs.
- Claim IDs and cited test path/function: `MM-AGENT-001` through
  `MM-AGENT-009` in `EVIDENCE_MAP.json`.
- Evidence/provenance/cutoff and uncertainty: fictional fixtures; M1F-02
  retains its existing as-of and model-card contracts.
- Scope of human review and approval: no human approval is simulated; every
  draft requires later review.
- New or changed contracts: local provider-turn, tool-call and result models;
  no public route or persisted schema.
- Docs updated: M2-03 walkthrough, learning exercise, debugging guide,
  change request, system map, status, backlog, handoff, local gate and evidence
  map; each local validation receipt stays scoped to its exact SHA.
- Known limitations / follow-up: no live provider or semantic entailment
  checking; M2-04 and M2-05 remain separate.
- Container/remote validation: local Docker engine unavailable, while the
  exact PR #87 head's official container-smoke check passed. The owner-reported
  included-allowance exhaustion and zero-paid budget remain unchanged; public
  `ubuntu-latest` runs were observed and no billing setting was changed. Neither
  protection nor verifier is bypassed.
- Independent explanation: this increment aligns the previously delivered M2-03
  code with main's new whole-package typing gate. Exact built-in containers are
  still traversed recursively and bounded; type annotations and casts are
  static only. Runtime trace/output validation remains Pydantic-based, and the
  fixed tool registry and no-action behavior are unchanged.
