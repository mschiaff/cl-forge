from cl_forge.rest.cmf.models.rates import TipList, TipRecord

from .config import CmfResourceSpec
from .rates import AsyncRateResource, SyncRateResource

TIP_SPEC = CmfResourceSpec[TipRecord, TipList](
    endpoint="/tip",
    root="TIPs",
    record_type=TipRecord,
    list_type=TipList,
)


class SyncTipResource(SyncRateResource[TipRecord, TipList]):
    _spec = TIP_SPEC


class AsyncTipResource(AsyncRateResource[TipRecord, TipList]):
    _spec = TIP_SPEC
