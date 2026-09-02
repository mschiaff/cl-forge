from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, cast

import httpx2
import pytest
from pydantic import ValidationError

from cl_forge.rest.auth.enums import ApiProvider
from cl_forge.rest.cmf.clients import AsyncCmfClient, CmfClient
from cl_forge.rest.cmf.models.indexes import EurList, EuroList, EuroRecord, EurRecord
from cl_forge.rest.cmf.resources.eur import (
    AsyncEuroResource,
    AsyncEurResource,
    SyncEuroResource,
    SyncEurResource,
)
from cl_forge.rest.cmf.resources.ipc import AsyncIpcResource, SyncIpcResource
from cl_forge.rest.cmf.resources.raw import AsyncRawResource, SyncRawResource
from cl_forge.rest.cmf.resources.tip import AsyncTipResource, SyncTipResource
from cl_forge.rest.cmf.resources.uf import AsyncUfResource, SyncUfResource

if TYPE_CHECKING:
    from cl_forge.rest.client.route import ClientRoute


INDEX_RECORD = {"Valor": "1,23", "Fecha": "2025-03-04"}
RATE_RECORD = {
    "Titulo": "Rate",
    "SubTitulo": "Monthly rate",
    "Valor": "4,50",
    "Fecha": "2025-03-01",
    "Hasta": "2025-03-31",
    "Tipo": 1,
}


class StubRoute:
    def __init__(
        self,
        *,
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


def _sync_route(client: httpx2.Client) -> ClientRoute:
    return cast("ClientRoute", StubRoute(client=client))


def _async_route(client: httpx2.AsyncClient) -> ClientRoute:
    return cast("ClientRoute", StubRoute(aclient=client))


def test_monthly_paths_and_parsing() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json={"IPCs": [INDEX_RECORD]})

    with httpx2.Client(
        base_url="https://example.test/api",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = SyncIpcResource(_sync_route(client))
        assert resource.latest().value == 0.0123
        assert len(resource.year(2025).root) == 1
        assert resource.month(2025, 3).date.day == 4
        resource.after(2025)
        resource.after(2025, 3)
        resource.before(2025)
        resource.before(2025, 3)
        resource.between(2024, 1, 2025, 2)
        resource.between(2024, 2025)
        resource.between(
            start_year=2024,
            start_month=1,
            end_year=2025,
            end_month=2,
        )
        resource.between(start_year=2024, end_year=2025)
        resource.between_years(2024, 2025)

    assert [request.url.path for request in seen] == [
        "/api/ipc",
        "/api/ipc/2025",
        "/api/ipc/2025/03",
        "/api/ipc/posteriores/2025",
        "/api/ipc/posteriores/2025/03",
        "/api/ipc/anteriores/2025",
        "/api/ipc/anteriores/2025/03",
        "/api/ipc/periodo/2024/01/2025/02",
        "/api/ipc/periodo/2024/2025",
        "/api/ipc/periodo/2024/01/2025/02",
        "/api/ipc/periodo/2024/2025",
        "/api/ipc/periodo/2024/2025",
    ]
    assert all(request.url.params["formato"] == "json" for request in seen)


def test_daily_paths_include_exact_day_markers() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json={"UFs": [INDEX_RECORD]})

    with httpx2.Client(
        base_url="https://example.test/api",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = SyncUfResource(_sync_route(client))
        assert len(resource.month(2025, 3).root) == 1
        assert resource.day(2025, 3, 4).value == 1.23
        resource.after(2025, 3, 4)
        resource.before(2025, 3, 4)
        resource.between(2024, 1, 2025, 2)
        resource.between_years(2024, 2025)
        resource.between_days(2024, 1, 2, 2025, 3, 4)

    assert [request.url.path for request in seen] == [
        "/api/uf/2025/03",
        "/api/uf/2025/03/dias/04",
        "/api/uf/posteriores/2025/03/dias/04",
        "/api/uf/anteriores/2025/03/dias/04",
        "/api/uf/periodo/2024/01/2025/02",
        "/api/uf/periodo/2024/2025",
        "/api/uf/periodo/2024/01/dias_i/02/2025/03/dias_f/04",
    ]


def test_rate_paths_and_parsing() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        return httpx2.Response(200, json={"TIPs": [RATE_RECORD]})

    with httpx2.Client(
        base_url="https://example.test/api",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = SyncTipResource(_sync_route(client))
        latest = resource.latest()
        assert latest.root[0].value == 0.045
        assert latest.root[0].date_to is not None
        resource.month(2025, 3)
        resource.after(2025, 3)
        resource.before(2025)
        resource.between(2024, 1, 2025, 2)
        resource.between_years(2024, 2025)

    assert [request.url.path for request in seen] == [
        "/api/tip",
        "/api/tip/2025/03",
        "/api/tip/posteriores/2025/03",
        "/api/tip/anteriores/2025",
        "/api/tip/periodo/2024/01/2025/02",
        "/api/tip/periodo/2024/2025",
    ]


def test_async_resources_have_and_execute_between_methods() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        root = "IPCs" if "/ipc/" in request.url.path else "UFs"
        payload = RATE_RECORD if "/tip/" in request.url.path else INDEX_RECORD
        if "/tip/" in request.url.path:
            root = "TIPs"
        return httpx2.Response(200, json={root: [payload]})

    async def run() -> None:
        async with httpx2.AsyncClient(
            base_url="https://example.test/api",
            transport=httpx2.MockTransport(handler),
        ) as client:
            route = _async_route(client)
            await AsyncIpcResource(route).between(2024, 1, 2025, 2)
            await AsyncIpcResource(route).between(2024, 2025)
            await AsyncUfResource(route).between(2024, 1, 2025, 2)
            await AsyncUfResource(route).between_days(2024, 1, 2, 2025, 3, 4)
            await AsyncTipResource(route).between(2024, 1, 2025, 2)

    asyncio.run(run())
    assert [request.url.path for request in seen] == [
        "/api/ipc/periodo/2024/01/2025/02",
        "/api/ipc/periodo/2024/2025",
        "/api/uf/periodo/2024/01/2025/02",
        "/api/uf/periodo/2024/01/dias_i/02/2025/03/dias_f/04",
        "/api/tip/periodo/2024/01/2025/02",
    ]


@pytest.mark.parametrize(
    "operation",
    [
        lambda resource: resource.year(-1),
        lambda resource: resource.month(2025, 0),
        lambda resource: resource.month(2025, 13),
        lambda resource: resource.day(2025, 1, 0),
        lambda resource: resource.day(2025, 1, 32),
    ],
)
def test_date_components_are_validated_at_runtime(operation: Any) -> None:
    with httpx2.Client(base_url="https://example.test") as client:
        resource = SyncUfResource(_sync_route(client))
        with pytest.raises(ValidationError):
            operation(resource)


def test_daily_day_filters_require_a_month() -> None:
    with httpx2.Client(base_url="https://example.test") as client:
        resource = SyncUfResource(_sync_route(client))
        with pytest.raises(ValueError, match="Month is required"):
            resource.after(2025, day=1)
        with pytest.raises(ValueError, match="Month is required"):
            resource.before(2025, day=1)


@pytest.mark.parametrize(
    ("payload", "error", "message"),
    [
        ({}, ValueError, "Missing CMF response root"),
        ({"IPCs": {}}, TypeError, "contain a list"),
        ({"IPCs": [INDEX_RECORD, INDEX_RECORD]}, ValueError, "exactly one record"),
    ],
)
def test_structured_response_shape_is_checked(
    payload: dict[str, object],
    error: type[Exception],
    message: str,
) -> None:
    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json=payload)

    with httpx2.Client(
        base_url="https://example.test",
        transport=httpx2.MockTransport(handler),
    ) as client:
        resource = SyncIpcResource(_sync_route(client))
        with pytest.raises(error, match=message):
            resource.latest()


def test_async_raw_formats_and_raw_validation() -> None:
    seen: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request)
        if request.url.params["formato"] == "xml":
            return httpx2.Response(200, content=b"<records />")
        return httpx2.Response(200, json={"ok": True})

    async def run() -> None:
        async with httpx2.AsyncClient(
            base_url="https://example.test/api",
            transport=httpx2.MockTransport(handler),
        ) as client:
            resource = AsyncRawResource(_async_route(client))
            assert await resource.json.get("/raw") == {"ok": True}
            assert await resource.xml.get("/raw") == "<records />"
            with pytest.raises(ValueError, match="cannot be empty"):
                await resource.json.get("  ")
            with pytest.raises(ValueError, match="must start"):
                await resource.json.get("raw")
            with pytest.raises(ValueError, match="Reserved query parameters"):
                await resource.json.get("/raw", params={"Formato": "xml"})

    asyncio.run(run())
    assert [request.url.params["formato"] for request in seen] == ["json", "xml"]


def test_raw_json_rejects_non_object_payloads() -> None:
    def handler(_request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json=[])

    with httpx2.Client(
        base_url="https://example.test",
        transport=httpx2.MockTransport(handler),
    ) as client:
        with pytest.raises(TypeError, match="JSON object"):
            SyncRawResource(_sync_route(client)).json.get("/raw")


@pytest.mark.parametrize("client_type", [CmfClient, AsyncCmfClient])
def test_client_surface_credentials_and_compatibility(client_type: Any) -> None:
    client = client_type(credentials="private-secret")

    assert client.provider is ApiProvider.CMF
    assert client.base_url.endswith("/recursos_api")
    assert client.credentials.value == "private-secret"
    assert client.euro is client.eur
    assert EuroRecord is EurRecord
    assert EuroList is EurList
    assert SyncEuroResource is SyncEurResource
    assert AsyncEuroResource is AsyncEurResource
    assert {
        "raw",
        "ipc",
        "uf",
        "utm",
        "usd",
        "eur",
        "euro",
        "tip",
        "tmc",
    } <= set(vars(client))
    assert "private-secret" not in repr(client)
