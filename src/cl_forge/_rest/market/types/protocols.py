from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Protocol, overload

if TYPE_CHECKING:
    from ...auth import ApiKeyCredentials


__all__ = ("MarketTransport", "ResponseFormat",)


type ResponseFormat = Literal["json", "xml"]


class MarketTransport(Protocol):
    @property
    def base_url(self) -> str: ...

    @property
    def credentials(self) -> ApiKeyCredentials: ...

    @overload
    def get(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    def get(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...
    @overload
    def get(
            self,
            path: str,
            fmt: ResponseFormat = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any] | str: ...

    def get(
            self,
            path: str,
            fmt: ResponseFormat = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str: ...

    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    async def aget(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...
    @overload
    async def aget(
            self,
            path: str,
            fmt: ResponseFormat = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any] | str: ...

    async def aget(
            self,
            path: str,
            fmt: ResponseFormat = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str: ...
