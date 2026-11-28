# M2-03 — bounded local tool orchestration

This guide traces the experimental in-process orchestration in
[`modules/agents`](../../src/mirrormind/modules/agents/) and the deterministic
demo at
[`m2_bounded_tool_orchestration.py`](../../examples/m2_bounded_tool_orchestration.py).
It composes the already integrated fictional M2-01 retriever with the M1F-02
synthetic decision workflow. The only shipped provider is a scripted example
double; no model, network service, credential, persistent session or public
agent route is present.

## 1. Purpose and current boundary

M1F-02 already computes a traceable fictional path: availability-aware input,
fixed seasonal-naive profile, uncertainty diagnostics, paired policy
simulation and a versioned decision trace. M2-01 already provides bounded
BM25 retrieval over generated documents with scope-first filtering and exact
citations. M2-03 adds a typed control loop that can ask for those existing
results without copying their algorithms or letting provider text execute as
Python.

The registered tool set is fixed in code:

| Tool | Input | Existing implementation called | Output boundary |
| --- | --- | --- | --- |
| `search_synthetic_evidence` | Bounded query and `top_k` | `build_fictional_index().search(EvidenceQuery(...))` | Up to ten excerpts with `untrusted_evidence`, exact citation and digest-bound `citation_ref` |
| `run_synthetic_retail_decision` | Fixture date, 1–3 replications and seed | `run_synthetic_decision_workflow(SyntheticDecisionWorkflowRequest(...))` | Typed forecast profile, paired policy summaries, caveats, selected test-double provenance and M1 trace/workflow digests |

The workflow tool intentionally wraps the existing M1F-02 composition. It
does not provide separate arbitrary forecast or simulation functions that
accept model-authored numeric data. Its forecast and simulation values are
computed by M1 code, and policy rankings remain uncomputed. The registry has
no filesystem, URL, shell, business-write, approval or action tool.

No third-party agent framework is used. This slice has two static tools, a
strict local provider protocol and a sequential maximum of three turns; an
ordinary Python loop plus Pydantic contracts makes dispatch, refusal and byte
budgets directly reviewable. A framework would add provider/plugin/context
behavior that this scope does not need and could obscure the narrow
authorization boundary. Reconsider only when an approved provider use case
requires measured capabilities the current contracts cannot supply.

`GET /v1/capabilities` advertises `local_synthetic_tool_orchestration` as
`experimental`. Generic `agentic_orchestration` stays `planned`; the local
scripted slice does not establish live-model grounding, identity or production
readiness.

## 2. Architecture and execution flow

```mermaid
sequenceDiagram
  participant C as Local caller
  participant O as run_bounded_tool_orchestration
  participant P as Injected provider protocol
  participant R as Fixed ToolRegistry
  participant E as M2-01 fictional retrieval
  participant W as M1F-02 synthetic workflow

  C->>O: AgentRunRequest + trusted local provider
  O->>P: bounded question, allowed descriptors, untrusted observations
  P-->>O: typed ToolCall
  O->>O: dump plain data and revalidate AgentTurn + nested contracts
  O->>R: verify registered name and caller allowlist
  R->>R: validate strict JSON input and size
  alt search_synthetic_evidence
    R->>E: fixed demo scope + EvidenceQuery
    E-->>R: exact citations, untrusted excerpts
  else run_synthetic_retail_decision
    R->>W: bounded SyntheticDecisionWorkflowRequest
    W-->>R: forecast, policy outcomes and DecisionTraceV2
    R->>R: validate and minimize typed summary
  end
  R-->>O: validated JSON + SHA-256 receipt
  O->>P: next bounded turn; tool output remains untrusted data
  P-->>O: final draft or another typed ToolCall
  O->>O: check observed citation membership and budgets
  O-->>C: query-free receipt; human review required; no authority
```

The orchestrator is synchronous and sequential. It admits at most three
provider turns and two tool-call attempts per run. A successful example uses
two calls and a third final turn. Every allowed tool name must belong to the
fixed registry. Provider-selected names are checked again before execution.
Duplicate call IDs, unregistered or disallowed tools, strict-contract errors,
oversized inputs/outputs/contexts and provider failures stop the run with a
fixed refusal code.

There is no hidden retry. A provider error, tool error or invalid final result
does not trigger a second attempt or expose its raw exception text. Successful
tool receipts store the call ID/name, canonical argument digest, output digest
and UTF-8 byte count; they omit raw arguments, query, excerpt and tool payload.
The provider necessarily sees the bounded question and prior tool JSON through
the in-process protocol. The returned draft is preserved for its caller but
is labeled `untrusted_provider_draft`.

## 3. Contracts and responsibilities

### `contracts.py`

All public value models inherit the frozen, strict `_AgentModel` with
`extra="forbid"`. `AgentRunRequest` bounds the question to 512 characters,
tool allowlist to the two fixed names, calls to 0–2 and provider turns to 1–3.
`ToolCall` limits top-level fields, nested JSON depth/nodes, scalar sizes and
finite numeric values before the registry serializes them. `AgentTurn` must
contain exactly one of a tool call or final `AgentDraft`.

`ProviderRequest` contains only the question, the static names/descriptions/
input-field lists for allowed tools, and previous `ToolObservation` values.
Each observation is a bounded JSON string, has a SHA-256 over its exact UTF-8
bytes, and is labeled `untrusted_tool_output`. Evidence excerpts inside the
retrieval result also retain `untrusted_evidence`.

`AgentDraft` has two terminal states. A `draft_for_human_review` must cite at
least one observed retrieval citation. An `insufficient_evidence` response
must have no citations. `AgentRunReport` contains only success receipts,
counts, refusal state and the untrusted draft. Its model validator enforces
`human_review_required=true`, `action_authorized=false` and
`writes_performed=false` for every state.

### `registry.py`

`ToolDefinition` binds one reviewed name to exact input/output model classes
and one trusted local callable. `ToolRegistry` copies the bounded definition
tuple into a read-only name map; it has no `register` or plugin-loading API.
`describe` exposes input field names, not handlers.

`invoke` converts the provider's JSON-shaped arguments into canonical,
sorted-key UTF-8 bytes, caps them at 8 KiB, validates them with
`model_validate_json(..., strict=True)`, then calls the handler. The handler
must return the exact declared output class. That value is serialized,
revalidated against the output contract and capped at 16 KiB before it can
become an observation. The registry derives SHA-256 digests from the exact
canonical input/output bytes. Fixed error codes deliberately hide handler
exception text.

The registry class can be constructed by trusted Python composition code for
unit tests. The exported orchestration path defaults to the two reviewed
synthetic tools, and no HTTP caller can supply a registry.

### `synthetic_tools.py`

`_search_synthetic_evidence` builds the existing fixed demo index for each
call. It accepts only the demo fixture's scope; callers cannot name another
principal or collection. `citation_ref` is a SHA-256 of the canonical typed
`EvidenceCitation`, while `EvidenceCitation` itself retains source/snapshot
refs and the exact excerpt digest.

`_summarize_workflow` invokes M1F-02 with a strict fixture date, at most three
replications and a bounded seed. It validates the resulting `DecisionTraceV2`
and its digest, requires all three fixed policy outcomes, and verifies each
lead-time scenario kept identical exogenous demand-stream digests across
policies. Its compact output retains the seasonal-naive 28-day profile,
model-card ref, units, assumptions status, seeds, aggregate policy metrics,
all modeling caveats, test-double engine contract, trace digest and complete
workflow digest. It omits per-day observations and the full trace body.

The summary is validated from the actual M1F-02 output. The provider cannot
substitute its own forecast or simulation values through either tool.

The adapter declares the consumed M1F-02 result shape with private `TypedDict`
types. They describe an existing in-process return value for static checking;
they do not parse or trust external JSON. The adapter still constructs and
validates `DecisionTraceV2` and `SyntheticDecisionToolOutput` at runtime, and
the registry validates that exact output model again before exposing it to a
provider. This keeps the shape declaration aligned with the source workflow
without adding a second runtime schema or copying the workflow algorithm.

### `orchestrator.py`

`run_bounded_tool_orchestration` validates the exact request and registry
types, reads the provider's declared `test_double` protocol mode inside a
sanitizing failure boundary and requires an exact built-in string value,
constructs each provider context and enforces its 64 KiB canonical byte limit.
After `next_turn`, `_revalidate_provider_turn` requires the exact `AgentTurn`
class, converts it to plain Python data with `model_dump(mode="python")`, then
rebuilds it using `AgentTurn.model_validate(..., strict=True)`. This second
pass checks nested `ToolCall`/`AgentDraft` constraints and model validators
before the orchestrator reads `kind`, dispatches a tool, or returns a draft.
Pydantic's `model_copy(update=...)` skips validation; checking the outer
instance type alone therefore does not establish a valid contract. Any dump or
validation exception becomes the sanitized `invalid_provider_turn` refusal.
The provider's raw value and validation detail are never added to the report.
It counts
every call attempt, checks the two-call budget, rejects unknown or
caller-disallowed names, and delegates typed validation/execution to the
registry. It retains each successful observation only in memory for the next
turn.

At a final turn, `_observed_citation_refs` reparses only successful evidence
tool outputs under their exact result contract. Every cited reference must
belong to those outputs. This is reference membership, not semantic
entailment, claim verification, source authenticity or relevance scoring.
The orchestrator returns a draft only when that membership check passes.

## 4. Failure behavior and security limits

| Condition | Result | What does not happen |
| --- | --- | --- |
| Unknown tool name | `refused / tool_not_registered` | No handler is looked up or executed |
| Known tool outside caller allowlist | `refused / tool_not_allowed` | No tool execution |
| Extra or malformed tool argument | `refused / invalid_tool_input` | No handler call, no raw input in report |
| Provider returns an invalid `AgentTurn` or nested model | `refused / invalid_provider_turn` | Plain-data revalidation rejects bypassed field/model constraints and missing/mismatched payloads before dispatch; raw exception details are omitted |
| Handler returns a different model | `refused / invalid_tool_output` | No output is sent to provider |
| Tool or provider throws | `tool_failed` or `provider_failure` | Raw exception is not returned |
| Missing citation in retrieved outputs | `refused / unsupported_evidence_reference` | Draft prose and unknown ref are omitted |
| Call/turn/context budget exceeded | Fixed refusal | No extra call is executed |
| Injection-like source text asks for private/action access | The fake provider may ask; registry refuses absent tool | No registry expansion or private/action handler exists |

The prompt-injection regression proves that an unregistered tool request cannot
expand this fixed registry. It does **not** prove that a live model will ignore
hostile text or that allowed tools will always be selected appropriately.
Caller-declared allowlists and the retrieval demo principal are not
authentication. The provider's `test_double` mode is a self-declared local
protocol marker, not cryptographic attestation or an isolation boundary.

The source data and tests are generated fiction. The local workflow does not
send data to a provider, use credentials, persist conversations, measure
tokens/cost, enforce concurrent server quotas or perform a business action.
It creates no human approval record. A provider-generated summary may be
inaccurate even when its citation ref exists. M2-04, M2-05, B-05 and the M2
definition-of-done gates remain open.

## 5. Reproduce the demo

From the repository root:

```powershell
uv run --no-sync --extra dev python -m examples.m2_bounded_tool_orchestration
uv run --no-sync --extra dev python -m pytest -q tests/unit/test_bounded_tool_orchestration.py
uv run --no-sync --extra dev python -m pytest -q tests/integration/test_m2_tool_orchestration_cli.py
uv run --no-sync --extra dev ruff check src/mirrormind/modules/agents examples/m2_bounded_tool_orchestration.py tests/unit/test_bounded_tool_orchestration.py tests/integration/test_m2_tool_orchestration_cli.py
```

The CLI uses fixed fictional text and a scripted provider. It prints a
deterministic query-free receipt with two successful tool calls, a digest for
each input and output, one draft and the non-authorization flags. It does not
print the question, retrieved excerpt, full forecast, full policy report or
trace body. Re-running with the same Python/Pydantic/toolchain should produce
the same JSON; the digests make byte changes visible.

## 6. Tests and what they establish

| Test | Evidence | Limitation |
| --- | --- | --- |
| `tests/unit/test_bounded_tool_orchestration.py::test_scripted_provider_runs_fixed_synthetic_tool_sequence` | Calls the fixed retriever and actual M1F-02 workflow, validates the two receipts and review/no-action flags | No live provider, runtime isolation or real-source evaluation |
| `...::test_scripted_provider_replays_identical_query_free_receipt` | Two scripted runs return identical minimized reports and omit the question/excerpt/private marker | Reproducibility only for this toolchain and fixtures |
| `...::test_injection_like_evidence_cannot_expand_the_tool_registry` | The adversarial fixture remains untrusted; an attempted private-data tool is refused | Does not certify how a generative model interprets prompts |
| `...::test_caller_allowlist_refuses_a_known_but_disallowed_tool` | A registered workflow outside the request allowlist is not invoked | The allowlist is a caller input, not identity/authorization |
| `...::test_tool_input_cannot_override_fictional_access_scope` | Strict `extra="forbid"` rejects a provider-supplied principal override before handler execution | Only the fixed local registry is covered |
| `...::test_unobserved_citation_is_refused_as_unsupported_evidence` | Final citations must resolve to visible prior retrieval outputs | Membership does not prove semantic support or source truth |
| `...::test_non_contract_provider_result_fails_closed` and `...::test_provider_error_is_sanitized_from_the_receipt` | Invalid provider values and thrown provider details cannot become a successful report | No transport retry, timeout or live-provider error taxonomy |
| `...::test_provider_turn_revalidates_nested_draft_fields_before_consumption` and `...::test_provider_turn_revalidates_nested_status_and_citation_invariants` | Exact `AgentTurn` instances corrupted with Pydantic `model_copy(update=...)` are rebuilt from plain data; empty summaries and review drafts without citations return `invalid_provider_turn` | Local in-process regressions for declared contracts; they do not isolate a provider or prove semantic citation support |
| `...::test_provider_turn_revalidates_nested_tool_call_before_dispatch` | A nested call with an empty ID is refused before the tool-attempt counter or registry changes | Proves this malformed call path only; Python provider code is not sandboxed |
| `...::test_provider_turn_with_missing_matching_payload_fails_closed` and `...::test_provider_turn_with_missing_tool_payload_fails_closed` | `model_copy(update=...)` cannot remove the required payload without a fixed refusal | Covers missing payloads for both turn kinds, not every possible malformed object graph |
| `...::test_provider_mode_inspection_failure_is_sanitized_and_fails_closed` and `...::test_non_test_double_provider_mode_is_refused_before_dispatch` | A missing/malformed/unreadable mode is refused before any provider turn; the property exception is not echoed | `test_double` remains self-declared and provides no provider identity or attestation |
| `...::test_provider_turn_budget_stops_before_an_extra_tool_call` and `...::test_tool_call_budget_records_the_refused_attempt_and_never_executes_it` | Turn/call ceilings are enforced and the refused attempt is visible as a count | No concurrent server-level quota |
| `...::test_duplicate_provider_call_id_is_refused_before_second_invocation` | Duplicate IDs fail before executing the second call and only the first success is receipted | In-process regression only; no distributed job/idempotency guarantee |
| `...::test_tool_registry_fields_cannot_be_reassigned_or_deleted` | The immutable registry rejects ordinary reassignment and deletion of its name map and definition tuple | Python encapsulation is not an isolation boundary; no HTTP caller can supply a registry |
| `...::test_registry_rejects_wrong_exact_output_contract` | Registry refuses a handler returning an untyped output | Does not prove arbitrary native-code containment |
| `...::test_registry_rejects_tool_input_over_the_canonical_json_byte_budget` | Canonical UTF-8 tool arguments over 8 KiB are refused before input-model validation or handler execution | Byte accounting covers canonical JSON, not every transient Python allocation |
| `tests/unit/test_bounded_tool_orchestration.py::test_tool_call_recursively_accepts_bounded_builtin_json_containers` and `...::test_tool_call_rejects_cyclic_and_oversized_nested_json_containers` | Nested exact built-in JSON lists and dictionaries are walked; cycles and containers above 64 items are rejected | Does not constrain arbitrary custom Python objects or every transient allocation |
| `...::test_registry_rejects_validated_output_over_the_utf8_byte_budget` | A valid declared output model over 16 KiB is refused before creating a provider observation | Does not impose process memory isolation or measure the handler's intermediate allocations |
| `...::test_registry_sanitizes_handler_exception_details` | Handler failure produces `tool_failed` without copying exception text to the caller | No worker-process containment, cancellation or timeout is provided |
| `tests/unit/test_bounded_tool_orchestration.py::test_scripted_provider_runs_fixed_synthetic_tool_sequence` plus `mypy --warn-unused-ignores src/mirrormind` | Exercises the existing M1F-02 response through the adapter and checks all 71 package modules against the declared source shape | Static typing does not validate an arbitrary runtime response; Pydantic contracts remain the runtime boundary |
| `tests/integration/test_m2_tool_orchestration_cli.py::test_bounded_tool_orchestration_cli_replays_minimized_receipt` | Documented command runs end-to-end and does not echo query or excerpt | One process, generated data and local execution only |
| `tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger` | Public capability status set matches the reviewed ledger | Structural/status parity is not semantic feature proof |

All cited tests must be run separately; a selector's existence is not a
passing result. The reviewed selectors and limitations are recorded as
`MM-AGENT-001`, `MM-AGENT-002`, `MM-AGENT-003`, `MM-AGENT-004`,
`MM-AGENT-005`, `MM-AGENT-006`, `MM-AGENT-007`, `MM-AGENT-008`,
`MM-AGENT-009`, `MM-AGENT-010`, `MM-AGENT-011`, `MM-AGENT-012`,
`MM-AGENT-013`, and `MM-AGENT-014` in the
[`EVIDENCE_MAP.json`](EVIDENCE_MAP.json).

## 7. Learning exercises

1. Read `AgentRunRequest`, then trace one `ToolCall` through
   `ToolRegistry.invoke`. Explain why date strings are validated from JSON
   bytes and why output is revalidated before it reaches the provider.
2. Run `test_injection_like_evidence_cannot_expand_the_tool_registry`. Change
   the attempted name to the registered M1 workflow and explain why the
   allowlist and compute budget still constrain the effect.
3. Replace the citation digest with another well-formed 64-character value.
   Predict why `unsupported_evidence_reference` is returned before the draft
   reaches the report. Then explain why a real ref still does not prove the
   summary is entailed by the excerpt.
4. Compare the workflow tool's `workflow_result_sha256` and each scenario's
   paired demand digest. Change only the seed and explain which digests and
   metrics should change without interpreting the output as empirical demand.
5. Propose a genuine human-approval record and authenticated tool scope. Keep
   both out of this local slice; identify the identity, persistence and audit
   requirements M3 must satisfy before any action tool exists.

## 8. Debugging and evolution

For `invalid_tool_input`, inspect the fixed input model and its `extra="forbid"`
fields; do not print the raw arguments. For `invalid_tool_output`, compare the
exact handler return class with the registered `output_model` and re-run the
normalizer against an M1 fixture. For `unsupported_evidence_reference`, parse
the prior `search_synthetic_evidence` observation with
`EvidenceSearchOutput` and compare citation refs; do not infer semantic
relevance from a matching digest. For a budget refusal, inspect provider turn
and tool attempt counts; do not raise the constants just to make a demo pass.

To add a tool later, first define its narrow input/output contracts, identify
its source permission and side effects, and add adverse tests for unknown,
disallowed, malformed and oversized calls. Review whether it can write state,
use network or expose private data before adding it to the fixed registry.
Live providers require B-05 owner approval, explicit data-transfer and spend
review, a distinct provider/model evaluation, redacted telemetry, server
budgets and injection/unsupported-evidence evaluation. Do not route a local
protocol directly into an HTTP endpoint.

## 9. M2-05 presentation composition

The optional `--agent-preview` mode in the
[offline portfolio report](PORTFOLIO_DEMO.md) composes this existing runner
with the exact bounded M1F-02 request. The local scripted provider receives the
same date, seed and one-to-three replication count as the main report. The
decision tool runs M1F-02 again and the final untrusted draft contains that
tool result's workflow digest. The report keeps full M1 output and minimized
M2 output in separate JSON payloads; neither becomes approval or action.

This opt-in path is local CLI presentation only. It adds no API route, provider,
session storage, identity, external dependency or new tool. If M1F-02 abstains
for incomplete history, the registry sanitizes its tool exception to
`tool_failed`; the report displays this fixed refusal and an M1 abstention
panel. The report's client code handles missing trace and simulation result
before reading success-only fields. Reproduce both branches and inspect their
limits in `tests/integration/test_portfolio_demo.py::test_agent_preview_composes_matching_bounded_workflow_and_digest`
and
`tests/integration/test_portfolio_demo.py::test_abstention_payload_and_renderer_guard_handle_missing_success_fields`.
Those tests inspect report payloads and guard order; they do not run a browser
DOM or certify browser isolation.
