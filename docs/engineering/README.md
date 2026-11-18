# Living Engineering Knowledge

This is the entry point for **understanding, changing, testing and maintaining** this repository. It is documentation for both engineers and AI coding agents, not a substitute for reading and validating the source.

## Start here
- [System map](SYSTEM_MAP.md) — what runs, key modules, entrypoints, boundaries and cross-project relationships.
- [Repository atlas](REPOSITORY_ATLAS.md) — human-reviewed links to **every tracked code, test, config and document file**; a CI guard fails on missing files/links.
- [Change request template](CHANGE_REQUEST_TEMPLATE.md) — describe a future feature or correction in plain language before coding; map it to modules, tests and docs.
- [Debugging playbook](DEBUGGING.md) — reproduce a failure, trace behavior, identify evidence, patch and add regression tests.
- [Learning guide](LEARNING.md) — guided source reading and independent practice.
- [Generated symbol catalog](generated/SYMBOLS.md) — AST-based index of Python functions, classes, methods, signatures, locations and local imports. Run the generator if the file is not checked in.
- [Agent instructions](../../AGENTS.md) — mandatory change/documentation protocol.
- Existing canonical architecture and roadmap documents live in the parent [docs](../) directory.

## Two types of documentation
**Generated facts:** syntax-level structure such as function signatures, classes, file paths and static imports. Recreate from code with `python scripts/docs/catalog.py --write`. Static analysis does not prove live call graphs, side effects or correctness.

**Reviewed explanations:** responsibilities, design rationale, contracts, state transitions, recovery behavior, failure modes and worked examples. Maintain these alongside code changes, backed by tests and explicit decisions.

## Routine
1. Write the desired behavior and acceptance criteria in a copy of [the change request template](CHANGE_REQUEST_TEMPLATE.md).
2. Follow [the system map](SYSTEM_MAP.md), symbol index, tests and related design records to determine the actual impact.
3. Implement and test. Keep new behavior and old behavior separate in the change description.
4. Update related documents and regenerate the code index in the same PR.
5. Ask an engineer to explain the change without an agent and make a small independent test or modification.

### Commands
```bash
python scripts/docs/catalog.py --write
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python -m pytest -q
python -m ruff check src tests
```

Documentation CI requires the **committed** symbol catalog to be current, regenerates it for inspection, and verifies every tracked file has a resolving link in the reviewed atlas and local Markdown links exist. This structural check is intentionally stricter than a filename mention. It does not validate prose semantics, statistical models, privacy or execution safety; these require source review and tests.

## Scope and independence
These conventions are shared across WorldKernel, MirrorMind and NeuroShift, but the repositories remain independent. Shared documentation layout does not create shared runtime dependencies. Changes to the *contracts* between projects require separate, coordinated reviews.
