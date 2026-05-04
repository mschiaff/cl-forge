from __future__ import annotations

import enum
from typing import Self

__all__ = ("OrderStatus", "OrderStatusCode", "TenderStatus", "TenderStatusCode")


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


class OrderStatus(BaseStrEnum):
    ACCEPTED = "Aceptada"
    CANCELED = "Cancelada"
    SENT = "EnviadaProveedor"
    RECEIVED = "RecepcionConforme"
    PENDING = "PendienteRecepcion"
    PARTIAL = "RecepcionadaParcialmente"
    INCOMPLETE = "RecepcionConformeIncompleta"

    @enum.nonmember
    class others(BaseStrEnum):  # noqa: N801
        ALL = "Todos"


class OrderStatusCode(enum.IntEnum):
    SENT = 4
    IN_PROCESS = 5
    ACCEPTED = 6
    CANCELED = 9
    RECEIVED = 12
