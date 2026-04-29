from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.tenders import Tender, TenderDetails
from ..parsing.tenders import TenderQuery
from .base import BaseTendersResource

if TYPE_CHECKING:
    from ..types import DateLike, StatusLike


class TendersResource(BaseTendersResource[Tender, TenderDetails]):
    def today(self) -> Tender:
        return self._get_tenders()

    def details(self, code: str) -> TenderDetails:
        query = TenderQuery(tender_code=code)
        return self._get_details(query)

    def by_date(self, date: DateLike) -> Tender:
        query = TenderQuery(date=date)
        return self._get_tenders(query)

    def by_status(self,
            status: StatusLike,
            *,
            date: DateLike | None = None
    ) -> Tender:
        query = TenderQuery(status=status, date=date)
        return self._get_tenders(query)
