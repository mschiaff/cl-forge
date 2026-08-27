import asyncio
import hashlib
from asyncio import AbstractEventLoop
from collections.abc import Callable
from dataclasses import field
from threading import Lock
from typing import ClassVar, Self

from httpx2 import AsyncClient, Client
from pydantic.dataclasses import dataclass

from cl_forge.rest.client.builder import ClientBuilder
from cl_forge.rest.client.config import ClientConfig
from cl_forge.rest.provider import ProviderSpec


@dataclass(frozen=True, slots=True)
class ClientKey:
    provider: ProviderSpec
    config: ClientConfig
    fingerprint: bytes = field(repr=False)

    @classmethod
    def create(cls, provider: ProviderSpec, config: ClientConfig, apikey: str) -> Self:
        fingerprint = hashlib.sha256(apikey.encode()).digest()
        return cls(provider, config, fingerprint)


@dataclass(frozen=True, slots=True)
class SyncClientKey(ClientKey): ...


@dataclass(config={"arbitrary_types_allowed": True}, frozen=True, slots=True)
class AsyncClientKey(ClientKey):
    loop: AbstractEventLoop = field(default_factory=asyncio.get_running_loop, repr=False)


class ClientRegistry:
    """Process-wide store for lazily created HTTP clients."""

    sync_clients: ClassVar[dict[SyncClientKey, Client]] = {}
    async_clients: ClassVar[dict[AsyncClientKey, AsyncClient]] = {}

    builder: ClassVar[type[ClientBuilder]] = ClientBuilder
    _lock: ClassVar[Lock] = Lock()

    @classmethod
    def _get_or_create[KeyT, ClientT: (Client, AsyncClient)](
        cls,
        registry: dict[KeyT, ClientT],
        key: KeyT,
        builder: Callable[[], ClientT],
    ) -> ClientT:
        """
        Retrieve an existing client from the registry or create a new one
        if it doesn't exist or is closed.
        """
        with cls._lock:
            client = registry.get(key)
            if client is None or client.is_closed:
                client = builder()
                registry[key] = client
            return client

    @classmethod
    def get_sync(cls, provider: ProviderSpec, config: ClientConfig, apikey: str) -> Client:
        """Get or create a synchronous HTTP client for the specified provider."""
        _args = (provider, config, apikey)
        key = SyncClientKey.create(*_args)
        builder = cls.builder(*_args).create_sync
        return cls._get_or_create(
            key=key,
            builder=builder,
            registry=cls.sync_clients,
        )

    @classmethod
    def get_async(cls, provider: ProviderSpec, config: ClientConfig, apikey: str) -> AsyncClient:
        """Get or create an asynchronous HTTP client for the specified provider."""
        _args = (provider, config, apikey)
        key = AsyncClientKey.create(*_args)
        builder = cls.builder(*_args).create_async
        return cls._get_or_create(
            key=key,
            builder=builder,
            registry=cls.async_clients,
        )
