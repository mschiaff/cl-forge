from pydantic.dataclasses import dataclass

from cl_forge.rest._types import NonEmptyStr
from cl_forge.rest.auth.enums import AuthLocation, AuthScheme


@dataclass(frozen=True, slots=True)
class AuthSpec:
    """Describe how an API key is added to a request.

    Parameters
    ----------
    label : NonEmptyStr
        Query parameter or header name.
    location : AuthLocation
        Location of the API key in the request.
    scheme : AuthScheme
        Authentication scheme to use, if any.
    """

    label: NonEmptyStr
    location: AuthLocation
    scheme: AuthScheme = AuthScheme.NONE
