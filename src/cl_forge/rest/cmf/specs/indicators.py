from __future__ import annotations

from ..models.euro import EuroCollection, EuroRecord
from ..models.ipc import IpcCollection, IpcRecord
from ..models.uf import UfCollection, UfRecord
from ..models.usd import UsdCollection, UsdRecord
from ..models.utm import UtmCollection, UtmRecord
from .base import IndicatorSpec

IPC_SPEC = IndicatorSpec[
    IpcRecord,
    IpcCollection
](
    public_name="IPC",
    path_name="ipc",
    root_key="IPCs",
    record_model=IpcRecord,
    collection_model=IpcCollection,
)

UF_SPEC = IndicatorSpec[
    UfRecord,
    UfCollection
](
    public_name="UF",
    path_name="uf",
    root_key="UFs",
    record_model=UfRecord,
    collection_model=UfCollection,
    daily=True,
)

UTM_SPEC = IndicatorSpec[
    UtmRecord,
    UtmCollection
](
    public_name="UTM",
    path_name="utm",
    root_key="UTMs",
    record_model=UtmRecord,
    collection_model=UtmCollection,
)

USD_SPEC = IndicatorSpec[
    UsdRecord,
    UsdCollection
](
    public_name="USD",
    path_name="dolar",
    root_key="Dolares",
    record_model=UsdRecord,
    collection_model=UsdCollection,
    daily=True,
)

EURO_SPEC = IndicatorSpec[
    EuroRecord,
    EuroCollection
](
    public_name="EURO",
    path_name="euro",
    root_key="Euros",
    record_model=EuroRecord,
    collection_model=EuroCollection,
    daily=True,
)
