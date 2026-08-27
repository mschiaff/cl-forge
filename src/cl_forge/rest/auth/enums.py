import enum


class AuthLocation(enum.StrEnum):
    """Supported API-key locations."""

    QUERY = enum.auto()
    HEADER = enum.auto()


class AuthScheme(enum.StrEnum):
    """Supported API-key authentication schemes."""

    NONE = ""
    BEARER = "Bearer"
    BASIC = "Basic"
    TOKEN = "Token"
