from datetime import datetime

from pydantic import BaseModel, Field, RootModel, field_validator


def convert_decimal(value: str) -> float:
    return float(value.replace(".", "").replace(",", "."))


class IndexRecord(BaseModel):
    value: float = Field(
        validation_alias="Valor",
        description="The value of the index.",
    )
    """The value of the index."""
    date: datetime = Field(
        validation_alias="Fecha",
        description="The date of the index.",
    )
    """The date of the index."""

    @field_validator("value", mode="before")
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return convert_decimal(value)


class IndexList[T: IndexRecord](RootModel[list[T]]): ...


class RateRecord(BaseModel):
    title: str | None = Field(
        validation_alias="Titulo",
        description="Descriptive title of the rate.",
    )
    """Descriptive title of the rate."""
    subtitle: str = Field(
        validation_alias="SubTitulo",
        description="More descriptive details about the rate.",
    )
    """More descriptive details about the rate."""
    value: float = Field(
        validation_alias="Valor",
        description="The value of the rate.",
    )
    """The value of the rate."""
    date: datetime = Field(
        validation_alias="Fecha",
        description="The date of the rate.",
    )
    """The date of the rate."""
    date_to: datetime | None = Field(
        default=None,
        validation_alias="Hasta",
        description="Date until which the rate is valid (if applicable).",
    )
    """Date until which the rate is valid (if applicable)."""
    type: int = Field(
        validation_alias="Tipo",
        description="Code of the rate type that matches title and subtitle descriptions.",
    )
    """Code of the rate type that matches title and subtitle descriptions."""

    @field_validator("value", mode="before")
    @classmethod
    def _parse_value(cls, value: str) -> float:
        return round(convert_decimal(value) / 100, 5)


class RateList[T: RateRecord](RootModel[list[T]]): ...
