from pydantic.dataclasses import dataclass

from cl_forge.rest._types import NonEmptyStr


@dataclass(slots=True, frozen=True)
class ResourceSpec:
    """Specification for a specific resource endpoint."""

    endpoint: NonEmptyStr
