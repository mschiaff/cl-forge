from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, overload

from pydantic import BaseModel, RootModel

from .shape import ResponseShape

if TYPE_CHECKING:
    from ..specs.base import IndicatorSpec


class CmfResponseParser[
    RecordT: BaseModel,
    CollectionT: RootModel[list[BaseModel]]
]:
    def __init__(
            self,
            spec: IndicatorSpec[RecordT, CollectionT]
    ) -> None:
        self._spec = spec
    
    @overload
    def parse(
            self,
            response: dict[str, Any],
            *,
            shape: Literal[ResponseShape.SINGLE],
    ) -> RecordT: ...
    @overload
    def parse(
            self,
            response: dict[str, Any],
            *,
            shape: Literal[ResponseShape.COLLECTION],
    ) -> CollectionT: ...

    def parse(
            self,
            response: dict[str, Any],
            *,
            shape: ResponseShape
    ) -> RecordT | CollectionT:
        records = self._extract_records(response)

        if shape is ResponseShape.SINGLE:
            return self._parse_single(records)

        return self._parse_collection(records)

    def _extract_records(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        try:
            records = response[self._spec.root_key]
        except KeyError as error:
            available_keys = ", ".join(response.keys())

            raise KeyError(
                f"Expected key {self._spec.root_key!r} "
                f"in CMF response. Available keys: {available_keys}"
            ) from error

        if not isinstance(records, list):
            raise TypeError(
                f"Expected response[{self._spec.root_key!r}]  "
                f"to be a list, but got {type(records).__name__!r}"
            )

        return records # type: ignore

    def _parse_single(self, records: list[dict[str, Any]]) -> RecordT:
        if len(records) != 1:
            raise ValueError(
                f"Expected exactly one record for "
                f"{self._spec.public_name!r}, but got {len(records)}"
            )

        return self._spec.record_model.model_validate(records[0])

    def _parse_collection(self, records: list[dict[str, Any]]) -> CollectionT:
        return self._spec.collection_model.model_validate(records)
