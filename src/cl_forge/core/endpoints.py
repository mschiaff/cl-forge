from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import TypeVar

from pydantic import BaseModel

from cl_forge.core.impl.rs_cl_forge.rs_cmf import CmfClient
from cl_forge.core.schemas import EurRecord, IpcRecord, UFRecord, UsdRecord, UTMRecord

T = TypeVar("T", bound=BaseModel)

class CmfEndpoint[T: BaseModel]:
    """
    Base class for CMF API endpoints.
    """
    __slots__ = ("_client", "_path", "_record_class", "_root_key")

    def __init__(
        self,
        api_key: str,
        path: str,
        record_class: type[T],
        root_key: str
    ) -> None:
        client = CmfClient(api_key=api_key)
        object.__setattr__(self, "_client", client)
        object.__setattr__(self, "_path", path)
        object.__setattr__(self, "_record_class", record_class)
        object.__setattr__(self, "_root_key", root_key)

    def current(self) -> T:
        """
        Fetches the current record from the endpoint.

        Returns
        -------
        T
            The current record.
        """
        return self._fetch_current(
            self._client,
            self._path,
            self._record_class,
            self._root_key
        )

    def year(self, year: int | None = None) -> list[T]:
        return self._fetch_year(
            self._client,
            self._path,
            self._record_class,
            self._root_key,
            year
        )

    @staticmethod
    @lru_cache
    def _fetch_current(
        client: CmfClient,
        path: str,
        record_class: type[T],
        root_key: str
    ) -> T:
        raw = client.get(path=path, fmt='json')
        return record_class(**raw[root_key][0])

    @staticmethod
    @lru_cache
    def _fetch_year(
        client: CmfClient,
        path: str,
        record_class: type[T],
        root_key: str,
        year: int | None
    ) -> list[T]:
        year = year or datetime.now().year
        raw = client.get(path=f"{path}/{year}", fmt='json')
        return [record_class(**item) for item in raw[root_key]]


@dataclass(frozen=True)
class Ipc(CmfEndpoint[IpcRecord]):
    """
    Client for the CMF IPC (Índice de Precios al Consumidor) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/ipc", IpcRecord, "IPCs")


@dataclass(frozen=True)
class Usd(CmfEndpoint[UsdRecord]):
    """
    Client for the CMF USD (Dólar Observado) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/dolar", UsdRecord, "Dolares")


@dataclass(frozen=True)
class Eur(CmfEndpoint[EurRecord]):
    """
    Client for the CMF EUR (Euro) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/euro", EurRecord, "Euros")


@dataclass(frozen=True)
class Uf(CmfEndpoint[UFRecord]):
    """
    Client for the CMF UF (Unidad de Fomento) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/uf", UFRecord, "UFs")


@dataclass(frozen=True)
class Utm(CmfEndpoint[UTMRecord]):
    """
    Client for the CMF UTM (Unidad Tributaria Mensual) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/utm", UTMRecord, "UTMs")