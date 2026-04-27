from __future__ import annotations

from typing import Any

from cl_forge.rest.cmf.types import MonthInt, TwoTupleDate, YearInt  # noqa: TC001

from ..models.base import InterestRateCollection, InterestRateRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import YearMonth
from .base import BaseRateResource


class RateResource[
    RecordT: InterestRateRecord,
    CollectionT: InterestRateCollection[Any]
](BaseRateResource[RecordT, CollectionT]):
    def current(self) -> CollectionT:
        path = IndicatorPath.current(self._spec.path_name).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def year(self, year: YearInt) -> CollectionT:
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def month(self, year: YearInt, month: MonthInt) -> CollectionT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)
    
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
    
    def between(
            self,
            start: YearInt | TwoTupleDate,
            end: YearInt | TwoTupleDate
    ) -> CollectionT:
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return self._get(path, shape=ResponseShape.COLLECTION)
