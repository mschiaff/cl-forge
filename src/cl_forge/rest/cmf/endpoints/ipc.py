from __future__ import annotations

from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord


def ipc_endpoint(
        year: int | None = None
) -> CmfEndpoint[IpcRecord] | CmfEndpoint[ListIpcRecord]:
    path = f"/ipc/{year}" if year else "/ipc"
    if year:
        return CmfEndpoint(path=path, model=ListIpcRecord)
    return CmfEndpoint(path=path, model=IpcRecord)
