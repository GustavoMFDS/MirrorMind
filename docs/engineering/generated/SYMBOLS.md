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

## `mirrormind.modules.__init__`

Source: [`src/mirrormind/modules/__init__.py`](../../../src/mirrormind/modules/__init__.py)

No top-level classes or functions.

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
