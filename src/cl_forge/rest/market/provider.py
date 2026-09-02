from cl_forge.rest.auth.enums import ApiProvider, AuthLocation
from cl_forge.rest.auth.spec import AuthSpec
from cl_forge.rest.provider import ProviderSpec

MARKET_V1 = ProviderSpec(
    family=ApiProvider.MARKET,
    version=1,
    base_url="https://api.mercadopublico.cl/servicios/v1/publico",
    auth=AuthSpec(label="ticket", location=AuthLocation.QUERY),
)

MARKET_V2 = ProviderSpec(
    family=ApiProvider.MARKET,
    version=2,
    base_url="https://api2.mercadopublico.cl/v2",
    auth=AuthSpec(label="ticket", location=AuthLocation.HEADER),
)

__all__ = ("MARKET_V1", "MARKET_V2")
