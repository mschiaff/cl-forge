from __future__ import annotations

from .base import IndicatorCollection, IndicatorRecord


class UtmRecord(IndicatorRecord): ...


class UtmCollection(IndicatorCollection[UtmRecord]): ...
