from __future__ import annotations

class ClientException(Exception): # noqa: N818
    """Base class for all exceptions raised by API clients."""

class EmptyApiKey(ClientException):
    """Raised when an API key is not provided."""

class EmptyPath(ClientException):
    """Raised when a path is not provided."""

class InvalidPath(ClientException):
    """Raised when API path is invalid."""

class HttpError(ClientException):
    """Raised when an HTTP error occurs."""

class BadStatus(ClientException):
    """Raised when an HTTP status code is not 200 (success)."""

class UnsupportedFormat(ClientException):
    """Raised when an unsupported format is requested."""


class Token:
    """
    Represents API tokens used for authentication.

    Tokens are loaded from environment variables or a .env file.
    System environment variables take precedence over .env file values.
    """

    def __init__(self, dotenv_path: str | None = None) -> None:
        """
        Initializes a new Token instance.

        If ``dotenv_path`` is provided, it loads the .env file from that path.
        Otherwise, it looks for a .env file in the current or parent directories.

        Parameters
        ----------
        dotenv_path : str | None
            Optional path to a .env file. Defaults to None.
        """

    @property
    def cmf(self) -> str:
        """
        Returns the CMF token (API key).

        Loaded from the ``CLFORGE_CMF_TOKEN`` environment variable.
        """

    @property
    def market(self) -> str:
        """
        Returns the Market token (ticket).

        Loaded from the ``CLFORGE_MARKET_TOKEN`` environment variable.
        """

class Config:
    """
    Configuration container for library settings.
    """

    def __init__(self, dotenv_path: str | None = None) -> None:
        """
        Initializes a new Config instance.

        If ``dotenv_path`` is provided, it loads the .env file from that path.
        Otherwise, it looks for a .env file in the current or parent directories.

        Parameters
        ----------
        dotenv_path : str | None
            Optional path to a .env file for loading tokens.

        Notes
        -----
        - Tokens are loaded from environment variables or a .env file. System
          environment variables take precedence over .env file values.
        - If ``dotenv_path`` is provided, it loads the .env file from that path.
          Otherwise, it looks for a .env file in the current or parent directories.
        """

    @property
    def tokens(self) -> Token:
        """
        Returns the loaded API tokens.
        """