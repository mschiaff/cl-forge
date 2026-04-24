from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cl_forge.core.types import EndpointEnum, ModeEnum, RangeMode


@dataclass(frozen=True)
class ModeProxy:
    _mode: ModeEnum
    _owner: BoundedMode

    def __repr__(self) -> str:
        _type = self.type
        _path = self.path
        _cls = type(self).__name__
        return f"{_cls}(type={_type!r}, path={_path!r})"

    @property
    def type(self) -> ModeEnum:
        return self._mode

    @property
    def path(self) -> str:
        return f"{self._owner.endpoint}/{self._mode}"


@dataclass
class ModeDescriptor:
    def __init__(self, mode: ModeEnum) -> None:
        self._mode = mode
        self._name = mode.private

    def __get__(
            self,
            obj: BoundedMode | None,
            owner: type[BoundedMode]
    ) -> ModeProxy | Exception:
        if obj is not None:
            return ModeProxy(self._mode, obj)

        _name = self._name
        _owner = owner.__name__
        raise AttributeError(f"Cannot access managed attribute {_name!r} from class {_owner!r}")

    def __set__(self, obj: Any, value: Any) -> None:
        raise AttributeError(f"Cannot assign to managed attribute {self._name!r}")


@dataclass
class BoundedMode:
    endpoint: EndpointEnum

    def __call__(self, mode: RangeMode) -> ModeProxy:
        name = f"_{mode}"
        if not hasattr(BoundedMode, name):
            setattr(
                BoundedMode,
                name,
                ModeDescriptor(
                    ModeEnum(mode)
                )
            )
        return getattr(self, name)
