# Change request — matched-origin descriptive Census evaluation

## Goal and scope
M1C-04 already returns synthetic aggregate metrics and origin eligibility but
not paired origin losses. Add a separate opt-in in-process descriptive
receipt over the exact same evaluation pass. Preserve v2 result and defaults.
No real data, acquisition, inference, winner, provider, API route, persistence,
or permission changes. B-01/B-02 remain open.

## Acceptance and impact map
- Existing v2 function and CLI return the same contract and numeric behavior.
- The new function emits exact rational absolute losses for matched scored
  origins only, with horizon, issue date, target and selected-vintage digest.
- Bind the descriptive report to the complete normalized input manifest,
  split label, origin schedule, row contents and existing v2 evaluation.
- Explicitly abstain from inferential conclusions on every result; a split
  label does not prove a locked holdout or cross-split independence.
- Preserve all date, numeric, record and origin bounds. No imputation.
- Test paired arithmetic, exclusion, deterministic binding, invalid inputs,
  unchanged v2 output and JSON serialization.

| Layer | Symbol or path | Impact |
|---|---|---|
| Core | census_evaluation.py | Shared private evaluator and optional loss collector |
| Caller | evaluate_census_vintage_backtest | Compatible wrapper; no new public API route |
| Local research | evaluate_census_vintage_descriptive | Separate experimental result |
| Tests | test_census_vintage_evaluation.py | Synthetic regressions |
| State / API / external dependencies | None | No capability promotion |

## Data and scientific limits
Use the existing fictional Census card and model card. Exact errors are
value-bearing derived data, not sanitized real-source output; only fictional
fixtures are permitted. Exploratory local coverage studies found inadequate
coverage of nominal 95% intervals under persistent and seasonal dependence.
Neither bootstrap nor group-t is promoted. Descriptive differences are not
causal or calibrated. No new model or decision authority.

## Implementation and evidence
Reuse the validated scoring loop, not a second forecast algorithm. Preserve
existing tests, add paired regressions, regenerate symbols, update guide,
model card, atlas, system map, debugging and learning. Run focused tests,
whole-package typing and exact-head gate. Independent review pending; no merge
authority inferred. Rollback is a source-only revert; no persisted state.
