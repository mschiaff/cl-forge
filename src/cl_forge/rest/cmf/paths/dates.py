from __future__ import annotations

from typing import Self, override

from pydantic.dataclasses import dataclass

from cl_forge.rest.cmf.paths.segments import PathSegment
from cl_forge.rest.cmf.types import (  # noqa: TC001
    DayInt,
    MonthInt,
    ThreeTupleDate,
    TwoTupleDate,
    YearInt,
)


@dataclass(frozen=True, slots=True)
class YearMonth:
    year: YearInt
    month: MonthInt | None = None

    @classmethod
    def from_value(
            cls,
            value: YearInt | TwoTupleDate
    ) -> YearMonth:
        if isinstance(value, int):
            return cls(year=value)

        return cls(*value)

    @property
    def parts(self) -> list[str]:
        parts = [str(self.year)]

        if self.month is not None:
            parts.append(f"{self.month:02d}")

        return parts


@dataclass(frozen=True, slots=True)
class YearMonthDay:
    year: YearInt
    month: MonthInt
    day: DayInt

    @classmethod
    def from_value(
            cls,
            value: ThreeTupleDate
    ) -> Self:
        return cls(*value)

    @property
    def parts(self) -> list[str]:
        return [
            str(self.year),
            f"{self.month:02d}",
            PathSegment.DAYS,
            f"{self.day:02d}"
        ]


@dataclass(frozen=True, slots=True)
class StartDay(YearMonthDay):
    @property
    @override
    def parts(self) -> list[str]:
        return [
            str(self.year),
            f"{self.month:02d}",
            PathSegment.START,
            f"{self.day:02d}"
        ]


@dataclass(frozen=True, slots=True)
class EndDay(YearMonthDay):
    @property
    @override
    def parts(self) -> list[str]:
        return [
            str(self.year),
            f"{self.month:02d}",
            PathSegment.END,
            f"{self.day:02d}"
        ]
