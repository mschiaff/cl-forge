from typing import Any, Literal, overload

from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import ResponseFormat

class CmfClient(BaseCmfClient):
    @overload
    def ipc(
        self,
        year: None = ...,
        *,
        raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    def ipc(
        self,
        year: int,
        *,
        raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    def ipc(
        self,
        year: int | None = ...,
        *,
        raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def ipc(
        self,
        year: int | None = ...,
        *,
        raw: Literal["xml"],
    ) -> str: ...

    def ipc(
            self,
            year: int | None = None,
            *,
            raw: ResponseFormat | None = None
    ) -> IpcRecord | ListIpcRecord | dict[str, Any] | str: ...