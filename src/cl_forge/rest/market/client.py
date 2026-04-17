from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cl_forge.core.impl.rs_cl_forge.rs_market import (  # type: ignore
    MarketClient as _RSMarketClient,
)
from cl_forge.rest.market.endpoints import tender

if TYPE_CHECKING:
    from cl_forge.rest.market.schemas import TenderDetailsResponse, TenderResponse


class MarketClient(_RSMarketClient):
    def tenders(
            self,
            *,
            date: str | None = None,
            status: str | None = None,
            provider_code: int | None = None,
            organism_code: int | None = None,
            raw: bool = False,
    ) -> TenderResponse | dict[str, Any]:
        endpoint = tender.tenders_endpoint(
            date=date,
            status=status,
            provider_code=provider_code,
            organism_code=organism_code,
        )
        response = self.get(
            path=endpoint.path,
            params=endpoint.params
        )
        if raw:
            return response
        return endpoint.model.model_validate(response)

    def tender_details(
            self, *,
            code: str,
            raw: bool = False,
    ) -> TenderDetailsResponse | dict[str, Any]:
        endpoint = tender.tender_details_endpoint(
            code=code
        )
        response = self.get(
            path=endpoint.path,
            params=endpoint.params
        )
        if raw:
            return response
        return endpoint.model.model_validate(response)
