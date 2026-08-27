from cl_forge.rest.cmf.models.indexes import UtmList, UtmRecord

from .config import CmfResourceSpec
from .monthly import AsyncMonthlyIndexResource, SyncMonthlyIndexResource

UTM_SPEC = CmfResourceSpec[UtmRecord, UtmList](
    endpoint="/utm",
    root="UTMs",
    record_type=UtmRecord,
    list_type=UtmList,
)


class SyncUtmResource(SyncMonthlyIndexResource[UtmRecord, UtmList]):
    _spec = UTM_SPEC


class AsyncUtmResource(AsyncMonthlyIndexResource[UtmRecord, UtmList]):
    _spec = UTM_SPEC
