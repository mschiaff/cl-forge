import re
from typing import Literal, overload

from ..models.directory import (
    BuyerRecord,
    BuyersDirectory,
    BuyersResult,
    SupplierRecord,
    SuppliersDirectory,
    SuppliersResult,
)
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


class BuyersSearchResult(BuyersResult):
    def _in(self, pattern: str) -> list[BuyerRecord]: ...

    def _match(
            self,
            pattern: str,
            flags: int | re.RegexFlag = 0
    ) -> list[BuyerRecord]: ...

    def contains(
            self,
            pattern:str,
            *,
            regex: bool = False,
            flags: int | re.RegexFlag = 0
    ) -> BuyersDirectory: ...

    def by_code(self, code: int) -> BuyerRecord: ...


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersSearchResult: ...
