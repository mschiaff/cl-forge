from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from cl_forge.rest._types import NonEmptyStr
from cl_forge.rest.resources.base import ResourceSpec


@dataclass(slots=True, frozen=True)
class CmfResourceSpec[RecordT: BaseModel, ListT: BaseModel](ResourceSpec):
    """
    Configuration for a specific CMF resource endpoint.

    Parameters
    ----------
    endpoint: NonEmptyStr
        The relative path of the resource endpoint.
    root: NonEmptyStr
        The root key in the JSON response that contains the resource data.
    """

    root: NonEmptyStr
    record_type: type[RecordT]
    list_type: type[ListT]
