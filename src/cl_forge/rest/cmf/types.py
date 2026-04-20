from __future__ import annotations

from typing import NamedTuple

from cl_forge.core.types import BaseType


class FormatType(
        NamedTuple(
            "FormatType",
            [("fmt", str)]
        ),
        BaseType
):
    JSON = "json"
    XML = "xml"


class ModeType(
        NamedTuple(
            "ModeType",
            [("path", str)]
        ),
        BaseType
):
    AFTER = "/ipc/posteriores"
    BEFORE = "/ipc/anteriores"
    BETWEEN = "/ipc/periodo"
