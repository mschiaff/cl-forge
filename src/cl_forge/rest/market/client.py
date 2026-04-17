from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from cl_forge.core.impl.rs_cl_forge.rs_market import (  # type: ignore
    MarketClient as _RSMarketClient,
)
from cl_forge.rest.market.endpoints.base import MarketEndpoint
from cl_forge.rest.market.schemas import TenderDetails, TenderResponse


class TenderParams(BaseModel):
    date: str | None = Field(default=None, serialization_alias="fecha")
    status: str | None = Field(default=None, serialization_alias="estado")
    provider_code: int | None = Field(default=None, serialization_alias="CodigoProveedor")
    organism_code: int | None = Field(default=None, serialization_alias="CodigoOrganismo")


class MarketClient(_RSMarketClient):
    def tenders(
            self,
            *,
            raw: bool = False,
            date: str | None = None,
            status: str | None = None,
            provider_code: int | None = None,
            organism_code: int | None = None,
    ) -> TenderResponse | dict[str, Any]:
        params = TenderParams(
            date=date,
            status=status,
            provider_code=provider_code,
            organism_code=organism_code,
        ).model_dump(
            exclude_none=True,
            by_alias=True
        )
        endpoint = MarketEndpoint(
            path="/licitaciones", model=TenderResponse, params=params
        )
        response = self.get(path=endpoint.path, params=endpoint.params)
        if raw:
            return response
        return endpoint.model.model_validate(response)

    def tender_details(
            self, code: str, raw: bool = False
    ) -> TenderDetails | dict[str, Any]:
        endpoint = MarketEndpoint(
            path="/licitaciones", model=TenderDetails, params={"codigo": code}
        )
        response = self.get(path=endpoint.path, params=endpoint.params)
        if raw:
            return response
        return endpoint.model.model_validate(response)