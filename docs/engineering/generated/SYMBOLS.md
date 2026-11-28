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

Static imports (including inside functions): `.routes`, `fastapi`, `mirrormind`

No top-level classes or functions.

## `mirrormind.api.routes.__init__`

Source: [`src/mirrormind/api/routes/__init__.py`](../../../src/mirrormind/api/routes/__init__.py)

No top-level classes or functions.

## `mirrormind.api.routes.decisions`

Source: [`src/mirrormind/api/routes/decisions.py`](../../../src/mirrormind/api/routes/decisions.py)

Static imports (including inside functions): `...domains.retail.synthetic_decision_workflow`, `fastapi`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `compare_synthetic_retail_decisions` | function | `def compare_synthetic_retail_decisions(request: SyntheticDecisionWorkflowRequest) -> dict[str, object]` | Return a deterministic fictional comparison without writes or engine I/O. | [L13](../../../src/mirrormind/api/routes/decisions.py#L13) |

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

## `mirrormind.core.decision_trace`

Source: [`src/mirrormind/core/decision_trace.py`](../../../src/mirrormind/core/decision_trace.py)

Static imports (including inside functions): `datetime`, `decimal`, `hashlib`, `json`, `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_TraceModel` | class | `class _TraceModel` | — | [L48](../../../src/mirrormind/core/decision_trace.py#L48) |
| `_require_timezone` | function | `def _require_timezone(value: datetime) -> datetime` | — | [L52](../../../src/mirrormind/core/decision_trace.py#L52) |
| `_require_optional_timezone` | function | `def _require_optional_timezone(value: datetime \| None) -> datetime \| None` | — | [L58](../../../src/mirrormind/core/decision_trace.py#L58) |
| `_canonical_decimal` | function | `def _canonical_decimal(value: Decimal) -> str` | Format a finite Decimal without consulting or rounding through context. | [L62](../../../src/mirrormind/core/decision_trace.py#L62) |
| `EvidenceReference` | class | `class EvidenceReference` | Opaque pointer supplied by a caller; not an authenticated source record. | [L72](../../../src/mirrormind/core/decision_trace.py#L72) |
| `ObservedFact` | class | `class ObservedFact` | One scalar observation, separate from estimates and modeled outcomes. | [L84](../../../src/mirrormind/core/decision_trace.py#L84) |
| `ForecastEstimate` | class | `class ForecastEstimate` | — | [L98](../../../src/mirrormind/core/decision_trace.py#L98) |
| `ModelingAssumption` | class | `class ModelingAssumption` | — | [L109](../../../src/mirrormind/core/decision_trace.py#L109) |
| `OutcomeMetric` | class | `class OutcomeMetric` | — | [L114](../../../src/mirrormind/core/decision_trace.py#L114) |
| `ConditionalOutcome` | class | `class ConditionalOutcome` | A declared conditional result; the reference does not prove execution. | [L120](../../../src/mirrormind/core/decision_trace.py#L120) |
| `MissingEvidence` | class | `class MissingEvidence` | — | [L139](../../../src/mirrormind/core/decision_trace.py#L139) |
| `CostMeasurement` | class | `class CostMeasurement` | — | [L147](../../../src/mirrormind/core/decision_trace.py#L147) |
| `CostMeasurement.check_measurement` | method | `def check_measurement(self) -> 'CostMeasurement'` | — | [L156](../../../src/mirrormind/core/decision_trace.py#L156) |
| `HumanReview` | class | `class HumanReview` | — | [L165](../../../src/mirrormind/core/decision_trace.py#L165) |
| `HumanReview.check_decision_fields` | method | `def check_decision_fields(self) -> 'HumanReview'` | — | [L174](../../../src/mirrormind/core/decision_trace.py#L174) |
| `DecisionTrace` | class | `class DecisionTrace` | Immutable v1 result shape; approval records review but grants no action. | [L189](../../../src/mirrormind/core/decision_trace.py#L189) |
| `DecisionTrace.result_sha256` | method | `def result_sha256(self) -> str` | Hash canonical result fields, excluding review to avoid circularity. | [L225](../../../src/mirrormind/core/decision_trace.py#L225) |
| `DecisionTrace.check_trace_references_and_cutoff` | method | `def check_trace_references_and_cutoff(self) -> 'DecisionTrace'` | — | [L247](../../../src/mirrormind/core/decision_trace.py#L247) |
| `ExecutionEvidence` | class | `class ExecutionEvidence` | Deterministic provenance for one selected or parity execution result. | [L332](../../../src/mirrormind/core/decision_trace.py#L332) |
| `ConditionalOutcomeV2` | class | `class ConditionalOutcomeV2` | A v2 outcome linked to the execution records that support its metrics. | [L345](../../../src/mirrormind/core/decision_trace.py#L345) |
| `DecisionTraceV2` | class | `class DecisionTraceV2` | Decision trace with explicit, linked simulation execution provenance. | [L353](../../../src/mirrormind/core/decision_trace.py#L353) |
| `DecisionTraceV2.check_execution_evidence` | method | `def check_execution_evidence(self) -> 'DecisionTraceV2'` | — | [L369](../../../src/mirrormind/core/decision_trace.py#L369) |

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

## `mirrormind.domains.retail.census_evaluation`

Source: [`src/mirrormind/domains/retail/census_evaluation.py`](../../../src/mirrormind/domains/retail/census_evaluation.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `decimal`, `fractions`, `hashlib`, `json`, `math`, `mirrormind.domains.retail.census_vintages`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `CensusForecastOrigin` | class | `class CensusForecastOrigin` | One predeclared monthly reference period and date-only issue boundary. | [L39](../../../src/mirrormind/domains/retail/census_evaluation.py#L39) |
| `_month_offset` | function | `def _month_offset(month: date, offset: int) -> date` | — | [L46](../../../src/mirrormind/domains/retail/census_evaluation.py#L46) |
| `_record_payload` | function | `def _record_payload(record: CensusVintageRecord) -> dict[str, str]` | — | [L54](../../../src/mirrormind/domains/retail/census_evaluation.py#L54) |
| `_manifest_sha256` | function | `def _manifest_sha256(records: tuple[CensusVintageRecord, ...]) -> str` | — | [L67](../../../src/mirrormind/domains/retail/census_evaluation.py#L67) |
| `_selection_receipt` | function | `def _selection_receipt(view: CensusVintageView, manifest_sha256: str) -> dict[str, object]` | Summarize a selected vintage without repeating every release identifier. | [L86](../../../src/mirrormind/domains/retail/census_evaluation.py#L86) |
| `_validate_metric_input` | function | `def _validate_metric_input(value: Decimal) -> None` | — | [L108](../../../src/mirrormind/domains/retail/census_evaluation.py#L108) |
| `_metric_float` | function | `def _metric_float(value: Fraction) -> float` | — | [L123](../../../src/mirrormind/domains/retail/census_evaluation.py#L123) |
| `_sqrt_metric_float` | function | `def _sqrt_metric_float(value: Fraction) -> float` | Round a non-negative exact mean square without underflowing its root. | [L137](../../../src/mirrormind/domains/retail/census_evaluation.py#L137) |
| `_metrics` | function | `def _metrics(forecasts: tuple[Fraction, ...], actuals: tuple[Fraction, ...]) -> dict[str, float \| None]` | — | [L173](../../../src/mirrormind/domains/retail/census_evaluation.py#L173) |
| `evaluate_census_vintage_backtest` | function | `def evaluate_census_vintage_backtest(records: tuple[CensusVintageRecord, ...], *, series_id: str, origins: tuple[CensusForecastOrigin, ...], split: Literal['validation', 'holdout']) -> dict[str, object]` | Evaluate fixed monthly baselines using only each origin's visible vintage. | [L194](../../../src/mirrormind/domains/retail/census_evaluation.py#L194) |

## `mirrormind.domains.retail.census_vintages`

Source: [`src/mirrormind/domains/retail/census_vintages.py`](../../../src/mirrormind/domains/retail/census_vintages.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `decimal`, `re`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `CensusVintageRecord` | class | `class CensusVintageRecord` | One normalized aggregate value from one immutable release artifact. | [L23](../../../src/mirrormind/domains/retail/census_vintages.py#L23) |
| `CensusVintageView` | class | `class CensusVintageView` | Selected values available before a target release date, not source proof. | [L36](../../../src/mirrormind/domains/retail/census_vintages.py#L36) |
| `CensusVintageView.receipt` | method | `def receipt(self) -> dict[str, object]` | Return sanitized selection provenance without value-level observations. | [L43](../../../src/mirrormind/domains/retail/census_vintages.py#L43) |
| `_validate_record` | function | `def _validate_record(record: CensusVintageRecord, *, series_id: str) -> None` | Reject malformed normalized metadata before applying time selection. | [L66](../../../src/mirrormind/domains/retail/census_vintages.py#L66) |
| `select_census_vintage_as_of` | function | `def select_census_vintage_as_of(records: tuple[CensusVintageRecord, ...], *, series_id: str, target_release_on: date) -> CensusVintageView` | Select latest per-month records published strictly before target release. | [L95](../../../src/mirrormind/domains/retail/census_vintages.py#L95) |

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

## `mirrormind.domains.retail.evaluation_flow`

Source: [`src/mirrormind/domains/retail/evaluation_flow.py`](../../../src/mirrormind/domains/retail/evaluation_flow.py)

Static imports (including inside functions): `__future__`, `datetime`, `mirrormind.domains.retail.evidence_flow`, `mirrormind.domains.retail.release_backtest`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `evaluate_retail_evidence_flow` | function | `def evaluate_retail_evidence_flow(flow: RetailUciEvidenceFlow, *, stock_code: str, evaluation_on: date, holdout_days: int=7) -> dict[str, object]` | Return an aggregate fixed-split evaluation and one status per target. | [L17](../../../src/mirrormind/domains/retail/evaluation_flow.py#L17) |

## `mirrormind.domains.retail.evidence_flow`

Source: [`src/mirrormind/domains/retail/evidence_flow.py`](../../../src/mirrormind/domains/retail/evidence_flow.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `mirrormind.domains.retail.calendar_coverage`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.uci_workbook`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.snapshots`, `types`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailCsvEvidenceFlow` | class | `class RetailCsvEvidenceFlow` | Staged CSV components and the rows matching one declared historical origin. | [L45](../../../src/mirrormind/domains/retail/evidence_flow.py#L45) |
| `RetailCsvEvidenceFlow.receipt` | method | `def receipt(self) -> dict[str, object]` | Return status and aggregate counts without series identifiers or values. | [L54](../../../src/mirrormind/domains/retail/evidence_flow.py#L54) |
| `RetailUciEvidenceFlow` | class | `class RetailUciEvidenceFlow` | Workbook projection, declared calendar and release audit for later offline use. | [L78](../../../src/mirrormind/domains/retail/evidence_flow.py#L78) |
| `RetailUciEvidenceFlow.receipt` | method | `def receipt(self) -> dict[str, object]` | Return component summaries only; never product IDs or transaction values. | [L87](../../../src/mirrormind/domains/retail/evidence_flow.py#L87) |
| `prepare_retail_csv_evidence_flow` | function | `def prepare_retail_csv_evidence_flow(stream: BinaryIO, *, expected_sha256: str, declaration: SourceReviewDeclaration, inspected_on: date, series_id: str, origin_on: str) -> RetailCsvEvidenceFlow` | Compose bounded CSV staging, review metadata, quality and declared as-of selection. | [L101](../../../src/mirrormind/domains/retail/evidence_flow.py#L101) |
| `prepare_retail_uci_evidence_flow` | function | `def prepare_retail_uci_evidence_flow(stream: BinaryIO, *, expected_sha256: str, declaration: SourceReviewDeclaration, inspected_on: date, declared_calendar: tuple[date, ...], declared_releases: tuple[DeclaredProductRelease, ...], origin_on: date) -> RetailUciEvidenceFlow` | Compose bounded XLSX projection and explicit, unverified calendar/release checks. | [L134](../../../src/mirrormind/domains/retail/evidence_flow.py#L134) |

## `mirrormind.domains.retail.policy_simulation`

Source: [`src/mirrormind/domains/retail/policy_simulation.py`](../../../src/mirrormind/domains/retail/policy_simulation.py)

Static imports (including inside functions): `__future__`, `hashlib`, `json`, `pydantic`, `random`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_DemandStream` | class | `class _DemandStream` | — | [L34](../../../src/mirrormind/domains/retail/policy_simulation.py#L34) |
| `RetailPolicySimulationState` | class | `class RetailPolicySimulationState` | JSON-safe inventory state shared by the reference and engine worlds. | [L41](../../../src/mirrormind/domains/retail/policy_simulation.py#L41) |
| `RetailPolicyAssumptions` | class | `class RetailPolicyAssumptions` | Explicit units, inventory controls and abstract synthetic costs. | [L57](../../../src/mirrormind/domains/retail/policy_simulation.py#L57) |
| `RetailPolicyComparisonRequest` | class | `class RetailPolicyComparisonRequest` | Input contract for one paired, 28-day synthetic experiment. | [L77](../../../src/mirrormind/domains/retail/policy_simulation.py#L77) |
| `RetailPolicyComparisonRequest.validate_experiment_bounds` | method | `def validate_experiment_bounds(self) -> RetailPolicyComparisonRequest` | — | [L88](../../../src/mirrormind/domains/retail/policy_simulation.py#L88) |
| `_build_demand_streams` | function | `def _build_demand_streams(request: RetailPolicyComparisonRequest) -> tuple[_DemandStream, ...]` | Generate one reproducible exogenous sequence per replication. | [L106](../../../src/mirrormind/domains/retail/policy_simulation.py#L106) |
| `sample_demand_units` | function | `def sample_demand_units(expected_units: int, multiplier_index: int) -> int` | Apply the fixed 75/100/125 percent synthetic multiplier with integer rounding. | [L137](../../../src/mirrormind/domains/retail/policy_simulation.py#L137) |
| `_order_quantity` | function | `def _order_quantity(*, policy_id: str, day_index: int, inventory_position_units: int, demand_profile_units: tuple[int, ...], lead_time_days: int, assumptions: RetailPolicyAssumptions) -> int` | — | [L150](../../../src/mirrormind/domains/retail/policy_simulation.py#L150) |
| `create_retail_policy_state` | function | `def create_retail_policy_state(assumptions: RetailPolicyAssumptions) -> RetailPolicySimulationState` | Create a fresh, JSON-safe state with the declared starting inventory. | [L181](../../../src/mirrormind/domains/retail/policy_simulation.py#L181) |
| `advance_retail_policy_day` | function | `def advance_retail_policy_day(state: RetailPolicySimulationState, *, policy_id: str, day_index: int, demand_units: int, demand_profile_units: tuple[int, ...], lead_time_days: int, assumptions: RetailPolicyAssumptions) -> RetailPolicySimulationState` | Apply one day boundary: receive, fulfill, cost, then place a new order. | [L202](../../../src/mirrormind/domains/retail/policy_simulation.py#L202) |
| `finalize_retail_policy_metrics` | function | `def finalize_retail_policy_metrics(state: RetailPolicySimulationState, assumptions: RetailPolicyAssumptions) -> dict[str, int]` | Derive the public cost and service metrics from a completed state. | [L279](../../../src/mirrormind/domains/retail/policy_simulation.py#L279) |
| `_simulate_replication` | function | `def _simulate_replication(*, policy_id: str, demand_units: tuple[int, ...], demand_profile_units: tuple[int, ...], lead_time_days: int, assumptions: RetailPolicyAssumptions) -> dict[str, int]` | Run one policy against one fixed demand stream using day-boundary rules. | [L325](../../../src/mirrormind/domains/retail/policy_simulation.py#L325) |
| `_basis_points` | function | `def _basis_points(numerator: int, denominator: int) -> int \| None` | — | [L348](../../../src/mirrormind/domains/retail/policy_simulation.py#L348) |
| `summarize_retail_policy_runs` | function | `def summarize_retail_policy_runs(policy_id: str, replication_results: list[dict[str, object]]) -> dict[str, object]` | Aggregate already computed replication rows without changing their source. | [L354](../../../src/mirrormind/domains/retail/policy_simulation.py#L354) |
| `_aggregate_policy` | function | `def _aggregate_policy(*, policy_id: str, demand_streams: tuple[_DemandStream, ...], demand_profile_units: tuple[int, ...], lead_time_days: int, assumptions: RetailPolicyAssumptions) -> dict[str, object]` | — | [L394](../../../src/mirrormind/domains/retail/policy_simulation.py#L394) |
| `_lead_time_scenarios` | function | `def _lead_time_scenarios(base_lead_time_days: int) -> tuple[int, ...]` | — | [L420](../../../src/mirrormind/domains/retail/policy_simulation.py#L420) |
| `compare_synthetic_retail_policies` | function | `def compare_synthetic_retail_policies(request: RetailPolicyComparisonRequest) -> dict[str, object]` | Compare three replenishment rules using paired caller-declared inputs. | [L432](../../../src/mirrormind/domains/retail/policy_simulation.py#L432) |

## `mirrormind.domains.retail.release_backtest`

Source: [`src/mirrormind/domains/retail/release_backtest.py`](../../../src/mirrormind/domains/retail/release_backtest.py)

Static imports (including inside functions): `__future__`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.modules.forecasting.baselines`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `backtest_declared_retail_releases` | function | `def backtest_declared_retail_releases(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, holdout_days: int=7) -> dict[str, object]` | Compare two fixed one-day baselines on matched, eligible fictional days. | [L19](../../../src/mirrormind/domains/retail/release_backtest.py#L19) |

## `mirrormind.domains.retail.residual_envelope`

Source: [`src/mirrormind/domains/retail/residual_envelope.py`](../../../src/mirrormind/domains/retail/residual_envelope.py)

Static imports (including inside functions): `__future__`, `datetime`, `heapq`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.modules.forecasting.baselines`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `evaluate_retail_residual_envelopes` | function | `def evaluate_retail_residual_envelopes(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, holdout_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5) -> dict[str, object]` | Audit one-day seasonal-naive envelopes using only past published errors. | [L21](../../../src/mirrormind/domains/retail/residual_envelope.py#L21) |

## `mirrormind.domains.retail.selection_sensitivity`

Source: [`src/mirrormind/domains/retail/selection_sensitivity.py`](../../../src/mirrormind/domains/retail/selection_sensitivity.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.residual_envelope`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `ExcludedTargetSensitivity` | class | `class ExcludedTargetSensitivity` | Two-window counterfactual mean bounds with eligibility denominators. | [L17](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L17) |
| `ExcludedTargetSensitivity.receipt` | method | `def receipt(self) -> dict[str, str \| int \| float \| None]` | Report counterfactual bounds without any excluded target values. | [L33](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L33) |
| `assess_excluded_target_sensitivity` | function | `def assess_excluded_target_sensitivity(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, excluded_value_ceiling: int, window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5) -> ExcludedTargetSensitivity` | Vary hypothetical excluded day values, preserving each window cutoff. | [L58](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L58) |
| `_collect_eligible_window_totals` | function | `def _collect_eligible_window_totals(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, window_days: int, calibration_days: int, min_calibration_residuals: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]` | Collect integer totals once at each declared as-of evaluation cutoff. | [L86](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L86) |
| `_scenario_from_eligible_totals` | function | `def _scenario_from_eligible_totals(earlier: tuple[int, int, int], later: tuple[int, int, int], excluded_value_ceiling: int) -> ExcludedTargetSensitivity` | Apply a caller's assumption to validated eligible totals, without I/O. | [L144](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L144) |

## `mirrormind.domains.retail.sensitivity_sweep`

Source: [`src/mirrormind/domains/retail/sensitivity_sweep.py`](../../../src/mirrormind/domains/retail/sensitivity_sweep.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `itertools`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.selection_sensitivity`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailSensitivitySweep` | class | `class RetailSensitivitySweep` | An ordered, bounded list of hypothetical scenario results. | [L22](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L22) |
| `RetailSensitivitySweep.receipt` | method | `def receipt(self) -> dict[str, object]` | Show scenario receipts but never selected source identifiers. | [L30](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L30) |
| `sweep_excluded_target_sensitivity` | function | `def sweep_excluded_target_sensitivity(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, ceilings: tuple[int, ...], window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5, minimum_eligible_per_window: int=3, minimum_coverage_percent: int=80) -> RetailSensitivitySweep` | Compare two to eight strictly increasing, hypothetical ceilings. | [L50](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L50) |

## `mirrormind.domains.retail.synthetic_decision_workflow`

Source: [`src/mirrormind/domains/retail/synthetic_decision_workflow.py`](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `datetime`, `hashlib`, `json`, `mirrormind.core.decision_trace`, `mirrormind.domains.retail.evaluation_flow`, `mirrormind.domains.retail.policy_simulation`, `mirrormind.domains.retail.residual_envelope`, `mirrormind.domains.retail.synthetic_fixtures`, `mirrormind.domains.retail.worldkernel_policy_world`, `mirrormind.modules.forecasting.baselines`, `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SyntheticDecisionWorkflowRequest` | class | `class SyntheticDecisionWorkflowRequest` | Strict bounded options for the generated local decision example. | [L82](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L82) |
| `SyntheticDecisionWorkflowRequest.validate_as_of` | method | `def validate_as_of(cls, value: date) -> date` | — | [L95](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L95) |
| `_default_policy_assumptions` | function | `def _default_policy_assumptions() -> RetailPolicyAssumptions` | Return the same explicit fictional controls used by the M1E-03 demo. | [L105](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L105) |
| `_cutoff_timestamp` | function | `def _cutoff_timestamp(value: date) -> datetime` | — | [L121](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L121) |
| `_canonical_json_sha256` | function | `def _canonical_json_sha256(value: object) -> str` | Hash a JSON value using the workflow's sorted-key UTF-8 encoding. | [L125](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L125) |
| `_versioned_artifact_digests` | function | `def _versioned_artifact_digests(result: dict[str, object]) -> dict[str, dict[str, str]]` | Bind each returned evaluation artifact to its declared local schema. | [L137](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L137) |
| `_decision_identity_sha256` | function | `def _decision_identity_sha256(request: SyntheticDecisionWorkflowRequest, artifact_digests: dict[str, dict[str, str]]) -> str` | Create a deterministic identity for this exact request/result pair. | [L155](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L155) |
| `_flow_snapshot_digest` | function | `def _flow_snapshot_digest(flow: Any) -> str` | — | [L170](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L170) |
| `_eligible_observation_rows` | function | `def _eligible_observation_rows(flow: Any, *, as_of: date) -> tuple[tuple[date, int, date], ...]` | — | [L178](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L178) |
| `_requested_history_window` | function | `def _requested_history_window(as_of: date) -> tuple[date, ...]` | — | [L202](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L202) |
| `_execution_evidence_records` | function | `def _execution_evidence_records(comparison: dict[str, object], *, produced_at: datetime) -> tuple[tuple[ExecutionEvidence, ...], tuple[str, ...], str, str, dict[str, object]]` | Validate selected-engine metadata and create replayable trace records. | [L206](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L206) |
| `_policy_outcomes` | function | `def _policy_outcomes(comparison: dict[str, object], *, engine_contract_ref: str, execution_evidence_refs: tuple[str, ...], forecast_refs: tuple[str, ...], assumption_refs: tuple[str, ...], policy_caveat_refs: tuple[str, ...]) -> tuple[ConditionalOutcomeV2, ...]` | — | [L330](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L330) |
| `_build_trace` | function | `def _build_trace(*, as_of: date, identity_sha256: str, snapshot_sha256: str, observations: tuple[tuple[date, int, date], ...], history: tuple[tuple[date, int, date], ...], forecast_profile: tuple[int, ...], comparison: dict[str, object], engine_contract_ref: str, execution_evidence: tuple[ExecutionEvidence, ...], execution_evidence_refs: tuple[str, ...]) -> DecisionTraceV2` | — | [L413](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L413) |
| `run_synthetic_decision_workflow` | function | `def run_synthetic_decision_workflow(request: SyntheticDecisionWorkflowRequest, *, future_units: int=9, all_unpublished: bool=False, policy_comparator: Callable[[RetailPolicyComparisonRequest], dict[str, object]] \| None=None) -> dict[str, object]` | Run one deterministic, non-persisting synthetic decision comparison. | [L631](../../../src/mirrormind/domains/retail/synthetic_decision_workflow.py#L631) |

## `mirrormind.domains.retail.synthetic_fixtures`

Source: [`src/mirrormind/domains/retail/synthetic_fixtures.py`](../../../src/mirrormind/domains/retail/synthetic_fixtures.py)

Static imports (including inside functions): `__future__`, `datetime`, `hashlib`, `io`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.evaluation_flow`, `mirrormind.domains.retail.evidence_flow`, `mirrormind.domains.retail.uci_workbook`, `mirrormind.modules.evidence.intake_review`, `openpyxl`, `re`, `zipfile`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `fixture_day` | function | `def fixture_day(index: int) -> date` | Return a one-based calendar day in the generated fixture. | [L34](../../../src/mirrormind/domains/retail/synthetic_fixtures.py#L34) |
| `_canonical_xlsx` | function | `def _canonical_xlsx(data: bytes) -> bytes` | Normalize ZIP order, timestamps and compression for a stable digest. | [L41](../../../src/mirrormind/domains/retail/synthetic_fixtures.py#L41) |
| `_synthetic_workbook` | function | `def _synthetic_workbook(*, future_units: int) -> bytes` | — | [L71](../../../src/mirrormind/domains/retail/synthetic_fixtures.py#L71) |
| `build_synthetic_evidence_flow` | function | `def build_synthetic_evidence_flow(*, future_units: int=9, all_unpublished: bool=False, evaluation_on: date=EVALUATION_ON) -> RetailUciEvidenceFlow` | Build a bounded fictional workbook with explicit fixture release dates. | [L101](../../../src/mirrormind/domains/retail/synthetic_fixtures.py#L101) |
| `run_synthetic_evaluation` | function | `def run_synthetic_evaluation(*, holdout_days: int=7, future_units: int=9, all_unpublished: bool=False, evaluation_on: date=EVALUATION_ON) -> dict[str, object]` | Build the fixture and run the existing local evidence evaluation. | [L162](../../../src/mirrormind/domains/retail/synthetic_fixtures.py#L162) |

## `mirrormind.domains.retail.uci_event_time`

Source: [`src/mirrormind/domains/retail/uci_event_time.py`](../../../src/mirrormind/domains/retail/uci_event_time.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `datetime`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.domains.retail.uci_workbook`, `mirrormind.modules.forecasting.baselines`, `re`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `UciEventTimeEvaluationError` | class | `class UciEventTimeEvaluationError` | A snapshot, coverage contract or fixed split is not representable. | [L39](../../../src/mirrormind/domains/retail/uci_event_time.py#L39) |
| `_date_range` | function | `def _date_range(start: date, end: date) -> tuple[date, ...]` | — | [L43](../../../src/mirrormind/domains/retail/uci_event_time.py#L43) |
| `_snapshot_counts` | function | `def _snapshot_counts(snapshot: UciWorkbookReadResult) -> dict[tuple[str, date], int]` | — | [L47](../../../src/mirrormind/domains/retail/uci_event_time.py#L47) |
| `_coverage_dates` | function | `def _coverage_dates(values: Iterable[date]) -> frozenset[date]` | — | [L78](../../../src/mirrormind/domains/retail/uci_event_time.py#L78) |
| `_metrics` | function | `def _metrics(forecasts: tuple[float, ...], actuals: tuple[int, ...]) -> dict[str, float \| None] \| None` | — | [L98](../../../src/mirrormind/domains/retail/uci_event_time.py#L98) |
| `evaluate_uci_event_time` | function | `def evaluate_uci_event_time(snapshot: UciWorkbookReadResult, *, complete_event_dates: Iterable[date], split: Literal['validation', 'holdout']) -> dict[str, object]` | Compare fixed one-day baselines on one frozen UCI event-time split. | [L107](../../../src/mirrormind/domains/retail/uci_event_time.py#L107) |

## `mirrormind.domains.retail.uci_transactions`

Source: [`src/mirrormind/domains/retail/uci_transactions.py`](../../../src/mirrormind/domains/retail/uci_transactions.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `re`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `ProductDayUnits` | class | `class ProductDayUnits` | Positive invoice-line units for a product/event day, not latent demand. | [L31](../../../src/mirrormind/domains/retail/uci_transactions.py#L31) |
| `UciRetailProjection` | class | `class UciRetailProjection` | Immutable local research projection with no authenticated data rights. | [L40](../../../src/mirrormind/domains/retail/uci_transactions.py#L40) |
| `UciRetailProjection.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | Return only aggregate counters and explicit permission/time uncertainty. | [L51](../../../src/mirrormind/domains/retail/uci_transactions.py#L51) |
| `_invoice_number` | function | `def _invoice_number(value: object) -> str` | Normalize an invoice code, preserving explicit C-prefixed cancellations. | [L65](../../../src/mirrormind/domains/retail/uci_transactions.py#L65) |
| `_transaction_day` | function | `def _transaction_day(value: object) -> date` | Accept only timezone-naive Excel-style datetimes as event observations. | [L74](../../../src/mirrormind/domains/retail/uci_transactions.py#L74) |
| `is_valid_uci_stock_code` | function | `def is_valid_uci_stock_code(value: object, *, allow_internal_spaces: bool=False) -> TypeGuard[str]` | Validate a normalized source code without trimming or coercion. | [L81](../../../src/mirrormind/domains/retail/uci_transactions.py#L81) |
| `project_uci_retail_rows` | function | `def project_uci_retail_rows(rows: Iterable[Mapping[str, object]], *, max_rows: int=MAX_ROWS, max_groups: int=MAX_GROUPS) -> UciRetailProjection` | Summarize strictly positive invoice quantities, never source availability. | [L102](../../../src/mirrormind/domains/retail/uci_transactions.py#L102) |
| `_project_uci_retail_rows` | function | `def _project_uci_retail_rows(rows: Iterable[Mapping[str, object]], *, max_rows: int, max_groups: int, max_groups_ceiling: int, allow_internal_stock_code_spaces: bool, allow_unverified_invoice_prefix: bool=False) -> UciRetailProjection` | Internal bounded implementation shared with the UCI workbook adapter. | [L123](../../../src/mirrormind/domains/retail/uci_transactions.py#L123) |

## `mirrormind.domains.retail.uci_workbook`

Source: [`src/mirrormind/domains/retail/uci_workbook.py`](../../../src/mirrormind/domains/retail/uci_workbook.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `hashlib`, `hmac`, `io`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.domains.retail.uci_xlsx_xml`, `openpyxl.utils.datetime`, `re`, `typing`, `zipfile`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `UciWorkbookReadResult` | class | `class UciWorkbookReadResult` | Local digest-coupled product-day projection without source approval. | [L47](../../../src/mirrormind/domains/retail/uci_workbook.py#L47) |
| `UciWorkbookReadResult.receipt` | method | `def receipt(self) -> dict[str, str \| int]` | Summarize input identity and exclusions, not raw customer or invoice data. | [L53](../../../src/mirrormind/domains/retail/uci_workbook.py#L53) |
| `_bounded_read` | function | `def _bounded_read(stream: BinaryIO) -> bytes` | Consume at most one sentinel byte over the compressed workbook limit. | [L65](../../../src/mirrormind/domains/retail/uci_workbook.py#L65) |
| `_check_zip_members` | function | `def _check_zip_members(raw: bytes, *, max_entry_bytes: int=MAX_ZIP_ENTRY_BYTES, max_total_bytes: int=MAX_ZIP_TOTAL_BYTES) -> None` | Reject excessive/active archive entries before workbook XML processing. | [L90](../../../src/mirrormind/domains/retail/uci_workbook.py#L90) |
| `_normalize_workbook_stock_code` | function | `def _normalize_workbook_stock_code(value: object) -> str` | Normalize only the exact UCI workbook's reviewed cell encodings. | [L128](../../../src/mirrormind/domains/retail/uci_workbook.py#L128) |
| `_normalize_uci_workbook_invoice` | function | `def _normalize_uci_workbook_invoice(value: object) -> object` | Classify scoped invoice IDs; only exact uppercase C marks cancellation. | [L137](../../../src/mirrormind/domains/retail/uci_workbook.py#L137) |
| `read_uci_workbook` | function | `def read_uci_workbook(stream: BinaryIO, *, expected_sha256: str, sheet_name: str='Online Retail', max_rows: int=MAX_ROWS, max_groups: int=MAX_GROUPS, max_zip_entry_bytes: int=MAX_ZIP_ENTRY_BYTES, max_zip_total_bytes: int=MAX_ZIP_TOTAL_BYTES) -> UciWorkbookReadResult` | Project a small, already-authorized local workbook through strict UCI schema. | [L152](../../../src/mirrormind/domains/retail/uci_workbook.py#L152) |

## `mirrormind.domains.retail.uci_xlsx_xml`

Source: [`src/mirrormind/domains/retail/uci_xlsx_xml.py`](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py)

Static imports (including inside functions): `__future__`, `collections`, `collections.abc`, `datetime`, `decimal`, `math`, `openpyxl.styles.numbers`, `openpyxl.utils.datetime`, `re`, `xml.parsers`, `zipfile`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_local_name` | function | `def _local_name(name: str) -> str` | — | [L41](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L41) |
| `_reject_xml_feature` | function | `def _reject_xml_feature(*_args: object) -> None` | — | [L45](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L45) |
| `_new_xml_parser` | function | `def _new_xml_parser() -> expat.XMLParserType` | — | [L49](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L49) |
| `_parse_small_xml_member` | function | `def _parse_small_xml_member(archive: ZipFile, name: str, start_handler) -> None` | — | [L58](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L58) |
| `_resolve_worksheet` | function | `def _resolve_worksheet(archive: ZipFile, sheet_name: str) -> tuple[str, bool]` | Resolve the one allowed sheet and the workbook's date-system flag. | [L74](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L74) |
| `_date_style_ids` | function | `def _date_style_ids(archive: ZipFile) -> frozenset[int]` | Return style indexes whose number formats represent Excel dates. | [L135](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L135) |
| `_column_and_row` | function | `def _column_and_row(reference: str) -> tuple[int, int]` | — | [L191](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L191) |
| `_iter_worksheet_rows` | function | `def _iter_worksheet_rows(archive: ZipFile, worksheet_path: str, *, max_rows: int, collect_shared_references: bool) -> Iterator[tuple[int, dict[int, dict[str, object]]]]` | Stream selected cells and reject duplicate coordinates or payloads. | [L204](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L204) |
| `_selected_shared_string_indices` | function | `def _selected_shared_string_indices(archive: ZipFile, worksheet_path: str, *, max_rows: int) -> frozenset[int]` | — | [L386](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L386) |
| `_read_required_shared_strings` | function | `def _read_required_shared_strings(archive: ZipFile, required: frozenset[int]) -> dict[int, str]` | — | [L404](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L404) |
| `_decode_cell` | function | `def _decode_cell(cell: dict[str, object] \| None, *, column: int, shared_strings: dict[int, str], date_style_ids: frozenset[int], epoch: datetime, is_header: bool=False) -> object` | Decode one selected cell under the header or field-specific type contract. | [L479](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L479) |
| `iter_uci_projection_rows` | function | `def iter_uci_projection_rows(archive: ZipFile, *, sheet_name: str, max_rows: int, expected_header: tuple[str, ...]) -> Iterator[dict[str, object]]` | Yield only approved projection fields; never materialize Description values. | [L548](../../../src/mirrormind/domains/retail/uci_xlsx_xml.py#L548) |

## `mirrormind.domains.retail.worldkernel_policy_world`

Source: [`src/mirrormind/domains/retail/worldkernel_policy_world.py`](../../../src/mirrormind/domains/retail/worldkernel_policy_world.py)

Static imports (including inside functions): `.policy_simulation`, `__future__`, `collections.abc`, `random`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `create_policy_world_initial_state` | function | `def create_policy_world_initial_state(assumptions: RetailPolicyAssumptions, lead_time_days: tuple[int, ...]) -> dict[str, object]` | Create the exact state envelope accepted by the registered handler. | [L40](../../../src/mirrormind/domains/retail/worldkernel_policy_world.py#L40) |
| `_validated_parameters` | function | `def _validated_parameters(parameters: Mapping[str, Any]) -> tuple[tuple[int, ...], tuple[int, ...], RetailPolicyAssumptions]` | — | [L68](../../../src/mirrormind/domains/retail/worldkernel_policy_world.py#L68) |
| `mirrormind_retail_policy_step` | function | `def mirrormind_retail_policy_step(state: dict[str, Any], parameters: Mapping[str, Any], rng: Random) -> dict[str, Any]` | Apply one shared synthetic demand draw to all policy/sensitivity pairs. | [L104](../../../src/mirrormind/domains/retail/worldkernel_policy_world.py#L104) |
| `register_mirrormind_policy_world` | function | `def register_mirrormind_policy_world(registrar: Callable[..., None]) -> None` | Register exactly this versioned handler through trusted worker code. | [L164](../../../src/mirrormind/domains/retail/worldkernel_policy_world.py#L164) |

## `mirrormind.modules.__init__`

Source: [`src/mirrormind/modules/__init__.py`](../../../src/mirrormind/modules/__init__.py)

No top-level classes or functions.

## `mirrormind.modules.evidence.__init__`

Source: [`src/mirrormind/modules/evidence/__init__.py`](../../../src/mirrormind/modules/evidence/__init__.py)

No top-level classes or functions.

## `mirrormind.modules.evidence.atomic_governed_publisher`

Source: [`src/mirrormind/modules/evidence/atomic_governed_publisher.py`](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.local_checkpoint_publisher`, `mirrormind.modules.evidence.operator_governance`, `pathlib`, `re`, `sqlite3`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `AtomicGovernedRevision` | class | `class AtomicGovernedRevision` | One local snapshot; does not represent source or production authorization. | [L54](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L54) |
| `AtomicGovernedRevision.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Only safe local consistency fields; never an access-control token. | [L64](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L64) |
| `_HistoricalSignatureVerifier` | class | `class _HistoricalSignatureVerifier` | Reuse tested signature/history helpers without enabling direct publishing. | [L83](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L83) |
| `_HistoricalSignatureVerifier.__init__` | method | `def __init__(self, checkpoint_keys: Mapping[str, bytes], witness_keys: Mapping[str, bytes], operator_keys: Mapping[str, bytes], bootstrap: str) -> None` | — | [L86](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L86) |
| `_HistoricalSignatureVerifier.publish` | method | `def publish(self, *args: object, **kwargs: object) -> NoReturn` | — | [L99](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L99) |
| `AtomicGovernedPublisher` | class | `class AtomicGovernedPublisher` | Opt-in local shared schema with serial policy updates and publication. | [L103](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L103) |
| `AtomicGovernedPublisher.__init__` | method | `def __init__(self, path: Path, *, administrator_public_keys: Mapping[str, bytes], checkpoint_keys: Mapping[str, bytes], witness_keys: Mapping[str, bytes], initial_witness_key_id: str, create: bool=False) -> None` | — | [L111](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L111) |
| `AtomicGovernedPublisher._connect` | method | `def _connect(self) -> sqlite3.Connection` | — | [L247](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L247) |
| `AtomicGovernedPublisher._schema` | method | `def _schema(self, db: sqlite3.Connection) -> None` | — | [L259](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L259) |
| `AtomicGovernedPublisher._read_policy` | method | `def _read_policy(self, db: sqlite3.Connection, checked_on: date) -> tuple[int, str, dict[str, tuple[str, date, bool]]]` | — | [L275](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L275) |
| `AtomicGovernedPublisher._check_policy_role_separation` | method | `def _check_policy_role_separation(self, records: Mapping[str, tuple[str, date, bool]]) -> None` | — | [L286](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L286) |
| `AtomicGovernedPublisher._verifier` | method | `def _verifier(self, records: Mapping[str, tuple[str, date, bool]]) -> _HistoricalSignatureVerifier` | — | [L299](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L299) |
| `AtomicGovernedPublisher._expected` | method | `def _expected(expected: int, head: str, current: int, current_head: str) -> None` | — | [L311](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L311) |
| `AtomicGovernedPublisher.append_policy` | method | `def append_policy(self, event: SignedOperatorPolicyEvent, *, expected_policy_revision: int, expected_policy_head_sha256: str, checked_on: date) -> OperatorPolicyRevision` | Atomically advance the same-file policy read by future publications. | [L319](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L319) |
| `AtomicGovernedPublisher.snapshot` | method | `def snapshot(self, packet: SourceReviewPacket, *, checked_on: date, externally_expected_policy_head_sha256: str \| None=None, externally_expected_publication_head_sha256: str \| None=None) -> AtomicGovernedRevision` | Reverify *both* local signed histories in the same read snapshot. | [L371](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L371) |
| `AtomicGovernedPublisher.publish` | method | `def publish(self, packet: SourceReviewPacket, command: SignedPublicationCommand, *, expected_policy_revision: int, expected_policy_head_sha256: str, expected_publication_sequence: int, expected_publication_head_sha256: str, checked_on: date) -> AtomicGovernedRevision` | Reject revoked/expired keys and append under ONE SQLite write lock. | [L410](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L410) |
| `_last_governance_date` | function | `def _last_governance_date(db: sqlite3.Connection, revision: int) -> date` | Read only the exact preceding canonical signed event's calendar date. | [L508](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L508) |

## `mirrormind.modules.evidence.authority_transcript`

Source: [`src/mirrormind/modules/evidence/authority_transcript.py`](../../../src/mirrormind/modules/evidence/authority_transcript.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.head_checkpoints`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.sqlite_review_registry`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedAuthorityReceipt` | class | `class SignedAuthorityReceipt` | Witness attestation of one independently signed review checkpoint. | [L36](../../../src/mirrormind/modules/evidence/authority_transcript.py#L36) |
| `WitnessKeyHandoff` | class | `class WitnessKeyHandoff` | Both old and new witness sign a specific forward key transition. | [L47](../../../src/mirrormind/modules/evidence/authority_transcript.py#L47) |
| `AuthorityTranscriptAssessment` | class | `class AuthorityTranscriptAssessment` | Non-authorizing result of a locally supplied and matched transcript. | [L61](../../../src/mirrormind/modules/evidence/authority_transcript.py#L61) |
| `AuthorityTranscriptAssessment.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Output only non-sensitive receipt metadata and blocked permissions. | [L70](../../../src/mirrormind/modules/evidence/authority_transcript.py#L70) |
| `_canonical_authority_receipt_message` | function | `def _canonical_authority_receipt_message(receipt: SignedAuthorityReceipt) -> bytes` | Separate signature domain from both review decisions and checkpoints. | [L86](../../../src/mirrormind/modules/evidence/authority_transcript.py#L86) |
| `_canonical_handoff_message` | function | `def _canonical_handoff_message(handoff: WitnessKeyHandoff) -> bytes` | Bind old/new witness keys to the exact predecessor and next sequence. | [L101](../../../src/mirrormind/modules/evidence/authority_transcript.py#L101) |
| `_verify_signature` | function | `def _verify_signature(public_key: bytes, signature: str, message: bytes) -> None` | Check one signature without leaking keys or caller-supplied text. | [L115](../../../src/mirrormind/modules/evidence/authority_transcript.py#L115) |
| `_keys_valid` | function | `def _keys_valid(keys: Mapping[str, bytes]) -> bool` | — | [L130](../../../src/mirrormind/modules/evidence/authority_transcript.py#L130) |
| `verify_authority_transcript` | function | `def verify_authority_transcript(registry: SQLiteReviewRegistry, packet: SourceReviewPacket, receipts: tuple[SignedAuthorityReceipt, ...], handoffs: tuple[WitnessKeyHandoff, ...], *, trusted_checkpoint_keys: Mapping[str, bytes], trusted_witness_keys: Mapping[str, bytes], previous_sequence: int, previous_receipt_sha256: str, previous_witness_key_id: str, previous_key_epoch: int, expected_current_sequence: int, expected_current_receipt_sha256: str, checked_on: date) -> AuthorityTranscriptAssessment` | Reject non-contiguous or conflicting witnessed history and unsafe rotation. | [L142](../../../src/mirrormind/modules/evidence/authority_transcript.py#L142) |

## `mirrormind.modules.evidence.head_checkpoints`

Source: [`src/mirrormind/modules/evidence/head_checkpoints.py`](../../../src/mirrormind/modules/evidence/head_checkpoints.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hmac`, `json`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.review_decisions`, `mirrormind.modules.evidence.sqlite_review_registry`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedReviewHeadCheckpoint` | class | `class SignedReviewHeadCheckpoint` | External signer's attestation of one exact packet's review log head. | [L30](../../../src/mirrormind/modules/evidence/head_checkpoints.py#L30) |
| `CheckpointComparison` | class | `class CheckpointComparison` | Identifier-minimized verification result; never an access-control token. | [L47](../../../src/mirrormind/modules/evidence/head_checkpoints.py#L47) |
| `CheckpointComparison.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Avoid leaking private record/key identifiers or implying authorization. | [L56](../../../src/mirrormind/modules/evidence/head_checkpoints.py#L56) |
| `_canonical_checkpoint_message` | function | `def _canonical_checkpoint_message(checkpoint: SignedReviewHeadCheckpoint) -> bytes` | Domain-separated, versioned bytes to be signed by the EXTERNAL authority. | [L72](../../../src/mirrormind/modules/evidence/head_checkpoints.py#L72) |
| `verify_signed_head_checkpoint` | function | `def verify_signed_head_checkpoint(packet: SourceReviewPacket, checkpoint: SignedReviewHeadCheckpoint, *, trusted_anchor_keys: Mapping[str, bytes], minimum_anchor_sequence: int, checked_on: date) -> None` | Verify metadata and signature against caller-supplied trust + high-water. | [L90](../../../src/mirrormind/modules/evidence/head_checkpoints.py#L90) |
| `compare_sqlite_to_signed_checkpoint` | function | `def compare_sqlite_to_signed_checkpoint(registry: SQLiteReviewRegistry, packet: SourceReviewPacket, checkpoint: SignedReviewHeadCheckpoint, *, trusted_anchor_keys: Mapping[str, bytes], minimum_anchor_sequence: int, checked_on: date) -> CheckpointComparison` | Check a verified signed head against the SAME atomic SQLite snapshot. | [L175](../../../src/mirrormind/modules/evidence/head_checkpoints.py#L175) |

## `mirrormind.modules.evidence.intake_review`

Source: [`src/mirrormind/modules/evidence/intake_review.py`](../../../src/mirrormind/modules/evidence/intake_review.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.domains.retail.uci_workbook`, `mirrormind.modules.evidence.snapshots`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SourceReviewDeclaration` | class | `class SourceReviewDeclaration` | Human-supplied review references; not authenticated permissions. | [L25](../../../src/mirrormind/modules/evidence/intake_review.py#L25) |
| `SourceReviewPacket` | class | `class SourceReviewPacket` | Identifier-minimized metadata for an external human reviewer. | [L41](../../../src/mirrormind/modules/evidence/intake_review.py#L41) |
| `SourceReviewPacket.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Expose a non-authorizing summary, never input rows or references. | [L54](../../../src/mirrormind/modules/evidence/intake_review.py#L54) |
| `prepare_source_review_packet` | function | `def prepare_source_review_packet(staged: StagedSnapshot \| UciWorkbookReadResult, declaration: SourceReviewDeclaration, *, inspected_on: date) -> SourceReviewPacket` | Bind a staged digest to unverified review declarations without approval. | [L77](../../../src/mirrormind/modules/evidence/intake_review.py#L77) |

## `mirrormind.modules.evidence.integrated_fence_transcript`

Source: [`src/mirrormind/modules/evidence/integrated_fence_transcript.py`](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hmac`, `json`, `mirrormind.modules.evidence.atomic_governed_publisher`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.integrated_head_fence`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedIntegratedFenceTransition` | class | `class SignedIntegratedFenceTransition` | Two witnesses endorse the exact successor of an authority-signed fence. | [L35](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L35) |
| `IntegratedFenceTranscriptAssessment` | class | `class IntegratedFenceTranscriptAssessment` | Caller-pinned chain agrees with local heads; NOT an authorization token. | [L47](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L47) |
| `IntegratedFenceTranscriptAssessment.receipt` | method | `def receipt(self) -> dict[str, int \| str \| bool]` | — | [L56](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L56) |
| `SuppliedFenceForkEvidence` | class | `class SuppliedFenceForkEvidence` | Two verified signed successors conflict; neither is selected as current. | [L73](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L73) |
| `SuppliedFenceForkEvidence.receipt` | method | `def receipt(self) -> dict[str, int \| str \| bool]` | — | [L83](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L83) |
| `_canonical_fence_transition_message` | function | `def _canonical_fence_transition_message(link: SignedIntegratedFenceTransition) -> bytes` | Both witness signatures cover the same immutable canonical message. | [L98](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L98) |
| `_validate_rosters` | function | `def _validate_rosters(trusted_fence_keys: Mapping[str, bytes], trusted_witness_keys: Mapping[str, bytes]) -> None` | — | [L138](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L138) |
| `_verify_one_transition` | function | `def _verify_one_transition(link: SignedIntegratedFenceTransition, packet: SourceReviewPacket, *, trusted_fence_keys: Mapping[str, bytes], trusted_witness_keys: Mapping[str, bytes], checked_on: date) -> str` | — | [L163](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L163) |
| `verify_integrated_fence_transcript` | function | `def verify_integrated_fence_transcript(gate: AtomicGovernedPublisher, packet: SourceReviewPacket, transitions: tuple[SignedIntegratedFenceTransition, ...], *, trusted_fence_keys: Mapping[str, bytes], trusted_witness_keys: Mapping[str, bytes], anchor_authority_sequence: int, anchor_fence_sha256: str, expected_current_authority_sequence: int, expected_current_fence_sha256: str, checked_on: date) -> IntegratedFenceTranscriptAssessment` | Verify caller-pinned consecutive two-witness links and terminal SQLite heads. | [L203](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L203) |
| `classify_supplied_fence_fork` | function | `def classify_supplied_fence_fork(packet: SourceReviewPacket, first: SignedIntegratedFenceTransition, second: SignedIntegratedFenceTransition, *, trusted_fence_keys: Mapping[str, bytes], trusted_witness_keys: Mapping[str, bytes], checked_on: date) -> SuppliedFenceForkEvidence` | Classify only two supplied valid incompatible successors; do not select a head. | [L293](../../../src/mirrormind/modules/evidence/integrated_fence_transcript.py#L293) |

## `mirrormind.modules.evidence.integrated_head_fence`

Source: [`src/mirrormind/modules/evidence/integrated_head_fence.py`](../../../src/mirrormind/modules/evidence/integrated_head_fence.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.atomic_governed_publisher`, `mirrormind.modules.evidence.intake_review`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedIntegratedHeadFence` | class | `class SignedIntegratedHeadFence` | Signer-supplied exact local policy and per-packet publication state. | [L30](../../../src/mirrormind/modules/evidence/integrated_head_fence.py#L30) |
| `IntegratedHeadFenceAssessment` | class | `class IntegratedHeadFenceAssessment` | Read-only local equality result; NEVER an authorization token. | [L47](../../../src/mirrormind/modules/evidence/integrated_head_fence.py#L47) |
| `IntegratedHeadFenceAssessment.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Return only identifier-minimized consistency and permission fields. | [L56](../../../src/mirrormind/modules/evidence/integrated_head_fence.py#L56) |
| `_canonical_fence_message` | function | `def _canonical_fence_message(fence: SignedIntegratedHeadFence) -> bytes` | Canonical message in a domain distinct from review and publish roles. | [L72](../../../src/mirrormind/modules/evidence/integrated_head_fence.py#L72) |
| `_fence_sha256` | function | `def _fence_sha256(fence: SignedIntegratedHeadFence) -> str` | Hash the canonical payload AND actual Ed25519 signature bytes. | [L114](../../../src/mirrormind/modules/evidence/integrated_head_fence.py#L114) |
| `verify_integrated_head_fence` | function | `def verify_integrated_head_fence(gate: AtomicGovernedPublisher, packet: SourceReviewPacket, fence: SignedIntegratedHeadFence, *, trusted_fence_keys: Mapping[str, bytes], expected_current_authority_sequence: int, expected_current_fence_sha256: str, checked_on: date) -> IntegratedHeadFenceAssessment` | Check supplied signed heads against one consistent local SQLite snapshot. | [L122](../../../src/mirrormind/modules/evidence/integrated_head_fence.py#L122) |

## `mirrormind.modules.evidence.local_checkpoint_publisher`

Source: [`src/mirrormind/modules/evidence/local_checkpoint_publisher.py`](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.authority_transcript`, `mirrormind.modules.evidence.head_checkpoints`, `mirrormind.modules.evidence.intake_review`, `pathlib`, `re`, `sqlite3`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedPublicationCommand` | class | `class SignedPublicationCommand` | Operator authorization of a single exact proposed witness receipt. | [L45](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L45) |
| `LocalPublicationRevision` | class | `class LocalPublicationRevision` | Sanitized local state, NOT an externally witnessed current head. | [L60](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L60) |
| `LocalPublicationRevision.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | — | [L69](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L69) |
| `_receipt_digest` | function | `def _receipt_digest(receipt: SignedAuthorityReceipt) -> str` | Exactly the existing witness-transcript receipt hashing convention. | [L84](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L84) |
| `_canonical_publication_message` | function | `def _canonical_publication_message(command: SignedPublicationCommand) -> bytes` | Distinct operator signing domain, binding witness and handoff signatures. | [L92](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L92) |
| `_serialize` | function | `def _serialize(command: SignedPublicationCommand) -> str` | — | [L116](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L116) |
| `_decode` | function | `def _decode(data: str) -> SignedPublicationCommand` | Decode only exact canonical records; never execute or deserialize objects. | [L164](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L164) |
| `_packet_json` | function | `def _packet_json(packet: SourceReviewPacket) -> str` | — | [L189](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L189) |
| `LocalCheckpointPublisher` | class | `class LocalCheckpointPublisher` | Local DB with configured operator-key admission and atomic per-packet CAS. | [L207](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L207) |
| `LocalCheckpointPublisher.__init__` | method | `def __init__(self, path: Path, *, checkpoint_keys: Mapping[str, bytes], witness_keys: Mapping[str, bytes], operator_keys: Mapping[str, bytes], initial_witness_key_id: str, create: bool=False) -> None` | — | [L214](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L214) |
| `LocalCheckpointPublisher._connect` | method | `def _connect(self) -> sqlite3.Connection` | — | [L296](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L296) |
| `LocalCheckpointPublisher._schema` | method | `def _schema(self, db: sqlite3.Connection) -> None` | — | [L308](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L308) |
| `LocalCheckpointPublisher._verify_event` | method | `def _verify_event(self, packet: SourceReviewPacket, command: SignedPublicationCommand, *, sequence: int, previous_hash: str, previous_witness: str, previous_epoch: int, previous_revision: int, previous_review_head: str \| None, previous_issue: date) -> tuple[str, str, int, int, str, date]` | — | [L329](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L329) |
| `LocalCheckpointPublisher._load` | method | `def _load(self, db: sqlite3.Connection, packet: SourceReviewPacket) -> tuple[int, str, str, int, int, str \| None, date, date \| None]` | — | [L426](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L426) |
| `LocalCheckpointPublisher.snapshot` | method | `def snapshot(self, packet: SourceReviewPacket, *, checked_on: date, externally_expected_head_sha256: str \| None=None) -> LocalPublicationRevision` | Recheck full local signed history; external head may detect rollback. | [L483](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L483) |
| `LocalCheckpointPublisher.publish` | method | `def publish(self, packet: SourceReviewPacket, command: SignedPublicationCommand, *, expected_sequence: int, expected_receipt_sha256: str, checked_on: date) -> LocalPublicationRevision` | Verify exact operator-signed proposal, then atomically commit. | [L514](../../../src/mirrormind/modules/evidence/local_checkpoint_publisher.py#L514) |

## `mirrormind.modules.evidence.local_integrated_fence_registry`

Source: [`src/mirrormind/modules/evidence/local_integrated_fence_registry.py`](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.atomic_governed_publisher`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.integrated_fence_transcript`, `mirrormind.modules.evidence.integrated_head_fence`, `pathlib`, `re`, `sqlite3`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `LocalFenceRegistryHead` | class | `class LocalFenceRegistryHead` | Replayed registry head, NOT a permission or independent timestamp. | [L39](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L39) |
| `LocalFenceRegistryHead.receipt` | method | `def receipt(self) -> dict[str, int \| str \| bool \| None]` | — | [L48](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L48) |
| `_dump_link` | function | `def _dump_link(link: SignedIntegratedFenceTransition) -> str` | Deterministic bounded JSON of complete signed payload, not just heads. | [L63](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L63) |
| `_load_link` | function | `def _load_link(serialized: str) -> SignedIntegratedFenceTransition` | Strictly parse one stored canonical transition; refuse extra/missing fields. | [L78](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L78) |
| `LocalIntegratedFenceRegistry` | class | `class LocalIntegratedFenceRegistry` | CAS-persist one packet's witnessed fence chain in a distinct SQLite file. | [L123](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L123) |
| `LocalIntegratedFenceRegistry.__init__` | method | `def __init__(self, path: Path, gate: AtomicGovernedPublisher, packet: SourceReviewPacket, *, trusted_fence_keys: Mapping[str, bytes], trusted_witness_keys: Mapping[str, bytes], create: bool=False) -> None` | — | [L131](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L131) |
| `LocalIntegratedFenceRegistry._connect` | method | `def _connect(self) -> sqlite3.Connection` | — | [L214](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L214) |
| `LocalIntegratedFenceRegistry._verify_schema` | method | `def _verify_schema(self, db: sqlite3.Connection) -> None` | — | [L217](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L217) |
| `LocalIntegratedFenceRegistry._replay` | method | `def _replay(self, db: sqlite3.Connection, checked_on: date) -> tuple[LocalFenceRegistryHead, tuple[SignedIntegratedFenceTransition, ...]]` | — | [L227](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L227) |
| `LocalIntegratedFenceRegistry.head` | method | `def head(self, *, checked_on: date) -> LocalFenceRegistryHead` | Read and verify all signed stored links, without trusting publisher DB. | [L289](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L289) |
| `LocalIntegratedFenceRegistry.compare_local` | method | `def compare_local(self, *, checked_on: date) -> LocalFenceRegistryHead` | Fail when governed publisher differs from verified separately stored pin. | [L308](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L308) |
| `LocalIntegratedFenceRegistry.append` | method | `def append(self, link: SignedIntegratedFenceTransition, *, expected_authority_sequence: int, expected_fence_sha256: str, checked_on: date) -> LocalFenceRegistryHead` | Commit a next doubly witnessed fence with registry-local BEGIN IMMEDIATE. | [L341](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L341) |
| `_fence_digest` | function | `def _fence_digest(link: SignedIntegratedFenceTransition) -> str` | — | [L404](../../../src/mirrormind/modules/evidence/local_integrated_fence_registry.py#L404) |

## `mirrormind.modules.evidence.local_review_registry`

Source: [`src/mirrormind/modules/evidence/local_review_registry.py`](../../../src/mirrormind/modules/evidence/local_review_registry.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.review_decisions`, `re`, `threading`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `LocalReviewRevision` | class | `class LocalReviewRevision` | Identifier-minimized snapshot; not a source authorization token. | [L31](../../../src/mirrormind/modules/evidence/local_review_registry.py#L31) |
| `LocalReviewRevision.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Return only local revision metadata and explicitly blocked permissions. | [L39](../../../src/mirrormind/modules/evidence/local_review_registry.py#L39) |
| `LocalReviewRegistry` | class | `class LocalReviewRegistry` | Atomic in-process append on a signed chain with expected revision and head. | [L55](../../../src/mirrormind/modules/evidence/local_review_registry.py#L55) |
| `LocalReviewRegistry.__init__` | method | `def __init__(self, trusted_reviewer_keys: Mapping[str, bytes]) -> None` | — | [L63](../../../src/mirrormind/modules/evidence/local_review_registry.py#L63) |
| `LocalReviewRegistry._current` | method | `def _current(self, packet: SourceReviewPacket) -> tuple[tuple[SignedReviewDecision, ...], str]` | — | [L81](../../../src/mirrormind/modules/evidence/local_review_registry.py#L81) |
| `LocalReviewRegistry.snapshot` | method | `def snapshot(self, packet: SourceReviewPacket, *, checked_on: date) -> LocalReviewRevision` | Inspect current in-process history; a snapshot is not a trusted fresh head. | [L98](../../../src/mirrormind/modules/evidence/local_review_registry.py#L98) |
| `LocalReviewRegistry.append` | method | `def append(self, packet: SourceReviewPacket, event: SignedReviewDecision, *, expected_revision: int, expected_head_sha256: str, checked_on: date) -> LocalReviewRevision` | Atomically append one signed event, rejecting stale or revoked writers. | [L114](../../../src/mirrormind/modules/evidence/local_review_registry.py#L114) |

## `mirrormind.modules.evidence.operator_governance`

Source: [`src/mirrormind/modules/evidence/operator_governance.py`](../../../src/mirrormind/modules/evidence/operator_governance.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `pathlib`, `re`, `sqlite3`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedOperatorPolicyEvent` | class | `class SignedOperatorPolicyEvent` | Enrollment/revocation attested by two separate configured admins. | [L31](../../../src/mirrormind/modules/evidence/operator_governance.py#L31) |
| `OperatorPolicyRevision` | class | `class OperatorPolicyRevision` | Local policy head; cannot be used to authorize publication. | [L47](../../../src/mirrormind/modules/evidence/operator_governance.py#L47) |
| `OperatorPolicyRevision.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | — | [L55](../../../src/mirrormind/modules/evidence/operator_governance.py#L55) |
| `OperatorPolicyAssessment` | class | `class OperatorPolicyAssessment` | A record status, NOT a valid permission to publish or ingest. | [L71](../../../src/mirrormind/modules/evidence/operator_governance.py#L71) |
| `OperatorPolicyAssessment.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | — | [L79](../../../src/mirrormind/modules/evidence/operator_governance.py#L79) |
| `_canonical_event_message` | function | `def _canonical_event_message(event: SignedOperatorPolicyEvent) -> bytes` | Domain-separated signable fields; signatures not included. | [L93](../../../src/mirrormind/modules/evidence/operator_governance.py#L93) |
| `_validate_event` | function | `def _validate_event(event: SignedOperatorPolicyEvent) -> None` | — | [L109](../../../src/mirrormind/modules/evidence/operator_governance.py#L109) |
| `_serialize` | function | `def _serialize(event: SignedOperatorPolicyEvent) -> str` | — | [L144](../../../src/mirrormind/modules/evidence/operator_governance.py#L144) |
| `_decode` | function | `def _decode(raw: str) -> SignedOperatorPolicyEvent` | No dynamic deserialization; reject noncanonical and huge records. | [L152](../../../src/mirrormind/modules/evidence/operator_governance.py#L152) |
| `_verify_admin_signature` | function | `def _verify_admin_signature(public: bytes, signature: str, message: bytes) -> None` | — | [L170](../../../src/mirrormind/modules/evidence/operator_governance.py#L170) |
| `LocalOperatorGovernance` | class | `class LocalOperatorGovernance` | Single-local-database CAS of dual-admin signed key policy events. | [L184](../../../src/mirrormind/modules/evidence/operator_governance.py#L184) |
| `LocalOperatorGovernance.__init__` | method | `def __init__(self, path: Path, *, administrator_public_keys: Mapping[str, bytes], create: bool=False) -> None` | — | [L192](../../../src/mirrormind/modules/evidence/operator_governance.py#L192) |
| `LocalOperatorGovernance._connect` | method | `def _connect(self) -> sqlite3.Connection` | — | [L266](../../../src/mirrormind/modules/evidence/operator_governance.py#L266) |
| `LocalOperatorGovernance._check_schema` | method | `def _check_schema(self, connection: sqlite3.Connection) -> None` | — | [L279](../../../src/mirrormind/modules/evidence/operator_governance.py#L279) |
| `LocalOperatorGovernance._read` | method | `def _read(self, connection: sqlite3.Connection) -> tuple[int, str, dict[str, tuple[str, date, bool]], date \| None]` | — | [L295](../../../src/mirrormind/modules/evidence/operator_governance.py#L295) |
| `LocalOperatorGovernance._evaluate` | method | `def _evaluate(self, event: SignedOperatorPolicyEvent, *, expected_sequence: int, previous_head: str, previous_date: date \| None, history: dict[str, tuple[str, date, bool]], used_material: set[str]) -> tuple[str, date]` | — | [L328](../../../src/mirrormind/modules/evidence/operator_governance.py#L328) |
| `LocalOperatorGovernance._check_external_head` | method | `def _check_external_head(head: str, expected: str \| None) -> None` | — | [L389](../../../src/mirrormind/modules/evidence/operator_governance.py#L389) |
| `LocalOperatorGovernance.snapshot` | method | `def snapshot(self, *, checked_on: date, externally_expected_head_sha256: str \| None=None) -> OperatorPolicyRevision` | — | [L397](../../../src/mirrormind/modules/evidence/operator_governance.py#L397) |
| `LocalOperatorGovernance.assess_operator` | method | `def assess_operator(self, operator_key_id: str, operator_public_key: bytes, *, checked_on: date, externally_expected_head_sha256: str \| None=None) -> OperatorPolicyAssessment` | — | [L423](../../../src/mirrormind/modules/evidence/operator_governance.py#L423) |
| `LocalOperatorGovernance.append` | method | `def append(self, event: SignedOperatorPolicyEvent, *, expected_revision: int, expected_head_sha256: str, checked_on: date) -> OperatorPolicyRevision` | — | [L466](../../../src/mirrormind/modules/evidence/operator_governance.py#L466) |

## `mirrormind.modules.evidence.remote_fence_head_client`

Source: [`src/mirrormind/modules/evidence/remote_fence_head_client.py`](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `mirrormind.modules.evidence.local_integrated_fence_registry`, `mirrormind.modules.evidence.remote_fence_head_protocol`, `secrets`, `ssl`, `urllib.error`, `urllib.request`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RemoteHeadComparison` | class | `class RemoteHeadComparison` | Local equality to an authenticated fresh reply, not source authorization. | [L51](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L51) |
| `RemoteHeadComparison.receipt` | method | `def receipt(self) -> dict[str, int \| str \| bool]` | — | [L59](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L59) |
| `_validate_remote_keys` | function | `def _validate_remote_keys(registry: LocalIntegratedFenceRegistry, trusted_service_keys: Mapping[str, bytes]) -> None` | — | [L74](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L74) |
| `verify_challenged_remote_head` | function | `def verify_challenged_remote_head(registry: LocalIntegratedFenceRegistry, raw_response: bytes, *, requested_nonce_hex: str, service_id: str, endpoint: str, trusted_service_keys: Mapping[str, bytes], checked_at: datetime) -> RemoteHeadComparison` | Verify a supplied online reply and compare against signed local heads. | [L98](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L98) |
| `_NoRedirect` | class | `class _NoRedirect` | — | [L164](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L164) |
| `_NoRedirect.redirect_request` | method | `def redirect_request(self, request: object, file: object, code: object, message: object, headers: object, new_url: object) -> None` | — | [L165](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L165) |
| `_https_read` | function | `def _https_read(endpoint: str, nonce_hex: str, packet_sha256: str) -> bytes` | Strict HTTPS GET, system CA chain, no redirects/proxies, bounded body. | [L172](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L172) |
| `fetch_and_compare_remote_head` | function | `def fetch_and_compare_remote_head(registry: LocalIntegratedFenceRegistry, *, endpoint: str, service_id: str, trusted_service_keys: Mapping[str, bytes]) -> RemoteHeadComparison` | Opt-in network query. A response signature does not prove true latest state. | [L199](../../../src/mirrormind/modules/evidence/remote_fence_head_client.py#L199) |

## `mirrormind.modules.evidence.remote_fence_head_protocol`

Source: [`src/mirrormind/modules/evidence/remote_fence_head_protocol.py`](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `ipaddress`, `json`, `re`, `urllib.parse`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedRemoteFenceHead` | class | `class SignedRemoteFenceHead` | Remote service signature over one challenge-bound claimed current head. | [L31](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py#L31) |
| `_utc` | function | `def _utc(raw: str) -> datetime` | — | [L47](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py#L47) |
| `_valid_endpoint` | function | `def _valid_endpoint(endpoint: str) -> None` | Avoid arbitrary URLs: an explicit fixed path, canonical public DNS, TLS. | [L56](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py#L56) |
| `_canonical_remote_message` | function | `def _canonical_remote_message(head: SignedRemoteFenceHead) -> bytes` | All signed fields in a protocol-specific domain excluding signature. | [L82](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py#L82) |
| `_signed_wire` | function | `def _signed_wire(head: SignedRemoteFenceHead) -> bytes` | Canonical complete signed JSON response; no raw source data. | [L123](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py#L123) |
| `_parse_signed_response` | function | `def _parse_signed_response(raw: bytes) -> SignedRemoteFenceHead` | — | [L128](../../../src/mirrormind/modules/evidence/remote_fence_head_protocol.py#L128) |

## `mirrormind.modules.evidence.remote_fence_head_service`

Source: [`src/mirrormind/modules/evidence/remote_fence_head_service.py`](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `cryptography.hazmat.primitives.serialization`, `dataclasses`, `datetime`, `mirrormind.modules.evidence.remote_fence_head_protocol`, `re`, `types`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `CurrentRemoteFenceHead` | class | `class CurrentRemoteFenceHead` | One store-supplied claim; it contains digests, never source payloads. | [L34](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L34) |
| `RemoteFenceHeadStoreError` | class | `class RemoteFenceHeadStoreError` | A store adapter cannot safely provide the requested current record. | [L43](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L43) |
| `RemoteFenceHeadClockError` | class | `class RemoteFenceHeadClockError` | A clock adapter cannot safely provide the requested UTC instant. | [L47](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L47) |
| `RemoteFenceHeadStore` | class | `class RemoteFenceHeadStore` | Read contract for a future separately implemented current-head store. | [L51](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L51) |
| `RemoteFenceHeadStore.read_current` | method | `def read_current(self, packet_sha256: str) -> CurrentRemoteFenceHead \| None` | Return the claimed head or raise ``RemoteFenceHeadStoreError``. | [L61](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L61) |
| `RemoteFenceHeadRequest` | class | `class RemoteFenceHeadRequest` | Minimal decoded request fields consumed by the responder. | [L66](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L66) |
| `RemoteFenceHeadResponse` | class | `class RemoteFenceHeadResponse` | Transport-neutral status, headers and bounded response bytes. | [L76](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L76) |
| `RemoteFenceHeadResponse.__post_init__` | method | `def __post_init__(self) -> None` | — | [L83](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L83) |
| `RemoteFenceHeadResponder` | class | `class RemoteFenceHeadResponder` | Sign one fixed-path nonce challenge from a typed current-head store. | [L87](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L87) |
| `RemoteFenceHeadResponder.__init__` | method | `def __init__(self, *, service_id: str, service_key_id: str, endpoint: str, signing_key: object, non_service_public_keys: Mapping[str, bytes], store: RemoteFenceHeadStore, clock: Callable[[], datetime], ttl_seconds: int=60) -> None` | — | [L106](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L106) |
| `RemoteFenceHeadResponder.respond` | method | `def respond(self, request: RemoteFenceHeadRequest) -> RemoteFenceHeadResponse` | Return one canonical signed response, or a bodyless generic failure. | [L169](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L169) |
| `_empty_response` | function | `def _empty_response(status_code: int, *, allow_get: bool=False) -> RemoteFenceHeadResponse` | — | [L250](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L250) |

## `mirrormind.modules.evidence.review_decisions`

Source: [`src/mirrormind/modules/evidence/review_decisions.py`](../../../src/mirrormind/modules/evidence/review_decisions.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `cryptography.exceptions`, `cryptography.hazmat.primitives.asymmetric.ed25519`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.intake_review`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `SignedReviewDecision` | class | `class SignedReviewDecision` | Externally signed metadata; must not originate from the intake requester. | [L27](../../../src/mirrormind/modules/evidence/review_decisions.py#L27) |
| `ReviewHistoryAssessment` | class | `class ReviewHistoryAssessment` | Non-authorizing, identifier-minimized result of signature/log verification. | [L45](../../../src/mirrormind/modules/evidence/review_decisions.py#L45) |
| `ReviewHistoryAssessment.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Expose a signed-review status, never source or reviewer references. | [L53](../../../src/mirrormind/modules/evidence/review_decisions.py#L53) |
| `_canonical_review_message` | function | `def _canonical_review_message(event: SignedReviewDecision) -> bytes` | Encode the exact v1 review record for external Ed25519 signature verification. | [L73](../../../src/mirrormind/modules/evidence/review_decisions.py#L73) |
| `verify_review_history` | function | `def verify_review_history(packet: SourceReviewPacket, events: tuple[SignedReviewDecision, ...], *, trusted_reviewer_keys: Mapping[str, bytes], expected_head_sha256: str, checked_on: date) -> ReviewHistoryAssessment` | Verify offline Ed25519 review events and fail closed on revoked/expired records. | [L92](../../../src/mirrormind/modules/evidence/review_decisions.py#L92) |

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

## `mirrormind.modules.evidence.sqlite_review_registry`

Source: [`src/mirrormind/modules/evidence/sqlite_review_registry.py`](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.review_decisions`, `pathlib`, `re`, `sqlite3`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_json` | function | `def _json(data: dict[str, object]) -> str` | — | [L35](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L35) |
| `_packet_json` | function | `def _packet_json(packet: SourceReviewPacket) -> str` | — | [L39](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L39) |
| `_event_json` | function | `def _event_json(event: SignedReviewDecision) -> str` | — | [L57](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L57) |
| `_parse_event` | function | `def _parse_event(serialized: str) -> SignedReviewDecision` | Fail closed on unexpected or rewritten persisted event encodings. | [L72](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L72) |
| `SQLiteReviewRevision` | class | `class SQLiteReviewRevision` | Non-authorizing local snapshot of the stored signed history. | [L90](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L90) |
| `SQLiteReviewRevision.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Report integrity status without exposing any source or reviewer IDs. | [L98](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L98) |
| `SQLiteReviewRegistry` | class | `class SQLiteReviewRegistry` | Per-packet signed event log using SQLite BEGIN IMMEDIATE transactions. | [L114](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L114) |
| `SQLiteReviewRegistry.__init__` | method | `def __init__(self, db_path: Path, trusted_reviewer_keys: Mapping[str, bytes], *, create: bool=False) -> None` | — | [L122](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L122) |
| `SQLiteReviewRegistry._connection` | method | `def _connection(self) -> sqlite3.Connection` | — | [L187](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L187) |
| `SQLiteReviewRegistry._validate_schema` | method | `def _validate_schema(connection: sqlite3.Connection) -> None` | — | [L200](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L200) |
| `SQLiteReviewRegistry._load` | method | `def _load(connection: sqlite3.Connection, packet: SourceReviewPacket) -> tuple[tuple[SignedReviewDecision, ...], str]` | — | [L212](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L212) |
| `SQLiteReviewRegistry.snapshot` | method | `def snapshot(self, packet: SourceReviewPacket, *, checked_on: date, externally_expected_head_sha256: str \| None=None) -> SQLiteReviewRevision` | Verify stored signatures, with optional *independent* rollback anchor. | [L243](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L243) |
| `SQLiteReviewRegistry.append` | method | `def append(self, packet: SourceReviewPacket, event: SignedReviewDecision, *, expected_revision: int, expected_head_sha256: str, checked_on: date) -> SQLiteReviewRevision` | Atomically compare the current stored head and append a signed event. | [L275](../../../src/mirrormind/modules/evidence/sqlite_review_registry.py#L275) |

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
| `project_seasonal_naive_lag7` | function | `def project_seasonal_naive_lag7(last_seven: tuple[int, ...], *, horizon_days: int) -> tuple[int, ...]` | Project the fixed lag-seven baseline over a bounded integer horizon. | [L40](../../../src/mirrormind/modules/forecasting/baselines.py#L40) |
| `_score` | function | `def _score(forecasts: tuple[float, ...], actuals: tuple[int, ...]) -> dict[str, float \| None]` | Return matched MAE/RMSE/signed bias and undefined-zero WAPE as None. | [L65](../../../src/mirrormind/modules/forecasting/baselines.py#L65) |
| `backtest_staged_snapshot` | function | `def backtest_staged_snapshot(snapshot: StagedSnapshot, *, series_id: str, evaluation_on: str, holdout_days: int=7, min_history_days: int=14) -> dict[str, object]` | Evaluate fixed daily origins only with data published before each origin. | [L80](../../../src/mirrormind/modules/forecasting/baselines.py#L80) |

## `mirrormind.modules.retrieval.__init__`

Source: [`src/mirrormind/modules/retrieval/__init__.py`](../../../src/mirrormind/modules/retrieval/__init__.py)

Static imports (including inside functions): `mirrormind.modules.retrieval.contracts`, `mirrormind.modules.retrieval.evaluation`, `mirrormind.modules.retrieval.index`

No top-level classes or functions.

## `mirrormind.modules.retrieval.contracts`

Source: [`src/mirrormind/modules/retrieval/contracts.py`](../../../src/mirrormind/modules/retrieval/contracts.py)

Static imports (including inside functions): `__future__`, `hashlib`, `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_RetrievalModel` | class | `class _RetrievalModel` | Share immutable, non-coercing validation across retrieval contracts. | [L32](../../../src/mirrormind/modules/retrieval/contracts.py#L32) |
| `EvidenceDocument` | class | `class EvidenceDocument` | One bounded fictional document with caller-declared visibility scope. | [L38](../../../src/mirrormind/modules/retrieval/contracts.py#L38) |
| `EvidenceDocument.reject_unsafe_controls` | method | `def reject_unsafe_controls(cls, value: str) -> str` | — | [L51](../../../src/mirrormind/modules/retrieval/contracts.py#L51) |
| `EvidenceDocument.require_unique_principals` | method | `def require_unique_principals(cls, value: tuple[str, ...]) -> tuple[str, ...]` | — | [L58](../../../src/mirrormind/modules/retrieval/contracts.py#L58) |
| `EvidenceAccessContext` | class | `class EvidenceAccessContext` | Trusted-caller scope; not an authenticated identity or permission grant. | [L64](../../../src/mirrormind/modules/retrieval/contracts.py#L64) |
| `EvidenceAccessContext.require_unique_collections` | method | `def require_unique_collections(cls, value: tuple[str, ...]) -> tuple[str, ...]` | — | [L72](../../../src/mirrormind/modules/retrieval/contracts.py#L72) |
| `EvidenceQuery` | class | `class EvidenceQuery` | Bounded lexical query and optional subset of caller-visible collections. | [L78](../../../src/mirrormind/modules/retrieval/contracts.py#L78) |
| `EvidenceQuery.normalize_and_bound_text` | method | `def normalize_and_bound_text(cls, value: str) -> str` | — | [L87](../../../src/mirrormind/modules/retrieval/contracts.py#L87) |
| `EvidenceQuery.require_unique_query_collections` | method | `def require_unique_query_collections(cls, value: tuple[str, ...] \| None) -> tuple[str, ...] \| None` | — | [L97](../../../src/mirrormind/modules/retrieval/contracts.py#L97) |
| `EvidenceCitation` | class | `class EvidenceCitation` | Exact source pointer for one excerpt, using Python Unicode code-point offsets. | [L105](../../../src/mirrormind/modules/retrieval/contracts.py#L105) |
| `EvidenceCitation.require_nonempty_span` | method | `def require_nonempty_span(self) -> EvidenceCitation` | — | [L117](../../../src/mirrormind/modules/retrieval/contracts.py#L117) |
| `RetrievedEvidence` | class | `class RetrievedEvidence` | Retrieved text stays explicitly untrusted and carries a verifiable citation. | [L123](../../../src/mirrormind/modules/retrieval/contracts.py#L123) |
| `RetrievedEvidence.require_excerpt_integrity` | method | `def require_excerpt_integrity(self) -> RetrievedEvidence` | — | [L132](../../../src/mirrormind/modules/retrieval/contracts.py#L132) |
| `EvidenceRetrievalResult` | class | `class EvidenceRetrievalResult` | Versioned result envelope; query text and denied-record metadata are omitted. | [L141](../../../src/mirrormind/modules/retrieval/contracts.py#L141) |
| `EvidenceRetrievalResult.match_status_to_hits` | method | `def match_status_to_hits(self) -> EvidenceRetrievalResult` | — | [L149](../../../src/mirrormind/modules/retrieval/contracts.py#L149) |

## `mirrormind.modules.retrieval.evaluation`

Source: [`src/mirrormind/modules/retrieval/evaluation.py`](../../../src/mirrormind/modules/retrieval/evaluation.py)

Static imports (including inside functions): `__future__`, `hashlib`, `mirrormind.modules.retrieval.contracts`, `mirrormind.modules.retrieval.index`, `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_EvaluationModel` | class | `class _EvaluationModel` | Immutable, non-coercing base for local evaluation contracts. | [L32](../../../src/mirrormind/modules/retrieval/evaluation.py#L32) |
| `RetrievalEvaluationCase` | class | `class RetrievalEvaluationCase` | One declared fictional query, caller scope and relevant-document set. | [L38](../../../src/mirrormind/modules/retrieval/evaluation.py#L38) |
| `RetrievalEvaluationCase.require_unique_relevance_labels` | method | `def require_unique_relevance_labels(cls, value: tuple[str, ...]) -> tuple[str, ...]` | — | [L48](../../../src/mirrormind/modules/retrieval/evaluation.py#L48) |
| `RetrievalCaseOutcome` | class | `class RetrievalCaseOutcome` | Query-free case counts and citation refs verified against visible data. | [L54](../../../src/mirrormind/modules/retrieval/evaluation.py#L54) |
| `RetrievalCaseOutcome.require_consistent_counts` | method | `def require_consistent_counts(self) -> RetrievalCaseOutcome` | — | [L70](../../../src/mirrormind/modules/retrieval/evaluation.py#L70) |
| `RetrievalEvaluationReport` | class | `class RetrievalEvaluationReport` | Aggregate retrieval metrics with explicit counts and no query text. | [L88](../../../src/mirrormind/modules/retrieval/evaluation.py#L88) |
| `RetrievalEvaluationReport.require_consistent_aggregate_counts` | method | `def require_consistent_aggregate_counts(self) -> RetrievalEvaluationReport` | — | [L119](../../../src/mirrormind/modules/retrieval/evaluation.py#L119) |
| `run_retrieval_evaluation` | function | `def run_retrieval_evaluation(documents: tuple[EvidenceDocument, ...] \| list[EvidenceDocument], cases: tuple[RetrievalEvaluationCase, ...] \| list[RetrievalEvaluationCase]) -> RetrievalEvaluationReport` | Evaluate a bounded declared test set against the fictional lexical index. | [L139](../../../src/mirrormind/modules/retrieval/evaluation.py#L139) |
| `_is_visible` | function | `def _is_visible(document: EvidenceDocument, case: RetrievalEvaluationCase) -> bool` | Apply both caller-declared access and requested collection scope. | [L289](../../../src/mirrormind/modules/retrieval/evaluation.py#L289) |
| `_matches_document_lineage` | function | `def _matches_document_lineage(citation: EvidenceCitation, document: EvidenceDocument) -> bool` | Check that a citation names the exact visible fixture and snapshot. | [L301](../../../src/mirrormind/modules/retrieval/evaluation.py#L301) |
| `_citation_is_supported` | function | `def _citation_is_supported(excerpt: str, citation: EvidenceCitation, document: EvidenceDocument) -> bool` | Verify lineage, code-point span, exact excerpt and UTF-8 digest. | [L313](../../../src/mirrormind/modules/retrieval/evaluation.py#L313) |
| `_rate` | function | `def _rate(numerator: int, denominator: int) -> float \| None` | Return a stable six-decimal descriptive rate or null if undefined. | [L327](../../../src/mirrormind/modules/retrieval/evaluation.py#L327) |

## `mirrormind.modules.retrieval.fictional_fixture`

Source: [`src/mirrormind/modules/retrieval/fictional_fixture.py`](../../../src/mirrormind/modules/retrieval/fictional_fixture.py)

Static imports (including inside functions): `mirrormind.modules.retrieval.contracts`, `mirrormind.modules.retrieval.evaluation`, `mirrormind.modules.retrieval.index`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `fictional_documents` | function | `def fictional_documents() -> tuple[EvidenceDocument, ...]` | Return small, deterministic documents with disjoint fictional scopes. | [L16](../../../src/mirrormind/modules/retrieval/fictional_fixture.py#L16) |
| `build_fictional_index` | function | `def build_fictional_index() -> InMemoryEvidenceIndex` | Build the CLI's fixed fictional scope; this is not an auth mechanism. | [L68](../../../src/mirrormind/modules/retrieval/fictional_fixture.py#L68) |
| `fictional_evaluation_cases` | function | `def fictional_evaluation_cases() -> tuple[RetrievalEvaluationCase, ...]` | Return a fixed query set with relevant, no-match and denied cases. | [L77](../../../src/mirrormind/modules/retrieval/fictional_fixture.py#L77) |

## `mirrormind.modules.retrieval.index`

Source: [`src/mirrormind/modules/retrieval/index.py`](../../../src/mirrormind/modules/retrieval/index.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `hashlib`, `math`, `mirrormind.modules.retrieval.contracts`, `re`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_TokenSpan` | class | `class _TokenSpan` | — | [L27](../../../src/mirrormind/modules/retrieval/index.py#L27) |
| `_IndexedDocument` | class | `class _IndexedDocument` | — | [L34](../../../src/mirrormind/modules/retrieval/index.py#L34) |
| `_token_spans` | function | `def _token_spans(text: str) -> tuple[_TokenSpan, ...]` | Tokenize Unicode words while retaining exact source offsets. | [L40](../../../src/mirrormind/modules/retrieval/index.py#L40) |
| `InMemoryEvidenceIndex` | class | `class InMemoryEvidenceIndex` | A read-only index containing only records visible to its build context. | [L49](../../../src/mirrormind/modules/retrieval/index.py#L49) |
| `InMemoryEvidenceIndex.build` | method | `def build(cls, documents: tuple[EvidenceDocument, ...] \| list[EvidenceDocument], access: EvidenceAccessContext) -> InMemoryEvidenceIndex` | Filter scope first, then tokenize only documents caller may see. | [L56](../../../src/mirrormind/modules/retrieval/index.py#L56) |
| `InMemoryEvidenceIndex.search` | method | `def search(self, query: EvidenceQuery) -> EvidenceRetrievalResult` | Run deterministic BM25 over pre-filtered documents and return exact citations. | [L104](../../../src/mirrormind/modules/retrieval/index.py#L104) |
| `_empty_result` | function | `def _empty_result() -> EvidenceRetrievalResult` | — | [L164](../../../src/mirrormind/modules/retrieval/index.py#L164) |
| `_make_hit` | function | `def _make_hit(score: float, item: _IndexedDocument, query_terms: frozenset[str]) -> RetrievedEvidence` | — | [L172](../../../src/mirrormind/modules/retrieval/index.py#L172) |

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

## `mirrormind.modules.simulation.worldkernel_mapping`

Source: [`src/mirrormind/modules/simulation/worldkernel_mapping.py`](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py)

Static imports (including inside functions): `...core.contracts`, `collections.abc`, `dataclasses`, `pydantic`, `types`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `WorldKernelMappingError` | class | `class WorldKernelMappingError` | The MirrorMind scenario cannot be represented by the allowlisted world. | [L24](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L24) |
| `WorldKernelWorldMapping` | class | `class WorldKernelWorldMapping` | Exact source and target identifiers reviewed for request translation. | [L29](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L29) |
| `WorldKernelOperatorLimits` | class | `class WorldKernelOperatorLimits` | Trusted composition-root ceilings, independent of scenario input. | [L53](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L53) |
| `WorldKernelOperatorLimits.__post_init__` | method | `def __post_init__(self) -> None` | — | [L60](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L60) |
| `InventoryWorldUnitContext` | class | `class InventoryWorldUnitContext` | Explicit units required by the integer-only inventory demo contract. | [L77](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L77) |
| `_nonnegative_integer_object` | function | `def _nonnegative_integer_object(values: object, *, name: str, allowed_fields: frozenset[str], required_fields: frozenset[str]) -> dict[str, int]` | — | [L85](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L85) |
| `_validate_units` | function | `def _validate_units(unit_context: InventoryWorldUnitContext) -> None` | — | [L115](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L115) |
| `build_worldkernel_exchange_request` | function | `def build_worldkernel_exchange_request(scenario: ScenarioSpec, *, operator_limits: WorldKernelOperatorLimits, unit_context: InventoryWorldUnitContext) -> dict[str, object]` | Build a strict WorldKernel v1 request without executing it. | [L130](../../../src/mirrormind/modules/simulation/worldkernel_mapping.py#L130) |

## `mirrormind.modules.simulation.worldkernel_policy_gateway`

Source: [`src/mirrormind/modules/simulation/worldkernel_policy_gateway.py`](../../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py)

Static imports (including inside functions): `...domains.retail.policy_simulation`, `...domains.retail.worldkernel_policy_world`, `.worldkernel_mapping`, `.worldkernel_policy_mapping`, `.worldkernel_runner`, `__future__`, `dataclasses`, `hashlib`, `json`, `pydantic`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `LocalWorldKernelRetailPolicyGateway` | class | `class LocalWorldKernelRetailPolicyGateway` | Execute only the code-owned retail policy world in a local worker. | [L45](../../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py#L45) |
| `LocalWorldKernelRetailPolicyGateway.compare` | method | `def compare(self, request: RetailPolicyComparisonRequest) -> dict[str, object]` | Run engine transitions, then reject any drift from the reviewed model. | [L51](../../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py#L51) |
| `_canonical_json_sha256` | function | `def _canonical_json_sha256(value: object) -> str` | — | [L125](../../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py#L125) |
| `_validate_policy_world_state` | function | `def _validate_policy_world_state(state: Any, assumptions: RetailPolicyAssumptions) -> None` | — | [L136](../../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py#L136) |
| `_summarize_engine_runs` | function | `def _summarize_engine_runs(*, final_states: list[dict[str, Any]], request: RetailPolicyComparisonRequest, expected_streams: tuple[_DemandStream, ...]) -> list[dict[str, object]]` | — | [L178](../../../src/mirrormind/modules/simulation/worldkernel_policy_gateway.py#L178) |

## `mirrormind.modules.simulation.worldkernel_policy_mapping`

Source: [`src/mirrormind/modules/simulation/worldkernel_policy_mapping.py`](../../../src/mirrormind/modules/simulation/worldkernel_policy_mapping.py)

Static imports (including inside functions): `...domains.retail.policy_simulation`, `...domains.retail.worldkernel_policy_world`, `.worldkernel_mapping`, `__future__`, `pydantic`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `build_worldkernel_policy_exchange_request` | function | `def build_worldkernel_policy_exchange_request(request: RetailPolicyComparisonRequest, *, operator_limits: WorldKernelOperatorLimits) -> dict[str, object]` | Build one fixed 28-step exchange request; reject work over operator limits. | [L25](../../../src/mirrormind/modules/simulation/worldkernel_policy_mapping.py#L25) |

## `mirrormind.modules.simulation.worldkernel_runner`

Source: [`src/mirrormind/modules/simulation/worldkernel_runner.py`](../../../src/mirrormind/modules/simulation/worldkernel_runner.py)

Static imports (including inside functions): `...core.contracts`, `.gateway`, `.worldkernel_mapping`, `__future__`, `dataclasses`, `hashlib`, `json`, `math`, `os`, `pathlib`, `pydantic`, `subprocess`, `sys`, `tempfile`, `threading`, `time`, `typing`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `WorldKernelRunnerError` | class | `class WorldKernelRunnerError` | A local WorldKernel execution could not produce an accepted result. | [L78](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L78) |
| `WorldKernelRuntimeUnavailable` | class | `class WorldKernelRuntimeUnavailable` | The optional pinned runtime is absent or does not match its source pin. | [L82](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L82) |
| `WorldKernelExecutionTimeout` | class | `class WorldKernelExecutionTimeout` | The local worker exceeded its effective wall-clock budget. | [L86](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L86) |
| `WorldKernelOutputLimitExceeded` | class | `class WorldKernelOutputLimitExceeded` | The local worker exceeded a bounded stdout or stderr size. | [L90](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L90) |
| `WorldKernelRuntimeConfig` | class | `class WorldKernelRuntimeConfig` | Trusted local-process settings, supplied by the application operator. | [L95](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L95) |
| `WorldKernelRuntimeConfig.__post_init__` | method | `def __post_init__(self) -> None` | — | [L102](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L102) |
| `LocalWorldKernelGateway` | class | `class LocalWorldKernelGateway` | Optional local implementation of the engine-neutral simulation gateway. | [L118](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L118) |
| `LocalWorldKernelGateway.execute` | method | `def execute(self, scenario: ScenarioSpec) -> SimulationSummary` | Execute one preconfigured scenario through the pinned local worker. | [L125](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L125) |
| `_scenario_snapshot` | function | `def _scenario_snapshot(scenario: ScenarioSpec) -> ScenarioSpec` | — | [L135](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L135) |
| `_worker_environment` | function | `def _worker_environment() -> dict[str, str]` | Pass OS-required variables only; omit arbitrary secrets and Python path overrides. | [L144](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L144) |
| `_read_bounded_stream` | function | `def _read_bounded_stream(stream: Any, *, limit: int, output: bytearray, exceeded: threading.Event) -> None` | Drain a child pipe while retaining at most limit + 1 bytes. | [L150](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L150) |
| `_terminate` | function | `def _terminate(process: subprocess.Popen[bytes]) -> None` | — | [L173](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L173) |
| `_read_limited` | function | `def _read_limited(handle: Any, limit: int) -> bytes` | — | [L190](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L190) |
| `_run_worker` | function | `def _run_worker(request_bytes: bytes, *, python_executable: str, timeout_seconds: float, max_output_bytes: int) -> bytes` | — | [L197](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L197) |
| `_reject_json_constant` | function | `def _reject_json_constant(value: str) -> None` | — | [L313](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L313) |
| `_parse_result` | function | `def _parse_result(raw: bytes) -> dict[str, object]` | — | [L317](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L317) |
| `_validate_mapped_exchange_request` | function | `def _validate_mapped_exchange_request(request: dict[str, object]) -> None` | — | [L329](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L329) |
| `_validate_exchange_result_envelope` | function | `def _validate_exchange_result_envelope(result: dict[str, object], request: dict[str, object]) -> tuple[list[dict[str, object]], list[str]]` | — | [L375](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L375) |
| `_validate_result` | function | `def _validate_result(result: dict[str, object], request: dict[str, object]) -> tuple[list[dict[str, int]], list[str]]` | — | [L411](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L411) |
| `execute_mapped_worldkernel_request` | function | `def execute_mapped_worldkernel_request(request: dict[str, object], *, runtime: WorldKernelRuntimeConfig \| None=None, timeout_seconds: float \| None=None) -> tuple[dict[str, object], bytes]` | Run one parent-mapped exchange request through the bounded pinned worker. | [L449](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L449) |
| `run_worldkernel_scenario` | function | `def run_worldkernel_scenario(scenario: ScenarioSpec, *, operator_limits: WorldKernelOperatorLimits, unit_context: InventoryWorldUnitContext, runtime: WorldKernelRuntimeConfig \| None=None) -> SimulationSummary` | Execute one strictly mapped scenario using the pinned local runtime. | [L484](../../../src/mirrormind/modules/simulation/worldkernel_runner.py#L484) |

## `mirrormind.modules.simulation.worldkernel_worker`

Source: [`src/mirrormind/modules/simulation/worldkernel_worker.py`](../../../src/mirrormind/modules/simulation/worldkernel_worker.py)

Static imports (including inside functions): `__future__`, `argparse`, `importlib`, `json`, `mirrormind.domains.retail.worldkernel_policy_world`, `re`, `sys`, `urllib.parse`, `worldkernel.adapters.exchange`, `worldkernel.core.registry`, `worldkernel.examples.bootstrap`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `_RuntimeMissing` | class | `class _RuntimeMissing` | — | [L21](../../../src/mirrormind/modules/simulation/worldkernel_worker.py#L21) |
| `_RuntimePinMismatch` | class | `class _RuntimePinMismatch` | — | [L25](../../../src/mirrormind/modules/simulation/worldkernel_worker.py#L25) |
| `_verify_installed_runtime` | function | `def _verify_installed_runtime(expected_commit: str) -> None` | — | [L29](../../../src/mirrormind/modules/simulation/worldkernel_worker.py#L29) |
| `main` | function | `def main() -> int` | — | [L59](../../../src/mirrormind/modules/simulation/worldkernel_worker.py#L59) |
