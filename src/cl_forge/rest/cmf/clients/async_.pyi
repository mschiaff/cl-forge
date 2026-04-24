from typing import Any, Literal, overload

from cl_forge.core.impl.cmf import BaseCmfClient
from cl_forge.rest.cmf.schemas import IpcRecord, ListIpcRecord, ListUfRecord, UfRecord

class AsyncCmfClient(BaseCmfClient):
    @overload
    async def ipc(
            self,
            *,
            year: None = ...,
            month: None = ...,
            raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    async def ipc(
            self,
            *,
            year: int,
            month: None = ...,
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    async def ipc(
            self,
            *,
            year: int,
            month: int,
            raw: None = ...,
    ) -> IpcRecord: ...
    @overload
    async def ipc(
            self,
            *,
            year: int | None = ...,
            month: None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def ipc(
            self,
            *,
            year: int,
            month: int,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def ipc(
            self,
            *,
            year: int | None = ...,
            month: None = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    async def ipc(
            self,
            *,
            year: int,
            month: int,
            raw: Literal["xml"],
    ) -> str: ...

    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            mode: Literal["after", "before"] = ...,
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            mode: Literal["between"],
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            mode: Literal["between"],
            raw: None = ...,
    ) -> ListIpcRecord: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            mode: Literal["after", "before"] = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            mode: Literal["between"],
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            mode: Literal["between"],
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            mode: Literal["after", "before"] = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            mode: Literal["between"],
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    async def ipc_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            mode: Literal["between"],
            raw: Literal["xml"],
    ) -> str: ...

    @overload
    async def uf(
            self,
            *,
            year: None = ...,
            month: None = ...,
            day: None = ...,
            raw: None = ...,
    ) -> UfRecord: ...
    @overload
    async def uf(
            self,
            *,
            year: int,
            month: int | None = ...,
            day: None = ...,
            raw: None = ...,
    ) -> ListUfRecord: ...
    @overload
    async def uf(
            self,
            *,
            year: int,
            month: int,
            day: int,
            raw: None = ...,
    ) -> UfRecord: ...
    @overload
    async def uf(
            self,
            *,
            year: None = ...,
            month: None = ...,
            day: None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def uf(
            self,
            *,
            year: int,
            month: int | None = ...,
            day: None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def uf(
            self,
            *,
            year: int,
            month: int,
            day: int | None = ...,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def uf(
            self,
            *,
            year: None = ...,
            month: None = ...,
            day: None = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    async def uf(
            self,
            *,
            year: int,
            month: int | None = ...,
            day: None = ...,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    async def uf(
            self,
            *,
            year: int,
            month: int,
            day: int | None = ...,
            raw: Literal["xml"],
    ) -> str: ...

    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            day: None = ...,
            mode: Literal["after", "before"] = ...,
            raw: None = ...,
    ) -> ListUfRecord: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            day: None = ...,
            mode: Literal["after", "before"] = ...,
            raw: Literal["json"]
    ) -> dict[str, Any]: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int | None = ...,
            end_year: None = ...,
            end_month: None = ...,
            day: None = ...,
            mode: Literal["after", "before"] = ...,
            raw: Literal["xml"]
    ) -> str: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: None = ...,
            end_month: None = ...,
            day: int | None = ...,
            mode: Literal["after", "before"] = ...,
            raw: None = ...,
    ) -> ListUfRecord: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: None = ...,
            end_month: None = ...,
            day: int | None = ...,
            mode: Literal["after", "before"] = ...,
            raw: Literal["json"]
    ) -> dict[str, Any]: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: None = ...,
            end_month: None = ...,
            day: int | None = ...,
            mode: Literal["after", "before"] = ...,
            raw: Literal["xml"]
    ) -> str: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            day: None = ...,
            mode: Literal["between"],
            raw: None = ...,
    ) -> ListUfRecord: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            day: None = ...,
            mode: Literal["between"],
            raw: Literal["json"]
    ) -> dict[str, Any]: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: None = ...,
            end_year: int,
            end_month: None = ...,
            day: None = ...,
            mode: Literal["between"],
            raw: Literal["xml"]
    ) -> str: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            day: None = ...,
            mode: Literal["between"],
            raw: None = ...,
    ) -> ListUfRecord: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            day: None = ...,
            mode: Literal["between"],
            raw: Literal["json"]
    ) -> dict[str, Any]: ...
    @overload
    async def uf_range(
            self,
            *,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
            day: None = ...,
            mode: Literal["between"],
            raw: Literal["xml"]
    ) -> str: ...
