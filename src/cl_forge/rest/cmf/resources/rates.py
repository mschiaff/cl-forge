from typing import Any

from cl_forge.rest.cmf.models.base import RateList, RateRecord

from .base import AsyncCmfResource, SyncCmfResource
from .dates import year_month_segments, year_segment
from .types import Month, Year


class SyncRateResource[RecordT: RateRecord, ListT: RateList[Any]](
    SyncCmfResource[RecordT, ListT]
):
    def latest(self) -> ListT:
        response = self._get()
        return self._parse_list(response)

    def year(self, year: Year) -> ListT:
        response = self._get(year_segment(year))
        return self._parse_list(response)

    def month(self, year: Year, month: Month) -> ListT:
        response = self._get(*year_month_segments(year, month))
        return self._parse_list(response)

    def after(self, year: Year, month: Month | None = None) -> ListT:
        response = self._get("posteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    def before(self, year: Year, month: Month | None = None) -> ListT:
        response = self._get("anteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    def between(
        self,
        start_year: Year,
        start_month: Month,
        end_year: Year,
        end_month: Month,
    ) -> ListT:
        response = self._get(
            "periodo",
            *year_month_segments(start_year, start_month),
            *year_month_segments(end_year, end_month),
        )
        return self._parse_list(response)

    def between_years(self, start_year: Year, end_year: Year) -> ListT:
        response = self._get("periodo", year_segment(start_year), year_segment(end_year))
        return self._parse_list(response)


class AsyncRateResource[RecordT: RateRecord, ListT: RateList[Any]](
    AsyncCmfResource[RecordT, ListT]
):
    async def latest(self) -> ListT:
        response = await self._get()
        return self._parse_list(response)

    async def year(self, year: Year) -> ListT:
        response = await self._get(year_segment(year))
        return self._parse_list(response)

    async def month(self, year: Year, month: Month) -> ListT:
        response = await self._get(*year_month_segments(year, month))
        return self._parse_list(response)

    async def after(self, year: Year, month: Month | None = None) -> ListT:
        response = await self._get("posteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    async def before(self, year: Year, month: Month | None = None) -> ListT:
        response = await self._get("anteriores", *year_month_segments(year, month))
        return self._parse_list(response)

    async def between(
        self,
        start_year: Year,
        start_month: Month,
        end_year: Year,
        end_month: Month,
    ) -> ListT:
        response = await self._get(
            "periodo",
            *year_month_segments(start_year, start_month),
            *year_month_segments(end_year, end_month),
        )
        return self._parse_list(response)

    async def between_years(self, start_year: Year, end_year: Year) -> ListT:
        response = await self._get("periodo", year_segment(start_year), year_segment(end_year))
        return self._parse_list(response)
