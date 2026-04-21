from __future__ import annotations

from typing import NamedTuple

from cl_forge.core.types import BaseType


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
