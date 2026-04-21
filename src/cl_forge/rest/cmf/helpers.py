from __future__ import annotations

from typing import Literal


def validate_month(month: int, word: Literal["start", "end"] | None = None) -> None:
    _word = f"{word.capitalize()} month" if word else "Month"

    if not (1 <= month <= 12):
        raise ValueError(f"{_word} must be between 1 and 12.")


def validate_day(day: int) -> None:
    if not (1 <= day <= 31):
        raise ValueError("Day must be between 1 and 31.")


def is_range_between_months(
        start_year: int,
        start_month: int | None,
        end_year: int | None,
        end_month: int | None,
        alt: str
) -> bool:
    if not end_year:
            raise ValueError(
                "End year must be specified for 'between' mode."
            )
    if start_year > end_year:
        raise ValueError(
            "Start year cannot be greater than end year for 'between' mode."
        )
    if start_month and not end_month:
        raise ValueError(
            "End month must be specified if start month is specified for 'between' mode."
        )
    if not start_month and end_month:
        raise ValueError(
            "Start month must be specified if end month is specified for 'between' mode."
        )
    if start_month and end_month:
        if (start_year, start_month) > (end_year, end_month):
            raise ValueError(
                "Start date cannot be greater than end date for 'between' mode."
            )
        if (start_year, start_month) == (end_year, end_month):
            raise ValueError(
                f"For individual month query, use the {alt!r} method."
            )
        return True
    return False
