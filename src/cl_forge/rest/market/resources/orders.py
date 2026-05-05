from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.orders import Order, OrderDetails
from ..query.orders import OrderQuery
from ..types import OrderStatus
from .base import BaseOrdersResource

if TYPE_CHECKING:
    from ..types import DateLike, OrderStatusLike


class OrdersResource(BaseOrdersResource[Order, OrderDetails]):
    def today(self) -> Order:
        """
        Get today's purchase orders by all statuses.

        Returns
        -------
        Order
            A collection of all purchase orders for today,
            regardless of their status.
        """
        return self._get_orders()

    def details(self, order_code: str) -> OrderDetails:
        """
        Get the details of a specific purchase order.

        Parameters
        ----------
        order_code : str
            The code of the purchase order to retrieve details for.

        Returns
        -------
        OrderDetails
            The details of the specified purchase order.
        """
        query = OrderQuery(order_code=order_code)
        return self._get_details(query)

    def by_date(self, date: DateLike) -> Order:
        """
        Get purchase orders by a specific date.

        Parameters
        ----------
        date : DateLike
            The date to filter purchase orders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Order
            A collection of purchase orders for the specified date.
        """
        query = OrderQuery(date=date)
        return self._get_orders(query)

    def all(self, date: DateLike | None = None) -> Order:
        """
        Get all purchase orders, optionally filtered by date.

        Parameters
        ----------
        date : DateLike, optional
            The date to filter purchase orders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Order
            A collection of all purchase orders, optionally filtered by date.
        """
        query = OrderQuery(status=OrderStatus.others.ALL, allow_others=True, date=date)
        return self._get_orders(query)

    def by_buyer(self, buyer_code: str | int, *, date: DateLike | None = None) -> Order:
        """
        Get purchase orders by a specific buyer.

        Parameters
        ----------
        buyer_code : str | int
            The code of the buyer to filter purchase orders by.
        date : DateLike, optional
            The date to filter purchase orders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Order
            A collection of purchase orders for the specified buyer,
            optionally filtered by date.
        """
        query = OrderQuery(date=date, buyer_code=buyer_code)
        return self._get_orders(query)

    def by_status(self, status: OrderStatusLike, *, date: DateLike | None = None) -> Order:
        """
        Get purchase orders by a specific status.

        Parameters
        ----------
        status : OrderStatusLike
            The status to filter purchase orders by.
        date : DateLike, optional
            The date to filter purchase orders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Order
            A collection of purchase orders with the specified status,
            optionally filtered by date.
        """
        query = OrderQuery(status=status, date=date)
        return self._get_orders(query)

    def by_supplier(self, supplier_code: str | int, *, date: DateLike | None = None) -> Order:
        """
        Get purchase orders by a specific supplier.

        Parameters
        ----------
        supplier_code : str | int
            The code of the supplier to filter purchase orders by.
        date : DateLike, optional
            The date to filter purchase orders by. Can be a `datetime.datetime`,
            `datetime.date`, or an ISO format string (yyyy-mm-dd).

        Returns
        -------
        Order
            A collection of purchase orders for the specified supplier,
            optionally filtered by date.
        """
        query = OrderQuery(date=date, supplier_code=supplier_code)
        return self._get_orders(query)
