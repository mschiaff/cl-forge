from typing import Any

from cl_forge.rest.cmf.models.base import IndexList, IndexRecord

from .base import AsyncCmfResource, SyncCmfResource


class SyncMonthlyIndexResource[RecordT: IndexRecord, ListT: IndexList[Any]](
    SyncCmfResource[RecordT, ListT]
):
    def latest(self) -> RecordT:
        response = self._get()
        return self._parse_record(response)

    def year(self, year: int) -> ListT:
        response = self._get(year)
        return self._parse_list(response)

    def month(self, year: int, month: int) -> RecordT:
        response = self._get(year, month)
        return self._parse_record(response)

    def after(self, year: int, month: int | None = None) -> ListT:
        response = self._get("posteriores", year, month)
        return self._parse_list(response)

    def before(self, year: int, month: int | None = None) -> ListT:
        response = self._get("anteriores", year, month)
        return self._parse_list(response)

    def between(self, start_year: int, start_month: int, end_year: int, end_month: int) -> ListT:
        response = self._get("periodo", start_year, start_month, end_year, end_month)
        return self._parse_list(response)


class AsyncMonthlyIndexResource[RecordT: IndexRecord, ListT: IndexList[Any]](
    AsyncCmfResource[RecordT, ListT]
):
    async def latest(self) -> RecordT:
        response = await self._get()
        return self._parse_record(response)

    async def year(self, year: int) -> ListT:
        response = await self._get(year)
        return self._parse_list(response)

    async def month(self, year: int, month: int) -> RecordT:
        response = await self._get(year, month)
        return self._parse_record(response)

    async def after(self, year: int, month: int | None = None) -> ListT:
        response = await self._get("posteriores", year, month)
        return self._parse_list(response)

    async def before(self, year: int, month: int | None = None) -> ListT:
        response = await self._get("anteriores", year, month)
        return self._parse_list(response)
