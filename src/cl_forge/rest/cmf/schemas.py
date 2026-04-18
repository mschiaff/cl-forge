from __future__ import annotations

from datetime import datetime
from typing import Any, override

from pydantic import (
    BaseModel,
    Field,
    RootModel,
    field_validator,
    model_validator,
)


def _convert_decimal(value: str) -> float:
    return float(value.replace('.', '').replace(',', '.'))


class DateValueRecord(BaseModel):
    value: float = Field(validation_alias="Valor")
    date: datetime = Field(validation_alias="Fecha")

    @field_validator('value', mode='before')
    @classmethod
    def _convert_value(cls, v):
        return _convert_decimal(v)


class IpcRecord(DateValueRecord):
    @model_validator(mode='before')
    @classmethod
    def _parse_response(
            cls,
            data: dict[str, Any]
    ) -> dict[str, Any]:
        if result := data.get("IPCs"):
            return result[0]
        return data
    
    @override
    @field_validator('value', mode='before')
    @classmethod
    def _convert_value(cls, v):
        return round(_convert_decimal(v) / 100, 5)


class ListIpcRecord(RootModel[list[IpcRecord]]):
    @model_validator(mode='before')
    @classmethod
    def _parse_response(
            cls,
            data: dict[str, Any]
    ) -> list[dict[str, Any]]:
        if result := data.get("IPCs"):
            return result
        return [data]