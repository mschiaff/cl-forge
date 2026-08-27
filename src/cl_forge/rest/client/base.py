from typing import ClassVar

from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.client.registry import ClientRegistry
from cl_forge.rest.client.route import ClientRoute
from cl_forge.rest.provider import ProviderSpec


class ApiClient:
    """Base facade that groups provider routes."""

    registry: ClassVar[type[ClientRegistry]] = ClientRegistry

    def __init__(self, apikey: str, config: ClientConfig | None = None) -> None:
        self._apikey = apikey
        self._config = config or ClientConfig()
        self._routes: dict[ProviderSpec, ClientRoute] = {}

    def route(self, provider: ProviderSpec) -> ClientRoute:
        """Return one cached, still-lazy route."""
        route = self._routes.get(provider)
        if route is None:
            _args = (self._apikey, self._config, self.registry)
            route = ClientRoute(provider, *_args)
            self._routes[provider] = route
        return route
