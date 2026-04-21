from typing import overload

from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import ListUfRecord, UfRecord

@overload
def uf_endpoint(
        *,
        year: None = ...,
        month: None = ...,
        day: None = ...
) -> CmfEndpoint[UfRecord]: ...
@overload
def uf_endpoint(
        *,
        year: int,
        month: None = ...,
        day: None = ...
) -> CmfEndpoint[ListUfRecord]: ...
@overload
def uf_endpoint(
        *,
        year: int,
        month: int,
        day: None = ...
) -> CmfEndpoint[ListUfRecord]: ...
@overload
def uf_endpoint(
        *,
        year: int,
        month: int,
        day: int
) -> CmfEndpoint[UfRecord]: ...
@overload
def uf_endpoint(
        *,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None
) -> CmfEndpoint[UfRecord] | CmfEndpoint[ListUfRecord]: ...