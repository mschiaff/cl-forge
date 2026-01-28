from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

class MarketClient:
    """
    Represents a client for interacting with the Chilean Public Market API.

    The API is free to use, but requires an API ticket for authentication
    which can be requested in `Contact`_ and is usually sent to the given
    email during the day.

    .. _Contact: https://api.mercadopublico.cl/modules/IniciarSesion.aspx

    Attributes
    ----------
    ticket : str
        The API ticket used for authenticating requests to the market API.
    base_url : str
        The base URL of the market API endpoint.
    """
    def __init__(self, ticket: str) -> None:
        """
        Initializes the MarketClient with the provided API ticket.

        Parameters
        ----------
        ticket : str
            The API ticket for authenticating requests.
        """

    @property
    def ticket(self) -> str:
        """
        Gets the API ticket used for authenticating requests.

        Returns
        -------
        str
            The API ticket.
        """

    @property
    def base_url(self) -> str:
        """
        Gets the base URL of the market API endpoint.

        Returns
        -------
        str
            The base URL of the market API.
        """

    def get(self, path: str) -> dict[str, Any]:
        """
        Sends a GET request to the specified path of the market API. See the
        `API Docs`_ for all the available endpoints.

        .. _API Docs: https://api.mercadopublico.cl/modules/api.aspx

        Parameters
        ----------
        path : str
            The API path to send the GET request to.

        Returns
        -------
        dict[str, Any]
            The JSON response from the API as a dictionary.
        """

    def __repr__(self) -> str: ...