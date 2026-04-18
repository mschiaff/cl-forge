from __future__ import annotations

import enum
from typing import Literal

type ResponseFormat = Literal["json", "xml"]

class FormatEnum(enum.StrEnum):
    JSON = enum.auto()
    XML = enum.auto()
