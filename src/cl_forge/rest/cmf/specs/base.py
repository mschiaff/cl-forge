from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, RootModel

from ..models.base import (
    IndicatorCollection,
    IndicatorRecord,
    RateCollection,
    RateRecord,
)


@dataclass(frozen=True, slots=True)
class BaseSpec[
    RecordT: BaseModel,
    CollectionT: RootModel[list[BaseModel]]
]:
    public_name: str
    path_name: str
    root_key: str
    record_model: type[RecordT]
    collection_model: type[CollectionT]


@dataclass(frozen=True, slots=True)
class IndicatorSpec[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseSpec[RecordT, CollectionT]): ...


@dataclass(frozen=True, slots=True)
class RateSpec[
    RecordT: RateRecord,
    CollectionT: RateCollection[Any]
](BaseSpec[RecordT, CollectionT]): ...
