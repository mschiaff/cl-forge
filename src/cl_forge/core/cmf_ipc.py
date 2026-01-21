from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ._rs_cl_forge import _rs_cmf as _cmf  # noqa

BadStatus: Exception = _cmf.BadStatus


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
def _current(
        _client,
        *,
        fmt: Literal['xml', 'json'] = 'json'
) -> IpcRecord:
    """
    Retrieves the IPC record for the current year.

    Parameters
    ----------
    _client : CmfClient
    fmt : Literal['xml', 'json']

    Returns
    -------
    IpcRecord
        IPC record for the current year.
    """
    raw = _client.get(path="/ipc", format=fmt)
    return IpcRecord(**raw['IPCs'][0])

@lru_cache
def _year(
        _client,
        *,
        year: int | None,
        fmt: Literal['xml', 'json'] = 'json'
) -> list[IpcRecord]:
    """
    Retrieves the IPC records for a specific year.

    Parameters
    ----------
    _client : CmfClient
    year : int | None
    fmt : Literal['xml', 'json']

    Returns
    -------
    list[IpcRecord]
        IPC records for the specified year.
    """
    year = year or datetime.now().year
    raw = _client.get(path=f"/ipc/{year}", format=fmt)
    return [IpcRecord(**item) for item in raw['IPCs']]


@dataclass(frozen=True)
class Ipc:
    """
    Client for the CMF IPC (Índice de Precios al Consumidor) endpoints.
    """
    __slots__ = ("_client",)

    def __init__(self, api_key: str) -> None:
        """
        Initializes the IPC client with the provided API key.

        Parameters
        ----------
        api_key : str
            The API key for authenticating with the CMF API.
        """
        client = _cmf.CmfClient(api_key=api_key)
        object.__setattr__(self, "_client", client)

    def current(
            self,
            fmt: Literal['xml', 'json'] = 'json'
    ) -> IpcRecord:
        """
        Retrieves the lastest available IPC record.

        Parameters
        ----------
        fmt : Literal['json', 'xml']
            The format of the response. Must be lower case 'json' or 'xml'.
            Defaults to 'json'.

        Returns
        -------
        IpcRecord
            The latest IPC record.
        """
        return _current(self._client, fmt=fmt)

    def year(
            self,
            year: int | None = None,
            fmt: Literal['xml', 'json'] = 'json'
    ) -> list[IpcRecord]:
        """
        Retrieves the IPC records for a specific year.

        Parameters
        ----------
        year : int | None
            The year for which to retrieve IPC records. If None, defaults to
            the current year.
        fmt : Literal['xml', 'json']
            The format of the response. Must be lower case 'json' or 'xml'.

        Returns
        -------
        list[IpcRecord]
            A list of IPC records for the specified year.

        Raises
        ------
        BadStatus
            If there's no data available for the specified year.
        """
        return _year(self._client, year=year, fmt=fmt)