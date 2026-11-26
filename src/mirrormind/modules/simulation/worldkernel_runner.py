"""Version-pinned local execution for one trusted WorldKernel demo world.

The optional engine is launched in a child Python process only on explicit
call. This module adds local operator timeout/output bounds and validates the
complete v1 result; it does not provide hostile-code CPU/memory isolation.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from ...core.contracts import ScenarioSpec
from .gateway import SimulationSummary
from .worldkernel_mapping import (
    InventoryWorldUnitContext,
    WorldKernelMappingError,
    WorldKernelOperatorLimits,
    build_worldkernel_exchange_request,
)

WORLDKERNEL_PACKAGE_VERSION = "0.0.1"
WORLDKERNEL_SOURCE_COMMIT = "9b133ef873f2b6a7206c9c5742d40df4fccdb04a"
_WORKER_SCRIPT = Path(__file__).with_name("worldkernel_worker.py")
_MAX_TIMEOUT_SECONDS = 300
_MAX_OUTPUT_BYTES = 1_000_000
_MAX_ERROR_BYTES = 4_096
_ALLOWED_RESULT_FIELDS = frozenset(
    {
        "schema_version",
        "engine",
        "engine_adapter_version",
        "world",
        "declared_world_version",
        "registered_world_version",
        "world_version_matches_registry",
        "runs",
        "steps",
        "seed",
        "final_states",
        "assumptions",
    }
)
_INVENTORY_RESULT_FIELDS = frozenset({"stock", "sold", "unmet", "orders"})
_EXCHANGE_REQUEST_FIELDS = frozenset(
    {
        "schema_version",
        "world",
        "world_version",
        "steps",
        "runs",
        "seed",
        "initial_state",
        "parameters",
        "limits",
    }
)
_EXCHANGE_LIMIT_FIELDS = frozenset(
    {"max_steps", "max_runs", "max_total_transitions"}
)
_ALLOWED_EXCHANGE_WORLDS = {
    "retail.inventory.demo": "demo-1",
    "mirrormind.retail.policy_comparison": "mm-retail-policy-v1",
}


class WorldKernelRunnerError(RuntimeError):
    """A local WorldKernel execution could not produce an accepted result."""


class WorldKernelRuntimeUnavailable(WorldKernelRunnerError):
    """The optional pinned runtime is absent or does not match its source pin."""


class WorldKernelExecutionTimeout(WorldKernelRunnerError):
    """The local worker exceeded its effective wall-clock budget."""


class WorldKernelOutputLimitExceeded(WorldKernelRunnerError):
    """The local worker exceeded a bounded stdout or stderr size."""


@dataclass(frozen=True, slots=True)
class WorldKernelRuntimeConfig:
    """Trusted local-process settings, supplied by the application operator."""

    python_executable: str = sys.executable
    max_timeout_seconds: float = 30.0
    max_output_bytes: int = _MAX_OUTPUT_BYTES

    def __post_init__(self) -> None:
        if type(self.python_executable) is not str or not self.python_executable.strip():
            raise ValueError("python_executable must be a nonempty path")
        if (
            type(self.max_timeout_seconds) not in (int, float)
            or not 0 < self.max_timeout_seconds <= _MAX_TIMEOUT_SECONDS
        ):
            raise ValueError("max_timeout_seconds must be positive and at most 300")
        if (
            type(self.max_output_bytes) is not int
            or not 1 <= self.max_output_bytes <= _MAX_OUTPUT_BYTES
        ):
            raise ValueError("max_output_bytes must be between 1 and 1000000")


@dataclass(frozen=True, slots=True)
class LocalWorldKernelGateway:
    """Optional local implementation of the engine-neutral simulation gateway."""

    operator_limits: WorldKernelOperatorLimits
    unit_context: InventoryWorldUnitContext
    runtime: WorldKernelRuntimeConfig = WorldKernelRuntimeConfig()

    def execute(self, scenario: ScenarioSpec) -> SimulationSummary:
        """Execute one preconfigured scenario through the pinned local worker."""
        return run_worldkernel_scenario(
            scenario,
            operator_limits=self.operator_limits,
            unit_context=self.unit_context,
            runtime=self.runtime,
        )


def _scenario_snapshot(scenario: ScenarioSpec) -> ScenarioSpec:
    if not isinstance(scenario, ScenarioSpec):
        raise WorldKernelMappingError("scenario must be a validated ScenarioSpec")
    try:
        return ScenarioSpec.model_validate(scenario.model_dump(mode="python"))
    except ValidationError as exc:
        raise WorldKernelMappingError("scenario failed execution-boundary revalidation") from exc


def _worker_environment() -> dict[str, str]:
    """Pass OS-required variables only; omit arbitrary secrets and Python path overrides."""
    keep = ("PATH", "SystemRoot", "WINDIR", "TEMP", "TMP")
    return {name: os.environ[name] for name in keep if name in os.environ}


def _read_bounded_stream(
    stream: Any,
    *,
    limit: int,
    output: bytearray,
    exceeded: threading.Event,
) -> None:
    """Drain a child pipe while retaining at most limit + 1 bytes."""
    while True:
        chunk = stream.read(8_192)
        if not chunk:
            return
        remaining = limit + 1 - len(output)
        if len(chunk) > remaining:
            output.extend(chunk[:remaining])
            exceeded.set()
            return
        output.extend(chunk)
        if len(output) > limit:
            exceeded.set()
            return


def _terminate(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    try:
        process.terminate()
        process.wait(timeout=1.0)
    except (OSError, subprocess.TimeoutExpired):
        try:
            process.kill()
        except OSError:
            pass
        try:
            process.wait(timeout=1.0)
        except (OSError, subprocess.TimeoutExpired):
            pass


def _read_limited(handle: Any, limit: int) -> bytes:
    value = bytes(handle)
    if len(value) > limit:
        raise WorldKernelOutputLimitExceeded("WorldKernel worker output exceeded local limit")
    return value


def _run_worker(
    request_bytes: bytes,
    *,
    python_executable: str,
    timeout_seconds: float,
    max_output_bytes: int,
) -> bytes:
    if not _WORKER_SCRIPT.is_file():
        raise WorldKernelRuntimeUnavailable("pinned WorldKernel worker is unavailable")
    try:
        process = subprocess.Popen(
            [
                python_executable,
                str(_WORKER_SCRIPT),
                "--expected-commit",
                WORLDKERNEL_SOURCE_COMMIT,
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=tempfile.gettempdir(),
            env=_worker_environment(),
            shell=False,
            close_fds=True,
        )
    except OSError as exc:
        raise WorldKernelRuntimeUnavailable("pinned WorldKernel runtime is unavailable") from exc
    if process.stdout is None or process.stderr is None:
        _terminate(process)
        raise WorldKernelRunnerError("WorldKernel worker output could not be opened")
    stdout = bytearray()
    stderr = bytearray()
    output_exceeded = threading.Event()
    readers = [
        threading.Thread(
            target=_read_bounded_stream,
            kwargs={
                "stream": process.stdout,
                "limit": max_output_bytes,
                "output": stdout,
                "exceeded": output_exceeded,
            },
            daemon=True,
        ),
        threading.Thread(
            target=_read_bounded_stream,
            kwargs={
                "stream": process.stderr,
                "limit": _MAX_ERROR_BYTES,
                "output": stderr,
                "exceeded": output_exceeded,
            },
            daemon=True,
        ),
    ]
    for reader in readers:
        reader.start()
    try:
        if process.stdin is None:
            _terminate(process)
            raise WorldKernelRunnerError("WorldKernel worker input could not be opened")
        try:
            process.stdin.write(request_bytes)
        except OSError:
            pass
        finally:
            if process.stdin is not None and not process.stdin.closed:
                try:
                    process.stdin.close()
                except OSError:
                    pass
        deadline = time.monotonic() + timeout_seconds
        while process.poll() is None:
            if output_exceeded.wait(timeout=min(0.02, max(0.0, deadline - time.monotonic()))):
                _terminate(process)
                raise WorldKernelOutputLimitExceeded(
                    "WorldKernel worker output exceeded local limit"
                )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                _terminate(process)
                raise WorldKernelExecutionTimeout("WorldKernel worker exceeded local timeout")
        for reader in readers:
            reader.join(timeout=1.0)
        if output_exceeded.is_set():
            raise WorldKernelOutputLimitExceeded(
                "WorldKernel worker output exceeded local limit"
            )
        stdout_bytes = _read_limited(stdout, max_output_bytes)
        stderr_text = _read_limited(stderr, _MAX_ERROR_BYTES).decode(
            "utf-8", errors="replace"
        ).strip()
        if process.returncode != 0:
            if stderr_text == "WORLDKERNEL_NOT_INSTALLED":
                raise WorldKernelRuntimeUnavailable("pinned WorldKernel package is not installed")
            if stderr_text == "WORLDKERNEL_PIN_MISMATCH":
                raise WorldKernelRuntimeUnavailable(
                    "installed WorldKernel package does not match the reviewed pin"
                )
            raise WorldKernelRunnerError("WorldKernel local execution failed")
        if not stdout_bytes:
            raise WorldKernelRunnerError("WorldKernel worker returned an empty result")
        return stdout_bytes
    finally:
        if process.poll() is None:
            _terminate(process)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None and not stream.closed:
                try:
                    stream.close()
                except OSError:
                    pass
        for reader in readers:
            reader.join(timeout=1.0)


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _parse_result(raw: bytes) -> dict[str, object]:
    try:
        result = json.loads(raw, parse_constant=_reject_json_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise WorldKernelRunnerError("WorldKernel returned invalid JSON") from exc
    if type(result) is not dict:
        raise WorldKernelRunnerError("WorldKernel result must be an object")
    if set(result) != _ALLOWED_RESULT_FIELDS:
        raise WorldKernelRunnerError("WorldKernel result fields do not match result v1")
    return result


def _validate_mapped_exchange_request(request: dict[str, object]) -> None:
    if type(request) is not dict or set(request) != _EXCHANGE_REQUEST_FIELDS:
        raise WorldKernelMappingError("mapped request fields do not match exchange v1")
    if (
        request.get("schema_version") != "worldkernel.simulation.v1"
        or type(request.get("world")) is not str
        or not request["world"].strip()
        or type(request.get("world_version")) is not str
        or not request["world_version"].strip()
    ):
        raise WorldKernelMappingError("mapped request identity is invalid")
    if _ALLOWED_EXCHANGE_WORLDS.get(request["world"]) != request["world_version"]:
        raise WorldKernelMappingError("mapped request world revision is not allowlisted")
    for field, minimum in (("steps", 1), ("runs", 1), ("seed", 0)):
        value = request.get(field)
        if type(value) is not int or value < minimum:
            raise WorldKernelMappingError(f"mapped request {field} is invalid")
    limits = request.get("limits")
    if (
        type(limits) is not dict
        or set(limits) != _EXCHANGE_LIMIT_FIELDS
        or any(type(value) is not int or value < 1 for value in limits.values())
    ):
        raise WorldKernelMappingError("mapped request limits are invalid")
    try:
        WorldKernelOperatorLimits(**limits)
    except (TypeError, ValueError) as exc:
        raise WorldKernelMappingError("mapped request limits exceed local ceilings") from exc
    if (
        request["steps"] > limits["max_steps"]
        or request["runs"] > limits["max_runs"]
        or request["steps"] * request["runs"]
        > limits["max_total_transitions"]
    ):
        raise WorldKernelMappingError("mapped request exceeds its declared limits")
    if any(
        type(request[field]) is not dict
        or any(type(key) is not str for key in request[field])
        for field in ("initial_state", "parameters")
    ):
        raise WorldKernelMappingError("mapped request state and parameters must be objects")


def _validate_exchange_result_envelope(
    result: dict[str, object], request: dict[str, object]
) -> tuple[list[dict[str, object]], list[str]]:
    if (
        result.get("schema_version") != "worldkernel.result.v1"
        or result.get("engine") != "worldkernel"
        or result.get("engine_adapter_version") != "1"
        or result.get("world") != request["world"]
        or result.get("declared_world_version") != request["world_version"]
        or result.get("registered_world_version") != request["world_version"]
        or result.get("world_version_matches_registry") is not True
    ):
        raise WorldKernelRunnerError("WorldKernel result schema or revision mismatch")
    for field in ("runs", "steps", "seed"):
        expected = request[field]
        actual = result.get(field)
        if type(actual) is not int or actual != expected:
            raise WorldKernelRunnerError(f"WorldKernel result {field} mismatch")
    final_states = result.get("final_states")
    runs = request["runs"]
    if (
        type(final_states) is not list
        or len(final_states) != runs
        or any(type(state) is not dict for state in final_states)
    ):
        raise WorldKernelRunnerError("WorldKernel result run count mismatch")
    assumptions = result.get("assumptions")
    if (
        type(assumptions) is not list
        or not assumptions
        or any(type(value) is not str or not value.strip() for value in assumptions)
    ):
        raise WorldKernelRunnerError("WorldKernel result assumptions are invalid")
    return final_states, assumptions


def _validate_result(
    result: dict[str, object], request: dict[str, object]
) -> tuple[list[dict[str, int]], list[str]]:
    final_states, assumptions = _validate_exchange_result_envelope(result, request)
    initial_state = request["initial_state"]
    parameters = request["parameters"]
    if type(initial_state) is not dict or type(parameters) is not dict:
        raise WorldKernelRunnerError("mapped inventory inputs are invalid")
    starting_stock = initial_state["stock"]
    starting_sold = initial_state.get("sold", 0)
    starting_unmet = initial_state.get("unmet", 0)
    starting_orders = initial_state.get("orders", 0)
    reorder_quantity = parameters["reorder_quantity"]
    normalized_states: list[dict[str, int]] = []
    for state in final_states:
        if type(state) is not dict or set(state) != _INVENTORY_RESULT_FIELDS:
            raise WorldKernelRunnerError("WorldKernel final state fields are invalid")
        if any(type(value) is not int or value < 0 for value in state.values()):
            raise WorldKernelRunnerError("WorldKernel final state values are invalid")
        if (
            state["sold"] < starting_sold
            or state["unmet"] < starting_unmet
            or state["orders"] < starting_orders
        ):
            raise WorldKernelRunnerError("WorldKernel cumulative inventory counters decreased")
        new_orders = state["orders"] - starting_orders
        new_sold = state["sold"] - starting_sold
        if starting_stock + new_orders * reorder_quantity != state["stock"] + new_sold:
            raise WorldKernelRunnerError("WorldKernel result violates inventory balance")
        normalized_states.append({key: state[key] for key in sorted(state)})
    return normalized_states, assumptions


def execute_mapped_worldkernel_request(
    request: dict[str, object],
    *,
    runtime: WorldKernelRuntimeConfig | None = None,
    timeout_seconds: float | None = None,
) -> tuple[dict[str, object], bytes]:
    """Run one parent-mapped exchange request through the bounded pinned worker."""
    _validate_mapped_exchange_request(request)
    runtime_config = runtime or WorldKernelRuntimeConfig()
    effective_timeout = runtime_config.max_timeout_seconds
    if timeout_seconds is not None:
        if (
            type(timeout_seconds) not in (int, float)
            or not math.isfinite(timeout_seconds)
            or timeout_seconds <= 0
        ):
            raise WorldKernelMappingError("exchange timeout must be positive")
        effective_timeout = min(effective_timeout, timeout_seconds)
    try:
        request_bytes = json.dumps(
            request, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise WorldKernelMappingError("mapped request is not finite JSON") from exc
    raw_result = _run_worker(
        request_bytes,
        python_executable=runtime_config.python_executable,
        timeout_seconds=effective_timeout,
        max_output_bytes=runtime_config.max_output_bytes,
    )
    result = _parse_result(raw_result)
    _validate_exchange_result_envelope(result, request)
    return result, raw_result


def run_worldkernel_scenario(
    scenario: ScenarioSpec,
    *,
    operator_limits: WorldKernelOperatorLimits,
    unit_context: InventoryWorldUnitContext,
    runtime: WorldKernelRuntimeConfig | None = None,
) -> SimulationSummary:
    """Execute one strictly mapped scenario using the pinned local runtime.

    The composition root owns ``operator_limits`` and ``runtime``. The
    caller-controlled scenario cannot increase those limits or choose a
    Python executable, worker, external package revision or registered world.
    """
    scenario_copy = _scenario_snapshot(scenario)
    if scenario_copy.budget.max_model_calls != 0 or scenario_copy.budget.max_output_tokens != 0:
        raise WorldKernelMappingError(
            "model-call and token budgets are unsupported by local simulation"
        )
    runtime_config = runtime or WorldKernelRuntimeConfig()
    request = build_worldkernel_exchange_request(
        scenario_copy,
        operator_limits=operator_limits,
        unit_context=unit_context,
    )
    effective_timeout = min(
        runtime_config.max_timeout_seconds,
        scenario_copy.budget.timeout_seconds,
    )
    result, raw_result = execute_mapped_worldkernel_request(
        request,
        runtime=runtime_config,
        timeout_seconds=effective_timeout,
    )
    final_states, assumptions = _validate_result(result, request)
    canonical = json.dumps(
        {
            "engine_commit": WORLDKERNEL_SOURCE_COMMIT,
            "request": request,
            "scenario": scenario_copy.model_dump(mode="json"),
        },
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    scenario_id = hashlib.sha256(canonical).hexdigest()
    result_digest = hashlib.sha256(raw_result).hexdigest()
    return SimulationSummary(
        scenario_id=scenario_id,
        engine_version=(
            f"worldkernel/{WORLDKERNEL_PACKAGE_VERSION}@{WORLDKERNEL_SOURCE_COMMIT}"
        ),
        run_count=len(final_states),
        results={
            "schema_version": "mirrormind.simulation.summary.v1",
            "engine_result_schema": "worldkernel.result.v1",
            "world": request["world"],
            "world_version": request["world_version"],
            "steps": request["steps"],
            "seed": request["seed"],
            "final_states": final_states,
            "result_sha256": result_digest,
        },
        assumptions=[
            *assumptions,
            "package source commit is checked through PEP 610 metadata, not installed-file attestation",
            "the inventory demo uses synthetic daily demand and immediate replenishment; it does not model lead time",
            "local process timeout and output bounds are not a general CPU or memory sandbox",
        ],
    )
