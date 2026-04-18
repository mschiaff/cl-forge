from typing import overload

from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord

@overload
def ipc_endpoint(year: None = ... ) -> CmfEndpoint[IpcRecord]: ...
@overload
def ipc_endpoint(year: int) -> CmfEndpoint[ListIpcRecord]: ...

def ipc_endpoint(
        year: int | None = None
) -> CmfEndpoint[IpcRecord] | CmfEndpoint[ListIpcRecord]: ...
