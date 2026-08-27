import enum
from datetime import date, datetime
from typing import Self

from cl_forge.core.impl.verify import calculate_verifier, validate_rut

type DateLike = date | datetime | str
type RutLike = int | str


class CaseInsensitiveStrEnum(enum.StrEnum):
    """String enum with a whitespace- and case-insensitive parser."""

    @classmethod
    def parse(cls, value: Self | str) -> Self:
        if isinstance(value, cls):
            return value

        normalized = value.strip().casefold()
        for member in cls:
            if member.value.casefold() == normalized:
                return member
        raise ValueError(f"Unknown {cls.__name__}: {value!r}")


class TenderStatus(CaseInsensitiveStrEnum):
    PUBLISHED = "publicada"
    CLOSED = "cerrada"
    DESERTED = "desierta"
    AWARDED = "adjudicada"
    REVOKED = "revocada"
    SUSPENDED = "suspendida"


class TenderStatusFilter(CaseInsensitiveStrEnum):
    ALL = "todos"
    ACTIVE = "activas"


class TenderStatusCode(enum.IntEnum):
    PUBLISHED = 5
    CLOSED = 6
    DESERTED = 7
    AWARDED = 8
    REVOKED = 18
    SUSPENDED = 19


class OrderStatus(CaseInsensitiveStrEnum):
    SENT = "EnviadaProveedor"
    ACCEPTED = "Aceptada"
    CANCELED = "Cancelada"
    RECEIVED = "RecepcionConforme"
    PENDING = "PendienteRecepcion"
    PARTIAL = "RecepcionadaParcialmente"
    INCOMPLETE = "RecepcionConformeIncompleta"


class OrderStatusFilter(CaseInsensitiveStrEnum):
    ALL = "Todos"


class OrderStatusCode(enum.IntEnum):
    SENT = 4
    IN_PROCESS = 5
    ACCEPTED = 6
    CANCELED = 9
    RECEIVED = 12
    PENDING = 13
    PARTIAL = 14
    INCOMPLETE = 15


type TenderStatusLike = TenderStatus | str
type OrderStatusLike = OrderStatus | str


def serialize_date(value: DateLike) -> str:
    """Serialize a supported date input using Mercado Publico's ``ddmmyyyy`` format."""
    parsed: date
    if isinstance(value, datetime):
        parsed = value.date()
    elif isinstance(value, date):
        parsed = value
    else:
        try:
            parsed = date.fromisoformat(value.strip())
        except ValueError as error:
            raise ValueError("Date strings must use ISO format YYYY-MM-DD") from error
    return parsed.strftime("%d%m%Y")


def normalize_rut(value: RutLike) -> str:
    """Validate and format a Chilean RUT for the supplier-directory endpoint."""
    if isinstance(value, bool):
        raise TypeError("RUT digits must be an integer, not bool")

    if isinstance(value, int):
        if value <= 0:
            raise ValueError("RUT digits must be positive")
        digits = value
        verifier = calculate_verifier(digits)
    else:
        normalized = value.strip().upper().replace(".", "")
        if normalized.count("-") != 1:
            raise ValueError("RUT must contain one hyphen separating digits and verifier")
        raw_digits, verifier = normalized.split("-", 1)
        if not raw_digits.isdecimal() or len(verifier) != 1:
            raise ValueError("RUT must contain numeric digits and one verifier character")
        digits = int(raw_digits)
        if not validate_rut(digits, verifier):
            expected = calculate_verifier(digits)
            raise ValueError(f"Invalid RUT verifier: expected {expected!r}, got {verifier!r}")
    return f"{digits:,}".replace(",", ".") + f"-{verifier}"


__all__ = (
    "DateLike",
    "OrderStatus",
    "OrderStatusCode",
    "OrderStatusFilter",
    "OrderStatusLike",
    "RutLike",
    "TenderStatus",
    "TenderStatusCode",
    "TenderStatusFilter",
    "TenderStatusLike",
    "normalize_rut",
    "serialize_date",
)
