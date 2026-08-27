from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from ..models.orders import Order, OrderDetails


@dataclass(frozen=True, slots=True)
class OrderSpec[
    RecordsT: BaseModel,
    DetailsT: BaseModel
]:
    path_name: str
    record_model: type[RecordsT]
    details_model: type[DetailsT]


ORDER_SPEC = OrderSpec[
    Order,
    OrderDetails
](
    path_name="/OrdenesDeCompra",
    record_model=Order,
    details_model=OrderDetails,
)
