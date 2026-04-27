from __future__ import annotations

from .base import IndicatorCollection, IndicatorRecord


class UfRecord(IndicatorRecord): ...


class UfCollection(IndicatorCollection[UfRecord]): ...
