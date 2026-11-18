# MM-M1A — Synthetic observation validation (bounded, non-public experiment)

## Goal and accepted scope

Introduce a **standalone** Python teaching utility for daily
nonnegative synthetic counts with an inclusive date cutoff
and deterministic diagnostics. This is a first executable
slice of M1, **not** actual dataset ingestion, model training,
forecasting, execution quotas, or a WorldKernel integration.

## Acceptance criteria

- [x] Explicit schema, nonblank labels, bounded bytes/rows and
  strict integer units (reject booleans and negative values).
- [x] Reject future dates, malformed dates, duplicate dates
  and duplicated JSON object keys; never silently impute gaps.
- [x] Summary includes date interval, observed row count,
  missing days and sum, labeled as synthetic and unverified.
- [x] CLI errors are generic, with no fixture contents/filename echoed.
- [x] Unit tests exercise normal and adverse behavior; subprocess
  tests check successful output and safe failures.
- [ ] Actual CI status is attached to the PR (check after validation).

## Impact map

| Layer | Change | Boundary |
| --- | --- | --- |
| Synthetic example | `examples/m1_observation_preflight.py` | Explicit command, **not** `src/mirrormind` production ingestion |
| Sample | `examples/synthetic-daily-sales.json` | Deliberately invented counts, no customer rights claims |
| HTTP capabilities | `api/routes/system.py:capabilities` | Only adds an `experimental` label; no new HTTP data endpoint |
| Tests | `tests/unit/test_m1_observation_preflight.py`, `tests/integration/test_m1_observation_preflight_cli.py` | Pure validation and subprocess examples, no third-party network |
| Documentation | `M1_DATA_PREFLIGHT.md`, atlas, status ledger, roadmap and security notes | Clearly separate input structure from truth/provenance |
| WorldKernel | **No change** | No reverse runtime dependency, no simulation adapter |

## Trust and reliability risks

Permission, license, source authenticity and temporal
availability are NOT verified. A value dated before cutoff
might still have been published or revised after cutoff.
The script requires no internet service and should never
be presented as an evaluated forecasting model. An
apparently valid dataset can be biased, incomplete or
synthetic. Inputs from actual customers require a separate
reviewed authorization and data minimization process.

## Reproduce

```bash
python examples/m1_observation_preflight.py examples/synthetic-daily-sales.json
python -m pytest -q tests/unit/test_m1_observation_preflight.py
python -m pytest -q tests/integration/test_m1_observation_preflight_cli.py
python scripts/docs/catalog.py --check
python scripts/docs/coverage.py --check
python scripts/docs/evidence.py --check
python scripts/docs/capabilities.py --check
```

The commands above are instructions. CI is the
authoritative result for this proposed PR; do not
claim all checks passed until those runs conclude.

## Independent explanation

The utility validates the calendar structure of a
small, explicitly synthetic series and reports gaps;
it does not fill missing rows, assert that a source
is authorized, use hidden future information, train
models, call agents or send work to WorldKernel.
