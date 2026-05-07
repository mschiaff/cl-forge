from __future__ import annotations

from typing import Any, Self

from pydantic import SecretStr

from cl_forge.core.impl.cmf import CoreCmfClient
from cl_forge.core.impl.market import CoreMarketClient

from .auth import (
    ApiKeyCredentials,
    CredentialScope,
    CredentialsProvider,
    CredentialType,
    StaticCredentials,
)

__all__ = ("BaseCmfClient", "BaseMarketClient",)


def as_credentials_provider(credentials: CredentialType) -> CredentialsProvider:
    """
    Convert a `CredentialType` to a `CredentialsProvider`.

    Parameters
    ----------
    credentials : CredentialType
        The credentials to convert, which can be a `str`,
        `SecretStr`, or `CredentialsProvider`.

    Returns
    -------
    CredentialsProvider
        A `CredentialsProvider` instance corresponding to
        the given credentials.
    """
    if isinstance(credentials, (str, SecretStr)):
        return StaticCredentials(api_key=credentials)
    return credentials


class CoreClientMeta(type):
    immutable_attrs: frozenset[str] = frozenset({"_scope"})

    def __setattr__(cls, name: str, value: Any) -> None:
        if name in cls.immutable_attrs and hasattr(cls, name):
            raise AttributeError(f"{name!r} is immutable.")
        super().__setattr__(name, value)


class CoreClientMixin(metaclass=CoreClientMeta):
    def __setattr__(self, name: str, value: Any) -> None:
        if name in type(self).immutable_attrs and hasattr(self, name):
            raise AttributeError(f"{name!r} is immutable.")
        super().__setattr__(name, value)


class BaseMarketClient(CoreClientMixin, CoreMarketClient):
    _scope: CredentialScope = CredentialScope.MARKET
    """Client scope for credential resolution."""
    credentials: ApiKeyCredentials
    """The resolved credentials used by the client."""

    def __new__(cls, credentials: CredentialType) -> Self:
        provider = as_credentials_provider(credentials)
        resolved = provider.resolve(cls._scope)

        self = super().__new__(cls, api_key=resolved.value)
        self.credentials = resolved
        return self

    def __init__(self, credentials: CredentialType) -> None: ...


class BaseCmfClient(CoreClientMixin, CoreCmfClient):
    _scope: CredentialScope = CredentialScope.CMF
    """Client scope for credential resolution."""
    credentials: ApiKeyCredentials
    """The resolved credentials used by the client."""

    def __new__(cls, credentials: CredentialType) -> Self:
        provider = as_credentials_provider(credentials)
        resolved = provider.resolve(cls._scope)

        self = super().__new__(cls, api_key=resolved.value)
        self.credentials = resolved
        return self

    def __init__(self, credentials: CredentialType) -> None: ...
