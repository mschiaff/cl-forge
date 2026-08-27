from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from cl_forge.rest.resources.base import AsyncResource, SyncResource
from cl_forge.rest.resources.formats import QueryParameterFormat

from .config import CmfResourceSpec
from .types import ListModel, RecordModel

if TYPE_CHECKING:
    from httpx2 import Response


class CmfDataHandler[RecordT: RecordModel, ListT: ListModel]:
    _spec: CmfResourceSpec[RecordT, ListT]

    def _extract_records(self, response: Response) -> list[dict[str, Any]]:
        data = response.json()

        try:
            records = data[self._spec.root]
        except KeyError as error:
            raise ValueError(f"Missing CMF response root {self._spec.root!r}") from error

        if not isinstance(records, list):
            raise TypeError(f"Expected {self._spec.root!r} to contain a list")

        return cast("list[dict[str, Any]]", records)

    def _parse_record(self, response: Response) -> RecordT:
        records = self._extract_records(response)

        if len(records) != 1:
            raise ValueError(f"Expected exactly one record, got {len(records)!r}")

        return self._spec.record_type.model_validate(records[0])

    def _parse_list(self, response: Response) -> ListT:
        records = self._extract_records(response)

        return self._spec.list_type.model_validate(records)


class SyncCmfResource[RecordT: RecordModel, ListT: ListModel](
    CmfDataHandler[RecordT, ListT], SyncResource[CmfResourceSpec[RecordT, ListT]]
):
    _reserved_params = frozenset({"apikey"})
    _format_policy = QueryParameterFormat("formato")


class AsyncCmfResource[RecordT: RecordModel, ListT: ListModel](
    CmfDataHandler[RecordT, ListT], AsyncResource[CmfResourceSpec[RecordT, ListT]]
):
    _reserved_params = frozenset({"apikey"})
    _format_policy = QueryParameterFormat("formato")
