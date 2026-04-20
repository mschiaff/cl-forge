from __future__ import annotations

from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import (
    ModeType,
    RangeMode,
)


def ipc_endpoint(
        year: int | None = None,
        month: int | None = None
) -> CmfEndpoint[IpcRecord] | CmfEndpoint[ListIpcRecord]:
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
    if isinstance(mode, str):
        # ModeType will raise ValueError on invalid type
        # or value, so we don't need to check for that here.
        _mode = ModeType(mode)

    if start_month and not (1 <= start_month <= 12):
        raise ValueError("Start month must be between 1 and 12.")
    if end_month and not (1 <= end_month <= 12):
        raise ValueError("End month must be between 1 and 12.")

    if _mode in (ModeType.AFTER, ModeType.BEFORE):
        if not start_month:
            path = f"{_mode.path}/{start_year}"
            return CmfEndpoint(path=path, model=ListIpcRecord)
        path = f"{_mode.path}/{start_year}/{start_month}"
        return CmfEndpoint(path=path, model=ListIpcRecord)

    if _mode is ModeType.BETWEEN:
        if not end_year:
            raise ValueError(
                "End year must be specified for 'between' mode."
            )
        if start_year > end_year:
            raise ValueError(
                "Start year cannot be greater than "
                "end year for 'between' mode."
            )
        if start_month and not end_month:
            raise ValueError(
                "End month must be specified if start "
                "month is specified for 'between' mode."
            )
        if not start_month and end_month:
            raise ValueError(
                "Start month must be specified if end "
                "month is specified for 'between' mode."
            )
        if start_month and end_month:
            if (start_year, start_month) > (end_year, end_month):
                raise ValueError(
                    "Start date cannot be greater than "
                    "end date for 'between' mode."
                )
            if (start_year, start_month) == (end_year, end_month):
                raise ValueError(
                    "For individual month query, use the 'ipc' method."
                )

            path = f"{_mode.path}/{start_year}/{start_month}/{end_year}/{end_month}"
            return CmfEndpoint(path=path, model=ListIpcRecord)

        path = f"{_mode.path}/{start_year}/{end_year}"
        return CmfEndpoint(path=path, model=ListIpcRecord)

    raise NotImplementedError(f"Unsupported range mode: {mode!r}")
