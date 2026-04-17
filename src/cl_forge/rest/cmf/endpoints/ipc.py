from __future__ import annotations

from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord


def ipc_last_endpoint() -> CmfEndpoint[IpcRecord]:
    return CmfEndpoint(path="/ipc", model=IpcRecord, root_key="IPCs")