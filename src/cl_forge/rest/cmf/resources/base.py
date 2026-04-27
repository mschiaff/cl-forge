from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.parser import CmfResponseParser

if TYPE_CHECKING:
    from cl_forge.core.types import RawFormat

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

    def _get(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: RawFormat | None = None,
    ) -> RecordT | CollectionT | dict[str, Any] | str:
        if raw:
            return self._transport.get(path, fmt=raw)

        data = self._transport.get(path)
        return self._parser.parse(data, shape=shape)

    async def _aget(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: RawFormat | None = None,
    ) -> RecordT | CollectionT | dict[str, Any] | str:
        if raw:
            return await self._transport.aget(path, fmt=raw)

        data = await self._transport.aget(path)
        return self._parser.parse(data, shape=shape)
