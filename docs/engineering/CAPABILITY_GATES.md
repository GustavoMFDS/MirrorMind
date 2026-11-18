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

At the initial baseline the status is `scaffold`.
The only publicly implemented claims are `health` and
`scenario_contract_validation`; the
`simulation_gateway_protocol` is `interface_only`
and must not appear in the implemented set. The new
`synthetic_observation_preflight` is a standalone
**experimental local fixture**, exposed under a separate
`experimental` list; it is not authorized ingestion,
forecasting or a production endpoint.

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

For forecasting: rolling temporal holdouts and a documented
baseline are necessary before making performance claims.
For retrieval: permission filtering, source lineage and
prompt-injection boundaries matter. For agents: denied tools,
explicit human approval and cost controls need adverse tests.
For simulations: valid WorldKernel contract mapping and bounded
execution do not imply causal or predictive accuracy.

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
If the system reports `worldkernel_adapter` as implemented
without a concrete adapter, the test should fail because
the ledger still classifies it as planned. If someone
changes the ledger alone to classify it as implemented,
the structural guard requires real source and a declared
test, but even then human review must verify that the
test exercises a real simulation.

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
