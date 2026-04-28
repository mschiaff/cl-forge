from __future__ import annotations

from typing import Any

from cl_forge.rest.cmf.types import MonthInt, TwoTupleDate, YearInt  # noqa: TC001

from ..models.base import RateCollection, RateRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import YearMonth
from .base import BaseRateResource


class RateResource[
    RecordT: RateRecord,
    CollectionT: RateCollection[Any]
](BaseRateResource[RecordT, CollectionT]):
    def current(self) -> CollectionT:
        """
        Get the latest available collection of this rate records.

        Returns
        -------
        CollectionT
            The latest available collection of this rate records.

        Examples
        --------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.tip.current()
        ```
        """
        path = IndicatorPath.current(self._spec.path_name).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def year(self, year: YearInt) -> CollectionT:
        """
        Get the collection of this rate records for a specific year.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve the rate records.

        Returns
        -------
        CollectionT
            The collection of this rate records for the specified year.

        Examples
        --------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.tip.year(2023)
        ```
        """
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def month(self, year: YearInt, month: MonthInt) -> CollectionT:
        """
        Get the collection of this rate records for a specific month.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve the rate records.
        month : MonthInt
            The month for which to retrieve the rate records.

        Returns
        -------
        CollectionT
            The collection of this rate records for the specified month.

        Examples
        --------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.tip.month(2023, 5)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of this rate records after a specific year and month.

        Parameters
        ----------
        year : YearInt
            The year after which to retrieve the rate records.
        month : MonthInt | None, optional
            The month after which to retrieve the rate records, by default None

        Returns
        -------
        CollectionT
            The collection of this rate records after the specified year and month.

        Examples
        --------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.tip.after(2023, 5)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.after_year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of this rate records before a specific year and month.

        Parameters
        ----------
        year : YearInt
            The year before which to retrieve the rate records.
        month : MonthInt | None, optional
            The month before which to retrieve the rate records, by default None

        Returns
        -------
        CollectionT
            The collection of this rate records before the specified year and month.

        Examples
        --------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.tip.before(2023, 5)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.before_year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def between(
            self,
            start: YearInt | TwoTupleDate,
            end: YearInt | TwoTupleDate
    ) -> CollectionT:
        """
        Get the collection of this rate records between a specific start and end dates.

        Parameters
        ----------
        start : YearInt | TwoTupleDate
            The start date for which to retrieve the rate records.
        end : YearInt | TwoTupleDate
            The end date for which to retrieve the rate records.

        Returns
        -------
        CollectionT
            The collection of this rate records between the specified start and end dates.

        Examples
        --------
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.tip.between((2023, 1), (2023, 5))
        ```
        """
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return self._get(path, shape=ResponseShape.COLLECTION)


class AsyncRateResource[
    RecordT: RateRecord,
    CollectionT: RateCollection[Any]
](BaseRateResource[RecordT, CollectionT]):
    async def current(self) -> CollectionT:
        """
        Get the latest available collection of this rate records.

        Returns
        -------
        CollectionT
            The latest available collection of this rate records.

        Examples
        --------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.tip.current()
        ```
        """
        path = IndicatorPath.current(self._spec.path_name).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def year(self, year: YearInt) -> CollectionT:
        """
        Get the collection of this rate records for a specific year.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve the rate records.

        Returns
        -------
        CollectionT
            The collection of this rate records for the specified year.

        Examples
        --------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.tip.year(2023)
        ```
        """
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def month(self, year: YearInt, month: MonthInt) -> CollectionT:
        """
        Get the collection of this rate records for a specific month.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve the rate records.
        month : MonthInt
            The month for which to retrieve the rate records.

        Returns
        -------
        CollectionT
            The collection of this rate records for the specified month.

        Examples
        --------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.tip.month(2023, 5)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of this rate records after a specific year and month.

        Parameters
        ----------
        year : YearInt
            The year after which to retrieve the rate records.
        month : MonthInt | None, optional
            The month after which to retrieve the rate records, by default None

        Returns
        -------
        CollectionT
            The collection of this rate records after the specified year and month.

        Examples
        --------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.tip.after(2023, 5)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.after_year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of this rate records before a specific year and month.

        Parameters
        ----------
        year : YearInt
            The year before which to retrieve the rate records.
        month : MonthInt | None, optional
            The month before which to retrieve the rate records, by default None

        Returns
        -------
        CollectionT
            The collection of this rate records before the specified year and month.

        Examples
        --------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.tip.before(2023, 5)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.before_year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def between(
            self,
            start: YearInt | TwoTupleDate,
            end: YearInt | TwoTupleDate
    ) -> CollectionT:
        """
        Get the collection of this rate records between a specific start and end dates.

        Parameters
        ----------
        start : YearInt | TwoTupleDate
            The start date for which to retrieve the rate records.
        end : YearInt | TwoTupleDate
            The end date for which to retrieve the rate records.

        Returns
        -------
        CollectionT
            The collection of this rate records between the specified start and end dates.

        Examples
        --------
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.tip.between((2023, 1), (2023, 5))
        ```
        """
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)
