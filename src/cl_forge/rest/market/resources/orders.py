from __future__ import annotations

from ..models.orders import Order
from .base import BaseOrdersResource


class OrdersResource(BaseOrdersResource[Order]):
    def today(self) -> Order:
        return self._get_orders()
