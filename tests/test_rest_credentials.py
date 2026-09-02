from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

import cl_forge
from cl_forge.rest.auth import (
    ApiKeyCredentials,
    ApiProvider,
    CredentialScope,
    CredentialsProvider,
    DotEnvCredentials,
    DotEnvCredentialsError,
    EnvCredentials,
    EnvCredentialsError,
    StaticCredentials,
)


def test_provider_scope_uses_one_enum_with_compatibility_alias():
    assert CredentialScope is ApiProvider
    assert ApiProvider.CMF.value == "cmf"
    assert ApiProvider.MARKET.value == "market"


@pytest.mark.parametrize("value", ["", " ", "\t\n"])
def test_static_credentials_reject_blank_api_keys(value: str):
    with pytest.raises(ValidationError, match="API key must not be blank"):
        StaticCredentials(value)


def test_static_credentials_normalize_and_mask_api_key():
    provider = StaticCredentials(SecretStr("  private-ticket  "))
    credentials = provider.resolve(ApiProvider.MARKET)

    assert credentials.value == "private-ticket"
    assert credentials.api_key.get_secret_value() == "private-ticket"
    assert "private-ticket" not in repr(provider)
    assert "private-ticket" not in repr(credentials)


def test_environment_credentials_resolve_provider_specific_key(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CLFORGE_CMF_API_KEY", "  cmf-secret  ")
    monkeypatch.setenv("CLFORGE_MARKET_API_KEY", "market-secret")

    provider = EnvCredentials()

    assert provider.resolve(ApiProvider.CMF).value == "cmf-secret"
    assert provider.resolve(ApiProvider.MARKET).value == "market-secret"


def test_environment_credentials_raise_specific_error(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("CLFORGE_CMF_API_KEY", raising=False)

    with pytest.raises(EnvCredentialsError, match="CLFORGE_CMF_API_KEY"):
        EnvCredentials().resolve(ApiProvider.CMF)


def test_dotenv_credentials_use_last_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("CLFORGE_CMF_API_KEY", raising=False)
    first = tmp_path / "first.env"
    second = tmp_path / "second.env"
    first.write_text("CLFORGE_CMF_API_KEY=first\n", encoding="utf-8")
    second.write_text("CLFORGE_CMF_API_KEY=second\n", encoding="utf-8")

    provider = DotEnvCredentials(env_file=(first, second))

    assert provider.resolve(ApiProvider.CMF).value == "second"


def test_dotenv_credentials_raise_specific_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("CLFORGE_MARKET_API_KEY", raising=False)
    env_file = tmp_path / "empty.env"
    env_file.write_text("UNRELATED=value\n", encoding="utf-8")

    with pytest.raises(DotEnvCredentialsError, match="CLFORGE_MARKET_API_KEY"):
        DotEnvCredentials(env_file).resolve(ApiProvider.MARKET)


def test_root_exports_environment_providers():
    assert cl_forge.DotEnvCredentials is DotEnvCredentials
    assert cl_forge.EnvCredentials is EnvCredentials


@pytest.mark.parametrize(
    ("client_type", "scope", "route_count"),
    [
        (cl_forge.CmfClient, ApiProvider.CMF, 1),
        (cl_forge.AsyncCmfClient, ApiProvider.CMF, 1),
        (cl_forge.MarketClient, ApiProvider.MARKET, 2),
        (cl_forge.AsyncMarketClient, ApiProvider.MARKET, 2),
    ],
)
def test_public_clients_accept_credentials_and_resolve_once(client_type, scope, route_count):
    calls: list[ApiProvider] = []

    class CountingProvider(CredentialsProvider):
        def resolve(self, requested_scope: ApiProvider) -> ApiKeyCredentials:
            calls.append(requested_scope)
            return ApiKeyCredentials(api_key=SecretStr("secret"))

    client = client_type(credentials=CountingProvider())

    assert client.credentials.value == "secret"
    assert len(client._routes) == route_count
    assert calls == [scope]


def test_api_key_credentials_are_immutable():
    credentials = ApiKeyCredentials(api_key=SecretStr("secret"))

    with pytest.raises(FrozenInstanceError, match="cannot assign"):
        credentials.api_key = SecretStr("replacement")  # type: ignore[misc]
