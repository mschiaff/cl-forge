from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DirectoryQuery(BaseModel):
    @property
    def params(self) -> dict[str, Any]:
        """
        Returns the query parameters as a dict with keys matching the API's
        expected parameter names.

        Notes
        -----
        - Only includes fields that are not `None`.
        - Uses Pydantic's :class:`Field` `serialization_alias` for field
          names to match the API's expected parameter names.
        """
        return self.model_dump(by_alias=True, exclude_none=True)

class BuyerQuery(DirectoryQuery): ...

class SupplierQuery(DirectoryQuery):
    rut: str = Field(
        serialization_alias="RutEmpresaProveedor",
        description="The RUT of the supplier to query.",
    )
