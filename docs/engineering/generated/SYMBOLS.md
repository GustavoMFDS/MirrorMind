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
