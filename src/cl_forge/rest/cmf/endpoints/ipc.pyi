from typing import Never, overload

from cl_forge.core.compat import deprecated
from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import RangeMode

@overload
@deprecated("Month cannot be specified without year.")
def ipc_endpoint(
        year: None = ...,
        month: int = ...
) -> Never: ...
@overload
def ipc_endpoint(
        year: None = ...,
        month: None = ...
) -> CmfEndpoint[IpcRecord]: ...
@overload
def ipc_endpoint(
        year: int,
        month: None = ...
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_endpoint(
        year: int,
        month: int
) -> CmfEndpoint[IpcRecord]: ...
@overload
def ipc_endpoint(
        year: int | None = ...,
        month: int | None = ...
) -> CmfEndpoint[IpcRecord] | CmfEndpoint[ListIpcRecord]: ...


@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: int | None = ...,
        mode: RangeMode = ...
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        end_year: int,
        mode: RangeMode = ...
) -> CmfEndpoint[ListIpcRecord]: ...
@overload
def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: int,
        end_year: int,
        end_month: int,
        mode: RangeMode = ...
) -> CmfEndpoint[ListIpcRecord]: ...
