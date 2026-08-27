from cl_forge.rest.client.base import ApiClient
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.cmf.provider import CMF_V3
from cl_forge.rest.cmf.resources.ipc import AsyncIpcResource, SyncIpcResource


class CmfClient(ApiClient):
    """
    Client for interacting with the CMF API.
    """

    ipc: SyncIpcResource

    def __init__(self, apikey: str, config: ClientConfig | None = None) -> None:
        super().__init__(apikey, config)
        self._v3 = self.route(CMF_V3)

        self.ipc = SyncIpcResource(self._v3)


class AsyncCmfClient(ApiClient):
    """
    Asynchronous client for interacting with the CMF API.
    """

    ipc: AsyncIpcResource

    def __init__(self, apikey: str, config: ClientConfig | None = None) -> None:
        super().__init__(apikey, config)
        self._v3 = self.route(CMF_V3)

        self.ipc = AsyncIpcResource(self._v3)
