from typing import Any

from httpx2 import Response

from cl_forge.rest.market.resources.base import MarketResource
from cl_forge.rest.resources.base import AsyncResource, ResourceSpec, SyncResource
from cl_forge.rest.resources.formats import PathExtensionFormat

TENDERS_CONFIG = ResourceSpec(endpoint="/licitaciones")


class TenderHandler(MarketResource):
    _format_policy = PathExtensionFormat()

    def _parse_all(self, response: Response) -> dict[str, Any]:
        return response.json()


class TenderResource(TenderHandler, SyncResource):
    _format_policy = PathExtensionFormat()

    def all(self) -> dict[str, Any]:
        """Fetch all tender data."""
        response = self._get()
        return self._parse_all(response)


class AsyncTenderResource(TenderHandler, AsyncResource):
    async def all(self) -> dict[str, Any]:
        """Fetch all tender data."""
        response = await self._get()
        return self._parse_all(response)
