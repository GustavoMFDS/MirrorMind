# Debugging and recovery playbook

This guide is a **method**, not an automated repair service.

## Evidence-first procedure
1. Define the observed symptom, expected behavior, runtime configuration and a safe reproducer. Preserve the failing input's schema, not private payloads or credentials.
2. Capture timestamp, version/commit, relevant feature flags, sanitized logs, a correlation/job ID if one exists, and stack trace.
3. Find the entrypoint in [SYSTEM_MAP](SYSTEM_MAP.md), then the symbol in the [generated catalog](generated/SYMBOLS.md). Follow callers, state mutations, contracts and related tests.
4. Generate competing root-cause hypotheses. Confirm or falsify with a focused test; never assume the AI-generated explanation is correct.
5. Fix the smallest relevant location, add a regression test for the observed failure, and run relevant broader tests.
6. Document the verified root cause, remediation, limitations, safe rollback and monitoring. Update the associated runbook in the PR.

## Incident note template
```text
Symptom:
Commit/version and environment:
How to reproduce (safe):
Observed / expected:
Relevant modules and stacktrace:
Evidence for root cause:
Mitigation / rollback:
Fix and regression test:
What is still unknown:
```

Never paste secrets, access tokens, user records, raw customer datasets or private prompt contents into agent context or public documentation.

## MirrorMind starting points
- Scenario-validation error: `api/routes/scenarios.py` → `core/contracts.py`; inspect `tests/unit/test_contracts.py`.
- Service/router mismatch: `api/app.py`, `api/routes/system.py`, `tests/integration/test_api.py`.
- Missing capability: check `GET /v1/capabilities` and [ROADMAP](../ROADMAP.md) before diagnosing a future feature as broken.
- Integrating WorldKernel: inspect `modules/simulation/gateway.py` and versioned contracts. An interface is not live execution.

## Decision trace validation or review-digest mismatch

Run the focused synthetic tests in
[`test_decision_trace.py`](../../tests/unit/test_decision_trace.py), then
follow the nested model and `DecisionTrace.check_trace_references_and_cutoff`
in [`decision_trace.py`](../../src/mirrormind/core/decision_trace.py). Check
record IDs and type-specific local references first, then timezone-aware
cutoff/availability fields, cost status and review digest. The references and
timestamps are caller assertions; do not log private payloads or infer source
rights, model execution, engine execution, reviewer identity or authorization
from a passing validation.
For a v2 execution-time error, compare every
`execution_evidence[].produced_at` with `created_at` as a timezone-aware
instant. A later instant fails; an equivalent offset for the same instant
passes. Generated timestamps are logical fixture metadata, not process
wall-clock evidence.
- For planned evidence/agents, design permission-bound provenance, error handling and budget limits before implementing.
- For the local M2-03 tool loop, inspect [`modules/agents/orchestrator.py`](../../src/mirrormind/modules/agents/orchestrator.py), [`registry.py`](../../src/mirrormind/modules/agents/registry.py), the [source walkthrough](M2_TOOL_ORCHESTRATION.md) and [`test_bounded_tool_orchestration.py`](../../tests/unit/test_bounded_tool_orchestration.py). A `provider_not_authorized` refusal means the self-declared local test-double mode was absent, malformed or could not be read; it is not a live-provider authentication decision. For `invalid_provider_turn`, run the `test_provider_turn_revalidates_*` and `test_provider_turn_with_missing_*_payload_fails_closed` selectors; inspect `_revalidate_provider_turn` to confirm the exact `AgentTurn` is dumped to plain data and reconstructed before `kind` or nested fields are consumed. `model_copy(update=...)` bypasses Pydantic validation, so an outer type check is insufficient. Keep the report fixed and query-free; do not log the invalid object or exception detail. For `tool_not_registered` or `tool_not_allowed`, compare the fixed registry names with the caller allowlist. For input/output failures, inspect only the strict model and fixed refusal code; never log arguments, excerpts or exception text. Citation membership proves only that the reference occurred in a prior retrieval result, not that the draft is supported.
- If package typing fails in M2-03, run `python -m mypy --warn-unused-ignores src/mirrormind` and compare `_SyntheticWorkflowResult` in `modules/agents/synthetic_tools.py` with the returned fields in `domains/retail/synthetic_decision_workflow.py`. The `TypedDict` is a static description only; runtime protection remains in `DecisionTraceV2`, the output Pydantic model and `ToolRegistry.invoke`. Keep those validators intact; annotations must not replace runtime validation.
- For fictional UCI-shaped retail projection failures: trace [`domains/retail/uci_transactions.py`](../../src/mirrormind/domains/retail/uci_transactions.py), [reviewed method guide](UCI_RETAIL_PROJECTION.md) and [unit regressions](../../tests/unit/test_uci_retail_projection.py). Do not copy customer IDs or invoice descriptions into bug reports.
- For bounded local XLSX input failures: inspect [`domains/retail/uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), [the workbook guide](UCI_WORKBOOK_READER.md) and [ZIP/schema tests](../../tests/unit/test_uci_workbook.py). Never paste original workbook bytes or customer fields in an issue.
- For event-time UCI evaluation failures: inspect [`domains/retail/uci_event_time.py`](../../src/mirrormind/domains/retail/uci_event_time.py), the [fixed-protocol walkthrough](M1_UCI_EVENT_TIME_RESEARCH.md), and [synthetic regressions](../../tests/unit/test_uci_event_time.py). Separate target-date coverage from seven-day history coverage; only synthetic declared-complete dates may justify a zero in the fixture. The result is never point-in-time evidence.
- For the approved UCI #352 local preflight: compare the sanitized [snapshot manifest](datasets/UCI_ONLINE_RETAIL_352_SNAPSHOT_MANIFEST.json) with [`uci_workbook.py`](../../src/mirrormind/domains/retail/uci_workbook.py), the [OOXML scanner](../../src/mirrormind/domains/retail/uci_xlsx_xml.py) and [reader regressions](../../tests/unit/test_uci_workbook.py). The corrected call stopped at `product-day group count exceeds local budget` above 250,000 groups; discard the incomplete in-memory projection. MM-024 confirms the current invoice classes but does not change the rows accepted or product-day group count from that attempt. Do not chunk, sample or raise the ceiling. For `invalid UCI workbook invoice number`, use synthetic fixtures only and report a redacted format class, never the identifier. Never log workbook cells, category keys, local paths or parser exceptions.
- Current invoice-policy diagnostic: MM-024 confirms exact six-digit IDs enter normal processing; only uppercase `C` plus six digits is cancellation; other one-letter ASCII prefixes use one aggregate unverified class. Reproduce the exclusion behavior with `tests/unit/test_uci_workbook.py::test_uci_non_c_alpha_invoice_prefixes_are_counted_and_excluded`; verify the full ASCII grammar and identifier-redaction boundary with `tests/unit/test_uci_workbook.py::test_all_single_ascii_letter_prefixes_have_one_aggregate_exclusion_class`. Check that excluded quantities do not enter category-day units in `tests/integration/test_uci_workbook_flow.py::test_synthetic_local_xlsx_file_to_product_day_projection`. Exclusions may affect the cohort, coverage denominators and scores, but the real attempt did not produce complete counts or metrics. Do not inspect the private workbook or report a source exclusion count.
- For duplicate OOXML cells or ambiguous values, use generated fixtures only. `test_duplicate_quantity_cell_is_rejected_instead_of_overwriting_original` covers repeated coordinates; `test_duplicate_scalar_value_does_not_overwrite_original_quantity` and `test_duplicate_scalar_values_fail_in_both_worksheet_passes` cover repeated `<v>` elements, including the shared-string index scan. `test_mixed_scalar_and_inline_payloads_fail_in_both_worksheet_passes` covers conflicting `<v>`/`<is>` forms for inline and shared-string cells; `test_valid_inline_rich_text_runs_remain_one_stock_code` is the compatibility control. Existing error/unknown-type and malformed-number tests cover decoding. Inspect `_iter_worksheet_rows` payload cardinality and capture state; the excluded Description callback must remain disabled. Errors intentionally omit workbook values; never dump source XML or cell contents into logs.
- For a point-in-time evaluation that selects a later source revision too early: compare `reference_month` with `published_at`, verify the immutable vintage manifest/hash, then check the official release schedule and the source review's ALFRED real-time boundary. Do not manufacture `available_on=InvoiceDate`; if a release timestamp or vintage is missing, abstain or exclude that origin.
- For synthetic Census vintage-selection failures: inspect [`census_vintages.py`](../../src/mirrormind/domains/retail/census_vintages.py), the [adapter walkthrough](CENSUS_VINTAGE_ADAPTER.md) and [`test_census_vintages.py`](../../tests/unit/test_census_vintages.py). Check strict `< target_release_on`, publication on or after the first day following `reference_month`, the `(reference_month, published_on)` ambiguity key and release-ID date/digest consistency. The period-close rule is only a lower bound; the adapter validates digest syntax but never verifies source bytes, the actual release schedule or rights.

- For missing or mismatched review packets: inspect [`modules/evidence/intake_review.py`](../../src/mirrormind/modules/evidence/intake_review.py), [the review guide](SOURCE_INTAKE_REVIEW.md) and [synthetic tests](../../tests/unit/test_source_intake_review.py). Share only sanitized refs/digests, never proof documents or raw rows in issues; references alone do not authorize use.

- For mismatched signed review chains: inspect [`review_decisions.py`](../../src/mirrormind/modules/evidence/review_decisions.py), [review security boundary](SIGNED_SOURCE_REVIEW.md) and [adversarial regressions](../../tests/unit/test_signed_source_review.py). Check key IDs, dates and independently anchored log heads without printing private keys, source IDs or reviewer evidence. A valid signature does not grant ingestion.

- For stale review writers in one process: inspect [`local_review_registry.py`](../../src/mirrormind/modules/evidence/local_review_registry.py), [the CAS limits](LOCAL_REVIEW_REGISTRY.md) and [concurrency tests](../../tests/unit/test_local_review_registry.py). Never assume a restart preserves the latest head, or infer permission from a local revision.

- For persistent review history failures: inspect [`sqlite_review_registry.py`](../../src/mirrormind/modules/evidence/sqlite_review_registry.py), [SQLite safety boundaries](SQLITE_REVIEW_REGISTRY.md) and [transaction regressions](../../tests/unit/test_sqlite_review_registry.py). Never expose raw SQLite databases containing review IDs; compare only sanitized revisions and independently provisioned heads. A correct local head is not an independent authority.

- If signed checkpoint verification refuses a restored SQLite database: inspect [`head_checkpoints.py`](../../src/mirrormind/modules/evidence/head_checkpoints.py), [checkpoint trust guide](SIGNED_HEAD_CHECKPOINTS.md) and [fictional replay tests](../../tests/unit/test_head_checkpoints.py). Do not use a checkpoint uploaded by the requester as a trusted freshness anchor, and never print private signing keys or source documents.

- For missing witness publications, rotation failures or stale head fences: inspect [`authority_transcript.py`](../../src/mirrormind/modules/evidence/authority_transcript.py), [witness protocol and limitations](AUTHORITY_TRANSCRIPT.md) and [fictional recovery tests](../../tests/unit/test_authority_transcript.py). Never assume a caller-supplied chain is current, or emit private key material/source IDs in issues.

- For publication CAS conflicts, missing operator role or local rollback: inspect [`local_checkpoint_publisher.py`](../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py), [the local publisher trust guide](LOCAL_CHECKPOINT_PUBLISHER.md) and [synthetic transactional tests](../../tests/unit/test_local_checkpoint_publisher.py). Never log private signing keys or copy a publisher SQLite database with metadata into issues. The journal cannot attest to its own globally current head.

- For operator policy enrollment or revocation incidents: inspect [`operator_governance.py`](../../src/mirrormind/modules/evidence/operator_governance.py), [its trust and TOCTOU limits](OPERATOR_GOVERNANCE.md) and [synthetic regressions](../../tests/unit/test_operator_governance.py). Do not mistake an active policy record for effective publisher authorization or log private key material; the databases are not atomically coupled.

- For the **integrated** publisher refusing an operator after a revocation or reporting stale policy heads: inspect [`atomic_governed_publisher.py`](../../src/mirrormind/modules/evidence/atomic_governed_publisher.py), [same-file transaction contract](ATOMIC_GOVERNED_PUBLISHER.md) and [concurrent revocation tests](../../tests/unit/test_atomic_governed_publisher.py). The legacy publisher intentionally refuses integrated files. Keep original source IDs and signed keys out of debug logs; local transactions do not prove external freshness.

Useful local checks:
```bash
python -m pytest -q
python -m ruff check src tests
```
Do not assert connectors, agents, forecasts or simulations are operational without implementation and tests.
## Supplied signed integrated-fence mismatch or rollback suspicion

Inspect [the fence contract](INTEGRATED_HEAD_FENCE.md), the
[verifier source](../../src/mirrormind/modules/evidence/integrated_head_fence.py)
and the [fictional rollback test](../../tests/unit/test_atomic_governed_publisher.py).
Record whether the separately pinned expected current sequence/digest
came from a genuinely independent trusted process. An old coherent
database may pass if those external values are stale. Never log
private signing keys, source-row payloads or customer identifiers.
A passing fence comparison cannot authorize a later publish.

## Dual-witness combined-fence continuity or conflict error

Follow the [transcript guide](INTEGRATED_FENCE_TRANSCRIPT.md)
and [generated-key fixture regressions](../../tests/unit/test_atomic_governed_publisher.py).
Check that anchor digest/sequence and exact expected latest digest
were obtained **separately** from the local publisher, that each link
signs the previous digest, and that both witness key IDs/public keys
are distinct from the authority key and each other. If two fully
signed same-predecessor successors conflict, preserve both original
records as evidence; do not silently choose a branch. Failure to
receive a competing record is **not** evidence that none exists.
Do not treat a successful offline chain check as live publication
admission or ingest permission.

## Separate signed-fence registry mismatch / disaster recovery

Use the [registry guide](LOCAL_INTEGRATED_FENCE_REGISTRY.md)
and [synthetic rollback tests](../../tests/unit/test_atomic_governed_publisher.py).
Check the identity marker (one packet and configured Ed25519 signing
rosters), signed event ordering, both witness signatures, CAS head and
actual publisher snapshot. Preserve original signed transition JSON
and both DB files for forensic comparison. If the governed DB alone
was restored, the intact separate journal can detect its older
policy/publication heads. If the registry was also restored or its
last valid event was removed, **do not claim** independent freshness.
Never repair by silently inserting unsigned records or granting
publish/ingestion permission. A publisher write may race a registry
comparison because there is no two-file transaction.

## Challenged HTTPS current-head read fails or remote signer disagrees

Inspect the [protocol and threat model](REMOTE_FENCE_HEAD_CLIENT.md)
and [generated-key/fake HTTPS regressions](../../tests/unit/test_atomic_governed_publisher.py).
Require an explicit trusted HTTPS domain with its fixed path;
validate outbound CA/hostname and firewall separately, without
disabling TLS checks or enabling redirects. A signed response must
echo **the current random request nonce**, the correct source-review
hash, the exact endpoint/service key and a 1–120-second UTC
validity interval. A remote/local sequence or digest mismatch is
not automatically evidence of attack: the remote service can be
ahead, behind, stale or falsely signing a head. Preserve minimal
hash evidence and verify each side with independent operators.
Never log signer private keys or source rows, retry with stale
pins, bypass on outage or use read receipt to authorize publishing.
No live authority is deployed in the project.

## Local retail evidence-flow failures

For a failed M1 composite preflight, reproduce with
[`tests/integration/test_retail_evidence_flow.py`](../../tests/integration/test_retail_evidence_flow.py)
and read the [flow contract](M1_SYNTHETIC_EVIDENCE_FLOW.md). Confirm the
caller-opened stream is binary and bounded, calculate its SHA-256 locally,
and compare it to both the expected digest and `SourceReviewDeclaration`.
Then isolate the format helper: CSV uses strict schema/two-date rules;
XLSX uses the optional workbook parser, caller calendar and explicit release
tuple. A missing CSV slice is a normal abstention. A workbook calendar gap or
missing release is invalid input, not evidence of zero sales. Do not dump raw
rows, references or workbook XML while diagnosing. Matching hashes and
synthetic release declarations never prove rights or real publisher
availability.

## Retail evidence evaluation abstains or rejects a cutoff

Reproduce the complete fictional path with
[`examples/m1_retail_synthetic_evaluation.py`](../../examples/m1_retail_synthetic_evaluation.py)
and the [evaluation guide](M1_RETAIL_SYNTHETIC_EVALUATION.md). If the
evaluator raises that the cutoff must match the evidence-flow audit, compare
`evaluation_on` with `flow.release_audit.origin_on`; rebuild the flow at the
intended cutoff rather than changing or inferring release dates. For a valid
abstention, inspect `origin_receipts` and distinguish
`target_missing_not_zero`, `target_unpublished_at_evaluation` and
`required_history_unavailable`. Never treat any of these as zero sales.
The evaluator reuses `backtest_declared_retail_releases`; inspect that
helper and its unit tests for product-day validation and seven-day history
rules. Do not log the typed projection or identifiers while debugging. A
stable fixture digest and matching cutoff still do not verify publisher
availability, source rights or demand completeness.

For a synthetic as-of backtest rejected for a calendar gap, inspect
`_require_contiguous_days` in
[`m1_asof_rolling_backtest.py`](../../examples/m1_asof_rolling_backtest.py).
It checks successive parsed dates with `itertools.pairwise`; missing dates
must keep producing `ValueError("missing event-date record; do not impute demand")`.
Run `python -m pytest -q tests/unit/test_m1_asof_rolling_backtest.py` and
compare the empty/singleton/consecutive helper cases with the public
`test_missing_event_day_not_imputed_even_with_publication_metadata` case.
Do not repair a fixture by filling an absent date with zero: zero is an
observed count, while a gap means no record. This synthetic check proves
calendar labels only, not source availability or authorization.

## WorldKernel request mapping rejects a retail scenario

Read the [mapping walkthrough](WORLDKERNEL_MAPPING_WALKTHROUGH.md) and
[`worldkernel_mapping.py`](../../src/mirrormind/modules/simulation/worldkernel_mapping.py).
Run `python -m pytest -q tests/unit/test_worldkernel_mapping.py`. Check the
exact `world_type`/`world_version` allowlist, explicit `item`/`day`/`order`
unit context, required starting stock and daily demand, and the separately
configured operator ceilings. Interventions and evidence/forecast references
are intentionally unsupported. The existing `examples/retail-scenario.json`
fails mapping because it has an intervention and omits daily demand; do not
add hidden defaults to make it pass. This module only constructs a request.
It does not verify remote package identity, run the simulation, enforce
`timeout_seconds`, model-call/output-token limits, worker quotas, wall-clock or
memory limits, or validate result payloads. A future adapter must enforce
budgets absent from exchange v1 or reject before execution.

## Retail residual diagnostic abstains for insufficient calibration

Inspect [`residual_envelope.py`](../../src/mirrormind/domains/retail/residual_envelope.py),
the [fixed split rules](RETAIL_RESIDUAL_ENVELOPE.md) and
[`test_retail_residual_envelope.py`](../../tests/unit/test_retail_residual_envelope.py).
Read `calibration_target_window_start/end` first: calibration labels are a
fixed interval immediately before `holdout_target_window_start`. At each
origin, a target in that interval contributes only after its declared release
is available and its own seven feature dates pass their own-origin checks.
Late releases, missing positive-line dates or unavailable feature history can
reduce the active residual count; a later holdout outcome cannot refill the
calibration interval. The correct response is an explicit abstention or a
reviewed change to the window/minimum settings, never zero imputation or
reusing holdout labels. Verify the exact `evaluated_origins` denominator and
keep `nominal_coverage` and `calibrated_prediction_interval` unset. The
synthetic diagnostic does not authenticate releases or establish empirical
coverage.

## Synthetic decision workflow abstains or a digest/identity is unexpected

Reproduce with
[`examples/m1_retail_decision_workflow.py`](../../examples/m1_retail_decision_workflow.py)
and follow the [M1F-02 walkthrough](M1_RETAIL_SYNTHETIC_DECISION_WORKFLOW.md).
Compare `as_of` with the historical `evaluation_cutoff` and the seven dates in
`forecast.history_start/history_end`. Inspect
`forecast_evidence_receipt.release_audit`; distinguish absent dates from
declared releases after the cutoff. An abstention must have no forecast, no
trace and no policy invocation, while retaining artifact digests and the
whole-response digest. Its decision identity is null because no trace exists.

On success, verify `trace_sha256` against the serialized M1F-01 trace, then
check `artifact_digests`, `decision_identity_sha256` and
`workflow_result_sha256` as separate scopes. The identity includes the
validated request and five versioned artifact digests, so changing only the
replication count must change the identity. The workflow digest includes the
trace and outer response fields and excludes only itself. Recompute it after a
copy is modified. The digests detect content changes but do not prove producer
identity, provenance or approval. Use
`test_trace_identity_includes_replications_and_exact_replay_is_stable` and
`test_versioned_artifact_and_workflow_digests_bind_the_complete_response` to
reproduce the reviewed cases.

For trace references, follow each forecast's seven `fact_refs` and each
outcome's forecast/assumption references. Check that profile-aware outcomes
carry the comparison's `modeling_caveats`, including the one-day lead-time
arrival-day demand exclusion. The HTTP route is experimental and has no
authentication, request body-size limit, rate limit or concurrency control;
do not expose it publicly. A digest is not a signature.

For an explicit WorldKernel run, check `simulation.selected_result_source`,
`simulation.policy_test_double_invoked` and
`simulation.policy_test_double_result_selected` independently. The expected
values are `worldkernel_policy_world`, `true` and `false`. In `trace`, find one
`selected_output` and one `parity_oracle` record. Every outcome must reference
both, name the selected engine contract and preserve equal result digests. The
selected record's provenance reference includes the package version, exact
source commit, registered world/revision, result schema and raw worker digest.
If these values disagree, reject the response and inspect the gateway metadata
before changing either engine.

## Synthetic retail policy comparison differs from its expected fixture

Reproduce with
[`examples/m1_retail_policy_test_double.py`](../../examples/m1_retail_policy_test_double.py)
and read the [M1 policy simulation walkthrough](M1_RETAIL_POLICY_SIMULATION.md).
Run `tests/unit/test_retail_policy_simulation.py` and
`tests/integration/test_retail_policy_simulation_cli.py`. Compare the request
seed and profile first, then verify that the per-replication demand digest is
identical across every policy and lead-time scenario. Trace day ordering in
`_simulate_replication`: due orders arrive at day start, demand is fulfilled,
holding cost is charged, and the policy places an order at day end. If a
one-day lead-time run with zero stock and safety stock orders zero despite a
positive arrival-day profile value, inspect the result's `modeling_caveats`
and `_order_quantity` interval `[day + 1, arrival_day)`. This is the current
toy convention; the output must not be described as a standard or optimized
order-up-to policy. Check `test_one_day_zero_safety_stock_exclusion_is_exposed_as_caveat`
and `test_inventory_mass_balance_holds_for_every_policy_replication` before
changing that behavior. A mismatch is a local deterministic behavior change,
not evidence about actual retail stock or costs. Never pass this result to the
WorldKernel mapper as if it were an engine receipt.

## WorldKernel policy-world execution fails or differs from the reference

Reproduce only with the generated fixture and explicit local opt-in:

```powershell
python -m examples.m1_retail_decision_workflow --as-of 2011-01-26 --replications 2 --seed 317 --engine worldkernel
python -m pytest -q tests/unit/test_worldkernel_policy_world.py tests/integration/test_worldkernel_policy_world_engine.py
```

Trace `LocalWorldKernelRetailPolicyGateway.compare` through the strict policy
mapper, fixed `worldkernel_worker.py`, `_validate_exchange_result_envelope`
and `_validate_policy_world_state`. Confirm the installed distribution's
`worldkernel` version, PEP 610 repository and commit; this checks declared
metadata, not installed-file integrity. A missing or mismatched package must
fail with a sanitized error, never fall back to the test double. For an
operator rejection, inspect the 28-day horizon, replication count and
fan-out-adjusted transition ceiling before looking at subprocess output.

For a seed mismatch, compare the WorldKernel run index rule `seed + run_index`
and verify that exactly one random demand draw is shared across all nine
policy/lead-time states each day. For an inventory mismatch, recompute the
state balance and verify every demand value against `_build_demand_streams`.
Then compare all returned policy metrics with the reference result. The
gateway rejects drift; do not patch the returned result from reference
values. Check `worldkernel_execution.result_sha256` only as a content digest,
not as a signature. Timeouts and output overflow remain local process limits,
not CPU/memory isolation. The API route is expected to use the test double
and must not launch this worker.

## API `test_health` hangs before application code

First record the exact interpreter, dependency versions, head, command and
whether the failure is a timeout or a stack-backed wait. Never increase the
test timeout, skip the health test or change application code based only on a
stalled test. In the 2026-11-25 restricted Windows execution, Python 3.13.5's
faulthandler stack stopped in `socket.accept` while AnyIO/Starlette created
the asyncio fallback self-pipe. This supports a loopback-socket restriction
in that execution context, not an application diagnosis and not a proven
cause for the older `8f906b8` timeout. PR #57's independent exact-head
checkout passed `test_health` and the complete local gate; preserve both
observations. Use the owner-approved exact-clean-head gate in an already
authorized local environment and report its full commit. Do not call a local
pass GitHub Actions success.

## Synthetic Census vintage evaluation abstains or rejects an origin

Inspect the normalized selector, the evaluation walkthrough and
tests/unit/test_census_vintage_evaluation.py. Check that each origin's own
first estimate was published before issued_on and on or after the first day
following its reference month; each target first estimate follows the issue
date, and all 12 consecutive reference months are present in the as-of view. A
publication dated inside its reference month is invalid chronology, even when
the issue cutoff would otherwise make it visible. The lower bound does not
verify an official release timestamp. A missing month is an abstention, never a zero. An unrelated
future reference month is a contract error; a target already published by
issue is not a future outcome. Compare the per-origin vintage fingerprint and
sanitized selector receipt before assuming a later revision affected a score.
If a revision precedes its known first-estimate date, expect chronology
rejection; a same-day collision is ambiguous at date-only precision. When the
first-estimate anchor is absent, inspect `unanchored_revision_count` and ensure
that row changes the full-input fingerprint but not the per-origin feature
fingerprint or missing-history abstention. To diagnose metric drift, rerun the
same records under Decimal precision 2 with `ROUND_DOWN` and `ROUND_UP`; exact
`Fraction` means/aggregates must be identical. For `ValueError` from metric
conversion, inspect the bounded coefficient/exponent domain and distinguish
WAPE overflow from positive-result float underflow. Do not replace either with
infinity, NaN or zero. If only the mean-square is below float range, inspect
`_sqrt_metric_float`: it scales the exact rational by a power of two before
converting the mantissa, so a representable RMSE remains available. The result
is schema v2 because it carries the explicit unanchored count.
The normalized-input fingerprint is not a publisher-byte digest, and no
diagnosis resolves source rights, archive completeness or empirical validity.

## Census metrics replay but lineage hashes differ

Check the exact normalized records, including Decimal scale and signed
zero. The evaluator uses explicit uppercase general formatting in
`_record_payload`; ambient Decimal capitals must not affect the v2 replay.
Run the scientific-notation fingerprint regression in
[the Census guide](CENSUS_VINTAGE_EVALUATION.md). Historical lowercase-context
hashes are superseded; do not silently rewrite stored receipts.

## Fictional evidence retrieval misses or returns an unexpected citation

Reproduce with [`examples/m2_evidence_retrieval.py`](../../examples/m2_evidence_retrieval.py)
and the [M2 retrieval walkthrough](M2_EVIDENCE_RETRIEVAL.md). For an empty
result, inspect query tokenization and the fixed collection/principal scope
before changing the ranker. For a scope regression, run
[`test_evidence_retrieval.py`](../../tests/unit/test_evidence_retrieval.py)
and verify filtering still precedes tokenization and score construction.
For a citation mismatch, compare the reported Python code-point slice and
recompute SHA-256 over its UTF-8 bytes. `RetrievedEvidence` rejects a changed
excerpt with the old digest and a different well-formed digest. Replacing both
excerpt and digest can still create a self-consistent untrusted envelope; the
digest is not source provenance. Never log denied IDs, hidden content or raw
queries. BM25 scores are ranking values, not relevance probabilities, and a
caller-declared scope is not authentication.

## In-process challenged-head responder returns an error

The experimental [G-01 responder walkthrough](REMOTE_FENCE_HEAD_SERVICE.md)
describes `RemoteFenceHeadResponder.respond`; it is not an HTTP route. For
400/405/406, inspect the method, fixed path, exact `Accept` value and raw
`nonce=...&packet_sha256=...` ordering in the generated request test. A 404
means no current record was found for the packet scope or the store returned
a different packet digest. A bodyless 503 means a typed store/clock
operational error, invalid record or invalid returned clock was observed.
Store adapters must translate expected unsafe/unavailable reads to
`RemoteFenceHeadStoreError`; clock adapters must translate expected time
service failures to `RemoteFenceHeadClockError`. Inspect sanitized adapter
diagnostics locally, never expose exception text or source rows in a response.
Unexpected programming exceptions propagate to the in-process caller. The
responder does not advance or repair state; use the generated-key round-trip
and adverse cases in
[`test_atomic_governed_publisher.py`](../../tests/unit/test_atomic_governed_publisher.py).
If the client rejects a 200 response, verify the configured service key,
request nonce, packet/snapshot digest and UTC validity against its existing
verifier. Do not infer an attack or independent freshness from a mismatch.

## Offline report fails to generate or render

Check the bounded workflow options and unused output path, then inspect the embedded M1 result and (when requested) M2 report. For a missing-history status, compare `trace` and `simulation.result` presence with the abstention object; `renderWorkflow` must take its fallback before any success-only access. Optional M2 preview rejects more than three replications; a tool failure is the fixed `tool_failed` refusal and omits raw exception detail. Reproduce both paths with `tests/integration/test_portfolio_demo.py::test_abstention_payload_and_renderer_guard_handle_missing_success_fields` and read the [report guide](PORTFOLIO_DEMO.md). Do not infer zeros, bypass the cutoff or overwrite earlier reports.

## Fictional retrieval evaluation reports a metric or citation mismatch

Reproduce with `python -m examples.m2_evidence_retrieval_evaluation` and
[`test_evidence_retrieval_evaluation.py`](../../tests/unit/test_evidence_retrieval_evaluation.py).
First check that the declared gold labels resolve inside both the case access
scope and query collection filter; a rejected label should produce a generic
error without echoing its ID. Compare `expected_relevant_document_count` with
`relevant_retrieved_document_count` before reading `recall_at_k`, then inspect
the query-level counts separately. For no-answer cases, distinguish a truly
empty retrieval from an unexpected visible hit; an empty gold set does not
make every returned result correct.

If citation support is lower than lineage match, compare the Python
code-point slice, excerpt string and UTF-8 SHA-256. If lineage match is low,
compare collection/source/snapshot refs with the visible fixture. Scope
violations include unknown or out-of-scope IDs and must appear only as
aggregate counts; the redaction regressions do not prove authentication. A
result containing more hits than `top_k` is a contract violation. Preserve the
unchanged `bm25_lexical_v1` ranking and use only generated fixtures. The report
contains verified refs but no query or excerpt; its fixed `fictional_fixture`
label is caller supplied, so it is not a control against passing private data.
Never paste private queries or user records into this evaluator or its logs.

## Synthetic workflow fixture performance

If timings regress, profile the fixture generator separately from the reader
and policy engine. The two cutoff audits must remain independent. Compare
complete output hashes before claiming a speedup; never reuse a parsed
release audit from a different cutoff or cache real-source bytes.

## Local BM25 search performance

Distinguish corpus construction from repeated searches on one immutable index.
Profile diverse and repeated synthetic vocabularies separately; compare full
result digests (scores, ties, excerpts and citations), not only hit counts.
The bounded corpus regression covers the previous implementation's output
without a timing threshold. Do not widen limits or expose denied documents.

When comparing compact-index memory, allocate the generated corpus before
starting tracemalloc and measure build separately from searches. Check
Unicode casefold and earliest-offset regressions before changing token
representation. Traced allocations are not total process RAM.
