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

Static imports (including inside functions): `__future__`, `datetime`, `functools`, `heapq`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.uci_transactions`, `mirrormind.modules.forecasting.baselines`, `re`

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
| `_scenario_from_eligible_totals` | function | `def _scenario_from_eligible_totals(earlier: tuple[int, int, int], later: tuple[int, int, int], excluded_value_ceiling: int) -> ExcludedTargetSensitivity` | Apply a caller's assumption to validated eligible totals, without I/O. | [L146](../../../src/mirrormind/domains/retail/selection_sensitivity.py#L146) |

## `mirrormind.domains.retail.sensitivity_sweep`

Source: [`src/mirrormind/domains/retail/sensitivity_sweep.py`](../../../src/mirrormind/domains/retail/sensitivity_sweep.py)

Static imports (including inside functions): `__future__`, `dataclasses`, `datetime`, `itertools`, `mirrormind.domains.retail.declared_releases`, `mirrormind.domains.retail.selection_sensitivity`, `mirrormind.domains.retail.uci_transactions`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `RetailSensitivitySweep` | class | `class RetailSensitivitySweep` | An ordered, bounded list of hypothetical scenario results. | [L22](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L22) |
| `RetailSensitivitySweep.receipt` | method | `def receipt(self) -> dict[str, object]` | Show scenario receipts but never selected source identifiers. | [L30](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L30) |
| `sweep_excluded_target_sensitivity` | function | `def sweep_excluded_target_sensitivity(projection: UciRetailProjection, releases: tuple[DeclaredProductRelease, ...], *, stock_code: str, evaluation_on: date, ceilings: tuple[int, ...], window_days: int=7, calibration_days: int=21, min_calibration_residuals: int=5, minimum_eligible_per_window: int=3, minimum_coverage_percent: int=80) -> RetailSensitivitySweep` | Compare two to eight strictly increasing, hypothetical ceilings. | [L50](../../../src/mirrormind/domains/retail/sensitivity_sweep.py#L50) |

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

## `mirrormind.modules.evidence.atomic_governed_publisher`

Source: [`src/mirrormind/modules/evidence/atomic_governed_publisher.py`](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py)

Static imports (including inside functions): `__future__`, `collections.abc`, `dataclasses`, `datetime`, `hashlib`, `hmac`, `json`, `mirrormind.modules.evidence.intake_review`, `mirrormind.modules.evidence.local_checkpoint_publisher`, `mirrormind.modules.evidence.operator_governance`, `pathlib`, `re`, `sqlite3`

| Symbol | Kind | Signature | Docstring first line | Source |
| --- | --- | --- | --- | --- |
| `AtomicGovernedRevision` | class | `class AtomicGovernedRevision` | One local snapshot; does not represent source or production authorization. | [L53](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L53) |
| `AtomicGovernedRevision.receipt` | method | `def receipt(self) -> dict[str, str \| int \| bool]` | Only safe local consistency fields; never an access-control token. | [L63](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L63) |
| `_HistoricalSignatureVerifier` | class | `class _HistoricalSignatureVerifier` | Reuse tested signature/history helpers without enabling direct publishing. | [L82](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L82) |
| `_HistoricalSignatureVerifier.__init__` | method | `def __init__(self, checkpoint_keys: Mapping[str, bytes], witness_keys: Mapping[str, bytes], operator_keys: Mapping[str, bytes], bootstrap: str) -> None` | — | [L85](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L85) |
| `_HistoricalSignatureVerifier.publish` | method | `def publish(self, *args: object, **kwargs: object) -> None` | — | [L98](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L98) |
| `AtomicGovernedPublisher` | class | `class AtomicGovernedPublisher` | Opt-in local shared schema with serial policy updates and publication. | [L102](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L102) |
| `AtomicGovernedPublisher.__init__` | method | `def __init__(self, path: Path, *, administrator_public_keys: Mapping[str, bytes], checkpoint_keys: Mapping[str, bytes], witness_keys: Mapping[str, bytes], initial_witness_key_id: str, create: bool=False) -> None` | — | [L110](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L110) |
| `AtomicGovernedPublisher._connect` | method | `def _connect(self) -> sqlite3.Connection` | — | [L246](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L246) |
| `AtomicGovernedPublisher._schema` | method | `def _schema(self, db: sqlite3.Connection) -> None` | — | [L258](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L258) |
| `AtomicGovernedPublisher._read_policy` | method | `def _read_policy(self, db: sqlite3.Connection, checked_on: date) -> tuple[int, str, dict[str, tuple[str, date, bool]]]` | — | [L274](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L274) |
| `AtomicGovernedPublisher._check_policy_role_separation` | method | `def _check_policy_role_separation(self, records: Mapping[str, tuple[str, date, bool]]) -> None` | — | [L285](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L285) |
| `AtomicGovernedPublisher._verifier` | method | `def _verifier(self, records: Mapping[str, tuple[str, date, bool]]) -> _HistoricalSignatureVerifier` | — | [L298](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L298) |
| `AtomicGovernedPublisher._expected` | method | `def _expected(expected: int, head: str, current: int, current_head: str) -> None` | — | [L310](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L310) |
| `AtomicGovernedPublisher.append_policy` | method | `def append_policy(self, event: SignedOperatorPolicyEvent, *, expected_policy_revision: int, expected_policy_head_sha256: str, checked_on: date) -> OperatorPolicyRevision` | Atomically advance the same-file policy read by future publications. | [L318](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L318) |
| `AtomicGovernedPublisher.snapshot` | method | `def snapshot(self, packet: SourceReviewPacket, *, checked_on: date, externally_expected_policy_head_sha256: str \| None=None, externally_expected_publication_head_sha256: str \| None=None) -> AtomicGovernedRevision` | Reverify *both* local signed histories in the same read snapshot. | [L370](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L370) |
| `AtomicGovernedPublisher.publish` | method | `def publish(self, packet: SourceReviewPacket, command: SignedPublicationCommand, *, expected_policy_revision: int, expected_policy_head_sha256: str, expected_publication_sequence: int, expected_publication_head_sha256: str, checked_on: date) -> AtomicGovernedRevision` | Reject revoked/expired keys and append under ONE SQLite write lock. | [L409](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L409) |
| `_last_governance_date` | function | `def _last_governance_date(db: sqlite3.Connection, revision: int) -> date` | Read only the exact preceding canonical signed event's calendar date. | [L507](../../../src/mirrormind/modules/evidence/atomic_governed_publisher.py#L507) |

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
| `LocalOperatorGovernance._check_external_head` | method | `def _check_external_head(head: str, expected: str \| None) -> None` | — | [L387](../../../src/mirrormind/modules/evidence/operator_governance.py#L387) |
| `LocalOperatorGovernance.snapshot` | method | `def snapshot(self, *, checked_on: date, externally_expected_head_sha256: str \| None=None) -> OperatorPolicyRevision` | — | [L395](../../../src/mirrormind/modules/evidence/operator_governance.py#L395) |
| `LocalOperatorGovernance.assess_operator` | method | `def assess_operator(self, operator_key_id: str, operator_public_key: bytes, *, checked_on: date, externally_expected_head_sha256: str \| None=None) -> OperatorPolicyAssessment` | — | [L421](../../../src/mirrormind/modules/evidence/operator_governance.py#L421) |
| `LocalOperatorGovernance.append` | method | `def append(self, event: SignedOperatorPolicyEvent, *, expected_revision: int, expected_head_sha256: str, checked_on: date) -> OperatorPolicyRevision` | — | [L464](../../../src/mirrormind/modules/evidence/operator_governance.py#L464) |

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
| `RemoteFenceHeadStore` | class | `class RemoteFenceHeadStore` | Read contract for a future separately implemented current-head store. | [L47](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L47) |
| `RemoteFenceHeadStore.read_current` | method | `def read_current(self, packet_sha256: str) -> CurrentRemoteFenceHead \| None` | Return the claimed head or raise ``RemoteFenceHeadStoreError``. | [L55](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L55) |
| `RemoteFenceHeadRequest` | class | `class RemoteFenceHeadRequest` | Minimal decoded request fields consumed by the responder. | [L60](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L60) |
| `RemoteFenceHeadResponse` | class | `class RemoteFenceHeadResponse` | Transport-neutral status, headers and bounded response bytes. | [L70](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L70) |
| `RemoteFenceHeadResponse.__post_init__` | method | `def __post_init__(self) -> None` | — | [L77](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L77) |
| `RemoteFenceHeadResponder` | class | `class RemoteFenceHeadResponder` | Sign one fixed-path nonce challenge from a typed current-head store. | [L81](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L81) |
| `RemoteFenceHeadResponder.__init__` | method | `def __init__(self, *, service_id: str, service_key_id: str, endpoint: str, signing_key: object, non_service_public_keys: Mapping[str, bytes], store: RemoteFenceHeadStore, clock: Callable[[], datetime], ttl_seconds: int=60) -> None` | — | [L95](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L95) |
| `RemoteFenceHeadResponder.respond` | method | `def respond(self, request: RemoteFenceHeadRequest) -> RemoteFenceHeadResponse` | Return one canonical signed response, or a bodyless generic failure. | [L158](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L158) |
| `_empty_response` | function | `def _empty_response(status_code: int, *, allow_get: bool=False) -> RemoteFenceHeadResponse` | — | [L235](../../../src/mirrormind/modules/evidence/remote_fence_head_service.py#L235) |

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
