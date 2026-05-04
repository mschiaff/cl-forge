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
        return self._get_tenders()

    def details(self, tender_code: str) -> TenderDetails:
        query = TenderQuery(tender_code=tender_code)
        return self._get_details(query)

    def active(self) -> Tender:
        query = TenderQuery(
            status=TenderStatus.others.ACTIVE,
            allow_others=True
        )
        return self._get_tenders(query)

    def all(self, date: DateLike | None = None) -> Tender:
        query = TenderQuery(
            status=TenderStatus.others.ALL,
            allow_others=True,
            date=date,
        )
        return self._get_tenders(query)

    def by_date(self, date: DateLike) -> Tender:
        query = TenderQuery(date=date)
        return self._get_tenders(query)

    def by_status(self,
            status: TenderStatusLike,
            *,
            date: DateLike | None = None
    ) -> Tender:
        query = TenderQuery(status=status, date=date)
        return self._get_tenders(query)

    def by_buyer(
            self,
            buyer_code: str | int,
            *,
            date: DateLike | None = None,
    ) -> Tender:
        query = TenderQuery(
            date=date,
            buyer_code=buyer_code,
        )
        return self._get_tenders(query)

    def by_supplier(
            self,
            supplier_code: str | int,
            *,
            date: DateLike | None = None,
    ) -> Tender:
        query = TenderQuery(
            date=date,
            supplier_code=supplier_code,
        )
        return self._get_tenders(query)
