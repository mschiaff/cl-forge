from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from cl_forge.rest.auth.enums import ApiProvider
from cl_forge.rest.client.base import ApiClient
from cl_forge.rest.cmf.provider import CMF_V3
from cl_forge.rest.cmf.resources.eur import AsyncEurResource, SyncEurResource
from cl_forge.rest.cmf.resources.ipc import AsyncIpcResource, SyncIpcResource
from cl_forge.rest.cmf.resources.raw import AsyncRawResource, SyncRawResource
from cl_forge.rest.cmf.resources.tip import AsyncTipResource, SyncTipResource
from cl_forge.rest.cmf.resources.tmc import AsyncTmcResource, SyncTmcResource
from cl_forge.rest.cmf.resources.uf import AsyncUfResource, SyncUfResource
from cl_forge.rest.cmf.resources.usd import AsyncUsdResource, SyncUsdResource
from cl_forge.rest.cmf.resources.utm import AsyncUtmResource, SyncUtmResource

if TYPE_CHECKING:
    from cl_forge.rest.auth.types import CredentialType
    from cl_forge.rest.client.config import ClientConfig


class CmfClient(ApiClient):
    """
    Client for interacting with the CMF API.
    """

    provider: ClassVar[ApiProvider] = ApiProvider.CMF

    raw: SyncRawResource
    ipc: SyncIpcResource
    uf: SyncUfResource
    utm: SyncUtmResource
    usd: SyncUsdResource
    eur: SyncEurResource
    euro: SyncEurResource
    tip: SyncTipResource
    tmc: SyncTmcResource

    def __init__(self, credentials: CredentialType, config: ClientConfig | None = None) -> None:
        super().__init__(credentials, config)
        self._v3 = self._route(CMF_V3)

        self.raw = SyncRawResource(self._v3)
        self.ipc = SyncIpcResource(self._v3)
        self.uf = SyncUfResource(self._v3)
        self.utm = SyncUtmResource(self._v3)
        self.usd = SyncUsdResource(self._v3)
        self.eur = SyncEurResource(self._v3)
        self.euro = self.eur
        self.tip = SyncTipResource(self._v3)
        self.tmc = SyncTmcResource(self._v3)

    @property
    def base_url(self) -> str:
        return CMF_V3.base_url

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(base_url={self.base_url!r}, credentials={self.credentials!r})"
        )


class AsyncCmfClient(ApiClient):
    """
    Asynchronous client for interacting with the CMF API.
    """

    provider: ClassVar[ApiProvider] = ApiProvider.CMF

    raw: AsyncRawResource
    ipc: AsyncIpcResource
    uf: AsyncUfResource
    utm: AsyncUtmResource
    usd: AsyncUsdResource
    eur: AsyncEurResource
    euro: AsyncEurResource
    tip: AsyncTipResource
    tmc: AsyncTmcResource

    def __init__(self, credentials: CredentialType, config: ClientConfig | None = None) -> None:
        super().__init__(credentials, config)
        self._v3 = self._route(CMF_V3)

        self.raw = AsyncRawResource(self._v3)
        self.ipc = AsyncIpcResource(self._v3)
        self.uf = AsyncUfResource(self._v3)
        self.utm = AsyncUtmResource(self._v3)
        self.usd = AsyncUsdResource(self._v3)
        self.eur = AsyncEurResource(self._v3)
        self.euro = self.eur
        self.tip = AsyncTipResource(self._v3)
        self.tmc = AsyncTmcResource(self._v3)

    @property
    def base_url(self) -> str:
        return CMF_V3.base_url

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(base_url={self.base_url!r}, credentials={self.credentials!r})"
        )


__all__ = ("AsyncCmfClient", "CmfClient")
