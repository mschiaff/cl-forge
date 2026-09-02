from httpx2 import AsyncClient, Client

from cl_forge.rest.auth.base import ApiKeyCredentials
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.client.registry import ClientRegistry
from cl_forge.rest.provider import ProviderSpec


class ClientRoute:
    """Lazy access to sync and async clients for one provider version."""

    def __init__(
        self,
        provider: ProviderSpec,
        credentials: ApiKeyCredentials,
        config: ClientConfig,
        registry: type[ClientRegistry],
    ) -> None:
        self.provider = provider
        self._credentials = credentials
        self._config = config
        self._registry = registry

    @property
    def client(self) -> Client:
        """Return the lazy shared synchronous client."""
        return self._registry.get_sync(self.provider, self._config, self._credentials)

    @property
    def aclient(self) -> AsyncClient:
        """Return the lazy shared asynchronous client."""
        return self._registry.get_async(self.provider, self._config, self._credentials)
