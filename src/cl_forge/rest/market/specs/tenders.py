from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from ..models.tenders import Tender, TenderDetails


@dataclass(frozen=True, slots=True)
class TenderSpec[
    RecordsT: BaseModel,
    DetailsT: BaseModel
]:
    path_name: str
    record_model: type[RecordsT]
    details_model: type[DetailsT]


TENDER_SPEC = TenderSpec[
    Tender,
    TenderDetails
](
    path_name="/licitaciones",
    record_model=Tender,
    details_model=TenderDetails,
)
