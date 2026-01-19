"""Simple yet powerful Chilean and other tools written in Rust and Python."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import cmf, verify

__all__ = (
    "cmf",
    "verify",
)


import importlib


def __getattr__(name: str):
    if name in __all__:
        return importlib.import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")