from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cl_forge.core.impl.cmf import BaseCmfClient
from cl_forge.core.types import FormatEnum, RangeMode, ResponseFormat
from cl_forge.rest.cmf.endpoints import ipc, uf

if TYPE_CHECKING:
    from cl_forge.rest.cmf.schemas import (
        IpcRecord,
        ListIpcRecord,
        ListUfRecord,
        UfRecord,
    )


class CmfClient(BaseCmfClient):
    def ipc(
            self,
            *,
            year: int | None = None,
            month: int | None = None,
            raw: ResponseFormat | None = None
    ) -> IpcRecord | ListIpcRecord | dict[str, Any] | str:
        endpoint = ipc.ipc_endpoint(year=year, month=month)

        if raw and raw in FormatEnum:
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

        if raw and raw in FormatEnum:
            # Raises UnsupportedFormat on wrong format
            return self.get(path=endpoint.path, fmt=raw)

        response = self.get(path=endpoint.path)
        return endpoint.model.model_validate(response)

    def uf(
            self,
            *,
            year: int | None = None,
            month: int | None = None,
            day: int | None = None,
            raw: ResponseFormat | None = None
    ) -> UfRecord | ListUfRecord | dict[str, Any] | str:
        endpoint = uf.uf_endpoint(year=year, month=month, day=day)

        if raw and raw in FormatEnum:
            # Raises UnsupportedFormat on wrong format
            return self.get(path=endpoint.path, fmt=raw)

        response = self.get(path=endpoint.path)
        return endpoint.model.model_validate(response)
