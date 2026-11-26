# Capability truth ledger — enforce what MirrorMind actually delivers

MirrorMind is intended to support real decisions. Claims about
working capabilities are therefore **versioned implementation claims**,
not architectural aspirations.

Source of truth for the currently **reviewed status vocabulary**:
[`CAPABILITY_LEDGER.json`](CAPABILITY_LEDGER.json). The
`GET /v1/capabilities` route must match its
`implemented` and `planned` sets, and an API integration test
will fail if the two drift. The independent documentation checker
also verifies source files and top-level pytest references.

## 1. Terms and claim boundaries

| Status | Permitted meaning | Minimum evidence before promotion |
| --- | --- | --- |
| `planned` | Documented future functionality, **not executable** | Accepted scope and security/research requirements |
| `interface_only` | Python Protocol/type/schema may exist, **no concrete capability** | Inspect source; do not expose as implementation |
| `experimental` | A bounded, test-backed implementation on trusted/synthetic inputs | Tests for normal and failure paths, resource cap, explicit limitations and honest API signal |
| `implemented` | The named **narrow behavior** is actually available and tested | Specific source and tests, stable contract and truthful capability description; **not** automatically production-safe |
| `deferred` | Intentionally postponed | Document dependency and acceptance gate |

An implemented health endpoint means **process liveness**,
not a working forecast or decision engine. Implemented
scenario validation means checking a subset of shape and
cross-field constraints. It does **not** mean executing
WorldKernel, authorizing `EvidenceRef`, calculating
forecasts or enforcing runtime budgets.

At the scaffold baseline, the only implemented claims were `health` and
`scenario_contract_validation`. Current ledger status also includes
`worldkernel_adapter` as **experimental**: an optional exact-pin local process
can execute one registered synthetic demo. The
`simulation_gateway_protocol` remains `interface_only`; it must not appear in
the implemented set. `synthetic_observation_preflight` is likewise an
experimental local fixture, not authorized ingestion, forecasting or a
production endpoint.

## 2. Change gate for any future externally visible capability

1. **Authorization:** who may provide inputs and who may see
   results? Define tenant/permission boundaries **before**
   ingesting data or launching privileged tools.
2. **Provenance:** distinguish observed, forecast and
   simulated values, cite source and cutoff; never fabricate
   missing data or treat prompt content as privileged instructions.
3. **Contract:** declare schema/version, units, null/missing
   rules, retries and compatibility across components.
4. **Execution:** implement domain-neutral code with real
   resource budgets/timeouts and deny unsafe operations;
   don't confuse declared limits with metering.
5. **Evidence:** write independent normal, adverse and
   authorization tests. Name exact `tests/...::test_...`
   selectors and state what they **do not** validate.
6. **Review:** update the capability ledger, human guides,
   API `/v1/capabilities`, change request, system map,
   atlas and CI evidence. Review both scientific and security
   limitations. Only mark a capability implemented
   **at the scope that those tests establish**.

### Decision trace result schema is interface-only

[`DecisionTrace`](DECISION_TRACE_RESULT.md) is a strict local result shape
for later M1 components. Its synthetic tests prove internal references,
declared time rules and approval-digest consistency. The schema cannot verify
that an evidence, model-card or engine reference is real, permitted or
authenticated. `decision_evaluation` therefore remains `planned`, and the
schema is not listed by the HTTP capability route as executable behavior.

For forecasting: rolling temporal holdouts and a documented
baseline are necessary before making performance claims.
For retrieval: permission filtering, source lineage and
prompt-injection boundaries matter. For agents: denied tools,
explicit human approval and cost controls need adverse tests.
For simulations: valid WorldKernel contract mapping and bounded local process
execution do not imply causal or predictive accuracy, arbitrary-code
containment or a production service.

## 3. How the integrity checks differ

```bash
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
python -m pytest -q tests/unit/test_docs_capabilities.py
python -m pytest -q tests/integration/test_api.py
```

- The **catalog** lists declarations, not execution behavior.
- The **atlas** checks resolving links to tracked files.
- The **evidence map** checks reviewed claim IDs, guide/test
  selector existence and documented limitations.
- The **capability checker** validates the ledger vocabulary,
  code/test existence and nonempty caveats.
- The **API integration test** checks that implemented/planned
  lists match the ledger. It cannot measure security or
  research quality.

These commands are reproduction instructions, not claims
of local execution for this documentation-only change.
All new capabilities must keep these checks green
**and** pass their own behavioral acceptance tests.

## 4. Worked example and independent exercise

Follow
`src/mirrormind/api/routes/system.py:capabilities` and
`tests/integration/test_api.py::
test_live_api_claims_equal_reviewed_capability_ledger`.
The API and ledger currently report `worldkernel_adapter` as experimental.
The optional pinned local worker executes the upstream inventory demo and a
fixed MirrorMind-owned synthetic policy world. Changing the ledger alone to
implemented must fail review: these paths do not establish endpoint
execution, service authorization, hostile-code isolation, model validity or
production operation. Human review must distinguish actual engine tests from
fake-worker protocol tests.

**Independent exercise:** choose forecasting or evidence
retrieval. Draft an acceptance case for one small
*experimental* step, an adverse test, the required
provenance/cutoff fields, and what would remain unproved.
Do not claim live connectivity, private data access or
model accuracy from a passing schema test.

## Local synthetic temporal baseline is not production forecasting

The separate `synthetic_rolling_backtest` is now
`experimental` only; its [guide](M1_TEMPORAL_BACKTEST.md)
and [model card](model_cards/SYNTHETIC_WEEKLY_BASELINES.md)
explain why a perfect repeated-week result is not
held-out empirical proof. Do not promote `forecasting`
before authorized source ingestion, availability-time
checks, independently locked holdouts, measured
generalization and safe deployment have been validated.

## Declared as-of timestamps are not source permissions

The [synthetic availability preflight](M1_AVAILABILITY_PRECHECK.md)
demonstrates why an old `observed_on` date does not prove
the value was knowable: `available_on` can be later.
The guard's dates are entirely **caller declared**, with
no verification of publisher records or retention rights.
The capability is `experimental` only. Do not promote
`evidence_and_rag` or any real ingestion capability
without independently verified access grants and
source availability/revision evidence.

## Rolling evaluation needs origin-specific publication history

The synthetic [as-of rolling evaluation](M1_ASOF_ROLLING_EVALUATION.md)
abstains when an origin's full seven-day input window
was not yet published. It reports **4/7 coverage**,
rather than hiding three unavailable-origin cases
behind the MAE. Actual publication proof, realistic
evaluation and source authorization remain future
requirements. The script is `experimental` and
does not change `forecasting` or
`evidence_and_rag` to implemented.

## Offline staged baselines are not deployable forecasting

[`local_staged_rolling_baselines`](M1_STAGED_ROLLING_BASELINES.md)
now implements fixed source-level one-step comparisons over
strict staged local CSV observations and returns coverage,
metrics or explicit null when too few origins remain.
That **experimental** library cannot authenticate
publisher release times or acquire licensed data,
has no fitted model or calibrated intervals,
and exposes no production inference endpoint.
Do not promote the broader `forecasting` capability
without independently verified provenance,
empirical holdout review and authorization.

## UCI-shaped row projection is not authorized source ingestion

The new [retail-only projection](UCI_RETAIL_PROJECTION.md)
is explicitly `experimental` on **invented** input
mappings. It does not read the UCI workbook,
authenticate user rights, retain a reviewed source
snapshot, protect data upstream of its trusted
caller or establish historical publisher
publication dates. Output explicitly records
`publication_time_status=unknown_not_derived_from_invoice_date`
and has no `available_on` property.
Never promote `evidence_and_rag` or
`forecasting` from this output alone.

## Bounded XLSX parsing is not an approved source connector

`local_uci_xlsx_reader` is an **experimental,
opt-in, offline** reader tested with invented
UCI-shaped XLSX files. Compressed byte, ZIP
metadata and row/group caps are supported,
but the full official UCI workbook is not
accepted by its current 10k-row limit.
Neither an operator-supplied checksum nor
a published dataset license automatically
provides customer privacy signoff,
trusted source identity, safe hostile-file
isolation or historical publication vintages.
Do not promote `evidence_and_rag` or
`forecasting` to implemented from
a successful small workbook parse.
