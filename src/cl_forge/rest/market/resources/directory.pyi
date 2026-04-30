from typing import Literal, overload

from ..models.directory import BuyersResult, SupplierRecord, SuppliersDirectory, SuppliersResult
from ..query.directory import BuyerQuery, SupplierQuery
from .base import BaseDirectoryResource

class SuppliersResource(BaseDirectoryResource[SuppliersResult, SupplierQuery]):
    @overload
    def search(
            self,
            rut: str,
            *,
            ignore_root: Literal[False] = ...,
            only_record: Literal[False] = ...,
    ) -> SuppliersResult: ...
    @overload
    def search(
            self,
            rut: str,
            *,
            ignore_root: Literal[True],
            only_record: Literal[False] = ...,
    ) -> SuppliersDirectory: ...
    @overload
    def search(
            self,
            rut: str,
            *,
            ignore_root: bool = ...,
            only_record: Literal[True],
    ) -> SupplierRecord: ...


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersResult: ...
