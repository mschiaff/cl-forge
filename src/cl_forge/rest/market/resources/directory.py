from __future__ import annotations

from ..models.directory import BuyersResult, SupplierRecord, SuppliersDirectory, SuppliersResult
from ..query.directory import BuyerQuery, SupplierQuery
from .base import BaseDirectoryResource


class SuppliersResource(BaseDirectoryResource[SuppliersResult, SupplierQuery]):
    def search(
            self,
            rut: str,
            *,
            ignore_root: bool = False,
            only_record: bool = False,
    ) -> SupplierRecord | SuppliersDirectory | SuppliersResult:
        query = SupplierQuery(rut=rut)
        response =  self._search(query)

        if only_record:
                return response.records.root[0]
        if ignore_root:
             return response.records

        return response


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersResult:
        return self._search()
