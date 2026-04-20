from typing import Any, Literal, overload

from cl_forge.core.impl.rs_cl_forge.rs_cmf import BaseCmfClient  # type: ignore
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord
from cl_forge.rest.cmf.types import RangeMode, ResponseFormat

class CmfClient(BaseCmfClient):
    @overload
    def ipc(
            self,
            *,
            year: None = ...,
            month: None = ...,
            raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    def ipc(
            self,
            *,
            year: int,
            month: None = ...,
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
    @overload
    def ipc(
            self,
            *,
            year: int | None = ...,
            month: int | None = ...,
            raw: ResponseFormat | None = ...,
    ) -> IpcRecord | ListIpcRecord | dict[str, Any] | str: ...

    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            mode: RangeMode = ...,
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            mode: RangeMode = ...,
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            mode: RangeMode = ...,
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            mode: RangeMode = ...,
            raw: Literal["json"] = ...,
    ) -> dict[str, Any]: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            mode: RangeMode = ...,
            raw: Literal["json"] = ...,
    ) -> dict[str, Any]: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            mode: RangeMode = ...,
            raw: Literal["json"] = ...,
    ) -> dict[str, Any]: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            mode: RangeMode = ...,
            raw: Literal["xml"] = ...,
    ) -> str: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            mode: RangeMode = ...,
            raw: Literal["xml"] = ...,
    ) -> str: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            mode: RangeMode = ...,
            raw: Literal["xml"] = ...,
    ) -> str: ...
    @overload
    def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: int | None = ...,
            end_month: int | None = ...,
            mode: RangeMode = ...,
            raw: ResponseFormat | None = ...,
    ) -> IpcRecord | ListIpcRecord | dict[str, Any] | str: ...