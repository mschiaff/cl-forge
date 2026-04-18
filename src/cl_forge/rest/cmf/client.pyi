from typing import Any, Literal, Never, overload

from cl_forge.core.compat import deprecated
from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import ResponseFormat

class CmfClient(BaseCmfClient):
    @overload
    @deprecated("Month cannot be specified without year.")
    def ipc(
        self,
        year: None = ...,
        month: int = ...,
        *,
        raw: ResponseFormat | None = ...,
    ) -> Never: ...
    @overload
    def ipc(
        self,
        year: None = ...,
        month: None = ...,
        *,
        raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    def ipc(
        self,
        year: int,
        month: None = ...,
        *,
        raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    def ipc(
        self,
        year: int,
        month: int,
        *,
        raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    def ipc(
        self,
        year: int | None = ...,
        month: int | None = ...,
        *,
        raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def ipc(
        self,
        year: int | None = ...,
        month: int | None = ...,
        *,
        raw: Literal["xml"],
    ) -> str: ...
