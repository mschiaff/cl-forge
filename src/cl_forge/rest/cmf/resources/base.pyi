from typing import Any, Literal, overload

from pydantic import BaseModel, RootModel

from cl_forge.core.types import RawFormat

from ..models.base import (
    IndicatorCollection,
    IndicatorRecord,
    RateCollection,
    RateRecord,
)
from ..parsing.parser import BaseCmfResponseParser
from ..parsing.shape import ResponseShape
from ..specs.base import BaseSpec, IndicatorSpec, RateSpec
from ..types import CmfTransport

class BaseRawResource:
    _transport: CmfTransport

    def __init__(self, transport: CmfTransport) -> None: ...

    @overload
    def _get(self, path: str, raw: Literal["json"] = ...) -> dict[str, Any]: ...
    @overload
    def _get(self, path: str, raw: Literal["xml"]) -> str: ...
    @overload
    def _get(self, path: str, raw: RawFormat = ...) -> dict[str, Any] | str: ...

    @overload
    async def _aget(self, path: str, raw: Literal["json"] = ...) -> dict[str, Any]: ...
    @overload
    async def _aget(self, path: str, raw: Literal["xml"]) -> str: ...
    @overload
    async def _aget(self, path: str, raw: RawFormat = ...) -> dict[str, Any] | str: ...


class BaseResource[
    RecordT: BaseModel,
    CollectionT: RootModel[list[BaseModel]],
    ParserT: BaseCmfResponseParser[BaseModel, RootModel[list[BaseModel]]],
]:
    _transport: CmfTransport
    _spec: BaseSpec[RecordT, CollectionT]
    _parser: BaseCmfResponseParser[RecordT, CollectionT]

    def __init__(self,
            transport: CmfTransport,
            *,
            spec: BaseSpec[RecordT, CollectionT]
    ) -> None: ...

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

    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.SINGLE],
    ) -> RecordT: ...
    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: Literal[ResponseShape.COLLECTION],
    ) -> CollectionT: ...
    @overload
    async def _aget(
            self,
            path: str,
            *,
            shape: ResponseShape,
    ) -> RecordT | CollectionT: ...


class BaseIndicatorResource[
    RecordT: IndicatorRecord,
    CollectionT: IndicatorCollection[Any]
](BaseResource[RecordT, CollectionT]):
    def __init__(
            self,
            transport: CmfTransport,
            *,
            spec: IndicatorSpec[RecordT, CollectionT]
    ) -> None: ...


class BaseRateResource[
    RecordT: RateRecord,
    CollectionT: RateCollection[Any]
](BaseResource[RecordT, CollectionT]):
    def __init__(
            self,
            transport: CmfTransport,
            *,
            spec: RateSpec[RecordT, CollectionT],
    ) -> None: ...
