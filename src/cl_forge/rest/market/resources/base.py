from cl_forge.rest.resources.base import BaseResource


class MarketResource(BaseResource):
    _reserved_params = frozenset({"ticket"})
