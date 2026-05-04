from __future__ import annotations

from pydantic import BaseModel


class OrderQuery(BaseModel):
    """
    Represents the query parameters for fetching orders from the Market API.

    Once initialized, the :attr:`params` property can be used to get the query
    parameters as a dict with keys matching the API's expected parameter names,
    which can then be passed to the API request.
    """

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
