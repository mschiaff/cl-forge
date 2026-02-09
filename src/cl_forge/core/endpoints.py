from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import TypeVar

from cl_forge.core.impl.rs_cl_forge.rs_cmf import CmfClient
from cl_forge.core.schemas import (
    CmfRecord,
    EuroRecord,
    IpcRecord,
    UfRecord,
    UsdRecord,
    UtmRecord,
)

T = TypeVar("T", bound=CmfRecord)

class CmfEndpoint[T]:
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
        """
        Initialize the endpoint client.

        Parameters
        ----------
        api_key : str
            CMF API key.
        path : str
            Path to the endpoint.
        record_class : type[T]
            Record class for the endpoint.
        root_key : str
            Root key in the API response containing the data.
        """
        client = CmfClient(api_key=api_key)
        object.__setattr__(self, "_client", client)
        object.__setattr__(self, "_path", path)
        object.__setattr__(self, "_record_class", record_class)
        object.__setattr__(self, "_root_key", root_key)

    def current(self) -> T:
        """
        Get the latest available record.
        """
        return self._fetch_current(
            self._client,
            self._path,
            self._record_class,
            self._root_key
        )

    def year(self, year: int | None = None) -> list[T]:
        """
        Get the records for a given year.

        Parameters
        ----------
        year : int | None
        """
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
class IpcEndpoint(CmfEndpoint[IpcRecord]):
    """
    Client for the CMF IPC (Índice de Precios al Consumidor) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        """
        Initialize the IPC endpoint client.

        Parameters
        ----------
        api_key : str
            CMF API key.
        """
        super().__init__(api_key, "/ipc", IpcRecord, "IPCs")

    def current(self) -> IpcRecord:
        """
        Get the latest available IPC value.

        Returns
        -------
        IpcRecord
            The latest IPC record.
        """
        return super().current()

    def year(self, year: int | None = None) -> list[IpcRecord]:
        """
        Get the IPC values for a given year.

        Parameters
        ----------
        year : int | None
            The year for which to retrieve IPC values. If None, defaults to the
            current year.

        Returns
        -------
        list[IpcRecord]
            A list of IPC records for the specified year.
        """
        return super().year(year)


@dataclass(frozen=True)
class UsdEndpoint(CmfEndpoint[UsdRecord]):
    """
    Client for the CMF USD endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/dolar", UsdRecord, "Dolares")


@dataclass(frozen=True)
class EuroEndpoint(CmfEndpoint[EuroRecord]):
    """
    Client for the CMF Euro endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/euro", EuroRecord, "Euros")


@dataclass(frozen=True)
class UfEndpoint(CmfEndpoint[UfRecord]):
    """
    Client for the CMF UF (Unidad de Fomento) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/uf", UfRecord, "UFs")


@dataclass(frozen=True)
class UtmEndpoint(CmfEndpoint[UtmRecord]):
    """
    Client for the CMF UTM (Unidad Tributaria Mensual) endpoints.
    """
    def __init__(self, api_key: str) -> None:
        super().__init__(api_key, "/utm", UtmRecord, "UTMs")