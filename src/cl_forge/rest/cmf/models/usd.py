from __future__ import annotations

from .base import IndicatorCollection, IndicatorRecord


class UsdRecord(IndicatorRecord): ...


class UsdCollection(IndicatorCollection[UsdRecord]): ...
