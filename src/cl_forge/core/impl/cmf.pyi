from typing import Any, Literal, Self, overload

from cl_forge.rest.cmf.types import RawFormat

class CoreCmfClient:
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
        The API key used for authenticating requests to the CMF API.
    base_url : str
        The base URL of the CMF API.

    Raises
    ------
    EmptyApiKey
        If no API key is provided or it's empty.
    """
    def __new__(cls, api_key: str) -> Self: ...

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
        Gets the API key used for authenticating requests.

        Returns
        -------
        str
            The API key.
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
    ) -> dict[str, Any]: ...
    @overload
    def get(
            self,
            path: str,
            fmt: Literal["xml"]
    ) -> str: ...
    @overload
    def get(
            self,
            path: str,
            fmt: RawFormat = ...
    ) -> dict[str, Any] | str: ...

    def get(
            self,
            path: str,
            fmt: RawFormat = "json"
    ) -> dict[str, Any] | str:
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
        fmt : RawFormat
            The format of the response. Can be ``'json'``, ``'xml'``.

        Returns
        -------
        dict[str, Any] | str
            The response from the CMF API. Returns a ``dict`` if format is
            ``'json'`` and a ``str`` if format is ``'xml'``.
        """
    
    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["json"] = ...
    ) -> dict[str, Any]: ...
    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["xml"]
    ) -> str: ...
    @overload
    async def aget(
            self,
            path: str,
            fmt: RawFormat = ...
    ) -> dict[str, Any] | str: ...

    async def aget(
            self,
            path: str,
            fmt: RawFormat = "json"
    ) -> dict[str, Any] | str:
        """
        Async implementation of :meth:`get`.
        
        Sends a GET request to the specified CMF API endpoint.

        Notes
        -----
        See the [API Docs](https://api.cmfchile.cl/documentacion/index.html)
        for all the available endpoints.

        Parameters
        ----------
        path : str
            The API endpoint path. Must start with ``'/'``.
        fmt : RawFormat
            The format of the response. Can be ``'json'``, ``'xml'``.

        Returns
        -------
        dict[str, Any] | str
            The response from the CMF API. Returns a ``dict`` if format is
            ``'json'`` and a ``str`` if format is ``'xml'``.
        """
