#TODO: Remove this entire module when ready with refactorin CMF endpoints
from cl_forge.core.endpoints import (
    EuroEndpoint,
    IpcEndpoint,
    UfEndpoint,
    UsdEndpoint,
    UtmEndpoint,
)
from cl_forge.rest.cmf.clients import CmfClient

__all__ = (
    "CmfClient",
    "EuroEndpoint",
    "IpcEndpoint",
    "UfEndpoint",
    "UsdEndpoint",
    "UtmEndpoint",
)
