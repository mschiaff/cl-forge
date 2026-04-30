from __future__ import annotations

import enum
from typing import Self

__all__ = ("TenderStatus", "TenderStatusCode")


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
