from dataclasses import dataclass
from typing import Any, overload

from cl_forge.core.types import EndpointEnum, ModeEnum, RangeMode

@dataclass(frozen=True)
class ModeProxy:
    _mode: ModeEnum
    _owner: BoundedMode

    @property
    def type(self) -> ModeEnum: ...

    @property
    def path(self) -> str: ...


@dataclass
class ModeDescriptor:
    def __init__(self, mode: ModeEnum) -> None: ...

    @overload
    def __get__(self, obj: None, owner: type[BoundedMode]) -> Exception: ...
    @overload
    def __get__(self, obj: BoundedMode, owner: type[BoundedMode]) -> ModeProxy: ...

    def __set__(self, obj: Any, value: Any) -> None: ...


@dataclass
class BoundedMode:
    endpoint: EndpointEnum

    def __call__(self, mode: RangeMode) -> ModeProxy: ...
