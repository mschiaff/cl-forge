from __future__ import annotations

from typing import override

from pydantic import field_validator

from .base import IndicatorCollection, IndicatorRecord, convert_decimal


class IpcRecord(IndicatorRecord):
    @override
    @field_validator('value', mode='before')
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return round(convert_decimal(value) / 100, 5)


class IpcCollection(IndicatorCollection[IpcRecord]): ...
