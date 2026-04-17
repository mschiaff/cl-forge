from __future__ import annotations

from datetime import datetime
from typing import override

from pydantic import BaseModel, Field, field_validator


class CmfRecord(BaseModel):
    value: float = Field(validation_alias="Valor")
    date: datetime = Field(validation_alias="Fecha")

    @field_validator('value', mode='before')
    @classmethod
    def convert_value(cls, v):
        return float(v.replace('.', '').replace(',', '.'))


class IpcRecord(CmfRecord):
    @override
    @field_validator('value', mode='before')
    @classmethod
    def convert_value(cls, v):
        return round(float(v.replace('.', '').replace(',', '.')) / 100, 5)