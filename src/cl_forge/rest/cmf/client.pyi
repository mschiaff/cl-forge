from typing import Any, Literal, overload

from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord

class CmfClient(BaseCmfClient):
    @overload
    def ipc(
            self,
            *,
            year: None = ...,
            raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    def ipc(
            self,
            *,
            year: int,
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    def ipc(
            self,
            *,
            year: int,
            month: int,
            raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    def ipc(
            self,
            *,
            year: int | None = ...,
            month: None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def ipc(
            self,
            *,
            year: int,
            month: int,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def ipc(
            self,
            *,
            year: int | None = ...,
            month: None = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    def ipc(
            self,
            *,
            year: int,
            month: int,
            raw: Literal["xml"],
    ) -> str: ...
