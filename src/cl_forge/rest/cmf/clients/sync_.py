from __future__ import annotations

from typing import Any

from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.endpoints import ipc
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import FormatType, RangeMode, ResponseFormat


class CmfClient(BaseCmfClient):
    def ipc(
            self,
            *,
            year: int | None = None,
            month: int | None = None,
            raw: ResponseFormat | None = None
    ) -> IpcRecord | ListIpcRecord | dict[str, Any] | str:
        endpoint = ipc.ipc_endpoint(year=year, month=month)

        if raw and raw in FormatType:
            # Raises UnsupportedFormat on wrong format
            return self.get(path=endpoint.path, fmt=raw)

        response = self.get(path=endpoint.path)
        return endpoint.model.model_validate(response)

    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = None,
            end_year: int | None = None,
            end_month: int | None = None,
            mode: RangeMode = "after",
            raw: ResponseFormat | None = None
    ) -> ListIpcRecord | dict[str, Any] | str:
        endpoint = ipc.ipc_range_endpoint(
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
            mode=mode
        )

        if raw and raw in FormatType:
            # Raises UnsupportedFormat on wrong format
            return self.get(path=endpoint.path, fmt=raw)

        response = self.get(path=endpoint.path)
        return endpoint.model.model_validate(response)
