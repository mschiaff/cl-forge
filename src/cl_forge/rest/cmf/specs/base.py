from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic.dataclasses import dataclass

if TYPE_CHECKING:
    from pydantic import BaseModel, RootModel


@dataclass(frozen=True, slots=True)
class IndicatorSpec[T: BaseModel, C: RootModel[Any]]:
    public_name: str
    path_name: str
    root_key: str
    record_model: type[T]
    collection_model: type[C]
    daily: bool = False
