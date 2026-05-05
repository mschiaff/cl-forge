from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..models.directory import (
    BuyerRecord,
    BuyersDirectory,
    BuyersResult,
    SupplierRecord,
    SuppliersDirectory,
    SuppliersResult,
)
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
            ignore_meta: bool = False,
            only_record: bool = False,
    ) -> SupplierRecord | SuppliersDirectory | SuppliersResult:
        """
        Search for suppliers based on the provided RUT.

        Parameters
        ----------
        rut : RutLike
            The RUT of the supplier to search for. Exptects a string in format
            "12345678-9", "12.345.678-9" or an integer like 12345678 only with
            RUT's digits.
        ignore_meta : bool, optional
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
        ValidationError
            If the provided RUT is not valid.
        
        Notes
        -----
        - When the RUT is given as a string, the verifier is validated
        before making the request using :func:`cl_forge.validate_rut`.
        - When the RUT's digits are given as an integer, the verifier is
        calculated using :func:`cl_forge.calculate_verifier`.

        Examples
        --------
        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        supplier = client.suppliers.search("12345678-9", only_record=True)
        print(supplier.code) # prints the supplier code
        ```
        """
        rut = RutLikeAdapter.validate_python(rut)
        query = SupplierQuery(rut=rut)
        response =  self._search(query)

        if only_record:
                return response.records.root[0]
        if ignore_meta:
             return response.records

        return response


class BuyersSearchResult(BuyersResult):
    def _in(self, pattern: str) -> list[BuyerRecord]:
         return [record for record in self.records.root if pattern in record.name]

    def _match(self, pattern: str, flags: int | re.RegexFlag = 0) -> list[BuyerRecord]:
        regex = re.compile(pattern, flags)
        return [record for record in self.records.root if regex.search(record.name)]

    def contains(
              self,
              pattern: str,
              *,
              regex: bool = False,
              flags: int | re.RegexFlag = 0
    ) -> BuyersDirectory:
        """
        Filter the buyers in the directory based on whether their name contains
        a given pattern.

        Parameters
        ----------
        pattern : str
            The pattern to search for in the buyer names.
        regex : bool, optional
            Whether to treat the pattern as a regular expression, by default False
        flags : int | re.RegexFlag, optional
            Flags to pass to the regular expression, by default 0

        Returns
        -------
        BuyersDirectory
            A directory of buyers that match the given pattern.
        """
        if regex:
            return BuyersDirectory(root=self._match(pattern, flags))
        return BuyersDirectory(root=self._in(pattern))

    def by_code(self, code: int) -> BuyerRecord:
        """
        Get a buyer record by its code.

        Parameters
        ----------
        code : int
            The code of the buyer to retrieve.

        Returns
        -------
        BuyerRecord
            The buyer record with the specified code.

        Raises
        ------
        ValueError
            If no buyer with the specified code is found in the directory.
        """
        for record in self.records.root:
            if record.code == code:
                return record
        raise ValueError(f"No buyer found with code {code}")


class BuyersResource(BaseDirectoryResource[BuyersResult, BuyerQuery]):
    def search(self) -> BuyersSearchResult:
        """
        Search for all buyers in the directory.

        Returns
        -------
        BuyersSearchResult
            The result of the search, which contains all buyers in the directory.

        Notes
        -----
        - This method retrieves all buyers from the directory and returns them
        wrapped in a :class:`BuyersSearchResult` object, which provides additional
        methods for filtering the results based on the buyer's name.
        """
        return BuyersSearchResult.model_validate(self._search().model_dump(by_alias=True))
