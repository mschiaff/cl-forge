import enum


class ApiProvider(enum.StrEnum):
    """API provider families and credential scopes."""

    CMF = enum.auto()
    MARKET = enum.auto()


# There is intentionally only one provider/scope enum. Keeping the old name as a
# compatibility alias for credential-provider implementations.
CredentialScope = ApiProvider


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
