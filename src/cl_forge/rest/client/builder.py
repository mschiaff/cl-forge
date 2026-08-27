import dataclasses

from httpx2 import AsyncClient, AsyncHTTPTransport, Client, HTTPTransport

from cl_forge.rest.auth.apikey import ApiKeyAuth
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.provider import ProviderSpec

type ClientType = Client | AsyncClient
type TransportType = HTTPTransport | AsyncHTTPTransport


@dataclasses.dataclass(slots=True)
class ClientBuilder:
    auth: ApiKeyAuth
    config: ClientConfig
    provider: ProviderSpec

    def __init__(self, provider: ProviderSpec, config: ClientConfig, apikey: str) -> None:
        self.config = config
        self.provider = provider
        self.auth = ApiKeyAuth(spec=self.provider.auth, apikey=apikey)

    def _create[ClientT: ClientType, TransportT: TransportType](
        self,
        client_cls: type[ClientT],
        transport_cls: type[TransportT],
    ) -> ClientT:
        """Create an HTTP client of the specified type with the appropriate transport."""
        transport = transport_cls(http2=self.config.http2, retries=self.config.retries)
        return client_cls(
            auth=self.auth,
            transport=transport,  # type: ignore
            timeout=self.config.timeout,
            base_url=self.provider.base_url,
        )

    def create_sync(self) -> Client:
        """Create a synchronous HTTP client for the specified provider."""
        return self._create(Client, HTTPTransport)

    def create_async(self) -> AsyncClient:
        """Create an asynchronous HTTP client for the specified provider."""
        return self._create(AsyncClient, AsyncHTTPTransport)
