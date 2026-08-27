from cl_forge.rest.cmf.models.indexes import IpcList, IpcRecord

from .config import CmfResourceSpec
from .monthly import AsyncMonthlyIndexResource, SyncMonthlyIndexResource

IPC_SPEC = CmfResourceSpec[IpcRecord, IpcList](
    endpoint="/ipc", root="IPCs", record_type=IpcRecord, list_type=IpcList
)


class SyncIpcResource(SyncMonthlyIndexResource[IpcRecord, IpcList]):
    _spec = IPC_SPEC


class AsyncIpcResource(AsyncMonthlyIndexResource[IpcRecord, IpcList]):
    _spec = IPC_SPEC
