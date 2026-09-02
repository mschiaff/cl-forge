from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from cl_forge.rest.auth.enums import ApiProvider
from cl_forge.rest.client.base import ApiClient
from cl_forge.rest.market.provider import MARKET_V1, MARKET_V2
from cl_forge.rest.market.resources.directory import (
    AsyncBuyerResource,
    AsyncSupplierResource,
    BuyerResource,
    SupplierResource,
)
from cl_forge.rest.market.resources.orders import AsyncOrderResource, OrderResource
from cl_forge.rest.market.resources.raw import AsyncRawResource, RawResource
from cl_forge.rest.market.resources.tenders import AsyncTenderResource, TenderResource

if TYPE_CHECKING:
    from cl_forge.rest.auth.types import CredentialType
    from cl_forge.rest.client.config import ClientConfig


class MarketClient(ApiClient):
    """Synchronous facade for the Mercado Publico APIs."""

    provider: ClassVar[ApiProvider] = ApiProvider.MARKET

    tender: TenderResource
    order: OrderResource
    supplier: SupplierResource
    buyer: BuyerResource
    raw: RawResource

    def __init__(
        self,
        credentials: CredentialType,
        config: ClientConfig | None = None,
    ) -> None:
        super().__init__(credentials, config)
        self._v1 = self._route(MARKET_V1)
        self._v2 = self._route(MARKET_V2)

        self.tender = TenderResource(self._v1)
        self.order = OrderResource(self._v1)
        self.supplier = SupplierResource(self._v1)
        self.buyer = BuyerResource(self._v1)
        self.raw = RawResource(self._v1, self._v2)

    @property
    def base_url(self) -> str:
        """Return the base URL of the default v1 Market API."""
        return MARKET_V1.base_url

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(base_url={self.base_url!r}, credentials={self.credentials!r})"
        )


class AsyncMarketClient(ApiClient):
    """Asynchronous facade for the Mercado Publico APIs."""

    provider: ClassVar[ApiProvider] = ApiProvider.MARKET

    tender: AsyncTenderResource
    order: AsyncOrderResource
    supplier: AsyncSupplierResource
    buyer: AsyncBuyerResource
    raw: AsyncRawResource

    def __init__(
        self,
        credentials: CredentialType,
        config: ClientConfig | None = None,
    ) -> None:
        super().__init__(credentials, config)
        self._v1 = self._route(MARKET_V1)
        self._v2 = self._route(MARKET_V2)

        self.tender = AsyncTenderResource(self._v1)
        self.order = AsyncOrderResource(self._v1)
        self.supplier = AsyncSupplierResource(self._v1)
        self.buyer = AsyncBuyerResource(self._v1)
        self.raw = AsyncRawResource(self._v1, self._v2)

    @property
    def base_url(self) -> str:
        """Return the base URL of the default v1 Market API."""
        return MARKET_V1.base_url

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(base_url={self.base_url!r}, credentials={self.credentials!r})"
        )


__all__ = ("AsyncMarketClient", "MarketClient")
