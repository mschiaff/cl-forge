from __future__ import annotations

from enum import StrEnum


class PathSegment(StrEnum):
    AFTER = "posteriores"
    BEFORE = "anteriores"
    BETWEEN = "periodo"
    DAYS = "dias"
    START = "dias_i"
    END = "dias_f"
