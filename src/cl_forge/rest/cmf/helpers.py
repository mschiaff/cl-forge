from __future__ import annotations

from typing import Literal


def validate_month(month: int, word: Literal["start", "end"] | None = None) -> None:
    _word = f"{word.capitalize()} month" if word else "Month"

    if not (1 <= month <= 12):
        raise ValueError(f"{_word} must be between 1 and 12.")


def validate_day(day: int) -> None:
    if not (1 <= day <= 31):
        raise ValueError("Day must be between 1 and 31.")