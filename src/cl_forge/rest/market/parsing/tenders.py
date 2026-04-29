from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from ..types import DateLike, StatusLike  # noqa: TC001


class TenderQuery(BaseModel):
    """
    Represents the query parameters for fetching tenders from the Market API.

    Once initialized, the :attr:`params` property can be used to get the query
    parameters as a dict with keys matching the API's expected parameter names,
    which can then be passed to the API request.
    """
    allow_others: bool = Field(
        default=False,
        exclude=True,
        repr=False,
        description="Whether to allow `TenderStatus.others` status values."
    )

    tender_code: str | None = Field(
        default=None,
        serialization_alias="Codigo",
        description="The code of the tender to query.",
    )
    buyer_code: str | None = Field(
        default=None,
        serialization_alias="CodigoOrganismo",
        description="The code of the buyer to query.",
    )
    supplier_code: str | None = Field(
        default=None,
        serialization_alias="CodigoProveedor",
        description="The code of the supplier to query.",
    )
    status: StatusLike | None = Field(
        default=None,
        serialization_alias="Estado",
        description="The status of the tender to query.",
    )
    date: DateLike | None = Field(
        default=None,
        serialization_alias="Fecha",
        description=(
            "The date for which to query tenders. Can be "
            "either `datetime.datetime`, `datetime.date`, "
            "or ISO format string (yyyy-mm-dd)."
        ),
    )

    @property
    def params(self) -> dict[str, Any]:
        """
        Returns the query parameters as a dict with keys matching the API's
        expected parameter names.

        Notes
        -----
        - Only includes fields that are not `None`.
        - Uses Pydantic's :class:`Field` `serialization_alias` for field
          names to match the API's expected parameter names.
        """
        # Market API expects query params names to be
        # in Spanish, so we use the `serialization_alias`
        # to get the correct param names, and we also exclude
        # any fields that are `None` since we don't want to
        # include those in the query, and the API might not
        # handle `None` values correctly.
        return self.model_dump(by_alias=True, exclude_none=True)
