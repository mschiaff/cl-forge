from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.impl.cmf import BaseCmfClient

from .resources.daily import AsyncDailyIndicatorResource, DailyIndicatorResource
from .resources.monthly import AsyncMonthlyIndicatorResource, MonthlyIndicatorResource
from .resources.rates import AsyncRateResource, RateResource
from .resources.raw import AsyncRawResource, RawResource
from .specs.indicators import EURO_SPEC, IPC_SPEC, UF_SPEC, USD_SPEC, UTM_SPEC
from .specs.rates import TIP_SPEC, TMC_SPEC

if TYPE_CHECKING:
    from cl_forge.rest.cmf.models.indicators import (
        EuroCollection,
        EuroRecord,
        IpcCollection,
        IpcRecord,
        UfCollection,
        UfRecord,
        UsdCollection,
        UsdRecord,
        UtmCollection,
        UtmRecord,
    )
    from cl_forge.rest.cmf.models.rates import TipCollection, TipRecord, TmcCollection, TmcRecord
    from cl_forge.rest.cmf.types import CmfTransport


__all__ = ("AsyncCmfClient", "CmfClient",)


class CmfClient:
    """Client for interacting with the CMF API."""
    
    raw: RawResource
    """Resource for accessing raw CMF API requests."""
    
    ipc: MonthlyIndicatorResource[IpcRecord, IpcCollection]
    """Resource for accessing IPC indicator data."""
    uf: DailyIndicatorResource[UfRecord, UfCollection]
    """Resource for accessing UF indicator data."""
    utm: MonthlyIndicatorResource[UtmRecord, UtmCollection]
    """Resource for accessing UTM indicator data."""
    usd: DailyIndicatorResource[UsdRecord, UsdCollection]
    """Resource for accessing USD/CLP exchange rate data."""
    euro: DailyIndicatorResource[EuroRecord, EuroCollection]
    """Resource for accessing Euro/CLP exchange rate data."""
    tip: RateResource[TipRecord, TipCollection]
    """Resource for accessing TIP data."""
    tmc: RateResource[TmcRecord, TmcCollection]
    """Resource for accessing TMC data."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize the CMF client.

        Parameters
        ----------
        api_key : str
            The API key for authenticating with the CMF API.
        """
        self._transport: CmfTransport = BaseCmfClient(api_key)

        self.raw = RawResource(self._transport)

        self.ipc = MonthlyIndicatorResource(transport=self._transport, spec=IPC_SPEC)
        self.uf = DailyIndicatorResource(transport=self._transport, spec=UF_SPEC)
        self.utm = MonthlyIndicatorResource(transport=self._transport, spec=UTM_SPEC)
        self.usd = DailyIndicatorResource(transport=self._transport, spec=USD_SPEC)
        self.euro = DailyIndicatorResource(transport=self._transport, spec=EURO_SPEC)
        self.tip = RateResource(transport=self._transport, spec=TIP_SPEC)
        self.tmc = RateResource(transport=self._transport, spec=TMC_SPEC)

    @property
    def api_key(self) -> str:
        """
        Get the API key used for authentication.

        Returns
        -------
        str
            The API key.
        """
        return self._transport.api_key

    @property
    def base_url(self) -> str:
        """
        Get the base URL for the CMF API.

        Returns
        -------
        str
            The base URL.
        """
        return self._transport.base_url


class AsyncCmfClient:
    """Asynchronous client for interacting with the CMF API."""
    
    raw: AsyncRawResource
    """Resource for accessing raw CMF API requests."""
    
    ipc: AsyncMonthlyIndicatorResource[IpcRecord, IpcCollection]
    """Resource for accessing IPC indicator data."""
    uf: AsyncDailyIndicatorResource[UfRecord, UfCollection]
    """Resource for accessing UF indicator data."""
    utm: AsyncMonthlyIndicatorResource[UtmRecord, UtmCollection]
    """Resource for accessing UTM indicator data."""
    usd: AsyncDailyIndicatorResource[UsdRecord, UsdCollection]
    """Resource for accessing USD/CLP exchange rate data."""
    euro: AsyncDailyIndicatorResource[EuroRecord, EuroCollection]
    """Resource for accessing Euro/CLP exchange rate data."""
    tip: AsyncRateResource[TipRecord, TipCollection]
    """Resource for accessing TIP data."""
    tmc: AsyncRateResource[TmcRecord, TmcCollection]
    """Resource for accessing TMC data."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize the asynchronous CMF client.

        Parameters
        ----------
        api_key : str
            The API key for authenticating with the CMF API.
        """
        self._transport: CmfTransport = BaseCmfClient(api_key)

        self.raw = AsyncRawResource(self._transport)

        self.ipc = AsyncMonthlyIndicatorResource(transport=self._transport, spec=IPC_SPEC)
        self.uf = AsyncDailyIndicatorResource(transport=self._transport, spec=UF_SPEC)
        self.utm = AsyncMonthlyIndicatorResource(transport=self._transport, spec=UTM_SPEC)
        self.usd = AsyncDailyIndicatorResource(transport=self._transport, spec=USD_SPEC)
        self.euro = AsyncDailyIndicatorResource(transport=self._transport, spec=EURO_SPEC)
        self.tip = AsyncRateResource(transport=self._transport, spec=TIP_SPEC)
        self.tmc = AsyncRateResource(transport=self._transport, spec=TMC_SPEC)

    @property
    def api_key(self) -> str:
        """
        Get the API key used for authentication.

        Returns
        -------
        str
            The API key.
        """
        return self._transport.api_key

    @property
    def base_url(self) -> str:
        """
        Get the base URL for the CMF API.

        Returns
        -------
        str
            The base URL.
        """
        return self._transport.base_url
