from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Annotated, ClassVar

from pydantic import AfterValidator, SecretStr
from pydantic.dataclasses import dataclass
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from cl_forge.rest.auth.enums import ApiProvider
    from cl_forge.rest.auth.types import DotenvType


def _normalize_api_key(value: SecretStr) -> SecretStr:
    api_key = value.get_secret_value().strip()
    if not api_key:
        raise ValueError("API key must not be blank")
    return SecretStr(api_key)


type ApiKey = Annotated[SecretStr, AfterValidator(_normalize_api_key)]


@dataclass(frozen=True, slots=True)
class CredentialsProvider(ABC):
    """Resolve credentials for a provider API."""

    prefix: ClassVar[str] = "CLFORGE_"

    @abstractmethod
    def resolve(self, scope: ApiProvider) -> ApiKeyCredentials:
        """Resolve credentials for ``scope``."""
        ...

    def _env_prefix(self, scope: ApiProvider) -> str:
        """Build the environment-variable prefix for ``scope``."""
        return f"{self.prefix}{scope.name}_"


@dataclass(frozen=True, slots=True)
class ApiKeyCredentials:
    """Immutable, masked API-key credentials."""

    api_key: ApiKey

    @property
    def value(self) -> str:
        """Return the API key for request authentication."""
        return self.api_key.get_secret_value()


class ApiKeySettings(BaseSettings):
    """Load API-key credentials from settings sources."""

    model_config = SettingsConfigDict(
        extra="ignore",
        env_ignore_empty=True,
        env_file_encoding="utf-8",
    )

    api_key: ApiKey

    def __init__(self, *, env_prefix: str, env_file: DotenvType | None = None) -> None:
        """Load an API key using a dynamic environment prefix.

        Parameters
        ----------
        env_prefix : str
            Prefix used for the ``API_KEY`` setting.
        env_file : DotenvType | None
            Optional dotenv path or ordered paths.
        """
        super().__init__(_env_prefix=env_prefix, _env_file=env_file)
