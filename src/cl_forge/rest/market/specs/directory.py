from __future__ import annotations

from dataclasses import dataclass

from ..models.directory import BuyersResult, DirectoryResult, SuppliersResult


@dataclass(frozen=True, slots=True)
class DirectorySpec[
    ResultT: DirectoryResult,
]:
    path_name: str
    model: type[ResultT]


SUPPLIER_SPEC = DirectorySpec[
    SuppliersResult
](
    path_name="/Empresas/BuscarProveedor",
    model=SuppliersResult,
)

BUYER_SPEC = DirectorySpec[
    BuyersResult
](
    path_name="/Empresas/BuscarComprador",
    model=BuyersResult,
)
