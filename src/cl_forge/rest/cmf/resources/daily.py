from __future__ import annotations

from typing import Any, override

from cl_forge.rest.cmf.types import (  # noqa: TC001
    DayInt,
    MonthInt,
    ThreeTupleDate,
    TwoTupleDate,
    YearInt,
)

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import EndDay, StartDay, YearMonth, YearMonthDay
from .monthly import AsyncMonthlyIndicatorResource, MonthlyIndicatorResource


def is_three_tuple(value: YearInt | TwoTupleDate | ThreeTupleDate) -> bool:
    return isinstance(value, tuple) and len(value) == 3


class DailyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](MonthlyIndicatorResource[RecordT, CollectionT]):
    @override
    def month(self, year: YearInt, month: MonthInt) -> CollectionT: # type: ignore
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def day(self, year: YearInt, month: MonthInt, day: DayInt) -> RecordT:
        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.day(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.SINGLE)

    @override
    def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        if day is None:
            return super().after(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.after_day(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    @override
    def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        if day is None:
            return super().before(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.before_day(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    @override
    def between(
            self,
            start: YearInt | TwoTupleDate | ThreeTupleDate,
            end: YearInt | TwoTupleDate | ThreeTupleDate
    ) -> CollectionT:
        if is_three_tuple(start) and is_three_tuple(end):
            _start = StartDay.from_value(start) # type: ignore
            _end = EndDay.from_value(end) # type: ignore
            path = IndicatorPath.between_days(self._spec.path_name, _start, _end).build()
            return self._get(path, shape=ResponseShape.COLLECTION)

        return super().between(start, end) # type: ignore


class AsyncDailyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](AsyncMonthlyIndicatorResource[RecordT, CollectionT]):
    @override
    async def month(self, year: YearInt, month: MonthInt) -> CollectionT: # type: ignore
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def day(self, year: YearInt, month: MonthInt, day: DayInt) -> RecordT:
        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.day(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.SINGLE)

    @override
    async def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        if day is None:
            return await super().after(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.after_day(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    @override
    async def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        if day is None:
            return await super().before(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.before_day(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    @override
    async def between(
            self,
            start: YearInt | TwoTupleDate | ThreeTupleDate,
            end: YearInt | TwoTupleDate | ThreeTupleDate
    ) -> CollectionT:
        if is_three_tuple(start) and is_three_tuple(end):
            _start = StartDay.from_value(start) # type: ignore
            _end = EndDay.from_value(end) # type: ignore
            path = IndicatorPath.between_days(self._spec.path_name, _start, _end).build()
            return await self._aget(path, shape=ResponseShape.COLLECTION)

        return await super().between(start, end) # type: ignore
