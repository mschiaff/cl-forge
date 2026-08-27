from collections.abc import Generator

import httpx2
from httpx2 import URL, Request, Response

from cl_forge.rest.auth.enums import AuthLocation, AuthScheme
from cl_forge.rest.auth.spec import AuthSpec


class ApiKeyAuth(httpx2.Auth):
    """Apply provider-specific API-key authentication."""

    def __init__(self, spec: AuthSpec, apikey: str) -> None:
        self._spec = spec
        self._apikey = apikey

    def _format_location_query(self, url: URL) -> URL:
        """Format the API key for use in a query parameter."""
        return url.copy_add_param(self._spec.label, self._apikey)

    def _format_location_header(self) -> str:
        """Format the API key for use in an HTTP header."""
        if self._spec.scheme is AuthScheme.NONE:
            return self._apikey
        return f"{self._spec.scheme} {self._apikey}"

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        """Apply API-key authentication to the request based on the provided :class:`AuthSpec`."""
        label = self._spec.label
        location = self._spec.location

        if location is AuthLocation.QUERY:
            request.url = self._format_location_query(request.url)
        elif location is AuthLocation.HEADER:
            request.headers[label] = self._format_location_header()
        else:
            raise ValueError(f"Unsupported auth location: {location}")

        yield request
