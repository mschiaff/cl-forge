import re
from datetime import datetime

from pydantic import BaseModel, Field, RootModel


class DirectoryRecord(BaseModel):
    """Common fields for a Mercado Publico organization."""

    code: int = Field(validation_alias="CodigoEmpresa")
    name: str = Field(validation_alias="NombreEmpresa")


class SupplierRecord(DirectoryRecord):
    """One supplier-directory entry."""


class BuyerRecord(DirectoryRecord):
    """One buyer-directory entry."""


class SupplierList(RootModel[list[SupplierRecord]]):
    """A list of supplier-directory entries."""


class BuyerList(RootModel[list[BuyerRecord]]):
    """A list of buyer-directory entries."""


class DirectoryResult(BaseModel):
    """Shared metadata returned by organization-directory queries."""

    quantity: int = Field(validation_alias="Cantidad")
    created_at: datetime = Field(validation_alias="FechaCreacion")


class SupplierResult(DirectoryResult):
    records: SupplierList = Field(validation_alias="listaEmpresas")


class BuyerResult(DirectoryResult):
    records: BuyerList = Field(validation_alias="listaEmpresas")

    def contains(
        self,
        pattern: str,
        *,
        regex: bool = False,
        flags: int | re.RegexFlag = 0,
    ) -> BuyerList:
        """Return buyers whose name contains or matches ``pattern``."""
        if regex:
            compiled = re.compile(pattern, flags)
            records = [record for record in self.records.root if compiled.search(record.name)]
        else:
            records = [record for record in self.records.root if pattern in record.name]
        return BuyerList(records)

    def by_code(self, code: int) -> BuyerRecord:
        """Return the buyer with ``code`` or raise :class:`ValueError`."""
        for record in self.records.root:
            if record.code == code:
                return record
        raise ValueError(f"No buyer found with code {code}")


__all__ = (
    "BuyerList",
    "BuyerRecord",
    "BuyerResult",
    "DirectoryRecord",
    "DirectoryResult",
    "SupplierList",
    "SupplierRecord",
    "SupplierResult",
)
