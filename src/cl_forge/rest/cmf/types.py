from __future__ import annotations

import enum
from typing import ClassVar, Literal

type ResponseFormat = Literal["json", "xml"]

class FormatEnum(enum.StrEnum):
    JSON = enum.auto()
    XML = enum.auto()


type RangeMode = Literal["after", "before", "between"]

class RangeModeEnum(enum.StrEnum):
    AFTER = enum.auto()
    BEFORE = enum.auto()
    BETWEEN = enum.auto()

class ReadOnlyMeta(type):
    def __setattr__(cls, name, value):
        raise AttributeError(
            f"Cannot modify attribute {name!r} "
            f"of {cls.__name__!r}"
        )

class RangeType(metaclass=ReadOnlyMeta):
    path: ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if "path" not in cls.__dict__:
            raise NotImplementedError(
                "Subclasses of 'RangeType' must "
                "define a 'path' class variable."
            )
        
        _name = cls.__name__
        path = cls.__dict__.get("path")

        if not isinstance(path, str):
            raise TypeError(
                "The 'path' class variable in "
                f"{_name!r} must be of type 'str'."
            )
        
        if not path or path is None:
            raise ValueError(
                f"The 'path' class variable in {_name!r} "
                "cannot be an empty string or None."
            )

class RangeAfter(RangeType):
    path = "ipc/posteriores"

class RangeBefore(RangeType):
    path = "ipc/anteriores"

class RangeBetween(RangeType):
    path = "ipc/periodo"