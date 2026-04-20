from __future__ import annotations

import enum
from typing import Literal, NamedTuple

type ResponseFormat = Literal["json", "xml"]
type RangeMode = Literal["after", "before", "between"]


class BaseTypeMeta(enum.EnumType):
    def __contains__(cls, value: str) -> bool:
        if isinstance(value, str):
            value = value.strip().lower()
            members = (member.name.lower() for member in cls) # type: ignore
            return any(member == value for member in members)
        return super().__contains__(value)


class BaseType(enum.Enum, metaclass=BaseTypeMeta):
    @classmethod
    def _missing_(cls, value: str):
        if isinstance(value, str):
            value = value.strip().lower()
            for member in cls:
                if member.name.lower() == value:
                    return member
        super()._missing_(value)


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