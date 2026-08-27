from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.rest.market.models.orders import OrderDetailsResult, OrderResult
from cl_forge.rest.market.resources.base import MarketResource
from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import PathExtensionFormat

from .query import OrderQuery
from .types import OrderStatus, OrderStatusFilter

if TYPE_CHECKING:
    from httpx2 import Response

    from cl_forge.rest.resources.types import QueryParams

    from .types import DateLike, OrderStatusLike


ORDER_SPEC = ResourceSpec(endpoint="/OrdenesDeCompra")


class OrderHandler(MarketResource[ResourceSpec]):
    _spec = ORDER_SPEC
    _format_policy = PathExtensionFormat()

    @staticmethod
    def _params(query: OrderQuery | None) -> QueryParams | None:
        return None if query is None else query.params

    @staticmethod
    def _parse_result(response: Response) -> OrderResult:
        response.raise_for_status()
        return OrderResult.model_validate(response.json())

    @staticmethod
    def _parse_details(response: Response) -> OrderDetailsResult:
        response.raise_for_status()
        return OrderDetailsResult.model_validate(response.json())


class OrderResource(OrderHandler, SyncResource[ResourceSpec]):
    """Synchronous access to Mercado Publico purchase orders."""

    def _query(self, query: OrderQuery | None = None) -> OrderResult:
        return self._parse_result(self._get(params=self._params(query)))

    def today(self) -> OrderResult:
        return self._query()

    def details(self, order_code: str) -> OrderDetailsResult:
        query = OrderQuery.model_validate({"order_code": order_code})
        return self._parse_details(self._get(params=query.params))

    def by_date(self, date: DateLike) -> OrderResult:
        return self._query(OrderQuery.model_validate({"date": date}))

    def all(self, date: DateLike | None = None) -> OrderResult:
        query = OrderQuery.model_validate({"status": OrderStatusFilter.ALL.value, "date": date})
        return self._query(query)

    def by_buyer(self, buyer_code: str | int, *, date: DateLike | None = None) -> OrderResult:
        query = OrderQuery.model_validate({"buyer_code": buyer_code, "date": date})
        return self._query(query)

    def by_status(
        self,
        status: OrderStatusLike,
        *,
        date: DateLike | None = None,
    ) -> OrderResult:
        normalized = OrderStatus.parse(status).value
        query = OrderQuery.model_validate({"status": normalized, "date": date})
        return self._query(query)

    def by_supplier(
        self,
        supplier_code: str | int,
        *,
        date: DateLike | None = None,
    ) -> OrderResult:
        query = OrderQuery.model_validate({"supplier_code": supplier_code, "date": date})
        return self._query(query)


class AsyncOrderResource(OrderHandler, AsyncResource[ResourceSpec]):
    """Asynchronous access to Mercado Publico purchase orders."""

    async def _query(self, query: OrderQuery | None = None) -> OrderResult:
        return self._parse_result(await self._get(params=self._params(query)))

    async def today(self) -> OrderResult:
        return await self._query()

    async def details(self, order_code: str) -> OrderDetailsResult:
        query = OrderQuery.model_validate({"order_code": order_code})
        return self._parse_details(await self._get(params=query.params))

    async def by_date(self, date: DateLike) -> OrderResult:
        return await self._query(OrderQuery.model_validate({"date": date}))

    async def all(self, date: DateLike | None = None) -> OrderResult:
        query = OrderQuery.model_validate({"status": OrderStatusFilter.ALL.value, "date": date})
        return await self._query(query)

    async def by_buyer(
        self,
        buyer_code: str | int,
        *,
        date: DateLike | None = None,
    ) -> OrderResult:
        query = OrderQuery.model_validate({"buyer_code": buyer_code, "date": date})
        return await self._query(query)

    async def by_status(
        self,
        status: OrderStatusLike,
        *,
        date: DateLike | None = None,
    ) -> OrderResult:
        normalized = OrderStatus.parse(status).value
        query = OrderQuery.model_validate({"status": normalized, "date": date})
        return await self._query(query)

    async def by_supplier(
        self,
        supplier_code: str | int,
        *,
        date: DateLike | None = None,
    ) -> OrderResult:
        query = OrderQuery.model_validate({"supplier_code": supplier_code, "date": date})
        return await self._query(query)


__all__ = ("ORDER_SPEC", "AsyncOrderResource", "OrderResource")
