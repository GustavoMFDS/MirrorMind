# ENG-02 — maintain synthetic example lint without changing behavior

## 1. Goal in plain language

**Current behavior:** Three standalone synthetic M1 examples have five existing
Ruff findings: three import-order findings, one unused import, and RUF007 on
the adjacent-date loop in `m1_asof_rolling_backtest.py`. The loop compares
`days` with `days[1:]`; it intentionally receives pairs of equal length only
because both operands are sliced.

**Desired behavior:** Keep all three examples lint-clean. Replace the adjacent
pair construction with `itertools.pairwise`, whose ordered adjacent pairs are
equivalent for the list input and the Python `>=3.11` runtime declared by the
project. Keep the same gap rejection and error text. Sort imports and remove
the unused `date` import without changing public behavior.

**Why:** ENG-02 is a separately tracked maintenance item. The Ruff autofix
marks RUF007 unsafe; verify the sequence and boundary semantics in source and
tests instead of applying an unreviewed change.

**Out of scope:** New forecast behavior, data connectors, changes to model
metrics, public APIs, schemas, capability promotion, real datasets, M2 feature
work, Actions/workflow changes, and changes to WorldKernel.

## 2. Acceptance criteria

- [ ] `ruff check examples` passes without suppressions or unsafe autofixes.
- [ ] Adjacent-date validation preserves behavior for empty, one-date,
  consecutive and gapped sequences.
- [ ] The public as-of backtest still rejects a missing event date; all
  existing forecast, cutoff and CLI regressions remain unchanged.
- [ ] No input, output, cutoff, metric, availability, or error-contract change.
- [ ] The focused unit/CLI tests and complete temporary local gate pass on the
  exact clean commit; results are identified as local, not official CI.
- [ ] Engineering guide, debugging guidance, learning exercise, system map,
  task backlog, handoff and reviewed repository atlas explain and link the
  change.

## 3. Impact map

| Layer | Relevant file/symbol | Change? | Evidence / tests |
| --- | --- | --- | --- |
| Entrypoint | `examples/m1_asof_rolling_backtest.py::main` | No | Existing CLI integration test |
| Core example | `examples/m1_asof_rolling_backtest.py::backtest_asof` and adjacent-date guard | Yes, semantics-preserving implementation | Unit regression for pair boundaries and existing missing-day rejection |
| Other examples | `examples/m1_observation_preflight.py`, `examples/m1_temporal_backtest.py` | Import cleanup only | Existing unit and CLI tests |
| State / persistence / API | None | No | No API, state or capability contract changes |
| Callers / consumers | `tests/unit/test_m1_asof_rolling_backtest.py`; guide and CLI docs | Tests and docs only | Focused unit/CLI suites; docs guards |
| External project/contracts | None | No | No cross-project dependency |

## 4. Constraints and risks

The old loop visits exactly `(days[i], days[i+1])` for each index before the
last. `pairwise(days)` yields the same ordered pairs and yields none for fewer
than two elements. The input is already a sorted list of `date` values; this
change does not alter sorting, date parsing, availability checks, or missing
day handling. Python 3.11 satisfies `itertools.pairwise`'s availability.

The principal risk is accidentally changing the empty/singleton edge case or
the existing fail-closed gap behavior. Direct helper tests plus the public
missing-day regression cover both. No data, permissions, source terms,
credentials, or external services are involved.

## 5. Implementation and documentation

1. Extract the adjacent-date invariant into a small private helper so its
   sequence semantics can be tested directly.
2. Add boundary and gap regressions before switching the helper to
   `itertools.pairwise`.
3. Sort imports and remove the unused import; do not use `--unsafe-fixes`.
4. Update the as-of walkthrough, system map, debugging and learning guides,
   backlog, handoff and atlas.
5. Run focused regressions, Ruff and the exact-head temporary local gate.

## 6. Evidence after implementation

- Commit / PR: PR #64 on `codex/eng-02-examples-ruff`; its description records
  the final committed head, local gate receipt and validation limits.
- Modified symbols and files: `_require_contiguous_days` and its caller in
  `examples/m1_asof_rolling_backtest.py`; import order in the two preflight /
  backtest examples; no public symbol or response changed.
- Tests executed before the committed-head gate: 49 focused unit tests and 11
  CLI tests passed; `ruff check examples` and the changed-test Ruff check
  passed. Full exact-head gate evidence is published in the PR description.
- Claim IDs and limitations: no new product or capability claim; existing
  MM-ASOF-001 covers public missing-day rejection. Direct helper tests cover
  pair boundaries and gap rejection.
- Contracts changed: none.
- Docs updated: as-of method guide, system map, debugging, learning, backlog,
  handoff, repository atlas and this change request.
- Known limitations: examples remain synthetic teaching tools; they do not
  validate original-source availability, forecast quality or authorization.
- Independent explanation: for sorted `list[date]`, `pairwise` yields the
  same `(days[i], days[i + 1])` sequence as the prior slice/zip loop and has
  the same empty/singleton boundaries. The guard still rejects the first
  non-consecutive day before scoring.
