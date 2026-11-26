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
