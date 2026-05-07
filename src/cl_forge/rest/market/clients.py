from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import BaseMarketClient
from .resources.directory import (
    AsyncBuyersResource,
    AsyncSuppliersResource,
    BuyersResource,
    SuppliersResource,
)
from .resources.orders import AsyncOrdersResource, OrdersResource
from .resources.raw import AsyncRawMarketResource, RawMarketResource
from .resources.tenders import AsyncTendersResource, TendersResource
from .specs.directory import BUYER_SPEC, SUPPLIER_SPEC
from .specs.orders import ORDER_SPEC
from .specs.tenders import TENDER_SPEC

if TYPE_CHECKING:
    from ..auth import ApiKeyCredentials, CredentialType
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

    def __init__(self, credentials: CredentialType) -> None:
        """
        Initialize the MarketClient with the provided credentials.

        Parameters
        ----------
        credentials : CredentialType
            The credentials to use for the client, which can be a `str`,
            `SecretStr`, or `CredentialsProvider`.
        """
        self._transport: MarketTransport = BaseMarketClient(credentials)

        self.raw = RawMarketResource(self._transport)
        self.tenders = TendersResource(self._transport, spec=TENDER_SPEC)
        self.orders = OrdersResource(self._transport, spec=ORDER_SPEC)
        self.suppliers = SuppliersResource(self._transport, spec=SUPPLIER_SPEC)
        self.buyers = BuyersResource(self._transport, spec=BUYER_SPEC)

    @property
    def base_url(self) -> str:
        """Get the base URL for the Market API."""
        return self._transport.base_url

    @property
    def credentials(self) -> ApiKeyCredentials:
        """Get the credentials used by the MarketClient."""
        return self._transport.credentials

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(base_url={self.base_url!r}, "
            f"credentials={self.credentials})"
        )


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
    buyers: AsyncBuyersResource
    """Resource for accessing buyers directory data."""

    def __init__(self, credentials: CredentialType) -> None:
        """
        Initialize the AsyncMarketClient with the provided credentials.

        Parameters
        ----------
        credentials : CredentialType
            The credentials to use for the client, which can be a `str`,
            `SecretStr`, or `CredentialsProvider`.
        """
        self._transport: MarketTransport = BaseMarketClient(credentials)

        self.raw = AsyncRawMarketResource(self._transport)
        self.tenders = AsyncTendersResource(self._transport, spec=TENDER_SPEC)
        self.orders = AsyncOrdersResource(self._transport, spec=ORDER_SPEC)
        self.suppliers = AsyncSuppliersResource(self._transport, spec=SUPPLIER_SPEC)
        self.buyers = AsyncBuyersResource(self._transport, spec=BUYER_SPEC)

    @property
    def base_url(self) -> str:
        """Get the base URL for the Market API."""
        return self._transport.base_url

    @property
    def credentials(self) -> ApiKeyCredentials:
        """Get the credentials used by the MarketClient."""
        return self._transport.credentials

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}"
            f"(base_url={self.base_url!r}, "
            f"credentials={self.credentials})"
        )
