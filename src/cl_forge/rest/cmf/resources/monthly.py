from __future__ import annotations

from typing import Any

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import MonthInt, YearInt, YearMonth
from .base import BaseIndicatorResource


class MonthlyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseIndicatorResource[RecordT, CollectionT]):
    def current(self) -> RecordT:
        path = IndicatorPath.current(self._spec.path_name).build()
        return self._get(path, shape=ResponseShape.SINGLE)

    def year(self, year: YearInt) -> CollectionT:
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def month(self, year: YearInt, month: MonthInt) -> RecordT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.SINGLE)

    def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.after_year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.before_year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)
