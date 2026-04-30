from __future__ import annotations

import datetime
import enum
from typing import TYPE_CHECKING, Annotated, Any, Literal, Protocol, Self, overload

from pydantic import AfterValidator, PlainSerializer, PositiveInt, StringConstraints, TypeAdapter

from cl_forge import calculate_verifier, validate_rut

if TYPE_CHECKING:
    from pydantic import ValidationInfo


__all__ = (
    "DateLike",
    "MarketTransport",
    "ResponseFormat",
    "StatusLike",
    "TenderStatus",
    "TenderStatusCode",
)


DATE_FORMAT = "%d%m%Y"
"""Date format required by the Market API for date params."""

DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"
"""Regex pattern to validate date strings in ISO format (yyyy-mm-dd)."""


type ResponseFormat = Literal["json", "xml"]


class BaseStrEnum(enum.StrEnum):
    @classmethod
    def from_str(cls, status: str) -> Self:
        for member in cls:
            if member == status.strip().lower():
                return member
        raise ValueError(f"Unknown status: {status!r}")


class TenderStatus(BaseStrEnum):
    PUBLISHED = "publicada"
    CLOSED = "cerrada"
    DESERTED = "desierta"
    AWARDED = "adjudicada"
    REVOKED = "revocada"
    SUSPENDED = "suspendida"

    @enum.nonmember
    class others(BaseStrEnum):  # noqa: N801
        ALL = "todos"
        ACTIVE = "activas"


class TenderStatusCode(enum.IntEnum):
    PUBLISHED = 5
    CLOSED = 6
    DESERTED = 7
    AWARDED = 8
    REVOKED = 15
    SUSPENDED = 16


def to_date(date: datetime.datetime | datetime.date) -> datetime.date:
    return date.date() if isinstance(date, datetime.datetime) else date

def serialize_date(date: datetime.date) -> str:
    return date.strftime(DATE_FORMAT)

def validate_status(
        value: TenderStatus | TenderStatus.others | str,
        info: ValidationInfo
) -> TenderStatus | TenderStatus.others:
    if info.data.get("allow_others", False):
        return TenderStatus.others.from_str(value)
    return TenderStatus.from_str(value)


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
        validate_status
    ),
]
type StatusLike = Annotated[
    TenderStatus | StatusString,
    PlainSerializer(
        lambda s: s.value,
        return_type=str
    ),
]


def remove_dots(value: str) -> str:
    return value.replace(".", "")

def split_rut(value: str) -> tuple[int, str]:
    if "-" not in value:
        raise ValueError(
            "RUT must contain a hyphen (-) "
            "separating digits and verifier."
        )
    digits, verifier = value.split("-", 1)
    return int(digits), verifier

def place_dots(value: int) -> str:
    return f"{value:,}".replace(",", ".")

def format_rut(digits: int, verifier: str) -> str:
    return f"{place_dots(digits)}-{verifier}"

def string_rut_validator(value: str) -> str:
    value = remove_dots(value)
    digits, verifier = split_rut(value)

    if not validate_rut(digits, verifier):
        calculated = calculate_verifier(digits)
        raise ValueError(
            f"Invalid RUT. Expected verifier: "
            f"{calculated!r}, but got: {verifier!r}."
        )
    return format_rut(digits, verifier)


type RutString = Annotated[
    str,
    StringConstraints(
        to_upper=True,
        strip_whitespace=True,
    ),
    AfterValidator(
        string_rut_validator
    ),
]


def int_rut_validator(digits: int) -> str:
    verifier = calculate_verifier(digits)
    return format_rut(digits, verifier)


type RutInt = Annotated[
    int,
    PositiveInt,
    AfterValidator(
        int_rut_validator
    ),
]


type RutLike = RutString | RutInt
RutLikeAdapter: TypeAdapter[str] = TypeAdapter(RutLike)


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
