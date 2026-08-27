from __future__ import annotations

from cl_forge.rest.cmf.models.rates import TipCollection, TipRecord, TmcCollection, TmcRecord
from cl_forge.rest.cmf.specs.base import RateSpec

TIP_SPEC = RateSpec[
    TipRecord,
    TipCollection
](
    public_name="TIP",
    path_name="tip",
    root_key="TIPs",
    record_model=TipRecord,
    collection_model=TipCollection,
)

TMC_SPEC = RateSpec[
    TmcRecord,
    TmcCollection
](
    public_name="TMC",
    path_name="tmc",
    root_key="TMCs",
    record_model=TmcRecord,
    collection_model=TmcCollection,
)
