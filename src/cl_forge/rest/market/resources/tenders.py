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
        """
        query = TenderQuery(status=TenderStatus.others.ALL, allow_others=True, date=date)
        return self._get_tenders(query)

    def by_buyer(self, buyer_code: str | int, *, date: DateLike | None = None) -> Tender:
        """
        Get tenders by a specific buyer.

        Parameters
        ----------
        buyer_code : str | int
            The code of the buyer to filter tenders by.
        date : DateLike, optional
            The date to filter tenders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Tender
            A collection of tenders for the specified buyer, optionally
            filtered by date.
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
        """
        query = TenderQuery(date=date, supplier_code=supplier_code)
        return self._get_tenders(query)
