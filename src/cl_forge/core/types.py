from __future__ import annotations

import enum
from typing import Literal

type ResponseFormat = Literal["json", "xml"]
type RangeMode = Literal["after", "before", "between"]


class BaseStrEnum(enum.StrEnum):
    @classmethod
    def _missing_(cls, value: object) -> BaseStrEnum:
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.lowercase == value:
                    return member
        return super()._missing_(value)
    
    @enum.property
    def lowercase(self) -> str:
        """Lowercase name of the enum member."""
        return self.name.lower()
    
    @enum.property
    def private(self) -> str:
        """Lowercase private name of the enum member."""
        return f"_{self.lowercase}"


class FormatEnum(BaseStrEnum):
    JSON = enum.auto()
    XML = enum.auto()


class EndpointEnum(BaseStrEnum):
    IPC = enum.auto()
    UF = enum.auto()
    USD = enum.auto()
    EURO = enum.auto()
    UTM = enum.auto()


class ModeEnum(BaseStrEnum):
    AFTER = "posteriores"
    BEFORE = "anteriores"
    BETWEEN = "periodo"
