from typing import Any, Literal, overload

from cl_forge.rest.market.types import MarketTransport, ResponseFormat


class BaseMarketRawResource:
    def __init__(self, transport: MarketTransport) -> None:
        self._transport = transport

    @overload
    def _get(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    def _get(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...

    def _get(
            self,
            path: str,
            fmt: ResponseFormat = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str:
        return self._transport.get(path, fmt=fmt, params=params)

    @overload
    async def _aget(
            self,
            path: str,
            fmt: Literal["json"] = ...,
            params: dict[str, Any] | None = ...
    ) -> dict[str, Any]: ...
    @overload
    async def _aget(
            self,
            path: str,
            fmt: Literal["xml"],
            params: dict[str, Any] | None = ...
    ) -> str: ...

    async def _aget(
            self,
            path: str,
            fmt: ResponseFormat = "json",
            params: dict[str, Any] | None = None
    ) -> dict[str, Any] | str:
        return await self._transport.aget(path, fmt=fmt, params=params)
