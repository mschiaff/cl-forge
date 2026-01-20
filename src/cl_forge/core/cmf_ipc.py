from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._rs_cl_forge import _rs_cmf as _cmf  # noqa

type _Format = Literal['json', 'xml']
type _Year = int | None


class IpcRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    value: float = Field(alias="Valor")
    date: datetime = Field(alias="Fecha")

    @field_validator('value', mode='before')
    @classmethod
    def convert_value(cls, v):
        return round(float(v.replace(',', '.')) / 100, 5)

    @field_validator('date', mode='before')
    @classmethod
    def convert_date(cls, v):
        return datetime.strptime(v, '%Y-%m-%d')


@lru_cache
def _current(_client, *,  format: _Format) -> IpcRecord:
    raw = _client.get(path="/ipc", format=format)
    return IpcRecord(**raw['IPCs'][0])

@lru_cache
def _year(_client, *, year: int, format: _Format) -> list[IpcRecord]:
    year = year or datetime.now().year
    raw = _client.get(path=f"/ipc/{year}", format=format)
    return [IpcRecord(**item) for item in raw['IPCs']]


@dataclass(frozen=True)
class Ipc:
    __slots__ = ("_client",)

    def __init__(self, api_key: str) -> None:
        client = _cmf.CmfClient(api_key=api_key)
        object.__setattr__(self, "_client", client)

    def current(self, format: _Format = 'json') -> IpcRecord:
        return _current(self._client, format=format)

    def year(self, year: _Year = None, format: _Format = 'json') -> list[IpcRecord]:
        return _year(self._client, year=year, format=format)