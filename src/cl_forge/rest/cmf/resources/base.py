from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, RootModel

from ..models.base import (
    IndicatorCollection,
    IndicatorRecord,
    InterestRateCollection,
    InterestRateRecord,
)
from ..parsing.parser import CmfResponseParser

if TYPE_CHECKING:
    from cl_forge.core.types import RawFormat

    from ..parsing.shape import ResponseShape
    from ..specs.base import IndicatorSpec
    from ..types import CmfTransport


class BaseRawResource:
    def __init__(self, transport: CmfTransport) -> None:
        self._transport = transport

    def _get(self, path: str, raw: RawFormat = "json") -> dict[str, Any] | str:
        return self._transport.get(path, fmt=raw)

    async def _aget(self, path: str, raw: RawFormat = "json") -> dict[str, Any] | str:
        return await self._transport.aget(path, fmt=raw)


class BaseResource[
    RecordT: BaseModel,
    CollectionT: RootModel[list[BaseModel]]
]:
    def __init__(
            self,
            transport: CmfTransport,
            *,
            spec: IndicatorSpec[RecordT, CollectionT]
    ) -> None:
        self._transport = transport
        self._spec = spec
        self._parser = CmfResponseParser(spec)

    def _get(
            self,
            path: str,
            *,
            shape: ResponseShape,
    ) -> RecordT | CollectionT:
        data = self._transport.get(path)
        return self._parser.parse(data, shape=shape)

    async def _aget(
            self,
            path: str,
            *,
            shape: ResponseShape,
    ) -> RecordT | CollectionT:
        data = await self._transport.aget(path)
        return self._parser.parse(data, shape=shape)


class BaseIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseResource[RecordT, CollectionT]): ...


class BaseRateResource[
    RecordT: InterestRateRecord,
    CollectionT: InterestRateCollection[Any]
](BaseResource[RecordT, CollectionT]): ...
