from __future__ import annotations

from typing import override

from pydantic import field_validator

from .base import IndicatorCollection, IndicatorRecord, convert_decimal


class IpcRecord(IndicatorRecord):
    """Represents a single IPC indicator record."""

    @override
    @field_validator('value', mode='before')
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return round(convert_decimal(value) / 100, 5)

class IpcCollection(IndicatorCollection[IpcRecord]):
    """Represents a collection of IPC indicator records."""


class EuroRecord(IndicatorRecord):
    """Represents a single Euro indicator record."""

class EuroCollection(IndicatorCollection[EuroRecord]):
    """Represents a collection of Euro indicator records."""


class UfRecord(IndicatorRecord):
    """Represents a single UF indicator record."""

class UfCollection(IndicatorCollection[UfRecord]):
    """Represents a collection of UF indicator records."""


class UsdRecord(IndicatorRecord):
    """Represents a single USD indicator record."""

class UsdCollection(IndicatorCollection[UsdRecord]):
    """Represents a collection of USD indicator records."""


class UtmRecord(IndicatorRecord):
    """Represents a single UTM indicator record."""

class UtmCollection(IndicatorCollection[UtmRecord]):
    """Represents a collection of UTM indicator records."""
