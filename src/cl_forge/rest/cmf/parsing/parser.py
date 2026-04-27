from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .shape import ResponseShape

if TYPE_CHECKING:
    from pydantic import BaseModel, RootModel
    
    from ..specs.base import IndicatorSpec


class CmfResponseParser[T: BaseModel, C: RootModel[Any]]:
    def __init__(self, spec: IndicatorSpec[T, C]) -> None:
        self._spec = spec

    def parse(
            self,
            response: dict[str, Any],
            *,
            shape: ResponseShape
    ) -> T | C:
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

    def _parse_single(self, records: list[dict[str, Any]]) -> T:
        if len(records) != 1:
            raise ValueError(
                f"Expected exactly one record for "
                f"{self._spec.public_name!r}, but got {len(records)}"
            )

        return self._spec.record_model.model_validate(records[0])

    def _parse_collection(self, records: list[dict[str, Any]]) -> C:
        return self._spec.collection_model.model_validate(records)
