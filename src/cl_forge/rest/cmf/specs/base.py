from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, RootModel

#from ..models.base import IndicatorCollection, IndicatorRecord


@dataclass(frozen=True, slots=True)
class IndicatorSpec[
    RecordT: BaseModel,
    CollectionT: RootModel[list[BaseModel]]
]:
    public_name: str
    path_name: str
    root_key: str
    record_model: type[RecordT]
    collection_model: type[CollectionT]
