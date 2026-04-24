from typing import Literal, overload

from cl_forge.core.types import RangeMode
from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord

@overload
def ipc_endpoint(
        *,
        year: None = ...
) -> CmfEndpoint[IpcRecord]: ...
@overload
def ipc_endpoint(
        *,
        year: int
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_endpoint(
        *,
        year: int,
        month: int
) -> CmfEndpoint[IpcRecord]: ...
@overload
def ipc_endpoint(
        *,
        year: int | None = ...,
        month: int | None = ...
) -> CmfEndpoint[IpcRecord] | CmfEndpoint[ListIpcRecord]: ...


@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: int | None = ...,
        end_year: None = ...,
        end_month: None = ...,
        mode: Literal["after", "before"]
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: None = ...,
        end_year: int,
        end_month: None = ...,
        mode: Literal["between"]
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: int,
        end_year: int,
        end_month: int,
        mode: Literal["between"]
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: int | None = ...,
        end_year: int | None = ...,
        end_month: int | None = ...,
        mode: RangeMode = ...
) -> CmfEndpoint[ListIpcRecord]: ...
