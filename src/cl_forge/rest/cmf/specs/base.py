from __future__ import annotations

from typing import Any

from pydantic.dataclasses import dataclass

from ..models.base import IndicatorCollection, IndicatorRecord


@dataclass(frozen=True, slots=True)
class IndicatorSpec[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
]:
    public_name: str
    path_name: str
    root_key: str
    record_model: type[RecordT]
    collection_model: type[CollectionT]
    daily: bool = False
