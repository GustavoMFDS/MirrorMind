# Change request - local fictional research observatory
Generate a self-contained static HTML report from the existing Runner's
fixed synthetic demo, with no arbitrary report ingestion or live service.
Use explicit absolute output path and exclusive creation; never overwrite.
Display per-split/horizon MAE, RMSE, WAPE, coverage, abstentions, receipt
digests and experiment provenance. Missing metrics must not become zero.
Escape all dynamic text; no JS, network, remote fonts, resources or forms.
Show synthetic scope and abstained inference prominently. Repeated runs
with identical revision and split are byte reproducible. Tests inspect
actual HTML, failure paths and deterministic replay. Independent review
pending. No new API, dependencies, trust authority or real-data access.

| Layer | Path | Impact |
|---|---|---|
| Example | examples/m1_census_research_observatory.py | Static local report generator |
| Tests | tests/integration/test_census_research_observatory.py | Synthetic report and CLI checks |
| Core / API / persistence | None | Existing runner reused with temporary journal |

Existing synthetic dataset/model cards apply. Report output is fictional
aggregate metrics only. No authenticated registration, runtime attestation,
independent holdout protection, calibrated intervals or production claim.
B-01/B-02 remain open. Rollback is source-only; user-owned reports preserved.
