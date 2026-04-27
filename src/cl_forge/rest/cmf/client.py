from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.impl.cmf import BaseCmfClient

from .resources.daily import DailyIndicatorResource
from .resources.monthly import MonthlyIndicatorResource
from .resources.raw import RawResource
from .specs.indicators import EURO_SPEC, IPC_SPEC, UF_SPEC, USD_SPEC, UTM_SPEC

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
    from cl_forge.rest.cmf.types import CmfTransport

class CmfClient:
    raw: RawResource
    ipc: MonthlyIndicatorResource[IpcRecord, IpcCollection]
    uf: DailyIndicatorResource[UfRecord, UfCollection]
    utm: MonthlyIndicatorResource[UtmRecord, UtmCollection]
    usd: DailyIndicatorResource[UsdRecord, UsdCollection]
    euro: DailyIndicatorResource[EuroRecord, EuroCollection]

    def __init__(self, api_key: str) -> None:
        self._transport: CmfTransport = BaseCmfClient(api_key)

        self.raw = RawResource(self._transport)

        self.ipc = MonthlyIndicatorResource(
            transport=self._transport,
            spec=IPC_SPEC
        )
        self.uf = DailyIndicatorResource(
            transport=self._transport,
            spec=UF_SPEC
        )
        self.utm = MonthlyIndicatorResource(
            transport=self._transport,
            spec=UTM_SPEC
        )
        self.usd = DailyIndicatorResource(
            transport=self._transport,
            spec=USD_SPEC
        )
        self.euro = DailyIndicatorResource(
            transport=self._transport,
            spec=EURO_SPEC
        )
