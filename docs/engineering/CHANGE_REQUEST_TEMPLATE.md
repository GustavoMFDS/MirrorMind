# Change request — <short behavior-oriented title>

> Copy this template into a PR description or a new file under `docs/engineering/changes/` for substantial work. The text below is a template, not an authorized implementation task. State uncertainty explicitly.

## 1. Goal in plain language
**Current behavior:** What actually happens now? Link a test, code path or reproduction.

**Desired behavior:** Describe what should change as if explaining it to a teammate.

**Why:** User need, operational failure or test result. Include a concrete example.

**Out of scope:** What must not change.

## Capability status change (required for user-visible features)
- Previous and proposed status from [CAPABILITY_LEDGER](CAPABILITY_LEDGER.json):
- Production behavior versus interface/experiment-only:
- Test selectors proving the *narrow* claim and their known limitations:
- Update to `GET /v1/capabilities` (or reason no externally visible change):

## 2. Acceptance criteria
- [ ] Given <state>, when <action>, then <observable result>.
- [ ] Backwards compatibility, determinism, security and error cases are addressed as applicable.
- [ ] Tests document both the normal path and the failure path.

## 3. Impact map (complete after inspecting code)
| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | TBD | TBD | TBD |
| Core implementation | TBD | TBD | TBD |
| State / persistence / API | TBD | TBD | TBD |
| Calling components | TBD | TBD | TBD |
| Downstream consumers | TBD | TBD | TBD |
| External project/contracts | None unless demonstrated | TBD | TBD |

## Data, modeling and decision review (required when applicable)
- Reviewed [dataset card](DATASET_CARD_TEMPLATE.md) (rights, provenance, event/availability cutoffs):
- Reviewed [forecast model card](FORECAST_MODEL_CARD_TEMPLATE.md) (holdout, baseline, uncertainty):
- [Decision trace](DECISION_TRACE_TEMPLATE.md) and human approval for sensitive actions:
- [WorldKernel compatibility gate](WORLDKERNEL_GATEWAY_GATE.md) (unsupported fields and revisions):
- Evidence for absence of temporal leakage and fabricated measurements:

## 4. Constraints and risks
Assumptions, data formats, versioning, performance, concurrency, security, privacy, reproducibility, migration and rollback plan.

## 5. Implementation plan
1. Trace the existing behavior through code and tests.
2. Identify and review tradeoffs; seek approval if a new architectural decision is required.
3. Implement with a focused diff and add tests.
4. Regenerate symbol reference; revise system map, runbooks, learning notes and existing docs as needed.
5. Run checks and document their **actual** results. Update the reviewed capability ledger and its live API regression for all feature promotions; run `python scripts/docs/capabilities.py --check`. For substantive behavior claims, update the reviewed [evidence map](EVIDENCE_MAP.json) only with real test paths, top-level function selectors, explicit limitations and a human-reviewed claim ID; run `python scripts/docs/evidence.py --check`.

## 6. Evidence after implementation
- Commit / PR:
- Modified symbols and files:
- Tests executed, result, environment:
- Claim IDs and cited test path/function (or reason not applicable):
- Evidence/provenance/cutoff and uncertainty, where relevant:
- Scope of human review and approval:
- New or changed contracts:
- Docs updated:
- Known limitations / follow-up:
- Independent explanation: What did I change, and where would I change it again?

## Agent instruction to paste with the request
"Read AGENTS.md and docs/engineering/README.md. Investigate this change request against the actual source, map impacted files and contracts, propose the smallest safe implementation, add regression tests, update technical and educational documentation and regenerate the Python symbol catalog. Report verified tests and unresolved risks; do not assert a feature works without evidence."
