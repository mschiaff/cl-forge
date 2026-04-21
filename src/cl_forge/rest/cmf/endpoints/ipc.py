from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.rest.cmf import helpers
from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import ModeType

if TYPE_CHECKING:
    from cl_forge.core.types import RangeMode


def ipc_endpoint(
        *,
        year: int | None = None,
        month: int | None = None
) -> CmfEndpoint[IpcRecord] | CmfEndpoint[ListIpcRecord]:
    helpers.validate_month(month) if month else None
    
    path = (
        f"/ipc/{year}/{month}" if year and month
            else f"/ipc/{year}" if year
            else "/ipc"
    )
    
    if year and not month:
        return CmfEndpoint(path=path, model=ListIpcRecord)
    if not year and month:
        raise ValueError("Month cannot be specified without year.")
    return CmfEndpoint(path=path, model=IpcRecord)


def ipc_range_endpoint(
        *,
        start_year: int,
        start_month: int | None = None,
        end_year: int | None = None,
        end_month: int | None = None,
        mode: RangeMode = "after"
) -> CmfEndpoint[ListIpcRecord]:
    helpers.validate_month(start_month, "start") if start_month else None
    helpers.validate_month(end_month, "end") if end_month else None

    if isinstance(mode, str): # type: ignore
        # ModeType will raise ValueError on invalid type
        # or value, so we don't need to check for that here.
        _mode = ModeType(mode)

    if _mode in (ModeType.AFTER, ModeType.BEFORE):
        if not start_month:
            path = f"{_mode.path}/{start_year}"
            return CmfEndpoint(path=path, model=ListIpcRecord)
        path = f"{_mode.path}/{start_year}/{start_month}"
        return CmfEndpoint(path=path, model=ListIpcRecord)

    if _mode is ModeType.BETWEEN:
        if helpers.is_range_between_months(start_year, start_month, end_year, end_month, "ipc"):
            path = f"{_mode.path}/{start_year}/{start_month}/{end_year}/{end_month}"
            return CmfEndpoint(path=path, model=ListIpcRecord)

        path = f"{_mode.path}/{start_year}/{end_year}"
        return CmfEndpoint(path=path, model=ListIpcRecord)
    raise ValueError("Invalid mode specified.")
