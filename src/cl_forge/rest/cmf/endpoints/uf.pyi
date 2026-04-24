from typing import Literal, overload

from cl_forge.core.types import RangeMode
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

@overload
def uf_range_endpoint(
    *,
        start_year: int,
        start_month: int | None = ...,
        end_year: None = ...,
        end_month: None = ...,
        day: None = ...,
        mode: Literal["after", "before"]
) -> CmfEndpoint[ListUfRecord]: ...
@overload
def uf_range_endpoint(
    *,
        start_year: int,
        start_month: int,
        end_year: None = ...,
        end_month: None = ...,
        day: int | None = ...,
        mode: Literal["after", "before"]
) -> CmfEndpoint[ListUfRecord]: ...
@overload
def uf_range_endpoint(
    *,
        start_year: int,
        start_month: None = ...,
        end_year: int,
        end_month: None = ...,
        day: None = ...,
        mode: Literal["between"]
) -> CmfEndpoint[ListUfRecord]: ...
@overload
def uf_range_endpoint(
    *,
        start_year: int,
        start_month: int,
        end_year: int,
        end_month: int,
        day: None = ...,
        mode: Literal["between"]
) -> CmfEndpoint[ListUfRecord]: ...
@overload
def uf_range_endpoint(
        *,
        start_year: int,
        start_month: int | None = ...,
        end_year: int | None = ...,
        end_month: int | None = ...,
        day: int | None = ...,
        mode: RangeMode = ...
) -> CmfEndpoint[ListUfRecord]: ...
