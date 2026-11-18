# Learning while building

Goal: be able to **explain, change and troubleshoot** this project without outsourcing every step to an AI agent.

## A practical 30–45 minute session
1. Pick one real entrypoint or function from [SYSTEM_MAP](SYSTEM_MAP.md).
2. Open its source and find it in the [symbol catalog](generated/SYMBOLS.md). Read signatures, types, docstrings and all called helpers; don't assume the index captures dynamic calls.
3. Explain inputs, outputs, state changes, exceptions and invariants in your own words.
4. Trace one passing test through the function. Change a small behavior **without AI**, write a test, run it, and review the diff.
5. Ask AI to review your explanation and identify possible omissions, rather than having it write the exercise.
6. Keep a short note: "What I understood / What I can now change / What remains unclear." Only add broadly useful insights to shared docs.

## Python concepts to look up in context
- `def`, `return`, `if`, `for`, comprehensions: control flow and transformations.
- `class`, `self`, `@dataclass`, `@property`: objects, structured state and behavior.
- `typing`, `Optional`, `Protocol`, `->`: type annotations and interfaces (not necessarily runtime validation).
- `try/except/finally`, `raise`: errors, propagation and cleanup.
- `async def`, `await`: cooperative asynchronous code, not automatically parallel CPU execution.
- `with`: context managers and resource lifetime.
- `pytest`: assertions, fixtures, unit versus integration tests.

The catalog captures syntax; use official Python docs, implementation and tests to understand semantics.

## Exercises in increasing difficulty
1. Trace `POST /v1/scenarios/validate` through route, contract and test.
2. Explain how a versioned Pydantic contract validates input and how invalid input is reported.
3. Add a harmless optional validation field in a practice branch, then write tests for old and new payloads.
4. Explain the distinction between a gateway *interface* and a functioning WorldKernel integration.
5. Draft a future evidence/forecast/simulation flow that keeps observed data, predictions and simulated results distinct, without claiming that it exists.

You should be able to add a contract field, test a route and explain compatibility before agent-led feature work.
## Guided exercise 6 — input validation is not execution (30 minutes)

Read [the contract walkthrough](CONTRACT_WALKTHROUGH.md) and follow
`ScenarioSpec.check_budget` into
`tests/unit/test_contracts.py::test_exceeding_budget_rejected`.
For a nonempty `EvidenceRef.observed_until`, explain why the string
is not an authenticated timestamp or a temporal leakage check.
Trace the HTTP endpoint in [API walkthrough](API_WALKTHROUGH.md).
Write which capabilities are implemented, interface-only or merely
planned according to [the semantic map](SEMANTIC_COVERAGE.md).

## Guided exercise 7 — can this claim be reproduced? (20 minutes)

Choose an ID in [the evidence map](EVIDENCE_MAP.json), open its
guide, source and actual test. Predict the assertion before running
`python -m pytest -q`. Explain how a test could pass while the
accompanying broader prose remains unproved. Document the environment,
limit and next regression you would add.

## Guided exercise 8 — make capability claims falsifiable (30 minutes)

Read [capability promotion gates](CAPABILITY_GATES.md) and
[the reviewed ledger](CAPABILITY_LEDGER.json). Run the focused
`tests/integration/test_api.py::test_live_api_claims_equal_reviewed_capability_ledger`
regression. Explain why `SimulationGateway` is an interface and why
a declared budget and a passing scenario validation do not qualify as
implemented forecasting or world simulation. Identify the precise
provenance and negative tests required for your first M1 feature.

## Guided exercise 9 — synthetic observation gaps are not zero demand (30 minutes)

Read [M1 preflight](M1_DATA_PREFLIGHT.md) and run the standalone
synthetic fixture. Predict the missing day count before comparing
the result with
`tests/unit/test_m1_observation_preflight.py::
test_synthetic_batch_is_bounded_and_reports_gaps_without_imputation`.
Then append one future-dated row and verify its rejection.
Explain why the test only proves **date labels** are bounded
and not historical source availability, license consent,
forecast reliability or simulation safety.
