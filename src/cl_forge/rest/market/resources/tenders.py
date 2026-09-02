from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.rest.market.models.tenders import TenderDetailsResult, TenderResult
from cl_forge.rest.market.resources.base import MarketResource
from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import PathExtensionFormat

from .query import TenderQuery
from .types import TenderStatus, TenderStatusFilter

if TYPE_CHECKING:
    from httpx2 import Response

    from cl_forge.rest.resources.types import QueryParams

    from .types import DateLike, TenderStatusLike


TENDER_SPEC = ResourceSpec(endpoint="/licitaciones")


class TenderHandler(MarketResource[ResourceSpec]):
    _spec = TENDER_SPEC
    _format_policy = PathExtensionFormat()

    @staticmethod
    def _params(query: TenderQuery | None) -> QueryParams | None:
        return None if query is None else query.params

    @staticmethod
    def _parse_result(response: Response) -> TenderResult:
        response.raise_for_status()
        return TenderResult.model_validate(response.json())

    @staticmethod
    def _parse_details(response: Response) -> TenderDetailsResult:
        response.raise_for_status()
        return TenderDetailsResult.model_validate(response.json())


class TenderResource(TenderHandler, SyncResource[ResourceSpec]):
    """Synchronous access to Mercado Publico tenders."""

    def _query(self, query: TenderQuery | None = None) -> TenderResult:
        return self._parse_result(self._get(params=self._params(query)))

    def today(self) -> TenderResult:
        """Return tender summaries for today."""
        return self._query()

    def details(self, tender_code: str) -> TenderDetailsResult:
        """Return full details for one tender code."""
        query = TenderQuery.model_validate({"tender_code": tender_code})
        return self._parse_details(self._get(params=query.params))

    def by_date(self, date: DateLike) -> TenderResult:
        """Return tender summaries for a date."""
        return self._query(TenderQuery.model_validate({"date": date}))

    def active(self) -> TenderResult:
        """Return all currently active tenders."""
        return self._query(TenderQuery(status=TenderStatusFilter.ACTIVE.value))

    def all(self, date: DateLike | None = None) -> TenderResult:
        """Return tenders in every status, optionally for a date."""
        query = TenderQuery.model_validate({"status": TenderStatusFilter.ALL.value, "date": date})
        return self._query(query)

    def by_buyer(self, buyer_code: str | int, *, date: DateLike | None = None) -> TenderResult:
        """Return tenders for a buyer, optionally for a date."""
        query = TenderQuery.model_validate({"buyer_code": buyer_code, "date": date})
        return self._query(query)

    def by_status(
        self,
        status: TenderStatusLike,
        *,
        date: DateLike | None = None,
    ) -> TenderResult:
        """Return tenders in one status, optionally for a date."""
        normalized = TenderStatus.parse(status).value
        query = TenderQuery.model_validate({"status": normalized, "date": date})
        return self._query(query)

    def by_supplier(
        self,
        supplier_code: str | int,
        *,
        date: DateLike | None = None,
    ) -> TenderResult:
        """Return tenders for a supplier, optionally for a date."""
        query = TenderQuery.model_validate({"supplier_code": supplier_code, "date": date})
        return self._query(query)


class AsyncTenderResource(TenderHandler, AsyncResource[ResourceSpec]):
    """Asynchronous access to Mercado Publico tenders."""

    async def _query(self, query: TenderQuery | None = None) -> TenderResult:
        return self._parse_result(await self._get(params=self._params(query)))

    async def today(self) -> TenderResult:
        return await self._query()

    async def details(self, tender_code: str) -> TenderDetailsResult:
        query = TenderQuery.model_validate({"tender_code": tender_code})
        return self._parse_details(await self._get(params=query.params))

    async def by_date(self, date: DateLike) -> TenderResult:
        return await self._query(TenderQuery.model_validate({"date": date}))

    async def active(self) -> TenderResult:
        return await self._query(TenderQuery(status=TenderStatusFilter.ACTIVE.value))

    async def all(self, date: DateLike | None = None) -> TenderResult:
        query = TenderQuery.model_validate({"status": TenderStatusFilter.ALL.value, "date": date})
        return await self._query(query)

    async def by_buyer(
        self,
        buyer_code: str | int,
        *,
        date: DateLike | None = None,
    ) -> TenderResult:
        query = TenderQuery.model_validate({"buyer_code": buyer_code, "date": date})
        return await self._query(query)

    async def by_status(
        self,
        status: TenderStatusLike,
        *,
        date: DateLike | None = None,
    ) -> TenderResult:
        normalized = TenderStatus.parse(status).value
        query = TenderQuery.model_validate({"status": normalized, "date": date})
        return await self._query(query)

    async def by_supplier(
        self,
        supplier_code: str | int,
        *,
        date: DateLike | None = None,
    ) -> TenderResult:
        query = TenderQuery.model_validate({"supplier_code": supplier_code, "date": date})
        return await self._query(query)


__all__ = ("TENDER_SPEC", "AsyncTenderResource", "TenderResource")
