from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.types import EndpointEnum, ModeEnum
from cl_forge.rest.cmf import helpers
from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import ListUfRecord, UfRecord
from cl_forge.rest.cmf.types import BoundedMode

if TYPE_CHECKING:
    from cl_forge.core.types import RangeMode


UF_MODE: BoundedMode = BoundedMode(EndpointEnum.UF)


def uf_endpoint(
        *,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None
) -> CmfEndpoint[UfRecord] | CmfEndpoint[ListUfRecord]:
    helpers.validate_month(month) if month else None
    helpers.validate_day(day) if day else None

    path = (
        f"/uf/{year}/{month}/dias/{day}" if year and month and day
            else f"/uf/{year}/{month}" if year and month
            else f"/uf/{year}" if year
            else "/uf"
    )

    if day and (not year or not month):
        raise ValueError("Day cannot be specified without year and month.")
    if not year and month:
        raise ValueError("Month cannot be specified without year.")
    if year and not month:
        return CmfEndpoint(path=path, model=ListUfRecord)
    if year and month and not day:
        return CmfEndpoint(path=path, model=ListUfRecord)
    return CmfEndpoint(path=path, model=UfRecord)


def uf_range_endpoint(
        *,
        start_year: int,
        start_month: int | None = None,
        end_year: int | None = None,
        end_month: int | None = None,
        day: int | None = None,
        mode: RangeMode = "after"
) -> CmfEndpoint[UfRecord] | CmfEndpoint[ListUfRecord]:
    helpers.validate_month(start_month, "start") if start_month else None
    helpers.validate_month(end_month, "end") if end_month else None
    helpers.validate_day(day) if day else None

    # ModeType will raise ValueError on invalid type
    # or value, so we don't need to check for that here.
    _mode = UF_MODE(mode)

    if _mode.type in (ModeEnum.AFTER, ModeEnum.BEFORE):
        if not start_month:
            path = f"{_mode.path}/{start_year}"
            return CmfEndpoint(path=path, model=ListUfRecord)
        path = f"{_mode.path}/{start_year}/{start_month}"
        return CmfEndpoint(path=path, model=ListUfRecord)

    if _mode.type is ModeEnum.BETWEEN:
        if helpers.is_range_between_months(
                start_year,
                start_month,
                end_year,
                end_month,
                "uf"
        ):
            path = f"{_mode.path}/{start_year}/{start_month}/{end_year}/{end_month}"
            return CmfEndpoint(path=path, model=ListUfRecord)
        if helpers.is_range_between_days(
                start_year,
                start_month,
                day,
                end_year,
                end_month,
                day,
                "uf"
        ):
            path = (
                f"{_mode.path}/{start_year}/{start_month}/dias"
                f"/{day}/{end_year}/{end_month}/dias/{day}"
            )
            return CmfEndpoint(path=path, model=UfRecord)

    raise ValueError("Invalid combination of parameters for uf range endpoint.")
