from cl_forge.rest.cmf.models.indexes import UfList, UfRecord

from .config import CmfResourceSpec
from .daily import AsyncDailyIndexResource, SyncDailyIndexResource

UF_SPEC = CmfResourceSpec[UfRecord, UfList](
    endpoint="/uf",
    root="UFs",
    record_type=UfRecord,
    list_type=UfList,
)


class SyncUfResource(SyncDailyIndexResource[UfRecord, UfList]):
    _spec = UF_SPEC


class AsyncUfResource(AsyncDailyIndexResource[UfRecord, UfList]):
    _spec = UF_SPEC
