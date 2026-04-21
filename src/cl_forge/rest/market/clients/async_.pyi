from typing import Any, Literal, overload

from cl_forge.core.impl.market import BaseMarketClient
from cl_forge.rest.market.schemas import TenderDetailsResponse, TenderResponse

class AsyncMarketClient(BaseMarketClient):
    @overload
    async def tenders(
            self,
            *,
            date: str | None = ...,
            status: str | None = ...,
            provider_code: int | None = ...,
            organism_code: int | None = ...,
            raw: Literal[False] = ...,
    ) -> TenderResponse: ...
    @overload
    async def tenders(
            self,
            *,
            date: str | None = ...,
            status: str | None = ...,
            provider_code: int | None = ...,
            organism_code: int | None = ...,
            raw: Literal[True],
    ) -> dict[str, Any]: ...
    
    async def tenders(
            self,
            *,
            date: str | None = None,
            status: str | None = None,
            provider_code: int | None = None,
            organism_code: int | None = None,
            raw: bool = False,
    ) -> TenderResponse | dict[str, Any]: ...


    @overload
    async def tender_details(
            self,
            *,
            code: str,
            raw: Literal[False] = ...,
    ) -> TenderDetailsResponse: ...
    @overload
    async def tender_details(
            self,
            *,
            code: str,
            raw: Literal[True],
    ) -> dict[str, Any]: ...
    
    async def tender_details(
            self,
            *,
            code: str,
            raw: bool = False,
    ) -> TenderDetailsResponse | dict[str, Any]: ...
