# Change request — M2-05 local decision report

## 1. Goal in plain language

**Current behavior:** The M1F-02 offline report embeds the complete workflow
result and renders the forecast, uncertainty, simulation and trace. The page
assumes a trace and simulation result always exist. A valid request for
`2011-02-04` abstains because the required history is incomplete; its report
JSON is valid, but the browser renderer dereferences the absent trace and
simulation result. M2-03 separately provides a deterministic scripted-provider
CLI, but the report does not show its run status, bounded tool receipts or
untrusted draft.

**Desired behavior:** Preserve the existing offline M1 report by default. Add an
explicit local `--agent-preview` option that runs the existing fixed M2-03
tools with the same bounded request values, then embeds both the complete M1
result and the minimized M2-03 report. Render successful and abstained M1
results safely. Show refusal, draft, receipts, review requirement and
non-authorization state without persisting or approving anything.

**Why:** M2-05 depends on M1F-02 and M2-03. A user should be able to inspect
the actual uncertainty and decision trace alongside the deterministic
orchestration outcome, including a fail-closed incomplete-history case. The
current failure case produces valid JSON but an unusable page.

**Out of scope:** A live model/provider, HTTP agent route, new API contract,
review identity or approval capture, persistence, business writes, public or
production deployment, new data sources, changes to M1 bounds, and raising the
M2 decision-tool replication limit above three.

## Capability status change

- `synthetic_retail_decision_workflow`, `local_synthetic_tool_orchestration`
  and `local_interactive_synthetic_report` remain `experimental`.
- No externally visible API route or `/v1/capabilities` list changes. The
  optional agent preview is local CLI/report composition only.
- Tests prove exact synthetic result embedding, bounded M2 tool composition,
  report rendering states, refusal sanitization and non-authorization. They do
  not prove browser security certification, real-data permission, forecast
  quality, authenticated review or production readiness.

## 2. Acceptance criteria

- [x] Without `--agent-preview`, keep the existing report payload byte-for-byte
  equivalent to the M1F-02 service result and retain current request bounds.
- [x] With `--agent-preview` and one to three replications, pass the same
  `as_of`, replication count and seed to the existing fixed M2-03 tool; expose
  the report status, tool receipts, digest-linked untrusted draft, mandatory
  human-review flag and false action/write flags.
- [x] Reject an agent preview above the M2-03 three-replication limit before
  creating an output file; never increase the tool or provider-call budgets.
- [x] Display a valid M1F-02 abstention without dereferencing absent trace or
  simulation fields; the corresponding M2-03 tool failure is a fixed
  `tool_failed` refusal with no draft or raw exception.
- [x] Escape both JSON payloads before embedding, retain `textContent`-only DOM
  rendering and the no-network CSP, and preserve the default report behavior.
- [x] Add normal, abstention, invalid-bound and escaping regressions; update the
  walkthrough, change request, system map, debugging/learning docs, evidence,
  capability ledger, atlas and generated symbols as applicable.
- [ ] Run the full documented local quality gate on the documentation-inclusive
  final head. Feature commit
  `2d592bd50b15c3b0d463c94e58a70be78553e8a6` already passed the complete gate
  (1,032 tests, zero skips, six checks); the final SHA and fresh receipt must
  be recorded in the review PR.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m2_portfolio_demo.py::main`, `build_report` | Add explicit optional preview flag; default remains unchanged | `tests/integration/test_portfolio_demo.py` |
| Provider example | `examples/m2_bounded_tool_orchestration.py::ScriptedSyntheticProvider` | Accept the report's bounded date/replication/seed and include the actual workflow digest in its fixed draft | `tests/integration/test_m2_tool_orchestration_cli.py`; report regression |
| UI | `examples/portfolio_demo.html` | Render success/abstention and optional M2 report without unsafe HTML interpolation | Report contract regressions; inspect generated report |
| API / contracts | Existing M1F-02 route and M2-03 strict contracts | No route or schema change | Existing API and M2-03 tests; `GET /v1/capabilities` parity |
| Documentation | `PORTFOLIO_DEMO.md`, `M2_TOOL_ORCHESTRATION.md`, source maps, evidence and this request | Explain data flow, bounds, failure behavior, verification and limitations | Catalog, atlas, evidence and capability guards |
| External project/contracts | None | No change | N/A |

## Data, modeling and decision review

- Data: generated fictional fixtures only; existing dataset cards and source
  permissions remain unchanged.
- Forecast: reuse the existing experimental seasonal-naive profile and
  uncalibrated residual diagnostic; add no accuracy or interval claim.
- Trace and human review: display existing trace and M2-03 review-required
  state; do not accept, persist or imply approval.
- WorldKernel: no new adapter or engine selection; report retains existing
  local M1 semantics.
- Temporal safety: use the existing cutoff-aware workflow; show abstention
  instead of fabricating missing history, forecast, simulation or trace.

## 4. Constraints and risks

The optional scripted preview executes the M1F-02 synthetic workflow a second
time through the existing M2-03 tool. Deterministic inputs should yield the
same workflow digest; the two result objects remain separately labeled. The
M2-03 path stays capped at three replications and two tool calls. The report is
a local snapshot, not a live UI or durable run service. The same-origin M1 API
route remains unchanged. Browser rendering tests do not establish deployed
browser isolation or screen-reader certification.

## 5. Implementation plan

1. Reproduce the `2011-02-04` abstention in the real synthetic workflow and
   trace the report renderer's unconditional field access.
2. Add regressions for default report compatibility, successful M2 preview,
   report-limit rejection, script escaping and abstention/refusal rendering.
3. Parameterize the existing scripted provider; do not add another registry,
   copy M1 algorithms, or raise the M2 contract limits.
4. Make the UI render the explicit M1 and M2 states with safe text insertion.
5. Update the full technical/educational walkthrough, capability/evidence
   records, generated symbol catalog and reviewed repository atlas.
6. Run the complete local gate on the clean final commit and record exact-SHA
   evidence separately from official CI.

## 6. Evidence after implementation

- Commit / PR: feature commit `2d592bd50b15c3b0d463c94e58a70be78553e8a6` on local candidate `codex/m2-05-usable-decision-workflow-20261128`; documentation-inclusive final gate and review PR pending.
- Modified symbols: `ScriptedSyntheticProvider.__init__`, `next_turn`,
  `build_report`, `_script_json`, `main`, `renderAgent` and `renderWorkflow`.
- Tests executed, result, environment: focused command
  `python -m pytest -q tests/integration/test_portfolio_demo.py tests/integration/test_m2_tool_orchestration_cli.py`
  passed 13 tests. The complete gate on feature commit
  `2d592bd50b15c3b0d463c94e58a70be78553e8a6` passed 1,032 tests, zero skips
  and all six checks in 45.01 seconds with Python 3.13.5 and the exact pinned
  WorldKernel. A restricted-sandbox attempt timed out in the Windows Proactor
  loopback socketpair during `test_health`; the unchanged isolated test passed
  outside that sandbox in 1.38 seconds. This diagnosis does not replace the
  required gate on the documentation-inclusive final commit.
- Claim IDs and cited test path/function: `MM-PORT-001` through `MM-PORT-005`
  cite `tests/integration/test_portfolio_demo.py` and named top-level functions
  in `EVIDENCE_MAP.json`.
- Evidence/provenance/cutoff and uncertainty: fictional fixtures and existing
  cutoff-aware M1F-02 workflow only.
- Scope of human review and approval: report requires review; no approval is
  recorded or inferred.
- New or changed contracts: none; local report adds an optional payload only.
- Docs updated: `PORTFOLIO_DEMO.md`, `M2_TOOL_ORCHESTRATION.md`, `SYSTEM_MAP.md`,
  `DEBUGGING.md`, `LEARNING.md`, capability/evidence maps, atlas, backlog,
  status, handoff, blocker and local-gate baseline notes.
- Known limitations / follow-up: no live provider, API agent route, persistent
  status, reviewer identity or production capability.
- Independent explanation: default mode serializes the existing M1 result;
  opt-in mode invokes existing M2 fixed tools with matching validated inputs.
  The provider includes the tool's workflow digest in an untrusted draft. The
  HTML renderer uses an early missing-success-fields branch for abstention and
  displays sanitized M2 refusal separately. No new source, public contract or
  authorization is introduced.
