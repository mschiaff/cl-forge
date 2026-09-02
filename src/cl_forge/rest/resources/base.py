from typing import ClassVar

from httpx2 import Request, Response

from cl_forge.rest.client.builder import ClientType
from cl_forge.rest.client.route import ClientRoute
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.formats import FormatPolicy
from cl_forge.rest.resources.types import QueryParams, ResponseFormat, UrlSegment


class BaseResource[SpecT: ResourceSpec]:
    _spec: SpecT
    _format_policy: ClassVar[FormatPolicy]
    _reserved_params: ClassVar[frozenset[str]] = frozenset()

    def __init__(self, route: ClientRoute) -> None:
        self._route = route

    def _validate_params(self, params: QueryParams | None) -> None:
        if params is None:
            return

        reserved = {
            name.casefold()
            for name in self._reserved_params | self._format_policy.reserved_params
        }
        conflicts = sorted(name for name in params if name.casefold() in reserved)

        if conflicts:
            names = ", ".join(conflicts)
            raise ValueError(f"Reserved query parameters: {names}")

    def _build_request(
        self,
        client: ClientType,
        method: str,
        *segments: UrlSegment | None,
        params: QueryParams | None = None,
        fmt: ResponseFormat | None = None,
        endpoint: str | None = None,
    ) -> Request:
        self._validate_params(params)

        target = self._format_policy.prepare(
            endpoint=self._spec.endpoint if endpoint is None else endpoint,
            segments=segments,
            params=params,
            fmt=fmt,
        )

        return client.build_request(
            method,
            target.path,
            params=target.params,
        )


class SyncResource[SpecT: ResourceSpec](BaseResource[SpecT]):
    def _get(
        self,
        *segments: UrlSegment | None,
        params: QueryParams | None = None,
        fmt: ResponseFormat | None = None,
        endpoint: str | None = None,
    ) -> Response:
        client = self._route.client
        request = self._build_request(
            client,
            "GET",
            *segments,
            params=params,
            fmt=fmt,
            endpoint=endpoint,
        )
        response = client.send(request)
        response.raise_for_status()
        return response


class AsyncResource[SpecT: ResourceSpec](BaseResource[SpecT]):
    async def _get(
        self,
        *segments: UrlSegment | None,
        params: QueryParams | None = None,
        fmt: ResponseFormat | None = None,
        endpoint: str | None = None,
    ) -> Response:
        client = self._route.aclient
        request = self._build_request(
            client,
            "GET",
            *segments,
            params=params,
            fmt=fmt,
            endpoint=endpoint,
        )
        response = await client.send(request)
        response.raise_for_status()
        return response
