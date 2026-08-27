import dataclasses

from httpx2 import AsyncClient, AsyncHTTPTransport, Client, HTTPTransport

from cl_forge.rest.auth.apikey import ApiKeyAuth
from cl_forge.rest.auth.base import ApiKeyCredentials
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.provider import ProviderSpec

type ClientType = Client | AsyncClient
type TransportType = HTTPTransport | AsyncHTTPTransport


@dataclasses.dataclass(slots=True)
class ClientBuilder:
    provider: ProviderSpec
    config: ClientConfig
    credentials: ApiKeyCredentials = dataclasses.field(repr=False)
    auth: ApiKeyAuth = dataclasses.field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.auth = ApiKeyAuth(spec=self.provider.auth, credentials=self.credentials)

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
