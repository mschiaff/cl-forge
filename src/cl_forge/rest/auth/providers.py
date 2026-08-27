from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

from pydantic import SecretStr, ValidationError
from pydantic.dataclasses import dataclass

from cl_forge.rest.auth.base import ApiKeyCredentials, ApiKeySettings, CredentialsProvider
from cl_forge.rest.auth.exceptions import DotEnvCredentialsError, EnvCredentialsError
from cl_forge.rest.auth.types import DotenvType  # noqa: TC001

if TYPE_CHECKING:
    from cl_forge.rest.auth.enums import ApiProvider
    from cl_forge.rest.auth.types import CredentialType


@dataclasses.dataclass(frozen=True, init=False, slots=True)
class StaticCredentials(CredentialsProvider):
    """Credentials provider for an explicitly supplied API key."""

    api_key: SecretStr

    def __init__(self, api_key: str | SecretStr) -> None:
        """Create a static provider.

        Parameters
        ----------
        api_key : str | SecretStr
            API key to resolve for any provider scope.
        """
        secret = api_key if isinstance(api_key, SecretStr) else SecretStr(api_key)
        normalized = ApiKeyCredentials(api_key=secret).api_key
        object.__setattr__(self, "api_key", normalized)

    def resolve(self, scope: ApiProvider) -> ApiKeyCredentials:
        """Return the static credentials for any provider scope."""
        return ApiKeyCredentials(api_key=self.api_key)


@dataclass(frozen=True, slots=True)
class EnvCredentials(CredentialsProvider):
    """Credentials provider backed by environment variables."""

    def resolve(self, scope: ApiProvider) -> ApiKeyCredentials:
        """Resolve ``CLFORGE_<SCOPE>_API_KEY``."""
        env_prefix = self._env_prefix(scope)
        try:
            settings = ApiKeySettings(env_prefix=env_prefix)
        except ValidationError as error:
            raise EnvCredentialsError(env_prefix) from error
        return ApiKeyCredentials(api_key=settings.api_key)


@dataclass(frozen=True, slots=True)
class DotEnvCredentials(CredentialsProvider):
    """Credentials provider backed by one or more dotenv files."""

    env_file: DotenvType = ".env"

    def resolve(self, scope: ApiProvider) -> ApiKeyCredentials:
        """Resolve an API key from the configured dotenv file(s)."""
        env_prefix = self._env_prefix(scope)
        try:
            settings = ApiKeySettings(env_prefix=env_prefix, env_file=self.env_file)
        except ValidationError as error:
            raise DotEnvCredentialsError(env_prefix, self.env_file) from error
        return ApiKeyCredentials(api_key=settings.api_key)


def as_credentials_provider(credentials: CredentialType) -> CredentialsProvider:
    """Normalize supported credential inputs to a provider."""
    if isinstance(credentials, (str, SecretStr)):
        return StaticCredentials(credentials)
    return credentials
