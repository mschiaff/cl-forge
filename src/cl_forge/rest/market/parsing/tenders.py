import datetime
import re
from typing import Any

from pydantic import BaseModel, Field, field_serializer, field_validator

DATE_FORMAT = "%d%m%Y"
"""Date format required by the Market API for date params."""

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
"""Regex pattern to validate date strings in ISO format (yyyy-mm-dd)."""


class TenderQuery(BaseModel):
    """
    Represents the query parameters for fetching tenders
    from the Market API.
    """
    
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
    status: str | None = Field(
        default=None,
        serialization_alias="Estado",
        description="The status of the tender to query.",
    )
    date: datetime.datetime | datetime.date | str | None = Field(
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
        Returns the query parameters as a dict with keys
        matching the API's expected parameter names.

        Notes
        -----
        - Only includes fields that are not `None`.
        """
        return self.model_dump(by_alias=True, exclude_none=True)

    @field_validator("date", mode="before")
    @classmethod
    def _parse_date(
            cls,
            value: datetime.datetime | datetime.date | str | None
    ) -> datetime.date | None:
        # Even though "date" field accepts `datetime`, `date` or
        # ISO format str, we make sure to always convert it to
        # `date` so internally we only deal with `date` or `None`.
        if isinstance(value, str):
            if DATE_PATTERN.match(value):
                return datetime.date.fromisoformat(value)
            raise ValueError(
                "Expected ISO format date string "
                f"(yyyy-mm-dd), but got: {value!r}"
            )

        if isinstance(value, datetime.datetime):
            return value.date()

        return value

    @field_serializer("date", return_type=str | None)
    def _serialize_date(self, value: datetime.date | None) -> str | None:
        # "date" field accepts `date`, `datetime` or ISO format str,
        # but because of field validator up to this point it can
        # only be `date` or `None`.
        if value is not None:
            return value.strftime(DATE_FORMAT)
