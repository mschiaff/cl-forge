from __future__ import annotations

from enum import StrEnum


class PathSegment(StrEnum):
    AFTER = "posteriores"
    BEFORE = "anteriores"
    PERIOD = "periodo"
    DAYS = "dias"
