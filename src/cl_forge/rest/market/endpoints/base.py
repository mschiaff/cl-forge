from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class MarketEndpoint[T: BaseModel]:
    path: str
    model: type[T]
    params: dict[str, Any] | None = None
