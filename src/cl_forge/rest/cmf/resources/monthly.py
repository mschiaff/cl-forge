from __future__ import annotations

from typing import Any

from cl_forge.rest.cmf.types import MonthInt, TwoTupleDate, YearInt  # noqa: TC001

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import YearMonth
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

    def between(
            self,
            start: YearInt | TwoTupleDate,
            end: YearInt | TwoTupleDate
    ) -> CollectionT:
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return self._get(path, shape=ResponseShape.COLLECTION)


class AsyncMonthlyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseIndicatorResource[RecordT, CollectionT]):
    async def current(self) -> RecordT:
        path = IndicatorPath.current(self._spec.path_name).build()
        return await self._aget(path, shape=ResponseShape.SINGLE)

    async def year(self, year: YearInt) -> CollectionT:
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def month(self, year: YearInt, month: MonthInt) -> RecordT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.SINGLE)

    async def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.after_year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.before_year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def between(
            self,
            start: YearInt | TwoTupleDate,
            end: YearInt | TwoTupleDate
    ) -> CollectionT:
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)
