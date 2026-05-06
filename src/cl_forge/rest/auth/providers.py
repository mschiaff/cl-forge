from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import SecretStr, ValidationError
from pydantic.dataclasses import dataclass

from .base import ApiKeyCredentials, ApiKeySettings, CredentialsProvider, DotenvType
from .exceptions import DotEnvCredentialsError, EnvCredentialsError

if TYPE_CHECKING:
    from .enums import CredentialScope


__all__ = ("DotEnvCredentials", "EnvCredentials", "StaticCredentials")


@dataclass(frozen=True, slots=True)
class StaticCredentials(CredentialsProvider):
    """Static credentials provider for explicitly defined API key."""

    api_key: SecretStr
    """API key to be used for API client authentication."""

    def __init__(self, api_key: str | SecretStr) -> None:
        """
        Initializes the static credentials provider with the provided API key.

        Parameters
        ----------
        api_key : str | SecretStr
            The API key to be used for authentication. It can be provided as a
            plain string or as a pydantic's `SecretStr` for better security.
        """
        api_key = api_key if isinstance(api_key, SecretStr) else SecretStr(api_key)
        object.__setattr__(self, "api_key", api_key)

    def resolve(self, scope: CredentialScope) -> ApiKeyCredentials:
        # The scope is not used in this provider since the API key
        # is static, but it's included in the method signature for
        # consistency with the base class.
        """
        Resolves the static API key credentials.

        Since the API key is static and provided directly to the constructor,
        the scope parameter is not used in this implementation. However, it
        is included in the method signature to maintain consistency with the
        base class.

        Returns
        -------
        ApiKeyCredentials
             An instance of `ApiKeyCredentials` containing the static API key.
        """
        return ApiKeyCredentials(api_key=self.api_key)


@dataclass(frozen=True, slots=True)
class EnvCredentials(CredentialsProvider):
    """Credentials provider for loading API key from environment variables."""

    def resolve(self, scope: CredentialScope) -> ApiKeyCredentials:
        """
        Resolves the API key credentials from environment variables.

        Parameters
        ----------
        scope : CredentialScope
            The scope for which to resolve the credentials (e.g., CMF, MARKET).

        Returns
        -------
        ApiKeyCredentials
            An instance of `ApiKeyCredentials` containing the API key loaded
            from the environment variable corresponding to the given scope.
        """
        env_prefix = self._env_prefix(scope)

        try:
            settings = ApiKeySettings(env_prefix=env_prefix)
            return ApiKeyCredentials(api_key=settings.api_key)
        except ValidationError as error:
            raise EnvCredentialsError(env_prefix) from error


@dataclass(frozen=True, slots=True)
class DotEnvCredentials(CredentialsProvider):
    """Credentials provider for loading API key from .env files.

    Parameters
    ----------
    env_file : DotenvType, optional
        Path to the .env file from which to load the API key.
        Defaults to '.env'.
    """

    env_file: DotenvType = ".env"
    """Path to the .env file from which to load the API key."""

    def resolve(self, scope: CredentialScope) -> ApiKeyCredentials:
        """
        Resolves the API key credentials from a .env file.

        Parameters
        ----------
        scope : CredentialScope
            The scope for which to resolve the credentials (e.g., CMF, MARKET).

        Returns
        -------
        ApiKeyCredentials
            An instance of `ApiKeyCredentials` containing the API key loaded
            from the .env file corresponding to the given scope.
        """
        env_prefix = self._env_prefix(scope)
        try:
            settings = ApiKeySettings(env_file=self.env_file, env_prefix=env_prefix)
            return ApiKeyCredentials(api_key=settings.api_key)
        except ValidationError as error:
            raise DotEnvCredentialsError(env_prefix, self.env_file) from error
