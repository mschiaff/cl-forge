from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.tenders import Tender, TenderDetails
from ..query.tenders import TenderQuery
from ..types import TenderStatus
from .base import BaseTendersResource

if TYPE_CHECKING:
    from ..types import DateLike, TenderStatusLike


class TendersResource(BaseTendersResource[Tender, TenderDetails]):
    def today(self) -> Tender:
        """
        Get today's tenders by all statuses.

        Returns
        -------
        Tender
            A collection of all tenders for today, regardless of their status.

        Examples
        --------
        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.today()
        ```
        """
        return self._get_tenders()

    def details(self, tender_code: str) -> TenderDetails:
        """
        Get the details of a specific tender by its code.

        Parameters
        ----------
        tender_code : str
            The code of the tender to retrieve details for.

        Returns
        -------
        TenderDetails
            The details of the specified tender.

        Examples
        --------
        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.details("1003473-14-LR26")
        ```
        """
        query = TenderQuery(tender_code=tender_code)
        return self._get_details(query)

    def by_date(self, date: DateLike) -> Tender:
        """
        Get tenders by a specific date, regardless of their status.

        Parameters
        ----------
        date : DateLike
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified date.

        Examples
        --------
        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.by_date("2024-01-01")
        ```
        """
        query = TenderQuery(date=date)
        return self._get_tenders(query)

    def active(self) -> Tender:
        """
        Get active tenders.

        Returns
        -------
        Tender
            A collection of active tenders.

        Examples
        --------
        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.active()
        ```
        """
        query = TenderQuery(status=TenderStatus.others.ACTIVE, allow_others=True)
        return self._get_tenders(query)

    def all(self, date: DateLike | None = None) -> Tender:
        """
        Get all tenders regardless of their status, optionally filtered by date.

        Parameters
        ----------
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of all tenders, optionally filtered by date.

        Examples
        --------
        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.all(date="2024-01-01")
        ```
        """
        query = TenderQuery(status=TenderStatus.others.ALL, allow_others=True, date=date)
        return self._get_tenders(query)

    def by_buyer(self, buyer_code: str | int, *, date: DateLike | None = None) -> Tender:
        """
        Get tenders by a specific buyer.

        Parameters
        ----------
        buyer_code : str | int
            The code of the buyer (public entity) to filter tenders by.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified buyer, optionally
            filtered by date.

        Examples
        --------
        If you already have the buyer code:

        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.by_buyer(12345, date="2024-01-01")
        ```

        If you don't have the buyer code, you can search for it by name using
        the buyers resource, e.g. `client.buyers.search()`, which will return
        all the available buyer records. Then you can filter those records by name:

        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        buyers = client.buyers.search()
        buyer = buyers.contains("UNIVERSIDAD DE CHILE").root[0]
        response = client.tenders.by_buyer(buyer.code, date="2024-01-01")
        ```
        """
        query = TenderQuery(date=date, buyer_code=buyer_code)
        return self._get_tenders(query)

    def by_status(self, status: TenderStatusLike, *, date: DateLike | None = None) -> Tender:
        """
        Get tenders by a specific status.

        Parameters
        ----------
        status : TenderStatusLike
            The status to filter tenders by. Can be a case-insensitive string
            matching a value of :class:`TenderStatus`, or a value of
            :class:`TenderStatus` itself.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified status, optionally
            filtered by date.

        Examples
        --------
        Using a string for the status parameter:

        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        response = client.tenders.by_status("Adjudicada", date="2026-05-04")
        ```

        Using a :class:`TenderStatus` value for the status parameter:

        ```python
        from cl_forge import MarketClient, TenderStatus

        client = MarketClient("your_api_key")
        response = client.tenders.by_status(TenderStatus.AWARDED, date="2026-05-04")
        ```
        """
        query = TenderQuery(status=status, date=date)
        return self._get_tenders(query)

    def by_supplier(self, supplier_code: str | int, *, date: DateLike | None = None) -> Tender:
        """
        Get tenders by a specific supplier.

        Parameters
        ----------
        supplier_code : str | int
            The code of the supplier to filter tenders by.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified supplier, optionally
            filtered by date.

        Notes
        -----
        - If the given supplier code has no tenders for the specified date
        (or no date is specified), an empty collection will be returned rather
        than an error.
        - If you don't have the supplier code, you can search for it by RUT using
        the suppliers resource, e.g. `client.suppliers.search(...)`, which will
        return the supplier record matching that RUT (if any).

        Examples
        --------
        If you don't have the supplier code, you can search for it by RUT:

        ```python
        from cl_forge import MarketClient

        client = MarketClient("your_api_key")
        supplier = client.suppliers.search("70017820-K", only_record=True)
        response = client.tenders.by_supplier(supplier.code, date="2026-05-04")
        ```
        """
        query = TenderQuery(date=date, supplier_code=supplier_code)
        return self._get_tenders(query)


class AsyncTendersResource(BaseTendersResource[Tender, TenderDetails]):
    async def today(self) -> Tender:
        """
        Get today's tenders by all statuses.

        Returns
        -------
        Tender
            A collection of all tenders for today, regardless of their status.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.today()

        response = asyncio.run(main())
        ```
        """
        return await self._aget_tenders()

    async def details(self, tender_code: str) -> TenderDetails:
        """
        Get the details of a specific tender by its code.

        Parameters
        ----------
        tender_code : str
            The code of the tender to retrieve details for.

        Returns
        -------
        TenderDetails
            The details of the specified tender.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.details("1003473-14-LR26")

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(tender_code=tender_code)
        return await self._aget_details(query)

    async def by_date(self, date: DateLike) -> Tender:
        """
        Get tenders by a specific date, regardless of their status.

        Parameters
        ----------
        date : DateLike
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified date.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.by_date("2024-01-01")

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(date=date)
        return await self._aget_tenders(query)

    async def active(self) -> Tender:
        """
        Get active tenders.

        Returns
        -------
        Tender
            A collection of active tenders.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.active()

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(status=TenderStatus.others.ACTIVE, allow_others=True)
        return await self._aget_tenders(query)

    async def all(self, date: DateLike | None = None) -> Tender:
        """
        Get all tenders regardless of their status, optionally filtered by date.

        Parameters
        ----------
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of all tenders, optionally filtered by date.

        Examples
        --------
        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.all(date="2024-01-01")

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(status=TenderStatus.others.ALL, allow_others=True, date=date)
        return await self._aget_tenders(query)

    async def by_buyer(self, buyer_code: str | int, *, date: DateLike | None = None) -> Tender:
        """
        Get tenders by a specific buyer.

        Parameters
        ----------
        buyer_code : str | int
            The code of the buyer (public entity) to filter tenders by.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified buyer, optionally
            filtered by date.

        Examples
        --------
        If you already have the buyer code:

        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.by_buyer(12345, date="2024-01-01")

        response = asyncio.run(main())
        ```

        If you don't have the buyer code, you can search for it by name using
        the buyers resource, e.g. `client.buyers.search()`, which will return
        all the available buyer records. Then you can filter those records by name:

        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            buyers = await client.buyers.search()
            buyer = buyers.contains("UNIVERSIDAD DE CHILE").root[0]
            return await client.tenders.by_buyer(buyer.code, date="2024-01-01")

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(date=date, buyer_code=buyer_code)
        return await self._aget_tenders(query)

    async def by_status(self, status: TenderStatusLike, *, date: DateLike | None = None) -> Tender:
        """
        Get tenders by a specific status.

        Parameters
        ----------
        status : TenderStatusLike
            The status to filter tenders by. Can be a case-insensitive string
            matching a value of :class:`TenderStatus`, or a value of
            :class:`TenderStatus` itself.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified status, optionally
            filtered by date.

        Examples
        --------
        Using a string for the status parameter:

        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.by_status("Adjudicada", date="2026-05-04")
        
        response = asyncio.run(main())
        ```

        Using a :class:`TenderStatus` value for the status parameter:

        ```python
        import asyncio
        from cl_forge import AsyncMarketClient, TenderStatus

        async def main():
            client = AsyncMarketClient("your_api_key")
            return await client.tenders.by_status(TenderStatus.AWARDED, date="2026-05-04")

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(status=status, date=date)
        return await self._aget_tenders(query)

    async def by_supplier(self, supplier_code: str | int, *, date: DateLike | None = None) -> Tender:  # noqa: E501
        """
        Get tenders by a specific supplier.

        Parameters
        ----------
        supplier_code : str | int
            The code of the supplier to filter tenders by.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified supplier, optionally
            filtered by date.

        Notes
        -----
        - If the given supplier code has no tenders for the specified date
        (or no date is specified), an empty collection will be returned rather
        than an error.
        - If you don't have the supplier code, you can search for it by RUT using
        the suppliers resource, e.g. `client.suppliers.search(...)`, which will
        return the supplier record matching that RUT (if any).

        Examples
        --------
        If you don't have the supplier code, you can search for it by RUT:

        ```python
        import asyncio
        from cl_forge import AsyncMarketClient

        async def main():
            client = AsyncMarketClient("your_api_key")
            supplier = await client.suppliers.search("70017820-K", only_record=True)
            return await client.tenders.by_supplier(supplier.code, date="2026-05-04")

        response = asyncio.run(main())
        ```
        """
        query = TenderQuery(date=date, supplier_code=supplier_code)
        return await self._aget_tenders(query)
