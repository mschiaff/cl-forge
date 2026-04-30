from __future__ import annotations

from ..models.directory import BuyersResult, SuppliersResult
from ..query.directory import BuyerQuery, SupplierQuery
from .base import BaseDirectoryResource


class SuppliersResource(BaseDirectoryResource[SuppliersResult, SupplierQuery]):
    def search(self, rut: str) -> SuppliersResult:
        query = SupplierQuery(rut=rut)
        return self._search(query)


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersResult:
        return self._search()
