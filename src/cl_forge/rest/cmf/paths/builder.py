from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic.dataclasses import dataclass

from .segments import PathSegment

if TYPE_CHECKING:
    from .dates import YearMonth, YearMonthDay


@dataclass(frozen=True, slots=True)
class IndicatorPath:
    indicator: str
    parts: tuple[str, ...] = Field(default_factory=tuple)

    def build(self) -> str:
        parts = [self.indicator, *self.parts]
        return "/" + "/".join(part for part in parts)

    @classmethod
    def current(cls, indicator: str) -> IndicatorPath:
        return cls(indicator=indicator)

    @classmethod
    def after_monthly(cls, indicator: str, date: YearMonth) -> IndicatorPath:
        return cls(
            indicator=indicator,
            parts=(PathSegment.AFTER, *date.path_parts())
        )
    
    @classmethod
    def after_day(cls, indicator: str, date: YearMonthDay) -> IndicatorPath:
        return cls(
            indicator=indicator,
            parts=(PathSegment.AFTER, *date.path_parts())
        )
