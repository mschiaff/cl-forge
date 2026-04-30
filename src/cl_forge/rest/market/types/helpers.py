from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from cl_forge import calculate_verifier, validate_rut

from .constants import DATE_FORMAT
from .enums import TenderStatus

if TYPE_CHECKING:
    from pydantic import ValidationInfo


__all__ = (
    "int_rut_validator",
    "serialize_date",
    "string_rut_validator",
    "to_date",
    "validate_status",
)


#
# Helper functions for DATE related annotated types
#

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


#
# Helper functions for RUT related annotated types
#

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


def int_rut_validator(digits: int) -> str:
    verifier = calculate_verifier(digits)
    return format_rut(digits, verifier)
