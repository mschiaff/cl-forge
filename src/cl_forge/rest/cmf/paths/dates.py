from __future__ import annotations

from typing import Annotated

from pydantic import Field
from pydantic.dataclasses import dataclass

from .segments import PathSegment

type YearInt = Annotated[int, Field(ge=0)]
type MonthInt = Annotated[int, Field(ge=1, le=12)]
type DayInt = Annotated[int, Field(ge=1, le=31)]


@dataclass(frozen=True, slots=True)
class YearMonth:
    year: YearInt
    month: MonthInt | None = None

    def path_parts(self) -> list[str]:
        parts = [str(self.year)]

        if self.month is not None:
            parts.append(f"{self.month:02d}")

        return parts


@dataclass(frozen=True, slots=True)
class YearMonthDay:
    year: YearInt
    month: MonthInt
    day: DayInt

    def path_parts(self) -> list[str]:
        return [
            str(self.year),
            f"{self.month:02d}",
            PathSegment.DAYS,
            f"{self.day:02d}"
        ]
