from __future__ import annotations

from typing import Literal

class CmfClient:
    """
    Client for interacting with the Chilean CMF API.

    The API is free to use, but has a limit of 10.000 monthly requests per
    user and requires an API key for authentication, which can be requested in
    `Contact`_ and is usually sent to the given email during the day.

    .. _Contact: https://api.cmfchile.cl/api_cmf/contactanos.jsp

    Attributes
    ----------
    api_key: str
        Truncated API Key to at most 5 characters.
    base_url: str
        The base URL for the CMF API.

    Notes
    -----
    - CMF stands for `Comisión para el Mercado Financiero`.
    """
    def __init__(self, api_key: str) -> None:
        """
        Initializes the CMF client with the provided API key.

        Parameters
        ----------
        api_key: str
            The API key for authenticating with the CMF API.
        """

    def get(
            self,
            path: str,
            format: Literal['json', 'xml'] = 'json', # noqa: A002
            params: dict | None = None
    ) -> dict | str:
        """
        Sends a GET request to the specified CMF API endpoint. See the `API Docs`_
        for all the available endpoints.

        .. _API Docs: https://api.cmfchile.cl/documentacion/index.html

        Parameters
        ----------
        path : str
            The API endpoint path. Must start with '/'.
        format : Literal['json', 'xml']
            The format of the response. Must be lower case 'json' or 'xml'.
            Defaults to 'json'.
        params : dict | None
            Optional query parameters for the request.

        Raises
        ------
        EmptyPath
            If the path is empty.
        InvalidPath
            If the path doesn't start with '/'.
        BadStatus
            If the request doesn't succeed (status code != 200).
        ValueError
            If the format is not 'json' or 'xml', or if fail to parse JSON the
            response.

        Returns
        -------
        dict | str
            The response from the CMF API. Returns a dict if format is 'json', 
            and a str if format is 'xml'.
        """