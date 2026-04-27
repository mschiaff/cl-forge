from __future__ import annotations

from typing import Annotated, Any, Literal, Protocol, overload

from pydantic import Field

type RawFormat = Literal["json", "xml"]

type YearInt = Annotated[int, Field(ge=0)]
type MonthInt = Annotated[int, Field(ge=1, le=12)]
type DayInt = Annotated[int, Field(ge=1, le=31)]

type TwoTupleDate = tuple[YearInt, MonthInt]
type ThreeTupleDate = tuple[YearInt, MonthInt, DayInt]


class CmfTransport(Protocol):
    @property
    def base_url(self) -> str: ...

    @property
    def api_key(self) -> str: ...

    @overload
    def get(self, path: str, fmt: Literal["json"] = ... ) -> dict[str, Any]: ...
    @overload
    def get(self, path: str, fmt: Literal["xml"]) -> str: ...
    @overload
    def get(self, path: str, fmt: RawFormat = ...) -> dict[str, Any] | str: ...

    def get(self, path: str, fmt: RawFormat = "json") -> dict[str, Any] | str: ...

    @overload
    async def aget(self, path: str, fmt: Literal["json"] = ... ) -> dict[str, Any]: ...
    @overload
    async def aget(self, path: str, fmt: Literal["xml"]) -> str: ...
    @overload
    async def aget(self, path: str, fmt: RawFormat = ...) -> dict[str, Any] | str: ...

    async def aget(self, path: str, fmt: RawFormat = "json") -> dict[str, Any] | str: ...
