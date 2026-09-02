import asyncio
from collections.abc import Iterator
from typing import ClassVar

import pytest
from httpx2 import AsyncClient, Client, Request
from pydantic import SecretStr

from cl_forge.rest.auth import ApiKeyCredentials, ApiProvider, CredentialsProvider
from cl_forge.rest.auth.apikey import ApiKeyAuth
from cl_forge.rest.auth.enums import AuthLocation, AuthScheme
from cl_forge.rest.auth.spec import AuthSpec
from cl_forge.rest.client.base import ApiClient
from cl_forge.rest.client.builder import ClientBuilder
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.client.registry import AsyncClientKey, ClientRegistry, SyncClientKey
from cl_forge.rest.cmf.provider import CMF_V3
from cl_forge.rest.market.provider import MARKET_V1
from cl_forge.rest.provider import ProviderSpec


class IsolatedRegistry(ClientRegistry):
    sync_clients: ClassVar[dict[SyncClientKey, Client]] = {}
    async_clients: ClassVar[dict[AsyncClientKey, AsyncClient]] = {}


class IsolatedApiClient(ApiClient):
    registry = IsolatedRegistry


@pytest.fixture(autouse=True)
def close_isolated_clients() -> Iterator[None]:
    yield
    for client in IsolatedRegistry.sync_clients.values():
        client.close()
    IsolatedRegistry.sync_clients.clear()
    IsolatedRegistry.async_clients.clear()


def test_facade_resolves_credentials_once_for_same_provider_family():
    calls: list[ApiProvider] = []

    class CountingProvider(CredentialsProvider):
        def resolve(self, scope: ApiProvider) -> ApiKeyCredentials:
            calls.append(scope)
            return ApiKeyCredentials(api_key=SecretStr("secret"))

    cmf_v4 = ProviderSpec(
        family=ApiProvider.CMF,
        version=4,
        base_url="https://example.test/cmf/v4",
        auth=CMF_V3.auth,
    )
    client = IsolatedApiClient(CountingProvider())

    first = client._route(CMF_V3)
    assert client._route(CMF_V3) is first
    client._route(cmf_v4)

    assert calls == [ApiProvider.CMF]
    assert client.credentials.value == "secret"


def test_facade_rejects_mixed_provider_families():
    client = IsolatedApiClient("secret")
    client._route(CMF_V3)

    with pytest.raises(ValueError, match="cannot mix"):
        client._route(MARKET_V1)


def test_registry_reuses_clients_by_resolved_credential_fingerprint():
    first_facade = IsolatedApiClient("same-secret")
    second_facade = IsolatedApiClient(SecretStr("same-secret"))

    first = first_facade._route(CMF_V3).client
    second = second_facade._route(CMF_V3).client

    assert first is second
    key = next(iter(IsolatedRegistry.sync_clients))
    assert "same-secret" not in repr(key)


def test_registry_separates_distinct_credentials():
    first = IsolatedApiClient("first")._route(CMF_V3).client
    second = IsolatedApiClient("second")._route(CMF_V3).client

    assert first is not second
    assert len(IsolatedRegistry.sync_clients) == 2


def test_registry_reuses_async_client_in_same_event_loop():
    async def exercise_registry() -> None:
        first_facade = IsolatedApiClient("same-secret")
        second_facade = IsolatedApiClient(SecretStr("same-secret"))

        first = first_facade._route(CMF_V3).aclient
        second = second_facade._route(CMF_V3).aclient
        try:
            assert first is second
            assert len(IsolatedRegistry.async_clients) == 1
        finally:
            await first.aclose()

    asyncio.run(exercise_registry())


def test_client_builder_repr_does_not_reveal_credentials():
    credentials = ApiKeyCredentials(api_key=SecretStr("private"))
    builder = ClientBuilder(CMF_V3, ClientConfig(), credentials)
    key = SyncClientKey.create(CMF_V3, ClientConfig(), credentials)

    assert "private" not in repr(builder)
    assert "private" not in repr(key)


def test_api_key_auth_adds_query_credential():
    credentials = ApiKeyCredentials(api_key=SecretStr("private"))
    auth = ApiKeyAuth(
        AuthSpec(label="apikey", location=AuthLocation.QUERY),
        credentials,
    )
    request = Request("GET", "https://example.test/data?existing=value")

    authenticated = next(auth.auth_flow(request))

    assert authenticated.url.params["existing"] == "value"
    assert authenticated.url.params["apikey"] == "private"


def test_api_key_auth_adds_schemed_header_credential():
    credentials = ApiKeyCredentials(api_key=SecretStr("private"))
    auth = ApiKeyAuth(
        AuthSpec(
            label="Authorization",
            location=AuthLocation.HEADER,
            scheme=AuthScheme.BEARER,
        ),
        credentials,
    )
    request = Request("GET", "https://example.test/data")

    authenticated = next(auth.auth_flow(request))

    assert authenticated.headers["Authorization"] == "Bearer private"
