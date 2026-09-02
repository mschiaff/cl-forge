from typing import Any, overload

from cl_forge.rest.cmf.models.base import IndexList, IndexRecord

from .base import AsyncCmfResource, SyncCmfResource
from .dates import year_month_day_segments, year_month_segments, year_segment
from .types import Day, Month, Year


def _between_segments(
    start_year: Year,
    start_month: Month,
    date_parts: tuple[int, ...],
) -> tuple[str, ...]:
    if len(date_parts) == 2:
        end_year, end_month = date_parts
        return (
            *year_month_segments(start_year, start_month),
            *year_month_segments(end_year, end_month),
        )
    if len(date_parts) == 4:
        start_day, end_year, end_month, end_day = date_parts
        return (
            *year_month_day_segments(start_year, start_month, start_day, marker="dias_i"),
            *year_month_day_segments(end_year, end_month, end_day, marker="dias_f"),
        )
    raise TypeError("between() expects four or six date components")


class SyncDailyIndexResource[RecordT: IndexRecord, ListT: IndexList[Any]](
    SyncCmfResource[RecordT, ListT]
):
    def latest(self) -> RecordT:
        response = self._get()
        return self._parse_record(response)

    def year(self, year: Year) -> ListT:
        response = self._get(year_segment(year))
        return self._parse_list(response)

    def month(self, year: Year, month: Month) -> ListT:
        response = self._get(*year_month_segments(year, month))
        return self._parse_list(response)

    def day(self, year: Year, month: Month, day: Day) -> RecordT:
        response = self._get(*year_month_day_segments(year, month, day))
        return self._parse_record(response)

    def after(
        self,
        year: Year,
        month: Month | None = None,
        day: Day | None = None,
    ) -> ListT:
        if day is None:
            response = self._get("posteriores", *year_month_segments(year, month))
        else:
            if month is None:
                raise ValueError("Month is required when day is provided")
            response = self._get(
                "posteriores",
                *year_month_day_segments(year, month, day),
            )
        return self._parse_list(response)

    def before(
        self,
        year: Year,
        month: Month | None = None,
        day: Day | None = None,
    ) -> ListT:
        if day is None:
            response = self._get("anteriores", *year_month_segments(year, month))
        else:
            if month is None:
                raise ValueError("Month is required when day is provided")
            response = self._get(
                "anteriores",
                *year_month_day_segments(year, month, day),
            )
        return self._parse_list(response)

    @overload
    def between(
        self,
        start_year: Year,
        start_month: Month,
        end_year: Year,
        end_month: Month,
        /,
    ) -> ListT: ...

    @overload
    def between(
        self,
        start_year: Year,
        start_month: Month,
        start_day: Day,
        end_year: Year,
        end_month: Month,
        end_day: Day,
        /,
    ) -> ListT: ...

    def between(
        self,
        start_year: Year,
        start_month: Month,
        *date_parts: int,
    ) -> ListT:
        response = self._get(
            "periodo",
            *_between_segments(start_year, start_month, date_parts),
        )
        return self._parse_list(response)

    def between_years(self, start_year: Year, end_year: Year) -> ListT:
        response = self._get("periodo", year_segment(start_year), year_segment(end_year))
        return self._parse_list(response)

    def between_days(
        self,
        start_year: Year,
        start_month: Month,
        start_day: Day,
        end_year: Year,
        end_month: Month,
        end_day: Day,
    ) -> ListT:
        return self.between(
            start_year,
            start_month,
            start_day,
            end_year,
            end_month,
            end_day,
        )


class AsyncDailyIndexResource[RecordT: IndexRecord, ListT: IndexList[Any]](
    AsyncCmfResource[RecordT, ListT]
):
    async def latest(self) -> RecordT:
        response = await self._get()
        return self._parse_record(response)

    async def year(self, year: Year) -> ListT:
        response = await self._get(year_segment(year))
        return self._parse_list(response)

    async def month(self, year: Year, month: Month) -> ListT:
        response = await self._get(*year_month_segments(year, month))
        return self._parse_list(response)

    async def day(self, year: Year, month: Month, day: Day) -> RecordT:
        response = await self._get(*year_month_day_segments(year, month, day))
        return self._parse_record(response)

    async def after(
        self,
        year: Year,
        month: Month | None = None,
        day: Day | None = None,
    ) -> ListT:
        if day is None:
            response = await self._get("posteriores", *year_month_segments(year, month))
        else:
            if month is None:
                raise ValueError("Month is required when day is provided")
            response = await self._get(
                "posteriores",
                *year_month_day_segments(year, month, day),
            )
        return self._parse_list(response)

    async def before(
        self,
        year: Year,
        month: Month | None = None,
        day: Day | None = None,
    ) -> ListT:
        if day is None:
            response = await self._get("anteriores", *year_month_segments(year, month))
        else:
            if month is None:
                raise ValueError("Month is required when day is provided")
            response = await self._get(
                "anteriores",
                *year_month_day_segments(year, month, day),
            )
        return self._parse_list(response)

    @overload
    async def between(
        self,
        start_year: Year,
        start_month: Month,
        end_year: Year,
        end_month: Month,
        /,
    ) -> ListT: ...

    @overload
    async def between(
        self,
        start_year: Year,
        start_month: Month,
        start_day: Day,
        end_year: Year,
        end_month: Month,
        end_day: Day,
        /,
    ) -> ListT: ...

    async def between(
        self,
        start_year: Year,
        start_month: Month,
        *date_parts: int,
    ) -> ListT:
        response = await self._get(
            "periodo",
            *_between_segments(start_year, start_month, date_parts),
        )
        return self._parse_list(response)

    async def between_years(self, start_year: Year, end_year: Year) -> ListT:
        response = await self._get(
            "periodo",
            year_segment(start_year),
            year_segment(end_year),
        )
        return self._parse_list(response)

    async def between_days(
        self,
        start_year: Year,
        start_month: Month,
        start_day: Day,
        end_year: Year,
        end_month: Month,
        end_day: Day,
    ) -> ListT:
        return await self.between(
            start_year,
            start_month,
            start_day,
            end_year,
            end_month,
            end_day,
        )
