from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, RootModel

from cl_forge.rest.cmf.specs.base import BaseSpec
from cl_forge.rest.cmf.types import CmfTransport

from ..models.base import (
    IndicatorCollection,
    IndicatorRecord,
    RateCollection,
    RateRecord,
)
from ..parsing.parser import BaseCmfResponseParser, IndicatorResponseParser, RateResponseParser

if TYPE_CHECKING:
    from cl_forge.rest.cmf.types import RawFormat

    from ..parsing.shape import ResponseShape
    from ..specs.base import BaseSpec, IndicatorSpec, RateSpec
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
            spec: BaseSpec[RecordT, CollectionT],
            parser: type[BaseCmfResponseParser[RecordT, CollectionT]]
    ) -> None:
        self._transport = transport
        self._spec = spec
        self._parser = parser(spec)

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
](BaseResource[RecordT, CollectionT]):
    def __init__(
            self,
            transport: CmfTransport,
            *,
            spec: IndicatorSpec[RecordT, CollectionT]
    ) -> None:
        super().__init__(transport, spec=spec, parser=IndicatorResponseParser)


class BaseRateResource[
    RecordT: RateRecord,
    CollectionT: RateCollection[Any]
](BaseResource[RecordT, CollectionT]):
    def __init__(
            self,
            transport: CmfTransport,
            *,
            spec: RateSpec[RecordT, CollectionT],
    ) -> None:
        super().__init__(transport, spec=spec, parser=RateResponseParser)
