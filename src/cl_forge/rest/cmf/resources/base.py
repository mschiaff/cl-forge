from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, overload

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.parser import CmfResponseParser

if TYPE_CHECKING:
    from ..parsing.shape import ResponseShape
    from ..specs.base import IndicatorSpec
    from ..types import CmfTransport


class BaseIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
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

    @overload
    def _get(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.SINGLE],
    ) -> RecordT: ...
    @overload
    def _get(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.COLLECTION],
    ) -> CollectionT: ...
    @overload
    def _get(
            self,
            path: str,
            *,
            shape: ResponseShape,
    ) -> RecordT | CollectionT: ...

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
