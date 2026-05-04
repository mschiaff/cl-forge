from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, overload

from cl_forge.rest.market.types import MarketTransport

if TYPE_CHECKING:
    from pydantic import BaseModel

    from cl_forge.rest.market.types import MarketTransport, ResponseFormat

    from ..models.directory import DirectoryResult
    from ..query.directory import DirectoryQuery
    from ..query.orders import OrderQuery
    from ..query.tenders import TenderQuery
    from ..specs.directory import DirectorySpec
    from ..specs.orders import OrderSpec
    from ..specs.tenders import TenderSpec


class BaseMarketResource:
    def __init__(self, transport: MarketTransport) -> None:
        self._transport = transport

    @overload
    def _get(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    def _get(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...

    def _get(
            self,
            path: str,
            fmt: ResponseFormat = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str:
        return self._transport.get(path, fmt=fmt, params=params)

    @overload
    async def _aget(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    async def _aget(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...

    async def _aget(
            self,
            path: str,
            fmt: ResponseFormat = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str:
        return await self._transport.aget(path, fmt=fmt, params=params)


class BaseTendersResource[
    RecordsT: BaseModel,
    DetailsT: BaseModel
](BaseMarketResource):
    def __init__(
            self,
            transport: MarketTransport,
            *,
            spec: TenderSpec[RecordsT, DetailsT]
    ) -> None:
        super().__init__(transport)
        self._spec = spec

    def _get_tenders(self, query: TenderQuery | None = None) -> RecordsT:
        data = self._get(path=self._spec.path_name, params=query.params if query else query)
        return self._spec.record_model.model_validate(data)

    def _get_details(self, query: TenderQuery) -> DetailsT:
        data = self._get(path=self._spec.path_name, params=query.params)
        return self._spec.details_model.model_validate(data)

    async def _aget_tenders(self, query: TenderQuery | None = None) -> RecordsT:
        data = await self._aget(path=self._spec.path_name, params=query.params if query else query)
        return self._spec.record_model.model_validate(data)

    async def _aget_details(self, query: TenderQuery) -> DetailsT:
        data = await self._aget(path=self._spec.path_name, params=query.params)
        return self._spec.details_model.model_validate(data)


class BaseOrdersResource[
    RecordsT: BaseModel,
    DetailsT: BaseModel
](BaseMarketResource):
    def __init__(
            self,
            transport: MarketTransport,
            *,
            spec: OrderSpec[RecordsT, DetailsT]
    ) -> None:
        super().__init__(transport)
        self._spec = spec

    def _get_orders(self, query: OrderQuery | None = None) -> RecordsT:
        data = self._get(path=self._spec.path_name, params=query.params if query else query)
        return self._spec.record_model.model_validate(data)

    def _get_details(self, query: OrderQuery) -> DetailsT:
        data = self._get(path=self._spec.path_name, params=query.params)
        return self._spec.details_model.model_validate(data)


class BaseDirectoryResource[
    ResultT: DirectoryResult,
    QueryT: DirectoryQuery,
](BaseMarketResource):
    def __init__(
            self,
            transport: MarketTransport,
            *,
            spec: DirectorySpec[ResultT]
    ) -> None:
        super().__init__(transport)
        self._spec = spec

    def _search(self, query: QueryT | None = None) -> ResultT:
        data = self._get(path=self._spec.path_name, params=query.params if query else query)
        return self._spec.model.model_validate(data)
