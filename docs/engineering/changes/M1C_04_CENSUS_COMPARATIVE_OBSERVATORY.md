# Change request - comparative fictional Research Observatory
Add an explicit all-scenarios HTML mode, keeping single scenario default.
Use all four fixed fixtures, one temporary journal, prepare all commitments
before scoring, run selected split(s) in fixed catalog order, replay through
the existing runner. Display a comparison table per split with scenario,
horizon, MAE/RMSE/WAPE per baseline and scored/requested counts; detailed
per-scenario coverage, abstentions and full provenance. No pooling, ranking,
winner, confidence interval, real data, new models or authority. Unique
anchors; native keyboard navigation, no scripts, external resources or
server. Exclusive output, deterministic bytes, no arbitrary report input.
Test real comparison values, all eight split receipts, reproducibility,
anchor integrity, default compatibility and failure paths. Browser smoke
is distinct from accessibility certification.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_research_observatory.py | Explicit comparative mode |
| Tests | tests/integration/test_census_research_observatory.py | Comparison and navigation |
| Core / API / storage | None | Reuse existing temporary journal |

No persistent history or deployment. Existing synthetic cards apply;
B-01/B-02 remain open. Independent review pending.
