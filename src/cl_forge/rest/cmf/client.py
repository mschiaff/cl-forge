from __future__ import annotations

from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.endpoints import ipc
from cl_forge.rest.cmf.schemas import IpcRecord


class CmfClient(BaseCmfClient):
    def ipc_last(self) -> IpcRecord:
        endpoint = ipc.ipc_last_endpoint()
        response = self.get(path=endpoint.path)
        return endpoint.model.model_validate(response.get(endpoint.root_key)[-1])