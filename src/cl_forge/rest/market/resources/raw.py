from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from cl_forge.rest.market.resources.base import MarketResource
from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import FixedJsonFormat, PathExtensionFormat

if TYPE_CHECKING:
    from httpx2 import Response

    from cl_forge.rest.client.route import ClientRoute
    from cl_forge.rest.resources.types import QueryParams


RAW_SPEC = ResourceSpec(endpoint="/")


class RawJsonHandler:
    @staticmethod
    def _parse_json(response: Response) -> dict[str, Any]:
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise TypeError("Expected the Market API to return a JSON object")
        return cast("dict[str, Any]", data)


class RawV1Handler(MarketResource[ResourceSpec]):
    _spec = RAW_SPEC
    _format_policy = PathExtensionFormat()


class RawJsonResource(RawJsonHandler, RawV1Handler, SyncResource[ResourceSpec]):
    """Synchronous raw JSON access to Market API v1."""

    def get(self, path: str, params: QueryParams | None = None) -> dict[str, Any]:
        return self._parse_json(self._get(endpoint=path, params=params, fmt="json"))


class RawXmlResource(RawV1Handler, SyncResource[ResourceSpec]):
    """Synchronous raw XML access to Market API v1."""

    def get(self, path: str, params: QueryParams | None = None) -> str:
        response = self._get(endpoint=path, params=params, fmt="xml")
        return response.text


class AsyncRawJsonResource(RawJsonHandler, RawV1Handler, AsyncResource[ResourceSpec]):
    """Asynchronous raw JSON access to Market API v1."""

    async def get(self, path: str, params: QueryParams | None = None) -> dict[str, Any]:
        return self._parse_json(await self._get(endpoint=path, params=params, fmt="json"))


class AsyncRawXmlResource(RawV1Handler, AsyncResource[ResourceSpec]):
    """Asynchronous raw XML access to Market API v1."""

    async def get(self, path: str, params: QueryParams | None = None) -> str:
        response = await self._get(endpoint=path, params=params, fmt="xml")
        return response.text


class RawV2Handler(MarketResource[ResourceSpec]):
    _spec = RAW_SPEC
    _format_policy = FixedJsonFormat()


class RawV2Resource(RawJsonHandler, RawV2Handler, SyncResource[ResourceSpec]):
    """Synchronous raw JSON access to Market API v2."""

    def get(self, path: str, params: QueryParams | None = None) -> dict[str, Any]:
        return self._parse_json(self._get(endpoint=path, params=params))


class AsyncRawV2Resource(RawJsonHandler, RawV2Handler, AsyncResource[ResourceSpec]):
    """Asynchronous raw JSON access to Market API v2."""

    async def get(self, path: str, params: QueryParams | None = None) -> dict[str, Any]:
        return self._parse_json(await self._get(endpoint=path, params=params))


class RawResource:
    """Grouped raw Market API access for a synchronous client."""

    json: RawJsonResource
    xml: RawXmlResource
    v2: RawV2Resource

    def __init__(self, v1: ClientRoute, v2: ClientRoute) -> None:
        self.json = RawJsonResource(v1)
        self.xml = RawXmlResource(v1)
        self.v2 = RawV2Resource(v2)


class AsyncRawResource:
    """Grouped raw Market API access for an asynchronous client."""

    json: AsyncRawJsonResource
    xml: AsyncRawXmlResource
    v2: AsyncRawV2Resource

    def __init__(self, v1: ClientRoute, v2: ClientRoute) -> None:
        self.json = AsyncRawJsonResource(v1)
        self.xml = AsyncRawXmlResource(v1)
        self.v2 = AsyncRawV2Resource(v2)


__all__ = (
    "RAW_SPEC",
    "AsyncRawJsonResource",
    "AsyncRawResource",
    "AsyncRawV2Resource",
    "AsyncRawXmlResource",
    "RawJsonResource",
    "RawResource",
    "RawV2Resource",
    "RawXmlResource",
)
