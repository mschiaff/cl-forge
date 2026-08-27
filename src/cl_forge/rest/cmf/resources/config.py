from typing import TypeVar

from pydantic.dataclasses import dataclass

from cl_forge.rest._types import NonEmptyStr
from cl_forge.rest.resources.base import ResourceSpec

from .types import ListModel, RecordModel

RecordT = TypeVar("RecordT", bound=RecordModel)
ListT = TypeVar("ListT", bound=ListModel)


@dataclass(slots=True, frozen=True)
class CmfResourceSpec[RecordT, ListT](ResourceSpec):
    """
    Configuration for a specific CMF resource endpoint.

    Parameters
    ----------
    endpoint: NonEmptyStr
        The relative path of the resource endpoint.
    root: NonEmptyStr | None
        The root key in the JSON response that contains
        the resource data, if applicable.
    """

    root: NonEmptyStr
    record_type: type[RecordT]
    list_type: type[ListT]
