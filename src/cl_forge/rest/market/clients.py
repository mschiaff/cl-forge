from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.impl.market import BaseMarketClient

from .resources.directory import BuyersResource, SuppliersResource
from .resources.orders import OrdersResource
from .resources.raw import RawMarketResource
from .resources.tenders import TendersResource
from .specs.directory import BUYER_SPEC, SUPPLIER_SPEC
from .specs.orders import ORDER_SPEC
from .specs.tenders import TENDER_SPEC

if TYPE_CHECKING:
    from .types import MarketTransport


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
        self._transport: MarketTransport = BaseMarketClient(api_key)

        self.raw = RawMarketResource(self._transport)
        self.tenders = TendersResource(self._transport, spec=TENDER_SPEC)
        self.orders = OrdersResource(self._transport, spec=ORDER_SPEC)
        self.suppliers = SuppliersResource(self._transport, spec=SUPPLIER_SPEC)
        self.buyers = BuyersResource(self._transport, spec=BUYER_SPEC)

    @property
    def api_key(self) -> str:
        return self._transport.api_key

    @property
    def base_url(self) -> str:
        return self._transport.base_url
