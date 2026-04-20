from __future__ import annotations

import enum
from typing import Literal, NamedTuple

type ResponseFormat = Literal["json", "xml"]
type RangeMode = Literal["after", "before", "between"]


class BaseTypeMeta(enum.EnumType):
    def __contains__(cls, value: str) -> bool:
        if isinstance(value, str):
            value = value.strip().lower()
            return any(
                member.name.lower() == value # type: ignore
                for member in cls
            )
        return super().__contains__(value)


class BaseType(enum.Enum, metaclass=BaseTypeMeta):
    @classmethod
    def _missing_(cls, value: str):
        if isinstance(value, str):
            value = value.strip().lower()
            for member in cls:
                if member.name.lower() == value:
                    return member
            raise ValueError(f"Invalid item: {value!r}")
        raise ValueError(
            "Expected a 'str' value, but got "
            f"{type(value).__name__!r}."
        )


class FormatType(
        NamedTuple(
            "FormatType",
            [("fmt", str)]
        ),
        BaseType
):
    JSON = "json"
    XML = "xml"


class ModeType(
        NamedTuple(
            "ModeType",
            [("path", str)]
        ),
        BaseType
):
    AFTER = "ipc/posteriores"
    BEFORE = "ipc/anteriores"
    BETWEEN = "ipc/periodo"