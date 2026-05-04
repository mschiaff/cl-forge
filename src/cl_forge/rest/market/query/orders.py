from __future__ import annotations

from pydantic import BaseModel, Field

from ..types import DateLike, OrderStatusLike  # noqa: TC001


class OrderQuery(BaseModel):
    """
    Represents the query parameters for fetching orders from the Market API.

    Once initialized, the :attr:`params` property can be used to get the query
    parameters as a dict with keys matching the API's expected parameter names,
    which can then be passed to the API request.
    """
    allow_others: bool = Field(
        default=False,
        exclude=True,
        repr=False,
        description="Whether to allow `OrderStatus.others` status values."
    )

    order_code: str | None = Field(
        default=None,
        serialization_alias="Codigo",
        description="The code of the order to query.",
    )
    status: OrderStatusLike | None = Field(
        default=None,
        serialization_alias="Estado",
        description="The status of the order to query.",
    )
    date: DateLike | None = Field(
        default=None,
        serialization_alias="Fecha",
        description=(
            "The date for which to query orders. Can be "
            "either `datetime.datetime`, `datetime.date`, "
            "or ISO format string (yyyy-mm-dd)."
        ),
    )

    @property
    def params(self) -> dict[str, str]:
        """
        Returns the query parameters as a dict with keys matching the API's
        expected parameter names.

        Notes
        -----
        - Only includes fields that are not `None`.
        - Uses Pydantic's :class:`Field` `serialization_alias` for field
          names to match the API's expected parameter names.
        """
        return self.model_dump(by_alias=True, exclude_none=True)
