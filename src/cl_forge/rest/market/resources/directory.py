from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.directory import BuyersResult, SupplierRecord, SuppliersDirectory, SuppliersResult
from ..query.directory import BuyerQuery, SupplierQuery
from ..types import RutLikeAdapter
from .base import BaseDirectoryResource

if TYPE_CHECKING:
     from ..types import RutLike


class SuppliersResource(BaseDirectoryResource[SuppliersResult, SupplierQuery]):
    def search(
            self,
            rut: RutLike,
            *,
            ignore_root: bool = False,
            only_record: bool = False,
    ) -> SupplierRecord | SuppliersDirectory | SuppliersResult:
        """
        Search for suppliers based on the provided RUT.

        Parameters
        ----------
        rut : RutLike
            The RUT of the supplier to search for.
        ignore_root : bool, optional
            Whether to ignore the response metadata object, by default False
        only_record : bool, optional
            Whether to return only the record, by default False

        Returns
        -------
        SupplierRecord | SuppliersDirectory | SuppliersResult
            The result of the search, which can be a single supplier record,
            a directory of suppliers, or the full search result.

        Raises
        ------
        BadStatus
            If the the searched supplier is not found or any other error
            occurs during the search.
        """
        rut = RutLikeAdapter.validate_python(rut)
        query = SupplierQuery(rut=rut)
        response =  self._search(query)

        if only_record:
                return response.records.root[0]
        if ignore_root:
             return response.records

        return response


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersResult:
        """
        Search for all buyers in the directory.

        Returns
        -------
        BuyersResult
            The result of the search, which contains all buyers in the directory.
        """
        return self._search()
