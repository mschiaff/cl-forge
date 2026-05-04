from __future__ import annotations

from pydantic import BaseModel, Field, RootModel


class OrderRecord(BaseModel):
    code: str = Field(alias="Codigo")
    name: str = Field(alias="Nombre")
    status_code: int = Field(alias="CodigoEstado")


class OrderCollection(RootModel[list[OrderRecord]]): ...


class Order(BaseModel):
    quantity: int = Field(alias="Cantidad")
    created_at: str = Field(alias="FechaCreacion")
    version: str = Field(alias="Version")
    records: OrderCollection = Field(alias="Listado")
