from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.rest.cmf import helpers
from cl_forge.rest.cmf.endpoints.base import CmfEndpoint
from cl_forge.rest.cmf.schemas import ListUfRecord, UfRecord
from cl_forge.rest.cmf.types import ModeType

if TYPE_CHECKING:
    from cl_forge.core.types import RangeMode


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
    if year and month:
        return CmfEndpoint(path=path, model=ListUfRecord)
    return CmfEndpoint(path=path, model=UfRecord)
