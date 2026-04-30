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
        """
        Search for suppliers based on the provided RUT.

        Parameters
        ----------
        rut : str
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
