from __future__ import annotations

from ..models.ipc import IpcCollection, IpcRecord
from ..models.uf import UfCollection, UfRecord
from .base import IndicatorSpec

IPC_SPEC = IndicatorSpec[
    IpcRecord,
    IpcCollection
](
    public_name="IPC",
    path_name="ipc",
    root_key="IPCs",
    record_model=IpcRecord,
    collection_model=IpcCollection
)

UF_SPEC = IndicatorSpec[
    UfRecord,
    UfCollection
](
    public_name="UF",
    path_name="uf",
    root_key="UFs",
    record_model=UfRecord,
    collection_model=UfCollection
)
