from __future__ import annotations

from datetime import datetime  # noqa: TC003

from pydantic import BaseModel, Field, RootModel

__all__ = (
    "BuyersResult",
    "DirectoryResult",
    "SupplierRecord",
    "SuppliersDirectory", 
    "SuppliersResult",
)


class DirectoryRecord(BaseModel): ...

class SupplierRecord(DirectoryRecord):
    code: int = Field(
        alias="CodigoEmpresa",
        description="Supplier code.",
    )
    name: str = Field(
        alias="NombreEmpresa",
        description="Supplier name."
    )

class BuyerRecord(DirectoryRecord):
    code: int = Field(
        alias="CodigoEmpresa",
        description="Buyer code.",
    )
    name: str = Field(
        alias="NombreEmpresa",
        description="Buyer name."
    )


class DirectoryCollection[RecordsT: DirectoryRecord](RootModel[list[RecordsT]]): ...

class SuppliersDirectory(DirectoryCollection[SupplierRecord]): ...

class BuyersDirectory(DirectoryCollection[BuyerRecord]): ...


class DirectoryResult(BaseModel): ...

class SuppliersResult(DirectoryResult):
    quantity: int = Field(
        alias="Cantidad",
        description="Number of suppliers in the search results.",
    )
    date_at: datetime = Field(
        alias="FechaCreacion",
        description="Date and time of the search.",
    )
    records: SuppliersDirectory = Field(
        alias="listaEmpresas",
        description="List of suppliers in the search results.",
    )

class BuyersResult(DirectoryResult):
    quantity: int = Field(
        alias="Cantidad",
        description="Number of buyers in the search results.",
    )
    date_at: datetime = Field(
        alias="FechaCreacion",
        description="Date and time of the search.",
    )
    records: BuyersDirectory = Field(
        alias="listaEmpresas",
        description="List of buyers in the search results.",
    )
