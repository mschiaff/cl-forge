from cl_forge.rest.resources.base import BaseResource
from cl_forge.rest.resources.config import ResourceSpec
from cl_forge.rest.resources.types import QueryParams


class MarketResource[SpecT: ResourceSpec](BaseResource[SpecT]):
    """Common behavior for Mercado Publico resources."""

    _reserved_params = frozenset({"ticket"})

    def _validate_params(self, params: QueryParams | None) -> None:
        """Reject auth parameters even when callers vary case or whitespace."""
        if params is None:
            return

        reserved = {
            name.casefold() for name in self._reserved_params | self._format_policy.reserved_params
        }
        conflicts = sorted(name for name in params if name.strip().casefold() in reserved)
        if conflicts:
            names = ", ".join(conflicts)
            raise ValueError(f"Reserved query parameters: {names}")
