# Engineering agent instructions

Read [the engineering knowledge hub](docs/engineering/README.md) before editing code or documentation.

## Non-negotiable workflow
1. Understand the request and the actual code. Treat generated references as an index, not as proof of runtime behavior.
2. For meaningful behavior, API, state, operational or architectural changes, first fill in a copy of [the change request template](docs/engineering/CHANGE_REQUEST_TEMPLATE.md), including explicit acceptance criteria and an impact map. Small editorial changes can skip a separate change request.
3. Locate the implementation, upstream callers, downstream consumers, tests and existing architecture decision records. Record confirmed links versus hypotheses.
4. Implement the smallest appropriate change, add or update tests, and do not silently broaden the scope.
5. Update human-written documentation in the same PR: [system map](docs/engineering/SYSTEM_MAP.md), relevant docs under docs/, [debugging](docs/engineering/DEBUGGING.md), [learning](docs/engineering/LEARNING.md), and a decision log entry only when a decision is actually approved.
6. Regenerate the source symbol catalog using `python scripts/docs/catalog.py --write` when source changes. Verify with `python scripts/docs/catalog.py --check`. Never hand-edit the generated file. **In the same PR**, add a real Markdown link in [the reviewed repository atlas](docs/engineering/REPOSITORY_ATLAS.md) for every new tracked code, config, test or document path; run `python scripts/docs/coverage.py --check`. Plain filenames do not satisfy the guard.
7. Run relevant tests and lint; report what was actually executed, outcomes, limitations and any deferred work. For reviewed claims in [the evidence map](docs/engineering/EVIDENCE_MAP.json), cite the actual test **file and top-level function**, add an explicit limitation, and run `python scripts/docs/evidence.py --check`. Changes affecting user-visible capabilities must update the [capability ledger](docs/engineering/CAPABILITY_LEDGER.json), verify `GET /v1/capabilities` matches implementation and run `python scripts/docs/capabilities.py --check`. A capability may not be promoted based on schema existence or aspirational docs. This checks references, not test execution or claim semantics. Do not use a passing AST/atlas guard as proof of semantic completeness or correctness. No claims of CI success until verified.
8. Keep project boundaries intact. Cross-project compatibility is handled by explicit, versioned contracts and separate PRs; never quietly edit another repository or introduce a hard dependency.

## Integrity and safety
- Never invent implemented features, test results, function behavior or system guarantees. Every new evidence/forecast/simulation/agent capability must distinguish `implemented`, `interface-only`, `experimental` and `planned`, and update `/v1/capabilities` truthfully when externally visible.
- Avoid untrusted arbitrary execution, exposing tokens, personal data, or copying customer payloads into logs/docs.
- Follow existing licensing, threat-model and research-quality restrictions. For any real data ingestion, a reviewed [dataset card](docs/engineering/DATASET_CARD_TEMPLATE.md) must document rights, snapshot, availability-time and retention. For any numeric forecast claim, a [model card](docs/engineering/FORECAST_MODEL_CARD_TEMPLATE.md) must document temporal holdouts, baselines and uncertainty evidence. For recommendations, maintain a [decision trace](docs/engineering/DECISION_TRACE_TEMPLATE.md) separating observed facts, forecasts, modeled outcomes and human approval. These are **requirements for future features**, not evidence those features already exist.
- Explain the likely cause of an incident as a hypothesis until reproduced or supported by evidence.
- Preserve backwards compatibility unless the change request explicitly approves breaking behavior and migration. Before implementing a WorldKernel adapter, follow the [versioned gateway acceptance gate](docs/engineering/WORLDKERNEL_GATEWAY_GATE.md): reject unrepresentable fields rather than guessing or silently discarding them.
- Avoid edits to generated artifacts other than by the generator; prefer documentation tied to symbols, tests and behavior.
- For requests written in Portuguese, respond in Portuguese but keep repository source docs in English for consistency.

## Hand-off format
Summarize: change intent; impacted files/functions; contracts and compatibility; tests and results; docs changed; unresolved risks; how a human can independently inspect or reproduce.
