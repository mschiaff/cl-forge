from typing import override

from pydantic import field_validator

from .base import IndexList, IndexRecord, convert_decimal


class IpcRecord(IndexRecord):
    """Represents a single IPC record."""

    @override
    @field_validator("value", mode="before")
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return round(convert_decimal(value) / 100, 5)


class IpcList(IndexList[IpcRecord]):
    """Represents a collection of IPC records."""


class EuroRecord(IndexRecord):
    """Represents a single Euro record."""


class EuroList(IndexList[EuroRecord]):
    """Represents a collection of Euro records."""


class UfRecord(IndexRecord):
    """Represents a single UF record."""


class UfList(IndexList[UfRecord]):
    """Represents a collection of UF records."""


class UsdRecord(IndexRecord):
    """Represents a single USD record."""


class UsdList(IndexList[UsdRecord]):
    """Represents a collection of USD records."""


class UtmRecord(IndexRecord):
    """Represents a single UTM record."""


class UtmList(IndexList[UtmRecord]):
    """Represents a collection of UTM records."""
