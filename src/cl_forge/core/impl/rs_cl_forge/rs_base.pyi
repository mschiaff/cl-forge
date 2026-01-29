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