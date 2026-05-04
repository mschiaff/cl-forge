from __future__ import annotations

import datetime
from typing import Annotated

from pydantic import AfterValidator, PlainSerializer, PositiveInt, StringConstraints

from .constants import DATE_PATTERN
from .enums import TenderStatus
from .helpers import (
    int_rut_validator,
    serialize_date,
    string_rut_validator,
    to_date,
    validate_tender_status,
)

__all__ = ("DateLike", "RutLike", "TenderStatusLike",)


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

type TenderStatusString = Annotated[
    str,
    StringConstraints(
        to_lower=True,
        strip_whitespace=True
    ),
    AfterValidator(
        validate_tender_status
    ),
]
type TenderStatusLike = Annotated[
    TenderStatus | TenderStatusString,
    PlainSerializer(
        lambda s: s.value,
        return_type=str
    ),
]

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
type RutInt = Annotated[
    int,
    PositiveInt,
    AfterValidator(
        int_rut_validator
    ),
]
type RutLike = Annotated[
    RutString | RutInt,
    ...
]
