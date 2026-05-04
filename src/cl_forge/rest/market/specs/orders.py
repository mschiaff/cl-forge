from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from ..models.orders import Order


@dataclass(frozen=True, slots=True)
class OrderSpec[
    RecordsT: BaseModel,
]:
    path_name: str
    record_model: type[RecordsT]


ORDER_SPEC = OrderSpec[
    Order
](
    path_name="/OrdenesDeCompra",
    record_model=Order,
)
