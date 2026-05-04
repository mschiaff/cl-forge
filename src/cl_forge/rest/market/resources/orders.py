from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.orders import Order, OrderDetails
from ..query.orders import OrderQuery
from .base import BaseOrdersResource

if TYPE_CHECKING:
    from ..types import DateLike


class OrdersResource(BaseOrdersResource[Order, OrderDetails]):
    def today(self) -> Order:
        return self._get_orders()

    def details(self, order_code: str) -> OrderDetails:
        query = OrderQuery(order_code=order_code)
        return self._get_details(query)

    def by_date(self, date: DateLike) -> Order:
        query = OrderQuery(date=date)
        return self._get_orders(query)

    def by_status(self, status: str, *, date: DateLike | None = None) -> Order:
        query = OrderQuery(status=status, date=date)
        return self._get_orders(query)
