from __future__ import annotations

from typing import TYPE_CHECKING

from cl_forge.core.impl.cmf import BaseCmfClient

from .resources.monthly import MonthlyIndicatorResource
from .specs.indicators import IPC_SPEC

if TYPE_CHECKING:
    from .models.ipc import IpcCollection, IpcRecord
    from .types import CmfTransport

class CmfClient:
    ipc: MonthlyIndicatorResource[IpcRecord, IpcCollection]

    def __init__(self, api_key: str) -> None:
        self._transport: CmfTransport = BaseCmfClient(api_key)

        self.ipc = MonthlyIndicatorResource(
            transport=self._transport,
            spec=IPC_SPEC
        )
