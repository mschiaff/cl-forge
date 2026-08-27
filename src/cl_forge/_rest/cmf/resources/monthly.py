from __future__ import annotations

from typing import Any

from cl_forge.rest.cmf.types import MonthInt, TwoTupleDate, YearInt  # noqa: TC001

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import YearMonth
from .base import BaseIndicatorResource


class MonthlyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseIndicatorResource[RecordT, CollectionT]):
    def current(self) -> RecordT:
        """
        Get the latest available record for the indicator.

        Returns
        -------
        RecordT
            The latest available record for the indicator.

        Examples
        --------
        Get the latest IPC record:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.ipc.current()
        ```
        """
        path = IndicatorPath.current(self._spec.path_name).build()
        return self._get(path, shape=ResponseShape.SINGLE)

    def year(self, year: YearInt) -> CollectionT:
        """
        Get the collection of records for the specified year.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve records.

        Returns
        -------
        CollectionT
            The collection of records for the specified year.

        Examples
        --------
        Get the IPC records for the year 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.ipc.year(2023)
        ```
        """
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def month(self, year: YearInt, month: MonthInt) -> RecordT:
        """
        Get the record for the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve the record.
        month : MonthInt
            The month for which to retrieve the record.

        Returns
        -------
        RecordT
            The record for the specified year and month.

        Examples
        --------
        Get the IPC record for March 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.ipc.month(2023, 3)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.SINGLE)

    def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of records after the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year after which to retrieve records.
        month : MonthInt | None, optional
            The month after which to retrieve records, by default None

        Returns
        -------
        CollectionT
            The collection of records after the specified year and month.

        Examples
        --------
        Get the IPC records after March 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.ipc.after(2023, 3)
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
        Get the collection of records before the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year before which to retrieve records.
        month : MonthInt | None, optional
            The month before which to retrieve records, by default None

        Returns
        -------
        CollectionT
            The collection of records before the specified year and month.

        Examples
        --------
        Get the IPC records before March 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.ipc.before(2023, 3)
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
        Get the collection of records between the specified start and end dates.

        Parameters
        ----------
        start : YearInt | TwoTupleDate
            The start date, which can be specified as a year (YearInt)
            or a tuple of (year, month) (TwoTupleDate).
        end : YearInt | TwoTupleDate
            The end date, which can be specified as a year (YearInt)
            or a tuple of (year, month) (TwoTupleDate).

        Returns
        -------
        CollectionT
            The collection of records between the specified start and end dates.

        Examples
        --------
        Get the IPC records between January 2023 and March 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        response = client.ipc.between((2023, 1), (2023, 3))
        ```
        """
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return self._get(path, shape=ResponseShape.COLLECTION)


class AsyncMonthlyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseIndicatorResource[RecordT, CollectionT]):
    async def current(self) -> RecordT:
        """
        Get the latest available record for the indicator.

        Returns
        -------
        RecordT
            The latest available record for the indicator.

        Examples
        --------
        Get the latest IPC record:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.ipc.current()
        ```
        """
        path = IndicatorPath.current(self._spec.path_name).build()
        return await self._aget(path, shape=ResponseShape.SINGLE)

    async def year(self, year: YearInt) -> CollectionT:
        """
        Get the collection of records for the specified year.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve records.

        Returns
        -------
        CollectionT
            The collection of records for the specified year.

        Examples
        --------
        Get the IPC records for the year 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.ipc.year(2023)
        ```
        """
        date = YearMonth(year=year)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def month(self, year: YearInt, month: MonthInt) -> RecordT:
        """
        Get the record for the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year for which to retrieve the record.
        month : MonthInt
            The month for which to retrieve the record.

        Returns
        -------
        RecordT
            The record for the specified year and month.

        Examples
        --------
        Get the IPC record for March 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.ipc.month(2023, 3)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.SINGLE)

    async def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of records after the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year after which to retrieve records.
        month : MonthInt | None, optional
            The month after which to retrieve records, by default None

        Returns
        -------
        CollectionT
            The collection of records after the specified year and month.

        Examples
        --------
        Get the IPC records after March 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.ipc.after(2023, 3)
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
        Get the collection of records before the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year before which to retrieve records.
        month : MonthInt | None, optional
            The month before which to retrieve records, by default None

        Returns
        -------
        CollectionT
            The collection of records before the specified year and month.

        Examples
        --------
        Get the IPC records before March 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.ipc.before(2023, 3)
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
        Get the collection of records between the specified start and end dates.

        Parameters
        ----------
        start : YearInt | TwoTupleDate
            The start date, which can be specified as a year (YearInt)
            or a tuple of (year, month) (TwoTupleDate).
        end : YearInt | TwoTupleDate
            The end date, which can be specified as a year (YearInt)
            or a tuple of (year, month) (TwoTupleDate).

        Returns
        -------
        CollectionT
            The collection of records between the specified start and end dates.

        Examples
        --------
        Get the IPC records between January 2023 and March 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        response = await client.ipc.between((2023, 1), (2023, 3))
        ```
        """
        _start = YearMonth.from_value(start)
        _end = YearMonth.from_value(end)
        path = IndicatorPath.between_year_month(self._spec.path_name, _start, _end).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)
