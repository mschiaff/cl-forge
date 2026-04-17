from __future__ import annotations

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class CmfEndpoint[T: BaseModel]:
    path: str
    model: type[T]
