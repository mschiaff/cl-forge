from typing import Literal

from pydantic import TypeAdapter

from .types import Day, Month, Year

_YEAR_ADAPTER = TypeAdapter[int](Year)
_MONTH_ADAPTER = TypeAdapter[int](Month)
_DAY_ADAPTER = TypeAdapter[int](Day)

type DayMarker = Literal["dias", "dias_i", "dias_f"]


def year_segment(year: Year) -> str:
    """Validate and format one CMF year path segment."""
    return str(_YEAR_ADAPTER.validate_python(year))


def month_segment(month: Month) -> str:
    """Validate and zero-pad one CMF month path segment."""
    return f"{_MONTH_ADAPTER.validate_python(month):02d}"


def day_segment(day: Day) -> str:
    """Validate and zero-pad one CMF day path segment."""
    return f"{_DAY_ADAPTER.validate_python(day):02d}"


def year_month_segments(year: Year, month: Month | None = None) -> tuple[str, ...]:
    """Return validated CMF year or year/month path segments."""
    segments = (year_segment(year),)
    if month is None:
        return segments
    return (*segments, month_segment(month))


def year_month_day_segments(
    year: Year,
    month: Month,
    day: Day,
    *,
    marker: DayMarker = "dias",
) -> tuple[str, ...]:
    """Return validated CMF day path segments with the requested marker."""
    return (
        year_segment(year),
        month_segment(month),
        marker,
        day_segment(day),
    )
