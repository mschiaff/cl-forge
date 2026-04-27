from __future__ import annotations

from ..models.ipc import IpcCollection, IpcRecord
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
