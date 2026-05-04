from __future__ import annotations

from ..models.orders import Order, OrderDetails
from ..query.orders import OrderQuery
from .base import BaseOrdersResource


class OrdersResource(BaseOrdersResource[Order, OrderDetails]):
    def today(self) -> Order:
        return self._get_orders()

    def details(self, order_code: str) -> OrderDetails:
        query = OrderQuery(order_code=order_code)
        return self._get_details(query)
