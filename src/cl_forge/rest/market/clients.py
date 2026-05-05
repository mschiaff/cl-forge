from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.impl.market import BaseMarketClient

from .resources.directory import AsyncSuppliersResource, BuyersResource, SuppliersResource
from .resources.orders import AsyncOrdersResource, OrdersResource
from .resources.raw import AsyncRawMarketResource, RawMarketResource
from .resources.tenders import AsyncTendersResource, TendersResource
from .specs.directory import BUYER_SPEC, SUPPLIER_SPEC
from .specs.orders import ORDER_SPEC
from .specs.tenders import TENDER_SPEC

if TYPE_CHECKING:
    from .types import MarketTransport


__all__ = ("AsyncMarketClient", "MarketClient")


class MarketClient:
    """Client for interacting with the Public Market API (ChileCompra)."""

    raw: RawMarketResource
    """Resource for accessing raw market API requests."""
    tenders: TendersResource
    """Resource for accessing tender data."""
    orders: OrdersResource
    """Resource for accessing purchase orders data."""
    suppliers: SuppliersResource
    """Resource for accessing suppliers directory data."""
    buyers: BuyersResource
    """Resource for accessing buyers directory data."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize the MarketClient with the provided API key.

        Parameters
        ----------
        api_key : str
            The API key to authenticate requests with the Public Market API.
        """
        self._transport: MarketTransport = BaseMarketClient(api_key)

        self.raw = RawMarketResource(self._transport)
        self.tenders = TendersResource(self._transport, spec=TENDER_SPEC)
        self.orders = OrdersResource(self._transport, spec=ORDER_SPEC)
        self.suppliers = SuppliersResource(self._transport, spec=SUPPLIER_SPEC)
        self.buyers = BuyersResource(self._transport, spec=BUYER_SPEC)

    @property
    def api_key(self) -> str:
        """Get the API key used by the client."""
        return self._transport.api_key

    @property
    def base_url(self) -> str:
        """Get the base URL used by the client."""
        return self._transport.base_url


class AsyncMarketClient:
    """Asynchronous client for interacting with the Public Market API (ChileCompra)."""

    raw: AsyncRawMarketResource
    """Resource for accessing raw market API requests."""
    tenders: AsyncTendersResource
    """Resource for accessing tender data."""
    orders: AsyncOrdersResource
    """Resource for accessing purchase orders data."""
    suppliers: AsyncSuppliersResource
    """Resource for accessing suppliers directory data."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize the AsyncMarketClient with the provided API key.

        Parameters
        ----------
        api_key : str
            The API key to authenticate requests with the Public Market API.
        """
        self._transport: MarketTransport = BaseMarketClient(api_key)

        self.raw = AsyncRawMarketResource(self._transport)
        self.tenders = AsyncTendersResource(self._transport, spec=TENDER_SPEC)
        self.orders = AsyncOrdersResource(self._transport, spec=ORDER_SPEC)
        self.suppliers = AsyncSuppliersResource(self._transport, spec=SUPPLIER_SPEC)

    @property
    def api_key(self) -> str:
        """Get the API key used by the client."""
        return self._transport.api_key

    @property
    def base_url(self) -> str:
        """Get the base URL used by the client."""
        return self._transport.base_url
