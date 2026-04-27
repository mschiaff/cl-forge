from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, Field, RootModel, field_validator


def convert_decimal(value: str) -> float:
    return float(value.replace('.', '').replace(',', '.'))


class IndicatorRecord(BaseModel):
    value: float = Field(validation_alias="Valor")
    date: datetime = Field(validation_alias="Fecha")

    @field_validator('value', mode='before')
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return convert_decimal(value)


class IndicatorCollection[T: IndicatorRecord](RootModel[list[T]]): ...


class RateRecord(BaseModel):
    title: str | None = Field(validation_alias="Titulo")
    subtitle: str = Field(validation_alias="SubTitulo")
    value: float = Field(validation_alias="Valor")
    date: datetime = Field(validation_alias="Fecha")
    date_to: datetime | None = Field(default=None, validation_alias="Hasta")
    type: int = Field(validation_alias="Tipo")

    @field_validator('value', mode='before')
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return round(convert_decimal(value) / 100, 5)


class RateCollection[T: RateRecord](RootModel[list[T]]): ...
