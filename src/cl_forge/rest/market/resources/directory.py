from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.rest.market.models.directory import (
    BuyerResult,
    SupplierList,
    SupplierRecord,
    SupplierResult,
)
from cl_forge.rest.market.resources.base import MarketResource
from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import FixedJsonFormat

from .query import SupplierQuery

if TYPE_CHECKING:
    from httpx2 import Response

    from .types import RutLike


SUPPLIER_SPEC = ResourceSpec(endpoint="/Empresas/BuscarProveedor")
BUYER_SPEC = ResourceSpec(endpoint="/Empresas/BuscarComprador")


class SupplierHandler(MarketResource[ResourceSpec]):
    _spec = SUPPLIER_SPEC
    _format_policy = FixedJsonFormat()

    @staticmethod
    def _parse_result(response: Response) -> SupplierResult:
        response.raise_for_status()
        return SupplierResult.model_validate(response.json())

    @staticmethod
    def _select_result(
        result: SupplierResult,
        *,
        ignore_meta: bool,
        only_record: bool,
    ) -> SupplierRecord | SupplierList | SupplierResult:
        if only_record:
            if not result.records.root:
                raise ValueError("Supplier search returned no records")
            return result.records.root[0]
        if ignore_meta:
            return result.records
        return result


class SupplierResource(SupplierHandler, SyncResource[ResourceSpec]):
    """Synchronous supplier-directory search."""

    def search(
        self,
        rut: RutLike,
        *,
        ignore_meta: bool = False,
        only_record: bool = False,
    ) -> SupplierRecord | SupplierList | SupplierResult:
        query = SupplierQuery.model_validate({"rut": rut})
        result = self._parse_result(self._get(params=query.params))
        return self._select_result(
            result,
            ignore_meta=ignore_meta,
            only_record=only_record,
        )


class AsyncSupplierResource(SupplierHandler, AsyncResource[ResourceSpec]):
    """Asynchronous supplier-directory search."""

    async def search(
        self,
        rut: RutLike,
        *,
        ignore_meta: bool = False,
        only_record: bool = False,
    ) -> SupplierRecord | SupplierList | SupplierResult:
        query = SupplierQuery.model_validate({"rut": rut})
        result = self._parse_result(await self._get(params=query.params))
        return self._select_result(
            result,
            ignore_meta=ignore_meta,
            only_record=only_record,
        )


class BuyerHandler(MarketResource[ResourceSpec]):
    _spec = BUYER_SPEC
    _format_policy = FixedJsonFormat()

    @staticmethod
    def _parse_result(response: Response) -> BuyerResult:
        response.raise_for_status()
        return BuyerResult.model_validate(response.json())


class BuyerResource(BuyerHandler, SyncResource[ResourceSpec]):
    """Synchronous buyer-directory search."""

    def search(self) -> BuyerResult:
        return self._parse_result(self._get())


class AsyncBuyerResource(BuyerHandler, AsyncResource[ResourceSpec]):
    """Asynchronous buyer-directory search."""

    async def search(self) -> BuyerResult:
        return self._parse_result(await self._get())


__all__ = (
    "BUYER_SPEC",
    "SUPPLIER_SPEC",
    "AsyncBuyerResource",
    "AsyncSupplierResource",
    "BuyerResource",
    "SupplierResource",
)
