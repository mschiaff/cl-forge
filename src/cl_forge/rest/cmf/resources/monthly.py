from typing import Any, overload

from cl_forge.rest.cmf.models.base import IndexList, IndexRecord

from .base import AsyncCmfResource, SyncCmfResource
from .dates import year_month_segments, year_segment
from .types import Month, Year


def _between_segments(
    start_year: Year,
    start_month: Month | None = None,
    end_year: Year | None = None,
    end_month: Month | None = None,
) -> tuple[str, ...]:
    if end_year is None:
        if start_month is None or end_month is not None:
            raise TypeError("between() expects two or four date components")
        return year_segment(start_year), year_segment(start_month)

    if start_month is None:
        if end_month is not None:
            raise TypeError("between() expects two or four date components")
        return year_segment(start_year), year_segment(end_year)

    if end_month is None:
        raise TypeError("between() expects two or four date components")

    return (
        *year_month_segments(start_year, start_month),
        *year_month_segments(end_year, end_month),
    )


class SyncMonthlyIndexResource[RecordT: IndexRecord, ListT: IndexList[Any]](
    SyncCmfResource[RecordT, ListT]
):
    def latest(self) -> RecordT:
        response = self._get()
        return self._parse_record(response)

    def year(self, year: Year) -> ListT:
        response = self._get(year_segment(year))
        return self._parse_list(response)

    def month(self, year: Year, month: Month) -> RecordT:
        response = self._get(*year_month_segments(year, month))
        return self._parse_record(response)

    def after(self, year: Year, month: Month | None = None) -> ListT:
        response = self._get("posteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    def before(self, year: Year, month: Month | None = None) -> ListT:
        response = self._get("anteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    @overload
    def between(self, start_year: Year, end_year: Year, /) -> ListT: ...

    @overload
    def between(self, start_year: Year, *, end_year: Year) -> ListT: ...

    @overload
    def between(
        self,
        start_year: Year,
        start_month: Month,
        end_year: Year,
        end_month: Month,
    ) -> ListT: ...

    def between(
        self,
        start_year: Year,
        start_month: Month | None = None,
        end_year: Year | None = None,
        end_month: Month | None = None,
    ) -> ListT:
        response = self._get(
            "periodo", *_between_segments(start_year, start_month, end_year, end_month)
        )
        return self._parse_list(response)

    def between_years(self, start_year: Year, end_year: Year) -> ListT:
        return self.between(start_year, end_year)


class AsyncMonthlyIndexResource[RecordT: IndexRecord, ListT: IndexList[Any]](
    AsyncCmfResource[RecordT, ListT]
):
    async def latest(self) -> RecordT:
        response = await self._get()
        return self._parse_record(response)

    async def year(self, year: Year) -> ListT:
        response = await self._get(year_segment(year))
        return self._parse_list(response)

    async def month(self, year: Year, month: Month) -> RecordT:
        response = await self._get(*year_month_segments(year, month))
        return self._parse_record(response)

    async def after(self, year: Year, month: Month | None = None) -> ListT:
        response = await self._get("posteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    async def before(self, year: Year, month: Month | None = None) -> ListT:
        response = await self._get("anteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    @overload
    async def between(self, start_year: Year, end_year: Year, /) -> ListT: ...

    @overload
    async def between(self, start_year: Year, *, end_year: Year) -> ListT: ...

    @overload
    async def between(
        self,
        start_year: Year,
        start_month: Month,
        end_year: Year,
        end_month: Month,
    ) -> ListT: ...

    async def between(
        self,
        start_year: Year,
        start_month: Month | None = None,
        end_year: Year | None = None,
        end_month: Month | None = None,
    ) -> ListT:
        response = await self._get(
            "periodo",
            *_between_segments(start_year, start_month, end_year, end_month),
        )
        return self._parse_list(response)

    async def between_years(self, start_year: Year, end_year: Year) -> ListT:
        return await self.between(start_year, end_year)
