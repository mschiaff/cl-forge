from typing import Any, Literal, overload

from cl_forge.core.impl.cmf import BaseCmfClient
from cl_forge.core.types import RangeMode
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord, ListUfRecord, UfRecord

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
            raw: Literal["json"],
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
            raw: Literal["json"],
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
            raw: Literal["json"],
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
            raw: Literal["xml"],
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
            raw: Literal["xml"],
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
            raw: Literal["xml"],
    ) -> str: ...

    @overload
    def uf(
            self,
            *,
            year: None = ...,
            month: None = ...,
            day: None = ...,
            raw: None = ...,
    ) -> UfRecord: ...
    @overload
    def uf(
            self,
            *,
            year: int,
            month: int | None = ...,
            day: None = ...,
            raw: None = ...,
    ) -> ListUfRecord: ...
    @overload
    def uf(
            self,
            *,
            year: int,
            month: int,
            day: int,
            raw: None = ...,
    ) -> UfRecord: ...
    @overload
    def uf(
            self,
            *,
            year: None = ...,
            month: None = ...,
            day: None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def uf(
            self,
            *,
            year: int,
            month: int | None = ...,
            day: None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def uf(
            self,
            *,
            year: int,
            month: int,
            day: int | None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def uf(
            self,
            *,
            year: None = ...,
            month: None = ...,
            day: None = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    def uf(
            self,
            *,
            year: int,
            month: int | None = ...,
            day: None = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    def uf(
            self,
            *,
            year: int,
            month: int,
            day: int | None = ...,
            raw: Literal["xml"],
    ) -> str: ...
