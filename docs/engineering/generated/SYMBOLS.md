# Source symbol catalog (generated)

> GENERATED from Python AST. Do not edit manually. Source of truth: `src/`.
> This is a *static* declaration/import index, not a verified call graph,
> behavioral contract, runtime dependency graph or proof of correctness.

Generate: `python scripts/docs/catalog.py --write`.
Check: `python scripts/docs/catalog.py --check`.

## `mirrormind.__init__`

Source: [`src/mirrormind/__init__.py`](../../../src/mirrormind/__init__.py)

No top-level classes or functions.

## `mirrormind.api.__init__`

Source: [`src/mirrormind/api/__init__.py`](../../../src/mirrormind/api/__init__.py)

Static imports (including inside functions): `.app`

No top-level classes or functions.

## `mirrormind.api.app`

Source: [`src/mirrormind/api/app.py`](../../../src/mirrormind/api/app.py)

Static imports (including inside functions): `.routes`, `fastapi`

No top-level classes or functions.

## `mirrormind.api.routes.__init__`

Source: [`src/mirrormind/api/routes/__init__.py`](../../../src/mirrormind/api/routes/__init__.py)

No top-level classes or functions.

## `mirrormind.api.routes.scenarios`

Source: [`src/mirrormind/api/routes/scenarios.py`](../../../src/mirrormind/api/routes/scenarios.py)

Static imports (including inside functions): `...core.contracts`, `fastapi`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `validate_scenario` | function | `def validate_scenario(spec: ScenarioSpec) -> dict[str, object]` | — | [L10](../../../src/mirrormind/api/routes/scenarios.py#L10) |

## `mirrormind.api.routes.system`

Source: [`src/mirrormind/api/routes/system.py`](../../../src/mirrormind/api/routes/system.py)

Static imports (including inside functions): `fastapi`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `health` | function | `def health() -> dict[str, str]` | — | [L8](../../../src/mirrormind/api/routes/system.py#L8) |
| `capabilities` | function | `def capabilities() -> dict[str, object]` | — | [L13](../../../src/mirrormind/api/routes/system.py#L13) |

## `mirrormind.core.__init__`

Source: [`src/mirrormind/core/__init__.py`](../../../src/mirrormind/core/__init__.py)

No top-level classes or functions.

## `mirrormind.core.contracts`

Source: [`src/mirrormind/core/contracts.py`](../../../src/mirrormind/core/contracts.py)

Static imports (including inside functions): `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `EvidenceRef` | class | `class EvidenceRef` | — | [L7](../../../src/mirrormind/core/contracts.py#L7) |
| `ForecastRef` | class | `class ForecastRef` | — | [L14](../../../src/mirrormind/core/contracts.py#L14) |
| `Intervention` | class | `class Intervention` | — | [L20](../../../src/mirrormind/core/contracts.py#L20) |
| `ExecutionBudget` | class | `class ExecutionBudget` | — | [L25](../../../src/mirrormind/core/contracts.py#L25) |
| `ScenarioSpec` | class | `class ScenarioSpec` | — | [L32](../../../src/mirrormind/core/contracts.py#L32) |
| `ScenarioSpec.check_budget` | method | `def check_budget(self) -> 'ScenarioSpec'` | — | [L47](../../../src/mirrormind/core/contracts.py#L47) |

## `mirrormind.domains.__init__`

Source: [`src/mirrormind/domains/__init__.py`](../../../src/mirrormind/domains/__init__.py)

No top-level classes or functions.

## `mirrormind.domains.retail.__init__`

Source: [`src/mirrormind/domains/retail/__init__.py`](../../../src/mirrormind/domains/retail/__init__.py)

No top-level classes or functions.

## `mirrormind.domains.retail.calendar_coverage`

Source: [`src/mirrormind/domains/retail/calendar_coverage.py`](../../../src/mirrormind/domains/retail/calendar_coverage.py)

Static imports (including inside functions): `__future__`, `bisect`, `dataclasses`, `datetime`, `mirrormind.domains.retail.coverage`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `DeclaredCalendarCoverage` | class | `class DeclaredCalendarCoverage` | Aggregate scheduled internal gaps without product identifiers. | [L19](../../../src/mirrormind/domains/retail/calendar_coverage.py#L19) |
| `DeclaredCalendarCoverage.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | Keep the unverified calendar and unknown publisher availability explicit. | [L29](../../../src/mirrormind/domains/retail/calendar_coverage.py#L29) |
| `summarize_declared_calendar_coverage` | function | `def summarize_declared_calendar_coverage(projection: UciRetailProjection, declared_days: tuple[date, ...]) -> DeclaredCalendarCoverage` | Count only absent *declared* dates between observed positive product-days. | [L44](../../../src/mirrormind/domains/retail/calendar_coverage.py#L44) |

## `mirrormind.domains.retail.coverage`

Source: [`src/mirrormind/domains/retail/coverage.py`](../../../src/mirrormind/domains/retail/coverage.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailCoverageSummary` | class | `class RetailCoverageSummary` | Bounded, identifier-free coverage metadata for observed positive lines. | [L19](../../../src/mirrormind/domains/retail/coverage.py#L19) |
| `RetailCoverageSummary.receipt` | method | `def receipt(self) -> dict[str, str \| int \| None]` | Return aggregate values only, with an explicit source-trust caveat. | [L29](../../../src/mirrormind/domains/retail/coverage.py#L29) |
| `summarize_retail_coverage` | function | `def summarize_retail_coverage(projection: UciRetailProjection) -> RetailCoverageSummary` | Count gaps *between* observed positive product-days, without imputation. | [L47](../../../src/mirrormind/domains/retail/coverage.py#L47) |

## `mirrormind.domains.retail.coverage_gate`

Source: [`src/mirrormind/domains/retail/coverage_gate.py`](../../../src/mirrormind/domains/retail/coverage_gate.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.release_backtest`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailBacktestCoverageGate` | class | `class RetailBacktestCoverageGate` | Identifier-free summary: eligibility is not accuracy or calibration. | [L17](../../../src/mirrormind/domains/retail/coverage_gate.py#L17) |
| `RetailBacktestCoverageGate.receipt` | method | `def receipt(self) -> dict[str, str \| int \| None]` | Expose exact coverage fractions and never invent intervals. | [L29](../../../src/mirrormind/domains/retail/coverage_gate.py#L29) |
| `assess_retail_backtest_coverage` | function | `def assess_retail_backtest_coverage(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, holdout_days: int=7, minimum_coverage_percent: int=80) -> RetailBacktestCoverageGate` | Gate conditional model ranking by eligible-origin count and fraction. | [L49](../../../src/mirrormind/domains/retail/coverage_gate.py#L49) |

## `mirrormind.domains.retail.declared_releases`

Source: [`src/mirrormind/domains/retail/declared_releases.py`](../../../src/mirrormind/domains/retail/declared_releases.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.coverage`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `DeclaredProductRelease` | class | `class DeclaredProductRelease` | An explicitly asserted release day for one positive product/event day. | [L19](../../../src/mirrormind/domains/retail/declared_releases.py#L19) |
| `DeclaredRetailAsOfAudit` | class | `class DeclaredRetailAsOfAudit` | Identifier-free counts, not an authenticated historical evidence view. | [L28](../../../src/mirrormind/domains/retail/declared_releases.py#L28) |
| `DeclaredRetailAsOfAudit.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | No identifiers or source data; prominently mark asserted release dates. | [L38](../../../src/mirrormind/domains/retail/declared_releases.py#L38) |
| `audit_declared_releases_as_of` | function | `def audit_declared_releases_as_of(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, origin_on: date) -> DeclaredRetailAsOfAudit` | Account for every positive product-day without inferring availability. | [L52](../../../src/mirrormind/domains/retail/declared_releases.py#L52) |

## `mirrormind.domains.retail.eligibility_drift`

Source: [`src/mirrormind/domains/retail/eligibility_drift.py`](../../../src/mirrormind/domains/retail/eligibility_drift.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.residual_envelope`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailEligibilityDrift` | class | `class RetailEligibilityDrift` | Two disjoint retrospective eligibility windows with honest denominators. | [L19](../../../src/mirrormind/domains/retail/eligibility_drift.py#L19) |
| `RetailEligibilityDrift.receipt` | method | `def receipt(self) -> dict[str, str \| int \| None]` | Expose aggregate eligibility changes only, never performance or identities. | [L35](../../../src/mirrormind/domains/retail/eligibility_drift.py#L35) |
| `audit_retail_eligibility_drift` | function | `def audit_retail_eligibility_drift(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5) -> RetailEligibilityDrift` | Compare independent adjacent windows at THEIR OWN evaluation cutoffs. | [L59](../../../src/mirrormind/domains/retail/eligibility_drift.py#L59) |

## `mirrormind.domains.retail.eligible_values`

Source: [`src/mirrormind/domains/retail/eligible_values.py`](../../../src/mirrormind/domains/retail/eligible_values.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.residual_envelope`, `mirrormind.domains.retail.uci_transactions`, `statistics`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `EligibleRetailValueComparison` | class | `class EligibleRetailValueComparison` | Aggregate values conditional on separate retrospective eligibility. | [L19](../../../src/mirrormind/domains/retail/eligible_values.py#L19) |
| `EligibleRetailValueComparison.receipt` | method | `def receipt(self) -> dict[str, str \| int \| float \| None]` | Expose exact eligibility fractions and only conditional statistics. | [L43](../../../src/mirrormind/domains/retail/eligible_values.py#L43) |
| `compare_eligible_retail_values` | function | `def compare_eligible_retail_values(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5, minimum_eligible_per_window: int=3, minimum_coverage_percent: int=80) -> EligibleRetailValueComparison` | Compare two disjoint eligible subsets; refuse sparse comparisons. | [L74](../../../src/mirrormind/domains/retail/eligible_values.py#L74) |

## `mirrormind.domains.retail.release_backtest`

Source: [`src/mirrormind/domains/retail/release_backtest.py`](../../../src/mirrormind/domains/retail/release_backtest.py)

Static imports (including inside functions): `__future__`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.modules.forecasting.baselines`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `backtest_declared_retail_releases` | function | `def backtest_declared_retail_releases(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, holdout_days: int=7) -> dict[str, object]` | Compare two fixed one-day baselines on matched, eligible fictional days. | [L19](../../../src/mirrormind/domains/retail/release_backtest.py#L19) |

## `mirrormind.domains.retail.residual_envelope`

Source: [`src/mirrormind/domains/retail/residual_envelope.py`](../../../src/mirrormind/domains/retail/residual_envelope.py)

Static imports (including inside functions): `__future__`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.modules.forecasting.baselines`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `evaluate_retail_residual_envelopes` | function | `def evaluate_retail_residual_envelopes(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, holdout_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5) -> dict[str, object]` | Audit one-day seasonal-naive envelopes using only past published errors. | [L19](../../../src/mirrormind/domains/retail/residual_envelope.py#L19) |

## `mirrormind.domains.retail.selection_sensitivity`

Source: [`src/mirrormind/domains/retail/selection_sensitivity.py`](../../../src/mirrormind/domains/retail/selection_sensitivity.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.residual_envelope`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `ExcludedTargetSensitivity` | class | `class ExcludedTargetSensitivity` | Two-window counterfactual mean bounds with eligibility denominators. | [L17](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L17) |
| `ExcludedTargetSensitivity.receipt` | method | `def receipt(self) -> dict[str, str \| int \| float \| None]` | Report counterfactual bounds without any excluded target values. | [L33](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L33) |
| `assess_excluded_target_sensitivity` | function | `def assess_excluded_target_sensitivity(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, excluded_value_ceiling: int, window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5) -> ExcludedTargetSensitivity` | Vary hypothetical excluded day values, preserving each window cutoff. | [L58](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L58) |

## `mirrormind.domains.retail.sensitivity_sweep`

Source: [`src/mirrormind/domains/retail/sensitivity_sweep.py`](../../../src/mirrormind/domains/retail/sensitivity_sweep.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `itertools`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.selection_sensitivity`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailSensitivitySweep` | class | `class RetailSensitivitySweep` | An ordered, bounded list of hypothetical scenario results. | [L21](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L21) |
| `RetailSensitivitySweep.receipt` | method | `def receipt(self) -> dict[str, object]` | Show scenario receipts but never selected source identifiers. | [L26](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L26) |
| `sweep_excluded_target_sensitivity` | function | `def sweep_excluded_target_sensitivity(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, ceilings: tuple[int, ...], window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5) -> RetailSensitivitySweep` | Compare two to eight strictly increasing, hypothetical ceilings. | [L39](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L39) |

## `mirrormind.domains.retail.uci_transactions`

Source: [`src/mirrormind/domains/retail/uci_transactions.py`](../../../src/mirrormind/domains/retail/uci_transactions.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `ProductDayUnits` | class | `class ProductDayUnits` | Positive invoice-line units for a product/event day, not latent demand. | [L22](../../../src/mirrormind/domains/retail/uci_transactions.py#L22) |
| `UciRetailProjection` | class | `class UciRetailProjection` | Immutable local research projection with no authenticated data rights. | [L31](../../../src/mirrormind/domains/retail/uci_transactions.py#L31) |
| `UciRetailProjection.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | Return only aggregate counters and explicit permission/time uncertainty. | [L41](../../../src/mirrormind/domains/retail/uci_transactions.py#L41) |
| `_invoice_number` | function | `def _invoice_number(value: object) -> str` | Normalize an invoice code, preserving explicit C-prefixed cancellations. | [L55](../../../src/mirrormind/domains/retail/uci_transactions.py#L55) |
| `_transaction_day` | function | `def _transaction_day(value: object) -> date` | Accept only timezone-naive Excel-style datetimes as event observations. | [L64](../../../src/mirrormind/domains/retail/uci_transactions.py#L64) |
| `project_uci_retail_rows` | function | `def project_uci_retail_rows(rows: Iterable[Mapping[str, object]], *, max_rows: int=MAX_ROWS, max_groups: int=MAX_GROUPS) -> UciRetailProjection` | Summarize strictly positive invoice quantities, never source availability. | [L71](../../../src/mirrormind/domains/retail/uci_transactions.py#L71) |

## `mirrormind.domains.retail.uci_workbook`

Source: [`src/mirrormind/domains/retail/uci_workbook.py`](../../../src/mirrormind/domains/retail/uci_workbook.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `hashlib`, `hmac`, `io`, `mirrormind.domains.retail.uci_transactions`, `openpyxl`, `re`, `typing`, `zipfile`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `UciWorkbookReadResult` | class | `class UciWorkbookReadResult` | Local digest-coupled product-day projection without source approval. | [L41](../../../src/mirrormind/domains/retail/uci_workbook.py#L41) |
| `UciWorkbookReadResult.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | Summarize input identity and exclusions, not raw customer or invoice data. | [L47](../../../src/mirrormind/domains/retail/uci_workbook.py#L47) |
| `_bounded_read` | function | `def _bounded_read(stream: BinaryIO) -> bytes` | Consume at most one sentinel byte over the compressed workbook limit. | [L56](../../../src/mirrormind/domains/retail/uci_workbook.py#L56) |
| `_check_zip_members` | function | `def _check_zip_members(raw: bytes) -> None` | Reject excessive/active archive entries before workbook XML processing. | [L81](../../../src/mirrormind/domains/retail/uci_workbook.py#L81) |
| `read_uci_workbook` | function | `def read_uci_workbook(stream: BinaryIO, *, expected_sha256: str, sheet_name: str='Online Retail', max_rows: int=MAX_ROWS, max_groups: int=MAX_GROUPS) -> UciWorkbookReadResult` | Project a small, already-authorized local workbook through strict UCI schema. | [L112](../../../src/mirrormind/domains/retail/uci_workbook.py#L112) |

## `mirrormind.modules.__init__`

Source: [`src/mirrormind/modules/__init__.py`](../../../src/mirrormind/modules/__init__.py)

No top-level classes or functions.

## `mirrormind.modules.evidence.__init__`

Source: [`src/mirrormind/modules/evidence/__init__.py`](../../../src/mirrormind/modules/evidence/__init__.py)

No top-level classes or functions.

## `mirrormind.modules.evidence.snapshots`

Source: [`src/mirrormind/modules/evidence/snapshots.py`](../../../src/mirrormind/modules/evidence/snapshots.py)

Static imports (including inside functions): `__future__`, `csv`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `io`, `re`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `Observation` | class | `class Observation` | One structurally checked row; its publisher and meaning remain unverified. | [L25](../../../src/mirrormind/modules/evidence/snapshots.py#L25) |
| `StagedSnapshot` | class | `class StagedSnapshot` | In-memory immutable receipt with observations, NOT an authorized dataset. | [L35](../../../src/mirrormind/modules/evidence/snapshots.py#L35) |
| `StagedSnapshot.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | Report structure and digest only, without returning raw observations. | [L41](../../../src/mirrormind/modules/evidence/snapshots.py#L41) |
| `_day` | function | `def _day(text: str) -> date` | Accept only canonical ISO calendar dates, never ambiguous local timestamps. | [L51](../../../src/mirrormind/modules/evidence/snapshots.py#L51) |
| `stage_csv_snapshot` | function | `def stage_csv_snapshot(data: bytes, *, expected_sha256: str, max_rows: int=MAX_ROWS) -> StagedSnapshot` | Verify declared bytes, then reject malformed/ambiguous daily CSV rows. | [L64](../../../src/mirrormind/modules/evidence/snapshots.py#L64) |
| `available_as_of` | function | `def available_as_of(snapshot: StagedSnapshot, *, series_id: str, origin_on: str) -> tuple[Observation, ...]` | Select only dates and values published by this *historical* origin. | [L128](../../../src/mirrormind/modules/evidence/snapshots.py#L128) |
| `read_staged_csv` | function | `def read_staged_csv(stream: BinaryIO, *, expected_sha256: str, max_rows: int=MAX_ROWS) -> StagedSnapshot` | Read a cooperative local binary stream with a strict byte ceiling. | [L153](../../../src/mirrormind/modules/evidence/snapshots.py#L153) |
| `snapshot_quality_summary` | function | `def snapshot_quality_summary(snapshot: StagedSnapshot) -> dict[str, str \| int]` | Summarize observed calendar gaps and delays without imputing or authorizing. | [L188](../../../src/mirrormind/modules/evidence/snapshots.py#L188) |

## `mirrormind.modules.forecasting.__init__`

Source: [`src/mirrormind/modules/forecasting/__init__.py`](../../../src/mirrormind/modules/forecasting/__init__.py)

No top-level classes or functions.

## `mirrormind.modules.forecasting.baselines`

Source: [`src/mirrormind/modules/forecasting/baselines.py`](../../../src/mirrormind/modules/forecasting/baselines.py)

Static imports (including inside functions): `__future__`, `datetime`, `math`, `mirrormind.modules.evidence.snapshots`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_day` | function | `def _day(value: str) -> date` | Require exact, unambiguous ISO calendar days for evaluation cutoffs. | [L17](../../../src/mirrormind/modules/forecasting/baselines.py#L17) |
| `_predict` | function | `def _predict(seven: tuple[int, ...]) -> dict[str, float]` | Return fixed one-day estimates from exactly seven prior daily values. | [L30](../../../src/mirrormind/modules/forecasting/baselines.py#L30) |
| `_score` | function | `def _score(forecasts: tuple[float, ...], actuals: tuple[int, ...]) -> dict[str, float \| None]` | Return matched MAE/RMSE/signed bias and undefined-zero WAPE as None. | [L40](../../../src/mirrormind/modules/forecasting/baselines.py#L40) |
| `backtest_staged_snapshot` | function | `def backtest_staged_snapshot(snapshot: StagedSnapshot, *, series_id: str, evaluation_on: str, holdout_days: int=7, min_history_days: int=14) -> dict[str, object]` | Evaluate fixed daily origins only with data published before each origin. | [L55](../../../src/mirrormind/modules/forecasting/baselines.py#L55) |

## `mirrormind.modules.simulation.__init__`

Source: [`src/mirrormind/modules/simulation/__init__.py`](../../../src/mirrormind/modules/simulation/__init__.py)

No top-level classes or functions.

## `mirrormind.modules.simulation.gateway`

Source: [`src/mirrormind/modules/simulation/gateway.py`](../../../src/mirrormind/modules/simulation/gateway.py)

Static imports (including inside functions): `...core.contracts`, `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SimulationSummary` | class | `class SimulationSummary` | — | [L9](../../../src/mirrormind/modules/simulation/gateway.py#L9) |
| `SimulationGateway` | class | `class SimulationGateway` | — | [L17](../../../src/mirrormind/modules/simulation/gateway.py#L17) |
| `SimulationGateway.execute` | method | `def execute(self, scenario: ScenarioSpec) -> SimulationSummary` | Run an approved scenario using a separately configured engine. | [L18](../../../src/mirrormind/modules/simulation/gateway.py#L18) |
