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

## Guided exercise — bind review to an exact result

Read the [decision trace result walkthrough](DECISION_TRACE_RESULT.md) and
[`DecisionTrace`](../../src/mirrormind/core/decision_trace.py). Run
`python -m pytest -q tests/unit/test_decision_trace.py`. Before changing the
fixture, predict which cross-reference validator runs and why an unavailable
cost cannot be encoded as zero. Compute `result_sha256`, create an approved
`HumanReview`, then change one forecast value without changing the digest and
predict the rejection. Explain why this proves local content binding but
does not authenticate a reviewer, data source or simulation.

## Guided exercise — inspect a strict external mapping (35 minutes)

Read the [WorldKernel mapping walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md),
then trace `build_worldkernel_exchange_request` through
`tests/unit/test_worldkernel_mapping.py::test_supported_inventory_scenario_maps_to_exact_v1_request`.
Predict the error for an unlisted world version, `lead_time_days`, a forecast
reference and an operator transition cap below `horizon_days * runs`. Then run
`test_mapping_revalidates_mutated_scenario_before_budget_mapping` and
`test_mapping_preserves_lower_scenario_or_operator_run_ceiling`: trace how a
mutable Pydantic object is revalidated and how the lower run ceiling is chosen.
Explain why the explicit unit object is still an assertion rather than
provenance, why the generated v1 limits are not an independently enforced
server quota, and why a deterministic request is not a simulation result.
Then trace the implemented M1E-02 worker boundary in the same walkthrough:
identify which budgets are enforced outside exchange v1 and which unsupported
budgets reject before process launch.

## Guided exercise — execute one pinned local simulation (40 minutes)

Read the [WorldKernel runtime gate](WORLDKERNEL_GATEWAY_GATE.md),
[`worldkernel_runner.py`](../../src/mirrormind/modules/simulation/worldkernel_runner.py),
[`worldkernel_worker.py`](../../src/mirrormind/modules/simulation/worldkernel_worker.py),
and [M1E-02 change request](changes/M1E_02_WORLDKERNEL_LOCAL_RUNTIME.md).
Install only the optional SHA-pinned extra, then run
`python -m examples.m1e_02_worldkernel_local_runner`. Explain how
`LocalWorldKernelGateway.execute` reaches the strict mapper, why the worker
checks PEP 610 package metadata separately from the `demo-1` world revision,
and how the parent rejects a malformed result before creating a summary.

Run `tests/unit/test_worldkernel_runner.py` and the actual-engine integration
test. Change a fake result's revision, unknown-field set, stdout size and
stderr size; predict the typed failure before running each test. Compare the
fake-worker tests with
`tests/integration/test_worldkernel_runner_engine.py::test_pinned_local_runner_executes_synthetic_inventory_world_deterministically`.
State why only the latter proves execution of the pinned engine. Finally list
what remains unproved: CPU/memory isolation, hostile-code safety, HTTP
execution, source rights, true demand, lead-time behavior, forecast quality
and production suitability.

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

## Guided exercise 16 — compare synthetic inventory policies (35 minutes)

Read the [M1 policy simulation walkthrough](M1_RETAIL_POLICY_SIMULATION.md),
[`policy_simulation.py`](../../src/mirrormind/domains/retail/policy_simulation.py),
and its [unit tests](../../tests/unit/test_retail_policy_simulation.py) and
[CLI integration tests](../../tests/integration/test_retail_policy_simulation_cli.py).
Run `python -m examples.m1_retail_policy_test_double` twice and compare the
JSON. Before inspecting metrics, predict how fixed-cycle, reorder-point and
profile-aware rules differ when lead time changes. Verify each replication's
demand digest matches across policy and sensitivity rows. Change one cost
coefficient and trace the affected total-cost components. Then explain why the
profile-aware rule and a lower synthetic cost establish neither a valid
forecast nor a realistic or optimal business policy. Set initial stock and
safety stock to zero with a one-day lead time, then inspect the positive
arrival-day profile value and the emitted `modeling_caveats`. Trace the case
through `test_one_day_zero_safety_stock_exclusion_is_exposed_as_caveat`, keep
`test_profile_aware_target_stops_before_arrival_day` intact, and run
`test_inventory_mass_balance_holds_for_every_policy_replication`. Explain why
the caveat documents this implementation boundary without establishing that
the rule is a conventional protection-period policy.

## Guided exercise 17 — keep uncertainty calibration labels disjoint (40 minutes)

Read [`evaluate_retail_residual_envelopes`](../../src/mirrormind/domains/retail/residual_envelope.py),
the [uncertainty walkthrough](RETAIL_RESIDUAL_ENVELOPE.md), the scoped
[M1D-01 change request](changes/M1D_01_DISJOINT_UNCERTAINTY_HOLDOUT.md), and
[`test_retail_residual_envelope.py`](../../tests/unit/test_retail_residual_envelope.py).
Start with `test_holdout_targets_never_enter_later_calibration_windows`:
draw the two date sets for a two-day holdout, then mark day 59 unavailable
until the second holdout origin. Predict whether the day-69 target may be
used as a day-70 calibration residual. Run the focused test and explain why
the answer is still no even though the earlier holdout result is now
published. Trace `release_events`, `_predict_on`, the active residual count
and the maximum-residual heap in the evaluator. Next inspect
`_naive_calibration_oracle` and the adversarial parameterized tests; explain
which implementation choices are independently recomputed and which remain
shared assumptions. Finally identify the exact numerator and denominator,
explain why their ratio is retrospective rather than nominal coverage, and
name the provenance and untouched-holdout evidence still required for a
scientific calibration claim. Reproduce with:

```bash
python -m pytest -q tests/unit/test_retail_residual_envelope.py
```

## Guided exercise — reconcile decision and workflow digest scopes

Read the [M1F-02 walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md),
[`synthetic_decision_workflow.py`](../../src/mirrormind/domains/retail/synthetic_decision_workflow.py)
and `tests/unit/test_synthetic_decision_workflow.py`. Run
`python -m examples.m1_retail_decision_workflow --as-of 2011-01-26 --replications 12 --seed 317`.
Before running, draw the diagnostic cutoff, historical holdout and last-seven
forecast window. Predict why `--as-of 2011-01-27` abstains when day 27 is late,
then follow `_eligible_observation_rows` to the release audit. On a successful
run, trace one `ForecastEstimate` from its seven facts to the nine conditional
outcomes. Change only the seed and confirm that the forecast remains fixed
while paired demand-stream digests change. Then run
`test_trace_identity_includes_replications_and_exact_replay_is_stable`, then
compare identical date/seed requests with different replication counts. Trace
the collision through `_decision_identity_sha256` and explain why the request
and versioned artifact digests both contribute to content identity. Run
`test_versioned_artifact_and_workflow_digests_bind_the_complete_response`;
change a nested simulation value in a copy and recompute the outer digest.
Distinguish that envelope digest from `DecisionTrace.result_sha256` and explain
why neither establishes producer identity, source provenance, a stored
revision history or human approval. Finally run
`test_profile_aware_policy_modeling_caveats_are_bound_into_trace` and trace the
arrival-day demand caveat to the affected outcome. Explain why an experimental
HTTP route with no authentication, body-size limit, rate limit or concurrency
control must not be exposed publicly even though its domain fields are
bounded.

## Guided exercise — inspect the WorldKernel policy world

Read the [M1E-04 policy-world walkthrough](WORLDKERNEL_POLICY_WORLD.md),
[`worldkernel_policy_world.py`](../../src/mirrormind/domains/retail/worldkernel_policy_world.py),
the [strict policy mapper](../../src/mirrormind/modules/simulation/worldkernel_policy_mapping.py),
and [`test_worldkernel_policy_world.py`](../../tests/unit/test_worldkernel_policy_world.py).
Run the focused commands in that guide and then run
`test_pinned_engine_policy_gateway_matches_synthetic_reference` with the exact
optional WorldKernel commit installed. Trace one WorldKernel event: prove
that the handler draws demand once, advances all three policies over each
lead-time case, and preserves the shared M1E-03 day transition. Deliberately
change the registered revision and one final inventory counter in fake-worker
fixtures; identify the exact parent validation that rejects each. Explain
why the in-process test double remains the parity oracle but its values are
not substituted for returned engine state. Finally inspect the API route and
verify that HTTP cannot inject this local comparator. A passing exact-engine
test still does not establish source rights, policy optimality, hostile-code
isolation, CPU/memory quotas or production safety.

## Guided exercise — trace the selected engine and parity evidence

Read the [v2 decision-trace contract](DECISION_TRACE_RESULT.md),
[M1F-03 change request](changes/M1F_03_ENGINE_EXECUTION_PROVENANCE.md),
[synthetic workflow walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md)
and [`test_worldkernel_policy_world_engine.py`](../../tests/integration/test_worldkernel_policy_world_engine.py).
Run the default command and then the explicit `--engine worldkernel` command
from the walkthrough. In each JSON result, explain the selected source,
`policy_test_double_invoked` and `policy_test_double_result_selected`. In the
engine run, follow each outcome's execution references to the selected-output
record and parity-oracle record. Confirm their contract references, equal
metric digests and the WorldKernel package, commit, world, revision, result
schema and raw worker digest in the selected provenance reference. Run
`test_trace_rejects_execution_evidence_from_a_different_engine_contract`,
`test_trace_rejects_dangling_execution_evidence_references`,
`test_trace_rejects_parity_evidence_with_a_different_selected_result_digest`
and the execution chronology tests. Set `produced_at` after, before and equal
to `created_at`; express equality with a second timezone offset. Explain why
only a later instant fails and why these logical timestamps do not authenticate
the machine clock.
Explain why the v1 example still validates as v1, why v2 records are separate
from historical input evidence and why exact parity against shared rules is
not independent scientific validation.

## Guided exercise — understand the UCI event-time boundary (35 minutes)

Read [`uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py),
the [event-time research guide](M1_UCI_EVENT_TIME_RESEARCH.md), the [synthetic
dataset card](datasets/SYNTHETIC_UCI_EVENT_TIME_CARD.md), the [model
card](model_cards/SYNTHETIC_UCI_EVENT_TIME.md), and
[`test_uci_event_time.py`](../../tests/unit/test_uci_event_time.py). Run the
generated CLI twice and compare JSON. Trace how fit dates freeze the product
cohort, then predict how a missing declared date affects target and history
abstentions. Change a product-day value on a declared complete date; contrast
the resulting zero assumption with removing that date from the coverage
declaration. Mutate a holdout value and verify validation metrics stay fixed.
Finally locate where `InvoiceDate` becomes an event day and explain why a
verified publication vintage requires a distinct source contract. Do not use
real UCI rows in this exercise.

## Guided exercise — evaluate aggregate Census vintages without lookahead

Read the [synthetic evaluation walkthrough](CENSUS_VINTAGE_EVALUATION.md),
[model card](model_cards/SYNTHETIC_CENSUS_VINTAGE_EVALUATION.md),
[aggregate-vintage protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md) and
[implementation](../../src/mirrormind/domains/retail/census_evaluation.py).
Run both CLI splits and the focused regressions:

    .\.venv\Scripts\python.exe -m examples.m1_census_vintage_evaluation --split validation
    .\.venv\Scripts\python.exe -m examples.m1_census_vintage_evaluation --split holdout
    .\.venv\Scripts\python.exe -m pytest -q tests/unit/test_census_vintage_evaluation.py tests/integration/test_census_vintage_evaluation_cli.py

Trace the December and January validation origins. For each, list the release
dates admitted by the strict issue cutoff, the 12 complete history months, the
lag-12 target and first-estimate label. Move a historical revision to the
second origin's issue date and predict why it leaves the history fingerprint
unchanged. Remove one month and identify the exact abstention count. Change a
target first-estimate value and explain why metrics change while the output
still omits that value and its forecast. Finally explain why a higher or lower
fictional error is not evidence about Census accuracy, source permission,
archive coverage or the proposed UCI product-level study.
Run `test_trailing_mean_and_metrics_ignore_ambient_decimal_context` under both
ROUND_DOWN and ROUND_UP and trace the `Decimal` to `Fraction` conversion.
Append a revision dated before its known first estimate, then on the same date;
identify the chronology error versus the date-only ambiguity error. Remove an
estimate but retain a later revision, compare `unanchored_revision_count`, the
full input hash and origin feature hashes, and explain why history remains
missing. Finally run the public WAPE overflow and positive-metric underflow
regressions; explain why they raise `ValueError` instead of serializing
infinity, NaN or zero. Then run
`test_representable_rmse_does_not_underflow_while_scaling_mean_square` and
trace how `_sqrt_metric_float` rescales an exact rational before taking its
square root. The explicit count changes the experimental result envelope to
schema v2.

## Guided exercise — select an aggregate vintage without lookahead

Read the [Census/ALFRED protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md),
[synthetic adapter walkthrough](CENSUS_VINTAGE_ADAPTER.md),
[fixture card](datasets/SYNTHETIC_CENSUS_VINTAGES.md) and
[`census_vintages.py`](../../src/mirrormind/domains/retail/census_vintages.py).
Run `python -m pytest -q tests/unit/test_census_vintages.py`. Draw the
reference month, first-estimate publication date, monthly revision date and
target-release cutoff for the first regression. Predict which `Decimal` is
selected, then move the revision to the cutoff date and explain why it is
excluded. Add two same-day records for one month; explain why input order
cannot safely break the tie. Remove one reference month and verify it remains
absent rather than becoming zero. Finally mutate a record's value without
changing its digest string and identify the missing byte-verification layer.
Explain why this normalized synthetic selector proves neither a real source
vintage nor permission, and why UCI `InvoiceDate` cannot supply
`published_on`.
Add an anchored revision dated before its first estimate and verify chronology
rejection; set both dates equal and explain why the date-only ambiguity guard
also rejects it.

### Regression extension — period-close lower bound

Move a first estimate's publication date into its reference month and run
`test_evaluator_rejects_first_estimates_published_before_reference_month_closes`.
Then move it to the first day of the following month and explain why the
normalized boundary still does not authenticate the official release date.

## Guided exercise — review a temporal source without acquiring its data

Read the [Census/ALFRED protocol](CENSUS_ALFRED_VINTAGE_PROTOCOL.md), the
[Census MARTS archive](https://www.census.gov/retail/marts/historic_releases.html),
the [annual revision archive](https://www.census.gov/retail/mrts/historic_releases.html),
the [current methodology](https://www.census.gov/retail/marts/how_surveys_are_collected.html),
the [release schedule](https://www.census.gov/retail/release_schedule.html),
and the [FRED Services terms](https://fred.stlouisfed.org/legal/terms/).
Without opening a release file or calling an API, identify which metadata proves
that an archive index exists and which evidence is still needed to prove each
month's first release, original bytes and local retention rights. Explain why
an API key does not grant the rights of a third-party series owner and why the
current Services terms apply to ALFRED and prohibit storage/cache/archive,
while API-specific terms also prohibit software/AI-development access and
API-associated storage. State why FRED/ALFRED is currently a NO-GO data route
for MirrorMind's reproducible development study unless written permission or
changed terms expressly cover these uses. Separate this conclusion from the
still-open rights review for direct Census artifacts.

Then add `methodology_edition` to a hypothetical source manifest. Trace the
documented April 2025 removal of nonemployers through the proposed time series:
state why publication-date eligibility alone cannot prove that values on both
sides have the same population definition, and design a fail-closed choice
between a reviewed comparability analysis, separate reporting by edition, or
abstention. Review the owner's proposed source package: original Census
MARTS files only, one verified national seasonally adjusted total, internal
research with attribution, access-controlled local storage, 30-day retention
of value-bearing artifacts and deletion, and no redistribution. Explain why
each item requires approval before acquisition. Keep the exercise metadata-
only; do not retrieve Census values, create an API key, or call the evaluation
an empirical pilot.

Finally, pre-register a chronological 60/20/20 development/validation/locked-
holdout split and the fixed 1/3/6-month baselines before looking at scores.
Explain why date-only publication values require strict-before selection,
why same-day correction metadata without orderable timestamps requires
abstention, and why fewer than 60 matched holdout origins per horizon supports
descriptive metrics only under the proposed 12-month moving-block bootstrap.
These are proposed acceptance criteria, not executed evidence.

## Guided exercise: fingerprint formatting and numeric replay

Read [the Census walkthrough](CENSUS_VINTAGE_EVALUATION.md), then compare
`str(Decimal("1.00E+20"))` with `format(Decimal("1.00E+20"), "G")`
under local Decimal contexts with capitals 0 and 1. Run
`test_scientific_notation_fingerprints_ignore_decimal_capitals` and
explain why exact Fraction arithmetic alone did not guarantee identical
normalized-input fingerprints. Inspect the stored uppercase-default digest;
no source-byte authenticity or empirical accuracy follows.

## Guided exercise — adjacent-date validation and safe lint changes

Read the [as-of rolling guide](M1_ASOF_ROLLING_EVALUATION.md),
`_require_contiguous_days` in
[`m1_asof_rolling_backtest.py`](../../examples/m1_asof_rolling_backtest.py),
and the tests `test_contiguous_day_guard_preserves_pairwise_boundary_semantics`,
`test_contiguous_day_guard_rejects_a_gap_without_imputing_a_day` and
`test_missing_event_day_not_imputed_even_with_publication_metadata`.
Predict the number of adjacent pairs for an empty list, one date, and three
dates. Compare that with `itertools.pairwise` and the former
`zip(days, days[1:])` expression. Explain why the Ruff RUF007 autofix is
marked unsafe in general, why it is equivalent for this sorted `list[date]`
input and Python 3.11 minimum, and why a missing day must raise instead of
being represented as zero demand. Re-run the three regressions and
`ruff check examples`; confirm imports and lint cleanup did not change any
forecast, output or authorization contract.

## Guided exercise — verify scope-first evidence retrieval (35 minutes)

Read the [M2 evidence retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md),
[`contracts.py`](../../src/mirrormind/modules/retrieval/contracts.py),
[`index.py`](../../src/mirrormind/modules/retrieval/index.py) and
[`fictional_fixture.py`](../../src/mirrormind/modules/retrieval/fictional_fixture.py).
Trace how `EvidenceAccessContext` filters documents before `_token_spans`
builds the index. Run
`python -m pytest -q tests/unit/test_evidence_retrieval.py` and predict what
the denied-record test would observe if tokenization moved before filtering.
For one result, verify that the cited Python string slice equals the excerpt
and recompute SHA-256 over its UTF-8 bytes. Run
`test_contract_rejects_same_length_excerpt_tampering` and
`test_contract_rejects_wrong_well_formed_excerpt_digest`; explain why the
contract detects excerpt/digest mismatch but cannot authenticate a source
when both values are replaced. Inspect the injection-like fixture and explain
why it remains `untrusted_evidence` without creating an instruction or tool
call. Finally change the fixed demo scope in a practice branch and explain why
this tests a local input boundary rather than identity or authorization.

## Guided exercise — sign a current-head challenge in process (35 minutes)

Read the [G-01 service walkthrough](REMOTE_FENCE_HEAD_SERVICE.md), the
[shared wire protocol](../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py),
the [responder](../../src/mirrormind/modules/evidence/remote_fence_head_service.py)
and
[`test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py).
Run all six `test_remote_head_service_*` selectors. Trace the request nonce
from the raw query into `SignedRemoteFenceHead`, the canonical signing
message and the existing client verifier. Change one query field and predict
whether the responder calls the store. Then reuse a protected public key as
the service signer and explain why initialization fails. Finally, list the
transport, durable storage and operational evidence that these tests do not
provide. Make a fake clock raise `RemoteFenceHeadClockError` and verify the
bodyless 503. Then make the clock and store raise `RuntimeError`; explain why
those programming failures propagate rather than being mislabeled as routine
service outages. Describe how a future HTTP adapter can map an unexpected
exception at its transport boundary without broad catches inside the typed
responder.


## Guided exercise — reject ambiguous worksheet cell payloads

Read the [bounded UCI workbook walkthrough](UCI_WORKBOOK_READER.md) and trace
`_iter_worksheet_rows` in [`uci_xlsx_xml.py`](../../src/mirrormind/domains/retail/uci_xlsx_xml.py).
The parser runs this iterator twice: first to discover only referenced shared
strings, then to decode selected values. Run
`test_duplicate_scalar_values_fail_in_both_worksheet_passes`,
`test_mixed_scalar_and_inline_payloads_fail_in_both_worksheet_passes`, and
`test_valid_inline_rich_text_runs_remain_one_stock_code` from
[`test_uci_workbook.py`](../../tests/unit/test_uci_workbook.py). Explain why
counting `<v>` structure matters even when the first pass does not capture
scalar text, why mixed `<v>` and `<is>` representations are ambiguous, and
why multiple ordered rich-text runs inside one valid `<is>` payload remain
supported. Verify that a failed cell produces a fixed redacted error and that
excluded `Description` text remains outside character callbacks. These
synthetic tests establish parser behavior only; they do not establish source
rights, private-workbook anomalies, archive completeness or hostile-file
isolation. Do not reread the private workbook or infer empirical quality.

## Guided exercise — conservatively classify UCI invoice prefixes

Trace `_normalize_uci_workbook_invoice` in
[`uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), then
run `test_uci_non_c_alpha_invoice_prefixes_are_counted_and_excluded` and
`test_all_single_ascii_letter_prefixes_have_one_aggregate_exclusion_class` in
[`test_uci_workbook.py`](../../tests/unit/test_uci_workbook.py). Explain why
only uppercase `C` plus six ASCII digits is a cancellation, why lowercase `c`
and other one-letter prefixes must not silently become sales, and why the
reader retains one aggregate unverified-prefix count instead of individual
IDs or per-prefix counts. Follow the excluded sentinel through
`_project_uci_retail_rows` and confirm that excluded rows bypass `StockCode`
normalization and product-day grouping. Then read
`test_synthetic_local_xlsx_file_to_product_day_projection` in
[`test_uci_workbook_flow.py`](../../tests/integration/test_uci_workbook_flow.py)
to verify that excluded quantities do not change category-day values.

Finally, explain how removing rows could change a fitted category cohort,
coverage denominators, zero-valued targets and forecast metrics. The approved
private UCI call exceeded its fixed 250,000-group budget before producing a
complete projection, so neither the full exclusion count nor those effects
were measured. These fixtures prove the classifier and aggregation boundary;
they do not prove full-source compatibility or empirical forecast quality.


## Exercise: inspect a local decision report

Follow the [report walkthrough](PORTFOLIO_DEMO.md), compare selected case metrics with original JSON and explain the difference between display selection and a new seeded workflow execution.

## Guided exercise — audit the bounded fictional retrieval evaluator (40 minutes)

Read the M2-02 section of the [retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md),
then trace `run_retrieval_evaluation` in
[`evaluation.py`](../../src/mirrormind/modules/retrieval/evaluation.py),
`InMemoryEvidenceIndex.build` and `search` in
[`index.py`](../../src/mirrormind/modules/retrieval/index.py), and the fixed
cases in [`fictional_fixture.py`](../../src/mirrormind/modules/retrieval/fictional_fixture.py).
Run `python -m pytest -q tests/unit/test_evidence_retrieval_evaluation.py`
and `python -m pytest -q tests/integration/test_m2_evidence_retrieval_evaluation_cli.py`.
For each case, hand-compute recall, relevant-query hit rate, correct
abstention, citation support and scope compliance from numerator and
denominator counts. Explain why a zero denominator is `null`, while
`abstention_rate` is always defined for a nonempty case set.

Inspect the out-of-scope and unknown-hit regressions. Follow how their IDs and
refs are replaced by aggregate counts, then explain why this redaction test
does not create authentication or prevent a caller from mislabeling real data
as a fictional fixture. Inspect the lineage and exact-span tests; identify
which source reference, code-point offsets and UTF-8 digest each check binds.
Run `python -m examples.m2_evidence_retrieval_evaluation` twice and compare
the stable query-free JSON. Finally, change a gold label to a visible but
irrelevant document and predict which metric numerators change. Do not infer
real-corpus quality, confidence calibration or production authorization from
the fixture's perfect scores.

## Guided exercise — trace a bounded scripted tool call (45 minutes)

Read the [M2-03 orchestration walkthrough](M2_TOOL_ORCHESTRATION.md), then
trace `AgentRunRequest` through `run_bounded_tool_orchestration`, the immutable
`ToolRegistry.invoke`, the existing fictional retriever and the M1F-02
decision adapter. Run
`tests/unit/test_bounded_tool_orchestration.py::test_injection_like_evidence_cannot_expand_the_tool_registry`
and
`tests/unit/test_bounded_tool_orchestration.py::test_unobserved_citation_is_refused_as_unsupported_evidence`.
Explain which boundary each regression proves and why neither proves that a
live model follows instructions or that a citation semantically entails a
summary. Then corrupt a valid `AgentDraft` and `AgentTurn` with
`model_copy(update=...)` and run
`test_provider_turn_revalidates_nested_draft_fields_before_consumption`,
`test_provider_turn_revalidates_nested_status_and_citation_invariants`,
`test_provider_turn_revalidates_nested_tool_call_before_dispatch`, and both
`test_provider_turn_with_missing_*_payload_fails_closed` tests. Explain why
dumping the exact model to plain Python data before strict reconstruction
re-runs field and model validators, and verify malformed tool calls are
refused before a tool attempt is counted. Then inspect the provider-mode
failure test, attempt to mutate the registry, and run
`python -m examples.m2_bounded_tool_orchestration` twice to compare query-free
receipts. Inspect the private `_SyntheticWorkflowResult`
`TypedDict` against the M1F-02 return construction. Explain why it assists
static checking but does not add runtime validation, and locate the Pydantic
checks that still define the runtime contract. The exercise uses fictional
inputs and establishes no identity, provider attestation, approval, network
isolation or action authority.

## Exercise: fixture reuse without temporal leakage

Run the synthetic workflow reuse regression and trace the two calls through
separate fresh BytesIO streams. Explain why shared immutable bytes do not
imply a shared release audit. Compare full result hashes at different cutoffs
and after a day-35 mutation; no real source is needed.

## Exercise: sparse BM25 frequency lookup

Trace the query terms through binary search of the sorted tuples, then
calculate inverse document frequency for one visible term. Explain why
filtering a query to one collection must not change corpus-wide IDF.
Run the bounded corpus regression and inspect complete result hashes; compare
a common term and an unknown term without inferring real-data quality.

For compact retrieval, explain why BM25 needs total token count rather
than distinct term count, and why the earliest source occurrence among
matched terms suffices for the unchanged excerpt window. Compare a
reversed query and a casefold-expanding word with the citation regression.

### Exercise: exact paired Census errors

Read [the descriptive walkthrough](CENSUS_VINTAGE_EVALUATION.md) and
`test_descriptive_receipt_exact_pairs_and_v2_compatibility`. Recompute
the 20 - 115/6 difference with Fraction, then remove the target label
and observe a missing row, not a zero error. Explain why a holdout label
and a report digest do not establish independent observations, locked
selection or calibrated confidence.

### Exercise: predeclared split boundaries
Use `test_frozen_split_binds_schedule_and_preserves_abstention` to
inspect the 6/2/2 partition. Move an earlier target publication to the
next split's issue date and observe rejection. Explain why a digest
comparison is not independent registration or a one-use holdout lock.

### Exercise: reproduce an experiment receipt
Read [the experiment walkthrough](CENSUS_VINTAGE_EVALUATION.md) and
`test_experiment_rejects_rehashed_forgery`. Modify one paired loss and
rehash the payload; compare its bytes to the actual replay. Explain why
a declared revision and caller-retained digest are not code attestation
or independent preregistration.

### Exercise: local replay and persistent metadata
Run `test_journal_external_digest_edit_requires_replay` and
`test_journal_abrupt_exit_and_recovery`. Explain why atomic persistence
and exact local replay do not establish independent custody or execution
attestation. See [Census evaluation guide](CENSUS_VINTAGE_EVALUATION.md).

### Exercise: complete fictional experiment
Use prepare then run with a caller-owned journal twice. Compare summary
and receipt hashes. Explain why a self-generated demo commitment is
not independent preregistration and lower descriptive MAE is not a
statistical winner.

### Exercise: inspect a fictional experiment
Generate the [local observatory](../../examples/m1_census_research_observatory.py)
twice to new paths. Compare file hashes, inspect horizon metrics and
receipt provenance. Explain why a reproducible report cannot establish
independent registration or statistical superiority.

### Exercise: descriptive comparison across fictional scenarios
Compare both baselines on the four fixed fixtures using the same horizon.
Explain the difference between zero error, unavailable metrics, scored-origin
coverage and inferential coverage. These designed scenarios are not
independent stochastic samples; no pooled statistical conclusion follows.

### Exercise: compare designed scenarios
Generate the all-scenarios observatory with both splits. Inspect metrics
by horizon, then each scenario's manifest and receipt. Explain why
identical schedules do not make these independent samples.

### Exercise: stored metadata versus replay
Run two fictional experiments in the same caller-owned journal. Generate
the [history report](../../examples/m1_census_research_history.py) before
and after explicitly replaying a stored split. Explain why a unique
commitment is not a count of executions or a timestamp.

### Exercise: one-factor sensitivity
Compare exact paired mean differences across the fixed trend, volatility
and shift grids. Explain why a sign change is descriptive, why levels
across axes are not comparable physical scales, and why this grid cannot
establish calibration or a universal model winner.

### Exercise: common-sample model comparison
Run the [five-model catalog](../../examples/m1_census_model_comparison.py).
Compare the two regime fixtures: only the added break occurs inside
validation. Explain why shared history and exact paired losses matter
and why deterministic comparisons do not establish statistical superiority.

### Exercise: exact discrete probability
Run the [probability tests](../../tests/unit/test_census_probability.py).
Compare CRPS computed by pairwise absolute differences and squared
CDF differences. Explain why inverse discrete quantiles can give
coverage above the nominal interval level, and why wide intervals
alone do not establish useful predictive uncertainty.

### Exercise: reproduce a probabilistic study
Use prepare and run in the [probability study](../../examples/m1_census_probability_study.py).
Compare coverage, width and CRPS for each group. Explain why oracle
knowledge is privileged and why exact replay is not statistical calibration.

### Exercise: inspect predictive distributions
Generate the [probabilistic observatory](../../examples/m1_census_probability_observatory.py).
Compare the fixed example PMFs, quantiles and realized displacement with
aggregate CRPS, coverage and width. Explain why a single example cannot
establish calibration and why the oracle is a privileged reference.

### Exercise: evaluate dependence
Run the [bivariate tests](../../tests/unit/test_census_bivariate.py).
Compare the independent projection with positive and negative joint
laws sharing both marginals. Explain why marginal scoring alone cannot
distinguish them and why joint Brier excess depends on the reference.

### Exercise: reproduce dependence estimates
Run the [bivariate study](../../examples/m1_census_bivariate_study.py).
Compare matched marginal CRPS, joint Brier and reference excess under
stable association, independence and a change in dependence. Discuss
why the oracle is privileged and why association is not causal effect.

### Exercise: inspect joint versus marginal predictions
Generate the [bivariate observatory](../../examples/m1_census_bivariate_observatory.py).
Compare joint matrices and the exact marginal tables of the matched
independent and joint methods. Equal marginals need not imply equal
joint events or covariance. No causal conclusion follows.
