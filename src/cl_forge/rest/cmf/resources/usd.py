from cl_forge.rest.cmf.models.indexes import UsdList, UsdRecord

from .config import CmfResourceSpec
from .daily import AsyncDailyIndexResource, SyncDailyIndexResource

USD_SPEC = CmfResourceSpec[UsdRecord, UsdList](
    endpoint="/dolar",
    root="Dolares",
    record_type=UsdRecord,
    list_type=UsdList,
)


class SyncUsdResource(SyncDailyIndexResource[UsdRecord, UsdList]):
    _spec = USD_SPEC


class AsyncUsdResource(AsyncDailyIndexResource[UsdRecord, UsdList]):
    _spec = USD_SPEC
