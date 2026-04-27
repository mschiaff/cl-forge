from typing import Any, Literal, overload

from cl_forge.core.types import RawFormat

from ..models.base import IndicatorCollection, IndicatorRecord
from ..parsing.parser import CmfResponseParser
from ..parsing.shape import ResponseShape
from ..specs.base import IndicatorSpec
from ..types import CmfTransport

class BaseIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
]:
    _transport: CmfTransport
    _spec: IndicatorSpec[RecordT, CollectionT]
    _parser: CmfResponseParser[RecordT, CollectionT]

    def __init__(
            self,
            transport: CmfTransport,
            *,
            spec: IndicatorSpec[RecordT, CollectionT]
    ) -> None: ...

    @overload
    def _get(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.SINGLE],
            raw: None = ...,
    ) -> RecordT: ...
    @overload
    def _get(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.COLLECTION],
            raw: None = ...,
    ) -> CollectionT: ...
    @overload
    def _get(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    def _get(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    def _get(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: RawFormat | None = ...,
    ) -> RecordT | CollectionT | dict[str, Any] | str: ...

    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.SINGLE],
            raw: None = ...,
    ) -> RecordT: ...
    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.COLLECTION],
            raw: None = ...,
    ) -> CollectionT: ...
    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: Literal["json"],
    ) -> dict[str, Any]: ...
    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: Literal["xml"],
    ) -> str: ...
    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: ResponseShape,
            raw: RawFormat | None = ...,
    ) -> RecordT | CollectionT | dict[str, Any] | str: ...
