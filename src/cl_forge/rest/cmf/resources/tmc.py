from cl_forge.rest.cmf.models.rates import TmcList, TmcRecord

from .config import CmfResourceSpec
from .rates import AsyncRateResource, SyncRateResource

TMC_SPEC = CmfResourceSpec[TmcRecord, TmcList](
    endpoint="/tmc",
    root="TMCs",
    record_type=TmcRecord,
    list_type=TmcList,
)


class SyncTmcResource(SyncRateResource[TmcRecord, TmcList]):
    _spec = TMC_SPEC


class AsyncTmcResource(AsyncRateResource[TmcRecord, TmcList]):
    _spec = TMC_SPEC
