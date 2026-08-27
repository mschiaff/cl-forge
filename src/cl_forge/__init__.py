"""Simple yet powerful Chilean and other tools written in Rust and Python."""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("cl-forge")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


from cl_forge.core.impl.verify import (
    Ppu,
    calculate_verifier,
    generate,
    normalize_ppu,
    ppu_to_numeric,
    validate_rut,
)
from cl_forge.core.timing import Timing
from cl_forge.rest.auth import DotEnvCredentials, EnvCredentials
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.cmf.clients import AsyncCmfClient, CmfClient
from cl_forge.rest.market.clients import AsyncMarketClient, MarketClient

__all__ = (
    "AsyncCmfClient",
    "AsyncMarketClient",
    "ClientConfig",
    "CmfClient",
    "DotEnvCredentials",
    "EnvCredentials",
    "MarketClient",
    "Ppu",
    "Timing",
    "calculate_verifier",
    "generate",
    "normalize_ppu",
    "ppu_to_numeric",
    "validate_rut",
)
