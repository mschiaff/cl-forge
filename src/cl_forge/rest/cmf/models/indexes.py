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


class EurRecord(IndexRecord):
    """Represents a single EUR record."""


class EurList(IndexList[EurRecord]):
    """Represents a collection of EUR records."""


# Compatibility aliases for the names exposed by the initial ``rest`` refactor.
EuroRecord = EurRecord
EuroList = EurList


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
