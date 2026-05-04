from typing import Any, Literal, overload

class BaseMarketClient:
    """
    Represents a client for interacting with the Chilean Public Market API.

    Notes
    -----
    The API is free to use, but requires an API ticket for authentication
    which can be requested in [Contact](https://api.mercadopublico.cl/modules/
    IniciarSesion.aspx) and is usually sent to the given email during the day.

    Attributes
    ----------
    api_key : str
        The API ticket used for authenticating requests to the market API.
    base_url : str
        The base URL of the market API endpoint.
    """
    def __init__(self, api_key: str) -> None:
        """
        Initializes the MarketClient with the provided API ticket.

        Parameters
        ----------
        api_key : str
            The API ticket for authenticating requests.
        """

    @property
    def api_key(self) -> str:
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

    @overload
    def get(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    def get(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...
    @overload
    def get(
            self,
            path: str,
            fmt: Literal["json", "xml"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any] | str: ...

    def get(
            self,
            path: str,
            fmt: Literal["json", "xml"] = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str:
        """
        Sends a GET request to the specified path of the market API.

        Notes
        -----
        See the [API Docs](https://api.mercadopublico.cl/modules/api.aspx)
        for all the available endpoints.

        Parameters
        ----------
        path : str
            The API path to send the GET request to.
        fmt : Literal["json", "xml"]
            The format of the response. Defaults to "json".
            When set to "xml", the response will be returned as
            a string, otherwise it will be parsed as a dictionary.
        params : dict[str, Any] | None
            Optional query parameters to include in the request.

        Returns
        -------
        dict[str, Any] | str
            The JSON response from the API as a dictionary or the XML response
            as a string.

        Raises
        ------
        ValueError
            If the API key is included in `params`.
        """
    
    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...
    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["json", "xml"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any] | str: ...
    
    async def aget(
            self,
            path: str,
            fmt: Literal["json", "xml"] = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str:
        """
        Async implementation of :meth:`get`.
        
        Sends a GET request to the specified path of the market API.

        Notes
        -----
        See the [API Docs](https://api.mercadopublico.cl/modules/api.aspx)
        for all the available endpoints.

        Parameters
        ----------
        path : str
            The API path to send the GET request to.
        fmt : Literal["json", "xml"]
            The format of the response. Defaults to "json".
            When set to "xml", the response will be returned as
            a string, otherwise it will be parsed as a dictionary.
        params : dict[str, Any] | None
            Optional query parameters to include in the request.

        Returns
        -------
        dict[str, Any] | str
            The JSON response from the API as a dictionary or the XML response
            as a string.

        Raises
        ------
        ValueError
            If the API key is included in `params`.
        """
