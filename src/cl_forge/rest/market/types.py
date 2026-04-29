from __future__ import annotations

import datetime
import enum
from typing import Annotated, Any, Literal, Protocol, overload

from pydantic import AfterValidator, PlainSerializer, StringConstraints

__all__ = ("DateLike", "MarketTransport", "StatusLike", "TenderStatus", "TenderStatusCode")


DATE_FORMAT = "%d%m%Y"
"""Date format required by the Market API for date params."""

DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
"""Regex pattern to validate date strings in ISO format (yyyy-mm-dd)."""


def to_date(date: datetime.datetime | datetime.date) -> datetime.date:
    return date.date() if isinstance(date, datetime.datetime) else date

def serialize_date(date: datetime.date) -> str:
    return date.strftime(DATE_FORMAT)


type ResponseFormat = Literal["json", "xml"]


class TenderStatus(enum.StrEnum):
    PUBLISHED = "publicada"
    CLOSED = "cerrada"
    DESERTED = "desierta"
    AWARDED = "adjudicada"
    REVOKED = "revocada"
    SUSPENDED = "suspendida"

    @enum.nonmember
    class others(enum.StrEnum):  # noqa: N801
        ALL = "todos"
        ACTIVE = "activas"

    @classmethod
    def from_str(cls, status: str) -> TenderStatus:
        for member in cls:
            if member == status.strip().lower():
                return member
        raise ValueError(f"Unknown status: {status!r}")


class TenderStatusCode(enum.IntEnum):
    PUBLISHED = 5
    CLOSED = 6
    DESERTED = 7
    AWARDED = 8
    REVOKED = 15
    SUSPENDED = 16


type DateObject = Annotated[
    datetime.datetime | datetime.date,
    AfterValidator(to_date),
]
type DateString = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        pattern=DATE_PATTERN
    ),
    AfterValidator(
        datetime.date.fromisoformat
    ),
]
type DateLike = Annotated[
    DateObject | DateString,
    PlainSerializer(
        serialize_date,
        return_type=str
    )
]


type StatusString = Annotated[
    str,
    StringConstraints(
        to_lower=True,
        strip_whitespace=True
    ),
    AfterValidator(
        TenderStatus.from_str
    ),
]
type StatusLike = Annotated[
    TenderStatus | StatusString,
    PlainSerializer(
        lambda s: s.value,
        return_type=str
    ),
]


class MarketTransport(Protocol):
    @property
    def base_url(self) -> str: ...

    @property
    def api_key(self) -> str: ...

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
