from __future__ import annotations

from .base import IndicatorCollection, IndicatorRecord


class EuroRecord(IndicatorRecord): ...


class EuroCollection(IndicatorCollection[EuroRecord]): ...
