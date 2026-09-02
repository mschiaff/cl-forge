from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, cast

import httpx2
import pytest

from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import PathExtensionFormat

if TYPE_CHECKING:
    from cl_forge.rest.client.route import ClientRoute
    from cl_forge.rest.resources.types import QueryParams


RESOURCE_SPEC = ResourceSpec(endpoint="/records")


class StubRoute:
    def __init__(
        self,
        client: httpx2.Client | None = None,
        aclient: httpx2.AsyncClient | None = None,
    ) -> None:
        self._client = client
        self._aclient = aclient

    @property
    def client(self) -> httpx2.Client:
        assert self._client is not None
        return self._client

    @property
    def aclient(self) -> httpx2.AsyncClient:
        assert self._aclient is not None
        return self._aclient


class DummySyncResource(SyncResource[ResourceSpec]):
    _spec = RESOURCE_SPEC
    _format_policy = PathExtensionFormat()
    _reserved_params = frozenset({"ticket"})

    def fetch(
        self,
        *segments: str | int,
        params: QueryParams | None = None,
        endpoint: str | None = None,
    ) -> httpx2.Response:
        return self._get(*segments, params=params, endpoint=endpoint)


class DummyAsyncResource(AsyncResource[ResourceSpec]):
    _spec = RESOURCE_SPEC
    _format_policy = PathExtensionFormat()

    async def fetch(self) -> httpx2.Response:
        return await self._get(2026, 3)


def test_resource_builds_formatted_paths_and_copies_query_params() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json={})

    with httpx2.Client(
        base_url="https://example.test/api",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = DummySyncResource(cast("ClientRoute", StubRoute(client=client)))
        params: dict[str, str] = {"status": "active"}
        resource.fetch(2026, 3, params=params)

    assert str(seen[0].url) == "https://example.test/api/records.json/2026/3?status=active"
    assert params == {"status": "active"}


def test_resource_supports_dynamic_raw_endpoints() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json={})

    with httpx2.Client(
        base_url="https://example.test/api",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = DummySyncResource(cast("ClientRoute", StubRoute(client=client)))
        resource.fetch(endpoint="/custom/path")

    assert seen[0].url.path == "/api/custom/path.json"


def test_reserved_parameters_are_case_insensitive() -> None:
    with httpx2.Client(base_url="https://example.test") as client:
        resource = DummySyncResource(cast("ClientRoute", StubRoute(client=client)))

        with pytest.raises(ValueError, match="Reserved query parameters: Ticket"):
            resource.fetch(params={"Ticket": "override"})


def test_resource_raises_for_http_errors() -> None:
    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(404, json={"message": "not found"})

    with httpx2.Client(
        base_url="https://example.test",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = DummySyncResource(cast("ClientRoute", StubRoute(client=client)))

        with pytest.raises(httpx2.HTTPStatusError):
            resource.fetch()


def test_async_resource_uses_the_same_request_pipeline() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json={})

    async def run() -> None:
        async with httpx2.AsyncClient(
            base_url="https://example.test/api",
            transport=httpx2.MockTransport(handler),
        ) as client:
            resource = DummyAsyncResource(cast("ClientRoute", StubRoute(aclient=client)))
            await resource.fetch()

    asyncio.run(run())
    assert seen[0].url.path == "/api/records.json/2026/3"
