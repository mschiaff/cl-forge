from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import BaseMarketRawResource

if TYPE_CHECKING:
    from ..types import MarketTransport


class RawMarketJsonResource(BaseMarketRawResource):
    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get(path=path, params=params)


class RawMarketXmlResource(BaseMarketRawResource):
    def get(self, path: str, params: dict[str, Any] | None = None) -> str:
        return self._get(path=path, fmt="xml", params=params)


class RawMarketResource:
    def __init__(self, transport: MarketTransport) -> None:
        self.json = RawMarketJsonResource(transport)
        self.xml = RawMarketXmlResource(transport)
