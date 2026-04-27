from __future__ import annotations

from typing import Any, override

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import DayInt, MonthInt, YearInt, YearMonth, YearMonthDay
from .monthly import MonthlyIndicatorResource


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
