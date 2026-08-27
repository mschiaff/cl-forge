from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import QueryParameterFormat

if TYPE_CHECKING:
    from httpx2 import Response

    from cl_forge.rest.client.route import ClientRoute
    from cl_forge.rest.resources.types import QueryParams

RAW_SPEC = ResourceSpec(endpoint="/")


class CmfRawHandler:
    _spec = RAW_SPEC
    _reserved_params = frozenset({"apikey"})
    _format_policy = QueryParameterFormat("formato")

    @staticmethod
    def _endpoint(path: str) -> str:
        endpoint = path.strip()
        if not endpoint:
            raise ValueError("Raw CMF path cannot be empty")
        if not endpoint.startswith("/"):
            raise ValueError("Raw CMF path must start with '/'")
        return endpoint

    @staticmethod
    def _parse_json(response: Response) -> dict[str, Any]:
        data = response.json()
        if not isinstance(data, dict):
            raise TypeError("Expected the CMF API to return a JSON object")
        return cast("dict[str, Any]", data)


class SyncRawJsonResource(CmfRawHandler, SyncResource[ResourceSpec]):
    def get(self, path: str, *, params: QueryParams | None = None) -> dict[str, Any]:
        response = self._get(
            endpoint=self._endpoint(path),
            params=params,
            fmt="json",
        )
        return self._parse_json(response)


class SyncRawXmlResource(CmfRawHandler, SyncResource[ResourceSpec]):
    def get(self, path: str, *, params: QueryParams | None = None) -> str:
        response = self._get(
            endpoint=self._endpoint(path),
            params=params,
            fmt="xml",
        )
        return response.text


class SyncRawResource:
    json: SyncRawJsonResource
    xml: SyncRawXmlResource

    def __init__(self, route: ClientRoute) -> None:
        self.json = SyncRawJsonResource(route)
        self.xml = SyncRawXmlResource(route)


class AsyncRawJsonResource(CmfRawHandler, AsyncResource[ResourceSpec]):
    async def get(self, path: str, *, params: QueryParams | None = None) -> dict[str, Any]:
        response = await self._get(
            endpoint=self._endpoint(path),
            params=params,
            fmt="json",
        )
        return self._parse_json(response)


class AsyncRawXmlResource(CmfRawHandler, AsyncResource[ResourceSpec]):
    async def get(self, path: str, *, params: QueryParams | None = None) -> str:
        response = await self._get(
            endpoint=self._endpoint(path),
            params=params,
            fmt="xml",
        )
        return response.text


class AsyncRawResource:
    json: AsyncRawJsonResource
    xml: AsyncRawXmlResource

    def __init__(self, route: ClientRoute) -> None:
        self.json = AsyncRawJsonResource(route)
        self.xml = AsyncRawXmlResource(route)
