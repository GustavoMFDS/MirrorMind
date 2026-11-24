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

## Guided exercise 10 — what makes a forecast defensible? (45 minutes)

Read the [M1 execution plan](M1_EXECUTION_PLAN.md), the
[dataset card](DATASET_CARD_TEMPLATE.md) and
[forecast model card](FORECAST_MODEL_CARD_TEMPLATE.md).
Explain why the observation date and its first available
date can differ, and design a counterexample demonstrating
temporal leakage despite an apparently valid cutoff.
Before writing a more complex model, specify a
seasonal-naive baseline and **predeclared** holdout.
Explain why no current MirrorMind endpoint can claim
forecast quality from passing ScenarioSpec validation.

## Guided exercise 11 — simulation is not a business decision (30 minutes)

Read the [WorldKernel compatibility gate](WORLDKERNEL_GATEWAY_GATE.md)
and [decision trace template](DECISION_TRACE_TEMPLATE.md).
List which MirrorMind 0.1 scenario fields cannot be sent
unchanged to WorldKernel exchange v1. Predict how an
unsupported intervention, unverified ForecastRef and
world-version mismatch should fail. Distinguish a
conditional simulation outcome from observed sales,
a valid forecast and a human-approved action.

## Guided exercise 10 — rolling-origin forecasts without lookahead (35 minutes)

Read [M1 synthetic temporal backtest](M1_TEMPORAL_BACKTEST.md)
and inspect `examples/m1_temporal_backtest.py:_predict`.
Compute the seven synthetic test-day forecasts and MAEs by hand,
then inspect
`tests/unit/test_m1_temporal_backtest.py::
test_each_one_step_prediction_receives_only_prior_observations`.
Explain why `values[:i]` excludes the target `values[i]`,
and why a rolling one-step assessment must not be advertised
as a fixed-origin seven-day forecast. Finally, contrast a
missing day with a measured zero; the first must trigger
abstention in this demonstration.

## Guided exercise 11 — event time versus availability time (30 minutes)

Read [synthetic as-of availability](M1_AVAILABILITY_PRECHECK.md)
and run the standalone example. Before execution,
predict why January 3 is absent from the January 6
eligible total even though the event occurred before
the cutoff. Trace
`tests/unit/test_m1_availability_preflight.py::
test_unavailable_value_change_cannot_change_eligible_aggregate`.
Change its count and explain why the January 6
aggregate remains unaffected. Then identify the
provenance evidence necessary to verify actual
publication timing for a real-world dataset.

## Guided exercise 12 — do not hide forecast abstentions (35 minutes)

Read [the as-of rolling guide](M1_ASOF_ROLLING_EVALUATION.md).
Predict the three unavailable January origins and
compute the baseline scores on the remaining four
February dates. Read
`tests/unit/test_m1_asof_rolling_backtest.py::
test_all_origins_can_abstain_without_fake_scores`
and explain why a model with 4/7 coverage cannot
be claimed superior to a model scored on all seven
without a carefully aligned comparison. State how
real publication-time evidence would differ
from dates typed into a JSON fixture.

## Guided exercise 13 — immutable does not mean authentic (35 minutes)

Read [the local CSV staging guide](M1_LOCAL_CSV_STAGING.md)
and follow `stage_csv_snapshot` to
`available_as_of`. With the invented fixture,
explain why the Jan 2 value is missing from a Jan 3
as-of view but the Jan 3 recorded **zero** remains.
Then modify one byte while reusing the previous
digest: predict the failure and identify which
source rights and publication dates the check
still cannot establish. Inspect
`tests/unit/test_evidence_snapshots.py::
test_digest_mismatch_fails_before_interpreting_unverified_bytes`
and explain why computing a new digest from an
untrusted file is not proof of publisher identity.

## Guided exercise 14 — staged and evaluated are still not authorized (40 minutes)

Read the [source-method guide](M1_STAGED_ROLLING_BASELINES.md)
and trace `backtest_staged_snapshot` through
`available_as_of`. With the invented weekly fixture,
explain why three of the seven requested one-day
origins abstain and why both baselines score the
**same four targets**. Inspect
`tests/unit/test_staged_rolling_baselines.py::
test_all_forecast_inputs_precede_origin_and_have_available_seven_day_window`
and predict the first and final seven-value input
tuples. Then explain why a zero MAE on repeated
synthetic seasonality is not evidence of licensed
real-world forecasting quality.

## Guided exercise 15 — the right to read is not the right to use (25 minutes)

Read [M5 source due diligence](datasets/M5_ACCESS_REVIEW.md),
then compare the official competition rules and
a third-party archive description. Identify what
would establish authorized **research** use,
what additional terms might control **commercial**
use, and which evidence is missing. Explain why
a SHA-256 match, a publicly downloadable zip or a
Creative Commons license on a *paper* cannot
automatically authorize the underlying data.
Do not download any competition data as part
of this exercise without approved permissions.

## Guided exercise 16 — explain every excluded model-evaluation day

Read [the origin audit section](M1_STAGED_ROLLING_BASELINES.md)
and `src/mirrormind/modules/forecasting/baselines.py`.
For January 29–February 4, predict the seven
nonvalue statuses before reading
`tests/unit/test_staged_rolling_baselines.py::
test_every_requested_origin_has_one_reproducible_nonvalue_audit_record`.
Then remove the final target row or shift its declared
publication past the cutoff. Explain how the
two outcomes differ and why even this precise
diagnostic cannot authenticate a real data source.

## Guided exercise 17 — age of data is not amount of history

Read [the updated staged baseline guide](M1_STAGED_ROLLING_BASELINES.md).
Construct an invented series with one ancient
date and seven recent pre-holdout dates. Predict
why `min_history_days=14` now rejects it even
though the first date is more than two weeks
before holdout. Inspect
`tests/unit/test_staged_rolling_baselines.py::
test_min_history_counts_observations_not_one_ancient_row`.
Lower the threshold to seven and explain why
publication-time abstention is still necessary.

## Guided exercise 18 — bound the read, not only the parser

Read the [bounded stream section](M1_LOCAL_CSV_STAGING.md)
and source `read_staged_csv`. Explain why
`Path.read_bytes()` on a large untrusted file
would allocate bytes **before** the existing
`stage_csv_snapshot` byte cap could reject it.
Read `tests/unit/test_evidence_snapshots.py::
test_partial_stream_reads_continue_until_eof_and_do_not_accept_prefix_hash`.
Change a mocked reader to return one byte at
a time, and verify the final digest still
covers the full input. Explain why this is
not permission to acquire an unauthorized
dataset or send it to an AI model.

## Guided exercise 19 — a CC license is necessary evidence, not a pipeline

Read [the UCI Online Retail source review](datasets/UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
and compare its original license link with
[the M5 candidate](datasets/M5_ACCESS_REVIEW.md).
Explain why CC BY 4.0 makes the source more
promising for reuse, yet does not waive
attribution, privacy or source-snapshot
integrity. From the UCI feature table, name
which transaction-level fields you would
exclude for a **product-day sales-only**
benchmark. Finally, identify why the
invoice transaction timestamp is not
a cryptographically verified historical
publication timestamp for as-of evaluation.

## Guided exercise 20 — a recorded zero is not an absent observation

Read the [staged quality method](M1_LOCAL_CSV_STAGING.md).
For the invented four-row CSV, predict
`calendar_gap_days`, `explicit_zero_unit_rows`
and `late_published_rows`. Then remove the
Jan 2 `item-A` row and explain why
the gap count changes while the explicit
Jan 3 zero remains. Inspect
`tests/unit/test_evidence_quality.py::
test_quality_report_distinguishes_explicit_zero_from_absent_day`.
Explain why missing internal dates cannot
prove lost customer demand, and why
a complete series needs independent
evidence of expected business operating days.

## Guided exercise 21 — transaction time cannot prove publication time (40 minutes)

Read [the retail projection method guide](UCI_RETAIL_PROJECTION.md)
and follow
`src/mirrormind/domains/retail/uci_transactions.py:
project_uci_retail_rows`.
For three fictional positive lines from the same
product/day plus a cancelled invoice and one
negative return, predict the aggregated positive
quantity and exclusion counts. Read
`tests/unit/test_uci_retail_projection.py::
test_customer_columns_are_not_accessed_or_serialized`
and explain what privacy boundaries the test
does **not** protect upstream.

Next, attempt to identify a trusted `available_on`
for a 2011 `InvoiceDate`. Why does it not exist?
What additional source release history, authorization,
deduplication policy and real-data signoff are required
before such data could be used for a historical
forecast or WorldKernel scenario?

## Guided exercise 22 — inspect a workbook without claiming source approval

Read the [UCI-shaped XLSX guide](UCI_WORKBOOK_READER.md)
and locate `_bounded_read`, `_check_zip_members`
and `read_uci_workbook`.
Explain why ZIP compressed and uncompressed
sizes require separate resource checks and
why even these do not make an arbitrary
malicious workbook safe.
Read `tests/unit/test_uci_workbook.py::
test_bounded_row_and_group_limits_do_not_truncate`.
Construct a two-row **fictional** workbook,
set `max_rows=1`, and explain why
a truncating "success" would be scientifically
misleading. What rights, source hash,
privacy review and publication-time
proof would a real source still need?

## Guided exercise — a checksum is not a data use grant (25 minutes)

Read [the source review packet guide](SOURCE_INTAKE_REVIEW.md),
[the metadata-only module](../../src/mirrormind/modules/evidence/intake_review.py)
and [its tests](../../tests/unit/test_source_intake_review.py).
Change one invented permission reference, keeping the same staged CSV
and snapshot SHA-256. Confirm the *manifest* fingerprint changes but
`ingestion_authorized` remains `false`. Explain why neither digest
is a license, why publication time must be established independently,
and which human source-card checks are still needed.

## Guided exercise — signatures, revocations and stale log replay (35 minutes)

Read [the signed-review guide](SIGNED_SOURCE_REVIEW.md) and
[the test-only signed events](../../tests/unit/test_signed_source_review.py).
Verify a fictional signed approval; then append a revocation and attempt
to resubmit the earlier, valid approval with the **new trusted head**.
Explain why the truncated chain must fail, why a self-supplied head and
public key would defeat that check, why the packet remains unauthorised,
and why signing is not evidence of publisher rights or retrospective vintages.

## Guided exercise — local CAS is not a durable approval registry (35 minutes)

Read the [review registry source](../../src/mirrormind/modules/evidence/local_review_registry.py),
[the trust boundary](LOCAL_REVIEW_REGISTRY.md) and
[its concurrency tests](../../tests/unit/test_local_review_registry.py).
Take two snapshots with the same version and head; attempt two
concurrent signed appends and observe one winning. Then start a new
registry object with the same public key and explain why it has no
memory of the previous revocation. Identify the missing transactional
store, authenticated reviewer identity and independently published
fresh head required before anyone relies on it for real permissions.

## Guided exercise — SQLite transactions and restored-history rollback (40 minutes)

Read the [transactional registry](../../src/mirrormind/modules/evidence/sqlite_review_registry.py),
[method guide](SQLITE_REVIEW_REGISTRY.md), and
[synthetic tests](../../tests/unit/test_sqlite_review_registry.py).
Follow the injected-abort test and explain why the event and updated
head must both disappear after rollback. Then restore a signed older
copy of the database and compare reads with and without the independently
retained later head. Explain why valid older signatures cannot themselves
prove freshness, reviewer rights, source permission or real ingestion.

## Guided exercise — signed history is not the latest history (35 minutes)

Review [the signed checkpoint verifier](../../src/mirrormind/modules/evidence/head_checkpoints.py),
[its trust guide](SIGNED_HEAD_CHECKPOINTS.md), and
[synthetic tests](../../tests/unit/test_head_checkpoints.py).
Restore a valid older SQLite review history with its older valid signed
checkpoint. Confirm a caller-provided stale sequence floor still accepts it,
then supply a newer trusted minimum and observe rejection. Explain what
independently governed signer keys, monotonic sequence, key rotation and
head publication the real system is missing before permissions can be used.

## Guided exercise — a witnessed chain is not a live authority (40 minutes)

Read [the witness transcript source](../../src/mirrormind/modules/evidence/authority_transcript.py),
[its trust model](AUTHORITY_TRANSCRIPT.md) and
[the synthetic key-handoff tests](../../tests/unit/test_authority_transcript.py).
Omit a witnessed checkpoint after a fictional outage, then supply only
the later receipt; observe a predecessor/sequence refusal. Try a key
change without both old and new signatures. Finally replay a complete
valid transcript using outdated start/end fences: explain why it can
still pass unless an independent authority publishes current fences
and exposes hidden conflicting forks.

## Guided exercise — a signed local operator is not an external authority (40 minutes)

Read the [local publisher source](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py),
[its trust guide](LOCAL_CHECKPOINT_PUBLISHER.md) and
[synthetic security tests](../../tests/unit/test_local_checkpoint_publisher.py).
Attempt publication with an unsigned operator command, reuse the same
signed proposal after a successful commit, then rotate the witness key
without old and new signatures. Restore a valid older SQLite backup
and explain why independently trusted new heads, authenticated roles,
key custody and witness consistency proofs are still necessary.

## Guided exercise — dual-admin signatures are not effective key revocation (40 minutes)

Read the [operator governance source](../../src/mirrormind/modules/evidence/operator_governance.py),
[governance guide](OPERATOR_GOVERNANCE.md), and
[synthetic tests](../../tests/unit/test_operator_governance.py).
Enroll and revoke a fictional operator with two admin signatures, then
attempt reenrollment with an old ID or reused public key. Reopen a
saved database from before the revocation and explain why the old
state is internally consistent. Identify the cross-database policy
admission race and independent current-head proof needed before
connecting this registry to the publisher.

## Guided exercise — atomic policy admission vs independent authority (40 minutes)

Read the [integrated gate](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py),
[the contract](ATOMIC_GOVERNED_PUBLISHER.md) and
[the race regressions](../../tests/unit/test_atomic_governed_publisher.py).
Enroll a fictional key, publish one checkpoint, sign a second one and
race revocation against publication. Explain why a publication committed
*before* revocation remains legitimate under SQLite's total local order,
while a later attempt fails. Restore a coherent pre-revocation combined
database and explain why external head custody, real identity and
legal source approvals remain necessary despite same-file atomicity.

## Guided exercise — current-state signatures versus actual freshness (35 minutes)

Read the [integrated head-fence verifier](../../src/mirrormind/modules/evidence/integrated_head_fence.py),
[trust guide](INTEGRATED_HEAD_FENCE.md) and
[generated-key regression cases](../../tests/unit/test_atomic_governed_publisher.py).
Copy a fictional combined DB before revocation; sign a fence on both
sides of the revocation. Verify that the old copy disagrees with the
newer supplied signed fence. Then provide the old fence and its old
expected digest, and explain why it can still match without genuine
independent latest-fence custody. Identify the TOCTOU risk of making
this read-only verifier a separate publication-admission precheck.

## Guided exercise — two witnesses do not prove global freshness (40 minutes)

Read the [dual-witness code](../../src/mirrormind/modules/evidence/integrated_fence_transcript.py)
and [threat-model guide](INTEGRATED_FENCE_TRANSCRIPT.md).
Using the synthetic fixtures in
[the combined publisher test suite](../../tests/unit/test_atomic_governed_publisher.py),
sign a two-link chain before and after a policy revocation. Demonstrate
that replacing one witness signature fails, both real competing
successors are **reported** as a supplied fork, and an old database plus
matching old trusted pins can still pass. Explain why a durable,
independently controlled and freshly queried current-head authority
is a different feature from multi-signature verification.

## Guided exercise — second file versus true independent authority (45 minutes)

Review the [registry code](../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py),
[operational trust guide](LOCAL_INTEGRATED_FENCE_REGISTRY.md)
and [synthetic regressions](../../tests/unit/test_atomic_governed_publisher.py).
Sign two successive dual-witness fences, reopen and replay a separate
SQLite journal, and test two concurrent attempts to append from the
same head. Restore only the publisher DB and observe head mismatch;
then restore **both** DBs and explain why a valid old prefix still
passes. Explain why independent hardware, key administration, external
latest pinning and a safe update protocol are distinct unimplemented
requirements, and why this journal is never a publication gate.

## Guided exercise — a fresh signature is not a true latest head (35 minutes)

Read the [challenged HTTPS client](../../src/mirrormind/modules/evidence/remote_fence_head_client.py),
[protocol/trust guide](REMOTE_FENCE_HEAD_CLIENT.md) and
[generated-key fake-response tests](../../tests/unit/test_atomic_governed_publisher.py).
Sign a reply containing a new random nonce and a 70-second UTC
validity window. Reuse that response against a second nonce and
observe refusal. Restore *both* local SQLite files after signing a
newer remote head; verify that a correct newer outside claim
disagrees with the old local registry. Then freshly sign the old
head with the new nonce and explain why a malicious remote signer
still passes. Identify what a genuinely independent deployed
authority and trusted key-custody process must add.

## Guided exercise — compose local retail evidence without granting permission (35 minutes)

Read [`evidence_flow.py`](../../src/mirrormind/domains/retail/evidence_flow.py),
the [M1 evidence-flow guide](M1_SYNTHETIC_EVIDENCE_FLOW.md), and
[`test_retail_evidence_flow.py`](../../tests/integration/test_retail_evidence_flow.py).
Trace the CSV fixture through digest verification, the metadata-only review
packet, quality summary and two-date as-of selection. Predict which rows are
present at January 3 and January 5, then move the origin before the first row
and verify the explicit abstention. Next inspect the generated XLSX test and
explain why each positive product-day needs a separate release declaration.
Remove one release and observe the fail-closed error. Finally compare the
typed result with `receipt()`: identify the fields retained for a later local
experiment, the fields omitted from receipts, and the still-false
`ingestion_authorized` and `forecast_eligible` flags. The exercise uses only
invented fixtures and does not establish a real source's rights or vintages.

## Guided exercise — trace a fixed-split retail evaluation (40 minutes)

Read [`evaluation_flow.py`](../../src/mirrormind/domains/retail/evaluation_flow.py),
the [M1 evidence-to-evaluation guide](M1_RETAIL_SYNTHETIC_EVALUATION.md),
the [synthetic fixture card](datasets/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md)
and the [baseline model card](model_cards/SYNTHETIC_RETAIL_RELEASE_EVALUATION.md).
Run the example CLI twice and compare the complete JSON. Before running the
integration test, predict why the seven targets produce two scored origins,
three unavailable-history statuses, one missing target and one unpublished
target. Mutate the final unavailable target and verify the digest changes
while metrics and origin receipts stay fixed. Then set all releases after the
cutoff and explain why no metrics or winner is returned. Finally explain why
the fixture's zero seasonal-naive MAE is not evidence of real predictive
skill, and list the publisher, calendar, holdout and uncertainty evidence
needed before an empirical claim.

## Guided exercise 14 — bind review to an exact result

Read the [decision trace result walkthrough](DECISION_TRACE_RESULT.md) and
[`DecisionTrace`](../../src/mirrormind/core/decision_trace.py). Run
`python -m pytest -q tests/unit/test_decision_trace.py`. Before changing the
fixture, predict which cross-reference validator runs and why an unavailable
cost cannot be encoded as zero. Compute `result_sha256`, create an approved
`HumanReview`, then change one forecast value without changing the digest and
predict the rejection. Explain why this proves local content binding but
does not authenticate a reviewer, data source or simulation.

## Guided exercise — trace chronology, canonical cost digests and resource bounds

Read [the result contract walkthrough](DECISION_TRACE_RESULT.md) and follow
`DecisionTrace.check_trace_references_and_cutoff` into the evidence-ID map and
review-time comparison. Run `tests/unit/test_decision_trace.py`, then inspect
`test_terminal_review_cannot_precede_trace_creation`,
`test_terminal_review_accepts_creation_boundary_and_equivalent_timezone`,
`test_result_digest_is_lossless_and_independent_of_decimal_context`, and the
collection-bound tests. Explain why a reviewer timestamp is compared as an
instant, why `Decimal.normalize()` can round under the active context, and why
the bounds on records/references do not enforce a transport request-size or
rate limit. Reproduce a same-length, valid-looking payload that stays below
every bound and identify which independent data-provenance checks are still
missing.
