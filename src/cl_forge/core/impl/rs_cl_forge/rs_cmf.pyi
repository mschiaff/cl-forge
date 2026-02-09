from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal, overload

class CmfClient:
    """
    Base client for interacting with the CMF API.

    Notes
    -----
    The API is free to use, but has a limit of 10.000 monthly requests per
    user and requires an API key for authentication, which can be requested
    in [Contact](https://api.cmfchile.cl/api_cmf/contactanos.jsp) and is
    usually sent to the given email during the day.

    Attributes
    ----------
    api_key : str
        The API ticket used for authenticating requests to the CMF API.
    base_url : str
        The base URL of the CMF API.

    Raises
    ------
    EmptyApiKey
        If no API key is provided or it's empty.
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the CMF client with the provided API key.

        Parameters
        ----------
        api_key: str
            The API key for authenticating with the CMF API.
        """

    def __repr__(self) -> str: ...

    @property
    def api_key(self) -> str:
        """
        Gets the API Key used for authenticating requests.

        Returns
        -------
        str
            The API Key.
        """

    @property
    def base_url(self) -> str:
        """
        Gets the base URL of the CMF API.

        Returns
        -------
        str
            The base URL of the CMF API.
        """

    @overload
    def get(
            self,
            path: str,
            fmt: Literal["json"] = ...
    ) -> dict[str, list[dict[str, str]]]: ...

    @overload
    def get(
            self,
            path: str,
            fmt: Literal["xml"]
    ) -> str: ...

    def get(
            self,
            path: str,
            fmt: Literal["json", "xml"] = "json"
    ) -> dict[str, list[dict[str, str]]] | str:
        """
        Sends a GET request to the specified CMF API endpoint.

        Notes
        -----
        See the [API Docs](https://api.cmfchile.cl/documentacion/index.html)
        for all the available endpoints.

        Parameters
        ----------
        path : str
            The API endpoint path. Must start with ``'/'``.
        fmt : Literal["json", "xml"]
            The format of the response. Can be ``'json'``, ``'xml'``.

        Returns
        -------
        dict[str, list[dict[str, str]]] | str
            The response from the CMF API. Returns a ``dict`` if format is
            ``'json'`` and a ``str`` if format is ``'xml'``.
        """