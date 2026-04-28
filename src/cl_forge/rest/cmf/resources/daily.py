from __future__ import annotations

from typing import Any, override

from cl_forge.rest.cmf.types import (  # noqa: TC001
    DayInt,
    MonthInt,
    ThreeTupleDate,
    TwoTupleDate,
    YearInt,
)

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.shape import ResponseShape
from ..paths.builder import IndicatorPath
from ..paths.dates import EndDay, StartDay, YearMonth, YearMonthDay
from .monthly import AsyncMonthlyIndicatorResource, MonthlyIndicatorResource


def is_three_tuple(value: YearInt | TwoTupleDate | ThreeTupleDate) -> bool:
    return isinstance(value, tuple) and len(value) == 3


class DailyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](MonthlyIndicatorResource[RecordT, CollectionT]):
    @override
    def month(self, year: YearInt, month: MonthInt) -> CollectionT: # type: ignore
        """
        Get the collection of records for the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year of the records.
        month : MonthInt
            The month of the records.

        Returns
        -------
        CollectionT
            The collection of records for the specified year and month.

        Examples
        --------
        Get UF records for January 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        records = client.uf.month(year=2023, month=1)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    def day(self, year: YearInt, month: MonthInt, day: DayInt) -> RecordT:
        """
        Get the record for the specified year, month, and day.

        Parameters
        ----------
        year : YearInt
            The year of the record.
        month : MonthInt
            The month of the record.
        day : DayInt
            The day of the record.

        Returns
        -------
        RecordT
            The record for the specified year, month, and day.

        Examples
        --------
        Get the UF record for January 15, 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        record = client.uf.day(year=2023, month=1, day=15)
        ```
        """
        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.day(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.SINGLE)

    @override
    def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of records after the specified date.

        Parameters
        ----------
        year : YearInt
            The year of the date.
        month : MonthInt | None, optional
            The month of the date, by default None
        day : DayInt | None, optional
            The day of the date, by default None

        Returns
        -------
        CollectionT
            The collection of records after the specified date.

        Raises
        ------
        ValueError
            If the month is not provided when the day is specified.

        Examples
        --------
        Get UF records after January 15, 2023:

        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        records = client.uf.after(year=2023, month=1, day=15)
        ```
        """
        if day is None:
            return super().after(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.after_day(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    @override
    def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of records before the specified date.

        Parameters
        ----------
        year : YearInt
            The year of the date.
        month : MonthInt | None, optional
            The month of the date, by default None
        day : DayInt | None, optional
            The day of the date, by default None

        Returns
        -------
        CollectionT
            The collection of records before the specified date.

        Raises
        ------
        ValueError
            If the month is not provided when the day is specified.

        Examples
        --------
        Get UF records before January 15, 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        records = client.uf.before(year=2023, month=1, day=15)
        ```
        """
        if day is None:
            return super().before(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.before_day(self._spec.path_name, date).build()
        return self._get(path, shape=ResponseShape.COLLECTION)

    @override
    def between(
            self,
            start: YearInt | TwoTupleDate | ThreeTupleDate,
            end: YearInt | TwoTupleDate | ThreeTupleDate
    ) -> CollectionT:
        """
        Get the collection of records between the specified start and end dates.

        Parameters
        ----------
        start : YearInt | TwoTupleDate | ThreeTupleDate
            The start date, which can be specified as a year (YearInt), a tuple of
            (year, month) (TwoTupleDate), or a tuple of (year, month, day) (ThreeTupleDate).
        end : YearInt | TwoTupleDate | ThreeTupleDate
            The end date, which can be specified as a year (YearInt), a tuple of
            (year, month) (TwoTupleDate), or a tuple of (year, month, day) (ThreeTupleDate).

        Returns
        -------
        CollectionT
            The collection of records between the specified start and end dates.

        Examples
        --------
        Get UF records between January 1, 2023 and January 15, 2023:
        ```python
        from cl_forge import CmfClient

        client = CmfClient("your_api_key")
        records = client.uf.between(start=(2023, 1, 1), end=(2023, 1, 15))
        ```
        """
        if is_three_tuple(start) and is_three_tuple(end):
            _start = StartDay.from_value(start) # type: ignore
            _end = EndDay.from_value(end) # type: ignore
            path = IndicatorPath.between_days(self._spec.path_name, _start, _end).build()
            return self._get(path, shape=ResponseShape.COLLECTION)

        return super().between(start, end) # type: ignore


class AsyncDailyIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](AsyncMonthlyIndicatorResource[RecordT, CollectionT]):
    @override
    async def month(self, year: YearInt, month: MonthInt) -> CollectionT: # type: ignore
        """
        Get the collection of records for the specified year and month.

        Parameters
        ----------
        year : YearInt
            The year of the records.
        month : MonthInt
            The month of the records.

        Returns
        -------
        CollectionT
            The collection of records for the specified year and month.

        Examples
        --------
        Get UF records for January 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        records = await client.uf.month(year=2023, month=1)
        ```
        """
        date = YearMonth(year=year, month=month)
        path = IndicatorPath.year_month(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    async def day(self, year: YearInt, month: MonthInt, day: DayInt) -> RecordT:
        """
        Get the record for the specified year, month, and day.

        Parameters
        ----------
        year : YearInt
            The year of the record.
        month : MonthInt
            The month of the record.
        day : DayInt
            The day of the record.

        Returns
        -------
        RecordT
            The record for the specified year, month, and day.

        Examples
        --------
        Get the UF record for January 15, 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        record = await client.uf.day(year=2023, month=1, day=15)
        ```
        """
        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.day(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.SINGLE)

    @override
    async def after(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of records after the specified date.

        Parameters
        ----------
        year : YearInt
            The year of the date.
        month : MonthInt | None, optional
            The month of the date, by default None
        day : DayInt | None, optional
            The day of the date, by default None

        Returns
        -------
        CollectionT
            The collection of records after the specified date.

        Raises
        ------
        ValueError
            If the month is not provided when the day is specified.

        Examples
        --------
        Get UF records after January 15, 2023:

        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        records = await client.uf.after(year=2023, month=1, day=15)
        ```
        """
        if day is None:
            return await super().after(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.after_day(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    @override
    async def before(
            self,
            year: YearInt,
            month: MonthInt | None = None,
            day: DayInt | None = None,
    ) -> CollectionT:
        """
        Get the collection of records before the specified date.

        Parameters
        ----------
        year : YearInt
            The year of the date.
        month : MonthInt | None, optional
            The month of the date, by default None
        day : DayInt | None, optional
            The day of the date, by default None

        Returns
        -------
        CollectionT
            The collection of records before the specified date.

        Raises
        ------
        ValueError
            If the month is not provided when the day is specified.

        Examples
        --------
        Get UF records before January 15, 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        records = await client.uf.before(year=2023, month=1, day=15)
        ```
        """
        if day is None:
            return await super().before(year=year, month=month)

        if month is None:
            raise ValueError("Month is required when day is provided")

        date = YearMonthDay(year=year, month=month, day=day)
        path = IndicatorPath.before_day(self._spec.path_name, date).build()
        return await self._aget(path, shape=ResponseShape.COLLECTION)

    @override
    async def between(
            self,
            start: YearInt | TwoTupleDate | ThreeTupleDate,
            end: YearInt | TwoTupleDate | ThreeTupleDate
    ) -> CollectionT:
        """
        Get the collection of records between the specified start and end dates.

        Parameters
        ----------
        start : YearInt | TwoTupleDate | ThreeTupleDate
            The start date, which can be specified as a year (YearInt), a tuple of
            (year, month) (TwoTupleDate), or a tuple of (year, month, day) (ThreeTupleDate).
        end : YearInt | TwoTupleDate | ThreeTupleDate
            The end date, which can be specified as a year (YearInt), a tuple of
            (year, month) (TwoTupleDate), or a tuple of (year, month, day) (ThreeTupleDate).

        Returns
        -------
        CollectionT
            The collection of records between the specified start and end dates.

        Examples
        --------
        Get UF records between January 1, 2023 and January 15, 2023:
        ```python
        from cl_forge import AsyncCmfClient

        client = AsyncCmfClient("your_api_key")
        records = await client.uf.between(start=(2023, 1, 1), end=(2023, 1, 15))
        ```
        """
        if is_three_tuple(start) and is_three_tuple(end):
            _start = StartDay.from_value(start) # type: ignore
            _end = EndDay.from_value(end) # type: ignore
            path = IndicatorPath.between_days(self._spec.path_name, _start, _end).build()
            return await self._aget(path, shape=ResponseShape.COLLECTION)

        return await super().between(start, end) # type: ignore
