from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class CmfEndpoint[T: BaseModel]:
    path: str
    model: type[T]
    root_key: str | None = Field(default=None)
