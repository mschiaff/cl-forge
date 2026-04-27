from __future__ import annotations

from typing import Any, override

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import DayInt, MonthInt, YearInt, YearMonthDay
from .monthly import MonthlyIndicatorResource


class DailyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](MonthlyIndicatorResource[RecordT, CollectionT]):
    def current(self) -> RecordT:
        path = IndicatorPath.current(self._spec.path_name).build()
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
