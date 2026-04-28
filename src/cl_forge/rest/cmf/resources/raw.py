from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cl_forge.rest.cmf.resources.base import BaseRawResource

if TYPE_CHECKING:
    from cl_forge.rest.cmf.types import CmfTransport


class RawJsonResource(BaseRawResource):
    def get(self, path: str) -> dict[str, Any]:
        """
        Make a raw GET request to the CMF API and return the response as JSON.

        Parameters
        ----------
        path : str
            The path to append to the base CMF API URL for the request.
            Must start with a leading slash.

        Returns
        -------
        dict[str, Any]
            The JSON response from the CMF API as a dictionary.

        Example
        -------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.raw.json.get("/path/to/resource")
        ```
        """
        return self._get(path, raw="json")


class RawXmlResource(BaseRawResource):
    def get(self, path: str) -> str:
        """
        Make a raw GET request to the CMF API and return the response as XML.

        Parameters
        ----------
        path : str
            The path to append to the base CMF API URL for the request.
            Must start with a leading slash.

        Returns
        -------
        str
            The XML response from the CMF API as a string.

        Example
        -------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.raw.xml.get("/path/to/resource")
        ```
        """
        return self._get(path, raw="xml")


class RawResource:
    def __init__(self, transport: CmfTransport) -> None:
        self.json = RawJsonResource(transport)
        """Resource for making raw JSON requests to the CMF API."""
        self.xml = RawXmlResource(transport)
        """Resource for making raw XML requests to the CMF API."""


class AsyncRawJsonResource(BaseRawResource):
    async def get(self, path: str) -> dict[str, Any]:
        """
        Make an async raw GET request to the CMF API and return the response as JSON.

        Parameters
        ----------
        path : str
            The path to append to the base CMF API URL for the request.
            Must start with a leading slash.

        Returns
        -------
        dict[str, Any]
            The JSON response from the CMF API as a dictionary.

        Example
        -------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.raw.json.get("/path/to/resource")
        ```
        """
        return await self._aget(path, raw="json")


class AsyncRawXmlResource(BaseRawResource):
    async def get(self, path: str) -> str:
        """
        Make an async raw GET request to the CMF API and return the response as XML.

        Parameters
        ----------
        path : str
            The path to append to the base CMF API URL for the request.
            Must start with a leading slash.

        Returns
        -------
        str
            The XML response from the CMF API as a string.
        
        Example
        -------
        ```python
        from cl_forge import AsyncCmfClient
        
        client = AsyncCmfClient("your_api_key")
        response = await client.raw.xml.get("/path/to/resource")
        ```
        """
        return await self._aget(path, raw="xml")


class AsyncRawResource:
    def __init__(self, transport: CmfTransport) -> None:
        self.json = AsyncRawJsonResource(transport)
        """Resource for making async raw JSON requests to the CMF API."""
        self.xml = AsyncRawXmlResource(transport)
        """Resource for making async raw XML requests to the CMF API."""
