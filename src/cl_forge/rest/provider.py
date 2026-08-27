import enum

from pydantic import PositiveInt
from pydantic.dataclasses import dataclass

from cl_forge.rest._types import BaseUrl
from cl_forge.rest.auth.spec import AuthSpec


class ApiProvider(enum.StrEnum):
    """API provider families."""

    CMF = enum.auto()
    MARKET = enum.auto()


@dataclass(frozen=True, slots=True)
class ProviderSpec:
    """Connection details for one provider API version.

    Parameters
    ----------
    family : ApiProvider
        Provider family.
    version : ApiVersion
        Positive API version.
    base_url : str
        Absolute HTTP or HTTPS base URL.
    auth : AuthSpec
        API-key authentication convention.
    """

    family: ApiProvider
    version: PositiveInt
    base_url: BaseUrl
    auth: AuthSpec
