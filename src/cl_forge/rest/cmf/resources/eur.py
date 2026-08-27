from cl_forge.rest.cmf.models.indexes import EurList, EurRecord

from .config import CmfResourceSpec
from .daily import AsyncDailyIndexResource, SyncDailyIndexResource

EUR_SPEC = CmfResourceSpec[EurRecord, EurList](
    endpoint="/euro",
    root="Euros",
    record_type=EurRecord,
    list_type=EurList,
)


class SyncEurResource(SyncDailyIndexResource[EurRecord, EurList]):
    _spec = EUR_SPEC


class AsyncEurResource(AsyncDailyIndexResource[EurRecord, EurList]):
    _spec = EUR_SPEC


# Compatibility aliases for the established Euro spelling.
EURO_SPEC = EUR_SPEC
SyncEuroResource = SyncEurResource
AsyncEuroResource = AsyncEurResource
