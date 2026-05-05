from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import BaseMarketResource

if TYPE_CHECKING:
    from ..types import MarketTransport


__all__ = ("AsyncRawMarketResource", "RawMarketResource")


class RawMarketJsonResource(BaseMarketResource):
    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Make a raw GET request to the market API and return the JSON response.

        Parameters
        ----------
        path : str
            The API endpoint path.
        params : dict[str, Any] | None, optional
            Query parameters for the request, by default None

        Returns
        -------
        dict[str, Any]
            The JSON response from the API.

        Examples
        --------
        ```python
        from cl_forge.rest.market import MarketClient

        client = MarketClient(api_key="your_api_key")
        response = client.raw.json.get(path="/licitaciones")
        ```
        """
        return self._get(path=path, params=params)


class RawMarketXmlResource(BaseMarketResource):
    def get(self, path: str, params: dict[str, Any] | None = None) -> str:
        """
        Make a raw GET request to the market API and return the XML response.

        Parameters
        ----------
        path : str
            The API endpoint path.
        params : dict[str, Any] | None, optional
            Query parameters for the request, by default None

        Returns
        -------
        str
            The XML response from the API.

        Examples
        --------
        ```python
        from cl_forge.rest.market import MarketClient

        client = MarketClient(api_key="your_api_key")
        response = client.raw.xml.get(path="/licitaciones")
        ```
        """
        return self._get(path=path, fmt="xml", params=params)


class RawMarketResource:
    json: RawMarketJsonResource
    """Resource for making raw JSON requests to the market API."""
    xml: RawMarketXmlResource
    """Resource for making raw XML requests to the market API."""

    def __init__(self, transport: MarketTransport) -> None:
        self.json = RawMarketJsonResource(transport)
        self.xml = RawMarketXmlResource(transport)


class AsyncRawMarketJsonResource(BaseMarketResource):
    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Make a raw GET request to the market API and return the JSON response.

        Parameters
        ----------
        path : str
            The API endpoint path.
        params : dict[str, Any] | None, optional
            Query parameters for the request, by default None

        Returns
        -------
        dict[str, Any]
            The JSON response from the API.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            response = await client.raw.json.get(path="/licitaciones")

        asyncio.run(main())
        ```
        """
        return await self._aget(path=path, params=params)


class AsyncRawMarketXmlResource(BaseMarketResource):
    async def get(self, path: str, params: dict[str, Any] | None = None) -> str:
        """
        Make a raw GET request to the market API and return the XML response.

        Parameters
        ----------
        path : str
            The API endpoint path.
        params : dict[str, Any] | None, optional
            Query parameters for the request, by default None

        Returns
        -------
        str
            The XML response from the API.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            response = await client.raw.xml.get(path="/licitaciones")

        asyncio.run(main())
        ```
        """
        return await self._aget(path=path, fmt="xml", params=params)


class AsyncRawMarketResource:
    json: AsyncRawMarketJsonResource
    """Resource for making raw JSON requests to the market API."""
    xml: AsyncRawMarketXmlResource
    """Resource for making raw XML requests to the market API."""

    def __init__(self, transport: MarketTransport) -> None:
        self.json = AsyncRawMarketJsonResource(transport)
        self.xml = AsyncRawMarketXmlResource(transport)
