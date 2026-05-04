from typing import Literal, overload

from ..models.directory import BuyersResult, SupplierRecord, SuppliersDirectory, SuppliersResult
from ..query.directory import BuyerQuery, SupplierQuery
from ..types import RutLike
from .base import BaseDirectoryResource

class SuppliersResource(BaseDirectoryResource[SuppliersResult, SupplierQuery]):
    @overload
    def search(
            self,
            rut: RutLike,
            *,
            ignore_meta: Literal[False] = ...,
            only_record: Literal[False] = ...,
    ) -> SuppliersResult: ...
    @overload
    def search(
            self,
            rut: RutLike,
            *,
            ignore_meta: Literal[True],
            only_record: Literal[False] = ...,
    ) -> SuppliersDirectory: ...
    @overload
    def search(
            self,
            rut: RutLike,
            *,
            ignore_meta: bool = ...,
            only_record: Literal[True],
    ) -> SupplierRecord: ...


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersResult: ...
