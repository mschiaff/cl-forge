from typing import Any, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator

from cl_forge.rest.resources.types import QueryParams

from .types import DateLike, RutLike, normalize_rut, serialize_date


class MarketQuery(BaseModel):
    """Base model for serializing API query parameter names."""

    model_config = ConfigDict(frozen=True)

    @property
    def params(self) -> QueryParams:
        return cast("QueryParams", self.model_dump(by_alias=True, exclude_none=True))

    @staticmethod
    def _serialize_code(value: object) -> str | None:
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            raise TypeError("Codes must be strings or integers")
        serialized = str(value).strip()
        if not serialized:
            raise ValueError("Codes must not be blank")
        return serialized


class TenderQuery(MarketQuery):
    tender_code: str | None = Field(default=None, serialization_alias="Codigo")
    buyer_code: str | None = Field(default=None, serialization_alias="CodigoOrganismo")
    supplier_code: str | None = Field(default=None, serialization_alias="CodigoProveedor")
    status: str | None = Field(default=None, serialization_alias="Estado")
    date: str | None = Field(default=None, serialization_alias="Fecha")

    @field_validator("tender_code", "buyer_code", "supplier_code", mode="before")
    @classmethod
    def _validate_code(cls, value: object) -> str | None:
        return cls._serialize_code(value)

    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls, value: Any) -> str | None:
        return None if value is None else serialize_date(cast("DateLike", value))


class OrderQuery(MarketQuery):
    order_code: str | None = Field(default=None, serialization_alias="Codigo")
    buyer_code: str | None = Field(default=None, serialization_alias="CodigoOrganismo")
    supplier_code: str | None = Field(default=None, serialization_alias="CodigoProveedor")
    status: str | None = Field(default=None, serialization_alias="Estado")
    date: str | None = Field(default=None, serialization_alias="Fecha")

    @field_validator("order_code", "buyer_code", "supplier_code", mode="before")
    @classmethod
    def _validate_code(cls, value: object) -> str | None:
        return cls._serialize_code(value)

    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls, value: Any) -> str | None:
        return None if value is None else serialize_date(cast("DateLike", value))


class SupplierQuery(MarketQuery):
    rut: str = Field(serialization_alias="RutEmpresaProveedor")

    @field_validator("rut", mode="before")
    @classmethod
    def _validate_rut(cls, value: Any) -> str:
        return normalize_rut(cast("RutLike", value))


__all__ = ("MarketQuery", "OrderQuery", "SupplierQuery", "TenderQuery")
