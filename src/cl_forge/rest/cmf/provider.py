from cl_forge.rest.auth.enums import ApiProvider
from cl_forge.rest.auth.spec import AuthLocation, AuthSpec
from cl_forge.rest.provider import ProviderSpec

CMF_V3 = ProviderSpec(
    family=ApiProvider.CMF,
    version=3,
    base_url="https://api.cmfchile.cl/api-sbifv3/recursos_api",
    auth=AuthSpec(label="apikey", location=AuthLocation.QUERY),
)
