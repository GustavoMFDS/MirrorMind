# Offline interactive portfolio report

This experimental presentation layer renders existing fictional M1F-02 output
as a reproducible local snapshot. An opt-in flag composes existing M2-03
scripted orchestration and embeds its minimized report beside the M1 result.
This adds no decision engine or live service. It is independent of the optional
private WorldKernel dependency and uses no network, download, external
JavaScript, LLM, credential or server.

## Reproduce

Run from the repository root with development dependencies installed:

```bash
python -m examples.m2_portfolio_demo --as-of 2011-01-26 --replications 2 --seed 317 --output mirror-demo.html
```

This keeps original M1-only behavior. Add M2-03 with explicit opt-in:

```bash
python -m examples.m2_portfolio_demo --as-of 2011-01-26 --replications 2 --seed 317 --agent-preview --output mirror-demo-agent.html
```

The preview accepts one to three replications because the existing decision
tool caps work at three. M1-only report retains its existing bound. Reproduce
the incomplete-history branch with:

```bash
python -m examples.m2_portfolio_demo --as-of 2011-02-04 --replications 2 --seed 317 --agent-preview --output mirror-demo-abstention.html
```

Open the new file in a browser. Change displayed lead time to inspect cases
already computed. To change date, seed or replication count, rerun with a new
output path. The CLI rejects an existing path, non-HTML suffix, missing parent,
invalid request, and an agent preview above three replications before writing.
Exclusive-create mode prevents overwriting an earlier report.

## Architecture and flow

```mermaid
sequenceDiagram
  participant CLI as m2_portfolio_demo.main
  participant M1 as M1F-02 workflow
  participant M2 as M2-03 orchestrator
  participant P as ScriptedSyntheticProvider
  participant T as Fixed tool registry
  participant H as Local HTML report
  CLI->>M1: validated date, replications, seed
  M1-->>CLI: complete result or explicit abstention
  opt --agent-preview (1-3 replications)
    CLI->>M2: AgentRunRequest + same bounded values
    M2->>P: bounded question and fixed tool descriptors
    P->>T: search_synthetic_evidence
    T-->>P: citation + minimized receipt
    P->>T: run_synthetic_retail_decision
    T->>M1: same date, replications and seed
    M1-->>T: typed summary + trace/workflow digests
    T-->>P: bounded result and receipt
    P-->>M2: untrusted digest-linked draft
    M2-->>CLI: status, receipts, draft or fixed refusal
  end
  CLI->>H: escaped JSON in inert script elements
  H->>H: parse JSON; render via textContent
```

### Responsibilities and execution

- [Generator](../../examples/m2_portfolio_demo.py) `main` parses
  `--as-of`, `--replications`, `--seed`, `--output` and optional
  `--agent-preview`, then constructs existing strict
  `SyntheticDecisionWorkflowRequest`. It contains no forecasting or simulation
  algorithm.
- `build_report` calls `run_synthetic_decision_workflow` once for primary M1
  payload. With opt-in it also constructs fixed `AgentRunRequest` and invokes
  `run_bounded_tool_orchestration` with
  [the existing scripted provider](../../examples/m2_bounded_tool_orchestration.py).
  Provider receives identical date, replication count and seed. M2-03 runs M1
  again through its registered decision tool. Duplication is intentional: the
  report shows complete M1 output beside independently produced minimized tool
  output. Deterministic inputs should produce equal workflow digests.
- Provider calls immutable registry's existing fictional evidence-search and
  decision-workflow tools. The latter returns strict
  `SyntheticDecisionToolOutput`; provider authors no numbers. Final draft
  includes exact `workflow_result_sha256` from typed observation and a returned
  citation. `AgentRunReport` stores minimized input/output hashes, byte counts,
  and call names; it does not persist raw tool arguments or outputs.
- [HTML template](../../examples/portfolio_demo.html) has separate inert JSON
  elements for complete M1 result and optional M2 report. Generator emits
  sorted JSON with `allow_nan=False`, escaping `<`, `>` and `&` so payload
  cannot terminate its script element. Page reads `textContent`, parses JSON,
  and writes dynamic strings using `textContent`; it never inserts payload text
  as HTML. Restrictive CSP disallows network connections and external assets.
- `renderWorkflow` checks for `trace` and `simulation.result` before entering
  success rendering. Missing fields select a fallback with status, abstention
  reason, available uncertainty metadata and original result JSON. It does not
  impute zero or access success-only forecast, simulation or trace fields.
  Optional M2 panel stays separate and displays sanitized refusal when tool
  execution fails.
- Successful browser interactions only select precomputed lead-time cases.
  `renderCase` preserves policy order and displays mean cost, fill rate, ending
  stock, order count and stockout days. Browser does not simulate or select a
  policy.

## Contracts and interpretation

| Value | Contract / bound | Meaning |
| --- | --- | --- |
| M1 request | `SyntheticDecisionWorkflowRequest` | Existing fixture date, replication and seed validation |
| Optional M2 request | `AgentRunRequest` | Fixed two-tool allowlist, at most two tool calls and three turns |
| M2 decision-tool input | `SyntheticDecisionToolInput` | Calendar date, one to three replications and bounded seed |
| M2 report | `AgentRunReport` | `completed`, `abstained` or `refused`; draft labeled untrusted; human review required; action and writes false |
| HTML file | New `.html` path | Local snapshot; exclusive creation; no server or durable run state |

Normal M2 path uses two calls: fictional method retrieval, then M1 workflow.
When M1 abstains because required seven-day history is missing, registry
sanitizes tool failure. Orchestrator returns fixed `tool_failed`, no draft and
no raw exception. This is fail-closed reporting, not evidence an agent
understood missing data.

No API route, public schema, `/v1/capabilities` label or M1 bound changes here.
`local_interactive_synthetic_report`, `local_synthetic_tool_orchestration`
and `synthetic_retail_decision_workflow` remain experimental. No reviewer
identity, human approval, source permission, forecast validity, policy ranking
or business authority is created by rendering the report.

## Tests and evidence

Run focused regressions:

```bash
python -m pytest -q tests/integration/test_portfolio_demo.py tests/integration/test_m2_tool_orchestration_cli.py
```

- `test_offline_report_preserves_exact_workflow_result` checks unchanged
  default M1 payload, no-network CSP and safe text rendering contract.
- `test_agent_preview_composes_matching_bounded_workflow_and_digest` checks
  both payloads, same request values, tool order, digest-linked draft, review
  requirement and false authorization/write flags.
- `test_abstention_payload_and_renderer_guard_handle_missing_success_fields`
  reproduces the `2011-02-04` case, checks sanitized refusal and checks the
  abstention guard precedes success-only field reads.
- `test_agent_preview_escapes_both_embedded_payloads` uses script terminators
  in both JSON inputs and verifies safe round-trip encoding.
- `test_agent_preview_rejects_more_than_three_replications_before_output`
  proves preview cap enforcement precedes file creation.
- `test_agent_preview_cli_embeds_local_orchestration_result` covers the opt-in
  CLI; `test_report_cli_writes_only_new_explicit_html` covers default output
  and no-overwrite; `test_invalid_report_request_creates_no_output` covers
  fail-closed request/path handling.
- `test_bounded_tool_orchestration_cli_replays_minimized_receipt` continues to
  verify standalone M2-03 replay.

Evidence-map claims `MM-PORT-001`, `MM-PORT-002`, `MM-PORT-003`,
`MM-PORT-004` and `MM-PORT-005` each name the top-level test and limitation.

Python regressions inspect payloads and template guard ordering. They do not
execute browser DOM, certify browser isolation/accessibility, establish draft
entailment or measure forecast quality. Evidence-map claims cite actual test
files and top-level functions, with those limits.

## Debugging and learning

For request errors, inspect M1 date/numeric bounds and enforce at most three
replications with `--agent-preview`. For output errors, verify parent directory
exists and target path is new. A history fallback means workflow abstained;
inspect displayed status and abstention object without converting missing data
to zero or bypassing cutoff. For `tool_failed`, inspect M2 status and local M1
result; raw exception is intentionally omitted.

Exercises:

1. Generate success and abstention reports. Compare M1
   `workflow_result_sha256` to digest in successful M2 draft. Explain why
   equality supports reproducibility but does not authenticate producer.
2. Trace date, replication count and seed through `build_report`,
   `ScriptedSyntheticProvider` and `_summarize_workflow`. Name Pydantic model
   validating each boundary.
3. Trace abstention through workflow, `ToolRegistry.invoke`, fixed refusal and
   early `renderWorkflow` branch. Explain why `trace.observations` is not read.
4. Put `</script>` in a synthetic test string. Explain what escaping proves
   and what it cannot prove about a real browser.
5. Compare reports with and without the flag. Explain why extra M2 compute is
   explicit, deterministic and still experimental.

Uncertainty remains an uncalibrated residual diagnostic. Fixtures remain
fictional. No real forecast skill, ranking, approval, authorization or
production deployment follows from this report.
