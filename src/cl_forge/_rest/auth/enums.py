from __future__ import annotations

import enum

__all__ = ("CredentialScope",)


class CredentialScope(enum.StrEnum):
    """
    Credential scopes for the different clients.

    Each scope corresponds to a specific API client (e.g., CMF, Market)
    and is used by credential providers to determine which API key to
    load based on the client's needs.

    Notes
    -----
    - Internally, only the scope `name` attribute is used to construct the
    environment variable prefix (e.g., `CLFORGE_CMF_`), which is then used
    by providers like `EnvCredentials` and `DotEnvCredentials` to load the
    appropriate API key for the given scope.
    """

    CMF = enum.auto()
    """Scope for the CMF API client."""
    MARKET = enum.auto()
    """Scope for the Market API client."""
