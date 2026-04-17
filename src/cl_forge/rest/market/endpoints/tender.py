from __future__ import annotations

from pydantic import BaseModel, Field

from cl_forge.rest.market.endpoints.base import MarketEndpoint
from cl_forge.rest.market.schemas import TenderDetailsResponse, TenderResponse


class TendersParams(BaseModel):
    date: str | None = Field(
        default=None,
        serialization_alias="fecha"
    )
    status: str | None = Field(
        default=None,
        serialization_alias="estado"
    )
    provider_code: int | None = Field(
        default=None,
        serialization_alias="CodigoProveedor"
    )
    organism_code: int | None = Field(
        default=None,
        serialization_alias="CodigoOrganismo"
    )


def tenders_endpoint(
        *,
        date: str | None = None,
        status: str | None = None,
        provider_code: int | None = None,
        organism_code: int | None = None,
) -> MarketEndpoint[TenderResponse]:
    params = TendersParams(
        date=date,
        status=status,
        provider_code=provider_code,
        organism_code=organism_code,
    ).model_dump(
        exclude_none=True,
        by_alias=True
    )
    return MarketEndpoint(
        path="/licitaciones",
        model=TenderResponse,
        params=params
    )


class TenderDetailsParams(BaseModel):
    code: str = Field(
        serialization_alias="codigo"
    )


def tender_details_endpoint(
        code: str
) -> MarketEndpoint[TenderDetailsResponse]:
    params = TenderDetailsParams(
        code=code
    ).model_dump(
        by_alias=True
    )
    return MarketEndpoint(
        path="/licitaciones",
        model=TenderDetailsResponse,
        params=params
    )
