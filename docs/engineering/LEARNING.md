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