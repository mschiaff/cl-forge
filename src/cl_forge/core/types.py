from __future__ import annotations

from enum import Enum, EnumType
from typing import Literal, NamedTuple

type ResponseFormat = Literal["json", "xml"]
type RangeMode = Literal["after", "before", "between"]


class BaseTypeMeta(EnumType):
    def __contains__(cls, value: object) -> bool:
        if isinstance(value, str):
            value = value.strip().lower()
            members = (member.name.lower() for member in cls) # type: ignore
            return any(member == value for member in members)
        return super().__contains__(value)


class BaseType(Enum, metaclass=BaseTypeMeta):
    @classmethod
    def _missing_(cls, value: object):
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
