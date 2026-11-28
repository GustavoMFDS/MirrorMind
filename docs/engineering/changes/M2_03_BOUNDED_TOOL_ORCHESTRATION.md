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

- [ ] A fixed, immutable registry exposes only fictional evidence search and
  the existing M1F-02 workflow; it adds no file, URL, command or action tool.
- [ ] Strict typed inputs, exact result contracts and bounded JSON/context
  sizes are enforced before a tool result reaches the provider.
- [ ] Provider turns, unique tool calls and total tool calls are bounded; an
  unknown or caller-disallowed tool is refused without execution.
- [ ] Invalid tool arguments, invalid tool output, provider errors, duplicate
  calls, unsupported citation refs and exhausted budgets fail closed without
  exposing raw exception details.
- [ ] An injection-like retrieved excerpt remains explicitly untrusted; a
  provider attempt to use a nonexistent private-data/action tool is refused.
  This proves registry enforcement, not immunity of a live model to injection.
- [ ] Forecast and policy numbers come only from the existing M1F-02 service;
  the provider cannot replace numeric computation. The report is synthetic,
  query-free, non-persisting, human-review-required and non-authorizing.
- [ ] The CLI example replays deterministically with the scripted provider;
  unit and integration regressions cover normal and adverse paths.
- [ ] Source walkthrough, architecture map, debugging guide, learning
  exercise, backlog/status/handoff, atlas, symbol catalog, evidence map and
  capability ledger are updated; all repository checks pass.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Contracts | `src/mirrormind/modules/agents/contracts.py` | Add strict run, provider-turn, tool-call, observation and report models | Unit validation and bounds tests |
| Registry | `src/mirrormind/modules/agents/registry.py` | Add immutable code-owned registry, exact input/output validation and digest receipts | Unknown-tool, invalid-input/output, duplicate and size regressions |
| Composition | `src/mirrormind/modules/agents/orchestrator.py` | Add synchronous bounded provider loop and citation-reference check | Unit tests for success, refusal, abstention, budgets and provider failures |
| Tool adapters | `src/mirrormind/modules/agents/synthetic_tools.py` | Wrap existing M2-01 search and M1F-02 workflow; no copied algorithms | Service-output parity and scope/injection tests |
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

- Commit / PR: pending implementation.
- Modified symbols and files: pending implementation.
- Tests executed, result, environment: pending exact-head gate.
- Claim IDs and cited test path/function: pending tests.
- Evidence/provenance/cutoff and uncertainty: fictional fixtures; M1F-02
  retains its existing as-of and model-card contracts.
- Scope of human review and approval: no human approval is simulated; every
  draft requires later review.
- New or changed contracts: local provider-turn, tool-call and result models;
  no public route or persisted schema.
- Docs updated: pending implementation.
- Known limitations / follow-up: no live provider or semantic entailment
  checking; M2-04 and M2-05 remain separate.
- Independent explanation: pending implementation.
