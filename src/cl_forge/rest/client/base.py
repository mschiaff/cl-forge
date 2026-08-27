from typing import ClassVar

from cl_forge.rest.auth.base import ApiKeyCredentials, CredentialsProvider
from cl_forge.rest.auth.enums import ApiProvider
from cl_forge.rest.auth.providers import as_credentials_provider
from cl_forge.rest.auth.types import CredentialType
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.client.registry import ClientRegistry
from cl_forge.rest.client.route import ClientRoute
from cl_forge.rest.provider import ProviderSpec


class ApiClient:
    """Base facade that groups provider routes."""

    registry: ClassVar[type[ClientRegistry]] = ClientRegistry

    def __init__(self, credentials: CredentialType, config: ClientConfig | None = None) -> None:
        self._credentials_provider: CredentialsProvider = as_credentials_provider(credentials)
        self._credentials: ApiKeyCredentials | None = None
        self._provider: ApiProvider | None = None
        self._config = config or ClientConfig()
        self._routes: dict[ProviderSpec, ClientRoute] = {}

    @property
    def credentials(self) -> ApiKeyCredentials:
        """Return the resolved, masked credentials.

        Credentials are resolved lazily from the first provider route so one
        facade can group multiple versions of that provider without resolving
        the credential source repeatedly.
        """
        if self._credentials is None:
            raise RuntimeError("Credentials have not been resolved; add a provider route first")
        return self._credentials

    def _resolve_credentials(self, provider: ApiProvider) -> ApiKeyCredentials:
        if self._credentials is None:
            self._credentials = self._credentials_provider.resolve(provider)
            self._provider = provider
        elif provider is not self._provider:
            raise ValueError(
                f"A client cannot mix {self._provider!s} and {provider!s} provider routes"
            )
        return self._credentials

    def route(self, provider: ProviderSpec) -> ClientRoute:
        """Return one cached, still-lazy route."""
        route = self._routes.get(provider)
        if route is None:
            credentials = self._resolve_credentials(provider.family)
            _args = (credentials, self._config, self.registry)
            route = ClientRoute(provider, *_args)
            self._routes[provider] = route
        return route
