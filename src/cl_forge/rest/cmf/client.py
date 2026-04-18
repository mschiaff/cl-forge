from __future__ import annotations

from typing import Any

from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.endpoints import ipc
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import FormatEnum, ResponseFormat


class CmfClient(BaseCmfClient):
    def ipc(
            self,
            year: int | None = None,
            *,
            raw: ResponseFormat | None = None
    ) -> IpcRecord | ListIpcRecord | dict[str, Any] | str:
        endpoint = ipc.ipc_endpoint(year=year)

        if raw and raw in FormatEnum:
            # Raises UnsupportedFormat on wrong format
            return self.get(path=endpoint.path, fmt=raw)

        response = self.get(path=endpoint.path)
        return endpoint.model.model_validate(response)
