"""Immutable code-owned tool definitions with strict contracts and digest receipts."""
from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from hashlib import sha256
from types import MappingProxyType
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ValidationError

from .contracts import (
    MAX_TOOL_OUTPUT_BYTES,
    ProviderRequest,
    RefusalCode,
    ToolCall,
    ToolDescriptor,
    ToolObservation,
    ToolReceipt,
)

MAX_TOOL_INPUT_BYTES = 8_192
MAX_TOOL_DEFINITIONS = 8
_NAME = re.compile(r"^[a-z][a-z0-9_.-]{0,63}$")
InputModel = TypeVar("InputModel", bound=BaseModel)
OutputModel = TypeVar("OutputModel", bound=BaseModel)


class ToolInvocationError(Exception):
    """Sanitized failure code; never retains input or handler exception text."""

    def __init__(self, code: RefusalCode, *, input_sha256: str | None = None) -> None:
        self.code = code
        self.input_sha256 = input_sha256
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class ToolDefinition(Generic[InputModel, OutputModel]):
    """Trusted local handler plus exact Pydantic input and output classes."""

    name: str
    description: str
    input_model: type[InputModel]
    output_model: type[OutputModel]
    handler: Callable[[InputModel], OutputModel]

    def __post_init__(self) -> None:
        if not _NAME.fullmatch(self.name):
            raise ValueError("tool name is not canonical")
        if not self.description or len(self.description) > 240:
            raise ValueError("tool description must contain 1..240 characters")
        if not issubclass(self.input_model, BaseModel) or not issubclass(
            self.output_model, BaseModel
        ):
            raise TypeError("tool input and output must be Pydantic model classes")


@dataclass(frozen=True, slots=True)
class _ToolExecution:
    observation: ToolObservation
    receipt: ToolReceipt


class ToolRegistry:
    """Read-only map of reviewed local functions; no run-time registration API."""

    __slots__ = ("_by_name", "_definitions")
    _definitions: tuple[ToolDefinition[Any, Any], ...]
    _by_name: Mapping[str, ToolDefinition[Any, Any]]

    def __init__(self, definitions: tuple[ToolDefinition[Any, Any], ...]) -> None:
        if type(definitions) is not tuple or not 1 <= len(definitions) <= MAX_TOOL_DEFINITIONS:
            raise ValueError("registry requires a bounded tuple of tool definitions")
        if any(type(item) is not ToolDefinition for item in definitions):
            raise TypeError("registry accepts exact ToolDefinition records")
        names = tuple(item.name for item in definitions)
        if len(names) != len(set(names)):
            raise ValueError("tool names must be unique")
        object.__setattr__(self, "_definitions", definitions)
        object.__setattr__(
            self,
            "_by_name",
            MappingProxyType({item.name: item for item in definitions}),
        )

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("tool registry is immutable")

    def __delattr__(self, name: str) -> None:
        raise AttributeError("tool registry is immutable")

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(item.name for item in self._definitions)

    def contains(self, name: str) -> bool:
        return name in self._by_name

    def describe(self, names: tuple[str, ...]) -> tuple[ToolDescriptor, ...]:
        if any(name not in self._by_name for name in names):
            raise ValueError("requested tool is not registered")
        return tuple(
            ToolDescriptor(
                name=name,
                description=self._by_name[name].description,
                input_fields=tuple(self._by_name[name].input_model.model_fields),
            )
            for name in names
        )

    def invoke(self, call: ToolCall) -> _ToolExecution:
        if type(call) is not ToolCall:
            raise TypeError("call must be an exact ToolCall")

        try:
            argument_bytes = _canonical_json(call.arguments)
        except (TypeError, ValueError, UnicodeError, RecursionError, OverflowError):
            raise ToolInvocationError("invalid_tool_input") from None
        input_sha256 = sha256(argument_bytes).hexdigest()
        if len(argument_bytes) > MAX_TOOL_INPUT_BYTES:
            raise ToolInvocationError(
                "tool_input_too_large", input_sha256=input_sha256
            )

        definition = self._by_name.get(call.tool_name)
        if definition is None:
            raise ToolInvocationError("tool_not_registered", input_sha256=input_sha256)
        try:
            parsed_input = definition.input_model.model_validate_json(
                argument_bytes, strict=True
            )
        except (ValidationError, ValueError, TypeError):
            raise ToolInvocationError("invalid_tool_input", input_sha256=input_sha256) from None
        if type(parsed_input) is not definition.input_model:
            raise ToolInvocationError("invalid_tool_input", input_sha256=input_sha256)

        try:
            output = definition.handler(parsed_input)
        except Exception:  # noqa: BLE001 - tool failures expose only a fixed refusal code
            raise ToolInvocationError("tool_failed", input_sha256=input_sha256) from None
        if type(output) is not definition.output_model:
            raise ToolInvocationError("invalid_tool_output", input_sha256=input_sha256)
        try:
            output_bytes = _canonical_json(output.model_dump(mode="json"))
            validated_output = definition.output_model.model_validate_json(
                output_bytes, strict=True
            )
        except (
            ValidationError,
            ValueError,
            TypeError,
            UnicodeError,
            RecursionError,
            OverflowError,
        ):
            raise ToolInvocationError("invalid_tool_output", input_sha256=input_sha256) from None
        if type(validated_output) is not definition.output_model:
            raise ToolInvocationError("invalid_tool_output", input_sha256=input_sha256)
        if len(output_bytes) > MAX_TOOL_OUTPUT_BYTES:
            raise ToolInvocationError("tool_output_too_large", input_sha256=input_sha256)

        output_sha256 = sha256(output_bytes).hexdigest()
        observation = ToolObservation(
            call_id=call.call_id,
            tool_name=call.tool_name,
            output_json=output_bytes.decode("utf-8"),
            output_sha256=output_sha256,
        )
        receipt = ToolReceipt(
            call_id=call.call_id,
            tool_name=call.tool_name,
            input_sha256=input_sha256,
            output_sha256=output_sha256,
            output_bytes=len(output_bytes),
        )
        return _ToolExecution(observation=observation, receipt=receipt)


def provider_context_size(request: ProviderRequest) -> int:
    """Measure canonical UTF-8 bytes before the provider receives a context."""
    return len(_canonical_json(request.model_dump(mode="json")))


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
