from cl_forge.rest.client.base import ApiClient, ClientConfig
from cl_forge.rest.market.provider import MARKET_V1, MARKET_V2
from cl_forge.rest.market.resources.tenders import (
    TENDERS_CONFIG,
    AsyncTenderResource,
    TenderResource,
)


class MarketClient(ApiClient):
    tender: TenderResource

    def __init__(self, apikey: str, config: ClientConfig | None = None) -> None:
        super().__init__(apikey, config)
        self._v1 = self.route(MARKET_V1)
        self._v2 = self.route(MARKET_V2)

        self.tender = TenderResource(self._v1, TENDERS_CONFIG)


class AsyncMarketClient(ApiClient):
    tender: AsyncTenderResource

    def __init__(self, apikey: str, config: ClientConfig | None = None) -> None:
        super().__init__(apikey, config)
        self._v1 = self.route(MARKET_V1)
        self._v2 = self.route(MARKET_V2)

        self.tender = AsyncTenderResource(self._v1, TENDERS_CONFIG)
