from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass

from cl_forge.rest.resources.types import QueryParams, ResponseFormat, UrlSegment


@dataclass(slots=True, frozen=True)
class RequestTarget:
    path: str
    params: QueryParams


@dataclass(frozen=True, slots=True)
class FormatPolicy(ABC):
    @property
    @abstractmethod
    def reserved_params(self) -> frozenset[str]: ...

    @abstractmethod
    def prepare(
        self,
        endpoint: str,
        segments: tuple[UrlSegment | None, ...],
        params: QueryParams | None,
        fmt: ResponseFormat | None,
    ) -> RequestTarget: ...

    @staticmethod
    def join_path(endpoint: str, segments: tuple[UrlSegment | None, ...]) -> str:
        parts = tuple(str(segment).strip("/") for segment in segments if segment is not None)
        if not parts:
            return endpoint

        return "/".join((endpoint.rstrip("/"), *parts))


@dataclass(slots=True, frozen=True)
class PathExtensionFormat(FormatPolicy):
    default: ResponseFormat = "json"

    @property
    def reserved_params(self) -> frozenset[str]:
        return frozenset()

    def prepare(
        self,
        endpoint: str,
        segments: tuple[UrlSegment | None, ...],
        params: QueryParams | None,
        fmt: ResponseFormat | None,
    ) -> RequestTarget:
        selected = fmt or self.default
        path = self.join_path(f"{endpoint}.{selected}", segments)
        return RequestTarget(path, dict(params or {}))


@dataclass(frozen=True, slots=True)
class QueryParameterFormat(FormatPolicy):
    parameter: str
    default: ResponseFormat = "json"

    @property
    def reserved_params(self) -> frozenset[str]:
        return frozenset({self.parameter})

    def prepare(
        self,
        endpoint: str,
        segments: tuple[UrlSegment | None, ...],
        params: QueryParams | None,
        fmt: ResponseFormat | None,
    ) -> RequestTarget:
        query = dict(params or {})
        query[self.parameter] = fmt or self.default

        return RequestTarget(
            path=self.join_path(endpoint, segments),
            params=query,
        )


@dataclass(frozen=True, slots=True)
class FixedJsonFormat(FormatPolicy):
    @property
    def reserved_params(self) -> frozenset[str]:
        return frozenset()

    def prepare(
        self,
        endpoint: str,
        segments: tuple[UrlSegment | None, ...],
        params: QueryParams | None,
        fmt: ResponseFormat | None,
    ) -> RequestTarget:
        if fmt not in (None, "json"):
            raise ValueError("This API only supports JSON responses.")

        return RequestTarget(
            path=self.join_path(endpoint, segments),
            params=dict(params or {}),
        )
