from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic.dataclasses import dataclass

from .segments import PathSegment

if TYPE_CHECKING:
    from .dates import EndDay, StartDay, YearMonth, YearMonthDay


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
    def year_month(cls, indicator: str, date: YearMonth) -> IndicatorPath:
        return cls(indicator=indicator, parts=(*date.parts,))

    @classmethod
    def day(cls, indicator: str, date: YearMonthDay) -> IndicatorPath:
        return cls(indicator=indicator, parts=(*date.parts,))

    @classmethod
    def after_year_month(cls, indicator: str, date: YearMonth) -> IndicatorPath:
        return cls(indicator=indicator, parts=(PathSegment.AFTER, *date.parts))

    @classmethod
    def after_day(cls, indicator: str, date: YearMonthDay) -> IndicatorPath:
        return cls(indicator=indicator, parts=(PathSegment.AFTER, *date.parts))

    @classmethod
    def before_year_month(cls, indicator: str, date: YearMonth) -> IndicatorPath:
        return cls(indicator=indicator, parts=(PathSegment.BEFORE, *date.parts))

    @classmethod
    def before_day(cls, indicator: str, date: YearMonthDay) -> IndicatorPath:
        return cls(indicator=indicator, parts=(PathSegment.BEFORE, *date.parts))

    @classmethod
    def between_year_month(cls, indicator: str, start: YearMonth, end: YearMonth) -> IndicatorPath:
        return cls(indicator=indicator, parts=(PathSegment.BETWEEN, *start.parts, *end.parts))

    @classmethod
    def between_days(cls, indicator: str, start: StartDay, end: EndDay) -> IndicatorPath:
        return cls(indicator=indicator, parts=(PathSegment.BETWEEN, *start.parts, *end.parts))
