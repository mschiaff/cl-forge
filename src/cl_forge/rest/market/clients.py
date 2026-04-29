from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.impl.market import BaseMarketClient

from .resources.raw import RawMarketResource
from .resources.tenders import TendersResource
from .specs.tenders import TENDER_SPEC

if TYPE_CHECKING:
    from .types import MarketTransport


class MarketClient:
    def __init__(self, api_key: str) -> None:
        self._transport: MarketTransport = BaseMarketClient(api_key)

        self.raw = RawMarketResource(self._transport)
        self.tenders = TendersResource(self._transport, spec=TENDER_SPEC)

    @property
    def api_key(self) -> str:
        return self._transport.api_key

    @property
    def base_url(self) -> str:
        return self._transport.base_url
